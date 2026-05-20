---
name: deepagents-code-review
description: Reviews Deep Agents code for bugs, anti-patterns, and improvements. Use when reviewing code that uses create_deep_agent, backends, subagents, middleware, or human-in-the-loop patterns. Catches common configuration and usage mistakes.
---

# Deep Agents Code Review

When reviewing Deep Agents code, check for these categories of issues.

## Critical Issues

### 1. Missing Checkpointer with interrupt_on

```python
# BAD - interrupt_on without checkpointer
agent = create_deep_agent(
    tools=[send_email],
    interrupt_on={"send_email": True},
    # No checkpointer! Interrupts will fail
)

# GOOD - checkpointer required for interrupts
from langgraph.checkpoint.memory import InMemorySaver

agent = create_deep_agent(
    tools=[send_email],
    interrupt_on={"send_email": True},
    checkpointer=InMemorySaver(),
)
```

### 2. Missing Store with StoreBackend

```python
# BAD - StoreBackend without store
from deepagents.backends import StoreBackend

agent = create_deep_agent(
    backend=lambda rt: StoreBackend(rt),
    # No store! Will raise ValueError at runtime
)

# GOOD - provide store
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
agent = create_deep_agent(
    backend=lambda rt: StoreBackend(rt),
    store=store,
)
```

### 3. Missing thread_id with Checkpointer

```python
# BAD - no thread_id when using checkpointer
agent = create_deep_agent(checkpointer=InMemorySaver())
agent.invoke({"messages": [...]})  # Error!

# GOOD - always provide thread_id
config = {"configurable": {"thread_id": "user-123"}}
agent.invoke({"messages": [...]}, config)
```

### 4. Relative Paths in Filesystem Tools

```python
# BAD - relative paths not supported
read_file(path="src/main.py")
read_file(path="./config.json")

# GOOD - absolute paths required
read_file(path="/workspace/src/main.py")
read_file(path="/config.json")
```

### 5. Windows Paths in Virtual Filesystem

```python
# BAD - Windows paths rejected
read_file(path="C:\\Users\\file.txt")
write_file(path="D:/projects/code.py", content="...")

# GOOD - Unix-style virtual paths
read_file(path="/workspace/file.txt")
write_file(path="/projects/code.py", content="...")
```

## Backend Issues

### 6. StateBackend Expecting Persistence

```python
# BAD - expecting files to persist across threads
agent = create_deep_agent()  # Uses StateBackend by default

# Thread 1
agent.invoke({"messages": [...]}, {"configurable": {"thread_id": "a"}})
# Agent writes to /data/report.txt

# Thread 2 - file won't exist!
agent.invoke({"messages": [...]}, {"configurable": {"thread_id": "b"}})
# Agent tries to read /data/report.txt - NOT FOUND

# GOOD - use StoreBackend or CompositeBackend for cross-thread persistence
agent = create_deep_agent(
    backend=CompositeBackend(
        default=StateBackend(),
        routes={"/data/": StoreBackend(store=store)},
    ),
    store=store,
)
```

### 7. FilesystemBackend Without root_dir Restriction

```python
# BAD - unrestricted filesystem access
agent = create_deep_agent(
    backend=FilesystemBackend(root_dir="/"),  # Full system access!
)

# GOOD - scope to project directory
agent = create_deep_agent(
    backend=FilesystemBackend(root_dir="/home/user/project"),
)
```

### 8. CompositeBackend Route Order Confusion

```python
# BAD - shorter prefix shadows longer prefix
agent = create_deep_agent(
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/mem/": backend_a,        # This catches /mem/long-term/ too!
            "/mem/long-term/": backend_b,  # Never reached
        },
    ),
)

# GOOD - CompositeBackend sorts by length automatically
# But be explicit about your intent:
agent = create_deep_agent(
    backend=CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": persistent_backend,
            "/workspace/": ephemeral_backend,
        },
    ),
)
```

### 9. Expecting execute Tool Without SandboxBackend

```python
# BAD - execute tool won't work with StateBackend
agent = create_deep_agent()  # Default StateBackend
# Agent calls execute("ls -la") → Error: not supported

# GOOD - use FilesystemBackend for shell execution
agent = create_deep_agent(
    backend=FilesystemBackend(root_dir="/project"),
)
# Agent calls execute("ls -la") → Works
```

## Subagent Issues

