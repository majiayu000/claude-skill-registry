---
name: deepagents-architecture
description: Guides architectural decisions for Deep Agents applications. Use when deciding between Deep Agents vs alternatives, choosing backend strategies, designing subagent systems, or selecting middleware approaches.
---

# Deep Agents Architecture Decisions

## When to Use Deep Agents

### Use Deep Agents When You Need:

- **Long-horizon tasks** - Complex workflows spanning dozens of tool calls
- **Planning capabilities** - Task decomposition before execution
- **Filesystem operations** - Reading, writing, and editing files
- **Subagent delegation** - Isolated task execution with separate context windows
- **Persistent memory** - Long-term storage across conversations
- **Human-in-the-loop** - Approval gates for sensitive operations
- **Context management** - Auto-summarization for long conversations

### Consider Alternatives When:

| Scenario | Alternative | Why |
|----------|-------------|-----|
| Single LLM call | Direct API call | Deep Agents overhead not justified |
| Simple RAG pipeline | LangChain LCEL | Simpler abstraction |
| Custom graph control flow | LangGraph directly | More flexibility |
| No file operations needed | `create_react_agent` | Lighter weight |
| Stateless tool use | Function calling | No middleware needed |

## Backend Selection

### Backend Comparison

| Backend | Persistence | Use Case | Requires |
|---------|-------------|----------|----------|
| `StateBackend` | Ephemeral (per-thread) | Working files, temp data | Nothing (default) |
| `FilesystemBackend` | Disk | Local development, real files | `root_dir` path |
| `StoreBackend` | Cross-thread | User preferences, knowledge bases | LangGraph `store` |
| `CompositeBackend` | Mixed | Hybrid memory patterns | Multiple backends |

### Backend Decision Tree

```
Need real disk access?
├─ Yes → FilesystemBackend(root_dir="/path")
└─ No
   └─ Need persistence across conversations?
      ├─ Yes → Need mixed ephemeral + persistent?
      │  ├─ Yes → CompositeBackend
      │  └─ No → StoreBackend
      └─ No → StateBackend (default)
```

### CompositeBackend Routing

Route different paths to different storage backends:

```python
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

agent = create_deep_agent(
    backend=CompositeBackend(
        default=StateBackend(),  # Working files (ephemeral)
        routes={
            "/memories/": StoreBackend(store=store),    # Persistent
            "/preferences/": StoreBackend(store=store), # Persistent
        },
    ),
)
```

## Subagent Architecture

### When to Use Subagents

**Use subagents when:**
- Task is complex, multi-step, and can run independently
- Task requires heavy context that would bloat the main thread
- Multiple independent tasks can run in parallel
- You need isolated execution (sandboxing)
- You only care about the final result, not intermediate steps

**Don't use subagents when:**
- Task is trivial (few tool calls)
- You need to see intermediate reasoning
- Splitting adds latency without benefit
- Task depends on main thread state mid-execution

### Subagent Patterns

#### Pattern 1: Parallel Research
```
         ┌─────────────┐
         │  Orchestrator│
         └──────┬──────┘
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌──────┐  ┌──────┐  ┌──────┐
│Task A│  │Task B│  │Task C│
└──┬───┘  └──┬───┘  └──┬───┘
   └──────────┼──────────┘
              ▼
      ┌─────────────┐
      │  Synthesize │
      └─────────────┘
```

Best for: Research on multiple topics, parallel analysis, batch processing.

#### Pattern 2: Specialized Agents
```python
research_agent = {
    "name": "researcher",
    "description": "Deep research on complex topics",
    "system_prompt": "You are an expert researcher...",
    "tools": [web_search, document_reader],
}

coder_agent = {
    "name": "coder",
    "description": "Write and review code",
    "system_prompt": "You are an expert programmer...",
    "tools": [code_executor, linter],
}

agent = create_deep_agent(subagents=[research_agent, coder_agent])
```

Best for: Domain-specific expertise, different tool sets per task type.

