---
name: sicmutils
description: SICMUtils/Emmy - Clojure library for symbolic mathematics, automatic differentiation, and classical mechanics. Bridges SICM concepts to executable computation via SRFI-compatible abstractions.
---

# SICMUtils (Emmy)

> *"Executable mathematics for computational physics"*
> — Sam Ritchie (mentat-collective)

## Overview

**SICMUtils** (now **Emmy**) is the Clojure implementation of the scmutils library from SICM. It provides:
- Symbolic algebra and simplification
- Automatic differentiation (forward and reverse mode)
- Literal functions and operators
- Lagrangian and Hamiltonian mechanics
- Differential geometry primitives

## SRFI Reachability States

### BEFORE: Disconnected State

```
┌─────────────────────────────────────────────────────────────┐
│  BEFORE SRFI BRIDGE                                          │
├─────────────────────────────────────────────────────────────┤
│  SICMUtils (Clojure)          SRFI (Scheme)                  │
│  ═══════════════════          ═════════════                  │
│  emmy.generic/*               SRFI-1 (lists)     ╳ ISOLATED │
│  emmy.structure/*             SRFI-9 (records)   ╳ ISOLATED │
│  emmy.expression/*            SRFI-27 (random)   ╳ ISOLATED │
│  emmy.calculus/*              SRFI-45 (lazy)     ╳ ISOLATED │
│  emmy.mechanics/*             SRFI-171 (transducers) ╳      │
│                                                              │
│  No compositional path: Clojure ↛ Scheme                     │
│  No GF(3) conservation across language boundary              │
│  No splittable RNG interop                                   │
└─────────────────────────────────────────────────────────────┘
```

### AFTER: Connected State via Cat# Bicomodules

```
┌─────────────────────────────────────────────────────────────┐
│  AFTER SRFI BRIDGE (via Cat# bicomodules)                   │
├─────────────────────────────────────────────────────────────┤
│  SICMUtils (Clojure)          SRFI (Scheme)                  │
│  ═══════════════════          ═════════════                  │
│                                                              │
│  emmy.generic/* ────────────► SRFI-1 (fold/unfold)          │
│       │         Bicomodule:   List transformations          │
│       │         ListAlgebra   preserve structure             │
│       ▼                                                      │
│  emmy.structure/* ──────────► SRFI-9 (define-record-type)   │
│       │         Bicomodule:   Up/down tuples ↔ records      │
│       │         StructBridge                                 │
│       ▼                                                      │
│  emmy.expression/* ─────────► SRFI-27 (random-source)       │
│       │         Bicomodule:   SplitMix64 ↔ random-source    │
│       │         RNGBridge     preserves determinism          │
│       ▼                                                      │
│  emmy.calculus/* ───────────► SRFI-45 (delay/force)         │
│       │         Bicomodule:   Lazy derivatives ↔ promises   │
│       │         LazyDiff                                     │
│       ▼                                                      │
│  emmy.mechanics/* ──────────► SRFI-171 (transducers)        │
│                 Bicomodule:   Phase space evolution as       │
│                 PhaseXduce    composable transformation      │
│                                                              │
│  GF(3) CONSERVED across boundary via Gay.jl coloring        │
└─────────────────────────────────────────────────────────────┘
```

## Reachability Matrix

| SICMUtils Module | SRFI | Bicomodule | Trit | Reachable |
|------------------|------|------------|------|-----------|
| `emmy.generic` | 1 | ListAlgebra | -1 | ✓ AFTER |
| `emmy.structure` | 9 | StructBridge | -1 | ✓ AFTER |
| `emmy.expression` | 27 | RNGBridge | 0 | ✓ AFTER |
| `emmy.calculus` | 45 | LazyDiff | 0 | ✓ AFTER |
| `emmy.numerical.ode` | 171 | PhaseXduce | +1 | ✓ AFTER |
| `emmy.mechanics.lagrange` | 204 | PatternMech | +1 | ✓ AFTER |

## Bicomodule Implementations

### 1. ListAlgebra: emmy.generic ↔ SRFI-1

