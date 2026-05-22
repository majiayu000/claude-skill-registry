---
name: langgraph-python
description: "Design and build AI agents with LangGraph. Use when building ReAct agents, multi-agent systems, workflow orchestration, human-in-the-loop patterns, or state machine workflows."
---

# LangGraph Skill

LangGraph: Framework for stateful, multi-actor AI applications.

**For latest API syntax, use `context7` MCP.**

---

## Core Concepts

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import create_react_agent, ToolNode, tools_condition
from langgraph.types import Command, interrupt, Send
from langgraph.checkpoint.memory import InMemorySaver
```

| Concept | Description |
|---------|-------------|
| **StateGraph** | Graph managing state. Updates after each node |
| **MessagesState** | Built-in state for chat (includes messages list) |
| **Node** | Function: receives state → returns updates |
| **Edge** | Transition: static (`add_edge`) or conditional |
| **Checkpointer** | Persistence for conversation history, pause/resume |
| **Command** | Dynamic routing + state update together |
| **interrupt** | Pause for human-in-the-loop |
| **Send** | Dynamically spawn parallel workers |

---

## Pattern Selection Guide

```
Need to use tools?
├─ Yes → ReAct Agent
└─ No → Workflow patterns

Sequential or parallel?
├─ Sequential → Prompt Chaining
├─ Parallel → Parallelization
└─ Both → Orchestrator-Worker

Different handling by input type?
└─ Yes → Routing

Need output validation?
└─ Yes → Evaluator-Optimizer

Multiple specialized agents?
├─ Central coordinator → Supervisor
├─ Team hierarchy → Hierarchical
└─ Peer collaboration → Network
```

---

## 1. ReAct Agent (Tool-Using)

**Use case**: LLM autonomously decides when to use tools

```
START → LLM → [Tool calls?] → Yes → Tools → LLM (loop)
                            → No  → END
```

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(model, tools=[search, calculator])
result = agent.invoke({"messages": [{"role": "user", "content": "..."}]})
```

**Pitfall**: Agent stuck in loop → add `max_iterations` or explicit stop condition

---

## 2. Prompt Chaining (Sequential)

**Use case**: Step-by-step processing

```
START → Generate → Edit → Review → END
```

```python
builder = StateGraph(State)
builder.add_edge(START, "generate")
builder.add_edge("generate", "edit")
builder.add_edge("edit", "review")
builder.add_edge("review", END)
```

**Pitfall**: Forgetting END edge → graph never terminates

---

## 3. Parallelization

**Use case**: Independent tasks simultaneously

```
START ──┬── Task A ──┐
        ├── Task B ──┼── Aggregate → END
        └── Task C ──┘
```

```python
builder.add_edge(START, "task_a")
builder.add_edge(START, "task_b")
builder.add_edge(START, "task_c")
builder.add_edge(["task_a", "task_b", "task_c"], "aggregate")
```

**Pitfall**: State conflicts → use reducer (e.g., `Annotated[list, operator.add]`)

---

## 4. Routing

**Use case**: Route to handler based on classification

```
START → Classifier → [Route] → Handler A/B/C → END
```

```python
def route_fn(state: State) -> str:
    return state["category"]  # Must match node names exactly

builder.add_conditional_edges("classifier", route_fn, 
    ["handler_a", "handler_b", "handler_c"])
```

**Pitfall**: Route function returns value not in edge map → runtime error

---

## 5. Orchestrator-Worker (Send)

**Use case**: Dynamically create parallel subtasks

```
START → Orchestrator → [Send] → Worker 1..N → Synthesizer → END
```

```python
from langgraph.types import Send

def assign_workers(state: State):
    return [Send("worker", {"task": t}) for t in state["tasks"]]

builder.add_conditional_edges("orchestrator", assign_workers, ["worker"])
```

**Pitfall**: Workers must return same state schema; results need aggregation reducer

---

## 6. Evaluator-Optimizer (Reflection)

**Use case**: Generate → evaluate → improve loop

```
START → Generate → Evaluate → [Pass?] → Yes → END
                                      → No  → Generate
```

```python
def should_continue(state: State) -> str:
    if state["score"] == "pass" or state["iterations"] >= 3:
        return "end"
    return "retry"

builder.add_conditional_edges("evaluate", should_continue, 
    {"retry": "generate", "end": END})
```

**Pitfall**: No max iterations → infinite loop; always add iteration counter

---

## 7. Multi-Agent: Supervisor