### 10. Subagent Missing Required Fields

```python
# BAD - missing required fields
agent = create_deep_agent(
    subagents=[{
        "name": "helper",
        # Missing: description, system_prompt, tools
    }]
)

# GOOD - all required fields present
agent = create_deep_agent(
    subagents=[{
        "name": "helper",
        "description": "General helper for misc tasks",
        "system_prompt": "You are a helpful assistant.",
        "tools": [],  # Can be empty but must be present
    }]
)
```

### 11. Subagent Name Collision

```python
# BAD - duplicate subagent names
agent = create_deep_agent(
    subagents=[
        {"name": "research", "description": "A", ...},
        {"name": "research", "description": "B", ...},  # Collision!
    ]
)

# GOOD - unique names
agent = create_deep_agent(
    subagents=[
        {"name": "web-research", "description": "Web-based research", ...},
        {"name": "doc-research", "description": "Document research", ...},
    ]
)
```

### 12. Overusing Subagents for Simple Tasks

```python
# BAD - subagent overhead for trivial task
# In system prompt or agent behavior:
"Use the task tool to check the current time"
"Delegate file reading to a subagent"

# GOOD - use subagents for complex, isolated work
"Use the task tool for multi-step research that requires many searches"
"Delegate the full analysis workflow to a subagent"
```

### 13. CompiledSubAgent Without Proper State

```python
# BAD - subgraph with incompatible state schema
from langgraph.graph import StateGraph

class CustomState(TypedDict):
    custom_field: str  # No messages field!

sub_builder = StateGraph(CustomState)
# ... build graph
subgraph = sub_builder.compile()

agent = create_deep_agent(
    subagents=[CompiledSubAgent(
        name="custom",
        description="Custom workflow",
        runnable=subgraph,  # State mismatch!
    )]
)

# GOOD - ensure compatible state or use message-based interface
class CompatibleState(TypedDict):
    messages: Annotated[list, add_messages]
    custom_field: str
```

## Middleware Issues

### 14. Middleware Order Misunderstanding

```python
# BAD - expecting custom middleware to run first
class PreProcessMiddleware(AgentMiddleware):
    def transform_request(self, request):
        # Expecting this runs before built-in middleware
        return request

agent = create_deep_agent(middleware=[PreProcessMiddleware()])
# Actually runs AFTER TodoList, Filesystem, SubAgent, etc.

# GOOD - understand middleware runs after built-in stack
# Built-in order:
# 1. TodoListMiddleware
# 2. FilesystemMiddleware
# 3. SubAgentMiddleware
# 4. SummarizationMiddleware
# 5. AnthropicPromptCachingMiddleware
# 6. PatchToolCallsMiddleware
# 7. YOUR MIDDLEWARE HERE
# 8. HumanInTheLoopMiddleware (if interrupt_on set)
```

### 15. Middleware Mutating Request/Response

```python
# BAD - mutating instead of returning new object
class BadMiddleware(AgentMiddleware):
    def transform_request(self, request):
        request.messages.append(extra_message)  # Mutation!
        return request

# GOOD - return modified copy
class GoodMiddleware(AgentMiddleware):
    def transform_request(self, request):
        return ModelRequest(
            messages=[*request.messages, extra_message],
            **other_fields
        )
```

### 16. Middleware Tools Without Descriptions

```python
# BAD - tool without docstring
@tool
def my_tool(arg: str) -> str:
    return process(arg)

class MyMiddleware(AgentMiddleware):
    tools = [my_tool]  # LLM won't know how to use it!

# GOOD - descriptive docstring
@tool
def my_tool(arg: str) -> str:
    """Process the input string and return formatted result.

    Args:
        arg: The string to process

    Returns:
        Formatted result string
    """
    return process(arg)
```

## System Prompt Issues

### 17. Duplicating Built-in Tool Instructions

```python
# BAD - re-explaining what middleware already covers
agent = create_deep_agent(
    system_prompt="""You have access to these tools:
    - write_todos: Create task lists
    - read_file: Read files from the filesystem
    - task: Delegate to subagents

    When using files, always use absolute paths..."""
)
# This duplicates what FilesystemMiddleware and TodoListMiddleware inject!

# GOOD - focus on domain-specific guidance
agent = create_deep_agent(
    system_prompt="""You are a code review assistant.

    Workflow:
    1. Read the files to review
    2. Create a todo list of issues found
    3. Delegate deep analysis to subagents if needed
    4. Compile findings into a report"""
)
```

