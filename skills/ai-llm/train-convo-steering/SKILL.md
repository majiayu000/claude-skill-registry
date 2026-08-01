---
name: train-convo-steering
description: Voice-first runtime steering + nightly deep analysis to learn per-user
  conversation steering priors.
---

---
name: train-convo-steering
description: Voice-first runtime steering + nightly deep analysis to learn per-user conversation priors.
triggers:
  - train convo steering
  - runtime steering step
  - train steering nightly

provides:
  - train-convo-steering
composes: [, task-monitor]
---

# train-convo-steering (Skill v2)

Voice-first **runtime steering** + nightly **deep analysis** to learn per-user conversation steering priors.

This skill is designed for:

- **Live voice**: per-turn inference must be fast and bounded (preset selection, not multi-candidate judging).
- **Nightly deep learning**: optional DeepSeek V3 (TEE) judge calls to improve labels and update per-user priors.

## Concepts

### Collaboration State

A compact state bucket per turn (`tempo`, `trust`, `alignment`, `affect`, `control`) mapped to `{low, mid, high}`.

### Steering Presets

Configuration of response knobs (length, questions, initiative, certainty, grounding) and voice prosody.

- `fast_proceed`
- `clarify_once`
- `trust_repair`
- `deep_dive`
- `exec_summary_plus_steps`
- `socratic`

### Priors

Per-user policy map `state key -> best preset` learned from reinforcement signals (user feedback, latency, DeepSeek judge).

## Commands

### Runtime (voice-first)

```bash
./run.sh runtime-step \\
  --user-id <USER_ID> \\
  --session-id <SESSION_ID> \\
  --channel <text|voice> \\
  --user-text "..."
```

Emits JSON with the selected preset and decision details.

### Nightly

```bash
./run.sh nightly \\
  --logs ./_out/live_logs.jsonl \\
  --out ./_out
```

Processes logs, runs DeepSeek judge (if configured), and updates priors.

## Memory Integration (memory_integration.py)

Cross-session memory persistence via `common.memory_client` with taxonomy bridge tagging.
Priors MUST persist to memory or they are useless across sessions.

### Pre-hook: `recall_user_priors(user_id, k=10)`
Recalls per-user conversation priors from memory for cross-session persistence of learned preferences.

### Post-hook: `learn_conversation_prior(user_id, prior_type, value, confidence, context)`
Learns steering decisions with confidence >= 0.6 during runtime-step.

### Post-hook: `learn_nightly_summary(user_id, global_best_preset, training_rows, ...)`
Learns nightly training results including state policies with confidence >= 0.5.

### Bridge Keywords
| Bridge | Keywords |
|--------|----------|
| Precision | preference, explicit, specific, configured |
| Resilience | consistent, stable, reliable, proven |
| Fragility | conflicting, unclear, ambiguous, volatile |
| Loyalty | trust, rapport, relationship, familiar |
| Stealth | implicit, inferred, unspoken, behavioral |

Tags: `["convo_steering", user_id] + bridges`

## Configuration

Set environment variables in `.env` (or project root):

- `DEEPSEEK_API_BASE`: Chutes API or gateway URL.
- `DEEPSEEK_API_KEY`: API Key.
- `DEEPSEEK_MODEL`: Model name (default `deepseek-v3`).
- `DEEPSEEK_JUDGE_ENABLED`: Set to `1` or `true` to enable.
