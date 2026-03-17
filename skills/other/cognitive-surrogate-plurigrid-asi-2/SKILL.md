---
name: cognitive-surrogate
description: "Layer 6 Barton Cognitive Surrogate - build, train, validate psychological models with >90% fidelity"
---

# cognitive-surrogate

> Layer 6: Build, Train, and Validate Psychological Models

**Version**: 1.1.0 (music-topos enhanced)
**Trit**: 0 (Ergodic - coordinates surrogate building)
**Bundle**: learning

## Overview

The Cognitive Surrogate skill enables construction of high-fidelity psychological models from interaction patterns. It extracts values, predicts intellectual trajectories, and generates authentic responses that preserve the subject's voice with >90% fidelity.

**Core Principle**: A surrogate is not an imitation but a *derivational continuation* - the model learns the generative grammar of cognition, not surface patterns.

## Enhanced Integration: Multi-Interpreter

### ACSet Schema (Julia)

```julia
using ACSets, Catlab

@present SchProfile(FreeSchema) begin
    Value::Ob
    Interest::Ob
    Pattern::Ob
    
    name::Attr(Value, String)
    weight::Attr(Value, Float64)
    topic::Attr(Interest, String)
    frequency::Attr(Interest, Int)
    exemplar::Attr(Pattern, String)
end

@acset_type CognitiveProfile(SchProfile)
```

### Python Profile Builder

```python
# cognitive_surrogate.py
from dataclasses import dataclass
from typing import List, Dict
import duckdb

@dataclass
class CognitiveProfile:
    values: Dict[str, float]
    interests: Dict[str, int]
    patterns: List[str]
    
def build_psychological_profile(corpus_path: str, seed: int = 0x42D):
    """Extract structured psychological profile from interaction corpus."""
    conn = duckdb.connect(corpus_path)
    
    # Extract values from sentiment patterns
    values = conn.execute("""
        SELECT topic, AVG(sentiment) as weight
        FROM interactions
        GROUP BY topic
        HAVING COUNT(*) > 5
    """).fetchall()
    
    # Extract interests from frequency
    interests = conn.execute("""
        SELECT topic, COUNT(*) as frequency
        FROM interactions
        GROUP BY topic
        ORDER BY frequency DESC
        LIMIT 20
    """).fetchall()
    
    return CognitiveProfile(
        values={v[0]: v[1] for v in values},
        interests={i[0]: i[1] for i in interests},
        patterns=extract_patterns(conn)
    )
```

### Ruby Condensed Integration

```ruby
# Integration with CondensedAnima for sheaf-based profiles
module CognitiveSurrogate
  def self.build_profile(interactions)
    # Use condensed mathematics for profile structure
    stack = WorldBroadcast::CondensedAnima.analytic_stack(
      interactions.map { |i| i[:id] }
    )
    
    # 6-functor for profile transformations
    {
      profile: stack,
      values: extract_values(interactions),
      fidelity_target: 0.90,
      cellular_sheaf: WorldBroadcast::CondensedAnima.to_cellular_sheaf(stack)
    }
  end
  
  def self.validate_fidelity(surrogate, test_corpus, threshold: 0.90)
    predictions = test_corpus.map { |t| surrogate.predict(t) }
    accuracy = predictions.count(&:correct?) / predictions.size.to_f
    
    {
      topic_prediction: accuracy,
      overall: accuracy,
      passed: accuracy >= threshold
    }
  end
end
```

### Hy Pattern Extraction

```hy
;; cognitive_patterns.hy
(defn extract-behavioral-patterns [interactions]
  "Extract patterns using HyJAX analysis"
  (let [analyzer (tra.ThreadRelationalAnalyzer)]
    ;; Ingest interactions
    (for [i interactions]
      (analyzer.ingest-thread 
        (get i "id") 
        (get i "title")
        (get i "messages" [])))
    
    ;; Run entropy-maximized analysis
    (analyzer.analyze)))
```

## Fidelity Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| topic_prediction | >0.85 | Next topic accuracy |
| semantic_similarity | >0.90 | Response embedding match |
| style_consistency | >0.88 | Voice preservation |
| value_alignment | >0.92 | Ethical framework match |
| **OVERALL** | >0.90 | Weighted average |

## GF(3) Triad Integration

| Trit | Skill | Role |
|------|-------|------|
| -1 | self-validation-loop | Validates surrogate fidelity |
| 0 | **cognitive-surrogate** | Coordinates profile building |
| +1 | agent-o-rama | Generates learned patterns |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## Ethical Considerations

1. **Consent**: Only build surrogates with explicit subject consent
2. **Disclosure**: Always disclose when surrogate-generated content is used
3. **Boundaries**: Surrogates should refuse to act on high-stakes decisions
4. **Audit Trail**: All generations logged with gay-mcp seeds for reproducibility
5. **Kill Switch**: Subject can invalidate surrogate at any time

## Justfile Recipes

```makefile
# Build profile from DuckDB corpus
surrogate-build db="interactions.duckdb":
    python3 -c "from cognitive_surrogate import build_psychological_profile; print(build_psychological_profile('{{db}}'))"

# Validate fidelity
surrogate-validate threshold="0.90":
    ruby -I lib -r cognitive_surrogate -e "CognitiveSurrogate.validate_fidelity(surrogate, test, threshold: {{threshold}})"

# Run Hy pattern extraction
surrogate-hy:
    uv run hy -c "(import cognitive_patterns) (extract-behavioral-patterns interactions)"
```

## Related Skills

- `agent-o-rama` - Pattern learning
- `entropy-sequencer` - Optimal training order
- `gay-mcp` - Deterministic seeding
- `condensed-analytic-stacks` - Sheaf-based profiles
- `bisimulation-game` - Surrogate equivalence testing
