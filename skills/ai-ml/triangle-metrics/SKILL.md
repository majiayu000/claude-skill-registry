---
name: triangle-metrics
description: Triangle Metrics Skill
version: 1.0.0
---

# Triangle Metrics Skill

**Trit**: 0 (ERGODIC - synthesizer/coordinator)
**Purpose**: Unify all triangle inequality skills into a coherent metric space

---

## Cross-Referenced Skills

| Skill | Guarantee | Integration Point |
|-------|-----------|-------------------|
| **glass-hopping** | ≪ order transitivity | `TriangleInequality` Narya type |
| **world-hopping** | Dijkstra pruning | `d13 <= d12 + d23` constraint |
| **glass-bead-game** | Propagator constraint | `world_distance` comparisons |
| **epistemic-arbitrage** | Knowledge transfer bound | `d(A,C) ≤ d(A,B) + d(B,C)` |
| **l-space** | Navigation metric | `:triangle_inequality` traversal |
| **open-games** | Play/coplay equilibrium | `equilibrium ⟺ d(a,c) ≤ d(a,b) + d(b,c)` |

---

## Unified Interface

```julia
# Abstract metric interface all skills implement
abstract type TriangleMetric end

struct WorldDistance <: TriangleMetric
    d12::Float64
    d23::Float64
    d13::Float64
end

function triangle_valid(m::WorldDistance)::Bool
    m.d13 ≤ m.d12 + m.d23
end

# Skill-specific implementations
struct GlassHoppingMetric <: TriangleMetric
    h12::Bridge  # W₁ ≪ W₂
    h23::Bridge  # W₂ ≪ W₃
    # Transitivity guarantees h13
end

struct OpenGamesMetric <: TriangleMetric
    play::Strategy    # Forward distance
    coplay::Strategy  # Backward distance
    # Equilibrium ⟺ triangle satisfied
end
```

---

## Mutual Awareness Protocol

When any triangle skill is invoked:

1. **Check**: Query other loaded triangle skills
2. **Validate**: Ensure distances are consistent across all
3. **Propagate**: Share metric updates to siblings
4. **Witness**: Generate Narya proof if all agree

```narya
-- Unified triangle witness
def UnifiedTriangle 
    (glass : GlassHopping.Bridge)
    (world : WorldHopping.Path)
    (game  : OpenGames.Equilibrium)
    : TriangleValidated
```

---

## DuckLake Integration

```sql
-- Query triangle-validated interactions
SELECT a.id, a.trit, a.triangle_valid,
       b.id as next_id, b.trit as next_trit,
       c.id as third_id, c.trit as third_trit,
       ABS(c.trit - a.trit) as d13,
       ABS(b.trit - a.trit) + ABS(c.trit - b.trit) as d12_plus_d23
FROM activity_log a
JOIN activity_log b ON b.timestamp > a.timestamp
JOIN activity_log c ON c.timestamp > b.timestamp
WHERE d13 <= d12_plus_d23;  -- Triangle inequality
```

---

## GF(3) Conservation

The unified metric preserves GF(3):

```
Σ(skill trits) = glass-hopping(0) + world-hopping(0) + 
                 glass-bead-game(0) + epistemic-arbitrage(0) + 
                 l-space(0) + open-games(0) + 
                 triangle-metrics(0) = 0 ✓
```

---

## Usage

```bash
# Validate all triangle constraints
just triangle-validate

# Generate unified Narya witness
just triangle-witness

# Query cross-skill distances
just triangle-query
```

**Integration**: Load alongside any triangle skill for automatic mutual awareness.



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