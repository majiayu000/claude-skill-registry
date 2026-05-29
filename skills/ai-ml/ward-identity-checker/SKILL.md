---
name: ward-identity-checker
description: Ward Identity Checker
version: 1.0.0
---

# Ward Identity Checker

Verify GF(3) conservation as Ward identities across RG flow with Markov blanket separation.

## Seed
```
741086072858456200
```

## Core Principle

Ward identities express symmetry conservation: **Σ trit = 0 (mod 3)** at every renormalization group (RG) level. Violations indicate "relevant operators" that break the symmetry.

## MCP Calibration Data

```yaml
markov_blanket:
  internal_states: ["#3FF1A7", "#10B99D", "#DF9811"]
  sensory_indices: [1, 2, 3]
  
active_inference:
  prediction_error: 0.5692
  free_energy: 0.6692
  recommendation: perceptual_inference
  
reafference:
  prediction: "#F7E182"
  sensation: "#3FF1A7"
  result: identity_mismatch
```

## Predicates

### GF3Conserved(level)
```
GF3Conserved(L) := Σᵢ trit(cᵢ) ≡ 0 (mod 3)
  where cᵢ ∈ colors_at_level(L)
```

### BlanketIntact(state)
```
BlanketIntact(s) := ∀ internal ∈ s.internal_states,
  ∃ blanket ∈ s.sensory_states ∪ s.active_states
  such that internal ⊥ external | blanket
```

### NoLeakage(flow)
```
NoLeakage(f) := GF3Conserved(f.source) ∧ GF3Conserved(f.target)
  ∧ Σ trit(f.source) = Σ trit(f.target)
```

## Ward Identity Check Protocol

```python
def check_ward_identity(colors: list[str], level: int) -> dict:
    """Verify Σ trit = 0 at RG level."""
    trits = [hex_to_trit(c) for c in colors]
    total = sum(trits) % 3
    
    return {
        "level": level,
        "trit_sum": total,
        "conserved": total == 0,
        "violation_type": None if total == 0 else "relevant_operator",
        "correction_needed": (3 - total) % 3
    }

def hex_to_trit(hex_color: str) -> int:
    """Map hex to GF(3) via hue angle."""
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    hue = compute_hue(r, g, b)
    return int(hue / 120) % 3  # 0-119 → 0, 120-239 → 1, 240-359 → 2
```

## Markov Blanket Separation

```
┌─────────────────────────────────────────────┐
│                 EXTERNAL                     │
│   (exafference: world-caused sensations)    │
├─────────────────────────────────────────────┤
│              BLANKET STATES                  │
│  Sensory: idx [1,2,3] → colors observed     │
│  Active:  predictions emitted               │
├─────────────────────────────────────────────┤
│                 INTERNAL                     │
│  #3FF1A7 (trit 1) ─┐                        │
│  #10B99D (trit 1) ─┼─ Σ = 3 ≡ 0 (mod 3) ✓  │
│  #DF9811 (trit 1) ─┘                        │
└─────────────────────────────────────────────┘
```

## Violation Detection

When reafference check shows identity mismatch (prediction ≠ sensation):

| Condition | Diagnosis | Action |
|-----------|-----------|--------|
| `GF3Conserved ∧ ¬BlanketIntact` | Boundary leak | Reseal blanket |
| `¬GF3Conserved ∧ BlanketIntact` | Relevant operator | Add counterterm |
| `¬GF3Conserved ∧ ¬BlanketIntact` | Full symmetry break | RG flow unstable |

## Usage

```bash
# Via Gay.jl MCP
gay_seed 741086072858456200
gay_markov_blanket --internal-seed 741086072858456200 --sensory-indices "1,2,3"

# Check conservation
just ward-check --level 0 --colors "#3FF1A7,#10B99D,#DF9811"
```

## Integration

- **cybernetic-immune**: Use Ward violations as non-self markers
- **active-inference**: Free energy ≈ Ward violation magnitude
- **unworld**: Color chain derivations must preserve Ward identity

## References

- Ward-Takahashi identities in QFT
- Friston's Markov blanket formalism
- GF(3) trit arithmetic for color conservation



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
ward-identity-checker (○) + SDF.Ch3 (○) + [balancer] (○) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch4: Pattern Matching
- Ch10: Adventure Game Example

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