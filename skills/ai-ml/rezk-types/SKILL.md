---
name: rezk-types
description: "Rezk types (complete Segal spaces). Local univalence: categorical isomorphisms ≃ type-theoretic identities."
version: 1.0.0
---


# Rezk Types Skill

> *"In a Rezk type, isomorphisms are equivalent to identities — local univalence."*
> — Emily Riehl & Michael Shulman

## Overview

Rezk types are Segal types with an additional **local univalence** condition: categorical isomorphisms are equivalent to type-theoretic identities. This is the ∞-categorical analogue of the univalence axiom.

## Core Definitions (Rzk)

```rzk
#lang rzk-1

-- Isomorphism in a Segal type
#define is-iso (A : Segal) (x y : A) (f : hom A x y) : U
  := Σ (g : hom A y x), 
     (hom2 A x y x f g (id x)) × (hom2 A y x y g f (id y))

-- The type of isomorphisms
#define Iso (A : Segal) (x y : A) : U
  := Σ (f : hom A x y), is-iso A x y f

-- Identity-to-isomorphism map
#define id-to-iso (A : Segal) (x y : A) : (x = y) → Iso A x y
  := λ p. transport (λ z. Iso A x z) p (id x, refl-iso)

-- Rezk condition (local univalence)
#define is-rezk (A : Segal) : U
  := (x y : A) → is-equiv (id-to-iso A x y)

-- Rezk type (complete Segal space)
#define Rezk : U
  := Σ (A : Segal), is-rezk A
```

## Chemputer Semantics

| ∞-Category Concept | Chemical Interpretation |
|--------------------|------------------------|
| Isomorphism | Reversible reaction (equilibrium) |
| Local univalence | "Isomers at equilibrium are the same species" |
| Rezk completion | Finding thermodynamic fixed points |
| Identity = Iso | Chemical identity = equilibrium class |

## GF(3) Triad

```
segal-types (-1) ⊗ directed-interval (0) ⊗ rezk-types (+1) = 0 ✓
```

As a **Generator (+1)**, rezk-types creates:
- Complete categorical structure
- Univalent foundations for chemistry
- Equilibrium-respecting species identification

## The Local Univalence Principle

In a Rezk type:
```
(A ≅ B) ≃ (A = B)
```

**Chemical interpretation**: Two species at mutual equilibrium can be identified. The equilibrium constant K = 1 means "same species up to naming."

## Lean4 Integration

```lean
import InfinityCosmos.ForMathlib.AlgebraicTopology.Quasicategory

-- Rezk completion functor
def RezkCompletion : SegalSpace → RezkSpace := sorry

-- Local univalence
theorem local_univalence (R : RezkSpace) (x y : R.X 0) :
    (x = y) ≃ Iso R x y := by
  exact R.rezk x y
```

## Integration with Interaction Entropy

```ruby
# Rezk completion for interaction sequences
module RezkCompletion
  # Two interaction sequences are "Rezk-equivalent" if
  # they produce the same observable effect
  
  def self.equivalent?(seq1, seq2)
    # Check if there's an isomorphism between outcomes
    # Isomorphism = both directions have GF(3) = 0
    forward_trit_sum = seq1.zip(seq2).map { |a, b| a.trit - b.trit }.sum
    backward_trit_sum = seq2.zip(seq1).map { |a, b| a.trit - b.trit }.sum
    
    (forward_trit_sum % 3 == 0) && (backward_trit_sum % 3 == 0)
  end
end
```

## Key Theorems

1. **Rezk completion exists**: Every Segal type has a universal Rezk completion.

2. **Functors preserve Rezk**: A functor F : A → B between Rezk types preserves isomorphisms.

3. **Adjoint is property**: For a functor between Rezk types, having an adjoint is a **mere proposition** (at most one adjoint up to iso).

## References

- Rezk, C. (2001). "A model for the homotopy theory of homotopy theory." *Trans. AMS*.
- Riehl, E. & Shulman, M. (2017). "A type theory for synthetic ∞-categories."
- [sHoTT library](https://rzk-lang.github.io/sHoTT/)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `homotopy-theory`: 29 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
rezk-types (○) + SDF.Ch3 (○) + [balancer] (○) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch5: Evaluation

### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.
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