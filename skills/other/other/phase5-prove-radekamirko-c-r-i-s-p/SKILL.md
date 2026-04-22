---
name: phase5-prove
description: The Mileva Method (CRISP) — Phase 5: Prove. Success validation against Phase R baseline metrics. Use after deployment. Triggers on "prove", "phase 5", "validate", "did it work", "success criteria", "measure results", or after go-live.
---

# P — Prove: Success Validation

> Did the needle move?

## Project State

> At the start of Phase P: read `docs/crisp-state.json`. Pull `phases.R.baseline` and `phases.R.successTarget` as the measurement baseline. Check `phases.S.sprints` to know what was built.
>
> At the end of Phase P: update `docs/crisp-state.json`:
> - Add `"P"` to `phases.complete`
> - Set `phases.P.complete` to `true`
> - Set `phases.P.outcome` to `"success"`, `"partial"`, or `"fail"`
> - Add summary notes to `phases.P.notes`

This phase closes the loop back to Phase R. One question drives everything.

---

## What to Measure

Pull the baseline and targets from `docs/success-metrics.md` and measure against them:
- **Quantitative:** Did each metric hit its target? (e.g. "quotes sent in 4min vs 4h before")
- **Qualitative:** Re-run the survey or interview from the Phase R baseline frustration score — did it improve?
- **Second-order effects:** Did the downstream impacts materialise? (e.g. cart abandonment dropped after checkout speed improved)

---

## Outcomes

**Success** → document what worked, close the project, capture learnings.

**Partial** → identify which metrics hit and which didn't. Was the target unrealistic, or did the solution miss?

**Fail** → return to Phase R. The problem may have been misdiagnosed, or the success criteria were wrong.

> In Serbia, when things go sideways, we make jokes. It's not denial — it's perspective. Balkan humor is the ability to look at a disaster and find the absurdity before you find the culprit. Apply that here. If Phase P says fail, laugh once — then go back to Phase R with fresh eyes. A failed outcome is the most honest piece of data you'll collect in the whole project. The problem was misdiagnosed. Now you know exactly where. That's worth something.

---

## Exit Checklist
- [ ] Quantitative metrics measured against baselines in `docs/success-metrics.md`
- [ ] Qualitative scores re-evaluated against Phase R frustration baseline
- [ ] Second-order effects checked
- [ ] Success / partial / fail called explicitly — no ambiguity
- [ ] Learnings documented
- [ ] Client signed off
