---
name: lp-do-assessment-07-measurement-profiling
description: Measurement profiling for new startups (ASSESSMENT-07). Elicits tracking setup, ≥2 key metrics, success thresholds, and data collection feasibility. Produces a measurement-plan artifact ready for current situation capture. Upstream of lp-do-assessment-08-current-situation.
---

# lp-do-assessment-07-measurement-profiling — Measurement Profiling (ASSESSMENT-07)

Elicits and records how the operator will measure whether the distribution plan is working. Defines the tracking method, ≥2 key metrics, success thresholds, and confirms data collection is feasible.

## Invocation

```
/lp-do-assessment-07-measurement-profiling --business <BIZ>
```

Required:
- `--business <BIZ>` — 3-4 character business identifier

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

ELICIT + WRITE

This skill:
- Reads ASSESSMENT-03 (selected product), ASSESSMENT-06 (channels identified)
- Pre-populates a draft from any measurement context already documented in strategy docs
- Surfaces gaps and asks the operator to fill or confirm each field
- Writes the final ASSESSMENT-07 artifact

Does NOT:
- Set up actual tracking infrastructure (that is S1B territory)
- Research industry benchmarks for conversion rates or CAC (that is S3 territory)
- Set field values the operator has not confirmed

## Precursor Inputs

Read before eliciting any fields:
- `docs/business-os/strategy/<BIZ>/s0c-option-select.user.md` — selected product (what is being measured)
- `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-launch-distribution-plan.user.md` — channels (what needs instrumentation)
- Any existing strategy doc with measurement or analytics references

## Elicitation Questions

Present as a structured Q&A. Pre-populate from existing docs where possible; mark pre-populated answers as `(pre-filled — confirm or correct)`.

**Section A — Tracking Setup**

1. What tool or method will you use to track results? (e.g. GA4, Plausible, spreadsheet, Etsy dashboard, manual order log)
2. Can this be set up with current resources? (yes / no — if no, what is blocking?)

**Section B — Key Metrics**

For each metric (minimum 2):
1. Metric name (e.g. "revenue", "conversion rate", "units sold", "email signups", "CAC")
2. How will it be captured? (tool/method from Section A, or separate source)
3. Reporting frequency: daily / weekly / monthly

**Section C — Success Thresholds**

1. What does "working" look like at 30 days? (e.g. "≥5 orders", "≥€500 revenue", "≥2% conversion")
2. What would trigger a channel reassessment? (e.g. "<1 order/week for 4 weeks")

**Section D — Data Collection Feasibility**

1. Is data collection GDPR/privacy-compliant? (yes / no — if no, describe required changes)
2. Does collection require any tooling or access not currently available? (yes / no — if yes, describe)

## Output Artifact

**Path:** `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-measurement-profile.user.md`

**Frontmatter:**
```yaml
---
Type: Measurement-Plan
Stage: ASSESSMENT-07
Business: <BIZ>
Status: Draft
Created: <today>
Updated: <today>
Owner: <operator name>
---
```

**Sections:**

### A) Tracking Setup

| Field | Value |
|---|---|
| Primary tracking tool/method | <e.g. GA4 + manual order log> |
| Setup feasibility | <yes — available now / conditional — requires X> |

### B) Key Metrics

| Metric | Capture method | Frequency |
|---|---|---|
| <metric 1> | <tool / source> | daily / weekly / monthly |
| <metric 2> | <tool / source> | daily / weekly / monthly |

### C) Success Thresholds

| Horizon | "Working" threshold | Reassessment trigger |
|---|---|---|
| 30 days | <e.g. ≥5 orders or ≥€500 revenue> | <e.g. <1 order/week for 4 weeks> |

### D) Data Collection Feasibility

| Check | Status | Notes |
|---|---|---|
| GDPR/privacy compliance | ✅ compliant / ⚠️ requires action | <detail> |
| Tooling availability | ✅ available / ⚠️ requires setup | <detail> |

## Quality Gate

Before saving, verify:
- [ ] Section A has a named tracking tool/method and feasibility status
- [ ] Section B has ≥2 metrics, each with capture method and frequency
- [ ] Section C has a 30-day "working" threshold and reassessment trigger
- [ ] Section D completed (privacy + tooling feasibility both addressed)
- [ ] Frontmatter fields all present: Type, Stage, Business, Status, Created, Updated, Owner
- [ ] Artifact saved to correct path before completion message

## Red Flags

Invalid outputs — do not emit:
- Fewer than 2 metrics in Section B (minimum 2 required for ASSESSMENT gate to pass)
- "We'll know if it works" (Section C must have specific numeric thresholds)
- Section D skipped (GDPR compliance check is mandatory)
- Artifact not saved (output must be written to file, not only displayed in chat)

## Completion Message

> "Measurement plan recorded: `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-measurement-profile.user.md`. [N] metrics defined; tracking via [method]. Ready for ASSESSMENT-08 Current Situation."

---

## Integration

**Upstream (ASSESSMENT-06):** Runs after `/lp-do-assessment-06-distribution-profiling --business <BIZ>` produces <YYYY-MM-DD>-launch-distribution-plan.user.md.

**Downstream consumer:** `modules/assessment-intake-sync.md` reads `<YYYY-MM-DD>-measurement-profile.user.md` as its sixth precursor (ASSESSMENT-07). Section B metrics inform intake Section F (Missing-Data Checklist — any metric with feasibility gap). Section A tracking setup informs intake Section A (Execution posture).

**Downstream:** `/lp-do-assessment-08-current-situation --business <BIZ>` runs after this artifact is active. ASSESSMENT gate checks ≥2 metrics and a named tracking method before allowing ASSESSMENT→S1 advance.
