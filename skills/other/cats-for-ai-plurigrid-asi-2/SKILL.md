# cats.for" (Categories for AI)

> "Category theory is compositionality made formal"
> — Bruno Gavranović, cats.for.ai

**URL**: https://cats.for.ai
**Trit**: 0 (ERGODIC)
**Color**: #26D826 (Green)
**Status**: ✅ Production Ready

## Overview

**cats.for.ai** is the definitive lecture series connecting category theory to machine learning, organized by DeepMind, Qualcomm AI, and academic researchers.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         cats.for.ai INTEGRATION                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   POLY INACCESSIBLE WORLDS AS COLORS MAXIMAL                               │
│                                                                             │
│   ┌───────────────┐     ┌───────────────┐     ┌───────────────┐            │
│   │   Poly(y)     │     │  Inaccessible │     │    Colors     │            │
│   │   Functors    │────▶│    Worlds     │────▶│    Maximal    │            │
│   │    (-1)       │     │     (0)       │     │     (+1)      │            │
│   └───────────────┘     └───────────────┘     └───────────────┘            │
│         │                      │                      │                     │
│         │    Optics/Lenses     │   Modal Semantics    │   GF(3) Coloring   │
│         │                      │                      │                     │
│         └──────────────────────┴──────────────────────┘                     │
│                                 │                                           │
│                    GF(3): (-1) + 0 + (+1) ≡ 0                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Organizing Committee

| Name | Affiliation | Role |
|------|-------------|------|
| Bruno Gavranović | Strathclyde / CyberCat | Optics, Lenses, Backprop |
| Petar Veličković | DeepMind / Cambridge | GNNs, Categories |
| Pim de Haan | Amsterdam / Qualcomm | Geometric DL, Equivariance |
| Andrew Dudzik | DeepMind | Monads, RNNs |
| João G. Araújo | Cohere / USP | LLMs, Semantics |

## Guest Speakers

| Speaker | Topic | Trit |
|---------|-------|------|
| David Spivak | Poly, Dynamic Systems | 0 (ERGODIC) |
| Jules Hedges | Categorical Cybernetics | 0 (ERGODIC) |
| Tai-Danae Bradley | CT for LLMs | +1 (PLUS) |
| Taco Cohen | Causal Abstraction | -1 (MINUS) |
| Pietro Vertechi | Parametric Spans | 0 (ERGODIC) |
| Thomas Gebhart | Sheaves for AI | -1 (MINUS) |

## Lecture Program

### Part 1: Introductory Lectures (Completed)

| Week | Topic | Speaker | Key Concepts |
|------|-------|---------|--------------|
| 1 | Why Category Theory? | Gavranović | Compositionality, Modularity |
| 2 | Categories & Functors | Veličković | Objects, Morphisms, Functors |
| 3 | Optics & Lenses | Gavranović | Bidirectional flow, Backprop |
| 4 | Geometric DL & Naturality | de Haan | Equivariance, Natural transformations |
| 5 | Monoids, Monads, LSTMs | Dudzik | Recurrence, State |

### Part 2: Research Seminars (Ongoing)

| Date | Topic | Speaker |
|------|-------|---------|
| Nov 14 | Neural network layers as parametric spans | Vertechi |
| Nov 21 | Causal Model Abstraction | Cohen |
| Dec 12 | Category Theory Inspired by LLMs | Bradley |
| Mar 20 | Categorical Cybernetics | Hedges |
| Mar 27 | Dynamic organizational systems | Spivak |
| May 29 | Sheaves for AI | Gebhart |

## Core Concepts

### 1. Polynomial Functors (Py)

```haskell
-- Poly = polynomial functors on Set
-- y = representable functor Hom(1, -)
-- ◁ = composition of polynomials

data Poly where
  Poly :: { positions :: Type
          , directions :: positions -> Type
          } -> Poly

-- Key operations
(⊗) :: Poly -> Poly -> Poly  -- parallel (tensor)
(◁) :: Poly -> Poly -> Poly  -- sequential (composition)
(+) :: Poly -> Poly -> Poly  -- coproduct
```

### 2. Inaccessible Worlds (Modal Semantics)

```agda
-- Kripke frame with inaccessibility
record KripkeFrame : Set₁ where
  field
    World : Set
    _≺_ : World → World → Set  -- accessibility
    inaccessible : World → Set  -- worlds with no predecessors

-- Modal operators
□ : (World → Prop) → (World → Prop)  -- necessity
□ φ w = ∀ v → w ≺ v → φ v

◇ : (World → Prop) → (World → Prop)  -- possibility
◇ φ w = ∃ v → w ≺ v × φ v

-- Inaccessible world: ¬∃v. v ≺ w
isInaccessible : World → Prop
isInaccessible w = ∀ v → ¬(v ≺ w)
```