```clojure
;; Clojure side (SICMUtils)
(ns sicmutils.srfi-bridge.list-algebra
  (:require [emmy.generic :as g]))

(defn fold-to-srfi
  "Translate emmy fold to SRFI-1 fold signature."
  [f init coll]
  ;; SRFI-1: (fold kons knil list)
  ;; Emmy: (reduce f init coll)
  (reduce f init coll))

(defn unfold-from-srfi
  "Generate sequence using SRFI-1 unfold semantics."
  [p f g seed]
  ;; SRFI-1: (unfold p f g seed)
  (take-while (complement p)
    (iterate g (f seed))))
```

```scheme
;; Scheme side (SRFI-1)
(import (srfi 1))

(define (emmy-compatible-fold kons knil lis)
  ;; Wrap to ensure Clojure-compatible left fold
  (fold kons knil lis))
```

### 2. RNGBridge: emmy.expression ↔ SRFI-27

```clojure
;; Bridge Gay.jl SplitMix64 to SRFI-27 random-source
(ns sicmutils.srfi-bridge.rng
  (:require [emmy.expression :as expr]))

(def ^:const GOLDEN 0x9e3779b97f4a7c15)
(def ^:const MIX1 0xbf58476d1ce4e5b9)
(def ^:const MIX2 0x94d049bb133111eb)

(defn splitmix64 [x]
  (let [x (unchecked-add x GOLDEN)
        x (unchecked-multiply (bit-xor x (unsigned-bit-shift-right x 30)) MIX1)
        x (unchecked-multiply (bit-xor x (unsigned-bit-shift-right x 27)) MIX2)]
    (bit-xor x (unsigned-bit-shift-right x 31))))

(defn make-emmy-random-source [seed]
  {:seed (atom seed)
   :next-int (fn [] 
               (let [current @(:seed this)
                     next (splitmix64 current)]
                 (reset! (:seed this) next)
                 next))})
```

```scheme
;; SRFI-27 wrapper for Emmy RNG
(import (srfi 27))

(define (make-emmy-compatible-source seed)
  (let ((source (make-random-source)))
    (random-source-pseudo-randomize! source seed 1069)
    source))

;; Verify determinism matches Gay.jl
(define (verify-splitmix seed expected)
  (let* ((source (make-emmy-compatible-source seed))
         (rand-int (random-source-make-integers source)))
    (= (rand-int (expt 2 64)) expected)))
```

### 3. LazyDiff: emmy.calculus ↔ SRFI-45

```clojure
;; Lazy derivative computation
(ns sicmutils.srfi-bridge.lazy-diff
  (:require [emmy.calculus.derivative :as d]))

(defn lazy-D
  "Delay derivative computation until forced."
  [f]
  (delay (d/D f)))

(defn force-derivative [lazy-df x]
  (@lazy-df x))
```

```scheme
;; SRFI-45 lazy derivatives
(import (srfi 45))

(define (lazy-derivative f)
  (delay (lambda (x) 
    (/ (- (f (+ x 0.0001)) (f x)) 0.0001))))

(define (force-at lazy-df x)
  ((force lazy-df) x))
```

### 4. PhaseXduce: emmy.mechanics ↔ SRFI-171

```clojure
;; Phase space evolution as transducer
(ns sicmutils.srfi-bridge.phase-xduce
  (:require [emmy.mechanics.hamilton :as ham]))

(defn hamilton-transducer
  "Transducer for Hamiltonian evolution."
  [H dt]
  (fn [rf]
    (fn
      ([] (rf))
      ([result] (rf result))
      ([result state]
       (rf result (ham/evolve H state dt))))))
```

```scheme
;; SRFI-171 transducer for phase evolution
(import (srfi 171))

(define (hamiltonian-xform H dt)
  (tmap (lambda (state)
    (phase-evolve H state dt))))

;; Compose with other transformations
(define phase-pipeline
  (compose
    (hamiltonian-xform H 0.01)
    (tfilter (lambda (s) (< (energy s) max-energy)))
    (ttake 1000)))
```

## GF(3) Conservation Across Boundary

