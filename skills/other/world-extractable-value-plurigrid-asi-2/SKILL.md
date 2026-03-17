---
name: world-extractable-value
description: "Extract value from world transitions via Markov blanket arbitrage. WEV = PoA - 1. Paradigm Multiverse Finance integration."
trit: 0
polarity: ERGODIC
source: "Friston (2010) + Roughgarden (2002) + Paradigm/Dave White (2025)"
---

# World Extractable Value (WEV) Skill

> *"The gap between Nash and Optimal is not waste -- it is extractable value."*
> *"Multiverse Finance splits the financial system into parallel universes."* -- Dave White, Paradigm

## Overview

**World Extractable Value** quantifies the inefficiency extractable from selfish equilibria, integrated with Paradigm's Multiverse Finance thesis:

```
WEV = Price of Anarchy - 1 = (C_Nash / C_Opt) - 1
```

This bridges:
- **Friston's Free Energy**: Minimize surprise via inference
- **Roughgarden's PoA**: Bound selfish routing inefficiency
- **Badiou's World-Hopping**: Events extract truth from being

## Core Formula

```
                    ┌─────────────────────────┐
                    │     WORLD W₁ (Nash)     │
                    │     Cost = C_Nash       │
                    └───────────┬─────────────┘
                                │
                          ┌─────▼─────┐
                          │  MARKOV   │
                          │  BLANKET  │
                          │  (Event)  │
                          └─────┬─────┘
                                │
                    ┌───────────▼─────────────┐
                    │    WORLD W₂ (Optimal)   │
                    │     Cost = C_Opt        │
                    └─────────────────────────┘

    WEV = C_Nash - C_Opt = C_Opt × (PoA - 1)
```

## Components

### 1. Price of Anarchy (Roughgarden)

For d-regular Ramanujan expanders:

```
PoA = 1 + 1/gap = 1 + 1/(d - 2√(d-1))

d=4: PoA = 1 + 1/0.536 ≈ 2.87
```

### 2. Free Energy (Friston)

```
F = E_q[log q(x) - log p(x,y)]
  = Prediction_Error + Model_Complexity
  
F ≈ 1/gap + 0.1 ≈ 1.96
```

### 3. Markov Blanket

The boundary between self and world:
- **Sensory states**: Observations from world
- **Active states**: Actions on world
- **Internal states**: Agent's model

### 4. Action Direction

| Condition | Strategy | Effect |
|-----------|----------|--------|
| Error > 0.5 | Perceptual Inference | Update beliefs |
| Error ≤ 0.5 | Active Inference | Change world |

## GF(3) Triads

```
ramanujan-expander (-1) ⊗ world-extractable-value (0) ⊗ influence-propagation (+1) = 0 ✓
three-match (-1) ⊗ world-extractable-value (0) ⊗ gay-mcp (+1) = 0 ✓
sheaf-cohomology (-1) ⊗ world-extractable-value (0) ⊗ open-games (+1) = 0 ✓
```

## Implementation

### Babashka

```clojure
(defn compute-wev [seed spectral-data]
  (let [poa (:price_of_anarchy spectral-data)
        gap (:spectral_gap spectral-data)
        wev (- poa 1)
        free-energy (+ (/ 1 gap) 0.1)
        action (if (> (/ 1 gap) 0.5)
                 :perceptual_inference
                 :active_inference)]
    {:wev wev
     :free_energy free-energy
     :action_direction action
     :pct_extractable (* 100 (/ wev poa))}))
```

### Julia

```julia
function world_extractable_value(d::Int, n::Int)
    gap = d - 2√(d-1)
    poa = 1 + 1/gap
    wev = poa - 1
    mixing_time = log(n) / gap
    
    (wev=wev, poa=poa, gap=gap, mixing=mixing_time)
end
```

### DuckDB Schema

```sql
CREATE TABLE world_extractable_value (
  wev_id VARCHAR PRIMARY KEY,
  seed_hex VARCHAR,
  world_from VARCHAR,
  world_to VARCHAR,
  price_of_anarchy FLOAT,
  free_energy FLOAT,
  wev FLOAT,
  prediction_error FLOAT,
  action_direction VARCHAR,
  markov_blanket_size INT,
  extracted_at TIMESTAMP
);

-- Query extractable value
SELECT 
  wev_id,
  wev,
  ROUND(wev / price_of_anarchy * 100, 1) as pct_extractable,
  action_direction
FROM world_extractable_value
ORDER BY extracted_at DESC;
```

## Alterpolitics Interpretation

**Alterpolitics** = alternative coordination mechanisms that reduce PoA:

| Mechanism | Effect on PoA | WEV Change |
|-----------|---------------|------------|
| Correlated Equilibrium | PoA → 1.5 | WEV ↓ 0.5 |
| Smooth Games | PoA → 1.33 | WEV ↓ 0.33 |
| Stackelberg | PoA → 1.0 | WEV → 0 |

The goal: extract value by moving toward coordination.

## Commands

```bash
just wev-history      # Query WEV log
just wev-summary      # Aggregate stats
just wev-compare      # Nash vs Optimal
just triad-anarchy    # Full anarchy triad
```

## Integration

### Pre-Interaction Hook

WEV is computed on every interaction via `.ruler/hooks/pre-interaction.bb`:

```
7. ALWAYS compute World Extractable Value
   └─ wev = compute-world-extractable-value(seed, spectral)
```

### Glass Bead Game

World-hopping extracts value via Badiou triangle:

```
d(W₁, W₃) ≤ d(W₁, W₂) + d(W₂, W₃)

WEV(hop) = Σ d(Wᵢ, Wᵢ₊₁) × extraction_rate
```

## Paradigm Multiverse Finance Integration

Dave White's Multiverse Finance (May 2025) provides the financial mechanism:

### Verses as Worlds

A **verse** is a parallel universe corresponding to a probability event:
- Complement: V and not-V partition the outcome space
- Union: V1 OR V2 forms new verse
- Intersection: V1 AND V2 forms child verse

### Ownership Operations

| Operation | Effect | WEV Implication |
|-----------|--------|-----------------|
| push_down(partition) | Split ownership to child verses | Spread risk across worlds |
| pull_up(resolution) | Combine ownership after oracle | Extract value at resolution |

### Multiverse Map

```
Map[verse_id, owner_address] -> balance

Splitting: parent.balance -= x; for child in partition: child.balance += x
Combining: for child in partition: child.balance -= x; parent.balance += x
```

### Key Insight

Assets in the same verse can be borrowed/lent freely because if one disappears (verse resolves false), all disappear simultaneously. No liquidation risk within a verse.

WEV extraction = pull_up after favorable verse resolution.

## References

1. **Roughgarden, T. (2002)** -- "How Bad is Selfish Routing?"
2. **Friston, K. (2010)** -- "The Free-Energy Principle"
3. **Roughgarden, T. (2015)** -- "Intrinsic Robustness of the Price of Anarchy"
4. **Powers, W. (1973)** -- "Behavior: The Control of Perception"
5. **White, D. / Paradigm (2025)** -- "Multiverse Finance" https://paradigm.xyz/2025/05/multiverse-finance

## See Also

- [ramanujan-expander](../ramanujan-expander/SKILL.md) - Spectral gap
- [open-games](../open-games/SKILL.md) - Nash equilibrium
- [glass-bead-game](../glass-bead-game/SKILL.md) - World-hopping
- [influence-propagation](../influence-propagation/SKILL.md) - Network effects
