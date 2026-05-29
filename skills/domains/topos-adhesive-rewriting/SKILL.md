---
name: topos-adhesive-rewriting
description: Adhesive categories for incremental query updating and pattern rewriting
version: 1.0.0
---


# SKILL: Topos Adhesive Rewriting

**Version**: 1.0.0
**Trit**: +1 (PLUS)
**Domain**: category-theory, rewriting, databases, incremental-computation
**Source**: Topos Institute Blog (Kris Brown)

---

## Overview

Adhesive categories provide a **general setting for pattern matching and rewriting** where pushouts along monomorphisms behave well. This skill covers:

1. **Incremental Query Updating** - Efficiently update query results when queried object changes
2. **Decompositions** - Q ≅ Q_G +_{Q_L} Q_R factorization
3. **Interactions** - Pullback squares between pattern subobjects and rewrite rules
4. **Rooted Search** - Transform subgraph isomorphism into rooted search problems
5. **Complements** - ∼A is smallest subobject where X = A ∨ ∼A

---

## Core Concept: The Incremental Search Problem

```
   Query Q          Old State G          New State H
  ┌───────┐        ┌───────────┐        ┌───────────┐
  │ a→b→c │   Hom  │  1 → 2 ↺  │   Δ    │  1→2↺     │
  └───────┘  ───→  └───────────┘  ───→  │   ↘3↙    │
                    matches:             └───────────┘
                    [1,2,2]              new matches:
                    [2,2,2]              [1,3,2], [3,2,2]
```

**Goal**: Compute `Hom(Q,H) \ Hom(Q,G)·Δ` efficiently without recomputing from scratch.

---

## Dictionary: Category Theory ↔ Computation

| Setting | Category Theory |
|---------|-----------------|
| Pattern/Query | Object Q ∈ Ob C |
| State of world | Object G ∈ Ob C |
| Pattern match | Morphism Q → G |
| Answer set | Hom_C(Q, G) |
| Additive rewrite rule | Monomorphism f: L ↣ R |
| Rule application | Pushout G →^Δ H ←^r R |

---

## The Adhesive Cube

For any match h: Q → H into a rewrite result, adhesivity gives a canonical decomposition:

```
           Q ≅ Q_R +_{Q_L} Q_G
              ╱     │     ╲
            Q_R    Q_L    Q_G
             │      │      │
             ↓      ↓      ↓
             R ←─── L ───→ G
              ╲     │     ╱
               ╲    ↓    ╱
                ─→ H ←──
```

**Key insight**: Every new match corresponds to a unique adhesive cube.

---

## Algorithm

### Compile Time (pre-computation)

```julia
# 1. Enumerate all decompositions Q ≅ Q_G +_{Q_L} Q_R
decompositions = enumerate_decompositions(Q)

# 2. Enumerate all interactions between Q_L ↣ Q_R and f: L ↣ R
for decomp in decompositions
    for rule in rules
        interactions[decomp, rule] = find_pullback_squares(decomp, rule)
    end
end
```

### Runtime (given match m: L → G)

```julia
function incremental_matches(Q, rule, match_m, G)
    new_matches = []
    
    for decomp in decompositions
        if decomp.Q_G == Q  # Skip trivial decomposition
            continue
        end
        
        for interaction in interactions[decomp, rule]
            # Find h_G: Q_G → G forming pullback with m and h_L
            partial_map = compose(interaction.h_L, match_m)
            
            for h_G in extend_partial_map(decomp.Q_G, partial_map, G)
                if forms_pullback(h_G, match_m, interaction)
                    h = [h_G ∘ Δ, interaction.h_R ∘ r]
                    push!(new_matches, h)
                end
            end
        end
    end
    
    return new_matches
end
```

---

## Complements Optimization

When C has complements, we can avoid filtering:

```julia
# Complement: ∼A is smallest subobject where X = A ∨ ∼A
# Boundary: ∂A = A ∧ ∼A

function optimized_incremental(Q, rule, match_m, G)
    # Only consider decompositions where Q_R = ∼Q_G
    minimal_decomps = filter(d -> d.Q_R == complement(d.Q_G, Q), decompositions)
    
    for decomp in minimal_decomps
        # All extensions are valid - no pullback filtering needed
        boundary_map = compose(boundary(decomp.Q_G), match_m)
        for h_G in extend(decomp.Q_G, boundary_map, G)
            yield_match(h_G, decomp)
        end
    end
end
```