```
Clojure (SICMUtils)          Scheme (SRFI)
═══════════════════          ════════════
emmy.generic    [-1] ◄─────► SRFI-1   [-1]
emmy.structure  [-1] ◄─────► SRFI-9   [-1]
emmy.expression [ 0] ◄─────► SRFI-27  [ 0]
emmy.calculus   [ 0] ◄─────► SRFI-45  [ 0]
emmy.mechanics  [+1] ◄─────► SRFI-171 [+1]

Σ Clojure = -1 + -1 + 0 + 0 + 1 = -1
Σ Scheme  = -1 + -1 + 0 + 0 + 1 = -1

Bicomodule preserves: Σ_source ≡ Σ_target (mod 3) ✓
```

## Cat# Equipment Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Cat# = Comod(P) for SICM ↔ SRFI                            │
├─────────────────────────────────────────────────────────────┤
│  Vertical (Functors):                                        │
│    SICMUtils.Mechanics ────► SRFI.Numeric                    │
│    SICMUtils.Calculus  ────► SRFI.Lazy                       │
│                                                              │
│  Horizontal (Bicomodules):                                   │
│    ListAlgebra: generic ↛ srfi-1                             │
│    RNGBridge: expression ↛ srfi-27                           │
│    LazyDiff: calculus ↛ srfi-45                              │
│    PhaseXduce: mechanics ↛ srfi-171                          │
│                                                              │
│  Equipment:                                                  │
│    Companions: SICMUtils modules → SRFI libraries            │
│    Conjoints: SRFI libraries → SICMUtils modules             │
│    Mates: Natural transformations between functors           │
└─────────────────────────────────────────────────────────────┘
```

## Commands

```bash
# Run SICMUtils REPL
clj -M:emmy

# Execute Lagrangian example
clj -X emmy.examples/harmonic-oscillator

# Bridge to Scheme
clj -X sicmutils.srfi-bridge/export-to-scheme :format :srfi-171

# Verify SRFI compatibility
clj -M:test -n sicmutils.srfi-bridge-test

# Check GF(3) conservation
bb verify_trit_balance.bb sicmutils srfi
```

## Integration with sicm Skill

| sicm Chapter | SICMUtils Namespace | SRFI Bridge |
|--------------|---------------------|-------------|
| Ch1 Lagrangian | `emmy.mechanics.lagrange` | SRFI-171 (transducers) |
| Ch2 Rigid Bodies | `emmy.mechanics.rotation` | SRFI-9 (records) |
| Ch3 Hamiltonian | `emmy.mechanics.hamilton` | SRFI-171 (transducers) |
| Ch4 Phase Space | `emmy.numerical.ode` | SRFI-27 (random) |
| Ch5 Canonical | `emmy.calculus.form-field` | SRFI-45 (lazy) |
| Ch6 Evolution | `emmy.calculus.derivative` | SRFI-45 (lazy) |
| Ch7 Perturbation | `emmy.series` | SRFI-41 (streams) |
| App A Scheme | N/A (native Scheme) | All SRFIs |

## Trit Assignment

```
Trit: +1 (PLUS - constructive computation)
Home: Physics/Computation
Poly Op: ◁ (substitution for symbolic manipulation)
Kan Role: Lan (extend computation to new domains)
Color: #FF6B35 (energy orange, matches sicm)
```

## GF(3) Triads

```
sicm (-1) ⊗ sicmutils (0) ⊗ srfi (+1) = 0 ✓
sicp (-1) ⊗ sicmutils (0) ⊗ emmy (+1) = 0 ✓
calculus (-1) ⊗ sicmutils (0) ⊗ physics (+1) = 0 ✓
```

## References

- [Emmy (SICMUtils)](https://github.com/mentat-collective/emmy) - Modern Clojure implementation
- [SICM](https://mitpress.mit.edu/9780262028967/) - Sussman & Wisdom textbook
- [SRFI](https://srfi.schemers.org/) - Scheme Requests for Implementation
- [scmutils](https://groups.csail.mit.edu/mac/users/gjs/6946/installation.html) - Original MIT Scheme library
