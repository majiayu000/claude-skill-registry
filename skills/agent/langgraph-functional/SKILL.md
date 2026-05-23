---
name: langgraph-functional
description: LangGraph Functional API with @entrypoint and @task decorators. Use when building workflows with the modern LangGraph pattern, enabling parallel execution, persistence, and human-in-the-loop.
context: fork
agent: workflow-architect
version: 1.0.0
author: SkillForge
user-invocable: false
---
# LangGraph Functional API
Build workflows using decorators instead of explicit graph construction.

## Overview

- Sequential workflows with conditional branching
- Orchestrator-worker patterns with parallel execution
- Workflows needing persistence and checkpointing
- Human-in-the-loop approval flows
- Simpler alternative to explicit StateGraph construction

## Core Concepts

### Graph API vs Functional API
```
Graph API (explicit):           Functional API (implicit):
StateGraph → add_node →        @task functions +
add_edge → compile              @entrypoint orchestration
```

**When to Use Functional API**:
- Sequential workflows with conditional logic
- Orchestrator-worker patterns
- Simpler debugging (regular Python functions)
- Parallel task execution

## Quick Start

### Basic Pattern
```python
from langgraph.func import entrypoint, task

@task
def step_one(data: str) -> str:
    """Task returns a future - call .result() to block"""
    return process(data)

@task
def step_two(result: str) -> str:
    return transform(result)

@entrypoint()
def my_workflow(input_data: str) -> str:
    # Tasks return futures - enables parallel execution
    result1 = step_one(input_data).result()
    result2 = step_two(result1).result()
    return result2

# Invoke
output = my_workflow.invoke("hello")
```

### Key Rules
1. **@task** functions return futures - call `.result()` to get value
2. **@entrypoint** is the workflow entry point - orchestrates tasks
3. Tasks inside entrypoint are tracked for persistence/streaming
4. Regular functions (no decorator) execute normally

## Parallel Execution

### Fan-Out Pattern
```python
@task
def fetch_source_a(query: str) -> dict:
    return api_a.search(query)

@task
def fetch_source_b(query: str) -> dict:
    return api_b.search(query)

@task
def merge_results(results: list[dict]) -> dict:
    return {"combined": results}

@entrypoint()
def parallel_search(query: str) -> dict:
    # Launch in parallel - futures start immediately
    future_a = fetch_source_a(query)
    future_b = fetch_source_b(query)

    # Block on both results
    results = [future_a.result(), future_b.result()]

    return merge_results(results).result()
```

### Map Over Collection
```python
@task
def process_item(item: dict) -> dict:
    return transform(item)

@entrypoint()
def batch_workflow(items: list[dict]) -> list[dict]:
    # Launch all in parallel
    futures = [process_item(item) for item in items]

    # Collect results
    return [f.result() for f in futures]
```

## Persistence & Checkpointing

### Enable Checkpointing
```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

@entrypoint(checkpointer=checkpointer)
def resumable_workflow(data: str) -> str:
    # Workflow state is automatically saved after each task
    result = expensive_task(data).result()
    return result

# Use thread_id for persistence
config = {"configurable": {"thread_id": "session-123"}}
result = resumable_workflow.invoke("input", config)
```

### Access Previous State
```python
from typing import Optional

@entrypoint(checkpointer=checkpointer)
def stateful_workflow(data: str, previous: Optional[dict] = None) -> dict:
    """previous contains last return value for this thread_id"""

    if previous and previous.get("step") == "complete":
        return previous  # Already done

    result = process(data).result()
    return {"step": "complete", "result": result}
```

## Human-in-the-Loop

### Interrupt for Approval
```python
from langgraph.types import interrupt, Command

@entrypoint(checkpointer=checkpointer)
def approval_workflow(request: dict) -> dict:
    # Process request
    result = analyze_request(request).result()

    # Pause for human approval
    approved = interrupt({
        "question": "Approve this action?",
        "details": result
    })

    if approved:
        return execute_action(result).result()
    else:
        return {"status": "rejected"}

# Initial run - pauses at interrupt
config = {"configurable": {"thread_id": "approval-1"}}
for chunk in approval_workflow.stream(request, config):
    print(chunk)

# Resume after human review
for chunk in approval_workflow.stream(Command(resume=True), config):
    print(chunk)
```

## Conditional Logic

### Branching
```python
@task
def classify(text: str) -> str:
    return llm.invoke(f"Classify: {text}")  # "positive" or "negative"

@task
def handle_positive(text: str) -> str:
    return "Thank you for the positive feedback!"

@task
def handle_negative(text: str) -> str:
    return "We're sorry to hear that. Creating support ticket..."

@entrypoint()
def feedback_workflow(text: str) -> str:
    sentiment = classify(text).result()

    if sentiment == "positive":
        return handle_positive(text).result()
    else:
        return handle_negative(text).result()
```

