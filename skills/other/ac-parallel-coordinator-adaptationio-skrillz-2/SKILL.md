---
name: ac-parallel-coordinator
description: Coordinate parallel autonomous operations. Use when running parallel features, managing concurrent work, coordinating multiple agents, or optimizing throughput.
---

# AC Parallel Coordinator

Coordinate parallel autonomous operations.

## Purpose

Manages parallel execution of independent features to maximize throughput while maintaining safety.

## Quick Start

```python
from scripts.parallel_coordinator import ParallelCoordinator

coordinator = ParallelCoordinator(project_dir)
parallel_groups = await coordinator.find_parallel_opportunities()
results = await coordinator.execute_parallel(parallel_groups[0])
```

## API Reference

See `scripts/parallel_coordinator.py` for full implementation.
