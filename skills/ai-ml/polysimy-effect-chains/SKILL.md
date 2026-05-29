---
name: polysimy-effect-chains
description: Verify multiple effect interpretations through propagator networks with temporal coalgebra bisimulation and common fixpoint solutions.
version: 1.0.0
---


# Polysimy Effect Chains Skill

> *"Multiple meanings flow through constraint networks to common solutions"*

**Status**: NOT IN plurigrid/asi (local only)
**Trit**: 0 (ERGODIC - coordinator)
**Color**: #26D826 (Green)
**Principle**: Effect polysimy → Propagation → Bisimulation → Common fixpoint

---

## Overview

**Polysimy** = multiple effect interpretations coexisting in a cell/channel.
**Effect chains** = sequences of transformations through propagator networks.
**Common solution** = fixpoint where all polysemic interpretations converge.

This skill bridges:
- `propagators` (+1) - bidirectional constraint flow
- `polysimy-effect-chains` (0) - effect coordination
- `temporal-coalgebra` (-1) - bisimulation verification

## Core Concepts

### 1. Polysemic Cells

Cells that hold **multiple effect interpretations** simultaneously:

```clojure
{:id :cell-a
 :effects [{:type :generate :transform inc}
           {:type :coordinate :transform #(* % 2)}
           {:type :validate :transform identity}]
 :value 20
 :trit 0}
```

### 2. Effect Chain Composition

Effects compose through the cell, creating a derivation stream:

```
init(10) → generate(inc) → coordinate(*2) → validate(id) → 22
```

### 3. Common Solution via Bisimulation

Two effect chains have a **common solution** iff they are **bisimilar**:

```
bisimilar?(chain-a, chain-b) ⟺
  observe(chain-a).head == observe(chain-b).head ∧
  effects-count(chain-a) ≡ effects-count(chain-b) (mod 3)
```

## API

```clojure
(require '[polysimy-effect-chains :as pec])

;; Create polysemic cell
(def cell (pec/make-cell :my-cell {:trit 0}))

;; Chain effects
(def chain-a
  (-> cell
      (pec/chain {:type :generate :init 10 :f inc})
      (pec/chain {:type :coordinate :f #(* % 2)})
      (pec/chain {:type :validate :f identity})))

;; Verify common solution
(pec/find-common-solution chain-a chain-b)
;; => {:bisimilar true
;;     :common-value 22
;;     :gf3-conserved true}
```

## GF(3) Integration

Forms valid triads:

```
propagators (+1) ⊗ polysimy-effect-chains (0) ⊗ temporal-coalgebra (-1) = 0 ✓
gay-mcp (+1) ⊗ polysimy-effect-chains (0) ⊗ sheaf-cohomology (-1) = 0 ✓
```

## Temporary Verification Pattern

For **temporary** (intermediate) verification before full fixpoint:

```clojure
(defn verify-temporary [cells depth]
  (loop [d 0]
    (when (< d depth)
      (let [obs (map observe cells)]
        (if (all-bisimilar? obs)
          {:status :bisimilar-at-depth :depth d}
          (recur (inc d)))))))
```

## Commands

```bash
# Verify effect chain bisimulation
just polysimy-verify chain-a chain-b

# Find common solution
just polysimy-common [cells...]

# Temporary verification to depth N
just polysimy-temp-verify 10
```

## Relationship to Uncommitted Skills

This skill relates to other **local-only skills not in plurigrid/asi**:

| Skill | Relation |
|-------|----------|
| `discrete-backprop` | Backward effect propagation |
| `dynamic-sufficiency-goblin` | Effect sufficiency checking |
| `skill-bonds` | Effect chain bonding |
| `ultrametric-distance` | Effect distance measurement |

## Mathematical Foundation

### Effect Polysimy

$$\text{Poly}(C) = \sum_{e \in \text{Effects}} e \circ C$$

Multiple effects acting on the same cell carrier.

### Bisimulation Quotient

$$X / {\sim} \cong \text{codom}(\text{anamorphism to } \nu F)$$

Cells are equivalent iff they unfold to the same infinite stream.

### Common Solution Existence

$$\exists \text{common} \iff H^0(\mathcal{U}, \mathcal{F}) \neq \emptyset$$

A common solution exists iff the zeroth cohomology is non-empty.

---

**Skill Name**: polysimy-effect-chains
**Type**: Effect Coordination
**Trit**: 0 (ERGODIC)
**NOT IN**: plurigrid/asi (should be committed)
**GF(3)**: Coordinates between generators and validators