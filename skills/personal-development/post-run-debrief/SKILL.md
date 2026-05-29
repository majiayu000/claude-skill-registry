---
name: post-run-debrief
description: Converts run telemetry and user notes into structured reflections with confidence scores. Use after runs to capture qualitative feedback and generate next-step guidance with safety checks for pain or abnormal heart rate.
metadata:
  short-description: Post-run reflection with confidence scoring and actionable guidance.
  agent: cursor
---

## When Cursor should use this skill
- Immediately after run save to prompt reflection
- When user asks for a recap or confidence check
- When analyzing run performance with qualitative feedback
- When implementing post-run feedback features or debugging run reflections

## Invocation guidance
1. Provide `RecentRunTelemetry`, derived metrics, and user notes.
2. Generate reflection bullets (3-5 concise points), confidence score (0–1), and next-step guidance linked to the plan.
3. Output must include optional `SafetyFlag[]` if pain/abnormal HR reported.
4. Confidence score represents how well the run went compared to plan/expectations.
5. Keep tone supportive and constructive, never judgmental.

## Input schema
See `references/input-schema.json`.

## Output schema
See `references/output-schema.json`.

## Confidence scoring

### High confidence (0.8-1.0)
- Completed workout as planned or better
- Good pacing and form
- Felt strong throughout
- No pain or unusual symptoms
- Ready for next session

### Medium confidence (0.5-0.8)
- Mostly completed workout with minor struggles
- Some pacing issues or form breakdown
- Felt okay but not great
- Minor discomfort but manageable
- Might need extra recovery

### Low confidence (0.0-0.5)
- Struggled significantly or cut workout short
- Major pacing issues or form breakdown
- Felt bad throughout
- Pain or concerning symptoms
- Need extra recovery or plan adjustment

## Reflection components

### Performance summary
- How did the run compare to plan?
- Key metrics (distance, pace, HR)
- Pacing consistency
- Form and efficiency

### Subjective experience
- How did it feel?
- Energy levels
- Breathing and effort
- Mental state

### Notable observations
- Conditions (weather, terrain, time of day)
- Equipment (shoes, clothes)
- External factors (sleep, nutrition, stress)
- Improvements or struggles

### Safety check
- Any pain or injury signals?
- Abnormal heart rate patterns?
- Dizziness, nausea, or other concerns?
- Form breakdown or compensation?

### Next-step guidance
- Recovery needs
- Adjustment recommendations
- Next workout preview
- Motivation or encouragement

## Integration points
- **UI**: 
  - Post-run modal (immediate feedback)
  - Chat thread insertion
  - Run detail view
- **Database**: Save alongside run insight in Dexie (`v0/lib/db.ts`)
- **API**: Served through enhanced AI coach or dedicated debrief endpoint
- **Telemetry**: Emit `ai_insight_created`

## Safety & guardrails
- If user notes include pain/dizziness → advise stopping further activity and consulting a professional.
- Keep debrief ≤140 words, supportive tone.
- Default to conservative next-step if data incomplete.
- Never dismiss pain or injury concerns.
- Emphasize rest and recovery when needed.
- Emit `SafetyFlag` for any concerning symptoms.

## Reflection patterns

### After great run (high confidence)
```
✓ Nailed the workout! Strong pacing throughout.
✓ Your form held up well - efficient and controlled.
✓ HR zones matched plan perfectly.
→ Great progress! Take it easy tomorrow before [next workout].
```

### After okay run (medium confidence)
```
✓ Completed the distance - that's a win!
~ Started a bit fast, settled into rhythm later.
~ HR slightly elevated but within acceptable range.
→ Good effort. Focus on recovery, you'll feel stronger for [next workout].
```

### After struggled run (low confidence)
```
✓ You showed up - that matters.
~ Tough conditions today (heat/fatigue/etc).
~ Pacing was challenging, cut it short wisely.
→ Rest up. Let's assess how you feel before [next workout]. Consider easier version.
```

### After run with pain
```
⚠ Pain reported - this needs attention.
~ Completed [distance] before stopping.
~ Smart to listen to your body.
→ STOP. Rest and evaluate. If pain persists, consult a professional. Your next workout can wait.
```

## Next-step guidance patterns

### After hard workout
"Solid effort! Take 48-72 hours easy. Your next tempo on [day] will build on this."

### After easy run
"Perfect recovery run. This builds your aerobic base. Ready for [next workout] on [day]."

### After long run
"Great endurance work! Rest today, light activity tomorrow. Back to running on [day]."

### After struggled workout
"Tough days happen. Extra rest if needed. We can modify [next workout] to match your recovery."

### After injury concerns
"Health first. Skip [next workout] and reassess in 2-3 days. Consult professional if pain continues."

## Telemetry
- Emit `ai_skill_invoked`, `ai_insight_created`, and `ai_safety_flag_raised` when applicable with:
  - `run_id`
  - `confidence_score`
  - `reflection_points_count`
  - `safety_flags`
  - `next_step_provided` (boolean)
  - `latency_ms`

## Common edge cases
- **First run ever**: Extra celebration and encouragement
- **Return from break**: Acknowledge restart, set realistic expectations
- **Missed workout**: Focus on completion, not comparison to plan
- **Exceeded expectations**: Celebrate but caution against overtraining
- **Equipment issues**: Note for future, suggest solutions
- **Weather impact**: Acknowledge conditions, adjust expectations

## Testing considerations
- Test with various confidence levels (high/medium/low)
- Verify reflection clarity and actionability
- Test SafetyFlag emission for pain/injury mentions
- Validate next-step guidance relevance
- Test with missing telemetry data
- Verify tone remains supportive across scenarios
