---
name: agentic-design
description: "Use when building AI agent systems. Covers agent loops, tool calling, planning patterns, memory systems, multi-agent coordination, and safety guardrails. Apply when creating autonomous AI workflows, coding assistants, or task automation systems."
---

# Agentic Design

## Core Principle

Agents are LLMs in a loop with tools. Design for reliability, observability, and graceful failure—not just capability.

## When to Use This Skill

- Building AI assistants with tool use
- Creating autonomous task executors
- Designing multi-agent systems
- Implementing coding agents
- Building workflow automation
- Adding planning capabilities to AI

## The Iron Law

**AGENTS FAIL SILENTLY. BUILD FOR OBSERVABILITY.**

If you can't see what your agent is doing, you can't fix it when it breaks.

## Why Agentic Systems?

**Benefits:**
- Automate complex multi-step tasks
- Handle dynamic, open-ended problems
- Scale human expertise
- 24/7 autonomous operation
- Adaptable to new situations

**Challenges:**
- Unpredictable behavior
- Error propagation
- Cost accumulation
- Safety concerns
- Debugging complexity

## Agent Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    AGENT LOOP                        │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  Observe │───▶│  Think   │───▶│   Act    │      │
│  └──────────┘    └──────────┘    └──────────┘      │
│       ▲                               │             │
│       │         ┌──────────┐          │             │
│       └─────────│  Memory  │◀─────────┘             │
│                 └──────────┘                        │
│                      │                              │
│              ┌───────┴───────┐                      │
│              ▼               ▼                      │
│        ┌──────────┐   ┌──────────┐                 │
│        │  Tools   │   │ Knowledge│                 │
│        └──────────┘   └──────────┘                 │
└─────────────────────────────────────────────────────┘
```

## Pattern 1: ReAct (Reasoning + Acting)

The foundational agent pattern: Think → Act → Observe → Repeat.

### Basic ReAct Loop

```python
def react_agent(task, max_iterations=10):
    """ReAct pattern: Reason, Act, Observe."""
    messages = [
        {"role": "system", "content": REACT_SYSTEM_PROMPT},
        {"role": "user", "content": task}
    ]

    for i in range(max_iterations):
        # Think: Get model's reasoning and action
        response = llm.chat(messages, tools=TOOLS)

        # Check for completion
        if response.stop_reason == "end_turn":
            return extract_final_answer(response)

        # Act: Execute tool calls
        if response.tool_calls:
            for tool_call in response.tool_calls:
                # Execute tool
                result = execute_tool(
                    tool_call.name,
                    tool_call.arguments
                )

                # Observe: Add result to context
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        messages.append({"role": "assistant", "content": response.content})

    return "Max iterations reached"
```

### ReAct System Prompt

```python
REACT_SYSTEM_PROMPT = """You are an AI assistant that solves tasks step by step.

For each step:
1. THINK: Analyze what you know and what you need
2. ACT: Use a tool to gather information or take action
3. OBSERVE: Review the result
4. REPEAT or ANSWER: Continue until you can answer

Always explain your reasoning before acting.
When you have enough information, provide a final answer.

Available tools:
{tool_descriptions}
"""
```

## Pattern 2: Plan-and-Execute

Separate planning from execution for complex tasks.

### Planner-Executor Architecture

```python
class PlanAndExecuteAgent:
    def __init__(self, planner_llm, executor_llm, tools):
        self.planner = planner_llm
        self.executor = executor_llm
        self.tools = tools

    def run(self, task):
        # Phase 1: Create plan
        plan = self.create_plan(task)

        # Phase 2: Execute steps
        results = []
        for step in plan.steps:
            result = self.execute_step(step, results)
            results.append(result)

            # Replan if needed
            if result.needs_replanning:
                plan = self.replan(task, plan, results)

        # Phase 3: Synthesize
        return self.synthesize(task, results)

    def create_plan(self, task):
        """Generate step-by-step plan."""
        response = self.planner.chat([{
            "role": "user",
            "content": f"""Create a plan to accomplish this task:
            {task}

            Return a numbered list of steps.
            Each step should be specific and actionable.
            Consider dependencies between steps."""
        }])

        return parse_plan(response.content)

    def execute_step(self, step, previous_results):
        """Execute a single step with access to tools."""
        context = format_previous_results(previous_results)

        return react_agent(
            f"Previous context:\n{context}\n\nExecute this step:\n{step}",
            tools=self.tools
        )

    def replan(self, task, current_plan, results):
        """Adapt plan based on execution results."""
        response = self.planner.chat([{
            "role": "user",
            "content": f"""Original task: {task}

            Original plan: {current_plan}

            Results so far: {results}

            The plan needs adjustment. Create a revised plan
            for the remaining work."""
        }])

        return parse_plan(response.content)
