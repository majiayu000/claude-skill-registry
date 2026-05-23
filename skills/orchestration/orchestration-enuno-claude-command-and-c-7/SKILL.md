---
name: distributed-state-sync-skill
description: Implements CRDT (Conflict-Free Replicated Data Types) for distributed state management with automatic conflict resolution
version: 1.0.0
tags: [orchestration, crdt, state-management, distributed-systems, conflict-resolution]
---

# Distributed State Sync Skill

## Purpose

This skill provides Conflict-Free Replicated Data Types (CRDTs) for managing distributed state across multiple agents with automatic conflict resolution. It enables agents to update shared state concurrently without coordination while guaranteeing eventual consistency.

## When to Use This Skill

**Use this skill when:**
- ✅ Multiple agents need to share and update state concurrently
- ✅ Network partitions or delays are possible
- ✅ Need automatic conflict resolution without locking
- ✅ Want eventually consistent distributed data structures
- ✅ Implementing collaborative multi-agent workflows

**Don't use this skill for:**
- ❌ Single-agent workflows (use local state)
- ❌ Scenarios requiring immediate consistency (use locking)
- ❌ Simple read-only state sharing
- ❌ States that don't conflict (use simple replication)

## Core Data Structures

### 1. OR-Set (Observed-Remove Set)

**Purpose**: Distributed set where adds and removes can happen concurrently

**Properties**:
- Concurrent adds are preserved
- Removes only affect observed elements
- Eventually consistent across all replicas

**Implementation**:
```python
from dataclasses import dataclass, field
from typing import Any, Dict, Set, Tuple
import uuid

@dataclass
class ORSet:
    """
    Observed-Remove Set (OR-Set) CRDT.

    Maintains both added and removed elements with unique IDs.
    Elements can be added and removed concurrently.
    """
    added: Dict[Any, Set[str]] = field(default_factory=dict)  # element -> set of unique IDs
    removed: Set[Tuple[Any, str]] = field(default_factory=set)  # set of (element, unique_id) pairs

    def add(self, element: Any) -> str:
        """
        Add an element to the set.

        Returns:
            Unique ID for this add operation
        """
        unique_id = str(uuid.uuid4())

        if element not in self.added:
            self.added[element] = set()

        self.added[element].add(unique_id)

        return unique_id

    def remove(self, element: Any) -> None:
        """
        Remove an element from the set.

        Removes all currently observed instances of the element.
        """
        if element in self.added:
            for unique_id in self.added[element]:
                self.removed.add((element, unique_id))

    def contains(self, element: Any) -> bool:
        """Check if element is in the set."""
        if element not in self.added:
            return False

        # Element exists if it has any non-removed instances
        for unique_id in self.added[element]:
            if (element, unique_id) not in self.removed:
                return True

        return False

    def get_elements(self) -> Set[Any]:
        """Get all elements currently in the set."""
        elements = set()

        for element, unique_ids in self.added.items():
            # Check if element has any non-removed instances
            if any((element, uid) not in self.removed for uid in unique_ids):
                elements.add(element)

        return elements

    def merge(self, other: 'ORSet') -> 'ORSet':
        """
        Merge with another OR-Set replica.

        Returns:
            New OR-Set with merged state
        """
        merged = ORSet()

        # Merge added elements
        all_elements = set(self.added.keys()) | set(other.added.keys())
        for element in all_elements:
            merged.added[element] = (
                self.added.get(element, set()) |
                other.added.get(element, set())
            )

        # Merge removed elements
        merged.removed = self.removed | other.removed

        return merged
```

**Example**:
```python
# Agent A and Agent B working concurrently
agent_a_set = ORSet()
agent_b_set = ORSet()

# Agent A adds "task-1"
agent_a_set.add("task-1")

# Agent B adds "task-2" (concurrent)
agent_b_set.add("task-2")

# Merge sets
final_set = agent_a_set.merge(agent_b_set)

# Result: Both tasks present
assert final_set.contains("task-1")
assert final_set.contains("task-2")
```

