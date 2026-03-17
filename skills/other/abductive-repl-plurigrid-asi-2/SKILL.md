---
name: abductive-repl
description: ' Hypothesis-Test Loops via REPL for Exploratory Abductive Inference'
metadata:
  trit: 0
---

# abductive-repl

> Hypothesis-Test Loops via REPL for Exploratory Abductive Inference

**Version**: 1.0.0  
**Trit**: 0 (Ergodic - coordinates inference)  
**Bundle**: repl  

## Overview

Abductive-REPL enables exploratory abductive reasoning through an interactive REPL. Given observed outcomes, it generates hypotheses, tests them, and refines understanding through iterative loops.

## Core Concept

```
Observation → Generate Hypotheses → Test → Refine → Repeat

Abduction: Given effect E and rule "A implies E", 
           hypothesize A as possible cause.
```

## Capabilities

### 1. abduce-from-observation

Generate hypotheses from observed behavior.

```python
from abductive_repl import AbductiveEngine

engine = AbductiveEngine(seed=0xf061ebbc2ca74d78)

# Observed: A specific color was generated
observed_color = RGB(216, 125, 157)

hypotheses = engine.abduce(
    observation=observed_color,
    search_space="invader_ids",
    search_range=range(1, 10000),
    top_k=5
)

# Returns ranked hypotheses:
# [
#   {hypothesis: "invader_id=42069", confidence: 0.98, distance: 0.02},
#   {hypothesis: "invader_id=42070", confidence: 0.45, distance: 0.55},
#   ...
# ]
```

### 2. repl-commands

Interactive REPL mode for exploration.

```
gay> !teleport 42069
Teleporting to invader 42069...
  Source color: RGB(180, 90, 120)
  Derangement: cyclic_1
  World color: RGB(216, 125, 157)
  Tropical t: 0.69

gay> !abduce 216 125 157
Generating hypotheses for RGB(216, 125, 157)...
  [1] invader_id=42069 (confidence: 0.98)
  [2] invader_id=42070 (confidence: 0.45)
  [3] invader_id=41999 (confidence: 0.23)

gay> !jump 1
Jumping to hypothesis 1 (invader_id=42069)...
  ✓ Hypothesis confirmed!

gay> !neighbors 5
Finding 5 neighbors of invader 42069...
  42068: RGB(214, 123, 155) distance=0.02
  42070: RGB(218, 127, 159) distance=0.02
  42067: RGB(212, 121, 153) distance=0.04
  ...

gay> !test 100
Running abductive roundtrip tests (n=100)...
  ✓ 100/100 passed (100% accuracy)
  Average inference time: 2.3ms
```

### 3. forward-simulate

Simulate forward from hypothesis to predict observations.

```python
simulation = engine.forward_simulate(
    hypothesis="invader_id=42069",
    seed=0xf061ebbc2ca74d78
)

# Returns:
# {
#   id: 42069,
#   source: RGB(180, 90, 120),
#   derangement_idx: 1,
#   tropical_t: 0.69,
#   world: RGB(216, 125, 157),
#   properties: {
#     spi_determinism: True,
#     derangement_bijectivity: True,
#     tropical_idempotence: True,
#     spin_consistency: True
#   }
# }
```

### 4. roundtrip-test

Verify abductive inference accuracy.

```python
def abductive_roundtrip_test(id: int, seed: int) -> bool:
    """
    Forward simulate → Abduce back → Check if recovered
    """
    # Forward
    sim = forward_simulate(id, seed)
    
    # Abduce
    hypotheses = abduce(
        observation=sim.world,
        search_range=range(id - 100, id + 100),
        top_k=1
    )
    
    # Verify
    return hypotheses[0].hypothesis == f"invader_id={id}"

# Run batch
results = [abductive_roundtrip_test(i, SEED) for i in range(1, 1001)]
accuracy = sum(results) / len(results)
assert accuracy > 0.99
```

### 5. hypothesis-refinement

Iteratively refine hypotheses based on feedback.

```python
# Initial hypothesis
hypothesis = engine.initial_hypothesis(observation)

for iteration in range(max_iterations):
    # Test hypothesis
    prediction = engine.predict(hypothesis)
    error = distance(prediction, observation)
    
    if error < threshold:
        break
    
    # Refine based on error
    hypothesis = engine.refine(hypothesis, error, observation)

print(f"Converged after {iteration} iterations")
```

## REPL Command Reference

| Command | Description |
|---------|-------------|
| `!teleport <id>` | Jump to invader's world state |
| `!world` | Show current world state |
| `!back` | Return to previous world |
| `!abduce r g b` | Infer invader from observed RGB |
| `!jump <n>` | Jump to nth hypothesis |
| `!neighbors [r]` | Explore nearby invaders (radius r) |
| `!test [n]` | Run n abductive roundtrip tests |
| `!property <name>` | Test specific property |
| `!history` | Show teleportation history |
| `!seed [s]` | Get/set RNG seed |

## Properties (Testable Predicates)

```python
class SPIDeterminism:
    """Same input always produces same output."""
    
class DerangementBijectivity:
    """Derangement is reversible."""
    
class TropicalIdempotence:
    """tropical_blend(x, x, t) = x for all t."""
    
class SpinConsistency:
    """Spin direction preserved through transformations."""

def test_all_properties(id: int, seed: int) -> dict:
    return {
        "spi_determinism": test_property(SPIDeterminism(), id, seed),
        "derangement_bijectivity": test_property(DerangementBijectivity(), id, seed),
        "tropical_idempotence": test_property(TropicalIdempotence(), id, seed),
        "spin_consistency": test_property(SpinConsistency(), id, seed)
    }
```

## GF(3) Triad Integration

| Trit | Skill | Role |
|------|-------|------|
| -1 | slime-lisp | Validates REPL expressions |
| 0 | **abductive-repl** | Coordinates inference |
| +1 | cider-clojure | Generates evaluations |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Configuration

```yaml
# abductive-repl.yaml
inference:
  search_range_default: 10000
  top_k_default: 5
  confidence_threshold: 0.7
  max_iterations: 100

testing:
  roundtrip_batch_size: 100
  property_tests: true

repl:
  history_file: "~/.abductive_history"
  prompt: "gay> "
  
reproducibility:
  seed: 0xf061ebbc2ca74d78
```

## Justfile Recipes

```makefile
# Start abductive REPL
abduce-repl:
    julia --project=Gay.jl -e 'using Gay; Gay.repl()'

# Run roundtrip tests
abduce-test n="100":
    julia --project=Gay.jl -e 'using Gay; Gay.test_abductive({{n}})'

# Abduce from color
abduce-color r g b:
    julia --project=Gay.jl -e 'using Gay; Gay.abduce(RGB({{r}}/255, {{g}}/255, {{b}}/255))'
```

## Related Skills

- `world-hopping` - Possible world navigation
- `unworld` - Derivation chains
- `gay-mcp` - Color generation
- `cider-clojure`, `slime-lisp`, `geiser-chicken` - REPL backends