---

## Julia Implementation with AlgebraicRewriting

```julia
using Catlab.CategoricalAlgebra
using AlgebraicRewriting

# Define schema (adhesive category of C-Sets)
@present SchGraph(FreeSchema) begin
    V::Ob; E::Ob
    src::Hom(E, V); tgt::Hom(E, V)
end
@acset_type Graph(SchGraph, index=[:src, :tgt])

# Define query: path of length 2 (a → b → c)
Q = @acset Graph begin
    V = 3; E = 2
    src = [1, 2]; tgt = [2, 3]
end

# Define rule: add triangle (edge becomes path of 2)
L = @acset Graph begin V = 2; E = 1; src = [1]; tgt = [2] end
R = @acset Graph begin V = 3; E = 3; src = [1, 1, 3]; tgt = [2, 3, 2] end

# Span L ← K → R (K is the preserved part)
K = @acset Graph begin V = 2 end
l = ACSetTransformation(K, L, V=[1, 2])
r = ACSetTransformation(K, R, V=[1, 2])
rule = Rule(l, r)

# State with loop
G = @acset Graph begin V = 2; E = 2; src = [1, 2]; tgt = [2, 2] end

# Find matches and apply rule
matches = get_matches(rule, G)
H, match_info = rewrite_match(rule, first(matches))

# Incremental update API
using AlgebraicRewriting: IncrementalHomSearch

# Precompute decompositions and interactions (compile time)
searcher = IncrementalHomSearch(Q, [rule])

# At runtime: find only NEW matches
new_matches = incremental_update(searcher, G, H, match_info)
```

---

## Batch Updates

Apply multiple rules simultaneously via colimit:

```
         L₁         L₂
         ↓ m₁       ↓ m₂
         G    ───→  H
         ↑          ↑
         R₁         R₂
```

```julia
# Batch rewrite: apply multiple rules at once
function batch_rewrite(rules_with_matches, G)
    # Compute colimit of all rewrites
    diagram = build_rewrite_diagram(rules_with_matches, G)
    H = colimit(diagram)
    
    # Find matches involving material from multiple rules
    for multicube in enumerate_multicubes(Q, rules_with_matches)
        for h_G in extend_multicube(multicube, G)
            yield_batch_match(h_G, multicube)
        end
    end
end
```

---

## Rooted Search Efficiency

**Key transformation**: Subgraph isomorphism → Rooted subgraph isomorphism

```
Unrooted (hard):          Rooted (easy):
Find Q in G               Find Q in G starting from partial match
  ┌─────┐                   ┌─────┐
  │  ?  │ in big G          │ 2→? │ in big G (vertex 2 fixed)
  └─────┘                   └─────┘
  
O(|V|^|Q|) worst case      O(deg^|Q|) typically
```

**Why it works**: Decompositions ensure Q_L ↣ Q_G is componentwise connected.

---

## GF(3) Integration

### Trit Assignment
```julia
# Adhesive rewriting is generative (+1)
# Creates new structure from patterns

function rewrite_trits(rule::Rule, seed::UInt64)
    rng = SplitMix64(seed)
    
    # Color newly created elements
    new_parts = setdiff(parts(rule.R), image(rule.K))
    trits = Dict()
    
    for part in new_parts
        h = next_u64!(rng)
        hue = (h >> 16 & 0xffff) / 65535.0 * 360
        trits[part] = hue < 60 || hue >= 300 ? 1 :
                      hue < 180 ? 0 : -1
    end
    
    trits
end
```

### Synergistic Triads
```
acsets-relational-thinking (-1) ⊗ glass-bead-game (0) ⊗ topos-adhesive (+1) = 0 ✓
three-match (-1) ⊗ unworld (0) ⊗ topos-adhesive (+1) = 0 ✓
gh-interactome (-1) ⊗ duckdb-temporal (0) ⊗ topos-adhesive (+1) = 0 ✓
```

---

## Integration Points

