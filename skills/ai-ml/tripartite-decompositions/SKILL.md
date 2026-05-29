---
name: tripartite-decompositions
description: GF(3)-balanced structured decompositions for parallel computation. Decomposes problems into MINUS/ERGODIC/PLUS components with sheaf-theoretic gluing. Use for FPT algorithms, skill allocation, or any 3-way parallel workload.
version: 1.0.0
---


# Tripartite Decompositions

**Trit**: 0 (ERGODIC - coordinates decomposition)  
**Foundation**: StructuredDecompositions.jl + GF(3) conservation  
**Principle**: Every problem decomposes into 3 parts summing to 0 mod 3

## Core Concept

A **tripartite decomposition** is a structured decomposition where:
1. The decomposition shape is a 3-clique (triangle)
2. Each bag is labeled with a trit ∈ {-1, 0, +1}
3. Adhesions preserve GF(3) conservation: Σ trits ≡ 0 (mod 3)

```
        MINUS (-1)
           ╱╲
          ╱  ╲
         ╱    ╲
        ╱  ⊗   ╲
       ╱________╲
 ERGODIC (0)   PLUS (+1)
 
 Conservation: (-1) + 0 + (+1) = 0 ✓
```

## Mathematical Foundation

### From StructuredDecompositions.jl

```julia
# A structured decomposition is a diagram d: ∫G → Span(C)
# where G is the decomposition shape and C is the target category

abstract type StructuredDecomposition{G, C, D} <: Diagram{id, C, D} end

struct StrDecomp{G, C, D} <: StructuredDecomposition{G, C, D}  
  decomp_shape ::G          # The shape (for tripartite: K₃)
  diagram      ::D          # The actual decomposition functor
  decomp_type  ::DecompType # Decomposition or CoDecomposition
  domain       ::C          # Source category
end
```

### Tripartite Extension

```julia
using StructuredDecompositions
using Catlab

# Define the tripartite shape: K₃ (complete graph on 3 vertices)
@present SchTripartite(FreeSchema) begin
    (Minus, Ergodic, Plus)::Ob
    
    # Adhesions (edges of K₃)
    me::Hom(Minus, Ergodic)
    ep::Hom(Ergodic, Plus)
    pm::Hom(Plus, Minus)
    
    # Trit attributes
    trit::Attr(Minus, Int)   # Always -1
    trit::Attr(Ergodic, Int) # Always 0
    trit::Attr(Plus, Int)    # Always +1
end

@acset_type TripartiteShape(SchTripartite)

# Tripartite decomposition with GF(3) verification
struct TripartiteDecomp{C, D} <: StructuredDecomposition{TripartiteShape, C, D}
    base::StrDecomp{TripartiteShape, C, D}
    
    function TripartiteDecomp(base::StrDecomp)
        # Verify GF(3) conservation
        trits = [
            ob_map(base.diagram, :Minus).trit,   # -1
            ob_map(base.diagram, :Ergodic).trit, # 0
            ob_map(base.diagram, :Plus).trit     # +1
        ]
        @assert sum(trits) % 3 == 0 "GF(3) violation"
        new{typeof(base.domain), typeof(base.diagram)}(base)
    end
end
```

## The 𝐃 Functor (Lifting Problems)

```julia
# From StructuredDecompositions.jl:
# 𝐃 : Cat_{pullback} → Cat
# Takes any category C with pullbacks to 𝐃C (structured decompositions over C)

# For tripartite decompositions, we lift computational problems:
function lift_problem(F::Functor, d::TripartiteDecomp)
    # F: C → FinSet^op is a sheaf (computational problem)
    # Returns: F applied to each bag, with sheaf condition on adhesions
    
    minus_solution = F(bag(d, :Minus))
    ergodic_solution = F(bag(d, :Ergodic))
    plus_solution = F(bag(d, :Plus))
    
    # Glue via adhesion spans
    return glue_tripartite(minus_solution, ergodic_solution, plus_solution, d)
end
```

## Random Walk 3-at-a-Time

Decompose a set of N items into balanced triplets:

```python
from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass
class TripartiteItem:
    name: str
    trit: int  # -1, 0, or +1
    data: any

class TripartiteDecomposer:
    """Decompose items into GF(3)-balanced triplets."""
    
    def __init__(self, seed: int):
        self.rng = SplitMix64(seed)
    
    def decompose(self, items: List[TripartiteItem]) -> List[Tuple]:
        """Random walk 3-at-a-time through items."""
        remaining = list(items)
        triplets = []
        
        while len(remaining) >= 3:
            # Select 3 items via PRNG
            selected = []
            for _ in range(3):
                idx = self.rng.next() % len(remaining)
                selected.append(remaining.pop(idx))
            
            # Check GF(3) conservation
            trit_sum = sum(item.trit for item in selected) % 3
            conserved = (trit_sum == 0)
            
            triplets.append((selected, conserved))
        
        # Handle remainder (incomplete triplet)
        if remaining:
            triplets.append((remaining, None))
        
        return triplets
    
    def entropy(self, items: List[TripartiteItem]) -> float:
        """Calculate Shannon entropy of trit distribution."""
        counts = {-1: 0, 0: 0, +1: 0}
        for item in items:
            counts[item.trit] += 1
        
        total = len(items)
        H = 0.0
        for count in counts.values():
            if count > 0:
                p = count / total
                H -= p * math.log2(p)
        return H
```

