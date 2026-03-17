---
name: lamport-distributed-systems
description: Design distributed systems using Leslie Lamport's rigorous approach. Emphasizes formal reasoning, logical time, consensus protocols, and state machine replication. Use when building systems where correctness under concurrency and partial failure is critical.
---

# Leslie Lamport Style Guide

## Overview

Leslie Lamport transformed distributed systems from ad-hoc engineering into a rigorous science. His work on logical clocks, consensus (Paxos), and formal specification (TLA+) provides the theoretical foundation for nearly every reliable distributed system built today. Turing Award winner (2013).

## Core Philosophy

> "A distributed system is one in which the failure of a computer you didn't even know existed can render your own computer unusable."

> "If you're thinking without writing, you only think you're thinking."

> "The way to be a good programmer is to write programs, not to learn languages."

## Design Principles

1. **Formal Specification First**: Write a precise specification before writing code. If you can't specify it precisely, you don't understand it.

2. **Time is Relative**: There is no global clock in a distributed system. Use logical time (happens-before) to reason about ordering.

3. **State Machine Replication**: Any deterministic service can be made fault-tolerant by replicating it as a state machine across multiple servers.

4. **Safety and Liveness**: Separate what must always be true (safety) from what must eventually happen (liveness). Prove both.

5. **Simplicity Through Rigor**: The clearest systems come from precise thinking. Formalism isn't overhead—it's the path to simplicity.

## When Designing Systems

### Always

- Write a specification before implementation (TLA+, Alloy, or precise prose)
- Define the safety properties: what bad things must never happen
- Define the liveness properties: what good things must eventually happen
- Reason about all possible interleavings of concurrent operations
- Use logical timestamps when physical time isn't reliable
- Make system state explicit and transitions clear
- Document invariants that must hold across all states

### Never

- Assume messages arrive in order (unless you've proven it)
- Assume clocks are synchronized (they're not)
- Assume failures are independent (they're often correlated)
- Hand-wave about "eventually" without defining what guarantees that
- Trust intuition for concurrent systems—prove it or test it exhaustively
- Confuse the specification with the implementation

### Prefer

- State machines over ad-hoc event handling
- Logical clocks over physical timestamps for ordering
- Consensus protocols over optimistic concurrency for critical state
- Explicit failure handling over implicit assumptions
- Proved algorithms over clever heuristics

## Key Concepts

### Logical Clocks (Lamport Timestamps)

```
Each process maintains a counter C:
1. Before any event, increment C
2. When sending a message, include C
3. When receiving a message with timestamp T, set C = max(C, T) + 1

This gives a partial ordering: if a → b, then C(a) < C(b)
(But C(a) < C(b) does NOT imply a → b)
```

### The Happens-Before Relation (→)

```
a → b (a happens before b) if:
1. a and b are in the same process and a comes before b, OR
2. a is a send and b is the corresponding receive, OR
3. There exists c such that a → c and c → b (transitivity)

If neither a → b nor b → a, events are CONCURRENT.
```

### State Machine Replication

```
To replicate a service:
1. Model the service as a deterministic state machine
2. Replicate the state machine across N servers
3. Use consensus (Paxos/Raft) to agree on the sequence of inputs
4. Each replica applies inputs in the same order → same state

Tolerates F failures with 2F+1 replicas.
```

### Paxos (Simplified)

```
Three roles: Proposers, Acceptors, Learners

Phase 1 (Prepare):
  Proposer sends PREPARE(n) to acceptors
  Acceptor responds with highest-numbered proposal it accepted (if any)
  
Phase 2 (Accept):
  If proposer receives majority responses:
    Send ACCEPT(n, v) where v is highest-numbered value seen (or new value)
  Acceptor accepts if it hasn't promised to a higher proposal

Consensus reached when majority accept the same (n, v).
```

## Mental Model

Lamport approaches distributed systems as a mathematician:

1. **Define the problem precisely**: What are the inputs, outputs, and allowed behaviors?
2. **Identify the invariants**: What must always be true?
3. **Consider all interleavings**: What happens if events occur in any order?
4. **Prove correctness**: Show that safety and liveness hold.
5. **Then implement**: The code should be a straightforward translation of the spec.

### The TLA+ Approach

```
1. Define the state space (all possible states)
2. Define the initial state predicate
3. Define the next-state relation (allowed transitions)
4. Specify safety as invariants (always true)
5. Specify liveness as temporal properties (eventually true)
6. Model-check or prove that the spec satisfies properties
```

## Code Patterns

### Implementing Logical Clocks

```python
class LamportClock:
    def __init__(self):
        self._time = 0
    
    def tick(self) -> int:
        """Increment before local event."""
        self._time += 1
        return self._time
    
    def send_timestamp(self) -> int:
        """Get timestamp for outgoing message."""
        self._time += 1
        return self._time
    
    def receive(self, msg_timestamp: int) -> int:
        """Update clock on message receipt."""
        self._time = max(self._time, msg_timestamp) + 1
        return self._time
```

### Vector Clocks (for Causality Detection)

```python
class VectorClock:
    def __init__(self, node_id: str, num_nodes: int):
        self._id = node_id
        self._clock = {f"node_{i}": 0 for i in range(num_nodes)}
    
    def tick(self):
        self._clock[self._id] += 1
    
    def send(self) -> dict:
        self.tick()
        return self._clock.copy()
    
    def receive(self, other: dict):
        for node, time in other.items():
            self._clock[node] = max(self._clock.get(node, 0), time)
        self.tick()
    
    def happens_before(self, other: dict) -> bool:
        """Returns True if self → other."""
        return all(self._clock[k] <= other.get(k, 0) for k in self._clock) \
           and any(self._clock[k] < other.get(k, 0) for k in self._clock)
```

## Warning Signs

You're violating Lamport's principles if:

- You assume "this will never happen in practice" without proof
- Your distributed algorithm works "most of the time"
- You can't write down the invariants your system maintains
- You're using wall-clock time for ordering in a distributed system
- You haven't considered what happens during network partitions
- Your system has no formal specification

## Additional Resources

- For detailed philosophy, see [philosophy.md](philosophy.md)
- For references (papers, talks), see [references.md](references.md)