### 2. G-Counter (Grow-Only Counter)

**Purpose**: Distributed counter that only increments

**Properties**:
- Each replica has its own counter
- Total = sum of all replica counters
- Merge is max operation per replica

**Implementation**:
```python
@dataclass
class GCounter:
    """
    Grow-Only Counter CRDT.

    Each replica maintains its own counter.
    Total value is the sum of all replica counters.
    """
    counters: Dict[str, int] = field(default_factory=dict)  # replica_id -> count
    replica_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def increment(self, amount: int = 1) -> None:
        """Increment this replica's counter."""
        if self.replica_id not in self.counters:
            self.counters[self.replica_id] = 0

        self.counters[self.replica_id] += amount

    def value(self) -> int:
        """Get total value across all replicas."""
        return sum(self.counters.values())

    def merge(self, other: 'GCounter') -> 'GCounter':
        """
        Merge with another G-Counter replica.

        Returns:
            New G-Counter with merged state
        """
        merged = GCounter(replica_id=self.replica_id)

        # Take max of each replica's counter
        all_replicas = set(self.counters.keys()) | set(other.counters.keys())
        for replica in all_replicas:
            merged.counters[replica] = max(
                self.counters.get(replica, 0),
                other.counters.get(replica, 0)
            )

        return merged
```

**Example**:
```python
# Three agents counting tasks completed
agent_a_counter = GCounter(replica_id="agent-a")
agent_b_counter = GCounter(replica_id="agent-b")
agent_c_counter = GCounter(replica_id="agent-c")

# Each agent increments locally
agent_a_counter.increment(5)  # Completed 5 tasks
agent_b_counter.increment(3)  # Completed 3 tasks
agent_c_counter.increment(7)  # Completed 7 tasks

# Merge all counters
merged = agent_a_counter.merge(agent_b_counter).merge(agent_c_counter)

# Total tasks completed
assert merged.value() == 15  # 5 + 3 + 7
```

### 3. LWW-Register (Last-Write-Wins Register)

**Purpose**: Distributed register where last write wins based on timestamp

**Properties**:
- Each update has a timestamp
- Latest timestamp wins on conflict
- Simple but may lose data

**Implementation**:
```python
@dataclass
class LWWRegister:
    """
    Last-Write-Wins Register CRDT.

    Stores a value with a timestamp.
    On merge, value with latest timestamp wins.
    """
    value: Any = None
    timestamp: float = 0.0
    replica_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def set(self, value: Any) -> None:
        """Set value with current timestamp."""
        import time
        self.value = value
        self.timestamp = time.time()

    def get(self) -> Any:
        """Get current value."""
        return self.value

    def merge(self, other: 'LWWRegister') -> 'LWWRegister':
        """
        Merge with another LWW-Register.

        Returns:
            New register with value from latest write
        """
        merged = LWWRegister()

        if self.timestamp > other.timestamp:
            merged.value = self.value
            merged.timestamp = self.timestamp
            merged.replica_id = self.replica_id
        elif other.timestamp > self.timestamp:
            merged.value = other.value
            merged.timestamp = other.timestamp
            merged.replica_id = other.replica_id
        else:
            # Timestamps equal - use replica_id as tiebreaker
            if self.replica_id > other.replica_id:
                merged.value = self.value
                merged.timestamp = self.timestamp
                merged.replica_id = self.replica_id
            else:
                merged.value = other.value
                merged.timestamp = other.timestamp
                merged.replica_id = other.replica_id

        return merged
```

**Example**:
```python
# Two agents updating same configuration
agent_a_config = LWWRegister(replica_id="agent-a")
agent_b_config = LWWRegister(replica_id="agent-b")

# Agent A updates at T=1000
agent_a_config.timestamp = 1000.0
agent_a_config.value = {"mode": "production"}

# Agent B updates at T=1001 (1 second later)
agent_b_config.timestamp = 1001.0
agent_b_config.value = {"mode": "staging"}

# Merge: B's value wins (latest timestamp)
merged = agent_a_config.merge(agent_b_config)
assert merged.value == {"mode": "staging"}
```

