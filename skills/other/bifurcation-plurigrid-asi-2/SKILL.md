---
name: bifurcation-generator
description: Generate bifurcation diagrams for dynamical systems. Use when visualizing parameter-dependent behavior transitions.
metadata:
  trit: 1
  created_with: amp
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