### With acsets-relational-thinking
```julia
# C-Set categories are adhesive!
# Rewriting works on any schema

@present SchKitchen(FreeSchema) begin
    Entity::Ob
    Food::Ob; food_is::Hom(Food, Entity)
    Knife::Ob; knife_is::Hom(Knife, Entity)
end

# Rules operate on kitchen states
slice_bread_rule = make_rule(...)

# Incremental query: "which foods can be sliced?"
query = @acset Kitchen begin ... end
searcher = IncrementalHomSearch(query, [slice_bread_rule])
```

### With GPU Kernels
```julia
# Batch parallel match finding on GPU
using CUDA

function gpu_incremental_update(searcher, G, H, match_info)
    # Decompositions precomputed on CPU
    decomps = searcher.decompositions
    
    # Parallel extension search on GPU
    partial_maps = prepare_partial_maps(decomps, match_info)
    candidates = CUDA.@cuda extend_all_parallel(partial_maps, G)
    
    # Filter valid matches
    filter_pullback_condition!(candidates)
end
```

### With gh-interactome (Author Graphs)
```julia
# Query: find collaboration patterns
collab_pattern = @acset AuthorGraph begin
    Author = 3; Paper = 1
    authored = [1, 2, 3]  # Three co-authors
end

# Rule: new paper adds collaboration edges
new_paper_rule = Rule(...)

# Track collaboration network evolution incrementally
searcher = IncrementalHomSearch(collab_pattern, [new_paper_rule])
```

---

## Commands

```bash
# Decomposition analysis
just adhesive-decompose QUERY        # Enumerate Q decompositions
just adhesive-interactions QUERY RULE # Find Q ↔ rule interactions
just adhesive-compile QUERY RULES    # Precompute all (compile time)

# Incremental search
just adhesive-update STATE RULE MATCH # Incremental match finding
just adhesive-batch STATE MATCHES     # Batch multi-rule update

# Complement operations
just adhesive-complement A X          # Compute ∼A in X
just adhesive-boundary A X            # Compute ∂A = A ∧ ∼A
just adhesive-minimal DECOMP          # Minimize decomposition

# Verification
just adhesive-verify-cube MATCH       # Check adhesive cube properties
just adhesive-benchmark QUERY STATE   # Compare incremental vs naive
```

---

## References

### Topos Institute
- [Incremental Query Updating in Adhesive Categories](https://topos.institute/blog/2025-08-15-incremental-adhesive/) (Kris Brown, 2025)
- [Substitution is Pushout](https://topos.institute/blog/2025-08-06-substitution-is-pushout/)
- [Agent-Based Modeling via Graph Rewriting](https://topos.institute/blog/2023-07-07-agent-based-modeling-graph-rewriting/)

### Papers
- Lack & Sobociński, "Adhesive and Quasiadhesive Categories" (RAIRO 2005)
- Patterson, Lynch, Fairbanks, "Categorical Data Structures for Technical Computing" (Compositionality 2022)
- Biondo, Castelnovo, Gadducci, "EGGs Are Adhesive!" (arXiv 2025)

### Implementations
- [AlgebraicRewriting.jl](https://github.com/AlgebraicJulia/AlgebraicRewriting.jl)
- [Catlab.jl](https://github.com/AlgebraicJulia/Catlab.jl)

---

## Related Skills

- `acsets-relational-thinking` (0) - C-Sets are adhesive categories
- `three-match` (-1) - Colored subgraph isomorphism gadgets  
- `gh-interactome` (-1) - Pattern matching on author collaboration graphs
- `duckdb-temporal-versioning` (0) - Incremental updates in time-travel queries
- `glass-bead-game` (0) - World hopping via pattern decomposition
- `julia-gpu-kernels` (+1) - Parallel batch match finding
- `coequalizers` (0) - Quotient redundant paths via pushout decomposition

---

**Skill Name**: topos-adhesive-rewriting
**Type**: Category-Theoretic Rewriting / Incremental Computation
**Trit**: +1 (PLUS - generative rewriting)
**GF(3)**: Conserved via triadic composition



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `category-theory`: 139 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
topos-adhesive-rewriting (○) + SDF.Ch10 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch8: Degeneracy

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.