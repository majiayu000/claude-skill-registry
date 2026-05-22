---
name: building-langgraph-agents
description: LangGraph development for stateful multi-agent applications, cyclic workflows, conditional routing, human-in-the-loop patterns, and persistent state management. Use for complex AI orchestration, agent coordination, and production-grade agentic systems.
---

# LangGraph Development Skill

## Quick Reference

LangGraph is LangChain's framework for building stateful, multi-actor applications with LLMs. It enables cyclic graphs, conditional branching, persistent state management, and human-in-the-loop workflows.

**Key capabilities**: StateGraph for workflow orchestration, checkpointers for persistence, prebuilt ReAct agents, streaming at multiple granularities, and LangGraph Platform for managed deployment.

---

## Table of Contents

1. [When to Use](#when-to-use)
2. [Package Ecosystem](#package-ecosystem)
3. [Quick Start - Python](#quick-start---python)
4. [Quick Start - TypeScript](#quick-start---typescript)
5. [Core Concepts](#core-concepts)
6. [Prebuilt Components](#prebuilt-components)
7. [Common Patterns](#common-patterns)
8. [Quick Persistence Setup](#quick-persistence-setup)
9. [CLI Commands](#cli-commands)
10. [Error Quick Reference](#error-quick-reference)
11. [When to Use REFERENCE.md](#when-to-use-referencemd)
12. [Agent Integration](#agent-integration)
13. [See Also](#see-also)

---

## When to Use

This skill is loaded by `backend-developer` when:
- `langgraph` in `requirements.txt`, `pyproject.toml`, or `setup.py`
- `@langchain/langgraph` in `package.json` dependencies
- Python imports: `from langgraph.graph import StateGraph`
- Environment variables `LANGSMITH_API_KEY`, `LANGGRAPH_API_URL`, or `LANGCHAIN_API_KEY` present
- User mentions "LangGraph", "StateGraph", "agent workflow", "cyclic agent", or "multi-agent graph"

---

## Package Ecosystem

| Package | Description |
|---------|-------------|
| `langgraph` | Core StateGraph, MessageGraph, prebuilt components |
| `langgraph-checkpoint-postgres` | PostgreSQL checkpointer for production |
| `langgraph-checkpoint-sqlite` | SQLite checkpointer with async support |
| `langgraph-sdk` | Python client for LangGraph Platform API |
| `@langchain/langgraph` | TypeScript/JavaScript implementation |

**Compatibility**: LangGraph 0.2.x requires `langchain-core>=0.3.0`.

---

## Quick Start - Python

```python
"""LangGraph Quick Start - Python"""
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 1. Define state schema
class State(TypedDict):
    messages: list[str]
    count: int

# 2. Define node functions
def process(state: State) -> dict:
    """Process node - increments counter."""
    return {"count": state["count"] + 1}

def respond(state: State) -> dict:
    """Response node - adds message to state."""
    return {"messages": state["messages"] + [f"Processed {state['count']} times"]}

# 3. Build graph
graph = StateGraph(State)
graph.add_node("process", process)
graph.add_node("respond", respond)

graph.add_edge(START, "process")
graph.add_edge("process", "respond")
graph.add_edge("respond", END)

# 4. Compile and run
app = graph.compile()
result = app.invoke({"messages": [], "count": 0})
# {'messages': ['Processed 1 times'], 'count': 1}
```

### With LLM and Tools

```python
"""LangGraph with ChatOpenAI and tools."""
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: 72F, sunny"

llm = ChatOpenAI(model="gpt-4o")
tools = [get_weather]
llm_with_tools = llm.bind_tools(tools)

def agent(state: MessagesState) -> dict:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

graph = StateGraph(MessagesState)
graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

app = graph.compile()
result = app.invoke({"messages": [("user", "What's the weather in NYC?")]})
```

---

## Quick Start - TypeScript

```typescript
import { StateGraph, START, END, Annotation } from "@langchain/langgraph";

const State = Annotation.Root({
  messages: Annotation<string[]>({
    default: () => [],
    reducer: (curr, update) => [...curr, ...update],
  }),
  count: Annotation<number>({ default: () => 0 }),
});

const process = (state: typeof State.State) => ({
  count: state.count + 1,
});

const respond = (state: typeof State.State) => ({
  messages: [`Processed ${state.count} times`],
});

const graph = new StateGraph(State)
  .addNode("process", process)
  .addNode("respond", respond)
  .addEdge(START, "process")
  .addEdge("process", "respond")
  .addEdge("respond", END);

const app = graph.compile();
const result = await app.invoke({ messages: [], count: 0 });
```

---

## Core Concepts

### StateGraph

The core abstraction - a directed graph where nodes read and write to shared state.

```python
from langgraph.graph import StateGraph

graph = StateGraph(State)  # State is a TypedDict
```

### State Schema

Defines the shape of data flowing through the graph.

```python
from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]  # With reducer
    context: str                              # Simple overwrite
```

### Nodes

Functions that receive state and return partial updates.

```python
def my_node(state: State) -> dict:
    return {"context": f"{state['context']} - processed"}
```

### Edges

Connections between nodes - unconditional or conditional.

```python
# Unconditional
graph.add_edge("node_a", "node_b")

# Conditional
graph.add_conditional_edges("router", routing_function)
```

### Special Nodes

| Node | Purpose |
|------|---------|
| `START` | Entry point of the graph |
| `END` | Terminal node, execution stops |

---

## Prebuilt Components

| Component | Import | Purpose |
|-----------|--------|---------|
| `create_react_agent` | `langgraph.prebuilt` | Full ReAct agent with tool loop |
| `ToolNode` | `langgraph.prebuilt` | Execute tools from AI messages |
| `tools_condition` | `langgraph.prebuilt` | Route: tools called vs end |
| `MessagesState` | `langgraph.graph` | Prebuilt chat state schema |

### create_react_agent

```python
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"

llm = ChatOpenAI(model="gpt-4o")
agent = create_react_agent(llm, [search])
result = agent.invoke({"messages": [("user", "Search for LangGraph")]})
```

---

## Common Patterns

### Linear Pipeline

```python
graph.add_edge(START, "extract")
graph.add_edge("extract", "transform")
graph.add_edge("transform", "load")
graph.add_edge("load", END)
```

### Conditional Routing

```python
def router(state: State) -> str:
    if state["intent"] == "search":
        return "search_node"
    return "default_node"

graph.add_conditional_edges("classifier", router)
```

### Cycle with Exit

```python
def check_done(state):
    return END if state["done"] else "process"

graph.add_edge(START, "process")
graph.add_edge("process", "check")
graph.add_conditional_edges("check", check_done)
```

---

## Quick Persistence Setup

```python
from langgraph.checkpoint.memory import MemorySaver

# Development - in-memory (lost on restart)
memory = MemorySaver()
app = graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke({"messages": [("user", "Hi")]}, config)
```

For production persistence, see **REFERENCE.md** for PostgreSQL/SQLite setup.

---

## CLI Commands

```bash
# Install
pip install langgraph langgraph-checkpoint-postgres

# Verify
python -c "import langgraph; print(langgraph.__version__)"

# LangGraph Platform
langgraph init      # Initialize project
langgraph dev       # Start dev server
langgraph build     # Build for deployment
langgraph up        # Deploy with Docker
```

### Environment Variables

```bash
export LANGSMITH_API_KEY="ls-..."
export LANGCHAIN_TRACING_V2="true"
export OPENAI_API_KEY="sk-..."
```

---

## Error Quick Reference

| Error | Solution |
|-------|----------|
| `InvalidUpdateError` | Node returned keys not in state schema |
| `GraphRecursionError` | Add exit condition or increase `recursion_limit` |
| `ValueError: Checkpointer required` | Add checkpointer to `compile()` for thread ops |

---

## When to Use REFERENCE.md

Load **REFERENCE.md** for:
- Full checkpointer setup (PostgreSQL, SQLite, async)
- Human-in-the-loop patterns with interrupts
- Multi-agent patterns (supervisor, hierarchical)
- Streaming modes and event handling
- Subgraph composition
- Production deployment with LangGraph Platform
- Tool integration patterns
- Time travel debugging
- Best practices and anti-patterns

---

## Agent Integration

| Agent | Use Case |
|-------|----------|
| `backend-developer` | Graph implementation, state design |
| `deep-debugger` | Execution issues, state bugs |
| `tech-lead-orchestrator` | Multi-agent architecture |
| `code-reviewer` | Graph logic review |

---

## See Also

- [REFERENCE.md](./REFERENCE.md) - Full patterns and advanced usage
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [LangSmith](https://smith.langchain.com/)

---

**Progressive Disclosure**: Start here for quick implementation. Load REFERENCE.md for comprehensive patterns, production setup, and advanced features.
