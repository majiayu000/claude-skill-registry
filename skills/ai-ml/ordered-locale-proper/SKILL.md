---
name: ordered-locale
description: "Ordered Locales (Heunen-van der Schaaf 2024): Point-free topology with direction. Frame + compatible preorder with open cone conditions."
version: 1.0.0
---


# Ordered Locale Skill

> *"We extend Stone duality between topological spaces and locales to include order."*
> — Heunen & van der Schaaf, 2024

## Overview

An **ordered locale** is a locale (point-free topological space) equipped with a compatible preorder satisfying the **open cone condition**.

```
Ordered Locale = Frame + Preorder + Open Cones
```

## Key Definitions

### Frame (Locale)

A **frame** is a complete lattice where finite meets distribute over arbitrary joins:

```
a ∧ (⋁ᵢ bᵢ) = ⋁ᵢ (a ∧ bᵢ)
```

Equivalently: a complete Heyting algebra.

### Open Cone Condition

For a preorder ≤ on locale L, the **open cone condition** requires:

```
↑x = {y ∈ L : x ≤ y}  is an open in L  (upper cone)
↓x = {y ∈ L : y ≤ x}  is an open in L  (lower cone)
```

This ensures the order is "visible" to the topology.

### Ordered Locale (Definition 2.1, Heunen-van der Schaaf)

An **ordered locale** is a tuple (L, ≤) where:
1. L is a locale (frame of opens)
2. ≤ is a preorder on O(L)
3. The open cone condition holds

## Stone Duality Extended

```
┌────────────────────────┐     adjunction     ┌─────────────────────┐
│ Preordered Topological │ ←───────────────→ │   Ordered Locales   │
│ Spaces (open cones)    │                    │     (spatial)       │
└────────────────────────┘                    └─────────────────────┘
```

Restricts to an **equivalence**:
- Spatial ordered locales ≃ Sober T₀-ordered spaces with open cones

## Julia Implementation (Catlab.jl)

### Frame as Subobject Heyting Algebra

From Catlab's `Subobjects.jl`:

```julia
using Catlab, Catlab.Theories, Catlab.CategoricalAlgebra

# Frame operations via ThSubobjectHeytingAlgebra
@signature ThFrame <: ThSubobjectHeytingAlgebra begin
  # Infinite joins (frame-specific)
  Join(I::TYPE, f::(I → Sub(X)))::Sub(X) ⊣ [X::Ob]
  
  # Frame distributivity: a ∧ (⋁ᵢ bᵢ) = ⋁ᵢ (a ∧ bᵢ)
end
```

### Ordered Locale Schema (ACSet)

```julia
using ACSets

@present SchOrderedLocale(FreeSchema) begin
  Open::Ob                    # Opens of the frame
  Arrow::Ob                   # Order relation arrows
  
  src::Hom(Arrow, Open)       # Source of order arrow
  tgt::Hom(Arrow, Open)       # Target of order arrow
  
  # Cone structure
  Cone::Ob
  apex::Hom(Cone, Open)       # Apex of cone
  leg::Hom(Cone, Arrow)       # Legs of cone
  
  # Attributes
  Index::AttrType
  idx::Attr(Open, Index)      # Open index
  is_upper::Attr(Cone, Bool)  # Upper vs lower cone
end

@acset_type OrderedLocale(SchOrderedLocale)
```

### Open Cone Verification

```julia
function verify_open_cone_condition(L::OrderedLocale)
  """
  Verify that ↑x and ↓x are opens for all x.
  """
  opens = parts(L, :Open)
  
  for x in opens
    # Upper cone: ↑x = {y : x ≤ y}
    upper_cone = Set{Int}()
    for arr in parts(L, :Arrow)
      if L[arr, :src] == x
        push!(upper_cone, L[arr, :tgt])
      end
    end
    push!(upper_cone, x)  # Reflexive
    
    # Check upper cone is an open (exists in frame)
    if !is_open(L, upper_cone)
      return false, "↑$x is not an open"
    end
    
    # Lower cone: ↓x = {y : y ≤ x}
    lower_cone = Set{Int}()
    for arr in parts(L, :Arrow)
      if L[arr, :tgt] == x
        push!(lower_cone, L[arr, :src])
      end
    end
    push!(lower_cone, x)  # Reflexive
    
    if !is_open(L, lower_cone)
      return false, "↓$x is not an open"
    end
  end
  
  return true, "Open cone condition satisfied"
end
```

### Cone and Cocone Operations

From Catlab's `Limits.jl`:

```julia
using Catlab.Theories: ThCompleteCategory, ThCocompleteCategory

# Cone: A natural transformation Δ(X) → D
# where Δ(X) is the constant diagram at X
struct Cone{Ob, Hom}
  apex::Ob
  legs::Vector{Hom}  # One leg per object in diagram
end

# Cocone: Dual - natural transformation D → Δ(X)
struct Cocone{Ob, Hom}
  apex::Ob
  legs::Vector{Hom}
end

# Limit = universal cone
function limit_cone(diagram::FreeDiagram, model)
  # Find apex and legs such that any other cone factors through
  lim = limit[model](diagram)
  Cone(ob(lim), collect(legs(lim)))
end

# Colimit = universal cocone  
function colimit_cocone(diagram::FreeDiagram, model)
  colim = colimit[model](diagram)
  Cocone(ob(colim), collect(legs(colim)))
end
```

### Frame Operations via Limits/Colimits

