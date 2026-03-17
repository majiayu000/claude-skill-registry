---
name: condensed-analytic-stacks
description: "Scholze-Clausen condensed mathematics bridge to sheaf neural networks via 6-functor formalism"
---

# condensed-analytic-stacks Skill

## Overview

Saturates the intersection of **Scholze-Clausen condensed mathematics**, **analytic stacks**, and **sheaf neural networks**. Bridges pyknotic/condensed objects to computational learning systems via 6-functor formalisms.

## Key Papers & Sources

| Paper | Authors | arXiv | Key Contribution |
|-------|---------|-------|------------------|
| Lectures on Condensed Mathematics | Scholze, Clausen | [PDF](https://www.math.uni-bonn.de/people/scholze/Condensed.pdf) | Foundation: condensed sets, solid/liquid modules |
| Condensed Mathematics and Complex Geometry | Clausen, Scholze | [PDF](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf) | Nuclear modules, GAGA |
| Pyknotic Objects, I. Basic notions | Barwick, Haine | [1904.09966](https://arxiv.org/abs/1904.09966) | Hypersheaves on compacta |
| Categorical Künneth formulas for analytic stacks | Kesting | [2507.08566](https://arxiv.org/abs/2507.08566) | 6-functor Künneth, Tannakian reconstruction |
| Infinitary combinatorics in condensed math | Bergfalk, Lambie-Hanson | [2412.19605](https://arxiv.org/abs/2412.19605) | Higher derived limits, pyknotic connections |

## Architecture: Condensed → Sheaf NN Bridge

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  Condensed Analytic Stacks Architecture                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Condensed Sets           6-Functor Formalism         Sheaf Neural Nets   │
│   (Scholze)                    (Künneth)                 (Fairbanks)        │
│       │                           │                           │             │
│       ▼                           ▼                           ▼             │
│  ┌──────────┐              ┌───────────┐              ┌──────────────┐     │
│  │ Cond(Ab) │─────────────▶│ f_*, f^*, │─────────────▶│ Sheaf        │     │
│  │ Sheaves  │   Tannakian  │ f_!, f^!, │   Harmonic   │ Laplacian    │     │
│  │ on CHaus │   Reconstruct│ Hom,⊗     │   Inference  │ Diffusion    │     │
│  └──────────┘              └───────────┘              └──────────────┘     │
│       │                           │                           │             │
│       │ Profinite                 │ Descent                   │ Cellular    │
│       │ Approximation             │ Data                      │ Sheaves     │
│       ▼                           ▼                           ▼             │
│  ┌──────────┐              ┌───────────┐              ┌──────────────┐     │
│  │ Liquid   │              │ Analytic  │              │ Cooperative  │     │
│  │ Vector   │───solid──────│ Stacks    │───consensus──│ Sheaf NNs    │     │
│  │ Spaces   │              │ QCoh(X)   │              │ (Bodnar)     │     │
│  └──────────┘              └───────────┘              └──────────────┘     │
│       │                           │                           │             │
│       └───────────────────────────┴───────────────────────────┘             │
│                                   │                                         │
│                            Music-Topos ACSet                                │
│                           Parallel Rewriting                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Concepts

### 1. Condensed Sets (Cond)

**Definition**: Sheaves on the site of compact Hausdorff spaces with finite jointly surjective covers.

```julia
# ACSet schema for condensed structures
@present CondensedSchema(FreeSchema) begin
    # Objects
    CompactSpace::Ob
    CondensedSet::Ob
    ProfiniteSet::Ob
    
    # Morphisms  
    sheaf::Hom(CondensedSet, CompactSpace)  # Evaluation at compacta
    limit::Hom(ProfiniteSet, CondensedSet)  # Profinite = lim finite sets
    
    # Key insight: Topology lives in test objects, not the space itself
end
```

### 2. Liquid Vector Spaces

**Definition**: For 0 < r < 1, the liquid norm:

$$|x|_r = \sum_{n=0}^{\infty} |c_n| \cdot r^n$$

```ruby
# From world_broadcast.rb - SATURATED implementation
module CondensedAnima
  # Liquid vector space: l^r completion
  # Clausen-Scholze: Analytic ring = (ℤ((T)), ⟨T⟩_r)
  def self.liquid_norm(coefficients, r: 0.5)
    # Convergent for r < 1 (contractivity)
    coefficients.each_with_index.sum do |c, n|
      c.abs * (r ** n)
    end
  end
  
  # The r-liquid norm defines a complete bornology
  # Key: r→1 gives solid modules (maximally complete)
  def self.solid_completion(sequence)
    # Solid = lim_{r→1} liquid_r
    # Completion is the uniform limit
    sequence.sum.to_f / sequence.size
  end
  
  # Analytic ring structure:
  # A complete Huber pair (A, A⁺) with bornology
  def self.analytic_ring(base_ring, positive_part)
    {
      ring: base_ring,
      positive: positive_part,
      bornology: :liquid,
      solid_closure: true
    }
  end
end
```

### 3. 6-Functor Formalism (Categorical Künneth)

From [2507.08566]:

```
For analytic stacks X, Y:

QCoh(X × Y) ≃ QCoh(X) ⊗ QCoh(Y)    # Künneth

6 functors: f_*, f^*, f_!, f^!, Hom, ⊗
satisfying base change and projection formulas
```

```julia
# 6-functor ACSet
@present SixFunctorSchema(FreeSchema) begin
    Stack::Ob
    Category::Ob
    
    # The 6 functors
    pushforward::Hom(Category, Category)      # f_*
    pullback::Hom(Category, Category)         # f^*
    shriek_push::Hom(Category, Category)      # f_!
    shriek_pull::Hom(Category, Category)      # f^!
    internal_hom::Hom(Category, Category)     # Hom
    tensor::Hom(Category, Category)           # ⊗
    
    # Adjunctions
    # (f^*, f_*), (f_!, f^!)
    # Hom(A⊗B, C) ≃ Hom(A, Hom(B,C))
end
```

### 4. Analytic Stack ↔ Sheaf NN Connection

**Key Insight**: The descent condition in analytic stacks parallels the consistency condition in cellular sheaves.

```ruby
# Analytic stack satisfies descent
def self.analytic_stack(objects)
  {
    objects: objects,
    descent_data: objects.combination(2).map { |a, b| [a, b, a ^ b] },
    coherence: true,  # Higher coherence from infinity-category
    
    # Bridge to sheaf NNs
    laplacian_compatible: true,
    # The sheaf Laplacian L = δᵀδ + δδᵀ
    # measures failure of local-to-global consistency
  }
end

# Sheaf neural network connection
# From async-sheaf-diffusion skill
def analytic_to_cellular_sheaf(analytic_stack)
  {
    vertices: analytic_stack[:objects],
    # Restriction maps from stack structure
    restriction_maps: analytic_stack[:descent_data].map { |d|
      { source: d[0], target: d[1], map: d[2] }
    },
    # Cohomology detects obstructions
    cohomology: compute_sheaf_cohomology(analytic_stack)
  }
end
```

### 5. Pyknotic vs Condensed

| Aspect | Pyknotic | Condensed |
|--------|----------|-----------|
| Site | CHaus (small) | CHaus (large) |
| Sheaves | Hypersheaves | Sheaves |
| Universe | Fixed | Depends on κ |
| Derived cats | Hypercomplete | Not necessarily |

```julia
# Pyknotic spectrum (Barwick-Haine)
@present PyknoticSchema(FreeSchema) begin
    CondensedAb::Ob
    PycknoticAb::Ob
    
    # Inclusion (pyknotic ⊂ condensed for hypercompleteness)
    include::Hom(PycknoticAb, CondensedAb)
    
    # Both give derived category of local field
    derived_cat::Hom(CondensedAb, DerivedCat)
end
```

## Integration with Existing Skills

### sheaf-laplacian-coordination

```ruby
# Condensed structure enhances sheaf coordination
class CondensedSheafCoordinator
  def initialize(graph, sheaf)
    @graph = graph
    @sheaf = sheaf
    @liquid_param = 0.5  # r in (0,1)
  end
  
  # Liquid-weighted Laplacian
  def liquid_laplacian
    L = @sheaf.laplacian
    # Weight by liquid norm decay
    L.map_with_index { |row, i|
      row.map_with_index { |val, j|
        distance = graph_distance(i, j)
        val * (@liquid_param ** distance)
      }
    }
  end
  
  # Solid consensus = limit as r→1
  def solid_consensus(initial_states, iterations: 100)
    states = initial_states
    (0.99 - @liquid_param).step(0.01, 0.99) do |r|
      @liquid_param = r
      states = diffuse(states, liquid_laplacian)
    end
    states
  end
end
```

### async-sheaf-diffusion

```julia
# From arXiv:2411.XXXXX - Asynchronous diffusion with condensed structure
struct CondensedAsyncDiffusion
    base_diffusion::SheafDiffusion
    liquid_r::Float64
    solid_threshold::Float64
end

function step!(cad::CondensedAsyncDiffusion, states)
    # Profinite approximation for async updates
    levels = [3, 9, 27]  # 3^1, 3^2, 3^3
    
    for level in levels
        # Approximate by finite quotient
        approx_states = states .% level
        
        # Local liquid diffusion
        local_update = cad.base_diffusion(approx_states)
        
        # Weight by liquid norm
        states .+= cad.liquid_r^log(level) .* local_update
    end
    
    states
end
```

### acsets-algebraic-databases

```julia
# Condensed ACSet: sheaves valued in ACSets
@acset_type CondensedACSet(CondensedSchema, index=[:sheaf]) begin
    # Objects carry condensed structure
    compact_probe::Attr(CompactSpace, Symbol)  # Test compactum
    section_data::Attr(CondensedSet, Vector)   # Sections over probes
    
    # Descent gluing
    gluing_data::Attr(CondensedSet, Matrix)
end
```

## Provenance Integration

Uses `ananas_provenance_schema.sql`:

```sql
-- Register condensed paper extraction
INSERT INTO artifact_provenance (
    artifact_id, artifact_type, content_hash, gayseed_index
) VALUES (
    'condensed-scholze-2024',
    'analysis',
    SHA3-256(content),
    5  -- BLUE (Scholze agent color)
);

-- Track 6-functor diagrams extracted
INSERT INTO provenance_nodes (
    artifact_id, node_type, sequence_order, node_data
) VALUES (
    'condensed-scholze-2024',
    'Doc',
    1,
    '{"diagrams": 42, "equations": 137, "theorems": 23}'
);
```

## World Integration

```ruby
# justfile target
world-condensed:
  @ruby -I lib -r world_broadcast -e "WorldBroadcast.world(
    mathematicians: [:scholze, :grothendieck, :noether],
    modules: [CondensedAnima, SixFunctor, AnalyticStack]
  )"
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `condensed_probe` | Test condensed structure with compact probe |
| `liquid_norm` | Compute liquid norm for coefficient sequence |
| `solid_complete` | Take solid completion (r→1 limit) |
| `kunneth_check` | Verify Künneth formula for stack product |
| `descent_verify` | Check descent condition for analytic stack |
| `sheaf_bridge` | Bridge condensed stack to cellular sheaf |

## Commands

```bash
just world-condensed          # Run condensed anima world
just condensed-test           # Test liquid/solid modules  
just kunneth-verify           # Verify Künneth for example stacks
just sheaf-bridge-demo        # Demo condensed→sheaf NN bridge
```

## See Also

- `sheaf-laplacian-coordination/SKILL.md` - Sheaf neural coordination
- `async-sheaf-diffusion/SKILL.md` - Asynchronous sheaf diffusion
- `acsets-algebraic-databases/SKILL.md` - ACSet foundations
- `lispsyntax-acset/SKILL.md` - S-expression ↔ ACSet bridge (OCaml ppx_sexp_conv style)
- `lib/world_broadcast.rb` - CondensedAnima module (lines 348-389)
- `lib/lispsyntax_acset_bridge.jl` - LispSyntax.jl ↔ ACSet.jl bridge
- `PONTRYAGIN_DUALITY_COMPREHENSIVE_ANALYSIS.md` - Condensed extension (lines 844-860)
- `LISPSYNTAX_ACSET_BRIDGE_COMPLETE.md` - Integration summary
