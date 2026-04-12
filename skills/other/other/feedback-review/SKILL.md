---
name: feedback-review
description: "Aggregate feedback signals across all active loops. Reports health, trajectory, overdue checks, regression warnings, and Goodhart's Law violations."
---

# Feedback Review

Single-place health check across all Mycelium feedback loops. Run periodically or when something feels off.

## When to Use
- Weekly as part of regular practice
- When metrics aren't moving despite active work
- When the team feels busy but unproductive
- After a failed launch or unexpected regression
- When `/diamond-assess` shows stale diamonds

## Workflow

### 1. Check Loop 1 (Immediate) Health
- How many reflexion iterations are averaging? (1 = healthy, 3 = struggling)
- Any corrections logged this session? Are they new patterns or repeats?
- Is the preflight gate catching issues, or are issues slipping through?

### 2. Check Loop 2 (Incremental) Health
- Are diamond phases progressing? Or stalled?
- Are ICE confidence scores increasing with each GIST step?
- Is the delivery journal being updated? (Empty = no incremental learning)
- Are retrospectives happening after delivery increments?

### 3. Check Loop 3 (Strategic) Health
Read canvas trend data and check cadence:
- **BVSSH**: Last assessed when? Any dimension declining? (Check `bvssh-health.yml` trend fields)
- **North Star**: Are input metrics moving? Flat for 2+ months = strategic concern.
- **Delivery metrics**: Any metric degrading? Check the product-type-appropriate canvas: `dora-metrics.yml` (software), `content-metrics.yml` (content), `ai-tool-metrics.yml` (ai_tool), `service-metrics.yml` (service).
- **Wardley Map**: Last refreshed when? Stale > 3 months = risk of strategic blind spot.
- **Corrections themes**: Are the same types of mistakes recurring? (Pattern = graduate to guardrail)

### 4. Check Loop 4 (Transformative) Health
- When was the last eval benchmark run?
- Are eval pass rates improving, stable, or declining?
- Are any skills consistently underutilized? (Check decision-log.md for skill invocation patterns)
- Has the escape hatch been used? How often? (Frequent = process too heavy for context)

### 5. Regression Warning Check
From `.claude/engine/feedback-loops.md`, check active triggers:
- DORA declined 2+ times? -> Warn about L4/L3 regression
- Confidence stagnant 3+ steps? -> Warn about opportunity reframing
- Same correction 3+ times? -> Suggest guardrail graduation
- BVSSH Safer declining while Sooner improving? -> Flag the BVSSH anti-pattern

### 6. Goodhart's Law Check
For each active metric, verify its counter-metric:
- Deployment frequency up BUT change failure rate also up? -> False improvement
- Confidence score up BUT evidence type hasn't changed? -> Inflation
- Test coverage up BUT defect leakage unchanged? -> Meaningless tests
- Diamond velocity up BUT regression rate also up? -> Rushing through gates
- Evidence source count up BUT external evidence ratio declining? -> Internal echo chamber risk. Suggest `/handoff` to plan external conversations.

## Output Format

```
## Feedback Loop Health Report

### Loop 1 (Immediate): [Healthy / Warning / Struggling]
- Reflexion avg iterations: [N]
- New corrections this period: [N] ([N] repeats of existing patterns)
- Secret detection blocks: [N]

### Loop 2 (Incremental): [Healthy / Warning / Struggling]
- Diamonds progressed this period: [N]
- Confidence trajectory: [improving / flat / declining]
- Delivery journal entries: [N]
- Retrospectives completed: [N]

### Loop 3 (Strategic): [Healthy / Warning / Overdue]
- BVSSH last checked: [date] ([days ago])
  Trajectory: B[trend] V[trend] S[trend] S[trend] H[trend]
- North Star: [current] -> [target] ([trajectory])
- DORA: [classification] ([trajectory])
- Wardley map last refreshed: [date]

### Loop 4 (Transformative): [Active / Dormant]
- Last eval run: [date]
- Pass rate trend: [improving / stable / declining]
- Escape hatch uses: [N] in last quarter

### Regression Warnings
- [Any active triggers from feedback-loops.md]

### Goodhart's Law Check
- [Any metric/counter-metric divergences]

### Recommended Actions
1. [Most urgent feedback loop action]
2. [Second priority]
3. [Third priority]
```

## Canvas Output
Update `canvas/bvssh-health.yml` trend fields if BVSSH was assessed.
Update `canvas/dora-metrics.yml` trend fields if DORA was assessed.
Log review in `.claude/memory/product-journal.md`.

## Theory Citations
- Kim: Three Ways of DevOps (Second Way: amplify feedback)
- Argyris: Single/double/triple-loop learning
- Meadows: Leverage points in systems
- Goodhart: When a measure becomes a target
- Forsgren: DORA metrics as feedback signals
- Smart: BVSSH as holistic health feedback
