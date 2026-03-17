---
name: langgraph-architecture
description: Guides architectural decisions for LangGraph applications. Use when deciding between LangGraph vs alternatives, choosing state management strategies, designing multi-agent systems, or selecting persistence and streaming approaches.
---

# LangGraph Architecture Decisions

## When to Use LangGraph

### Use LangGraph When You Need:

- **Stateful conversations** - Multi-turn interactions with memory
- **Human-in-the-loop** - Approval gates, corrections, interventions
- **Complex control flow** - Loops, branches, conditional routing
- **Multi-agent coordination** - Multiple LLMs working together
- **Persistence** - Resume from checkpoints, time travel debugging
- **Streaming** - Real-time token streaming, progress updates
- **Reliability** - Retries, error recovery, durability guarantees

### Consider Alternatives When:

| Scenario | Alternative | Why |
|----------|-------------|-----|
| Single LLM call | Direct API call | Overhead not justified |
| Linear pipeline | LangChain LCEL | Simpler abstraction |
| Stateless tool use | Function calling | No persistence needed |
| Simple RAG | LangChain retrievers | Built-in patterns |
| Batch processing | Async tasks | Different execution model |

## State Schema Decisions

### TypedDict vs Pydantic

| TypedDict | Pydantic |
|-----------|----------|
| Lightweight, faster | Runtime validation |
| Dict-like access | Attribute access |
| No validation overhead | Type coercion |
| Simpler serialization | Complex nested models |

**Recommendation**: Use TypedDict for most cases. Use Pydantic when you need validation or complex nested structures.

### Reducer Selection

| Use Case | Reducer | Example |
|----------|---------|---------|
| Chat messages | `add_messages` | Handles IDs, RemoveMessage |
| Simple append | `operator.add` | `Annotated[list, operator.add]` |
| Keep latest | None (LastValue) | `field: str` |
| Custom merge | Lambda | `Annotated[list, lambda a, b: ...]` |
| Overwrite list | `Overwrite` | Bypass reducer |

### State Size Considerations

```python
# SMALL STATE (< 1MB) - Put in state
class State(TypedDict):
    messages: Annotated[list, add_messages]
    context: str

# LARGE DATA - Use Store
class State(TypedDict):
    messages: Annotated[list, add_messages]
    document_ref: str  # Reference to store

def node(state, *, store: BaseStore):
    doc = store.get(namespace, state["document_ref"])
    # Process without bloating checkpoints
```

## Graph Structure Decisions

### Single Graph vs Subgraphs

**Single Graph** when:
- All nodes share the same state schema
- Simple linear or branching flow
- < 10 nodes

**Subgraphs** when:
- Different state schemas needed
- Reusable components across graphs
- Team separation of concerns
- Complex hierarchical workflows

### Conditional Edges vs Command

| Conditional Edges | Command |
|------------------|---------|
| Routing based on state | Routing + state update |
| Separate router function | Decision in node |
| Clearer visualization | More flexible |
| Standard patterns | Dynamic destinations |

```python
# Conditional Edge - when routing is the focus
def router(state) -> Literal["a", "b"]:
    return "a" if condition else "b"
builder.add_conditional_edges("node", router)

# Command - when combining routing with updates
def node(state) -> Command:
    return Command(goto="next", update={"step": state["step"] + 1})
```

### Static vs Dynamic Routing

**Static Edges** (`add_edge`):
- Fixed flow known at build time
- Clearer graph visualization
- Easier to reason about

**Dynamic Routing** (`add_conditional_edges`, `Command`, `Send`):
- Runtime decisions based on state
- Agent-driven navigation
- Fan-out patterns

## Persistence Strategy

### Checkpointer Selection

| Checkpointer | Use Case | Characteristics |
|--------------|----------|-----------------|
| `InMemorySaver` | Testing only | Lost on restart |
| `SqliteSaver` | Development | Single file, local |
| `PostgresSaver` | Production | Scalable, concurrent |
| Custom | Special needs | Implement BaseCheckpointSaver |

### Checkpointing Scope

```python
# Full persistence (default)
graph = builder.compile(checkpointer=checkpointer)

# Subgraph options
subgraph = sub_builder.compile(
    checkpointer=None,   # Inherit from parent
    checkpointer=True,   # Independent checkpointing
    checkpointer=False,  # No checkpointing (runs atomically)
)
```

### When to Disable Checkpointing

- Short-lived subgraphs that should be atomic
- Subgraphs with incompatible state schemas
- Performance-critical paths without need for resume

