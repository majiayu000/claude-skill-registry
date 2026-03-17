---
name: acsets-hatchery
description: Attributed C-Sets as algebraic databases. Category-theoretic data structures generalizing graphs and dataframes with Gay.jl color integration.
metadata:
  trit: 0
  color: "#E146A8"
---

# ACSets Hatchery

## Overview

**ACSets.jl** provides acsets ("attributed C-sets") - data structures generalizing both graphs and data frames. They are an efficient in-memory implementation of category-theoretic relational databases.

## Core Features

- **Acset schemas** - Category-theoretic data structure definitions
- **Acsets** - Instances of schemas (like database rows)
- **Tabular columns** - Efficient columnar storage
- **Serialization** - JSON/binary format support

## What Are ACSets?

An ACSet is a functor from a category C to Set, with attributes. This means:
- **Objects** become tables
- **Morphisms** become foreign keys
- **Attributes** add data types to objects

## Usage

```julia
using ACSets

# Define a schema
@present SchGraph(FreeSchema) begin
    V::Ob
    E::Ob
    src::Hom(E, V)
    tgt::Hom(E, V)
end

# Create an acset
g = @acset Graph begin
    V = 3
    E = 2
    src = [1, 2]
    tgt = [2, 3]
end
```

## Extensions

- **Catlab.jl** - Homomorphisms, limits/colimits, functorial data migration
- **AlgebraicRewriting.jl** - DPO/SPO/SqPO rewriting for acsets

## Learning Resources

1. [Graphs and C-sets I](https://blog.algebraicjulia.org/post/2020/09/cset-graphs-1/) - What is a graph?
2. [Graphs and C-sets II](https://blog.algebraicjulia.org/post/2020/09/cset-graphs-2/) - Half-edges and rotation systems
3. [Graphs and C-sets III](https://blog.algebraicjulia.org/post/2021/04/cset-graphs-3/) - Reflexive graphs and homomorphisms
4. [Graphs and C-sets IV](https://blog.algebraicjulia.org/post/2021/09/cset-graphs-4/) - Propositional logic of subgraphs

## Gay.jl Integration

```julia
# Rec2020 wide gamut with acset seed
gay_seed!(0xb4545686b9115a09)

# Mixed mode checkpointing
params = OkhslParameters()
∂params = Enzyme.gradient(Reverse, loss, params, seed)
```

## Citation

> Patterson, Lynch, Fairbanks. Categorical data structures for technical computing. *Compositionality* 4, 5 (2022). [arXiv:2106.04703](https://arxiv.org/abs/2106.04703)

## Repository

- **Source**: plurigrid/ACSets.jl (fork of AlgebraicJulia/ACSets.jl)
- **Seed**: `0xb4545686b9115a09`
- **Index**: 494/1055
- **Color**: #204677

## GF(3) Triad

```
algebraic-rewriting (-1) ⊗ acsets-hatchery (0) ⊗ gay-monte-carlo (+1) = 0 ✓
```

## Related Skills

- `acsets-algebraic-databases` - Full ACSet guide
- `specter-acset` - Bidirectional navigation
- `world-a` - AlgebraicJulia ecosystem
