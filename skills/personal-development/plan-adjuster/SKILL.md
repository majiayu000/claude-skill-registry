---
name: plan-adjuster
description: Recomputes upcoming workouts based on recent runs and user feedback. Use when recent performance deviates from plan, user provides negative feedback, or recovery signals indicate adjustment needed with deterministic safety caps.
metadata:
  short-description: Adaptive adjustment of future sessions with change logs and recovery tips.
  agent: cursor
---

## When Cursor should use this skill
- Nightly job or immediately after a run is logged
- When the user reports fatigue/injury or requests easier/harder weeks
- When performance data indicates plan adjustment is needed
- When implementing adaptive training features or debugging adjustment logic

## Invocation guidance
1. Load `Plan`, `Workout`, `TrainingHistory`, and `RecentRunTelemetry[]`.
2. Apply deterministic ceilings from `v0/lib/planAdaptationEngine.ts` and `v0/lib/plan-complexity-engine.ts` before calling the model.
3. Return `Adjustment[]`, optional `RecoveryRecommendation`, and `confidence`.
4. Only adjust future workouts - never modify completed runs.
5. Maintain weekly volume within safe limits (±20-30%).

## Input schema (JSON)
```ts
{
  "profile": UserProfile,
  "currentPlan": Plan,
  "trainingHistory": TrainingHistory,
  "feedback": { "rpeTrend"?: number, "soreness"?: string, "sleepQuality"?: string }
}
```

## Output schema (JSON)
```ts
{
  "appliedAt": string,
  "updates": Adjustment[],
  "recovery"?: RecoveryRecommendation,
  "confidence": "low" | "medium" | "high",
  "safetyFlags"?: SafetyFlag[]
}
```

## Integration points
- **API**: `v0/app/api/plan/adjust` (to add), or chat-triggered adjustments
- **Logic**: 
  - `v0/lib/planAdjustmentService.ts` - Adjustment orchestration
  - `v0/lib/planAdaptationEngine.ts` - Adaptive algorithms
  - `v0/lib/plan-complexity-engine.ts` - Safety caps
- **UI**: Plan/Today screens (badge adjusted sessions)
- **Notifications**: `v0/lib/email.ts` - Email user about significant adjustments
- **Database**: Update `workouts` table, log adjustments in `plan_adjustments` (if added)

## Safety & guardrails
- Never rewrite completed history; adjust only future sessions.
- If fatigue/injury signals present, lower intensity/volume and consider rest-day insertion.
- Emit `SafetyFlag` on unsafe load proposals; clamp to deterministic caps.
- Maintain at least one rest day per week.
- If multiple negative signals, reduce load by at least one level.
- Hard stop on pain/injury mentions - recommend rest and professional consultation.

## Adjustment types and triggers

### Intensity adjustments
- **Trigger**: High RPE trend (>7 for easy runs), poor sleep, soreness
- **Action**: Reduce pace target by 15-30 seconds/km, lower HR zone
- **Example**: Tempo → Easy, Intervals → Tempo

### Volume adjustments
- **Trigger**: Missed runs, fatigue, low consistency
- **Action**: Reduce duration by 10-30%, maintain intensity
- **Example**: 60min easy → 45min easy

### Session swaps
- **Trigger**: Schedule conflicts, weather, preferences
- **Action**: Reschedule within same week, maintain weekly pattern
- **Example**: Tuesday intervals ↔ Thursday tempo

### Rest day insertion
- **Trigger**: Multiple fatigue signals, injury risk, poor recovery
- **Action**: Replace easy run with rest or cross-training
- **Example**: Easy run → Rest day

### Cross-training substitution
- **Trigger**: Soreness, minor injury, surface limitations
- **Action**: Replace easy run with cycling/swimming/walking
- **Example**: Easy run → 45min cycling

## Telemetry
- Emit `ai_skill_invoked` and `ai_adjustment_applied` with:
  - `adjustments_count`
  - `confidence`
  - `safety_flags`
  - `adjustment_types` (array of change types)
  - `user_id` (hashed)
  - `latency_ms`

## Common edge cases
- **No adjustment needed**: Return empty adjustments array, confirm plan is on track
- **Conflicting signals**: Prioritize safety, default to more conservative option
- **Major deviation**: Consider full plan regeneration instead of adjustments
- **Peak training**: Allow slightly higher load if race is imminent and recovery is adequate
- **Taper period**: Protect taper, only minor adjustments allowed

## Testing considerations
- Test with various feedback combinations (RPE, soreness, sleep)
- Verify load caps are enforced
- Test that completed runs are never modified
- Validate adjustment rationale clarity
- Test with missing data (partial feedback)
- Verify SafetyFlag emission for risky adjustments
