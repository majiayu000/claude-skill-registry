---
name: agent-o-rama
description: "Layer 4 Learning and Pattern Extraction for Cognitive Surrogate Systems"
---

# agent-o-rama

> Layer 4: Learning and Pattern Extraction for Cognitive Surrogate Systems

**Version**: 1.1.0 (music-topos enhanced)
**Trit**: +1 (Generator - produces learned patterns)
**Bundle**: learning

## Overview

Agent-o-rama trains learning agents on interaction sequences to discover behavioral patterns. It extracts temporal, topic, and network patterns from raw interaction data, producing models compatible with the cognitive-surrogate skill.

## Enhanced Integration: Multi-Interpreter

### DuckDB Pattern Storage

```sql
CREATE TABLE learned_patterns (
    pattern_id VARCHAR PRIMARY KEY,
    pattern_type VARCHAR,  -- 'temporal', 'topic', 'network', 'skill'
    pattern_data JSON,
    confidence FLOAT,
    learned_at TIMESTAMP,
    seed BIGINT  -- SPI seed for reproducibility
);

-- Temporal pattern query
SELECT
    EXTRACT(HOUR FROM created_at) as hour,
    EXTRACT(DOW FROM created_at) as day_of_week,
    COUNT(*) as post_count,
    AVG(response_time_minutes) as avg_response_time
FROM interactions
GROUP BY hour, day_of_week
ORDER BY post_count DESC;
```

### Python Predictor

```python
# agent_o_rama.py
import jax
import jax.numpy as jnp
from dataclasses import dataclass

@dataclass
class InteractionPredictor:
    learning_rate: float = 0.01
    epochs: int = 100
    batch_size: int = 32
    seed: int = 0xf061ebbc2ca74d78
    
    def fit(self, db_path: str, table: str, validation_split: float = 0.2):
        """Train on DuckDB interaction sequences."""
        import duckdb
        conn = duckdb.connect(db_path)
        
        data = conn.execute(f"SELECT * FROM {table}").fetchall()
        # JAX training loop with SPI seed
        key = jax.random.PRNGKey(self.seed)
        
        for epoch in range(self.epochs):
            key, subkey = jax.random.split(key)
            # ... training logic
            
    def predict(self, history):
        """Predict next interaction given history."""
        return self.model(history)
```

### Ruby Skill Discovery

```ruby
# lib/agent_o_rama.rb
module AgentORama
  def self.discover_skills(interactions, min_frequency: 5, coherence_threshold: 0.7)
    # Group by inferred skill
    skill_candidates = interactions.group_by { |i| infer_skill(i) }
    
    skill_candidates.map do |skill_name, examples|
      frequency = examples.size
      coherence = calculate_coherence(examples)
      
      next unless frequency >= min_frequency && coherence >= coherence_threshold
      
      {
        skill: skill_name,
        frequency: frequency,
        coherence: coherence,
        exemplars: examples.first(3)
      }
    end.compact
  end
  
  def self.calculate_coherence(examples)
    # Coherence via condensed stack descent
    stack = WorldBroadcast::CondensedAnima.analytic_stack(
      examples.map { |e| e[:id].hash }
    )
    stack[:descent_data].size.to_f / examples.size
  end
end
```

### Hy Bidirectional Learning

```hy
;; From thread_relational_hyjax.hy - enhanced
(defclass ThreadBidirectionalLearner []
  "Learn thread patterns by coupling reading (analysis) with writing (synthesis)"
  
  (defn __init__ [self latent-dim]
    (setv self.latent-dim latent-dim)
    (setv self.read-patterns {})
    (setv self.write-templates {})
    (setv self.coupling-loss []))
  
  (defn encode-thread [self acset]
    "READ: ACSet → Latent representation"
    (setv features
          {:n-threads (len acset.threads)
           :n-messages (len acset.messages)
           :n-concepts (len acset.concepts)
           :n-files (len acset.files)
           :n-relations (len acset.related)
           :concept-entropy (compute-message-entropy 
                              (list (.values acset.concepts)))})
    (setv latent (jnp.array 
                   [(get features "n-threads")
                    (get features "n-messages")
                    (get features "n-concepts")
                    (get features "n-files")
                    (get features "n-relations")
                    (float (get features "concept-entropy"))]))
    (setv (get self.read-patterns "latest") features)
    latent)
  
  (defn bidirectional-loss [self acset]
    "Coupling loss: read → latent → write should reconstruct"
    (setv latent (self.encode-thread acset))
    (setv template (self.decode-thread latent))
    ;; Reconstruction error
    (setv error
          (+ (abs (- (get template "suggested-threads") (len acset.threads)))
             (abs (- (get template "suggested-messages") (len acset.messages)))))
    {:latent latent :error error}))
```

## GF(3) Triad Integration

| Trit | Skill | Role |
|------|-------|------|
| -1 | self-validation-loop | Validates learned patterns |
| 0 | cognitive-surrogate | Consumes patterns for prediction |
| +1 | **agent-o-rama** | Generates learned patterns |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Justfile Recipes

```makefile
# Train interaction predictor
agent-train db="interactions.duckdb" epochs="100":
    python3 -c "from agent_o_rama import InteractionPredictor; p = InteractionPredictor(epochs={{epochs}}); p.fit('{{db}}', 'interactions')"

# Discover skills via Ruby
agent-skills:
    ruby -I lib -r agent_o_rama -e "puts AgentORama.discover_skills(interactions).to_json"

# Hy bidirectional learning
agent-hy:
    uv run hy -c '(import lib.thread_relational_hyjax :as tra) (setv learner (tra.ThreadBidirectionalLearner 6)) (print "Learner ready")'
```

## Related Skills

- `cognitive-surrogate` (Layer 6) - Consumes learned patterns
- `entropy-sequencer` (Layer 5) - Arranges training data
- `acsets` (Layer 3) - Structured pattern storage
- `gay-mcp` - Deterministic seeding via SPI