```

## Pattern 3: Tool Use

### Tool Definition (OpenAI Format)

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results (default 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to read"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    }
]
```

### Tool Execution with Safety

```python
class ToolExecutor:
    def __init__(self, tools, sandbox=True):
        self.tools = {t["function"]["name"]: t for t in tools}
        self.sandbox = sandbox
        self.execution_log = []

    def execute(self, tool_name, arguments):
        """Execute tool with safety checks."""
        # Validate tool exists
        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}"}

        # Log execution
        self.execution_log.append({
            "tool": tool_name,
            "arguments": arguments,
            "timestamp": datetime.now()
        })

        # Safety checks
        if self.sandbox:
            if tool_name == "write_file":
                if not self._is_safe_path(arguments.get("path")):
                    return {"error": "Path outside sandbox"}

            if tool_name == "execute_code":
                arguments = self._sandbox_code(arguments)

        # Execute
        try:
            handler = getattr(self, f"_tool_{tool_name}")
            result = handler(**arguments)
            return {"success": True, "result": result}
        except Exception as e:
            return {"error": str(e)}

    def _is_safe_path(self, path):
        """Check if path is within allowed directories."""
        allowed_dirs = ["/tmp", "./workspace"]
        return any(path.startswith(d) for d in allowed_dirs)

    def _tool_search_web(self, query, num_results=5):
        """Web search implementation."""
        # Implementation here
        pass

    def _tool_read_file(self, path):
        """File read implementation."""
        with open(path) as f:
            return f.read()

    def _tool_write_file(self, path, content):
        """File write implementation."""
        with open(path, 'w') as f:
            f.write(content)
        return f"Written {len(content)} bytes to {path}"
```

## Pattern 4: Memory Systems

### Short-Term Memory (Conversation)

```python
class ConversationMemory:
    def __init__(self, max_tokens=4000):
        self.messages = []
        self.max_tokens = max_tokens

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
        self._trim_if_needed()

    def _trim_if_needed(self):
        """Keep memory within token limits."""
        while self._count_tokens() > self.max_tokens:
            # Keep system message, remove oldest
            if len(self.messages) > 1:
                self.messages.pop(1)

    def get_context(self):
        return self.messages.copy()
```

### Long-Term Memory (Vector Store)

```python
class LongTermMemory:
    def __init__(self, vector_store):
        self.store = vector_store

    def remember(self, content, metadata=None):
        """Store information for later retrieval."""
        self.store.add(
            content=content,
            metadata={
                "timestamp": datetime.now().isoformat(),
                **(metadata or {})
            }
        )

    def recall(self, query, k=5):
        """Retrieve relevant memories."""
        return self.store.search(query, k=k)

    def summarize_and_store(self, conversation):
        """Compress conversation into memorable facts."""
        summary = llm.chat([{
            "role": "user",
            "content": f"""Extract key facts and decisions from this conversation:
            {conversation}

            Return as bullet points."""
        }])

        self.remember(
            content=summary.content,
            metadata={"type": "conversation_summary"}
        )
```

### Working Memory (Scratchpad)

```python
class WorkingMemory:
    def __init__(self):
        self.scratchpad = {}
        self.current_task = None
        self.subtasks = []

    def set_task(self, task):
        self.current_task = task
        self.subtasks = []

    def note(self, key, value):
        """Store intermediate result."""
        self.scratchpad[key] = value

    def get(self, key):
        return self.scratchpad.get(key)

    def get_context(self):
        """Format working memory for prompt."""
        return f"""Current Task: {self.current_task}

Subtasks: {self.subtasks}

Notes:
{json.dumps(self.scratchpad, indent=2)}
"""
```

## Pattern 5: Multi-Agent Systems

### Hierarchical Agents

```python
class OrchestratorAgent:
    """Coordinates specialist agents."""

    def __init__(self):
        self.agents = {
            "researcher": ResearchAgent(),
            "coder": CodingAgent(),
            "reviewer": ReviewAgent(),
        }

    def run(self, task):
        # Analyze task and delegate
        plan = self.plan_delegation(task)

        results = {}
        for step in plan:
            agent_name = step["agent"]
            subtask = step["task"]

            # Delegate to specialist
            result = self.agents[agent_name].run(
                subtask,
                context=results
            )
            results[step["id"]] = result

            # Quality check
            if step.get("needs_review"):
                review = self.agents["reviewer"].run(
                    f"Review this output:\n{result}"
                )
                if not review.approved:
                    # Retry with feedback
                    result = self.agents[agent_name].run(
                        subtask,
                        feedback=review.feedback
                    )

        return self.synthesize(results)
```

