---
name: algebraic-rewriting
description: Category-theoretic graph rewriting with DPO, SPO, and SqPO pushouts for C-Sets. Declarative transformation of acset data structures.
metadata:
  trit: -1
  color: "#0BAD20"
---

# Algebraic Rewriting

## Overview

**AlgebraicRewriting.jl** is a Julia library for performing category-theoretic rewrites over C-Sets and other Catlab.jl data structures.

## Rewriting Approaches

| Type | Description | Use Case |
|------|-------------|----------|
| **DPO** | Double Pushout | Safe deletion (no dangling edges) |
| **SPO** | Single Pushout | Greedy deletion |
| **SqPO** | Sesqui-Pushout | Cloning + deletion |

## Core Concepts

### Rewrite Rules

A rewrite rule consists of:
- **L** (left) - Pattern to match
- **K** (interface) - What to preserve
- **R** (right) - Replacement pattern

```julia
using AlgebraicRewriting

# Define a rule: merge two vertices
L = @acset Graph begin V=2; E=1; src=[1]; tgt=[2] end
K = @acset Graph begin V=1 end
R = @acset Graph begin V=1 end

rule = Rule(L, K, R)
```

### Apply Rewriting

```julia
G = @acset Graph begin
    V = 4
    E = 3
    src = [1, 2, 3]
    tgt = [2, 3, 4]
end

# Find matches and rewrite
matches = homomorphisms(L, G)
G′ = rewrite(rule, G, matches[1])
```

## Double Pushout (DPO)

```
    L ←─ K ─→ R
    ↓    ↓    ↓
    G ←─ D ─→ H
```

The context D ensures no "dangling edges" after deletion.

## Sesqui-Pushout (SqPO)

Supports cloning via the final pullback complement:

```julia
# Clone a vertex
L = @acset Graph begin V=1 end
K = @acset Graph begin V=1 end
R = @acset Graph begin V=2 end

clone_rule = Rule(L, K, R; type=:SqPO)
```

## Gay.jl Integration

```julia
# sRGB boundary learning with rewriting seed
gay_seed!(0xabfca37b6b4bc699)

# Forward mode autodiff
∂params = Enzyme.gradient(Forward, loss, params, seed)
```

## Documentation

- [Full Documentation](https://algebraicjulia.github.io/AlgebraicRewriting.jl/dev/)
- [Brown 2022](https://arxiv.org/abs/2111.03784) - Theoretical foundation

## Repository

- **Source**: plurigrid/AlgebraicRewriting.jl (fork of AlgebraicJulia)
- **Seed**: `0xabfca37b6b4bc699`
- **Index**: 496/1055
- **Color**: #c25d0b

## GF(3) Triad

```
algebraic-rewriting (-1) ⊗ acsets-hatchery (0) ⊗ gay-monte-carlo (+1) = 0 ✓
```

## Related Skills

- `acsets-hatchery` - ACSet data structures
- `topos-adhesive-rewriting` - Adhesive categories
- `dpo-rewriting` - Graph transformation
- `world-a` - AlgebraicJulia ecosystem
