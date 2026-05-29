---
name: adherence-coach
description: Identifies missed sessions or inconsistency and proposes plan reshuffles with motivational nudges.
metadata:
  short-description: Weekly adherence check with reshuffle suggestions and supportive messaging.
---

## When Codex should use it
- Weekly digest (e.g., Sunday) or when multiple sessions are skipped.
- When the user asks for help getting back on track.

## Invocation guidance
1. Provide `Plan`, completed vs. missed workouts, and user preferences (available days, constraints).
2. Output reshuffle suggestions, prioritized focus areas, and motivational `CoachMessage`.
3. Keep volume conservative after lapses; bias toward habit re-entry.

## Input schema
See `references/input-schema.json`.

## Output schema
See `references/output-schema.json`.

## Integration points
- UI: Weekly digest card; chat prompt suggestions.
- API: `v0/app/api/plan/adherence`.
- Notifications: Email/push via `v0/lib/email.ts`.

## Safety & guardrails
- If repeated missed sessions due to pain → suggest rest and professional consult, not catch-up volume.
- Limit catch-up to 1 session per week; avoid stacking intensity.
- Emit `SafetyFlag` for risky catch-up proposals.

## Telemetry
- Emit `ai_skill_invoked`, `ai_adjustment_applied` (if reshuffle applied), and `ai_user_feedback` on user rating.