**Use case**: Central coordinator delegates to specialists

```
START → Supervisor ←→ Agent A/B/C → END
```

```python
from langgraph.types import Command

def supervisor(state) -> Command[Literal["agent_a", "agent_b", "__end__"]]:
    next_agent = decide_next(state)
    return Command(goto=next_agent)
```

**Pitfall**: Supervisor must explicitly return `__end__` to terminate

---

## 8. Multi-Agent: Hierarchical

**Use case**: Team leads manage sub-teams

```python
from langgraph_supervisor import create_supervisor

research_team = create_supervisor([search_agent, scraper_agent], model=model)
writing_team = create_supervisor([writer_agent, editor_agent], model=model)
top_supervisor = create_supervisor([research_team, writing_team], model=model)
```

**Pitfall**: Deep hierarchies slow down; keep ≤3 levels

---

## 9. Human-in-the-Loop

**Use case**: Human approval, state editing, input requests

```python
from langgraph.types import interrupt, Command

def approval_node(state) -> Command[Literal["proceed", "cancel"]]:
    response = interrupt({"question": "Approve?", "data": state["action"]})
    return Command(goto="proceed" if response["approved"] else "cancel")

# Requires checkpointer
graph = builder.compile(checkpointer=InMemorySaver())
result = graph.invoke(inputs, {"configurable": {"thread_id": "1"}})
# Resume
graph.invoke(Command(resume={"approved": True}), config)
```

**Pitfall**: No checkpointer → interrupt fails; thread_id required for resume

---

## Persistence (Memory)

| Type | Purpose | Implementation |
|------|---------|----------------|
| **Short-term** | Within conversation | `checkpointer` + `thread_id` |
| **Long-term** | Across conversations | `store` |

```python
from langgraph.checkpoint.memory import InMemorySaver  # Dev only
from langgraph.checkpoint.postgres import PostgresSaver  # Production

graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "user-123"}}
```

---

## State Definition

```python
from typing import TypedDict, Annotated
import operator

class State(TypedDict):
    messages: Annotated[list, operator.add]  # Reducer: accumulate
    current_step: str                         # No reducer: overwrite
```

**Pitfall**: Parallel nodes updating same field without reducer → last write wins (data loss)

---

## Common Errors & Fixes

### Graph Never Terminates
**Cause**: Missing edge to END
```python
# ❌ Forgot END
builder.add_edge("final_node", "somewhere")

# ✅ Add END edge
builder.add_edge("final_node", END)
```

### Infinite Loop
**Cause**: Conditional edge always returns same route
```python
# ✅ Add counter or max iterations
def should_continue(state):
    if state["iterations"] >= 3:
        return "end"
    return "retry"
```

### "Node X not found"
**Cause**: Route function returns string not in edge mapping
```python
# ❌ Mismatch
def route(state): return "process"  # But node is "processor"

# ✅ Match exactly
def route(state): return "processor"
```

### State Update Not Reflected
**Cause**: Node not returning dict, or returning wrong keys
```python
# ❌ Returns None
def my_node(state):
    do_something(state)
    # Missing return!

# ✅ Return state updates
def my_node(state):
    return {"result": do_something(state)}
```

### Interrupt Not Working
**Cause**: Missing checkpointer or thread_id
```python
# ❌ No persistence
graph = builder.compile()

# ✅ With checkpointer
graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "123"}}
```

### Parallel State Conflicts
**Cause**: Multiple nodes write same field without reducer
```python
# ❌ Overwrites
class State(TypedDict):
    results: list  # Last write wins

# ✅ Use reducer
class State(TypedDict):
    results: Annotated[list, operator.add]  # Accumulates
```

---

## Debugging

```python
# Visualize graph
from IPython.display import Image
Image(graph.get_graph().draw_mermaid_png())

# Stream with debug info
for chunk in graph.stream(inputs, stream_mode="debug"):
    print(chunk)

# Inspect state
graph.get_state(config).values
```

---

## Quick Reference

| Pattern | When to Use | Key Component |
|---------|-------------|---------------|
| ReAct | Tool-using agent | `create_react_agent` |
| Chaining | Sequential steps | `add_edge` |
| Parallel | Independent tasks | Multiple edges from START |
| Routing | Input classification | `add_conditional_edges` |
| Orchestrator | Dynamic subtasks | `Send` |
| Evaluator | Quality loop | Conditional + counter |
| Supervisor | Agent coordination | `Command` |
| HITL | Human approval | `interrupt` + checkpointer |
