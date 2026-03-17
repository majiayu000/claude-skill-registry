# SKILL: ACSets Relational Thinking

**Version**: 2.0.0
**Trit**: 0 (ERGODIC)
**Domain**: database, category-theory, rewriting
**Source**: Topos Institute RelationalThinking Course + AlgebraicJulia

---

## Overview

ACSets (Attributed C-Sets) are **functors X: C → Set** where C is a small category (schema). This skill integrates:

1. **RelationalThinking Course** - Topos Institute's pedagogical approach
2. **DPO Rewriting** - Double Pushout graph transformation
3. **Self-Play Loop** - Query → Execute → Evaluate → Refine
4. **GF(3) Conservation** - Triadic skill composition

---

## Core Concept: C-Set as Functor

```
Schema (Category C)          Instance (Functor X: C → Set)
┌─────────────────┐          ┌─────────────────────────────┐
│  E ──src──→ V   │    X     │  X(E) = {e1, e2, e3}        │
│    ←──tgt──     │   ───→   │  X(V) = {v1, v2}            │
└─────────────────┘          │  X(src): e1↦v1, e2↦v1, e3↦v2│
                             │  X(tgt): e1↦v2, e2↦v2, e3↦v1│
                             └─────────────────────────────┘
```

---

## Schema Definition

### Basic Graph Schema
```julia
using Catlab.CategoricalAlgebra

@present SchGraph(FreeSchema) begin
  V::Ob                    # Vertices (object)
  E::Ob                    # Edges (object)
  src::Hom(E, V)           # Source morphism
  tgt::Hom(E, V)           # Target morphism
end

@acset_type Graph(SchGraph, index=[:src, :tgt])
```

### Entity-Subtype Hierarchy (from RelationalThinking Ch8)
```julia
@present SchKitchen(FreeSchema) begin
  Entity::Ob
  
  Food::Ob
  food_in_on::Hom(Food, Entity)
  food_is_entity::Hom(Food, Entity)
  
  Kitchenware::Ob
  ware_in_on::Hom(Kitchenware, Entity)
  ware_is_entity::Hom(Kitchenware, Entity)
  
  BreadLoaf::Ob
  bread_loaf_is_food::Hom(BreadLoaf, Food)
  Knife::Ob
  knife_is_ware::Hom(Knife, Kitchenware)
end

@acset_type Kitchen(SchKitchen)
```

---

## DPO Rewriting (Double Pushout)

### The Pattern: L ← K → R

```
     L ←──l── K ──r──→ R
     │        │        │
match│        │        │
     ↓        ↓        ↓
     G ←───── D ──────→ H
       pushout      pushout
       complement
```

- **L** = Find (what to match)
- **K** = Keep (overlap preserved)
- **R** = Replace (new structure)
- **G** = Host graph
- **H** = Result graph

### Rule Definition
```julia
using AlgebraicRewriting

# Slice bread rule: adds BreadSlice when knife + loaf present
slice_bread = @migration(SchKitchen, begin
  L => @join begin
    loaf::BreadLoaf
    knife::Knife
  end
  R => @join begin
    loaf::BreadLoaf
    slice::BreadSlice
    food_in_on(bread_slice_is_food(slice)) == food_in_on(bread_loaf_is_food(loaf))
    knife::Knife
  end
  K => @join begin
    loaf::BreadLoaf
    knife::Knife
  end
end)

rule = make_rule(slice_bread, yKitchen)
```

### Apply Rewrite
```julia
matches = get_matches(rule, state)
new_state = rewrite_match(rule, matches[1])
```

---

## Self-Play Loop

The ACSet self-refinement monad:

```
Query₀ → Execute → Evaluate → Mine Patterns → Refine → Query₁ → ...
```

### Implementation
```julia
struct SelfRefinementLoop
  schema::Presentation
  state::ACSet
  patterns::Vector{Pattern}
  generation::Int
end

function step!(loop::SelfRefinementLoop, rule::Rule)
  # Find matches
  matches = get_matches(rule, loop.state)
  
  # Evaluate each match
  evaluations = [evaluate_match(m, loop.patterns) for m in matches]
  
  # Mine new patterns from successful evaluations
  new_patterns = mine_patterns(evaluations)
  append!(loop.patterns, new_patterns)
  
  # Apply best match
  best = argmax(e -> e.score, evaluations)
  loop.state = rewrite_match(rule, matches[best.index])
  loop.generation += 1
  
  loop
end
```

