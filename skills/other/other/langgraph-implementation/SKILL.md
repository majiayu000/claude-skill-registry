---
name: langgraph-implementation
description: Implements stateful agent graphs using LangGraph. Use when building graphs, adding nodes/edges, defining state schemas, implementing checkpointing, handling interrupts, or creating multi-agent systems with LangGraph.
---

# LangGraph Implementation

## Core Concepts

LangGraph builds stateful, multi-actor agent applications using a graph-based architecture:

- **StateGraph**: Builder class for defining graphs with shared state
- **Nodes**: Functions that read state and return partial updates
- **Edges**: Define execution flow (static or conditional)
- **Channels**: Internal state management (LastValue, BinaryOperatorAggregate)
- **Checkpointer**: Persistence for pause/resume capabilities

## Essential Imports

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState, add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, Send, interrupt, RetryPolicy
from typing import Annotated
from typing_extensions import TypedDict
```

## State Schema Patterns

### Basic State with TypedDict

```python
class State(TypedDict):
    counter: int                                    # LastValue - stores last value
    messages: Annotated[list, operator.add]         # Reducer - appends lists
    items: Annotated[list, lambda a, b: a + [b] if b else a]  # Custom reducer
```

### MessagesState for Chat Applications

```python
from langgraph.graph.message import MessagesState

class State(MessagesState):
    # Inherits: messages: Annotated[list[AnyMessage], add_messages]
    user_id: str
    context: dict
```

### Pydantic State (for validation)

```python
from pydantic import BaseModel

class State(BaseModel):
    messages: Annotated[list, add_messages]
    validated_field: str  # Pydantic validates on assignment
```

## Building Graphs

### Basic Pattern

```python
builder = StateGraph(State)

# Add nodes - functions that take state, return partial updates
builder.add_node("process", process_fn)
builder.add_node("decide", decide_fn)

# Add edges
builder.add_edge(START, "process")
builder.add_edge("process", "decide")
builder.add_edge("decide", END)

# Compile
graph = builder.compile()
```

### Node Function Signature

```python
def my_node(state: State) -> dict:
    """Node receives full state, returns partial update."""
    return {"counter": state["counter"] + 1}

# With config access
def my_node(state: State, config: RunnableConfig) -> dict:
    thread_id = config["configurable"]["thread_id"]
    return {"result": process(state, thread_id)}

# With Runtime context (v0.6+)
def my_node(state: State, runtime: Runtime[Context]) -> dict:
    user_id = runtime.context.get("user_id")
    return {"result": user_id}
```

### Conditional Edges

```python
from typing import Literal

def router(state: State) -> Literal["agent", "tools", "__end__"]:
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"
    return END  # or "__end__"

builder.add_conditional_edges("agent", router)

# With path_map for visualization
builder.add_conditional_edges(
    "agent",
    router,
    path_map={"agent": "agent", "tools": "tools", "__end__": END}
)
```

### Command Pattern (Dynamic Routing + State Update)

```python
from langgraph.types import Command

def dynamic_node(state: State) -> Command[Literal["next", "__end__"]]:
    if state["should_continue"]:
        return Command(goto="next", update={"step": state["step"] + 1})
    return Command(goto=END)

# Must declare destinations for visualization
builder.add_node("dynamic", dynamic_node, destinations=["next", END])
```

### Send Pattern (Fan-out/Map-Reduce)

```python
from langgraph.types import Send

def fan_out(state: State) -> list[Send]:
    """Route to multiple node instances with different inputs."""
    return [Send("worker", {"item": item}) for item in state["items"]]

builder.add_conditional_edges(START, fan_out)
builder.add_edge("worker", "aggregate")  # Workers converge
```

## Checkpointing

### Enable Persistence

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver  # Development
from langgraph.checkpoint.postgres import PostgresSaver  # Production

# In-memory (testing only)
graph = builder.compile(checkpointer=InMemorySaver())

# SQLite (development)
with SqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)

# Thread-based invocation
config = {"configurable": {"thread_id": "user-123"}}
result = graph.invoke({"messages": [...]}, config)
```

