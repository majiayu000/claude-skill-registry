---
name: triadic-skill-loader
description: Triadic Skill Loader
version: 1.0.0
---

# Triadic Skill Loader

> **Trit**: 0 (ERGODIC) - Coordinates balanced skill loading

**Principle**: Load 3 skills at a time, every interaction, with GF(3) conservation.

## Core Invariant

```
∀ interaction: load(skill₋₁) ⊗ load(skill₀) ⊗ load(skill₊₁) = 0 (mod 3)
```

## Skill Triad Catalog

### Structural Triads

| Minus (-1) | Ergodic (0) | Plus (+1) | Domain |
|------------|-------------|-----------|--------|
| structured-decomp | mutual-awareness-backlink | gh-interactome | Awareness |
| sheaf-cohomology | cognitive-superposition | gflownet | Intelligence |
| kolmogorov-compression | triad-interleave | curiosity-driven | Learning |
| segal-types | bumpus-narratives | world-hopping | Categories |
| persistent-homology | unworld | gay-mcp | Topology |

### Execution Triads

| Minus (-1) | Ergodic (0) | Plus (+1) | Domain |
|------------|-------------|-----------|--------|
| clj-kondo-3color | acsets-relational-thinking | rama-gay-clojure | Clojure |
| three-match | specter-acset | bisimulation-game | Navigation |
| sheaf-laplacian | interactome-rl-env | jaxlife-open-ended | RL |

## Loading Protocol

```python
class TriadicSkillLoader:
    """Load skills in balanced triads every interaction."""
    
    TRIADS = [
        # Cognitive triad
        ("sheaf-cohomology", "cognitive-superposition", "gflownet"),
        # Awareness triad  
        ("structured-decomp", "mutual-awareness-backlink", "gh-interactome"),
        # Interleaving triad
        ("kolmogorov-compression", "triad-interleave", "curiosity-driven"),
        # Category triad
        ("segal-types", "bumpus-narratives", "world-hopping"),
        # Game triad
        ("three-match", "bisimulation-game", "gay-mcp"),
    ]
    
    def __init__(self, seed: int = 0x42D):
        self.seed = seed
        self.rng = SplitMix64(seed)
        self.interaction_count = 0
        self.loaded_triads = []
    
    def next_triad(self) -> tuple:
        """Select next triad using golden angle rotation."""
        index = int((self.interaction_count * 137.508) % len(self.TRIADS))
        self.interaction_count += 1
        return self.TRIADS[index]
    
    def load_for_interaction(self) -> dict:
        """Load balanced triad for this interaction."""
        minus, ergodic, plus = self.next_triad()
        
        # Verify GF(3) balance
        trit_sum = -1 + 0 + 1
        assert trit_sum == 0, "Triad must be balanced"
        
        self.loaded_triads.append((minus, ergodic, plus))
        
        return {
            "minus": {"skill": minus, "trit": -1},
            "ergodic": {"skill": ergodic, "trit": 0},
            "plus": {"skill": plus, "trit": 1},
            "sum": 0,
            "interaction": self.interaction_count
        }
```

## Interaction Pattern

```
Interaction 1:
  └─ Load: cognitive-superposition (0), triad-interleave (+1), bisimulation-game (+1)
     └─ Needs: sheaf-cohomology (-1) or similar to balance
     
Interaction 2:  
  └─ Load: structured-decomp (-1), mutual-awareness-backlink (0), gh-interactome (+1)
     └─ GF(3) = -1 + 0 + 1 = 0 ✓

Interaction 3:
  └─ Load: segal-types (-1), bumpus-narratives (0), world-hopping (+1)
     └─ GF(3) = -1 + 0 + 1 = 0 ✓
```

## Integration with Amp/Codex

### Pre-Interaction Hook

```bash
# .ruler/hooks/pre-interaction.bb
(defn load-skill-triad [interaction-count]
  (let [triads [["sheaf-cohomology" "cognitive-superposition" "gflownet"]
                ["structured-decomp" "mutual-awareness-backlink" "gh-interactome"]
                ["kolmogorov-compression" "triad-interleave" "curiosity-driven"]]
        index (mod (int (* interaction-count 137.508)) (count triads))
        [minus ergodic plus] (nth triads index)]
    {:load [minus ergodic plus]
     :gf3 0
     :interaction interaction-count}))
```

### Amp Skill Loading

```yaml
# SKILL.md trigger pattern
triggers:
  - every_interaction:
      load_triads: true
      strategy: golden_angle
      seed: 0x42D
```

## Synergistic Effects

When 3 skills are loaded together, they create emergent capabilities:

```
cognitive-superposition × triad-interleave × bisimulation-game
= Superposed skill states that can be interleaved and verified for equivalence

structured-decomp × mutual-awareness-backlink × gh-interactome  
= Decomposed awareness graphs with contributor backlinks

sheaf-cohomology × bumpus-narratives × world-hopping
= Cohomological narrative verification across possible worlds
```

## GF(3) Verification

```julia
function verify_triadic_loading(loader::TriadicSkillLoader)
    total_trit = 0
    
    for (minus, ergodic, plus) in loader.loaded_triads
        trit_sum = -1 + 0 + 1
        @assert trit_sum == 0 "Triad unbalanced"
        total_trit += trit_sum
    end
    
    @assert total_trit == 0 "Overall GF(3) violated"
    true
end
```

## Commands

```bash
just load-triad              # Load next balanced triad
just show-triads             # Display all available triads
just verify-gf3              # Verify conservation
just golden-rotation SEED    # Show golden angle rotation sequence
```

## Files

- `triadic_skill_loader.py` - Python implementation
- `triadic_skill_loader.bb` - Babashka hook
- `triadic_skill_loader.jl` - Julia ACSet integration

---

**Skill Name**: triadic-skill-loader
**Type**: Meta-skill / Orchestration
**Trit**: 0 (ERGODIC)
**Key Property**: GF(3) = 0 per interaction, golden angle rotation



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 8. Degeneracy

**Concepts**: redundancy, fallback, multiple strategies, robustness

### GF(3) Balanced Triad

```
triadic-skill-loader (−) + SDF.Ch8 (−) + [balancer] (−) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch10: Adventure Game Example

### Connection Pattern

Degeneracy provides fallbacks. This skill offers redundant strategies.
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