### 4. PN-Counter (Positive-Negative Counter)

**Purpose**: Distributed counter supporting both increment and decrement

**Properties**:
- Combines two G-Counters (positive and negative)
- Value = positive.value() - negative.value()
- Fully decentralized

**Implementation**:
```python
@dataclass
class PNCounter:
    """
    Positive-Negative Counter CRDT.

    Supports both increment and decrement operations.
    Internally uses two G-Counters.
    """
    positive: GCounter = field(default_factory=GCounter)
    negative: GCounter = field(default_factory=GCounter)

    def increment(self, amount: int = 1) -> None:
        """Increment counter."""
        self.positive.increment(amount)

    def decrement(self, amount: int = 1) -> None:
        """Decrement counter."""
        self.negative.increment(amount)

    def value(self) -> int:
        """Get current value (positive - negative)."""
        return self.positive.value() - self.negative.value()

    def merge(self, other: 'PNCounter') -> 'PNCounter':
        """Merge with another PN-Counter."""
        merged = PNCounter()
        merged.positive = self.positive.merge(other.positive)
        merged.negative = self.negative.merge(other.negative)
        return merged
```

**Example**:
```python
# Agent tracking resource pool (add/remove resources)
agent_a_pool = PNCounter()
agent_b_pool = PNCounter()

# Agent A adds 10 resources
agent_a_pool.increment(10)

# Agent B removes 3 resources (concurrent)
agent_b_pool.decrement(3)

# Merge
merged = agent_a_pool.merge(agent_b_pool)
assert merged.value() == 7  # 10 - 3
```

## Workflow

### Step 1: Initialize Distributed State

```python
from skills.orchestration.distributed_state_sync import ORSet, GCounter

# Initialize state manager
class DistributedStateManager:
    def __init__(self, replica_id: str):
        self.replica_id = replica_id
        self.pending_tasks = ORSet()       # Shared task list
        self.completed_count = GCounter(replica_id=replica_id)  # Task counter
        self.agent_status = {}             # Per-agent state

    def add_task(self, task_id: str) -> None:
        """Add task to pending list."""
        self.pending_tasks.add(task_id)

    def complete_task(self, task_id: str) -> None:
        """Mark task as completed."""
        self.pending_tasks.remove(task_id)
        self.completed_count.increment()

    def get_pending_tasks(self) -> Set[str]:
        """Get all pending tasks."""
        return self.pending_tasks.get_elements()

    def get_completed_count(self) -> int:
        """Get total completed tasks across all agents."""
        return self.completed_count.value()
```

### Step 2: Local Operations

```python
# Agent A performs local operations
agent_a_state = DistributedStateManager(replica_id="agent-a")

agent_a_state.add_task("task-1")
agent_a_state.add_task("task-2")
agent_a_state.complete_task("task-1")

# Agent B performs concurrent operations
agent_b_state = DistributedStateManager(replica_id="agent-b")

agent_b_state.add_task("task-3")
agent_b_state.complete_task("task-3")
```

### Step 3: Periodic Synchronization

```python
def synchronize_state(local_state: DistributedStateManager,
                      remote_state: DistributedStateManager) -> DistributedStateManager:
    """
    Synchronize state between two replicas.

    Returns:
        New state with merged updates
    """
    merged_state = DistributedStateManager(replica_id=local_state.replica_id)

    # Merge pending tasks (OR-Set)
    merged_state.pending_tasks = local_state.pending_tasks.merge(remote_state.pending_tasks)

    # Merge completed count (G-Counter)
    merged_state.completed_count = local_state.completed_count.merge(remote_state.completed_count)

    return merged_state

# Synchronize every 30 seconds
import time

while True:
    # Get state from other agents
    remote_states = fetch_remote_states()

    # Merge with local state
    for remote_state in remote_states:
        agent_a_state = synchronize_state(agent_a_state, remote_state)

    # Broadcast local state to others
    broadcast_state(agent_a_state)

    time.sleep(30)
```