### 3. Colors Maximal (GF(3) Saturation)

```clojure
(ns cats4ai.colors
  (:require [gay.core :as gay]))

(defn color-world [world-seed trit]
  "Assign maximal color to world based on trit"
  (let [hue (case trit
              :MINUS   (+ 180 (mod (* world-seed 37) 120))  ; cold
              :ERGODIC (+ 60 (mod (* world-seed 41) 120))   ; neutral
              :PLUS    (mod (* world-seed 43) 60))          ; warm
        saturation 1.0  ; MAXIMAL
        lightness 0.5]
    {:hue hue :sat saturation :lit lightness
     :hex (gay/hsl->hex hue saturation lightness)}))

(defn worlds-palette [n]
  "Generate n inaccessible worlds with maximal colors"
  (for [i (range n)
        :let [trit (case (mod i 3) 0 :ERGODIC 1 :PLUS 2 :MINUS)]]
    {:world-id i
     :accessible? false  ; inaccessible
     :color (color-world i trit)
     :trit trit}))
```

## Optics for Machine Learning

### Lens = Backpropagation

```haskell
-- A lens captures forward/backward pass
data Lens s t a b = Lens
  { view :: s -> a        -- forward pass
  , update :: s -> b -> t  -- backward pass (gradient)
  }

-- Backprop is lens composition
backprop :: Lens s t a b -> Lens a b c d -> Lens s t c d
backprop l1 l2 = Lens
  { view = view l2 . view l1
  , update = \s d ->
      let a = view l1 s
          b = update l2 a d
      in update l1 s b
  }

-- Chain rule emerges from lens composition!
-- d(g∘f)/dx = dg/df · df/dx
```

### Para = Parametric Morphisms

```haskell
-- Parametric morphism (neural network layer)
data Para p a b = Para
  { params :: p           -- learnable parameters
  , forward :: p -> a -> b  -- parameterized forward
  }

-- Para composition
(>>>) :: Para p a b -> Para q b c -> Para (p, q) a c
(Para p f) >>> (Para q g) = Para (p, q) (\(p,q) a -> g q (f p a))
```

### Optic = Generalized Bidirectional

```haskell
-- Optic generalizes lens, prism, traversal
type Optic p s t a b = p a b -> p s t

-- Specific optics for ML:
type Lens s t a b = Optic (Star ((->) s)) s t a b      -- deterministic
type Prism s t a b = Optic (Costar (Either a)) s t a b -- optional
type Affine s t a b = Optic (Star Maybe) s t a b       -- at most one
```

## Integration Map

### With Existing Skills

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      cats.for.ai SKILL INTEGRATION                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  cats.for.ai                                                                │
│       │                                                                     │
│       ├──▶ open-games (Hedges)                                             │
│       │         └── Play/Coplay bidirectional                               │
│       │                                                                     │
│       ├──▶ catsharp (Spivak)                                               │
│       │         └── Cat# = Comod(P) equipment                              │
│       │                                                                     │
│       ├──▶ topos-catcolab (Patterson)                                      │
│       │         └── Double theories, ACSets                                 │
│       │                                                                     │
│       ├──▶ cybernetic-open-game                                            │
│       │         └── Agent-O-Rama ↔ Worldnet ↔ STC                          │
│       │                                                                     │
│       ├──▶ elements-infinity-cats (Riehl-Verity)                           │
│       │         └── ∞-cosmos model independence                             │
│       │                                                                     │
│       ├──▶ sheaf-laplacian-coordination (Gebhart)                          │
│       │         └── Sheaf neural networks                                   │
│       │                                                                     │
│       ├──▶ crdt (Automerge)                                                │
│       │         └── Join-semilattice merge                                  │
│       │                                                                     │
│       └──▶ derangement-crdt                                                │
│                 └── Colorable permutations                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### GF(3) Triads

```
# Core cats.for.ai triads
optics-lenses (-1) ⊗ cats-for-ai (0) ⊗ backprop (+1) = 0 ✓
sheaves (-1) ⊗ cats-for-ai (0) ⊗ gnns (+1) = 0 ✓
cybernetics (-1) ⊗ cats-for-ai (0) ⊗ open-games (+1) = 0 ✓
poly-functors (-1) ⊗ cats-for-ai (0) ⊗ para-morphisms (+1) = 0 ✓
causal-abstraction (-1) ⊗ cats-for-ai (0) ⊗ llm-semantics (+1) = 0 ✓
```

## Inaccessible Worlds Protocol

