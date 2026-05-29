---
name: workout-explainer
description: Translates planned workouts into execution cues, purpose explanations, and common mistakes to avoid. Use before workouts when user asks "what should I do?" or "how do I run this session?" with beginner-friendly guidance.
metadata:
  short-description: Explains workouts with cues, intent, and safe substitutions.
---

## When Claude should use this skill
- When the user opens a workout detail modal or asks "how do I do this workout?"
- During chat if the user needs clarifications or substitutions
- When user wants to understand workout purpose or execution details

## Invocation guidance
1. Provide the `Workout` object and user capability context (experience, recent runs).
2. Return execution cues, purpose, common mistakes, and two substitutions.
3. Keep guidance concise (<120 words) and beginner-friendly when experience is low.

## Input schema
See `references/input-schema.json`.

## Output schema
See `references/output-schema.json`.

## Integration points
- UI: Workout detail modal and plan screen tooltips.
- Chat: Served through `v0/app/api/chat/route.ts` with `workout-explainer` intent.

## Safety & guardrails
- If workout intensity mismatches user level, propose easier substitution and emit `SafetyFlag`.
- No medical advice; advise stopping on pain/dizziness.

## Telemetry
- Emit `ai_skill_invoked` with `workout_type`, `experience`, `safety_flags`.
