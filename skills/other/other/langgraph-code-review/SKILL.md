---
name: langgraph-code-review
description: Reviews LangGraph code for bugs, anti-patterns, and improvements. Use when reviewing code that uses StateGraph, nodes, edges, checkpointing, or other LangGraph features. Catches common mistakes in state management, graph structure, and async patterns.
---

# LangGraph Code Review

When reviewing LangGraph code, check for these categories of issues.

## Critical Issues

### 1. State Mutation Instead of Return

```python
# BAD - mutates state directly
def my_node(state: State) -> None:
    state["messages"].append(new_message)  # Mutation!

# GOOD - returns partial update
def my_node(state: State) -> dict:
    return {"messages": [new_message]}  # Let reducer handle it
```

### 2. Missing Reducer for List Fields

```python
# BAD - no reducer, each node overwrites
class State(TypedDict):
    messages: list  # Will be overwritten, not appended!

# GOOD - reducer appends
class State(TypedDict):
    messages: Annotated[list, operator.add]
    # Or use add_messages for chat:
    messages: Annotated[list, add_messages]
```

### 3. Wrong Return Type from Conditional Edge

```python
# BAD - returns invalid node name
def router(state) -> str:
    return "nonexistent_node"  # Runtime error!

# GOOD - use Literal type hint for safety
def router(state) -> Literal["agent", "tools", "__end__"]:
    if condition:
        return "agent"
    return END  # Use constant, not string
```

### 4. Missing Checkpointer for Interrupts

```python
# BAD - interrupt without checkpointer
def my_node(state):
    answer = interrupt("question")  # Will fail!
    return {"answer": answer}

graph = builder.compile()  # No checkpointer!

# GOOD - checkpointer required for interrupts
graph = builder.compile(checkpointer=InMemorySaver())
```

### 5. Forgetting Thread ID with Checkpointer

```python
# BAD - no thread_id
graph.invoke({"messages": [...]})  # Error with checkpointer!

# GOOD - always provide thread_id
config = {"configurable": {"thread_id": "user-123"}}
graph.invoke({"messages": [...]}, config)
```

## State Schema Issues

### 6. Using add_messages Without Message Types

```python
# BAD - add_messages expects message-like objects
class State(TypedDict):
    messages: Annotated[list, add_messages]

def node(state):
    return {"messages": ["plain string"]}  # May fail!

# GOOD - use proper message types or tuples
def node(state):
    return {"messages": [("assistant", "response")]}
    # Or: [AIMessage(content="response")]
```

### 7. Returning Full State Instead of Partial

```python
# BAD - returns entire state (may reset other fields)
def my_node(state: State) -> State:
    return {
        "counter": state["counter"] + 1,
        "messages": state["messages"],  # Unnecessary!
        "other": state["other"]          # Unnecessary!
    }

# GOOD - return only changed fields
def my_node(state: State) -> dict:
    return {"counter": state["counter"] + 1}
```

### 8. Pydantic State Without Annotations

```python
# BAD - Pydantic model without reducer loses append behavior
class State(BaseModel):
    messages: list  # No reducer!

# GOOD - use Annotated even with Pydantic
class State(BaseModel):
    messages: Annotated[list, add_messages]
```

## Graph Structure Issues

### 9. Missing Entry Point

```python
# BAD - no edge from START
builder.add_node("process", process_fn)
builder.add_edge("process", END)
graph = builder.compile()  # Error: no entrypoint!

# GOOD - connect START
builder.add_edge(START, "process")
```

### 10. Unreachable Nodes

```python
# BAD - orphan node
builder.add_node("main", main_fn)
builder.add_node("orphan", orphan_fn)  # Never reached!
builder.add_edge(START, "main")
builder.add_edge("main", END)

# Check with visualization
print(graph.get_graph().draw_mermaid())
```

### 11. Conditional Edge Without All Paths

```python
# BAD - missing path in conditional
def router(state) -> Literal["a", "b", "c"]:
    ...

builder.add_conditional_edges("node", router, {"a": "a", "b": "b"})
# "c" path missing!

# GOOD - include all possible returns
builder.add_conditional_edges("node", router, {"a": "a", "b": "b", "c": "c"})
# Or omit path_map to use return values as node names
```

### 12. Command Without destinations