For each inaccessible world (no predecessor in accessibility relation):

```python
class InaccessibleWorld:
    """A world with no accessible predecessors - epistemic ground truth"""

    def __init__(self, seed: int, trit: int):
        self.seed = seed
        self.trit = trit  # -1, 0, +1
        self.color = self._maximal_color()
        self.accessible_from = set()  # empty = inaccessible

    def _maximal_color(self) -> dict:
        """Assign maximally saturated color based on trit"""
        hue_base = {-1: 240, 0: 120, 1: 0}[self.trit]  # blue/green/red
        hue = (hue_base + (self.seed * 37) % 60) % 360
        return {"h": hue, "s": 1.0, "l": 0.5}  # MAXIMAL saturation

    def poly_action(self, p: "Poly") -> "InaccessibleWorld":
        """Apply polynomial functor action"""
        new_seed = (self.seed * p.positions + sum(p.directions)) % (2**64)
        new_trit = (self.trit + p.trit) % 3
        return InaccessibleWorld(new_seed, new_trit)
```

## YouTube Resources

All lectures available: [YouTube Playlist](https://www.youtube.com/playlist?list=PLSdFiFTAI4sQ0Rg4BIZcNnU-45I9DI-VB)

| Lecture | Views | Key Insight |
|---------|-------|-------------|
| Why Category Theory? | 24K+ | Compositionality = modularity |
| Optics and Lenses | 15K+ | Chain rule = lens composition |
| Categorical Cybernetics | 10K+ | Agency via parametrised optics |
| Sheaves for AI | 8K+ | Local-to-global inference |

## Commands

```bash
# Watch lecture
just cats4ai-watch LECTURE_NUM

# Run optics demo
just cats4ai-optics-demo

# Generate inaccessible worlds
just cats4ai-worlds N

# Color palette
just cats4ai-colors --maximal

# Integration check
just cats4ai-integrate SKILL_NAME
```

## Babashka Integration

```clojure
#!/usr/bin/env bb
;; cats4ai.bb - Categories for AI utilities

(ns cats4ai
  (:require [babashka.http-client :as http]
            [cheshire.core :as json]))

(def LECTURES
  [{:week 1 :title "Why Category Theory?" :speaker "Gavranović" :trit 0}
   {:week 2 :title "Categories & Functors" :speaker "Veličković" :trit 0}
   {:week 3 :title "Optics & Lenses" :speaker "Gavranović" :trit -1}
   {:week 4 :title "Geometric DL" :speaker "de Haan" :trit +1}
   {:week 5 :title "Monads & LSTMs" :speaker "Dudzik" :trit 0}])

(defn gf3-conservation? [lectures]
  (zero? (mod (reduce + (map :trit lectures)) 3)))

(defn inaccessible-world [seed]
  {:seed seed
   :trit (case (mod seed 3) 0 :ERGODIC 1 :PLUS 2 :MINUS)
   :accessible-from #{}
   :color {:h (mod (* seed 37) 360) :s 1.0 :l 0.5}})

(defn -main [& args]
  (println "cats.for.ai - Categories for AI")
  (println "GF(3) conserved?" (gf3-conservation? LECTURES))
  (println "Inaccessible worlds:"
           (map inaccessible-world (range 3))))

(when (= *file* (System/getProperty "babashka.file"))
  (apply -main *command-line-args*))
```

## References

### Primary
- [cats.for.ai](https://cats.for.ai) - Official site
- [YouTube Playlist](https://www.youtube.com/playlist?list=PLSdFiFTAI4sQ0Rg4BIZcNnU-45I9DI-VB)
- [Zulip Chat](https://cats-for-ai.zulipchat.com/)

### Papers
- Gavranović et al. "Categorical Foundations of Gradient-Based Learning" (2024)
- Hedges "Compositional Game Theory" (2016)
- Spivak "Poly: An abundant categorical setting" (2020)
- Bradley "Language Models as Semantic Functors" (2023)
- Gebhart "Sheaf Neural Networks" (2022)

### Related Skills
- `open-games` - Hedges' compositional games
- `catsharp` - Spivak's Cat# = Comod(P)
- `topos-catcolab` - Topos collaborative CT
- `cybernetic-open-game` - Cybernetic feedback
- `sheaf-laplacian-coordination` - Gebhart sheaves
- `crdt` - Join-semilattice CRDTs
- `derangement-crdt` - Colorable derangements

---

**Skill Name**: cats-for-ai
**Type**: Categorical Machine Learning
**Trit**: 0 (ERGODIC)
**Poly**: Inaccessible worlds as colors maximal
**GF(3)**: Conserved across all triads
