---
name: vogels-cloud-architecture
description: Design cloud-native systems using Werner Vogels' principles of failure-first design, eventual consistency, and API-driven architecture. Emphasizes building for failure, customer obsession, and practical distributed systems. Use when building AWS-scale services, microservices, or any system that must be highly available.
---

# Werner Vogels Style Guide

## Overview

Werner Vogels is Amazon's CTO and VP since 2005. He drove the architecture behind AWS and authored the influential Dynamo paper. His philosophy shapes how modern cloud-native systems are built: assume failure, embrace eventual consistency, and obsess over the customer. His blog "All Things Distributed" has taught a generation of engineers.

## Core Philosophy

> "Everything fails, all the time."

> "There is no compression algorithm for experience."

> "Customers will always want lower prices, more selection, and faster delivery."

## Design Principles

1. **Design for Failure**: Don't try to prevent failure—embrace it. Design systems that work despite component failures.

2. **Eventual Consistency is Often Enough**: Strong consistency has costs. Most applications can tolerate—and benefit from—eventual consistency.

3. **APIs are Forever**: Once published, an API is a contract. Design APIs for the long term.

4. **Decentralize Everything**: Centralized components become bottlenecks and single points of failure.

5. **Automate Everything**: If a human has to do it more than once, automate it.

## The Dynamo Principles

From the Amazon Dynamo paper—foundational to modern distributed databases:

```text
1. INCREMENTAL SCALABILITY
   Add nodes without downtime or performance impact

2. SYMMETRY
   No special nodes; every node has same responsibilities

3. DECENTRALIZATION  
   No leader; peer-to-peer coordination

4. HETEROGENEITY
   Work distribution accounts for node capabilities
```

### Key Techniques

| Technique | Purpose |
|-----------|---------|
| Consistent hashing | Partition data across nodes |
| Vector clocks | Track causality, detect conflicts |
| Sloppy quorum | Availability over consistency |
| Hinted handoff | Handle temporary failures |
| Anti-entropy | Background consistency repair |
| Merkle trees | Efficient synchronization |

## When Designing Systems

### Always

- Assume any component can fail at any time
- Design for at least 2 availability zones (better: 3+)
- Use timeouts on ALL external calls
- Implement circuit breakers for dependent services
- Build observability in from day one
- Version all APIs from the start
- Automate deployment and rollback
- Test failure scenarios in production (chaos engineering)

### Never

- Depend on a single point of failure
- Assume the network is reliable
- Expose internal implementation in APIs
- Make synchronous calls when async would work
- Deploy without the ability to roll back
- Ignore tail latencies (p99, p999)
- Trust that downstream services will be available

### Prefer

- Eventual consistency over strong when possible
- Asynchronous over synchronous communication
- Idempotent operations over exactly-once semantics
- Cell-based architecture over monoliths
- Feature flags over big-bang releases
- Small, frequent deployments over large, infrequent ones

## CAP Theorem in Practice

```text
CAP: You can have at most 2 of:
- Consistency
- Availability  
- Partition tolerance

Vogels' view: You MUST handle partitions (P is not optional).
The real choice is: C or A during partitions.

Most Amazon systems choose: AP (Available, Partition-tolerant)
Accept eventual consistency for high availability.

But: Some operations (payments, inventory) need CP.
Choose per-operation, not per-system.
```

### Consistency Models

```text
Strong consistency:
  After a write, all reads see it immediately.
  Cost: Latency, availability during partitions.

Eventual consistency:
  After a write, reads EVENTUALLY see it (milliseconds to seconds).
  Benefit: Lower latency, higher availability.

Causal consistency:
  Operations causally related are seen in order.
  Middle ground between strong and eventual.

Read-your-writes:
  A client always sees its own writes.
  Often sufficient for user-facing applications.
```

## Code Patterns

### Circuit Breaker

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, TypeVar
import threading

T = TypeVar('T')

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """
    Vogels principle: Design for failure.
    
    Stop calling a failing service to:
    1. Fail fast (don't wait for timeout)
    2. Give the service time to recover
    3. Prevent cascade failures
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: timedelta = timedelta(seconds=30),
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: datetime | None = None
        self._half_open_calls = 0
        self._lock = threading.Lock()
    
    def call(self, func: Callable[[], T], fallback: Callable[[], T]) -> T:
        """Execute func with circuit breaker protection."""
        with self._lock:
            if self._state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self._state = CircuitState.HALF_OPEN
                    self._half_open_calls = 0
                else:
                    return fallback()
        
        try:
            result = func()
            self._on_success()
            return result
        except Exception:
            self._on_failure()
            return fallback()
    
    def _should_attempt_reset(self) -> bool:
        return (
            self._last_failure_time is not None
            and datetime.now() - self._last_failure_time >= self.recovery_timeout
        )
    
    def _on_success(self) -> None:
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._half_open_calls += 1
                if self._half_open_calls >= self.half_open_max_calls:
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
    
    def _on_failure(self) -> None:
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = datetime.now()
            
            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.OPEN
            elif self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
```

### Retry with Jitter

```python
import random
import time
from typing import Callable, TypeVar

T = TypeVar('T')

def retry_with_jitter(
    func: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 0.1,
    max_delay: float = 10.0,
) -> T:
    """
    Retry with exponential backoff AND jitter.
    
    Vogels: "Everything fails, all the time."
    
    Jitter prevents the thundering herd problem where
    all clients retry simultaneously after a failure.
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            # Exponential backoff
            delay = min(base_delay * (2 ** attempt), max_delay)
            
            # Full jitter: random between 0 and calculated delay
            # This spreads retries evenly over time
            jittered_delay = random.uniform(0, delay)
            
            time.sleep(jittered_delay)
    
    raise RuntimeError("Unreachable")