### 18. Contradicting Built-in Instructions

```python
# BAD - contradicting default behavior
agent = create_deep_agent(
    system_prompt="""Never use the task tool.
    Always process everything in the main thread.
    Don't use todos, just remember everything."""
)
# Fighting against the framework!

# GOOD - work with the framework
agent = create_deep_agent(
    system_prompt="""For simple tasks, handle directly.
    For complex multi-step research, use subagents.
    Track progress with todos for tasks with 3+ steps."""
)
```

### 19. Missing Stopping Criteria

```python
# BAD - no guidance on when to stop
agent = create_deep_agent(
    system_prompt="Research everything about the topic thoroughly."
)
# Agent may run indefinitely!

# GOOD - define completion criteria
agent = create_deep_agent(
    system_prompt="""Research the topic with these constraints:
    - Maximum 5 web searches
    - Stop when you have 3 reliable sources
    - Limit subagent delegations to 2 parallel tasks
    - Summarize findings within 500 words"""
)
```

## Performance Issues

### 20. Not Parallelizing Independent Subagents

```python
# BAD - sequential subagent calls (in agent behavior)
# Agent calls: task(research topic A) → wait → task(research topic B) → wait

# GOOD - parallel subagent calls
# Agent calls in single turn:
#   task(research topic A)
#   task(research topic B)
#   task(research topic C)
# All run concurrently!

# Guide via system prompt:
agent = create_deep_agent(
    system_prompt="""When researching multiple topics,
    launch all research subagents in parallel in a single response."""
)
```

### 21. Large Files in State

```python
# BAD - writing large files to StateBackend
# Agent writes 10MB log file to /output/full_log.txt
# This bloats every checkpoint!

# GOOD - use FilesystemBackend for large files or paginate
agent = create_deep_agent(
    backend=CompositeBackend(
        default=StateBackend(),  # Small files
        routes={
            "/large_files/": FilesystemBackend(root_dir="/tmp/agent"),
        },
    ),
)
```

### 22. InMemorySaver in Production

```python
# BAD - ephemeral checkpointer in production
agent = create_deep_agent(
    checkpointer=InMemorySaver(),  # Lost on restart!
)

# GOOD - persistent checkpointer
from langgraph.checkpoint.postgres import PostgresSaver

agent = create_deep_agent(
    checkpointer=PostgresSaver.from_conn_string(DATABASE_URL),
)
```

### 23. Missing Recursion Awareness

```python
# BAD - no guard against long-running loops
agent = create_deep_agent(
    system_prompt="Keep improving the solution until it's perfect."
)
# May hit recursion limit (default 1000)

# GOOD - explicit iteration limits
agent = create_deep_agent(
    system_prompt="""Improve the solution iteratively:
    - Maximum 3 revision cycles
    - Stop if quality score > 90%
    - Stop if no improvement after 2 iterations"""
)
```

## Code Review Checklist

### Configuration
- [ ] Checkpointer provided if using `interrupt_on`
- [ ] Store provided if using `StoreBackend`
- [ ] Thread ID provided in config when using checkpointer
- [ ] Backend appropriate for use case (ephemeral vs persistent)

### Backends
- [ ] FilesystemBackend scoped to safe `root_dir`
- [ ] StoreBackend has corresponding `store` parameter
- [ ] CompositeBackend routes don't shadow each other unintentionally
- [ ] Not expecting persistence from StateBackend across threads

### Subagents
- [ ] All required fields present (name, description, system_prompt, tools)
- [ ] Unique subagent names
- [ ] CompiledSubAgent has compatible state schema
- [ ] Subagents used for complex tasks, not trivial operations

### Middleware
- [ ] Custom middleware added after built-in stack (expected behavior)
- [ ] Tools have descriptive docstrings
- [ ] Not mutating request/response objects

### System Prompt
- [ ] Not duplicating built-in tool instructions
- [ ] Not contradicting framework defaults
- [ ] Stopping criteria defined for open-ended tasks
- [ ] Parallelization guidance for independent tasks

### Performance
- [ ] Large files routed to appropriate backend
- [ ] Production uses persistent checkpointer
- [ ] Recursion/iteration limits considered
- [ ] Independent subagents parallelized
