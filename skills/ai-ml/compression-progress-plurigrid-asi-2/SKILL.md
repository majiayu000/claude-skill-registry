---
name: compression-progress
description: Schmidhuber's compression progress as intrinsic curiosity reward for
  learning systems.
license: UNLICENSED
metadata:
  trit: 0
  source: local
---

# Compression Progress Skill: Curiosity-Driven Learning

**Status**: ✅ Production Ready
**Trit**: +1 (PLUS - generator)
**Color**: #D82626 (Red)
**Principle**: Learning = Compression improvement
**Frame**: Compressor improvement rate as reward signal

---

## Overview

**Compression Progress** measures the *derivative* of compression ability over time. When a learner compresses data better than before, that improvement is intrinsic reward—the formal theory of curiosity and creativity.

1. **Compressor C(t)**: Current world model
2. **Compression ratio**: |C(data)| / |data|
3. **Progress**: C(t) - C(t-1) improvement
4. **Reward**: Proportional to progress, not absolute compression

## Core Formula

```
r(t) = |C(t-1)(data)| - |C(t)(data)|

Curiosity reward = compression improvement rate
Boredom = zero progress (already compressed or incompressible)
```

```python
def compression_progress(compressor_old, compressor_new, data) -> float:
    """Intrinsic reward from model improvement."""
    old_bits = len(compressor_old.compress(data))
    new_bits = len(compressor_new.compress(data))
    return old_bits - new_bits  # positive = learned something
```

## Key Concepts

### 1. Curiosity as Compression Gradient

```python
class CuriousAgent:
    def __init__(self):
        self.world_model = Compressor()
        self.history = []
    
    def intrinsic_reward(self, observation) -> float:
        old_len = self.world_model.compressed_length(observation)
        self.world_model.update(observation)
        new_len = self.world_model.compressed_length(observation)
        return old_len - new_len  # curiosity signal
    
    def should_explore(self, state) -> bool:
        """Explore where compression progress is expected."""
        return self.expected_progress(state) > self.threshold
```

### 2. Creativity as Compression Search

```python
def generate_interesting(compressor) -> Data:
    """Generate data that maximizes expected compression progress."""
    candidates = sample_latent_space()
    return max(candidates, 
               key=lambda x: expected_progress(compressor, x))
```

### 3. Optimal Curriculum via Progress

```python
def select_next_task(tasks, compressor) -> Task:
    """Choose task with maximum learning potential."""
    progress_estimates = [
        estimate_compression_progress(compressor, task)
        for task in tasks
    ]
    # Not too easy (zero progress), not too hard (negative/zero)
    return tasks[argmax(progress_estimates)]
```

## Commands

```bash
# Measure compression progress
just compression-progress before.model after.model data/

# Generate curiosity curriculum
just curiosity-curriculum tasks.json

# Visualize learning trajectory
just compression-trajectory log.json
```

## Integration with GF(3) Triads

```
yoneda-directed (-1) ⊗ cognitive-superposition (0) ⊗ compression-progress (+1) = 0 ✓  [Riehl-Schmidhuber]
kolmogorov-compression (-1) ⊗ turing-chemputer (0) ⊗ compression-progress (+1) = 0 ✓  [Formal Learning]
```

## Related Skills

- **kolmogorov-compression** (-1): Absolute complexity baseline
- **godel-machine** (+1): Self-improvement via provable progress
- **cognitive-superposition** (0): Multi-hypothesis compression

---

**Skill Name**: compression-progress
**Type**: Curiosity Generator
**Trit**: +1 (PLUS)
**Color**: #D82626 (Red)