### Loop Until Done
```python
@task
def call_llm(messages: list) -> dict:
    return llm_with_tools.invoke(messages)

@task
def call_tool(tool_call: dict) -> str:
    tool = tools[tool_call["name"]]
    return tool.invoke(tool_call["args"])

@entrypoint()
def agent_loop(query: str) -> str:
    messages = [{"role": "user", "content": query}]

    while True:
        response = call_llm(messages).result()

        if not response.get("tool_calls"):
            return response["content"]

        # Execute tools in parallel
        tool_futures = [call_tool(tc) for tc in response["tool_calls"]]
        tool_results = [f.result() for f in tool_futures]

        messages.extend([response, *tool_results])
```

## Streaming

### Stream Updates
```python
@entrypoint()
def streaming_workflow(data: str) -> str:
    step1 = task_one(data).result()
    step2 = task_two(step1).result()
    return step2

# Stream task completion updates
for update in streaming_workflow.stream("input", stream_mode="updates"):
    print(f"Task completed: {update}")
```

### Stream Modes
```python
# "updates" - task completion events
for chunk in workflow.stream(input, stream_mode="updates"):
    print(chunk)

# "values" - full state after each task
for chunk in workflow.stream(input, stream_mode="values"):
    print(chunk)

# "custom" - custom events from your code
for chunk in workflow.stream(input, stream_mode="custom"):
    print(chunk)
```

## TypeScript

### Basic Pattern
```typescript
import { entrypoint, task, MemorySaver } from "@langchain/langgraph";

const processData = task("processData", async (data: string) => {
  return await transform(data);
});

const workflow = entrypoint(
  { name: "myWorkflow", checkpointer: new MemorySaver() },
  async (input: string) => {
    const result = await processData(input);
    return result;
  }
);

// Invoke
const config = { configurable: { thread_id: "session-1" } };
const result = await workflow.invoke("hello", config);
```

### Parallel Execution
```typescript
const fetchA = task("fetchA", async (q: string) => api.fetchA(q));
const fetchB = task("fetchB", async (q: string) => api.fetchB(q));

const parallelWorkflow = entrypoint("parallel", async (query: string) => {
  // Launch in parallel using Promise.all
  const [resultA, resultB] = await Promise.all([
    fetchA(query),
    fetchB(query)
  ]);
  return { a: resultA, b: resultB };
});
```

## Common Patterns

### Orchestrator-Worker
```python
@task
def plan(topic: str) -> list[str]:
    """Orchestrator creates work items"""
    sections = planner.invoke(f"Create outline for: {topic}")
    return sections

@task
def write_section(section: str) -> str:
    """Worker processes one item"""
    return llm.invoke(f"Write section: {section}")

@task
def synthesize(sections: list[str]) -> str:
    """Combine results"""
    return "\n\n".join(sections)

@entrypoint()
def report_workflow(topic: str) -> str:
    sections = plan(topic).result()

    # Fan-out to workers
    section_futures = [write_section(s) for s in sections]
    completed = [f.result() for f in section_futures]

    # Fan-in
    return synthesize(completed).result()
```

### Retry Pattern
```python
@task
def unreliable_api(data: str) -> dict:
    return external_api.call(data)

@entrypoint()
def retry_workflow(data: str, max_retries: int = 3) -> dict:
    for attempt in range(max_retries):
        try:
            return unreliable_api(data).result()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            continue
```

## Anti-Patterns

1. **Forgetting .result()**: Tasks return futures, must call `.result()`
2. **Blocking in tasks**: Keep tasks focused, don't nest entrypoints
3. **Missing checkpointer**: Without it, can't resume interrupted workflows
4. **Sequential when parallel**: Launch tasks before blocking on results

## Migration from Graph API

```python
# Graph API (before)
from langgraph.graph import StateGraph

def node_a(state): return {"data": process(state["input"])}
def node_b(state): return {"result": transform(state["data"])}

graph = StateGraph(State)
graph.add_node("a", node_a)
graph.add_node("b", node_b)
graph.add_edge("a", "b")
app = graph.compile()

# Functional API (after)
@task
def process_data(input: str) -> str:
    return process(input)

@task
def transform_data(data: str) -> str:
    return transform(data)

@entrypoint()
def workflow(input: str) -> str:
    data = process_data(input).result()
    return transform_data(data).result()
```

## Related Skills

- `langgraph-state` - State management patterns for complex workflow data
- `langgraph-routing` - Conditional routing and branching decisions
- `langgraph-parallel` - Advanced parallel execution and fan-out patterns
- `langgraph-checkpoints` - Persistence and recovery for long-running workflows

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| API Style | Functional over Graph | Simpler debugging, familiar Python patterns, implicit graph construction |
| Task Returns | Futures with .result() | Enables parallel execution without explicit async/await |
| Checkpointing | Optional per-entrypoint | Flexibility for stateless vs. resumable workflows |
| Human-in-Loop | interrupt() function | Clean pause/resume semantics with Command pattern |

## Resources
- LangGraph Functional API: https://langchain-ai.github.io/langgraph/concepts/functional_api/
- Workflows Tutorial: https://langchain-ai.github.io/langgraph/tutorials/workflows/