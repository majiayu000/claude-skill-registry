---
name: dean-large-scale-systems
description: Design large-scale systems using Jeff Dean's pragmatic approach. Emphasizes performance intuition, building reliable systems from unreliable components, and solving problems at Google scale. Use when building infrastructure that must handle millions of QPS, petabytes of data, or global distribution.
---

# Jeff Dean Style Guide

## Overview

Jeff Dean is the architect behind much of Google's infrastructure: MapReduce, BigTable, Spanner, TensorFlow, and more. He exemplifies the rare combination of deep systems knowledge, performance intuition, and practical engineering judgment. His work defines how modern internet-scale systems are built.

## Core Philosophy

> "Design for 10x the current load, but plan to rewrite before 100x."

> "Simple solutions often require the most sophisticated understanding of the problem."

> "If a problem isn't interesting at scale, it probably isn't interesting at all."

## Design Principles

1. **Embrace Failure**: At scale, everything fails. Design systems that degrade gracefully, not catastrophically.

2. **Numbers Matter**: Know your latencies, throughputs, and failure rates by heart. Performance intuition comes from data.

3. **Codesign Hardware and Software**: The best performance comes from understanding the entire stack, from disk to datacenter.

4. **Simplicity at Scale**: Complex systems break in complex ways. The simplest solution that scales is usually the best.

5. **Measure, Then Optimize**: Never optimize without profiling. Intuition fails; data doesn't.

## Numbers Every Engineer Should Know

```text
L1 cache reference                           0.5 ns
Branch mispredict                            5   ns
L2 cache reference                           7   ns
Mutex lock/unlock                           25   ns
Main memory reference                      100   ns
Compress 1K bytes with Zippy             3,000   ns
Send 1K bytes over 1 Gbps network       10,000   ns
Read 4K randomly from SSD              150,000   ns
Read 1 MB sequentially from memory     250,000   ns
Round trip within same datacenter      500,000   ns
Read 1 MB sequentially from SSD      1,000,000   ns
Disk seek                           10,000,000   ns
Read 1 MB sequentially from disk    20,000,000   ns
Send packet CA→Netherlands→CA      150,000,000   ns
```

These numbers should guide every design decision.

## When Designing Systems

### Always

- Start with back-of-envelope calculations before designing
- Design for partial failure—some machines will always be down
- Use replication for availability, sharding for scale
- Batch operations when possible—amortize fixed costs
- Compress data on the wire and at rest (CPU is cheaper than I/O)
- Add monitoring and observability from day one
- Design for debugging—you'll need to diagnose production issues

### Never

