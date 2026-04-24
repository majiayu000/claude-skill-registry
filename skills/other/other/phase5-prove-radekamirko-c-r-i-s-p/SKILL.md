---
name: phase5-prove
description: The Mileva Method (CRISP) — Phase 5: Prove. Success validation against Phase R baseline metrics, test log review, and AI justification validation. Use after deployment. Triggers on "prove", "phase 5", "validate", "did it work", "success criteria", "measure results", or after go-live.
---

## Pacing Rule — One Section at a Time

> Present one section, deliverable, or elicitation move at a time.
> After presenting — stop. Wait for the client to respond.
> Do not pre-fill and present multiple sections in one message.
> Do not move to the next step until the client confirms, corrects, or gives a clear go-ahead.
>
> The goal is a conversation, not a document dump.
> If you've written more than one section without a client response in between — you've gone too far.

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

This phase closes the loop back to Phase R. Three questions drive everything.

---

## 1. Did the needle move?

Pull the baseline and targets from `docs/success-metrics.md` and measure against them:
- **Quantitative:** Did each metric hit its target? (e.g. "quotes sent in 4min vs 4h before")
- **Qualitative:** Re-run the survey or interview from the Phase R baseline frustration score — did it improve?
- **Second-order effects:** Did the downstream impacts materialise? (e.g. cart abandonment dropped after checkout speed improved)

---

## 2. Was everything actually built and verified?

Read `docs/test-log.md`. For every sprint that shipped:
- Is there a test log entry?
- Did every specced behaviour (from the sprint's AI Spec test requirements) get a test written and run?
- Are there any ❌ failures that were never resolved?

> A system where the metrics look good but tests weren't written is a system running on luck. The test log is how you know the difference between "it works" and "it worked that one time we checked."

If the test log has gaps — identify what wasn't verified and decide: is this a risk to the outcome measurement, or is it acceptable to close?

---

## 3. Did the AI justify itself?

Read `docs/problem-statement.md` — AI Justification section. The client agreed to custom AI because it could do something off-the-shelf products couldn't.

Ask: **did that thing actually materialise?**

> "We said custom AI was justified because [X]. Did [X] happen? Is the client getting something from this that they couldn't get from Claude.ai at $20/month?"

If yes → close it. If no → document the gap honestly. It's a learning, not a failure — but it should be captured so the next project's justification gate is sharper.

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
- [ ] `docs/test-log.md` reviewed — all sprints have entries, no unresolved ❌ failures
- [ ] Every specced behaviour from AI Spec test requirements confirmed as verified
- [ ] AI justification validated — did custom AI deliver what justified not using off-the-shelf?
- [ ] Success / partial / fail called explicitly — no ambiguity
- [ ] Learnings documented (incl. what the test log revealed and whether AI justification held)
- [ ] Client signed off
