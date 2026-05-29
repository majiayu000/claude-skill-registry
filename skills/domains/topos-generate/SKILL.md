---
name: topos-generate
description: Topos Generation Skill (PLUS +1)
version: 1.0.0
---


# Topos Generation Skill (PLUS +1)

> Sheaf-theoretic model generation via forcing

**Trit**: +1 (PLUS)  
**Color**: #D82626 (Red)  
**Role**: Generator/Creator

## Core Concept

A topos E generates models via:
- **Subobject classifier** Ω (truth values)
- **Internal language** (Mitchell-Bénabou)
- **Forcing semantics** (Kripke-Joyal)

```
      E^op
        ↓ yoneda
    [E^op, Set]
        ↓ sheafification
     Sh(E, J)  ← topos!
```

## Subobject Classifier Ω

In Set: Ω = {0, 1} = Bool
In Sh(X): Ω = {open subsets of X}
In Sh(C,J): Ω = sieves

```
For any mono m: A ↣ B
∃! χ_m: B → Ω such that:

    A ───→ 1
    ↓      ↓ true
    B ──→ Ω
       χ_m
```

## Internal Language (Mitchell-Bénabou)

Every topos has an internal type theory:

```
Types      ↔ Objects
Terms      ↔ Morphisms  
Predicates ↔ Subobjects
∧, ∨, →    ↔ Ω operations
∀, ∃       ↔ Quantifiers via adjoints
```

### Internal Logic
```
⟦A ∧ B⟧ = ⟦A⟧ ×_Ω ⟦B⟧
⟦A → B⟧ = Ω^{⟦A⟧ → ⟦B⟧}
⟦∀x:X. φ(x)⟧ = ∏_{x:X} ⟦φ(x)⟧
```

## Kripke-Joyal Forcing

Stage-wise truth at object U:

```
U ⊩ φ ∧ ψ  ⟺  U ⊩ φ and U ⊩ ψ
U ⊩ φ → ψ  ⟺  ∀f:V→U. V ⊩ φ ⟹ V ⊩ ψ  
U ⊩ ∀x:X.φ ⟺  ∀f:V→U, ∀a:X(V). V ⊩ φ[a/x]
U ⊩ ∃x:X.φ ⟺  ∃ cover {Uᵢ→U}, ∃aᵢ:X(Uᵢ). Uᵢ ⊩ φ[aᵢ/x]
```

## Integration with Cider/Clojure

```clojure
(ns topos.generate
  (:require [acsets.core :as acs]))

;; Subobject classifier for finite topos
(defn omega [topos]
  (let [sieves (all-sieves (:site topos))]
    {:object sieves
     :true (maximal-sieve topos)
     :false (empty-sieve)}))

;; Force a proposition at stage
(defn force [stage prop env]
  (case (:type prop)
    :and (and (force stage (:left prop) env)
              (force stage (:right prop) env))
    :implies (every? (fn [morphism]
                       (let [stage' (compose stage morphism)]
                         (if (force stage' (:antecedent prop) env)
                           (force stage' (:consequent prop) env)
                           true)))
                     (covers stage))
    :forall (every? (fn [[morphism witness]]
                      (force (compose stage morphism) 
                             (:body prop) 
                             (assoc env (:var prop) witness)))
                    (all-witnesses stage (:type prop)))
    :exists (some (fn [[cover witnesses]]
                    (every? (fn [[morph wit]]
                              (force (compose stage morph)
                                     (:body prop)
                                     (assoc env (:var prop) wit)))
                            (zip cover witnesses)))
                  (all-covers-with-witnesses stage (:type prop)))))

;; Generate model satisfying formula
(defn generate-model [topos formula]
  (let [stages (objects topos)]
    (for [stage stages
          :when (force stage formula {})]
      {:stage stage
       :witnesses (collect-witnesses stage formula)})))
```

## Forcing for Set Theory

Cohen forcing generates new sets:

```
P = partial functions ω → 2 (finite approximations)
G = generic filter (added by forcing)

M[G] = { interpretation of names under G }
```

## GF(3) Triads

```
sheaf-cohomology (-1) ⊗ dialectica (0) ⊗ topos-generate (+1) = 0 ✓
temporal-coalgebra (-1) ⊗ open-games (0) ⊗ topos-generate (+1) = 0 ✓
three-match (-1) ⊗ kan-extensions (0) ⊗ topos-generate (+1) = 0 ✓
```

## Commands

```bash
# Generate subobject classifier
just topos-omega site

# Force proposition at stage
just topos-force stage "∀x. φ(x)"

# Generate satisfying model
just topos-model formula

# Internal language translation
just topos-internal formula
```

## Topos Models in Practice

| Topos | Generates | Application |
|-------|-----------|-------------|
| Set | Classical sets | Standard math |
| Sh(X) | Varying sets over X | Geometry |
| Sh(G) | G-sets | Symmetry |
| Eff | Computable functions | Computability |
| Dialectica | Proof-relevant math | Type theory |

## References

- Mac Lane & Moerdijk, "Sheaves in Geometry and Logic"
- Johnstone, "Sketches of an Elephant"
- Awodey, "Category Theory" §8
- nLab: https://ncatlab.org/nlab/show/forcing



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Bioinformatics
- **biopython** [○] via bicomodule
  - Hub for biological sequences

### Bibliography References

- `category-theory`: 139 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 9. Generic Procedures

**Concepts**: dispatch, multimethod, predicate dispatch, generic

### GF(3) Balanced Triad

```
topos-generate (+) + SDF.Ch9 (○) + [balancer] (−) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch5: Evaluation
- Ch2: Domain-Specific Languages
- Ch10: Adventure Game Example

### Connection Pattern

Generic procedures dispatch on predicates. This skill selects implementations dynamically.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 1 (PLUS)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #4ECDC4
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.