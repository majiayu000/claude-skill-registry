---
name: lp-do-assessment-10-brand-profiling
description: Brand profiling for new startups (ASSESSMENT-10). Confirms business name, defines audience, personality, and voice & tone. Produces brand-strategy artifact ready for visual identity work. Upstream of lp-do-assessment-11-brand-identity.
---

# lp-do-assessment-10-brand-profiling — Brand Profiling (ASSESSMENT-10)

Load: ../_shared/assessment/assessment-base-contract.md

Elicits and records the foundational brand strategy for a new startup entering the ASSESSMENT stage. Confirms the business name from the naming shortlist, defines the target audience from a brand perspective, establishes personality adjective pairs, and captures voice & tone guidelines. All four sections must be present before the artifact is saved.

## Invocation

```
/lp-do-assessment-10-brand-profiling --business <BIZ>
```

Required:
- `--business <BIZ>` — 3-4 character business identifier

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

WRITE-FIRST ELICIT

This skill uses a write-first pattern:
1. Read all available ASSESSMENT artifacts
2. Write the artifact immediately with everything that can be inferred or confirmed from existing docs — marking each field `confirmed`, `provisional`, or `missing`
3. Save the artifact to disk
4. Ask the operator **only** about genuine gaps (fields marked `missing` or `provisional` that block ASSESSMENT-11)

Do NOT present a full Q&A before writing. Do NOT ask the operator to confirm fields that are already well-evidenced. Write first, then surface only the real gaps.

Does NOT:
- Research external sources (that is ASSESSMENT-01–ASSESSMENT-08 territory)
- Make naming decisions for the operator without confirmation
- Ask questions that can be answered from existing docs

## Required Inputs (pre-flight)

| Source | Path | Required |
|--------|------|----------|
| ASSESSMENT intake packet | `docs/business-os/startup-baselines/<BIZ>/<YYYY-MM-DD>-assessment-intake-packet.user.md` | Yes — primary source for name shortlist, ICP, and product context |
| Naming shortlist | `docs/business-os/strategy/<BIZ>/assessment/naming-workbench/latest-naming-shortlist.user.md` | Yes if present — extract `recommended_business_name` and `shortlist` array from YAML front matter |
| Problem statement | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-problem-statement.user.md` | No — read if present for ICP and pain-point context |
| Option selection | `docs/business-os/strategy/<BIZ>/s0c-option-select.user.md` | No — read if present for product and positioning context |
| Operator evidence | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-operator-context.user.md` | No — read if present for any pre-confirmed brand notes |

If any upstream ASSESSMENT artifacts are absent, note the gap but proceed — ASSESSMENT-10 captures operator-confirmed brand decisions and does not depend on all research outputs being complete.

---

## Steps

Load: modules/steps.md

---

## Output Contract and Quality Gate

Load: modules/output-and-quality.md

---

## Completion Message

> "Brand strategy recorded: `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-profile.user.md`. Name: <name> (<confirmed|provisional>). [N] personality pairs. Voice: <formality>."
>
> "Next step: run `/lp-do-assessment-11-brand-identity --business <BIZ>` to produce the visual brand identity and brand dossier."

---

## Integration

**Upstream (ASSESSMENT-08):** Runs after `/lp-do-assessment-08-current-situation` and the ASSESSMENT gate are complete.

**Downstream (ASSESSMENT-11):** `<YYYY-MM-DD>-brand-profile.user.md` is the primary required input for `/lp-do-assessment-11-brand-identity`. The Audience, Personality, and Voice & Tone sections are read directly into the brand dossier — they are not re-elicited at ASSESSMENT-11.

**No gate:** ASSESSMENT has no gate. After ASSESSMENT-11 completes, the operator proceeds directly to S1 (`/lp-readiness`).
