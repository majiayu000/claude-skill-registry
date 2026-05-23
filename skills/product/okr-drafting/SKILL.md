---
name: definition.okr_drafting
phase: definition
roles:
  - Product Manager
  - Product Director
description: Draft outcome-oriented OKRs with leading indicators and initiatives tied to the product strategy.
variables:
  required:
    - name: timeframe
      description: Planning horizon such as Q3 FY25.
    - name: strategic_theme
      description: Strategic theme or focus area guiding the OKRs.
  optional:
    - name: baseline_metrics
      description: Key baseline metrics informing targets.
    - name: risks
      description: Known risks that could impact OKR success.
outputs:
  - Objective statements emphasizing customer and business outcomes.
  - Key results with baseline, target, and measurement plan.
  - Initiative ideas aligned to each key result.
---

# Purpose
Accelerate quarterly planning by supplying a high-quality OKR draft that balances ambition with feasibility and instrumentation.

# Pre-run Checklist
- ✅ Review prior OKR performance and learnings.
- ✅ Align with leadership on strategic themes and investment levels.
- ✅ Validate data availability to measure key results.

# Invocation Guidance
```bash
codex skills run definition.okr_drafting \
  --vars "timeframe={{timeframe}}" \
         "strategic_theme={{strategic_theme}}" \
         "baseline_metrics={{baseline_metrics}}" \
         "risks={{risks}}"
```

# Recommended Input Attachments
- Past OKR reports and retrospective notes.
- Strategic brief or executive priorities deck.

# Claude Workflow Outline
1. Summarize the strategic theme, timeframe, and context.
2. Draft 1–3 objectives highlighting desired customer and business outcomes.
3. Propose 3–5 measurable key results per objective with baseline and target values.
4. Suggest initiatives, owners, and confidence levels for each key result.
5. Flag risks, dependencies, and instrumentation actions required.

# Output Template
```
## OKR Draft — {{timeframe}}

### Objective 1 — <Outcome-focused statement>
| Key Result | Baseline | Target | Measurement Plan | Confidence | Owner |
| --- | --- | --- | --- | --- | --- |
- Supporting Initiatives:
  - Initiative — Owner (Confidence)

### Objective 2 — ...

## Risks & Dependencies
- Risk:
- Mitigation:

## Instrumentation Checklist
- Metric:
- Action:
- Owner:
```

# Follow-up Actions
- Review draft OKRs with cross-functional leadership for calibration.
- Translate agreed initiatives into backlog epics with discovery tasks.
- Schedule mid-quarter reviews to monitor progress and adjust.
