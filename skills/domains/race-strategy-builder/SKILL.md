---
name: race-strategy-builder
description: Generates race-day pacing and fueling strategies with contingency plans. Use when user has an upcoming race, asks for race preparation advice, or wants a printable race-day plan with segment pacing and fueling schedule.
metadata:
  short-description: Race-day pacing, fueling, and contingency plan generator.
---

## When Claude should use this skill
- When the user sets up a race event or asks for race pacing guidance
- Prior to race week to deliver printable/shareable strategy
- When user requests race preparation or race-day tactics

## Invocation guidance
1. Provide `UserProfile`, `TrainingHistory`, target race distance/date, course notes (elevation, weather).
2. Produce pacing plan by segment, fueling schedule, and contingencies (heat, hills).
3. Keep recommendations conservative if recent load is low or injury flags exist.

## Input schema
See `references/input-schema.json`.

## Output schema
See `references/output-schema.json`.

## Integration points
- UI: Race setup flow and shareable race card.
- API: `v0/app/api/race/strategy` (new).
- Export: Optionally generate text for notes and chat share via `v0/lib/enhanced-ai-coach.ts`.

## Safety & guardrails
- No medical advice; if user reports pain/injury, advise deferring race or adjusting pace drastically.
- Clamp pacing to safe ranges based on recent easy pace; avoid aggressive negative splits for beginners.
- Emit `SafetyFlag` when hydration/fueling cannot be recommended due to missing data.

## Telemetry
- Emit `ai_skill_invoked` and `ai_plan_generated` with `race_distance`, `fueling_steps`, `safety_flags`.
