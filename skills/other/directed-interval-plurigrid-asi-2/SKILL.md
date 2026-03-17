---
name: directed-interval
description: Directed interval type 2 axiomatizing (0 → 1). Time-directed homotopy
  for reactions.
metadata:
  trit: 0
  polarity: ERGODIC
  source: 'Riehl-Shulman 2017: directed cubes and extension types'
  technologies:
  - Rzk
  - Cubical Agda
---

# Directed Interval Skill

> *"The directed interval 2 is the walking arrow: a single morphism 0 → 1."*
> — Riehl-Shulman

## Overview

The **directed interval 2** replaces the undirected interval 𝕀 of cubical type theory with a directed version. This axiomatizes the notion of "time flows forward" essential for modeling reactions.

## Core Definitions (Rzk)

```rzk
#lang rzk-1

-- CUBES: The category of directed cubes
-- 2 is the basic directed interval [0 → 1]

-- The directed interval (primitive)
#define 2 : CUBE

-- Endpoints
#define 0₂ : 2
#define 1₂ : 2

-- The unique arrow (built-in)
-- There is a morphism 0₂ → 1₂ but NOT 1₂ → 0₂

-- Higher cubes built from 2
#define 2×2 : CUBE := 2 × 2

-- Directed square (all arrows point same way)
#define □ : CUBE := 2 × 2

-- Simplex shapes
#define Δ¹ : CUBE := 2
#define Δ² : CUBE := { (t₁, t₂) : 2 × 2 | t₁ ≤ t₂ }
#define Δ³ : CUBE := { (t₁, t₂, t₃) : 2 × 2 × 2 | t₁ ≤ t₂ ∧ t₂ ≤ t₃ }

-- Hom type as extension type
#define hom (A : U) (x y : A) : U
  := { f : 2 → A | f 0₂ = x ∧ f 1₂ = y }
  -- equivalently: (t : 2) → A [t ≡ 0₂ ↦ x, t ≡ 1₂ ↦ y]
```

## Chemputer Semantics

| Directed Cube Concept | Chemical Interpretation |
|----------------------|------------------------|
| 2 (interval) | Reaction progress (0% → 100%) |
| 0₂ | Reactants (starting materials) |
| 1₂ | Products |
| hom A x y | Reaction pathway from x to y |
| Δ² | Two-step synthesis (A → B → C) |
| Δ³ | Three-step synthesis with associativity |
| □ (square) | Commuting reaction pathways |

## GF(3) Triad

```
segal-types (-1) ⊗ directed-interval (0) ⊗ rezk-types (+1) = 0 ✓
```

As a **Coordinator (0)**, directed-interval:
- Mediates between validators and generators
- Provides the "time axis" for computation
- Enables transport along directed paths

## Extension Types

The key innovation is **extension types** for partial elements:

```rzk
-- Extension type: functions with prescribed boundary
#define extension-type 
  (I : CUBE) (ψ : I → TOPE) (A : I → U) (a : (t : ψ) → A t) : U
  := { f : (t : I) → A t | (t : ψ) → f t = a t }

-- This generalizes path types of cubical TT to directed setting
```

## SplitMix64 Time Axis

```ruby
# The directed interval in our system
module DirectedInterval
  # Map SplitMix64 index to directed interval position
  def self.to_interval(index, max_index)
    # 0₂ = index 0, 1₂ = index max_index
    index.to_f / max_index.to_f
  end
  
  # Check if one interaction is "after" another in directed time
  def self.after?(i1, i2)
    i1.epoch > i2.epoch  # Epoch = position on directed interval
  end
  
  # Directed hom: all interactions from x to y
  def self.hom(manager, x_epoch, y_epoch)
    manager.interactions.select do |i|
      i.epoch > x_epoch && i.epoch <= y_epoch
    end
  end
end
```

## Julia ACSet Integration

```julia
# Directed interval as ACSet
@present SchDirectedInterval(FreeSchema) begin
  Point::Ob
  Arrow::Ob
  
  src::Hom(Arrow, Point)
  tgt::Hom(Arrow, Point)
  
  # The unique arrow 0 → 1
  # No arrow 1 → 0 (directedness)
end

@acset_type DirectedIntervalGraph(SchDirectedInterval)

function walking_arrow()
  g = DirectedIntervalGraph()
  add_parts!(g, :Point, 2)  # 0₂ and 1₂
  add_part!(g, :Arrow, src=1, tgt=2)  # The unique arrow
  g
end
```

## Key Properties

1. **No loops**: There is no morphism 1₂ → 0₂ (time irreversibility)

2. **Higher simplices**: Δⁿ built from directed cubes model n-step processes

3. **Extension types**: Generalize path types to directed setting

4. **Cubical structure**: Compatible with cubical type theory machinery

## References

- Riehl, E. & Shulman, M. (2017). "A type theory for synthetic ∞-categories." §3.
- [Rzk documentation](https://rzk-lang.github.io/rzk/)
- Licata, D. & Harper, R. (2011). "2-Dimensional Directed Type Theory."