- Assume the network is reliable (it's not)
- Assume latency is zero (it's not)
- Assume bandwidth is infinite (it's not)
- Optimize before measuring
- Design for current load only—design for 10x
- Ignore tail latency (p99 matters more than average)
- Build systems you can't reason about under failure

### Prefer

- Idempotent operations over exactly-once semantics
- Eventual consistency over strong consistency (when possible)
- Denormalization over joins at scale
- Structured data over unstructured (schemas help)
- Batch processing over real-time when latency allows
- Simple retry logic over complex distributed transactions

## Architectural Patterns

### MapReduce Mental Model

```text
Problem: Process petabytes of data
Solution: 
  1. Map: Transform input into (key, value) pairs in parallel
  2. Shuffle: Group all values by key
  3. Reduce: Aggregate values for each key

Why it works:
  - Embarrassingly parallel map phase
  - Fault tolerance via re-execution
  - Simple programming model hides distribution
```

### BigTable Design

```text
Problem: Structured storage at massive scale
Solution:
  - Sparse, distributed, multi-dimensional sorted map
  - (row, column, timestamp) → value
  - Rows sorted lexicographically (enables range scans)
  - Column families for locality
  - Tablets (row ranges) as unit of distribution

Key insight: One data model, flexible enough for many use cases.
```

### Spanner's TrueTime

```text
Problem: Global consistency requires synchronized clocks
Solution:
  - GPS + atomic clocks in every datacenter
  - API returns interval [earliest, latest] not a point
  - Wait out uncertainty before committing
  
TrueTime.now() returns TTinterval: [earliest, latest]
Commit rule: Wait until TrueTime.now().earliest > commit_timestamp
```

## Code Patterns

### Back-of-Envelope Capacity Planning

```python
def estimate_storage_needs(
    daily_active_users: int,
    actions_per_user_per_day: int,
    bytes_per_action: int,
    retention_days: int,
    replication_factor: int = 3
) -> dict:
    """Jeff Dean-style capacity estimation."""
    
    daily_bytes = daily_active_users * actions_per_user_per_day * bytes_per_action
    total_bytes = daily_bytes * retention_days * replication_factor
    
    return {
        "daily_raw_gb": daily_bytes / (1024**3),
        "total_storage_tb": total_bytes / (1024**4),
        "monthly_bandwidth_tb": (daily_bytes * 30) / (1024**4),
        "estimated_machines_1tb_each": total_bytes / (1024**4),
    }

# Example: 100M DAU, 10 actions/day, 1KB each, 90 day retention
# = 270 TB storage, ~300 machines (with replication)
```

### Sharding Strategy

```python
class ConsistentHashRing:
    """Distribute data across nodes with minimal reshuffling."""
    
    def __init__(self, nodes: list[str], virtual_nodes: int = 150):
        self.ring: dict[int, str] = {}
        self.sorted_keys: list[int] = []
        
        for node in nodes:
            for i in range(virtual_nodes):
                key = self._hash(f"{node}:{i}")
                self.ring[key] = node
        
        self.sorted_keys = sorted(self.ring.keys())
    
    def get_node(self, key: str) -> str:
        """Find the node responsible for this key."""
        if not self.ring:
            raise ValueError("Empty ring")
        
        h = self._hash(key)
        for ring_key in self.sorted_keys:
            if h <= ring_key:
                return self.ring[ring_key]
        return self.ring[self.sorted_keys[0]]
    
    def _hash(self, key: str) -> int:
        import hashlib
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
```

### Retry with Exponential Backoff

```python
import random
import time
from typing import TypeVar, Callable

T = TypeVar('T')

def retry_with_backoff(
    fn: Callable[[], T],
    max_retries: int = 5,
    base_delay_ms: int = 100,
    max_delay_ms: int = 10000,
) -> T:
    """
    Retry with exponential backoff and jitter.
    
    At Google scale, thundering herds kill systems.
    Jitter prevents synchronized retries.
    """
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            delay = min(base_delay_ms * (2 ** attempt), max_delay_ms)
            jitter = random.uniform(0, delay * 0.1)
            time.sleep((delay + jitter) / 1000)
    
    raise RuntimeError("Unreachable")
```

## Mental Model

Jeff Dean approaches problems with:

1. **Quantify first**: How much data? How many QPS? What latency budget?
2. **Identify bottlenecks**: Where will the system break first?
3. **Design for failure**: What happens when (not if) components fail?
4. **Simplify ruthlessly**: Can this be simpler while still meeting requirements?
5. **Plan for evolution**: Today's solution should be replaceable in 3 years

### The Google Design Doc

```text
1. Context & Scope
   - What problem are we solving? Why now?
   
2. Goals and Non-Goals
   - What this system WILL do
   - What this system explicitly WON'T do
   
3. Design
   - System architecture
   - Data model
   - API
   
4. Alternatives Considered
   - What else could we do? Why not?
   
5. Cross-cutting Concerns
   - Security, privacy, monitoring, rollout
   
6. Open Questions
   - What don't we know yet?
```

## Warning Signs

You're violating Dean's principles if:

- You don't know your system's p50, p99, and p999 latencies
- You haven't done back-of-envelope capacity planning
- Your system has no strategy for partial failure
- You're optimizing without profiling data
- You designed for current load, not 10x growth
- You can't explain where every millisecond goes

## Additional Resources

- For detailed philosophy, see [philosophy.md](philosophy.md)
- For references (papers, talks), see [references.md](references.md)