```python
# BAD - Command return without destinations (breaks visualization)
def dynamic(state) -> Command[Literal["next", "__end__"]]:
    return Command(goto="next")

builder.add_node("dynamic", dynamic)  # Graph viz won't show edges

# GOOD - declare destinations
builder.add_node("dynamic", dynamic, destinations=["next", END])
```

## Async Issues

### 13. Mixing Sync/Async Incorrectly

```python
# BAD - async node called with sync invoke
async def my_node(state):
    result = await async_operation()
    return {"result": result}

graph.invoke(input)  # May not await properly!

# GOOD - use ainvoke for async graphs
await graph.ainvoke(input)
# Or provide both sync and async versions
```

### 14. Blocking Calls in Async Context

```python
# BAD - blocking call in async node
async def my_node(state):
    result = requests.get(url)  # Blocks event loop!
    return {"result": result}

# GOOD - use async HTTP client
async def my_node(state):
    async with httpx.AsyncClient() as client:
        result = await client.get(url)
    return {"result": result}
```

## Tool Integration Issues

### 15. Tool Calls Without Corresponding ToolMessage

```python
# BAD - AI message with tool_calls but no tool execution
messages = [
    HumanMessage(content="search for X"),
    AIMessage(content="", tool_calls=[{"id": "1", "name": "search", ...}])
    # Missing ToolMessage! Next LLM call will fail
]

# GOOD - always pair tool_calls with ToolMessage
messages = [
    HumanMessage(content="search for X"),
    AIMessage(content="", tool_calls=[{"id": "1", "name": "search", ...}]),
    ToolMessage(content="results", tool_call_id="1")
]
```

### 16. Parallel Tool Calls Before Interrupt

```python
# BAD - model may call multiple tools including interrupt
model = ChatOpenAI().bind_tools([interrupt_tool, other_tool])
# If both called in parallel, interrupt behavior is undefined

# GOOD - disable parallel tool calls before interrupt
model = ChatOpenAI().bind_tools(
    [interrupt_tool, other_tool],
    parallel_tool_calls=False
)
```

## Checkpointing Issues

### 17. InMemorySaver in Production

```python
# BAD - in-memory checkpointer loses state on restart
graph = builder.compile(checkpointer=InMemorySaver())  # Testing only!

# GOOD - use persistent storage in production
from langgraph.checkpoint.postgres import PostgresSaver
checkpointer = PostgresSaver.from_conn_string(conn_string)
graph = builder.compile(checkpointer=checkpointer)
```

### 18. Subgraph Checkpointer Confusion

```python
# BAD - subgraph with explicit False prevents persistence
subgraph = sub_builder.compile(checkpointer=False)

# GOOD - use None to inherit parent's checkpointer
subgraph = sub_builder.compile(checkpointer=None)  # Inherits from parent
# Or True for independent checkpointing
subgraph = sub_builder.compile(checkpointer=True)
```

## Performance Issues

### 19. Large State in Every Update

```python
# BAD - returning large data in every node
def node(state):
    large_data = fetch_large_data()
    return {"large_field": large_data}  # Checkpointed every step!

# GOOD - use references or store
from langgraph.store.memory import InMemoryStore

def node(state, *, store: BaseStore):
    store.put(namespace, key, large_data)
    return {"data_ref": f"{namespace}/{key}"}
```

### 20. Missing Recursion Limit Handling

```python
# BAD - no protection against infinite loops
def router(state):
    return "agent"  # Always loops!

# GOOD - check remaining steps or use RemainingSteps
from langgraph.managed import RemainingSteps

class State(TypedDict):
    messages: Annotated[list, add_messages]
    remaining_steps: RemainingSteps

def check_limit(state):
    if state["remaining_steps"] < 2:
        return END
    return "continue"
```

## Code Review Checklist

1. [ ] State schema uses Annotated with reducers for collections
2. [ ] Nodes return partial state updates, not mutations
3. [ ] Conditional edges return valid node names or END
4. [ ] Graph has path from START to all nodes
5. [ ] Checkpointer provided if using interrupts
6. [ ] Thread ID provided in config when using checkpointer
7. [ ] Tool calls paired with ToolMessages
8. [ ] Async nodes use async operations
9. [ ] Production uses persistent checkpointer
10. [ ] Recursion limits considered for loops
