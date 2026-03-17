---
name: segal-types
description: Segal types for synthetic ∞-categories. Binary composites exist uniquely
  up to homotopy. Foundation for topological chemputer.
metadata:
  trit: -1
  polarity: MINUS
  source: 'Riehl-Shulman 2017: A type theory for synthetic ∞-categories'
  technologies:
  - Rzk
  - Lean4
  - Agda
  - InfinityCosmos
---

# Segal Types Skill

> *"A Segal type is a type where binary composites exist uniquely up to homotopy."*
> — Emily Riehl & Michael Shulman

## Overview

Segal types are the synthetic ∞-categorical analogue of categories. They automatically ensure composition is **coherently associative and unital at all dimensions**.

## Core Definitions (Rzk)

```rzk
#lang rzk-1

-- The directed interval (axiomatized)
#define 2 : CUBE

-- Hom type (directed paths)
#define hom (A : U) (x y : A) : U
  := (t : 2) → A [t ≡ 0₂ ↦ x, t ≡ 1₂ ↦ y]

-- 2-simplex (composite witness)
#define Δ² : CUBE
  := (t₁ : 2) × (t₂ : 2) × (t₁ ≤ t₂)

-- Composition witness type
#define hom2 (A : U) (x y z : A) 
  (f : hom A x y) (g : hom A y z) (h : hom A x z) : U
  := (σ : Δ²) → A [
       σ = (0₂, t) ↦ f t,
       σ = (t, 1₂) ↦ g t,
       σ = (t, t) ↦ h t
     ]

-- Segal condition: unique composites
#define is-segal (A : U) : U
  := (x y z : A) → (f : hom A x y) → (g : hom A y z)
  → is-contr (Σ (h : hom A x z), hom2 A x y z f g h)

-- Segal type
#define Segal : U
  := Σ (A : U), is-segal A
```

## Chemputer Semantics

| ∞-Category Concept | Chemical Interpretation |
|--------------------|------------------------|
| Objects | Chemical species |
| 1-morphisms (hom) | Reactions A → B |
| 2-morphisms (hom2) | Witnesses that pathways yield same product |
| Segal condition | Unique composite reactions |
| Coherent associativity | Reaction order doesn't matter (up to iso) |

## GF(3) Triad

```
segal-types (-1) ⊗ directed-interval (0) ⊗ rezk-types (+1) = 0 ✓
```

As a **Validator (-1)**, segal-types verifies that:
- Composites exist and are unique
- Associativity holds at all dimensions
- The type has categorical structure

## Lean4 Integration (InfinityCosmos)

```lean
import InfinityCosmos.ForMathlib.AlgebraicTopology.SimplicialCategory

-- Segal space as simplicial space with Segal condition
structure SegalSpace where
  X : SimplicalSpace
  segal : ∀ n, IsEquiv (segalMap X n)

-- Composition in a Segal space
def compose {S : SegalSpace} {x y z : S.X 0} 
    (f : S.X 1 ⦃x, y⦄) (g : S.X 1 ⦃y, z⦄) : S.X 1 ⦃x, z⦄ :=
  (S.segal 2).inv ⟨f, g⟩
```

## Self-Avoiding Walk Integration

```ruby
# lib/segal_interaction.rb
module SegalInteraction
  # Each interaction is a morphism in a Segal type
  # Composition = sequential skill invocation
  
  def self.compose_interactions(f, g)
    # f : Interaction (skill A → skill B)
    # g : Interaction (skill B → skill C)
    # Result: unique composite f;g : (skill A → skill C)
    
    composite_seed = (f.seed ^ g.seed) & MASK64
    InteractionEntropy::Interaction.new(
      { composed: [f.id, g.id] }.to_json,
      seed: composite_seed
    )
  end
end
```

## Key Theorems

1. **Composition is coherent**: All ways of associating a sequence of morphisms yield the same result (up to higher homotopy).

2. **Identity exists**: For each object x, there is id_x : hom A x x.

3. **2-out-of-3**: If two of f, g, g∘f are equivalences, so is the third.

## References

- Riehl, E. & Shulman, M. (2017). "A type theory for synthetic ∞-categories." *Higher Structures* 1(1):116-193.
- [Rzk repository](https://github.com/rzk-lang/rzk)
- [InfinityCosmos](https://github.com/emilyriehl/infinity-cosmos)