### State Management

```python
# Get current state
state = graph.get_state(config)

# Get state history
for state in graph.get_state_history(config):
    print(state.values, state.next)

# Update state manually
graph.update_state(config, {"key": "new_value"}, as_node="node_name")
```

## Human-in-the-Loop

### Using interrupt()

```python
from langgraph.types import interrupt, Command

def review_node(state: State) -> dict:
    # Pause and surface value to client
    human_input = interrupt({"question": "Please review", "data": state["draft"]})
    return {"approved": human_input["approved"]}

# Resume with Command
graph.invoke(Command(resume={"approved": True}), config)
```

### Interrupt Before/After Nodes

```python
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["human_review"],  # Pause before node
    interrupt_after=["agent"],          # Pause after node
)

# Check pending interrupts
state = graph.get_state(config)
if state.next:  # Has pending nodes
    # Resume
    graph.invoke(None, config)
```

## Streaming

```python
# Stream modes: "values", "updates", "custom", "messages", "debug"

# Updates only (node outputs)
for chunk in graph.stream(input, stream_mode="updates"):
    print(chunk)  # {"node_name": {"key": "value"}}

# Full state after each step
for chunk in graph.stream(input, stream_mode="values"):
    print(chunk)

# Multiple modes
for mode, chunk in graph.stream(input, stream_mode=["updates", "messages"]):
    if mode == "messages":
        print("Token:", chunk)

# Custom streaming from within nodes
from langgraph.config import get_stream_writer

def my_node(state):
    writer = get_stream_writer()
    writer({"progress": 0.5})  # Custom event
    return {"result": "done"}
```

## Subgraphs

```python
# Define subgraph
sub_builder = StateGraph(SubState)
sub_builder.add_node("step", step_fn)
sub_builder.add_edge(START, "step")
subgraph = sub_builder.compile()

# Use as node in parent
parent_builder = StateGraph(ParentState)
parent_builder.add_node("subprocess", subgraph)
parent_builder.add_edge(START, "subprocess")

# Subgraph checkpointing
subgraph = sub_builder.compile(
    checkpointer=None,   # Inherit from parent (default)
    # checkpointer=True,   # Use persistent checkpointing
    # checkpointer=False,  # Disable checkpointing
)
```

## Retry and Caching

```python
from langgraph.types import RetryPolicy, CachePolicy

retry = RetryPolicy(
    initial_interval=0.5,
    backoff_factor=2.0,
    max_attempts=3,
    retry_on=ValueError,  # Or callable: lambda e: isinstance(e, ValueError)
)

cache = CachePolicy(ttl=3600)  # Cache for 1 hour

builder.add_node("risky", risky_fn, retry_policy=retry, cache_policy=cache)
```

## Prebuilt Components

### create_react_agent (moved to langchain.agents in v1.0)

```python
from langgraph.prebuilt import create_react_agent, ToolNode

# Simple agent
graph = create_react_agent(
    model="anthropic:claude-3-5-sonnet",
    tools=[my_tool],
    prompt="You are a helpful assistant",
    checkpointer=InMemorySaver(),
)

# Custom tool node
tool_node = ToolNode([tool1, tool2])
builder.add_node("tools", tool_node)
```

## Common Patterns

### Agent Loop

```python
def should_continue(state) -> Literal["tools", "__end__"]:
    if state["messages"][-1].tool_calls:
        return "tools"
    return END

builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")
```

### Parallel Execution

```python
# Multiple nodes execute in parallel when they share the same trigger
builder.add_edge(START, "node_a")
builder.add_edge(START, "node_b")  # Runs parallel with node_a
builder.add_edge(["node_a", "node_b"], "join")  # Wait for both
```

See [PATTERNS.md](PATTERNS.md) for advanced patterns including multi-agent systems, hierarchical graphs, and complex workflows.
