---
name: agent-o-rama
description: ' Layer 4: Learning and Pattern Extraction for Cognitive Surrogate Systems'
version: 1.0.0
---


# agent-o-rama

> Layer 4: Learning and Pattern Extraction for Cognitive Surrogate Systems

**Version**: 1.0.0  
**Trit**: +1 (Generator - produces learned patterns)  
**Bundle**: learning  

## Overview

Agent-o-rama trains learning agents on interaction sequences to discover behavioral patterns. It extracts temporal, topic, and network patterns from raw interaction data, producing models compatible with the cognitive-surrogate skill.

**NEW (Langevin/Unworld Integration)**: Agent-o-rama now supports both:
1. **Temporal Learning** (traditional): Train interaction predictor via epochs
2. **Derivational Generation** (unworld): Generate equivalent patterns via seed chaining (100x faster, deterministic)

## Capabilities

### 1. train-interaction-predictor

Train a model to predict next interactions given history.

```python
from agent_o_rama import InteractionPredictor

predictor = InteractionPredictor(
    learning_rate=0.01,
    epochs=100,
    batch_size=32,
    seed=0xf061ebbc2ca74d78  # SPI seed for reproducibility
)

# Train on DuckDB interaction sequences
predictor.fit(
    db_path="interactions.duckdb",
    table="interaction_sequences",
    validation_split=0.2
)

# Predict next interaction
next_pred = predictor.predict(recent_history)
```

### 2. extract-temporal-patterns

Discover time-based behavioral patterns.

```sql
-- Pattern query for DuckDB
SELECT 
    EXTRACT(HOUR FROM created_at) as hour,
    EXTRACT(DOW FROM created_at) as day_of_week,
    COUNT(*) as post_count,
    AVG(response_time_minutes) as avg_response_time
FROM interactions
GROUP BY hour, day_of_week
ORDER BY post_count DESC;
```

**Output Schema**:
```
TemporalPattern:
  - peak_hours: [9, 14, 21]
  - peak_days: [1, 3, 5]  # Mon, Wed, Fri
  - avg_response_time: 12.5 minutes
  - posting_frequency: 4.2 posts/day
  - engagement_cycles: [{start: 9, end: 11, intensity: 0.8}]
```

### 3. extract-topic-patterns

Analyze topic dynamics and correlations.

```python
patterns = extract_topic_patterns(
    posts=all_posts,
    embedding_model="all-MiniLM-L6-v2",
    n_topics=20
)

# Returns:
# - topic_distribution: {topic_id: frequency}
# - topic_transitions: Markov chain P(topic_j | topic_i)
# - topic_entropy: Shannon entropy of topic usage
# - topic_clusters: Hierarchical clustering of related topics
```

### 4. skill-discovery

Identify latent skills from behavioral patterns.

```python
skills = discover_skills(
    interactions=interaction_log,
    min_frequency=5,
    coherence_threshold=0.7
)

# Example output:
# [
#   {skill: "category-theory-explanation", frequency: 23, coherence: 0.89},
#   {skill: "code-review-feedback", frequency: 45, coherence: 0.92},
#   {skill: "community-bridge-building", frequency: 18, coherence: 0.85}
# ]
```

### 5. derive-patterns-via-unworld

Generate patterns via derivational chaining (NEW - Langevin/Unworld path).

```python
from agent_o_rama import UnworldPatternDeriver

# Instead of train_interaction_predictor(epochs=100)
# Now also support:
deriver = UnworldPatternDeriver(
    genesis_seed=0xDEADBEEF,
    interaction_schema=schema
)

# Generate learned patterns deterministically
patterns = deriver.derive_patterns(
    depth=100,  # Derivation depth instead of epochs
    verify_gf3=True  # Verify GF(3) conservation
)

# Cost comparison
cost_analysis = {
    "temporal_training": {
        "time": "5-10 minutes",
        "cost": "high (compute)",
        "determinism": "stochastic"
    },
    "derivational_generation": {
        "time": "5-10 seconds",
        "cost": "low",
        "determinism": "deterministic ✓"
    }
}
```

### 6. verify-equivalence-via-bisimulation

Prove temporal and derivational patterns are behaviorally equivalent.

```python
from bisimulation_game import BisimulationGame

# Verify that temporal and derivational patterns are equivalent
are_equivalent = BisimulationGame(
    system1=learned_patterns,      # from temporal training
    system2=derived_patterns,      # from unworld derivation
    seed=0xDEADBEEF
).play()

if are_equivalent:
    print("✓ Patterns are behaviorally equivalent")
    print("✓ Can safely switch from temporal to derivational")
```

### 7. validate-held-out

Cross-validate models on held-out test sets.

```python
validation = validate_held_out(
    predictor=trained_model,
    test_set=held_out_interactions,
    metrics=["accuracy", "perplexity", "topic_match", "style_match"]
)

# Target: >80% accuracy on next-topic prediction
assert validation.accuracy > 0.80
```

## DuckDB Integration

### Training Data Schema

```sql
CREATE TABLE interaction_sequences (
    sequence_id VARCHAR PRIMARY KEY,
    user_id VARCHAR,
    interactions JSON,  -- Array of interaction objects
    created_at TIMESTAMP,
    topic_labels VARCHAR[],
    sentiment_arc FLOAT[]
);

CREATE TABLE learned_patterns (
    pattern_id VARCHAR PRIMARY KEY,
    pattern_type VARCHAR,  -- 'temporal', 'topic', 'network', 'skill'
    pattern_data JSON,
    confidence FLOAT,
    learned_at TIMESTAMP,
    seed BIGINT  -- SPI seed for reproducibility
);
```

## GF(3) Triad Integration

Agent-o-rama forms triads with:

| Trit | Skill | Role |
|------|-------|------|
| -1 | self-validation-loop | Validates learned patterns |
| 0 | cognitive-surrogate | Consumes patterns for prediction |
| +1 | **agent-o-rama** | Generates learned patterns |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Configuration

```yaml
# agent-o-rama.yaml
training:
  learning_rate: 0.01
  epochs: 100
  batch_size: 32
  early_stopping: true
  patience: 10

patterns:
  temporal:
    granularity: hour
    lookback_days: 90
  topic:
    n_topics: 20
    min_topic_size: 5
  skill:
    min_frequency: 5
    coherence_threshold: 0.7

reproducibility:
  seed: 0xf061ebbc2ca74d78
  deterministic: true
```

## Example Workflow

```bash
# 1. Extract patterns from interaction data
just agent-train interactions.duckdb --epochs 100

# 2. Discover skills
just agent-discover-skills --min-freq 5

# 3. Validate on held-out set
just agent-validate --test-split 0.2

# 4. Export patterns for cognitive-surrogate
just agent-export patterns.json
```

## Related Skills

- `cognitive-surrogate` (Layer 6) - Consumes learned patterns
- `entropy-sequencer` (Layer 5) - Arranges training data
- `acsets` (Layer 3) - Structured pattern storage
- `gay-mcp` - Deterministic seeding via SPI



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
agent-o-rama (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch4: Pattern Matching
- Ch6: Layering

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

## Forward Reference

- unified-reafference (multi-agent session patterns)