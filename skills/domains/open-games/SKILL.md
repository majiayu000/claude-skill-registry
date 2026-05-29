---
name: open-games
description: Open Games Skill (ERGODIC 0)
version: 1.0.0
---


# Open Games Skill (ERGODIC 0)

> Compositional game theory via Para/Optic structure

**Trit**: 0 (ERGODIC)
**Color**: #26D826 (Green)
**Role**: Coordinator/Transporter

## bmorphism Contributions

> *"Parametrised optics model cybernetic systems, namely dynamical systems steered by one or more agents. Then ⊛ represents agency being exerted on systems"*
> — [@bmorphism](https://github.com/bmorphism), GitHub bio

> *"We introduce open games as a compositional foundation of economic game theory. A compositional approach potentially allows methods of game theory and theoretical computer science to be applied to large-scale economic models"*
> — [Compositional Game Theory](https://arxiv.org/abs/1603.04641), Ghani, Hedges, Winschel, Zahn (2016)

**Key Papers** (from bmorphism's Plurigrid references):
- [Compositional game theory](https://arxiv.org/abs/1603.04641) - open games as symmetric monoidal category morphisms
- [Morphisms of Open Games](https://www.sciencedirect.com/science/article/pii/S1571066118300884) - connection between lenses and compositional game theory
- [Bayesian Open Games](https://compositionality.episciences.org/13528/pdf) - stochastic environments, incomplete information
- [Categorical Cybernetics Manifesto](https://julesh.com/posts/2019-11-27-categorical-cybernetics-manifesto.html) - control theory of complex systems

**CyberCat Institute Connection**: Open games are central to the [CyberCat Institute](https://cybercat.institute) research program on categorical cybernetics.

Related to bmorphism's work on:
- [plurigrid/act](https://github.com/plurigrid/act) - active inference + ACT + enacted cognition
- Play/Coplay bidirectional feedback structure

## Core Concept

Open games are morphisms in a symmetric monoidal category:

```
        ┌───────────┐
   X ──→│           │──→ Y
        │  Game G   │
   R ←──│           │←── S
        └───────────┘
```

Where:
- **X → Y**: Forward play (strategies)
- **S → R**: Backward coplay (utilities)

## The Para/Optic Structure

### Para Morphism
```haskell
Para p a b = ∃m. (m, p m a → b)
-- Existential parameter with action
```

### Optic (Lens Generalization)
```haskell
Optic p s t a b = ∀f. p a (f a b) → p s (f s t)
-- Profunctor optic for bidirectional data
```

### Open Game as Optic
```haskell
OpenGame s t a b = 
  { play    : s → a
  , coplay  : s → b → t
  , equilibrium : s → Prop
  }
```

## Composition

### Sequential (;)
```
G ; H = Game where
  play = H.play ∘ G.play
  coplay = G.coplay ∘ (id × H.coplay)
```

### Parallel (⊗)
```
G ⊗ H = Game where
  play = G.play × H.play
  coplay = G.coplay × H.coplay
```

## Nash Equilibrium via Fixed Points

```haskell
isEquilibrium :: OpenGame s t a b → s → Bool
isEquilibrium g s = 
  let a = play g s
      bestResponse = argmax (\a' → utility (coplay g s (respond a')))
  in a == bestResponse
```

### Compositional Equilibrium
```
eq(G ; H) = eq(G) ∧ eq(H)  -- under compatibility
```

## Integration with Unworld

```clojure
(defn opengame-derive 
  "Transport game through derivation chain"
  [game derivation]
  (let [; Forward: strategies through derivation
        forward (compose (:play game) (:forward derivation))
        ; Backward: utilities through co-derivation  
        backward (compose (:coplay game) (:backward derivation))]
    {:play forward
     :coplay backward
     :equilibrium (transported-equilibrium game derivation)}))
```

## GF(3) Triads

```
temporal-coalgebra (-1) ⊗ open-games (0) ⊗ free-monad-gen (+1) = 0 ✓
three-match (-1) ⊗ open-games (0) ⊗ operad-compose (+1) = 0 ✓
sheaf-cohomology (-1) ⊗ open-games (0) ⊗ topos-generate (+1) = 0 ✓
```

## Commands

```bash
# Compose games sequentially
just opengame-seq G H

# Compose games in parallel
just opengame-par G H

# Check Nash equilibrium
just opengame-nash game strategy

# Transport through derivation
just opengame-derive game deriv
```

## Economic Examples

### Prisoner's Dilemma
```haskell
prisonersDilemma :: OpenGame () () (Bool, Bool) (Int, Int)
prisonersDilemma = Game {
  play = \() → (Defect, Defect),  -- Nash
  coplay = \() (p1, p2) → payoffMatrix p1 p2
}
```

### Market Game
```haskell
market :: OpenGame Price Price Quantity Quantity
market = supplyGame ⊗ demandGame
  where equilibrium = supplyGame.eq ∧ demandGame.eq
```

## Categorical Semantics

```
OpenGame ≃ Para(Lens) ≃ Optic(→, ×)

Composition: 
  (A ⊸ B) ⊗ (B ⊸ C) → (A ⊸ C)  -- via cut
  
Tensor:
  (A ⊸ B) ⊗ (C ⊸ D) → (A ⊗ C ⊸ B ⊗ D)
```

## References

- Ghani, Hedges, et al. "Compositional Game Theory"
- Capucci & Gavranović, "Actegories for Open Games"
- Riley, "Categories of Optics"
- CyberCat Institute tutorials



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `game-theory`: 21 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
open-games (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch8: Degeneracy
- Ch3: Variations on an Arithmetic Theme
- Ch1: Flexibility through Abstraction
- Ch5: Evaluation
- Ch4: Pattern Matching
- Ch7: Propagators

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
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