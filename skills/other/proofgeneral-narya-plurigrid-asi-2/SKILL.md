---
name: proofgeneral-narya
description: "Proof General + Narya: Higher-dimensional type theory proof assistant with observational bridge types for version control."
source: ProofGeneral/PG + mikeshulman/narya + music-topos
license: GPL-3.0
xenomodern: true
stars: 768  # PG: 543 + Narya: 225
---

# ProofGeneral + Narya Skill

> *"Observational type theory: where equality is what you can observe, not what you can prove."*

## Overview

This skill combines:
- **Proof General** (543⭐): The universal Emacs interface for proof assistants
- **Narya** (225⭐): Higher-dimensional type theory proof assistant

## Proof General Basics

```elisp
;; Install via straight.el or package.el
(use-package proof-general
  :mode ("\\.v\\'" . coq-mode)
  :config
  (setq proof-splash-enable nil
        proof-three-window-mode-policy 'hybrid))
```

### Key Bindings

| Key | Action | Description |
|-----|--------|-------------|
| `C-c C-n` | `proof-assert-next-command-interactive` | Step forward |
| `C-c C-u` | `proof-undo-last-successful-command` | Step backward |
| `C-c C-RET` | `proof-goto-point` | Process to cursor |
| `C-c C-b` | `proof-process-buffer` | Process entire buffer |
| `C-c C-.` | `proof-goto-end-of-locked` | Jump to locked region end |

### Proof State Visualization

```
┌─────────────────────────────────────────────────────────────┐
│  ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  ▲ Locked (proven)   ▲ Processing      ▲ Unprocessed       │
│                                                             │
│  GF(3) Trit Mapping:                                        │
│    Locked    → +1 (LIVE)     → Red    #FF0000              │
│    Processing → 0  (VERIFY)  → Green  #00FF00              │
│    Unprocessed → -1 (BACKFILL) → Blue #0000FF              │
└─────────────────────────────────────────────────────────────┘
```

## Narya: Higher-Dimensional Type Theory

Narya is a proof assistant for higher observational type theory (HOTT).

### Key Features

1. **Observational Equality**: Bridge types computed inductively from type structure
2. **Higher Dimensions**: Support for 2-cells, 3-cells, etc.
3. **No Interval Type**: Unlike cubical type theory, no explicit interval

### Narya Syntax

```narya
-- Define a type
def Nat : Type := data [
  | zero : Nat
  | suc : Nat → Nat
]

-- Bridge type between values
def bridge (A : Type) (x y : A) : Type := x ≡ y

-- Transport along bridge
def transport (A : Type) (P : A → Type) (x y : A) (p : x ≡ y) : P x → P y
  := λ px. subst P p px
```

## Observational Bridge Types (gay.el integration)

From `narya_observational_bridge.el`:

```elisp
(cl-defstruct (obs-bridge (:constructor obs-bridge-create))
  "An observational bridge type connecting two versions."
  source      ; Source object
  target      ; Target object  
  bridge      ; The diff/relation between them
  dimension   ; 0 = value, 1 = diff, 2 = conflict resolution
  tap-state   ; TAP state: -1 BACKFILL, 0 VERIFY, +1 LIVE
  color       ; Gay.jl color
  fingerprint) ; Content hash

;; Create diff as bridge type
(defun obs-bridge-diff (source target seed)
  "Create an observational bridge (diff) from SOURCE to TARGET."
  (let* ((source-hash (sxhash source))
         (target-hash (sxhash target))
         (bridge-hash (logxor source-hash target-hash))
         (index (mod bridge-hash 1000))
         (color (gay/color-at seed index)))
    (obs-bridge-create
     :source source
     :target target
     :bridge (list :from source-hash :to target-hash)
     :dimension 1
     :color color)))
```

## Hierarchical Agent Structure: 3×3×3 = 27

```
Level 0: Root (VERIFY)
    │
    ├── Level 1: BACKFILL (-1) ─── L2: [-1, 0, +1] ─── L3: 3×3 = 9 agents
    ├── Level 1: VERIFY (0)    ─── L2: [-1, 0, +1] ─── L3: 3×3 = 9 agents  
    └── Level 1: LIVE (+1)     ─── L2: [-1, 0, +1] ─── L3: 3×3 = 9 agents

Total: 1 + 3 + 9 + 27 = 40 agents (or 27 leaves)
```

### Bruhat-Tits Tree Navigation

```elisp
;; Navigate the Z_3 gamut poset
(defun bt-node-child (node branch)
  "Return child of NODE at BRANCH (0, 1, or 2)."
  (bt-node (append (bt-node-path node) (list branch))))

(defun bt-node-distance (node1 node2)
  "Return tree distance between NODE1 and NODE2."
  (let* ((lca (bt-node-lca-depth node1 node2))
         (d1 (bt-node-depth node1))
         (d2 (bt-node-depth node2)))
    (+ (- d1 lca) (- d2 lca))))
```

## Möbius Inversion for Trajectory Analysis

```elisp
;; Map TAP trajectory to multiplicative structure
;; -1 → 2, 0 → 3, +1 → 5 (first three primes)
(defun moebius/trajectory-to-multiplicative (trajectory)
  (let ((result 1))
    (dolist (t trajectory)
      (setq result (* result
                      (pcase t
                        (-1 2)
                        (0 3)
                        (+1 5)))))
    result))

;; μ(n) ≠ 0 ⟹ square-free trajectory (no redundancy)
```

## Bumpus Laxity Measures

For coherence between proof states:

```elisp
(defun bumpus/compute-laxity (agent1 agent2)
  "Laxity = 0 means strict functor (perfect coherence).
   Laxity = 1 means maximally lax."
  (let* ((d (bt-node-distance (narya-agent-bt-node agent1)
                               (narya-agent-bt-node agent2)))
         (mu1 (narya-agent-moebius-mu agent1))
         (mu2 (narya-agent-moebius-mu agent2))
         (mu-diff (abs (- mu1 mu2))))
    (min 1.0 (/ (+ d (* 0.5 mu-diff)) 10.0))))
```

## Version Control Operations

| Operation | Description | Dimension |
|-----------|-------------|-----------|
| `fork` | Create 3 branches (balanced ternary) | 0 → 1 |
| `continue` | Choose branch (-1, 0, +1) | 1 → 1 |
| `merge` | Resolve conflict (2D cubical) | 1 → 2 |

## Xenomodern Stance

The ironic detachment here is recognizing that:

1. **Proof assistants are version control systems** for mathematical truth
2. **Type theory is a programming language** for proofs
3. **Observational equality** is more practical than definitional equality
4. **Higher dimensions** emerge naturally from conflict resolution

## Commands

```bash
just narya-demo           # Run Narya bridge demonstration
just proofgeneral-setup   # Configure Proof General
just spawn-hierarchy      # Create 27-agent hierarchy
just measure-laxity       # Compute Bumpus laxity metrics
```

## References

- [Proof General Manual](https://proofgeneral.github.io/)
- [Narya GitHub](https://github.com/mikeshulman/narya)
- [Higher Observational Type Theory](https://ncatlab.org/nlab/show/higher+observational+type+theory)
- [Topos Institute: Structure-Aware Version Control](https://topos.institute/blog/2024-11-13-structure-aware-version-control-via-observational-bridge-types/)