## Multi-Agent Architecture

### Supervisor Pattern

Best for:
- Clear hierarchy
- Centralized decision making
- Different agent specializations

```
          ┌─────────────┐
          │  Supervisor │
          └──────┬──────┘
    ┌────────┬───┴───┬────────┐
    ▼        ▼       ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│Agent1│ │Agent2│ │Agent3│ │Agent4│
└──────┘ └──────┘ └──────┘ └──────┘
```

### Peer-to-Peer Pattern

Best for:
- Collaborative agents
- No clear hierarchy
- Flexible communication

```
┌──────┐     ┌──────┐
│Agent1│◄───►│Agent2│
└──┬───┘     └───┬──┘
   │             │
   ▼             ▼
┌──────┐     ┌──────┐
│Agent3│◄───►│Agent4│
└──────┘     └──────┘
```

### Handoff Pattern

Best for:
- Sequential specialization
- Clear stage transitions
- Different capabilities per stage

```
┌────────┐    ┌────────┐    ┌────────┐
│Research│───►│Planning│───►│Execute │
└────────┘    └────────┘    └────────┘
```

## Streaming Strategy

### Stream Mode Selection

| Mode | Use Case | Data |
|------|----------|------|
| `updates` | UI updates | Node outputs only |
| `values` | State inspection | Full state each step |
| `messages` | Chat UX | LLM tokens |
| `custom` | Progress/logs | Your data via StreamWriter |
| `debug` | Debugging | Tasks + checkpoints |

### Subgraph Streaming

```python
# Stream from subgraphs
async for chunk in graph.astream(
    input,
    stream_mode="updates",
    subgraphs=True  # Include subgraph events
):
    namespace, data = chunk  # namespace indicates depth
```

## Human-in-the-Loop Design

### Interrupt Placement

| Strategy | Use Case |
|----------|----------|
| `interrupt_before` | Approval before action |
| `interrupt_after` | Review after completion |
| `interrupt()` in node | Dynamic, contextual pauses |

### Resume Patterns

```python
# Simple resume (same thread)
graph.invoke(None, config)

# Resume with value
graph.invoke(Command(resume="approved"), config)

# Resume specific interrupt
graph.invoke(Command(resume={interrupt_id: value}), config)

# Modify state and resume
graph.update_state(config, {"field": "new_value"})
graph.invoke(None, config)
```

## Error Handling Strategy

### Retry Configuration

```python
# Per-node retry
RetryPolicy(
    initial_interval=0.5,
    backoff_factor=2.0,
    max_interval=60.0,
    max_attempts=3,
    retry_on=lambda e: isinstance(e, (APIError, TimeoutError))
)

# Multiple policies (first match wins)
builder.add_node("node", fn, retry_policy=[
    RetryPolicy(retry_on=RateLimitError, max_attempts=5),
    RetryPolicy(retry_on=Exception, max_attempts=2),
])
```

### Fallback Patterns

```python
def node_with_fallback(state):
    try:
        return primary_operation(state)
    except PrimaryError:
        return fallback_operation(state)

# Or use conditional edges for complex fallback routing
def route_on_error(state) -> Literal["retry", "fallback", "__end__"]:
    if state.get("error") and state["attempts"] < 3:
        return "retry"
    elif state.get("error"):
        return "fallback"
    return END
```

## Scaling Considerations

### Horizontal Scaling

- Use PostgresSaver for shared state
- Consider LangGraph Platform for managed infrastructure
- Use stores for large data outside checkpoints

### Performance Optimization

1. **Minimize state size** - Use references for large data
2. **Parallel nodes** - Fan out when possible
3. **Cache expensive operations** - Use CachePolicy
4. **Async everywhere** - Use ainvoke, astream

### Resource Limits

```python
# Set recursion limit
config = {"recursion_limit": 50}
graph.invoke(input, config)

# Track remaining steps in state
class State(TypedDict):
    remaining_steps: RemainingSteps

def check_budget(state):
    if state["remaining_steps"] < 5:
        return "wrap_up"
    return "continue"
```

## Decision Checklist

Before implementing:

1. [ ] Is LangGraph the right tool? (vs simpler alternatives)
2. [ ] State schema defined with appropriate reducers?
3. [ ] Persistence strategy chosen? (dev vs prod checkpointer)
4. [ ] Streaming needs identified?
5. [ ] Human-in-the-loop points defined?
6. [ ] Error handling and retry strategy?
7. [ ] Multi-agent coordination pattern? (if applicable)
8. [ ] Resource limits configured?