```julia
# Meet (∧) = pullback = limit of cospan
function frame_meet(L::OrderedLocale, a::Int, b::Int)
  # Pullback in the locale category
  diagram = FreeDiagram([a, b], [(a, top(L)), (b, top(L))])
  lim = limit_cone(diagram, L)
  return lim.apex
end

# Join (∨) = pushout = colimit of span
function frame_join(L::OrderedLocale, a::Int, b::Int)
  # Pushout in the locale category
  bot = bottom(L)
  diagram = FreeDiagram([a, b], [(bot, a), (bot, b)])
  colim = colimit_cocone(diagram, L)
  return colim.apex
end

# Infinite join (frame-specific)
function frame_sup(L::OrderedLocale, opens::Vector{Int})
  # Colimit of discrete diagram
  diagram = FreeDiagram(opens, Pair{Int,Int}[])
  colim = colimit_cocone(diagram, L)
  return colim.apex
end

# Heyting implication: a ⇒ b = ⋁{c : a ∧ c ≤ b}
function frame_implies(L::OrderedLocale, a::Int, b::Int)
  candidates = [c for c in parts(L, :Open) 
                if below_or_eq(L, frame_meet(L, a, c), b)]
  return frame_sup(L, candidates)
end
```

## GF(3) Triads

```
acsets (-1) ⊗ ordered-locale (0) ⊗ topos-generate (+1) = 0 ✓  [Schema]
sheaf-cohomology (-1) ⊗ ordered-locale (0) ⊗ kan-extensions (+1) = 0 ✓  [Gluing]
directed-interval (-1) ⊗ ordered-locale (0) ⊗ mlx-apple-silicon (+1) = 0 ✓  [Scale]
```

## Example Locales

### 1. Sierpinski Locale (2-point)

```julia
function sierpinski_locale()
  L = OrderedLocale{Bool}()
  add_parts!(L, :Open, 2, idx=[false, true])  # ⊥, ⊤
  add_part!(L, :Arrow, src=1, tgt=2)          # ⊥ < ⊤
  
  # Cones
  add_part!(L, :Cone, apex=2, is_upper=true)  # ↑⊥ = {⊥,⊤} = ⊤
  add_part!(L, :Cone, apex=1, is_upper=false) # ↓⊤ = {⊥,⊤} = ⊤
  L
end
```

### 2. Diamond Locale

```julia
function diamond_locale()
  L = OrderedLocale{Int}()
  add_parts!(L, :Open, 4, idx=[0, 1, 1, 2])  # ⊥, a, b, ⊤
  add_part!(L, :Arrow, src=1, tgt=2)  # ⊥ < a
  add_part!(L, :Arrow, src=1, tgt=3)  # ⊥ < b
  add_part!(L, :Arrow, src=2, tgt=4)  # a < ⊤
  add_part!(L, :Arrow, src=3, tgt=4)  # b < ⊤
  L
end
```

### 3. Scott Topology (Domain Theory)

```julia
function scott_locale(poset::OrderedLocale)
  """
  Scott topology: opens are upper sets closed under directed joins.
  """
  scott_opens = Vector{Set{Int}}()
  
  for u in parts(poset, :Open)
    upset = upper_cone(poset, u)
    if is_scott_open(poset, upset)
      push!(scott_opens, upset)
    end
  end
  
  scott_opens
end

function is_scott_open(L, U::Set{Int})
  # U is Scott-open iff:
  # 1. U is upper-closed
  # 2. For any directed D with ⋁D ∈ U, some d ∈ D is in U
  is_upper_closed(L, U) && is_inaccessible_by_directed_joins(L, U)
end
```

## Comparison with Implementation

| Aspect | ordered_locale_mlx.py | Proper Ordered Locale |
|--------|----------------------|----------------------|
| Structure | Adjacency matrix (poset) | Frame + ACSet schema |
| Opens | Finite indices | Complete Heyting algebra |
| Meets/Joins | Graph search | Pullback/Pushout (categorical) |
| Cones | Not implemented | Cone/Cocone with legs |
| Open Cone Condition | Not checked | `verify_open_cone_condition` |
| Infinite joins | No | `frame_sup` |

## Applications

1. **Spacetime Causality** — Order = causal influence, no points
2. **Domain Theory** — Way-below relation, compact elements
3. **Directed Homotopy** — Irreversible paths (directed-interval)
4. **Modal Logic** — Accessibility relations as order
5. **Concurrent Computing** — Partial order of events

## Commands

```bash
# Run ordered locale demo
just ordered-locale-demo

# Verify open cone condition
just ordered-locale-verify

# Scale test with MLX
just ordered-locale-mlx
```

## Files

- `ordered_locale.jl` — Julia implementation with Catlab
- `ordered_locale_mlx.py` — MLX-accelerated (finite approximation)
- `frame.jl` — Frame operations via limits/colimits
- `cone_cocone.jl` — Cone/cocone constructions

## References

1. Heunen, C. & van der Schaaf, N. (2024). "Ordered Locales." *J. Pure Appl. Algebra* 228(7), 107654.
2. Heunen, C. & van der Schaaf, N. (2025). "Causal Coverage in Ordered Locales and Spacetimes." arXiv:2510.17417.
3. Johnstone, P. (1982). *Stone Spaces*. Cambridge University Press.
4. Catlab.jl — `src/theories/Limits.jl`, `src/categorical_algebra/cats/Subobjects.jl`

---

**Skill Name**: ordered-locale
**Type**: Point-free Topology / Frame Theory / Directed Order
**Trit**: 0 (ERGODIC - coordinator)
**GF(3)**: Mediates between schema (-1) and generation (+1)
**Open Cones**: ↑x and ↓x must be opens
**Duality**: Spatial ordered locales ≃ Sober T₀-ordered spaces



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

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