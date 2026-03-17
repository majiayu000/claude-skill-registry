---
name: koopman-generator
description: "Koopman operator theory for infinite-dimensional linear lifting of nonlinear dynamics. Generates dynamics from observables."
source: Brunton+Kutz+Mezić + music-topos
license: MIT
trit: +1
---

# Koopman Generator Skill

## Core Idea

The **Koopman operator** K linearizes nonlinear dynamics by lifting to infinite-dimensional observable space:

```
State space (nonlinear)     Observable space (linear)
      x_{t+1} = f(x_t)   →   (Kg)(x) = g(f(x))
```

**Key property**: K is **linear** even when f is nonlinear.

## Connection to DMD

DMD finds finite-rank approximation of K:
```
K ≈ Φ Λ Φ†
```
- Φ = DMD modes (approximate Koopman eigenfunctions)
- Λ = eigenvalues

## As ACSet Morphism

Koopman = natural transformation on observable presheaves:
```julia
# Observable functor
F: StateSpace → ObservableSpace

# Koopman as pushforward
K = f_*: Sh(X) → Sh(X)
```

## GF(3) Triads

```
dmd-spectral (-1) ⊗ structured-decomp (0) ⊗ koopman-generator (+1) = 0 ✓
temporal-coalgebra (-1) ⊗ acsets (0) ⊗ koopman-generator (+1) = 0 ✓
```

## References

- Brunton et al. "Modern Koopman Theory" (2021)
- Mezić "Spectral Properties of Dynamical Systems" (2005)
- PyDMD: https://github.com/mathLab/PyDMD
