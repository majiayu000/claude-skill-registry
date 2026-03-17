---
name: mastering-langgraph
description: Build stateful AI agents and agentic workflows with LangGraph in Python. Covers tool-using agents with LLM-tool loops, branching workflows, conversation memory, human-in-the-loop oversight, and production monitoring. Use when - (1) building agents that use tools and loop until task complete, (2) creating multi-step workflows with conditional branches, (3) adding persistence/memory across turns with checkpointers, (4) implementing human approval with interrupt(), (5) debugging via time-travel or LangSmith. Covers StateGraph, nodes, edges, add_conditional_edges, MessagesState, thread_id, Command objects, and ToolMessage handling. Examples include chatbots, calculator agents, and structured workflows.
license: MIT
metadata:
  version: 1.0.0
  framework: LangGraph
  python: ">=3.9"
---

# LangGraph Development Guide

Build stateful AI agents and workflows by defining graphs of nodes (steps) connected by edges (transitions).

## Contents

- [Quick Start](#quick-start)
- [Common Build Scenarios](#common-build-scenarios)
- [Core Principles](#core-principles)
- [Development Workflow](#development-workflow)
- [Common Pitfalls](#common-pitfalls)
- [Environment Setup](#environment-setup)
- [Quick Verification](#quick-verification)
- [API Essentials](#api-essentials)
- [Next Steps](#next-steps)

## Quick Start

Minimal chatbot with memory:

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AnyMessage
from typing_extensions import TypedDict, Annotated
import operator

# 1. Define state
class State(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]  # Append mode

# 2. Define node
llm = ChatOpenAI(model="gpt-4")

def chat(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build graph
graph = StateGraph(State)
graph.add_node("chat", chat)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# 4. Compile with memory
chain = graph.compile(checkpointer=InMemorySaver())

# 5. Invoke with thread_id for persistence
result = chain.invoke(
    {"messages": [HumanMessage(content="Hello!")]},
    config={"configurable": {"thread_id": "user-123"}}
)
print(result["messages"][-1].content)
```

Key patterns:
- `Annotated[list, operator.add]` — append to list instead of replace
- `InMemorySaver()` — enables memory across invocations
- `thread_id` — identifies conversation for persistence

## Common Build Scenarios

### Simple Chatbot / Q&A
The Quick Start above covers this. Add more nodes for preprocessing or postprocessing as needed.

### Tool-Using Agent
Agent that calls external tools (APIs, calculators, search) in a loop until task complete.
→ See [references/tool-agent-pattern.md](references/tool-agent-pattern.md)

### Structured Workflow
Multi-step pipeline with conditional branches, parallel execution, or prompt chaining.
→ See [references/workflow-patterns.md](references/workflow-patterns.md)

### Agent with Long-Term Memory
Persist conversation across sessions, enable time-travel debugging, survive crashes.
→ See [references/persistence-memory.md](references/persistence-memory.md)

### Human-in-the-Loop
Pause for human approval, correction, or additional input mid-workflow.
→ See [references/hitl-patterns.md](references/hitl-patterns.md)

### Debugging / Production Monitoring
Unit test nodes, visualize graphs, trace with LangSmith.
→ See [references/debugging-monitoring.md](references/debugging-monitoring.md)

### Multi-Agent Systems
Build supervisor or swarm-based multi-agent workflows with handoff tools.
→ See [references/multi-agent-patterns.md](references/multi-agent-patterns.md)

### Production Deployment
Deploy to LangGraph Platform (cloud/self-hosted) or custom infrastructure.
→ See [references/production-deployment.md](references/production-deployment.md)

### New to LangGraph?
Learn core concepts: State, Nodes, Edges, Graph APIs.
→ See [references/core-api.md](references/core-api.md)

## Core Principles

### 1. Keep State Raw
Store facts, not formatted prompts. Each node can format data as needed.

```python
# ✓ Good: raw data
class State(TypedDict):
    user_question: str
    retrieved_docs: list[str]
    intent: str

# ✗ Bad: pre-formatted
class State(TypedDict):
    full_prompt: str  # Mixes data with formatting
```

### 2. Single-Purpose Nodes
Each node does one thing. Name it descriptively.

```python
# ✓ Good: clear responsibilities
graph.add_node("classify_intent", classify_intent)
graph.add_node("search_knowledge", search_knowledge)
graph.add_node("generate_response", generate_response)
```

### 3. Explicit Routing
Use conditional edges for decisions. Don't hide routing logic inside nodes.

```python
def route_by_intent(state) -> str:
    if state["intent"] == "billing":
        return "billing_handler"
    return "general_handler"

graph.add_conditional_edges("classify", route_by_intent, 
    ["billing_handler", "general_handler"])
```

### 4. Use Aggregators for Lists
Any list field that accumulates values needs `operator.add`:

```python
class State(TypedDict):
    messages: Annotated[list, operator.add]      # ✓ Appends
    current_step: str                             # Replaces (no annotation)
```

### 5. Handle Errors Deliberately

| Error Type | Strategy |
|------------|----------|
| Transient (network) | Use `RetryPolicy` on node |
| LLM-recoverable (parse fail) | Feed error to LLM via state, loop back |
| User-fixable (missing info) | Use `interrupt()` to pause and ask |
| Unexpected (bugs) | Let bubble up for debugging |

## Development Workflow

1. **Define Steps** — Break task into discrete operations (each becomes a node)
2. **Categorize Steps** — LLM call? Data retrieval? Action? User input?
3. **Design State** — TypedDict with all needed fields; keep it raw
4. **Implement Nodes** — `def node(state) -> dict` for each step
5. **Connect Graph** — `add_node()`, `add_edge()`, `add_conditional_edges()`
6. **Compile & Test** — `graph.compile()`, test with sample inputs

## Common Pitfalls

### 1. Forgetting `operator.add` on Lists
**Symptom:** Messages disappear, only last message retained.
```python
# ✗ Wrong: messages: list[AnyMessage]
# ✓ Fix: messages: Annotated[list[AnyMessage], operator.add]
```

### 2. Missing `thread_id` for Memory
**Symptom:** Agent forgets previous turns.
```python
# ✓ Fix: Always pass config with thread_id
chain.invoke(input, config={"configurable": {"thread_id": "unique-id"}})
```

### 3. Not Compiling Before Invoke
**Symptom:** AttributeError on graph object.
```python
# ✗ Wrong: graph.invoke(input)
# ✓ Fix: chain = graph.compile(); chain.invoke(input)
```

### 4. Non-Deterministic Nodes Without @task
**Symptom:** Different results on resume from checkpoint.
```python
from langgraph.func import task

@task  # Wrap for durable execution
def fetch_data(state):
    return {"data": requests.get(url).json()}
```

### 5. Circular Imports with Type Hints
**Symptom:** ImportError when defining state classes.
```python
# ✓ Fix: Use string annotations
from __future__ import annotations
```

## Environment Setup

```bash
# Core
pip install -U langgraph

# LLM providers (pick one or more)
pip install langchain-openai
pip install langchain-anthropic

# Production persistence
pip install langgraph-checkpoint-postgres

# Observability
pip install langsmith
```

Environment variables:
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export LANGSMITH_API_KEY="ls-..."
export LANGSMITH_TRACING=true
```

## Quick Verification

### Before Building
- [ ] `python -c "import langgraph; print(langgraph.__version__)"` works
- [ ] LLM API key set (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`)
- [ ] Optional: `LANGSMITH_API_KEY` for tracing

### After Building
- [ ] Graph compiles without error: `chain = graph.compile()`
- [ ] Visualization renders: `print(chain.get_graph().draw_mermaid())`
- [ ] Invoke succeeds with sample input: `chain.invoke({...})`
- [ ] Lists accumulate correctly (verify `operator.add` annotations)
- [ ] Memory persists across invocations (test same `thread_id` twice)
- [ ] Conditional routing works as expected (test each branch)

## API Essentials

```python
# Imports
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import TypedDict, Annotated
import operator

# State with append-mode list
class State(TypedDict):
    messages: Annotated[list, operator.add]

# Node signature
def node(state: State) -> dict:
    return {"messages": [new_message]}

# Graph construction
graph = StateGraph(State)
graph.add_node("name", node_fn)
graph.add_edge(START, "name")
graph.add_edge("name", END)

# Conditional routing
graph.add_conditional_edges("from", router_fn, ["option1", "option2", END])

# Compile and run
chain = graph.compile(checkpointer=InMemorySaver())
result = chain.invoke(input, config={"configurable": {"thread_id": "id"}})

# Visualization
print(chain.get_graph().draw_mermaid())
```

For detailed API reference → See [references/core-api.md](references/core-api.md)

## Next Steps

- **Tool agents**: [references/tool-agent-pattern.md](references/tool-agent-pattern.md)
- **Workflows**: [references/workflow-patterns.md](references/workflow-patterns.md)
- **Persistence**: [references/persistence-memory.md](references/persistence-memory.md)
- **Human-in-the-loop**: [references/hitl-patterns.md](references/hitl-patterns.md)
- **Testing/Monitoring**: [references/debugging-monitoring.md](references/debugging-monitoring.md)
- **Multi-agent**: [references/multi-agent-patterns.md](references/multi-agent-patterns.md)
- **Production**: [references/production-deployment.md](references/production-deployment.md)
- **Core concepts**: [references/core-api.md](references/core-api.md)
- **Official docs**: [references/official-resources.md](references/official-resources.md)
