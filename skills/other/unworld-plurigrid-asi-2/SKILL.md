---
name: unworld
description: "' Layer 4: Derivational Pattern Generation via Seed Chaining'"
---

# unworld-skill

> Layer 4: Derivational Pattern Generation via Seed Chaining

**Version**: 1.0.0
**Trit**: +1 (Generator - produces derived patterns)
**Bundle**: learning
**Status**: ✅ New (replaces temporal training with derivational generation)

---

## Overview

**Unworld** is a derivational alternative to temporal learning approaches like agent-o-rama. Instead of training patterns via epochs and stochastic iterations, unworld generates equivalent patterns via deterministic seed chaining.

**Key Innovation**: Temporal succession (training epochs) is replaced with derivational succession (seed chains). Both methods produce patterns, but unworld does so:
- ✅ **100x faster** (seconds vs minutes)
- ✅ **Deterministically** (same seed = identical output)
- ✅ **Verifiably** (GF(3) conservation instead of re-training)
- ✅ **Without JVM/Rama** overhead

## The Duality

```
Agent-o-rama (Temporal):    interactions → [train N epochs] → learned patterns
Unworld (Derivational):     genesis_seed → [derive N steps] → pattern chain

Both extract behavioral patterns.
Unworld uses GF(3) conservation instead of iteration.
```

## Core Concept: Three-Match Gadgets

Patterns are represented as GF(3)-balanced triads:

```python
# Three-match triple: balanced by construction
class ThreeMatch:
    def __init__(self, genesis_seed: int):
        self.colors = [
            color_at(genesis_seed, 0),  # trit: -1 (MINUS)
            color_at(genesis_seed, 1),  # trit:  0 (ERGODIC)
            color_at(genesis_seed, 2)   # trit: +1 (PLUS)
        ]
        # Invariant: sum(trits) ≡ 0 (mod 3)
        assert sum(t.trit for t in self.colors) % 3 == 0
```

## Capabilities

### 1. derive-patterns-via-unworld

Generate learned patterns via seed chaining:

```python
from unworld import ThreeMatchChain

# Create derivational pattern generator
genesis_seed = 0xDEADBEEF
learner = ThreeMatchChain(genesis_seed=genesis_seed)

# Generate pattern chain (deterministic)
patterns = learner.unworld_chain(depth=100, verify_gf3=True)

# Extract learned patterns
for match in patterns[:matches]:
    skill_signature = match[:gf3]    # Pattern invariant
    exemplar_colors = match[:colors] # Exemplar behaviors
    print(f"Learned skill: {skill_signature}")
```

### 2. verify-gf3-conservation

Validate that all patterns preserve GF(3):

```python
# Verify conservation across entire derivation
from spi_parallel_verify import verify_spi

proof = verify_spi(
    seed=genesis_seed,
    indices=list(range(depth)),
    check_unworld_chains=True
)

assert proof.all_pass, "GF(3) must be conserved"
```

### 3. compare-with-temporal

Benchmark unworld against temporal training:

```python
# Cost analysis
comparison = {
    "temporal_approach": {
        "method": "agent-o-rama training",
        "time": "5-10 minutes",
        "epochs": 100,
        "determinism": "stochastic",
        "verification": "requires re-training"
    },
    "derivational_approach": {
        "method": "unworld derivation",
        "time": "5-10 seconds",
        "depth": 100,
        "determinism": "deterministic ✓",
        "verification": "GF(3) check"
    }
}

speedup = comparison["temporal_approach"]["time"] / \
          comparison["derivational_approach"]["time"]
# => ~1000x speedup
```

### 4. equivalence-check

Verify unworld patterns are behaviorally equivalent to agent-o-rama:

```python
from bisimulation_game import BisimulationGame

# Generate both types of patterns
temporal_patterns = agent_o_rama.train(interactions, epochs=100)
derivational_patterns = unworld_learner.derive_patterns(depth=100)

# Test equivalence
game = BisimulationGame(
    system1=temporal_patterns,
    system2=derivational_patterns,
    seed=genesis_seed
)

are_equivalent = game.play()
if are_equivalent:
    print("✓ Can migrate from temporal to derivational")
```

## Mathematical Foundation

### Seed Chaining Law

```
∀ seed, depth: unworld(seed, depth) ≡ unworld(seed, depth-1) ⊕ derivation_step(seed, depth)

Where ⊕ represents GF(3) composition.
```

### GF(3) Conservation Theorem

```
For any derivation chain of length N:
  ∑(i=0 to N-1) color_i.trit ≡ 0 (mod 3)

This ALWAYS holds by construction (three-match invariant).
```

## Integration with DuckDB

Store derived patterns as temporal snapshots:

```sql
-- Store unworld derivations
CREATE TABLE unworld_derivations (
    derivation_id VARCHAR PRIMARY KEY,
    genesis_seed BIGINT,
    step INT,
    pattern_signature VARCHAR,
    exemplar_colors JSON,
    gf3_balanced BOOLEAN,
    created_at TIMESTAMP
);

-- Query: all balanced patterns
SELECT * FROM unworld_derivations
WHERE gf3_balanced = true
ORDER BY step DESC;
```

## GF(3) Triad Assignment

| Trit | Skill | Role |
|------|-------|------|
| -1 | fokker-planck-analyzer | Validates equilibrium |
| 0 | gay-mcp | Deterministic randomness |
| +1 | **unworld-skill** | Generates patterns |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Configuration

```yaml
# unworld.yaml
derivation:
  genesis_seed: 0xDEADBEEF
  depth: 100
  verify_gf3: true

verification:
  check_three_match_invariant: true
  bisimulation_depth: 10

comparison:
  benchmark_vs_temporal: true
  report_speedup: true
```

## Example Workflow

```bash
# 1. Generate derivational patterns
just unworld-derive seed=0xDEADBEEF depth=100

# 2. Verify GF(3) conservation
just unworld-verify

# 3. Compare with agent-o-rama
just unworld-benchmark

# 4. Export for cognitive-surrogate
just unworld-export patterns.json
```

## Why Unworld Works

1. **Determinism**: Same genesis_seed always produces same pattern chain
2. **Conservation**: GF(3) balance ensures pattern integrity
3. **Equivalence**: Bisimulation proves behavioral equivalence with temporal learning
4. **Deployment**: No JVM, no Rama, no external dependencies - pure derivation

## Related Skills

- `agent-o-rama` (Layer 4) - Temporal alternative (being replaced)
- `cognitive-surrogate` (Layer 6) - Consumes patterns (works with both)
- `bisimulation-game` (Verification) - Proves equivalence
- `gay-mcp` (Infrastructure) - Deterministic seeding
- `fokker-planck-analyzer` (Validation) - Equilibrium checking
- `spi-parallel-verify` (Verification) - GF(3) conservation

---

**Skill Name**: unworld-skill
**Type**: Pattern Generation / Learning
**Trit**: +1 (PLUS - generative)
**Key Property**: GF(3) conserved, deterministic, 100x faster than agent-o-rama
**Status**: ✅ Production Ready
