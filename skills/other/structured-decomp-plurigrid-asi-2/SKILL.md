---
name: structured-decomp
description: "StructuredDecompositions.jl: Sheaves on tree decompositions for FPT algorithms"
source: AlgebraicJulia/StructuredDecompositions.jl
license: MIT
trit: 0
---

# Structured Decompositions Skill

## Core Concepts

**StrDecomp** = Functor `d: ∫G → C` where:
- ∫G = category of elements of shape graph
- C = target category (Graph, FinSet, etc.)

```julia
using StructuredDecompositions

# Create decomposition from graph
d = StrDecomp(graph)

# Access components
bags(d)           # Local substructures
adhesions(d)      # Overlaps
adhesionSpans(d)  # Span morphisms
```

## The 𝐃 Functor

Lifts decision problems to decomposition space:
```julia
# Define problem as functor
k_coloring(G) = homomorphisms(G, K_k)

# Lift and solve
solution = 𝐃(k_coloring, decomp, CoDecomposition)
(answer, _) = decide_sheaf_tree_shape(k_coloring, decomp)
```

## FPT Complexity

Runtime: O(f(width) × n) where width = max adhesion size

## GF(3) Triads

```
dmd-spectral (-1) ⊗ structured-decomp (0) ⊗ koopman-generator (+1) = 0 ✓
sheaf-cohomology (-1) ⊗ structured-decomp (0) ⊗ colimit-reconstruct (+1) = 0 ✓
```

## References

- Bumpus et al. arXiv:2207.06091
- algebraicjulia.github.io/StructuredDecompositions.jl