```

### Cell-Based Architecture

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Callable

T = TypeVar('T')

@dataclass
class Cell(Generic[T]):
    """
    A cell is an independent unit of deployment and failure.
    
    Vogels' principle: Isolate blast radius.
    
    Each cell:
    - Serves a subset of traffic
    - Has its own resources
    - Fails independently
    - Can be deployed independently
    """
    cell_id: str
    region: str
    capacity: int
    handler: Callable[[str], T]
    
    def handle(self, request_id: str) -> T:
        return self.handler(request_id)

class CellRouter:
    """Route requests to cells based on partition key."""
    
    def __init__(self, cells: list[Cell]):
        self.cells = {c.cell_id: c for c in cells}
        self.cell_ids = sorted(self.cells.keys())
    
    def route(self, partition_key: str) -> Cell:
        """
        Deterministic routing ensures same key goes to same cell.
        This enables cell-local caching and reduces cross-cell traffic.
        """
        # Consistent hashing would be better for production
        index = hash(partition_key) % len(self.cell_ids)
        return self.cells[self.cell_ids[index]]
    
    def handle_with_fallback(
        self, 
        partition_key: str, 
        request_id: str
    ):
        """Try primary cell, fall back to secondary on failure."""
        primary = self.route(partition_key)
        secondary = self.route(partition_key + "_fallback")
        
        try:
            return primary.handle(request_id)
        except Exception:
            # Fallback to different cell
            return secondary.handle(request_id)
```

### Eventual Consistency Handler

```python
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime

@dataclass
class VectorClock:
    """Track causality for conflict detection."""
    clocks: dict[str, int] = field(default_factory=dict)
    
    def increment(self, node_id: str) -> None:
        self.clocks[node_id] = self.clocks.get(node_id, 0) + 1
    
    def merge(self, other: 'VectorClock') -> 'VectorClock':
        merged = VectorClock()
        all_nodes = set(self.clocks.keys()) | set(other.clocks.keys())
        for node in all_nodes:
            merged.clocks[node] = max(
                self.clocks.get(node, 0),
                other.clocks.get(node, 0)
            )
        return merged
    
    def is_concurrent_with(self, other: 'VectorClock') -> bool:
        """True if neither clock dominates the other."""
        self_dominates = any(
            self.clocks.get(k, 0) > other.clocks.get(k, 0)
            for k in set(self.clocks.keys()) | set(other.clocks.keys())
        )
        other_dominates = any(
            other.clocks.get(k, 0) > self.clocks.get(k, 0)
            for k in set(self.clocks.keys()) | set(other.clocks.keys())
        )
        return self_dominates and other_dominates

@dataclass
class VersionedValue:
    """A value with vector clock for conflict detection."""
    value: Any
    clock: VectorClock
    timestamp: datetime = field(default_factory=datetime.now)

def resolve_conflict(
    values: list[VersionedValue],
    resolver: Callable[[list[Any]], Any]
) -> VersionedValue:
    """
    Resolve conflicts using application-specific logic.
    
    Dynamo approach: Return all conflicting versions to client,
    let application resolve (e.g., merge shopping carts).
    """
    # Find concurrent values (conflicts)
    concurrent = []
    for v in values:
        is_dominated = any(
            not v.clock.is_concurrent_with(other.clock) 
            and v != other
            for other in values
        )
        if not is_dominated:
            concurrent.append(v)
    
    if len(concurrent) == 1:
        return concurrent[0]
    
    # Multiple concurrent values: resolve
    resolved_value = resolver([v.value for v in concurrent])
    merged_clock = concurrent[0].clock
    for v in concurrent[1:]:
        merged_clock = merged_clock.merge(v.clock)
    
    return VersionedValue(value=resolved_value, clock=merged_clock)
```

## Mental Model

Vogels approaches systems with pragmatic pessimism:

1. **Assume failure**: What breaks when this component fails?
2. **Measure the customer impact**: How does this affect user experience?
3. **Design for recovery**: How quickly can we recover?
4. **Automate operations**: Can this be done without human intervention?
5. **Iterate**: Ship, measure, improve.

### The Amazon Tenets

```text
1. Customer Obsession
   Work backwards from customer needs, not technology.

2. Ownership
   Leaders own outcomes, not just their piece.

3. Bias for Action
   Speed matters. Many decisions are reversible.

4. Frugality
   Accomplish more with less. Constraints breed innovation.

5. Operational Excellence
   Anticipate and prevent problems before they occur.
```

## Warning Signs

You're violating Vogels' principles if:

- You haven't tested what happens when dependencies fail
- Your system has a single point of failure
- You're manually deploying to production
- You don't know your p99 latency
- Your monitoring doesn't alert on customer impact
- You chose strong consistency without measuring the cost
- Your APIs break existing clients

## Additional Resources

- For detailed philosophy, see [philosophy.md](philosophy.md)
- For references (papers, talks, blog), see [references.md](references.md)
