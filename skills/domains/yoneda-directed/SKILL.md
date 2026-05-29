---
name: yoneda-directed
description: Directed Yoneda lemma as directed path induction. Riehl-Shulman's key
version: 1.0.0
---


# Directed Yoneda Skill

> *"The dependent Yoneda lemma is a directed analogue of path induction."*
> — Emily Riehl & Michael Shulman

## The Key Insight

| Standard HoTT | Directed HoTT |
|---------------|---------------|
| Path induction | Directed path induction |
| Yoneda for ∞-groupoids | Dependent Yoneda for ∞-categories |
| Types have identity | Segal types have composition |

## Core Definition (Rzk)

```rzk
#lang rzk-1

-- Dependent Yoneda lemma
-- To prove P(x, f) for all x : A and f : hom A a x,
-- it suffices to prove P(a, id_a)

#define dep-yoneda
  (A : Segal-type) (a : A)
  (P : (x : A) → hom A a x → U)
  (base : P a (id a))
  : (x : A) → (f : hom A a x) → P x f
  := λ x f. transport-along-hom P f base

-- This is "directed path induction"
#define directed-path-induction := dep-yoneda
```

## Chemputer Semantics

**Chemical Interpretation**:
- To prove a property of all reaction products from starting material A,
- It suffices to prove it for A itself (the identity "null reaction")
- Directed induction propagates the property along all reaction pathways

## GF(3) Triad

```
yoneda-directed (-1) ⊗ elements-infinity-cats (0) ⊗ synthetic-adjunctions (+1) = 0 ✓
yoneda-directed (-1) ⊗ cognitive-superposition (0) ⊗ curiosity-driven (+1) = 0 ✓
```

As **Validator (-1)**, yoneda-directed verifies:
- Properties propagate correctly along morphisms
- Base case at identity suffices
- Induction principle is sound

## Theorem

```
For any Segal type A, element a : A, and type family P,
if we have base : P(a, id_a), then for all x : A and f : hom(a, x),
we get P(x, f).

This is analogous to:
"To prove ∀ paths from a, prove for the reflexivity path"
```

## References

1. Riehl, E. & Shulman, M. (2017). "A type theory for synthetic ∞-categories." §5.
2. [Rzk sHoTT library](https://rzk-lang.github.io/sHoTT/)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `category-theory`: 139 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 5. Evaluation

**Concepts**: eval, apply, interpreter, environment

### GF(3) Balanced Triad

```
yoneda-directed (+) + SDF.Ch5 (−) + [balancer] (○) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch7: Propagators

### Connection Pattern

Evaluation interprets expressions. This skill processes or generates evaluable forms.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Presheaves
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