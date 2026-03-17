---
name: unstable-manifold
description: Manifold of points diverging from equilibrium
trit: 1
geodesic: true
moebius: "μ(n) ≠ 0"
---

# Unstable Manifold

**Trit**: 1 (PLUS)
**Domain**: Dynamical Systems Theory
**Principle**: Manifold of points diverging from equilibrium

## Overview

Unstable Manifold is a fundamental concept in dynamical systems theory, providing tools for understanding the qualitative behavior of differential equations and flows on manifolds.

## Mathematical Definition

```
UNSTABLE_MANIFOLD: Phase space × Time → Phase space
```

## Key Properties

1. **Local behavior**: Analysis near equilibria and invariant sets
2. **Global structure**: Long-term dynamics and limit sets  
3. **Bifurcations**: Parameter-dependent qualitative changes
4. **Stability**: Robustness under perturbation

## Integration with GF(3)

This skill participates in triadic composition:
- **Trit 1** (PLUS): Sources/generators
- **Conservation**: Σ trits ≡ 0 (mod 3) across skill triplets

## AlgebraicDynamics.jl Connection

```julia
using AlgebraicDynamics

# Unstable Manifold as compositional dynamical system
# Implements oapply for resource-sharing machines
```

## Related Skills

- equilibrium (trit 0)
- stability (trit +1)  
- bifurcation (trit +1)
- attractor (trit +1)
- lyapunov-function (trit -1)

---

**Skill Name**: unstable-manifold
**Type**: Dynamical Systems / Unstable Manifold
**Trit**: 1 (PLUS)
**GF(3)**: Conserved in triplet composition

## Non-Backtracking Geodesic Qualification

**Condition**: μ(n) ≠ 0 (Möbius squarefree)

This skill is qualified for non-backtracking geodesic traversal:

1. **Prime Path**: No state revisited in skill invocation chain
2. **Möbius Filter**: Composite paths (backtracking) cancel via μ-inversion
3. **GF(3) Conservation**: Trit sum ≡ 0 (mod 3) across skill triplets
4. **Spectral Gap**: Ramanujan bound λ₂ ≤ 2√(k-1) for k-regular expansion

```
Geodesic Invariant:
  ∀ path P: backtrack(P) = ∅ ⟹ μ(|P|) ≠ 0
  
Möbius Inversion:
  f(n) = Σ_{d|n} g(d) ⟹ g(n) = Σ_{d|n} μ(n/d) f(d)
```