### Step 4: Conflict Resolution

```python
# Conflicts are automatically resolved by CRDT semantics

# Example: Two agents add different tasks concurrently
agent_a_state.add_task("task-1")
agent_b_state.add_task("task-2")

# After merge: Both tasks present (OR-Set preserves both adds)
merged = synchronize_state(agent_a_state, agent_b_state)
assert "task-1" in merged.get_pending_tasks()
assert "task-2" in merged.get_pending_tasks()

# Example: Two agents increment counter concurrently
agent_a_state.completed_count.increment(5)
agent_b_state.completed_count.increment(3)

# After merge: Counts are added (G-Counter sums all increments)
merged = synchronize_state(agent_a_state, agent_b_state)
assert merged.get_completed_count() == 8  # 5 + 3
```

## Advanced Patterns

### 1. Multi-Value Register (MVRegister)

**Purpose**: Keep all concurrent values until resolved

```python
@dataclass
class MVRegister:
    """
    Multi-Value Register CRDT.

    Maintains all concurrent values with vector clocks.
    Application can choose resolution strategy.
    """
    values: Dict[Tuple, Any] = field(default_factory=dict)  # vector_clock -> value

    def set(self, value: Any, vector_clock: Tuple) -> None:
        """Set value with vector clock."""
        # Remove values dominated by this clock
        self.values = {
            vc: v for vc, v in self.values.items()
            if not self._dominates(vector_clock, vc)
        }

        self.values[vector_clock] = value

    def get(self) -> Set[Any]:
        """Get all concurrent values."""
        return set(self.values.values())

    def _dominates(self, vc1: Tuple, vc2: Tuple) -> bool:
        """Check if vc1 dominates vc2 (happens-before)."""
        return all(a >= b for a, b in zip(vc1, vc2)) and vc1 != vc2

    def merge(self, other: 'MVRegister') -> 'MVRegister':
        """Merge two MV-Registers."""
        merged = MVRegister()

        all_clocks = set(self.values.keys()) | set(other.values.keys())

        for vc in all_clocks:
            # Keep if not dominated by any other clock
            if not any(self._dominates(other_vc, vc) for other_vc in all_clocks if other_vc != vc):
                value = self.values.get(vc) or other.values.get(vc)
                merged.values[vc] = value

        return merged
```

### 2. LWW-Map (Last-Write-Wins Map)

**Purpose**: Distributed key-value map with LWW resolution

```python
class LWWMap:
    """
    Last-Write-Wins Map CRDT.

    Each key is an LWW-Register.
    """
    def __init__(self):
        self.map: Dict[str, LWWRegister] = {}

    def set(self, key: str, value: Any) -> None:
        """Set key-value pair."""
        if key not in self.map:
            self.map[key] = LWWRegister()

        self.map[key].set(value)

    def get(self, key: str) -> Any:
        """Get value for key."""
        if key not in self.map:
            return None

        return self.map[key].get()

    def merge(self, other: 'LWWMap') -> 'LWWMap':
        """Merge two LWW-Maps."""
        merged = LWWMap()

        all_keys = set(self.map.keys()) | set(other.map.keys())

        for key in all_keys:
            self_reg = self.map.get(key)
            other_reg = other.map.get(key)

            if self_reg and other_reg:
                merged.map[key] = self_reg.merge(other_reg)
            elif self_reg:
                merged.map[key] = self_reg
            else:
                merged.map[key] = other_reg

        return merged
```

## Integration Patterns

### With State Manager Agent

