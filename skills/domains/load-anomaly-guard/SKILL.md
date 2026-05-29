---
name: load-anomaly-guard
description: Detects unsafe training load spikes (>20-30% week-over-week) and emits safety flags. Use in nightly background jobs or when reviewing weekly training volume with conservative adjustment recommendations.
metadata:
  short-description: Background load monitor that flags spikes and proposes protective changes.
---

## When Claude should use this skill
- Nightly background check on training data
- Immediately after a high-intensity or long run is logged
- When analyzing weekly training load patterns for safety issues

## Invocation guidance
1. Provide recent `TrainingHistory`, planned `Plan` window, and any injury flags.
2. Compute week-over-week changes and monotony; flag spikes > deterministic caps.
3. Suggest adjustments (rest/swaps) and emit `SafetyFlag[]`.

## Input schema
See `references/input-schema.json`.

## Output schema
See `references/output-schema.json`.

## Integration points
- Background job: nightly cron.
- API: `v0/app/api/plan/load-guard` (new) returning flags + suggested adjustments.
- UI: Badge on Plan/Today screens; push/email via `v0/lib/email.ts`.

## Safety & guardrails
- If spike >20–30% week-over-week, emit `load_spike` and recommend rest or reduced volume.
- If injury signals present, bias toward `rest-day` adjustments.
- No medical diagnosis; advise professional consult on repeated spikes or pain.

## Telemetry
- Emit `ai_skill_invoked`, `ai_safety_flag_raised`, and optionally `ai_adjustment_applied` when suggestions are auto-applied.
