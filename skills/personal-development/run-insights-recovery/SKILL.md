---
name: run-insights-recovery
description: Analyzes completed runs to provide effort assessment, recovery recommendations, and next-session guidance. Use immediately after user saves a run, asks "how did I do?", or requests recovery advice.
metadata:
  short-description: Post-run insights with effort assessment, recovery tips, and safety flags.
---

## When Claude should use this skill
- Immediately after a run is saved
- When the user asks "how did I do?" or "what should I do next?"
- When user requests recovery advice or post-run analysis

## Invocation guidance
1. Provide `RecentRunTelemetry` plus derived metrics (pace stability, splits) and upcoming workouts.
2. Map effort to easy/moderate/hard and generate concise bullets.
3. Return `Insight` with `RecoveryRecommendation` and optional `nextSessionNudge`.

## Input schema (JSON)
```ts
{
  "run": RecentRunTelemetry,
  "derivedMetrics": { "paceStability": string, "cadenceNote"?: string, "hrNote"?: string },
  "upcomingWorkouts": Workout[],
  "userFeedback"?: { "rpe"?: number, "soreness"?: string }
}
```

## Output schema (JSON)
```ts
Insight
```

## Integration points
- API/hooks: Post-run pipeline in `v0/lib/run-recording.ts` and chat surface in `v0/lib/enhanced-ai-coach.ts`.
- UI: Today screen banners and run detail modal.
- Storage: Save alongside run in Dexie via `v0/lib/db.ts`.

## Safety & guardrails
- If HR missing, default to pace/RPE and add `SafetyFlag` with `missing_data`.
- If user reports pain/dizziness, advise stopping and consulting a professional; downgrade next session.
- Keep guidance ≤120 words; no medical diagnosis.

## Telemetry
- Emit `ai_skill_invoked` and `ai_insight_created` with `run_id`, `effort`, `safety_flags`.