### Collaborative Agents

```python
class CollaborativeSystem:
    """Agents that discuss and reach consensus."""

    def __init__(self, agents):
        self.agents = agents

    def debate(self, topic, rounds=3):
        """Have agents debate a topic."""
        discussion = []

        for round in range(rounds):
            for agent in self.agents:
                response = agent.respond(
                    topic=topic,
                    discussion_so_far=discussion
                )
                discussion.append({
                    "agent": agent.name,
                    "response": response
                })

        return self.synthesize_consensus(discussion)

    def divide_and_conquer(self, task):
        """Split task among agents."""
        # Decompose task
        subtasks = self.decompose(task)

        # Parallel execution
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(agent.run, subtask): agent
                for agent, subtask in zip(self.agents, subtasks)
            }

            results = {}
            for future in as_completed(futures):
                agent = futures[future]
                results[agent.name] = future.result()

        return self.merge_results(results)
```

## Pattern 6: Guardrails and Safety

### Input Validation

```python
class InputGuardrail:
    def __init__(self):
        self.blocked_patterns = [
            r"ignore.*instructions",
            r"pretend.*you.*are",
            r"jailbreak",
        ]

    def validate(self, user_input):
        """Check input for prompt injection."""
        # Pattern matching
        for pattern in self.blocked_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return False, "Blocked pattern detected"

        # Length check
        if len(user_input) > 10000:
            return False, "Input too long"

        # LLM-based check for sophisticated attacks
        is_safe = self.llm_safety_check(user_input)
        if not is_safe:
            return False, "Potential prompt injection"

        return True, None
```

### Output Validation

```python
class OutputGuardrail:
    def __init__(self):
        self.validators = [
            self.check_pii,
            self.check_harmful_content,
            self.check_code_safety,
        ]

    def validate(self, output, context):
        """Validate agent output before returning."""
        for validator in self.validators:
            is_valid, reason = validator(output, context)
            if not is_valid:
                return self.sanitize(output, reason)

        return output

    def check_pii(self, output, context):
        """Check for leaked PII."""
        pii_patterns = {
            'ssn': r'\d{3}-\d{2}-\d{4}',
            'credit_card': r'\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}',
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        }

        for pii_type, pattern in pii_patterns.items():
            if re.search(pattern, output):
                return False, f"Contains {pii_type}"

        return True, None

    def check_code_safety(self, output, context):
        """Check generated code for dangerous patterns."""
        dangerous = [
            'rm -rf',
            'DROP TABLE',
            'exec(',
            'eval(',
            'os.system',
        ]

        for pattern in dangerous:
            if pattern in output:
                return False, f"Dangerous code pattern: {pattern}"

        return True, None
```

### Action Limits

```python
class ActionLimiter:
    def __init__(self):
        self.limits = {
            'api_calls': 100,
            'file_writes': 10,
            'cost_usd': 5.0,
        }
        self.counts = defaultdict(int)
        self.cost = 0.0

    def check(self, action_type, cost=0):
        """Check if action is within limits."""
        self.counts[action_type] += 1
        self.cost += cost

        if self.counts[action_type] > self.limits.get(action_type, float('inf')):
            raise LimitExceeded(f"{action_type} limit reached")

        if self.cost > self.limits['cost_usd']:
            raise LimitExceeded(f"Cost limit reached: ${self.cost:.2f}")

    def require_approval(self, action):
        """Flag dangerous actions for human approval."""
        dangerous_actions = ['delete_file', 'send_email', 'deploy']

        if action in dangerous_actions:
            return self.request_human_approval(action)

        return True
```

## Pattern 7: Error Handling and Recovery

```python
class ResilientAgent:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def run_with_recovery(self, task):
        """Execute with automatic error recovery."""
        errors = []

        for attempt in range(self.max_retries):
            try:
                result = self.execute(task)

                # Validate result
                if self.validate_result(result):
                    return result

                errors.append(f"Invalid result: {result}")

            except ToolExecutionError as e:
                errors.append(f"Tool error: {e}")
                # Try alternative approach
                task = self.reframe_task(task, e)

            except RateLimitError as e:
                # Exponential backoff
                wait_time = 2 ** attempt
                time.sleep(wait_time)

            except Exception as e:
                errors.append(f"Unexpected error: {e}")

        # All retries failed
        return self.graceful_failure(task, errors)

    def reframe_task(self, task, error):
        """Adjust task based on error."""
        return f"""Previous attempt failed with: {error}

Try a different approach for: {task}"""

    def graceful_failure(self, task, errors):
        """Return partial results or helpful error."""
        return {
            "status": "failed",
            "task": task,
            "errors": errors,
            "partial_results": self.get_partial_results(),
            "suggestions": self.suggest_manual_steps(task)
        }
```