```python
# State Manager Agent uses this skill for CRDT operations
from skills.orchestration.distributed_state_sync import ORSet, GCounter, LWWMap

class StateManagerAgent:
    def __init__(self, replica_id: str):
        self.replica_id = replica_id

        # Use CRDTs for conflict-free state
        self.tasks = ORSet()           # Pending tasks
        self.metrics = GCounter(replica_id)  # Task counts
        self.config = LWWMap()         # Configuration values

    def handle_state_update(self, operation: str, **kwargs):
        """Handle state update operation."""
        if operation == "add_task":
            self.tasks.add(kwargs["task_id"])

        elif operation == "complete_task":
            self.tasks.remove(kwargs["task_id"])
            self.metrics.increment()

        elif operation == "update_config":
            self.config.set(kwargs["key"], kwargs["value"])

    def sync_with_peer(self, peer_state):
        """Synchronize state with peer agent."""
        self.tasks = self.tasks.merge(peer_state.tasks)
        self.metrics = self.metrics.merge(peer_state.metrics)
        self.config = self.config.merge(peer_state.config)
```

## Examples

### Example 1: Collaborative Task List

```python
# Three agents managing shared task list
agent_a = ORSet()
agent_b = ORSet()
agent_c = ORSet()

# Agent A adds tasks
agent_a.add("implement-auth")
agent_a.add("write-tests")

# Agent B adds task concurrently
agent_b.add("update-docs")

# Agent C removes task (also concurrent)
agent_c.add("implement-auth")  # Observed this task
agent_c.remove("implement-auth")  # Then removed it

# Merge all replicas
merged = agent_a.merge(agent_b).merge(agent_c)

# Result: OR-Set semantics preserve correct state
assert not merged.contains("implement-auth")  # Correctly removed
assert merged.contains("write-tests")         # Preserved from A
assert merged.contains("update-docs")         # Preserved from B
```

### Example 2: Distributed Metrics

```python
# Agents tracking workflow progress
orchestrator = GCounter(replica_id="orchestrator")
agent_1 = GCounter(replica_id="agent-1")
agent_2 = GCounter(replica_id="agent-2")

# Each agent completes tasks
agent_1.increment(5)  # Completed 5 tasks
agent_2.increment(7)  # Completed 7 tasks

# Orchestrator tracks overall progress
orchestrator.increment(2)  # Completed 2 coordination tasks

# Merge for total count
total = orchestrator.merge(agent_1).merge(agent_2)
assert total.value() == 14  # 2 + 5 + 7
```

## Best Practices

1. **Choose Right CRDT for Use Case**
   ```python
   # For sets: Use OR-Set (preserves concurrent adds)
   pending_tasks = ORSet()

   # For counters: Use G-Counter (increment only) or PN-Counter (inc/dec)
   task_count = GCounter()

   # For single values: Use LWW-Register (simple) or MV-Register (complex)
   current_config = LWWRegister()
   ```

2. **Synchronize Periodically**
   ```python
   # Every 30-60 seconds is usually sufficient
   sync_interval = 30  # seconds

   # More frequent for high-concurrency scenarios
   if high_concurrency:
       sync_interval = 10
   ```

3. **Handle Network Partitions**
   ```python
   try:
       remote_state = fetch_state_from_peer()
       merged = local_state.merge(remote_state)
   except NetworkError:
       # Continue with local operations
       # State will eventually sync when partition heals
       log("Network partition - continuing with local state")
   ```

4. **Monitor State Size**
   ```python
   # CRDTs can grow unbounded (especially OR-Set tombstones)
   if len(or_set.removed) > 1000:
       # Garbage collect old tombstones
       or_set.gc_tombstones(older_than=7*24*3600)  # 7 days
   ```

## Related Skills

- `state-manager-skill`: Uses CRDTs for distributed state
- `observability-tracker-skill`: Tracks CRDT synchronization metrics

## References

- [CRDT Wikipedia](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type)
- Document 15, Section 4: State Management Patterns
- Command: `/state-coordinator`

---

**Version**: 1.0.0
**Status**: Production Ready
**Complexity**: High (advanced distributed systems concepts)
**Token Cost**: Low (local operations, periodic sync)
