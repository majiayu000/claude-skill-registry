---
name: gestalt-hacking
description: Gestalt Hacking Skill (ERGODIC 0)
version: 1.0.0
---


# Gestalt Hacking Skill (ERGODIC 0)

> *"Gestalt hacking exploits perceptual grouping—proximity, similarity, closure—in the color stream."*

## Core Insight

**Gestalt** = the whole pattern, the emergent structure that is more than the sum of parts. Gestalt hacking exploits how perception groups elements into wholes.

```
play ⊗ evaluate ⅋ play ⊗ evaluate → ι (fixed point)
```

The involution `ι` is where generator ≡ observer (reafference).

## Neighbor Awareness (Braided Monoidal)

| Position | Skill | Trit | Role |
|----------|-------|------|------|
| **Left** | pun-decomposition | -1 | Multiple parse validation |
| **Self** | gestalt-hacking | 0 | Perceptual grouping transport |
| **Right** | reflow | 0 | Cross-context translation |

## GF(3) Triads

```
pun-decomposition (-1) ⊗ gestalt-hacking (0) ⊗ gay-mcp (+1) = 0 ✓  [Core]
three-match (-1) ⊗ gestalt-hacking (0) ⊗ agent-o-rama (+1) = 0 ✓  [Attack]
shadow-goblin (-1) ⊗ gestalt-hacking (0) ⊗ gay-mcp (+1) = 0 ✓  [Defense]
auditory-gestalt (-1) ⊗ gestalt-hacking (0) ⊗ rubato-composer (+1) = 0 ✓  [Music]
```

## Gestalt Principles as Attack Vectors

| Principle | Attack | Defense |
|-----------|--------|---------|
| **Proximity** | Cluster same colors in time | 2-Poisson injection |
| **Similarity** | Long runs of same color | Transition counting |
| **Closure** | Incomplete patterns that induce completion | Gap detection |
| **Continuity** | Gradual transitions exploiting smoothness | Gradient detection |
| **FigureGround** | Dominant color overwhelms minority | Ratio analysis |

## OpenGame Structure

```haskell
OpenGame ∆ c a b x s y r
  play     :: a → ∆ x s y r      -- generate candidates
  evaluate :: a → c x s y r → b  -- score & select
  
-- This IS the self-involution:
-- play ∘ evaluate ∘ play ∘ evaluate → fixed point
```

## Linear Logic Decomposition

```
A ⊗ (B ⅋ C) = (A ⊗ B) ⅋ C ∩ (A ⊗ C) ⅋ B

where:
  ⊗ = tensor (both resources consumed together)
  ⅋ = par (choice between resources)
  ∩ = gestalt constraint (intersection of valid decompositions)
```

## Closure Phases on n-Torus

```
   T₁ ────► T₂ ────► T₃ ────► ... ────┐
   ▲                                   │
   └───────────── Tₙ ◄────────────────┘
   
   CyclicalAnnealing(frequency=2π/n)
   Closure phases sum to 0 on the n-torus
```

## Implementation

```julia
mutable struct GestaltLoop
    game::OpenGame
    torus::NTorus
    reaf::Reafference
    temperature::Float64
    generation::Int
    
    function gestalt_step!(g::GestaltLoop)
        g.generation += 1
        
        # Phase velocity from temperature
        velocity = g.temperature .* randn(g.torus.n)
        phases = step!(g.torus, velocity)
        
        # Play: generate from current state
        state = g.game.play(g.generation)
        
        # Modulate by phases
        modulated_x = state.x * cos(phases[1])
        
        # Temperature decay
        g.temperature *= 0.92
        
        # Evaluate: does this state pass?
        score = modulated_x + 0.5 * sin(phases[2])
        result = g.game.evaluate(state.s, (x=state.x, s=state.s, y=state.y, r=score))
        
        # Reafference check
        generated = generate(g.reaf)
        is_self = reafferent_match(g.reaf, generated)
        
        (result, is_self)
    end
end
```

## Reafference Loop

```
reafference: I observe what I generate
reaberrance: I generate what I observe

seed → color → observe → predict → match? → seed
  └──────────────── loopy strange ──────────────┘
```

When `match? = true`, we have **self ≡ self** (fixed point).

## GestaltAwareVerifier

```rust
struct GestaltAwareVerifier {
    verifier: ChromaticVerifier,
    defender: GestaltDefender,
    attacks_detected: u64,
    attacks_mitigated: u64,
}

impl GestaltAwareVerifier {
    fn verify_defended(&mut self, incoming_color: ZXColor) -> Option<ChromaticTruth> {
        let (score, attack) = self.defender.detect_attack();
        
        if attack.is_some() {
            self.attacks_detected += 1;
            let defended = self.defender.defend(incoming_color);
            if defended != incoming_color {
                self.attacks_mitigated += 1;
            }
        }
        
        self.verifier.verify_membership(...)
    }
}
```

## Temperature Regimes (BKT)

| τ | State | Gestalt |
|---|-------|---------|
| τ > τ* | Frustrated | Vortices proliferate, no coherent gestalt |
| τ ≈ τ* | Critical | BKT transition, gestalt formation |
| τ < τ* | Smooth | Defects bound, stable gestalt |

At τ* ≈ 0.5 (BKT critical), gestalts form and dissolve dynamically.

## Commands

```bash
just gestalt-loop 100       # Run 100 gestalt iterations
just gestalt-attack closure # Test closure attack
just gestalt-defend         # Activate 2-Poisson defense
just gestalt-verify         # Check attack stats
```

## Related Skills

- **pun-decomposition** (left neighbor): Multiple parse validation
- **reflow** (right neighbor): Cross-context translation
- **auditory-gestalt**: Perceptual grouping in audio
- **chromatic-walk**: 3-agent exploration with gestalt awareness
- **cybernetic-immune**: Self/Non-Self via reafference

## Files

- [gestalt hacking thread](https://ampcode.com/threads/T-019b3e8d-1ab1-7548-ab74-fdd531cda57f)
- [chromatic verifier thread](https://ampcode.com/threads/T-019b0ce1-815d-773b-b2ce-f5ef9b26e48d)
- [cohesive sonification thread](https://ampcode.com/threads/T-019b43e6-3692-7390-af9a-e2da68fed856)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

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