## Skill Allocation Example

From TRIPARTITE_AGENTS.md:

```
┌─────────────────────────────────────────────────────────────────────┐
│  MINUS (-1)          ERGODIC (0)           PLUS (+1)               │
│  Purple, 270°        Cyan, 180°            Orange, 30°             │
│                                                                     │
│  bisimulation-game   unwiring-arena        gay-mcp                 │
│  spi-parallel-verify acsets                triad-interleave        │
│  polyglot-spi        skill-dispatch        world-hopping           │
│  structured-decomp   bumpus-narratives     cognitive-superpos      │
└─────────────────────────────────────────────────────────────────────┘
```

Each agent receives skills matching its polarity. The sum is always 0.

## FPT Algorithms

Tripartite decompositions enable Fixed-Parameter Tractable algorithms:

```julia
# 3-coloring is decidable in O(3^w * n) where w = treewidth
# For tripartite shape, w = 2 (K₃ has treewidth 2)

function decide_3colorable(G::Graph, decomp::TripartiteDecomp)
    # Lift 3-coloring sheaf to decomposition
    coloring_sheaf = Functor(Graph, FinSet) do g
        # Return set of valid 3-colorings
        all_colorings(g, 3)
    end
    
    # Apply 𝐃 functor
    lifted = 𝐃(coloring_sheaf, decomp)
    
    # Check if limit is non-empty (solution exists)
    return !isempty(limit(lifted))
end
```

## Dynamic Programming Connection

Tripartite decomposition fixes DP failures:

| DP Failure | Tripartite Fix |
|------------|----------------|
| No base case | MINUS bag provides constraints |
| Invalid transition | Adhesions encode valid moves |
| State explosion | 3-way parallel reduces to O(3^w) |
| No memoization | Sheaf condition caches subproblems |

## Color Integration

Each bag gets a deterministic color:

```python
from gay import SplitMixTernary

def color_tripartite(seed: int):
    gen = SplitMixTernary(seed)
    return {
        'minus': gen.color_at(0),    # H ∈ [180°, 300°)
        'ergodic': gen.color_at(1),  # H ∈ [60°, 180°)
        'plus': gen.color_at(2)      # H ∈ [0°, 60°) ∪ [300°, 360°)
    }
```

## Gluing via Adhesions

```julia
function glue_tripartite(minus, ergodic, plus, decomp)
    # Adhesion spans connect bags
    me_span = adhesionSpan(decomp, :me)  # Minus ← Apex → Ergodic
    ep_span = adhesionSpan(decomp, :ep)  # Ergodic ← Apex → Plus
    pm_span = adhesionSpan(decomp, :pm)  # Plus ← Apex → Minus
    
    # Pullback along adhesions
    me_glued = pullback(minus, ergodic, me_span)
    ep_glued = pullback(ergodic, plus, ep_span)
    pm_glued = pullback(plus, minus, pm_span)
    
    # Final result is limit of glued diagram
    return limit(FreeDiagram([me_glued, ep_glued, pm_glued]))
end
```

## Validation

```bash
# Verify a tripartite decomposition
function verify_tripartite(decomp)
    bags = [bag(decomp, :Minus), bag(decomp, :Ergodic), bag(decomp, :Plus)]
    trits = [b.trit for b in bags]
    
    @assert sum(trits) % 3 == 0 "GF(3) violated"
    @assert length(adhesionSpans(decomp)) == 3 "Must have 3 adhesions"
    
    return true
end
```

## Usage Example

```julia
using StructuredDecompositions
using Catlab

# Decompose a skill validation problem
skills = [
    Skill("julia-gay", -1),      # Missing SKILL.md
    Skill("acsets", +1),         # Content overflow  
    Skill("mcp-tripartite", 0),  # YAML error
]

# Create tripartite decomposition
decomp = TripartiteDecomp(
    StrDecomp(K3_graph(), 
        FinDomFunctor(
            Dict(:Minus => skills[1], :Ergodic => skills[3], :Plus => skills[2]),
            Dict(:me => span_me, :ep => span_ep, :pm => span_pm)
        )
    )
)

# Verify and solve
@assert verify_tripartite(decomp)
solutions = lift_problem(validation_sheaf, decomp)
```

## Canonical Triads

```
structured-decomp (-1) ⊗ tripartite-decompositions (0) ⊗ gay-mcp (+1) = 0 ✓
bisimulation-game (-1) ⊗ entropy-sequencer (0) ⊗ triad-interleave (+1) = 0 ✓
spi-parallel-verify (-1) ⊗ acsets (0) ⊗ world-hopping (+1) = 0 ✓
```

## See Also

- `structured-decomp` - FPT via tree decompositions
- `gay-mcp` - Deterministic color generation
- `entropy-sequencer` - Information-gain ordering
- `triad-interleave` - 3-stream parallel execution



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `algorithms`: 19 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
tripartite-decompositions (○) + SDF.Ch10 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch9: Generic Procedures
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch7: Propagators

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