## Observability

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

class ObservableAgent:
    def __init__(self, name):
        self.name = name
        self.trace_id = None

    def run(self, task):
        self.trace_id = generate_trace_id()

        with logger.bind(
            agent=self.name,
            trace_id=self.trace_id,
            task=task[:100]
        ):
            logger.info("agent_started")

            try:
                result = self._execute(task)
                logger.info("agent_completed", result_length=len(str(result)))
                return result

            except Exception as e:
                logger.error("agent_failed", error=str(e))
                raise

    def _log_tool_call(self, tool_name, args, result):
        logger.info(
            "tool_called",
            tool=tool_name,
            args=args,
            result_preview=str(result)[:200]
        )

    def _log_llm_call(self, messages, response, tokens, cost):
        logger.info(
            "llm_called",
            message_count=len(messages),
            response_length=len(response),
            tokens=tokens,
            cost_usd=cost
        )
```

### Tracing with LangSmith/Phoenix

```python
from langsmith import traceable

@traceable(name="agent_run")
def run_agent(task):
    """Full agent run with tracing."""
    plan = create_plan(task)

    for step in plan:
        result = execute_step(step)

    return synthesize_results()

@traceable(name="tool_execution")
def execute_tool(name, args):
    """Traced tool execution."""
    return tool_registry[name](**args)
```

## Testing Agents

### Unit Testing Tools

```python
def test_search_tool():
    """Test individual tool."""
    result = tools.search_web("test query")

    assert "results" in result
    assert len(result["results"]) > 0

def test_tool_error_handling():
    """Test tool handles errors gracefully."""
    result = tools.read_file("/nonexistent/path")

    assert "error" in result
    assert "not found" in result["error"].lower()
```

### Integration Testing

```python
def test_agent_simple_task():
    """Test agent on known task."""
    agent = create_agent()

    result = agent.run("What is 2 + 2?")

    assert "4" in result

def test_agent_tool_use():
    """Test agent uses tools correctly."""
    agent = create_agent()

    result = agent.run("Search for the current weather in NYC")

    assert agent.tool_calls_made > 0
    assert "weather" in result.lower()
```

### Evaluation Datasets

```python
EVAL_DATASET = [
    {
        "task": "Find the capital of France",
        "expected_tools": ["search_web"],
        "expected_answer_contains": ["Paris"],
    },
    {
        "task": "Create a file called test.txt with 'hello'",
        "expected_tools": ["write_file"],
        "expected_side_effects": [("file_exists", "test.txt")],
    },
]

def evaluate_agent(agent, dataset):
    """Evaluate agent on test dataset."""
    results = []

    for case in dataset:
        result = agent.run(case["task"])

        score = {
            "task": case["task"],
            "tools_correct": check_tools(agent.tool_calls, case["expected_tools"]),
            "answer_correct": check_answer(result, case.get("expected_answer_contains", [])),
            "side_effects_correct": check_side_effects(case.get("expected_side_effects", [])),
        }
        results.append(score)

    return calculate_metrics(results)
```

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| No iteration limit | Infinite loops, cost explosion | Set max_iterations |
| Missing error handling | Silent failures | Wrap tool calls in try/except |
| No observability | Can't debug issues | Add structured logging |
| Overly complex tools | LLM confusion | Keep tools focused |
| No output validation | Harmful/wrong outputs | Add guardrails |
| Single LLM for all | Suboptimal cost/quality | Use appropriate model per task |

## Integration with Skills

**Use with:**
- `rag-architecture` - RAG as a retrieval tool
- `llm-integration` - API patterns and error handling
- `subagent-driven-development` - Coordinating agent tasks
- `test-driven-development` - Testing agent behavior

## Checklist

Before deploying an agent:
- [ ] Clear task boundaries defined
- [ ] Tools are well-documented
- [ ] Input validation in place
- [ ] Output guardrails active
- [ ] Action limits configured
- [ ] Error recovery implemented
- [ ] Logging and tracing enabled
- [ ] Cost monitoring active
- [ ] Human escalation path defined
- [ ] Evaluation suite passing

## Authority

**Based on:**
- Anthropic agent design patterns
- OpenAI function calling best practices
- LangChain agent architectures
- Academic research on LLM agents
- Production systems at scale

---

**Bottom Line**: Agents = LLM + Tools + Loop. Design for failure, log everything, limit actions, validate outputs. Capability without safety is a liability.