### Convergence Criterion
```julia
function converged(loop::SelfRefinementLoop; threshold=0.95)
  recent = loop.patterns[end-10:end]
  stability = std([p.score for p in recent])
  stability < (1 - threshold)
end
```

---

## GF(3) Integration

### Trit Assignment
```julia
function acset_to_trits(g::Graph, seed::UInt64)
  rng = SplitMix64(seed)
  trits = Int[]
  for e in parts(g, :E)
    h = next_u64!(rng)
    hue = (h >> 16 & 0xffff) / 65535.0 * 360
    trit = hue < 60 || hue >= 300 ? 1 :
           hue < 180 ? 0 : -1
    push!(trits, trit)
  end
  trits
end

# Conservation check
gf3_conserved(trits) = sum(trits) % 3 == 0
```

### Synergistic Triads Containing ACSets
```
clj-kondo-3color (-1) ⊗ acsets (0) ⊗ rama-gay-clojure (+1) = 0 ✓
three-match (-1) ⊗ acsets (0) ⊗ gay-mcp (+1) = 0 ✓
slime-lisp (-1) ⊗ acsets (0) ⊗ cider-clojure (+1) = 0 ✓
hatchery-papers (-1) ⊗ acsets (0) ⊗ frontend-design (+1) = 0 ✓
```

---

## Orthogonal Bundles

ACSets participates in the **STRUCTURAL** bundle:

| Direction | Skills | Behavior |
|-----------|--------|----------|
| STRUCTURAL | clj-kondo(-1) ⊗ acsets(0) ⊗ rama-gay(+1) | Schema validation → transport → generation |
| TEMPORAL | three-match(-1) ⊗ unworld(0) ⊗ gay-mcp(+1) | Reduction → derivation → coloring |
| STRATEGIC | proofgeneral(-1) ⊗ glass-bead(0) ⊗ rubato(+1) | Verification → hopping → composition |

---

## Visual Conventions (from RelationalThinking)

| Concept | Visual |
|---------|--------|
| Schema object | Gray circle |
| Schema morphism | Colored arrow (cyan=src, blue=tgt) |
| Instance element | Filled shape |
| Morphism mapping | Slot/containment |
| Pushout | Merged regions with distinct colors |
| DPO rule | Thought bubble (L,K,R) |

---

## Commands

```bash
# Schema operations
just acset-schema FILE       # Display schema diagram
just acset-instance FILE     # Display instance elements
just acset-morphism F G      # Show homomorphism F → G

# DPO rewriting
just acset-rule RULE STATE   # Apply rewrite rule
just acset-matches RULE STATE # Find all matches
just acset-chain RULES STATE # Chain multiple rewrites

# Self-play
just acset-selfplay SCHEMA   # Run self-refinement loop
just acset-patterns STATE    # Mine patterns from state
just acset-converge SCHEMA   # Run until convergence

# GF(3) operations
just acset-trits STATE SEED  # Color state with seed
just acset-gf3 STATE         # Check GF(3) conservation
just acset-triads            # Show synergistic triads
```

---

## References

### Topos Institute
- [RelationalThinking Book](https://toposinstitute.github.io/RelationalThinking-Book/)
- [RelationalThinking Code](https://github.com/ToposInstitute/RelationalThinking-code)

### AlgebraicJulia
- [Catlab.jl](https://github.com/AlgebraicJulia/Catlab.jl)
- [ACSets.jl](https://github.com/AlgebraicJulia/ACSets.jl)
- [AlgebraicRewriting.jl](https://github.com/AlgebraicJulia/AlgebraicRewriting.jl)

### Papers
- Patterson et al. "Categorical data structures for technical computing" (Compositionality 2022)
- Aguinaldo et al. "Categorical Representation Language for Knowledge-Based Planning" (AAAI 2023)

---

## Related Skills

- `rama-gay-clojure` (+1) - Scalable backends with color tracing
- `clj-kondo-3color` (-1) - Schema validation/linting
- `glass-bead-game` (0) - World hopping across schemas
- `unworld` (0) - Derivational chains for state evolution
- `discohy-streams` (0) - DisCoPy categorical color streams

---

**Skill Name**: acsets-relational-thinking
**Type**: Category-Theoretic Database / DPO Rewriting
**Trit**: 0 (ERGODIC)
**GF(3)**: Conserved via triadic composition
