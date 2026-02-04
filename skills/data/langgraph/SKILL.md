---
name: langgraph
description: LangGraph skill for building stateful agent graphs, subgraphs, checkpoints, conditional flows, parallel execution, streaming, and multi-agent orchestration.
---

# LangGraph - Skill

Purpose

This skill explains core patterns for building directed graph based AI workflows with LangGraph in Python. Use it for agent orchestration, stateful pipelines, subgraph composition, RAG plus node processing, and checkpointed experiments.

When an AI assistant should apply this skill

- When editing files that import langgraph or create StateGraph objects
- When authoring node functions that use LLMs or tools
- When adding checkpoints, persistence, or streaming to agent runs
- When composing subgraphs or multi-agent flows

Quick start

1. Model the workflow state with a TypedDict. 2. Write small pure node functions that accept and return partial state. 3. Use START as entry. 4. Compile the builder to get a runnable graph. 5. Add a checkpointer for persistence and safe experimentation.

Core concepts and cheat sheet

- StateGraph
  - The builder models nodes and edges over a typed state. Compile the builder into a runnable.

- Node functions
  - Node functions receive the current state and return updates. Keep them small and testable.

- Edges and routing
  - add_edge for deterministic flows. add_conditional_edges or routing functions for branching.
  - Returning multiple node names fans out and runs downstream nodes in parallel on the next superstep.

- Checkpointing
  - Attach a checkpointer during compile to persist intermediate states. Use checkpointers to resume, diff, and fork runs.

- Subgraphs
  - Compose graphs by calling subgraphs from nodes or by attaching compiled subgraphs as nodes.

- Agents as nodes
  - A node can call an LLM to make decisions. Combine LangChain LLMs inside node functions to implement agent logic.

- Streaming and debugging
  - Use graph.stream to receive partial outputs as nodes finish. Enable tracing or export runs to your monitoring backend.

Examples

1) Minimal state graph

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START

class S(TypedDict):
    count: int

def inc(state: S) -> dict:
    return {"count": state["count"] + 1}

b = StateGraph(S)
b.add_node("inc", inc)
b.add_edge(START, "inc")

g = b.compile()
print(g.invoke({"count": 1}))
```

2) Conditional loop with checkpoint

```python
from langgraph.checkpoint.memory import MemorySaver

class LoopState(TypedDict):
    x: int
    done: bool

def step(state: LoopState) -> dict:
    x = state["x"] + 1
    done = x >= 3
    return {"x": x, "done": done}

b = StateGraph(LoopState)
b.add_node("step", step)
b.add_edge(START, "step")

# route back to step until done
def route(state: LoopState) -> str:
    return "step" if not state["done"] else "END"

b.add_conditional_edges("step", route, {True: "step", False: "END"})

g = b.compile(checkpointer=MemorySaver())
print(g.invoke({"x": 0, "done": False}))
```

3) Subgraph composition

```python
# subgraph definition
class SubState(TypedDict):
    value: int

def multiply10(s: SubState) -> dict:
    return {"value": s["value"] * 10}

sub = StateGraph(SubState)
sub.add_node("mul10", multiply10)
sub.add_edge(START, "mul10")
sub_g = sub.compile()

# parent graph calls subgraph
class ParentState(TypedDict):
    x: int

def call_sub(state: ParentState) -> dict:
    res = sub_g.invoke({"value": state["x"]})
    return {"x": res["value"]}

p = StateGraph(ParentState)
p.add_node("run_sub", call_sub)
p.add_edge(START, "run_sub")
pg = p.compile()
print(pg.invoke({"x": 2}))
```

4) Agent node with LangChain LLM decision

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class AState(TypedDict):
    prompt: str
    action: str

# node uses LLM to decide action
def decide(state: AState) -> dict:
    out = llm.invoke(state["prompt"])  # returns assistant text
    # minimal parsing, prefer structured output in production
    action = "search" if "search" in out.lower() else "respond"
    return {"action": action}

b = StateGraph(AState)
b.add_node("decide", decide)
b.add_edge(START, "decide")
g = b.compile()
print(g.invoke({"prompt": "Find the latest version of X"}))
```

5) Streaming execution and monitoring

```python
for update in g.stream({"x": 0}, stream_mode="updates", subgraphs=True):
    print(update)
```

Patterns and best practices

- Keep node functions small and deterministic. If you need heavy LLM logic, isolate it and parse structured outputs.
- Use checkpointers to experiment safely. Take a checkpoint when a stable milestone is reached.
- Use subgraphs to separate concerns and enable reuse.
- For multi-agent flows, model each agent as a node or subgraph and use edges as communication channels.
- Use the stream API during development for fast feedback.

Debugging tips

- Run graphs locally with MemorySaver checkpointer and inspect get_state to see intermediate state.
- Use logging inside node functions and callbacks to trace execution.
- When agent nodes call LLMs, record the prompt and model config in your telemetry to reproduce decisions.

Folder structure suggestion

.github/skills/
  langchain/SKILL.md
  langgraph/SKILL.md



