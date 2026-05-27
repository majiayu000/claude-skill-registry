---
name: bifurcation-generator
description: Generate bifurcation diagrams for dynamical systems. Use when visualizing parameter-dependent behavior transitions.
version: 1.0.0
---


# Bifurcation Generator

Generates bifurcation diagrams showing how system behavior changes with parameters.

## When to Use
- Visualizing Hopf, pitchfork, saddle-node bifurcations
- Parameter sweeps in dynamical systems
- Stability boundary identification

## GF(3) Role
PLUS (+1) Generator - creates visual outputs from system parameters.

## Quick Examples

```python
# Logistic map bifurcation
import numpy as np
import matplotlib.pyplot as plt

def logistic_bifurcation(r_min=2.5, r_max=4.0, steps=1000):
    r_vals = np.linspace(r_min, r_max, steps)
    x = 0.5
    for r in r_vals:
        for _ in range(100):  # transient
            x = r * x * (1 - x)
        for _ in range(50):   # attractor
            x = r * x * (1 - x)
            yield r, x
```

## Integration with bifurcation (0) skill

This skill (PLUS +1) pairs with `bifurcation` (ERGODIC 0) for balanced analysis:
- bifurcation: detects and classifies transitions
- bifurcation-generator: visualizes parameter space

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 2. Domain-Specific Languages

**Concepts**: DSL, wrapper, pattern-directed, embedding

### GF(3) Balanced Triad

```
bifurcation-generator (+) + SDF.Ch2 (−) + [balancer] (○) = 0
```

**Skill Trit**: 1 (PLUS - generation)


### Connection Pattern

DSLs embed domain knowledge. This skill defines domain-specific operations.
