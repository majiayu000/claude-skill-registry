---
name: langgraph-checkpoints
description: LangGraph checkpointing and persistence. Use when implementing fault-tolerant workflows, resuming interrupted executions, debugging with state history, or avoiding re-running expensive operations.
context: fork
agent: workflow-architect
version: 1.0.0
author: SkillForge
user-invocable: false
---

# LangGraph Checkpointing

Persist workflow state for recovery and debugging.

## Checkpointer Options

```python
from langgraph.checkpoint import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver

# Development: In-memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Production: SQLite
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
app = workflow.compile(checkpointer=checkpointer)

# Production: PostgreSQL
checkpointer = PostgresSaver.from_conn_string("postgresql://...")
app = workflow.compile(checkpointer=checkpointer)
```

## Using Thread IDs

```python
# Start new workflow
config = {"configurable": {"thread_id": "analysis-123"}}
result = app.invoke(initial_state, config=config)

# Resume interrupted workflow
config = {"configurable": {"thread_id": "analysis-123"}}
result = app.invoke(None, config=config)  # Resumes from checkpoint
```

## PostgreSQL Setup

```python
def create_checkpointer():
    """Create PostgreSQL checkpointer for production."""
    return PostgresSaver.from_conn_string(
        settings.DATABASE_URL,
        save_every=1  # Save after each node
    )

# Compile with checkpointing
app = workflow.compile(
    checkpointer=create_checkpointer(),
    interrupt_before=["quality_gate"]  # Manual review point
)
```

## Inspecting Checkpoints

```python
# Get all checkpoints for a workflow
checkpoints = app.get_state_history(config)

for checkpoint in checkpoints:
    print(f"Step: {checkpoint.metadata['step']}")
    print(f"Node: {checkpoint.metadata['source']}")
    print(f"State: {checkpoint.values}")

# Get current state
current = app.get_state(config)
print(current.values)
```

## Resuming After Crash

```python
import logging

async def run_with_recovery(workflow_id: str, initial_state: dict):
    """Run workflow with automatic recovery."""
    config = {"configurable": {"thread_id": workflow_id}}

    try:
        # Try to resume existing workflow
        state = app.get_state(config)
        if state.values:
            logging.info(f"Resuming workflow {workflow_id}")
            return app.invoke(None, config=config)
    except Exception:
        pass  # No existing checkpoint

    # Start fresh
    logging.info(f"Starting new workflow {workflow_id}")
    return app.invoke(initial_state, config=config)
```

## Step-by-Step Debugging

```python
# Execute one node at a time
for step in app.stream(initial_state, config):
    print(f"After {step['node']}: {step['state']}")
    input("Press Enter to continue...")

# Rollback to previous checkpoint
history = list(app.get_state_history(config))
previous_state = history[1]  # One step back
app.update_state(config, previous_state.values)
```

## Store vs Checkpointer (2026 Best Practice)

```python
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore

# Checkpointer = SHORT-TERM memory (thread-scoped)
# - Conversation history within a session
# - Workflow state for resume/recovery
# - Scoped to thread_id

checkpointer = PostgresSaver.from_conn_string(DATABASE_URL)

# Store = LONG-TERM memory (cross-thread)
# - User preferences across sessions
# - Learned facts about users
# - Shared across ALL threads for a user

store = PostgresStore.from_conn_string(DATABASE_URL)

# Compile with BOTH for full memory support
app = workflow.compile(
    checkpointer=checkpointer,  # Thread-scoped state
    store=store                  # Cross-thread memory
)
```

## Using Store for Cross-Thread Memory

```python
from langgraph.store.base import BaseStore

async def agent_with_memory(state: AgentState, *, store: BaseStore):
    """Agent that remembers across conversations."""
    user_id = state["user_id"]

    # Read cross-thread memory (user preferences)
    memories = await store.aget(namespace=("users", user_id), key="preferences")

    # Use memories in agent logic
    if memories and memories.value.get("prefers_concise"):
        state["system_prompt"] += "\nBe concise in responses."

    # Update cross-thread memory (learned facts)
    await store.aput(
        namespace=("users", user_id),
        key="last_topic",
        value={"topic": state["current_topic"], "timestamp": datetime.now().isoformat()}
    )

    return state

# Register node with store access
workflow.add_node("agent", agent_with_memory)
```

## Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User: alice                               │
├─────────────────────────────────────────────────────────────┤
│  Thread 1 (chat-001)    │  Thread 2 (chat-002)              │
│  ┌─────────────────┐    │  ┌─────────────────┐              │
│  │ Checkpointer    │    │  │ Checkpointer    │              │
│  │ - msg history   │    │  │ - msg history   │              │
│  │ - workflow pos  │    │  │ - workflow pos  │              │
│  └─────────────────┘    │  └─────────────────┘              │
├─────────────────────────────────────────────────────────────┤
│                     Store (cross-thread)                     │
│  namespace=("users", "alice")                                │
│  - preferences: {prefers_concise: true}                     │
│  - last_topic: {topic: "langgraph", timestamp: "..."}       │
└─────────────────────────────────────────────────────────────┘
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Development | MemorySaver (fast, no setup) |
| Production | PostgresSaver (shared, durable) |
| save_every | 1 for expensive nodes, 5 for cheap |
| Thread ID | Use deterministic ID (workflow_id) |
| **Short-term memory** | **Checkpointer (thread-scoped)** |
| **Long-term memory** | **Store (cross-thread, namespaced)** |

## Common Mistakes

- No checkpointer in production (lose progress)
- Random thread IDs (can't resume)
- Not handling missing checkpoints
- Saving too frequently (overhead)
- **Using only checkpointer for user preferences (lost across threads)**
- **Not using namespaces in Store (data collisions)**

## Related Skills

- `langgraph-state` - State design for checkpointing
- `langgraph-human-in-loop` - Interrupt patterns
- `database-schema-designer` - PostgreSQL setup

## Capability Details

### checkpoint-saving
**Keywords:** save checkpoint, checkpoint, persist state, save state
**Solves:**
- Save workflow state at key points
- Implement checkpoint strategies
- Handle checkpoint serialization

### checkpoint-loading
**Keywords:** load checkpoint, restore, resume, recovery
**Solves:**
- Resume workflows from checkpoints
- Implement state recovery
- Handle checkpoint versioning

### memory-backends
**Keywords:** memory backend, MemorySaver, SqliteSaver, PostgresSaver
**Solves:**
- Configure checkpoint storage backends
- Choose between memory/SQLite/Postgres
- Implement custom checkpoint storage

### async-checkpoints
**Keywords:** async checkpoint, AsyncSqliteSaver, async persistence
**Solves:**
- Implement async checkpoint operations
- Handle concurrent checkpoint access
- Optimize checkpoint performance

### conversation-history
**Keywords:** conversation, history, message history, thread
**Solves:**
- Persist conversation history
- Implement thread-based checkpoints
- Manage conversation state
