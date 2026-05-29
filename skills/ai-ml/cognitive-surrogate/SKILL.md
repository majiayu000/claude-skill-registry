---
name: cognitive-surrogate
description: "cognitive-surrogate skill"
version: 1.0.0
---


# Cognitive Surrogate

```yaml
name: cognitive-surrogate
description: Layer 6 Barton Cognitive Surrogate System - build, train, and validate psychological models that predict and generate authentic responses matching a subject's cognitive patterns
version: 1.0.0
trit: 0  # Ergodic/coordinator role in GF(3) triadic system
```

## bmorphism Contributions

> *"We are building cognitive infrastructure for the next trillion minds"*
> — [Plurigrid: the story thus far](https://gist.github.com/bmorphism/a400e174b9f93db299558a6986be0310)

**Active Inference Foundation**: Cognitive surrogates implement the core [Active Inference in String Diagrams](https://arxiv.org/abs/2308.00861) pattern where an agent maintains a generative model of itself and others. The surrogate IS the generative model — it predicts responses by minimizing free energy between expected and observed behavior.

**Self-Model as Markov Blanket**: The surrogate defines the statistical boundary (Markov blanket) between self and world. The model's internal states predict the subject's behavior while remaining conditionally independent of external states given sensory input.

**Reafference in Surrogates**: When the surrogate predicts a response that matches actual behavior, this is **reafference** — self-caused sensation that confirms identity. Mismatches are **exafference** — signals that the model needs updating.

**Autopoietic Surrogates**: Following Maturana & Varela's autopoiesis concept, the surrogate is a self-maintaining system that reproduces its own patterns. It embodies bmorphism's **autopoietic ergodicity** — self-sustaining systems that explore all accessible cognitive states.

## Overview

The Cognitive Surrogate skill enables construction of high-fidelity psychological models from interaction patterns. It extracts values, predicts intellectual trajectories, and generates authentic responses that preserve the subject's voice with >90% fidelity.

**Core Principle**: A surrogate is not an imitation but a *derivational continuation* - the model learns the generative grammar of cognition, not surface patterns.

**NEW (Langevin/Gibbs Integration)**: Predictions now use Gibbs distribution from Langevin analysis. Confidence scores reflect mixing time and temperature parameters.

## Key Capabilities

### 1. build-psychological-profile

Extract structured psychological profile from interaction corpus:

```python
profile = build_psychological_profile(
    corpus=[threads, emails, writings],
    dimensions=[
        "values",           # Core beliefs, ethical framework
        "interests",        # Topic affinities, curiosity patterns
        "communication",    # Tone, formality, humor markers
        "reasoning",        # Deductive vs intuitive, uncertainty handling
        "social",           # Collaboration style, conflict patterns
    ],
    seed=gay_seed          # Deterministic via gay-mcp
)
```

**Output ACSets Schema**:
```julia
@present SchProfile(FreeSchema) begin
    Value::Ob; Interest::Ob; Pattern::Ob
    name::Attr(Value, String)
    weight::Attr(Value, Float64)
    topic::Attr(Interest, String)
    frequency::Attr(Interest, Int)
    exemplar::Attr(Pattern, String)
end
```

### 2. train-predictor

Train next-topic and next-response predictors:

```python
predictor = train_predictor(
    profile=profile,
    corpus=corpus,
    model_type="markov_transformer",  # or "hmm", "lstm", "gpt_finetune"
    context_window=8,                  # conversation turns
    validation_split=0.15
)

# Predict likely next topics given conversation state
next_topics = predictor.predict_topics(
    context=current_thread,
    top_k=5,
    temperature=0.7
)
```

### 3. validate-fidelity

Measure surrogate fidelity against held-out data:

```python
fidelity = validate_fidelity(
    surrogate=predictor,
    test_corpus=held_out_threads,
    metrics=[
        "topic_prediction_accuracy",   # Target: >0.85
        "response_semantic_sim",       # Target: >0.90
        "style_consistency",           # Target: >0.88
        "value_alignment",             # Target: >0.92
    ],
    threshold=0.90  # Overall fidelity threshold
)

assert fidelity.overall >= 0.90, f"Fidelity {fidelity.overall} below threshold"
```

**Fidelity Report**:
```
┌─────────────────────────┬────────┬────────┐
│ Metric                  │ Score  │ Target │
├─────────────────────────┼────────┼────────┤
│ topic_prediction        │ 0.87   │ 0.85   │
│ semantic_similarity     │ 0.91   │ 0.90   │
│ style_consistency       │ 0.89   │ 0.88   │
│ value_alignment         │ 0.94   │ 0.92   │
├─────────────────────────┼────────┼────────┤
│ OVERALL                 │ 0.9025 │ 0.90   │
└─────────────────────────┴────────┴────────┘
```

### 4. generate-authentic-reply

Generate text matching subject's voice:

```python
reply = generate_authentic_reply(
    surrogate=predictor,
    context=conversation_history,
    prompt=incoming_message,
    constraints={
        "max_tokens": 500,
        "preserve_uncertainty": True,  # Don't overclaim knowledge
        "style_lock": True,            # Enforce style consistency
    },
    gay_seed=thread_seed  # Reproducible generation
)

# Reply includes confidence and divergence markers
print(reply.text)
print(f"Confidence: {reply.confidence}")
print(f"Style divergence: {reply.style_delta}")
```

### 5. predict-via-gibbs-distribution (NEW)

Use Gibbs distribution from Langevin dynamics for predictions:

```python
# Instead of generic pattern matching
# Use p(pattern | θ) ∝ exp(-L(θ)/T) from Langevin
prediction = gibbs_based_prediction(
    state=current_state,
    temperature=0.01,  # From Langevin analysis
    loss_fn=pattern_energy,
    mixing_time=500    # Estimated convergence time
)

# Adaptive confidence based on equilibration
confidence = estimate_equilibrium(
    steps_so_far=n,
    mixing_time=tau_mix,
    temperature=T
)

# Returns:
# - prediction: Most likely next state
# - confidence: P(equilibrium reached)
# - temperature_influence: How much T affected prediction
```

### 6. project-trajectory

Predict intellectual/professional trajectory:

```python
trajectory = project_trajectory(
    profile=profile,
    horizon="6_months",
    dimensions=[
        "research_interests",
        "skill_acquisition", 
        "collaboration_patterns",
        "publication_topics",
    ],
    monte_carlo_samples=1000,
    seed=gay_seed
)

# Returns probability distributions over future states
for dim, distribution in trajectory.items():
    print(f"{dim}: {distribution.mode} (p={distribution.confidence:.2f})")
```

## Integration: gay-mcp

All stochastic operations use gay-mcp deterministic seeding:

```python
from gay_mcp import GaySeed, derive_color

# Create reproducible surrogate session
session_seed = GaySeed.from_thread(thread_id)
profile_color = derive_color(session_seed, "profile")  # trit=0
training_color = derive_color(session_seed, "train")   # trit=1
validation_color = derive_color(session_seed, "valid") # trit=2

# GF(3) conservation: 0 + 1 + 2 ≡ 0 (mod 3)
assert (profile_color.trit + training_color.trit + validation_color.trit) % 3 == 0
```

## Integration: acsets

Profile data stored as attributed C-sets:

```julia
using ACSets

# Define cognitive schema
@acset_type CognitiveProfile(SchProfile)

# Populate from extraction
profile = CognitiveProfile()
add_part!(profile, :Value, name="intellectual_honesty", weight=0.95)
add_part!(profile, :Interest, topic="category_theory", frequency=47)
add_part!(profile, :Pattern, exemplar="tends to use analogies from music")

# Query patterns
high_values = incident(profile, x -> x.weight > 0.8, :Value)
```

## GF(3) Trit Assignment

| Component | Trit | Role |
|-----------|------|------|
| cognitive-surrogate | 0 | Coordinator/ergodic - orchestrates profile building |
| gay-mcp | 1 | Generator - provides deterministic randomness |
| acsets | 2 | Storage - structured data persistence |

**Conservation**: `0 + 1 + 2 ≡ 0 (mod 3)` — closed triadic system.

## Usage Example

```python
# Complete surrogate construction workflow
from cognitive_surrogate import (
    build_psychological_profile,
    train_predictor,
    validate_fidelity,
    generate_authentic_reply,
    project_trajectory
)
from gay_mcp import GaySeed

# Initialize with deterministic seed
seed = GaySeed.from_string("barton_surrogate_v1")

# 1. Build profile from corpus
profile = build_psychological_profile(
    corpus=load_interaction_corpus("barton_threads/"),
    seed=seed
)

# 2. Train predictor
predictor = train_predictor(profile, model_type="markov_transformer")

# 3. Validate fidelity
fidelity = validate_fidelity(predictor, test_corpus, threshold=0.90)
print(f"Fidelity: {fidelity.overall:.2%}")

# 4. Generate replies
reply = generate_authentic_reply(
    predictor,
    context=current_conversation,
    prompt="What do you think about applying category theory to social systems?"
)

# 5. Project trajectory
trajectory = project_trajectory(profile, horizon="1_year")
print(f"Predicted focus: {trajectory['research_interests'].mode}")
```

## Ethical Considerations

1. **Consent**: Only build surrogates with explicit subject consent
2. **Disclosure**: Always disclose when surrogate-generated content is used
3. **Boundaries**: Surrogates should refuse to act on high-stakes decisions
4. **Audit Trail**: All generations logged with gay-mcp seeds for reproducibility
5. **Kill Switch**: Subject can invalidate surrogate at any time

## Files

```
skills/cognitive-surrogate/
├── SKILL.md                    # This file
├── src/
│   ├── profile_builder.py      # Psychological extraction
│   ├── predictor.py            # Training and prediction
│   ├── fidelity.py             # Validation metrics
│   ├── generator.py            # Authentic reply generation
│   └── trajectory.py           # Future projection
├── schemas/
│   └── cognitive_acset.jl      # ACSets schema definitions
└── tests/
    └── test_fidelity.py        # >90% threshold tests
```

## See Also

- [gay-mcp](../gay-mcp/SKILL.md) - Deterministic seeding
- [acsets](../acsets/SKILL.md) - Structured data storage
- [bisimulation-game](../bisimulation-game/SKILL.md) - Surrogate equivalence testing



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

## Forward Reference

- unified-reafference (cross-agent psychological modeling)