#### Pattern 3: Pre-compiled Subagents
```python
from deepagents import CompiledSubAgent, create_deep_agent

# Use existing LangGraph graph as subagent
custom_graph = create_react_agent(model=..., tools=...)

agent = create_deep_agent(
    subagents=[CompiledSubAgent(
        name="custom-workflow",
        description="Runs specialized workflow",
        runnable=custom_graph
    )]
)
```

Best for: Reusing existing LangGraph graphs, complex custom workflows.

## Middleware Architecture

### Built-in Middleware Stack

Deep Agents applies middleware in this order:

1. **TodoListMiddleware** - Task planning with `write_todos`/`read_todos`
2. **FilesystemMiddleware** - File ops: `ls`, `read_file`, `write_file`, `edit_file`, `glob`, `grep`, `execute`
3. **SubAgentMiddleware** - Delegation via `task` tool
4. **SummarizationMiddleware** - Auto-summarizes at ~85% context or 170k tokens
5. **AnthropicPromptCachingMiddleware** - Caches system prompts (Anthropic only)
6. **PatchToolCallsMiddleware** - Fixes dangling tool calls from interruptions
7. **HumanInTheLoopMiddleware** - Pauses for approval (if `interrupt_on` configured)

### Custom Middleware Placement

```python
from langchain.agents.middleware import AgentMiddleware

class MyMiddleware(AgentMiddleware):
    tools = [my_custom_tool]

    def transform_request(self, request):
        # Modify system prompt, inject context
        return request

    def transform_response(self, response):
        # Post-process, log, filter
        return response

# Custom middleware added AFTER built-in stack
agent = create_deep_agent(middleware=[MyMiddleware()])
```

### Middleware vs Tools Decision

| Need | Use Middleware | Use Tools |
|------|----------------|-----------|
| Inject system prompt content | ✅ | ❌ |
| Add tools dynamically | ✅ | ❌ |
| Transform requests/responses | ✅ | ❌ |
| Standalone capability | ❌ | ✅ |
| User-invokable action | ❌ | ✅ |

### Subagent Middleware Inheritance

Subagents receive their own middleware stack by default:
- TodoListMiddleware
- FilesystemMiddleware (shared backend)
- SummarizationMiddleware
- AnthropicPromptCachingMiddleware
- PatchToolCallsMiddleware

Override with `default_middleware=[]` in SubAgentMiddleware or per-subagent `middleware` key.

## Gates: architecture decisions before implementation

Complete **in order**. A step **passes** only when the stated artifact exists in the design note, ADR stub, or ticket; internal intent alone does not count.

1. **Fit** - Confirm Deep Agents vs alternatives (see tables above).
   - **Pass:** Short written rationale that either names one matching "Use Deep Agents When You Need" bullet **or** one "Consider Alternatives" row plus the chosen alternative.

2. **Backend** - Match the Backend Decision Tree to a concrete choice.
   - **Pass:** Backend name(s) from the Backend Comparison table; if `FilesystemBackend` or `CompositeBackend`, `root_dir` and any route prefixes are written down (path placeholders OK).

3. **Subagents** - Decide delegation boundaries.
   - **Pass:** Either "no subagents" plus one sentence why **or** a named list where each subagent maps to at least one "When to Use Subagents" reason; parallel plans state what merges outputs.

4. **Human-in-the-loop** - Approval surface.
   - **Pass:** Explicit list of tools/operations that use `interrupt_on`, **or** "no HITL" plus one-line risk acceptance.

5. **Middleware** - Custom vs built-in only.
   - **Pass:** Either "custom middleware: none" **or** each custom piece named, placed after the built-in stack, and tied to prompt injection, tools, or request/response transforms.

6. **Context** - Long threads and large inputs.
   - **Pass:** Stated plan for default summarization behavior (~85% context / ~170k tokens) or an alternative cap; large files handled via references/chunking or equivalent, named in text.

7. **Checkpointing** - Resume and durability.
   - **Pass:** Checkpoint/checkpointer approach named for the graph **or** "none" with one-line rationale (e.g. ephemeral demo only).
