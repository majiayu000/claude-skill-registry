---
name: lp-do-assessment-03-solution-selection
description: Solution selection gate for new startups (ASSESSMENT-03). Reads solution-space research results, builds an evaluation matrix, and produces a shortlist of 1-2 options with elimination rationale. Explicit kill gate — decision record required to continue to ASSESSMENT-04.
---

# lp-do-assessment-03-solution-selection — Solution Selection (ASSESSMENT-03)

Reads solution-space research results from the operator's deep research run, evaluates options against feasibility criteria, and produces a decision record with a shortlist of 1–2 viable options and elimination rationale for all others. An explicit decision record is required to continue to ASSESSMENT-04 (naming handoff).

## Invocation

```
/lp-do-assessment-03-solution-selection --business <BIZ>
```

Required:
- `--business <BIZ>` — 3-4 character business identifier

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

READ-THEN-DECIDE

This skill:
- Reads solution-space results and problem statement artifacts
- Builds an evaluation matrix across feasibility dimensions
- Produces a shortlist and decision record
- Applies a kill gate — if no viable option exists, stops the operator before ASSESSMENT-04

## Required Inputs

Required:
- `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-solution-profile-results.user.md` — operator-filled research output from `/lp-do-assessment-02-solution-profiling`

If no results file exists, stop: instruct the operator to complete the deep research run from `/lp-do-assessment-02-solution-profiling` first.

Also read if present:
- `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-problem-statement.user.md` — use to verify options are still solving the stated problem

## Steps

### Step 1: Load and parse results

Read the results file. Extract all product-type options returned by the research tool. List them. If fewer than 3 options are present, flag as a thin research result and note that the shortlist may be unreliable.

### Step 2: Build the evaluation matrix

For each option, score across these four criteria:

1. **Launch feasibility** — can a small team launch this within 6 months with realistic capital?
2. **Distribution path** — is there a known, accessible channel to reach the target user group?
3. **Regulatory/compliance burden** — are there licensing, certification, or compliance requirements that would materially delay or block launch?
4. **Problem-solution fit** — does this option directly address the stated problem in `<YYYY-MM-DD>-problem-statement.user.md`, or does it require the problem to be reframed?

Score each: Pass / Flag / Fail. A single Fail does not automatically eliminate an option — use judgment based on all four together. Document the rationale for each score; do not leave scores unexplained.

### Step 3: Apply elimination logic

Eliminate options that:
- Score Fail on Launch feasibility AND Fail on Distribution path
- Score Fail on Regulatory burden (hard legal block, not just complexity)
- Score Fail on Problem-solution fit (option solves a different problem)

For each eliminated option, write a 1-sentence elimination rationale. "Not interesting" is not a valid rationale — cite the specific criterion that failed.

### Step 4: Select shortlist

From remaining options, select 1–2 to carry forward to ASSESSMENT-04. If two options remain and both are genuinely viable, include both — the naming research phase can handle parallel tracks. Do not reduce to one arbitrarily.

Apply the problem-fit check: verify that each shortlisted option still addresses the problem statement as written. If an option requires reframing the problem, note this explicitly in the decision record.

### Step 5: Apply kill gate

**If no options survive elimination, apply the kill gate:**

> Explicit decision record required to continue to ASSESSMENT-04. No viable option identified from current solution-space results. Do not advance to ASSESSMENT-04 (naming handoff). Options:
> 1. Re-run `/lp-do-assessment-02-solution-profiling --business <BIZ>` with a refined problem scope or broader option set
> 2. Return to `/lp-do-assessment-01-problem-statement --business <BIZ>` to reassess the problem statement

Write the kill gate output to the artifact and stop. Do not proceed to ASSESSMENT-04.

### Step 6: Write and save decision record

Assemble all outputs into the decision record format below. Save to the output path.

## Output Contract

**Path:** `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-solution-decision.user.md`

**Format:**

```markdown
# Option Selection Decision — <BIZ>

## Evaluation Matrix

| Option | Launch Feasibility | Distribution Path | Regulatory Burden | Problem Fit | Status |
|---|---|---|---|---|---|
| <option name> | Pass/Flag/Fail | Pass/Flag/Fail | Pass/Flag/Fail | Pass/Flag/Fail | Shortlisted/Eliminated |

## Elimination Log

- **<option>**: [1-sentence rationale citing specific criterion]
- **<option>**: [1-sentence rationale citing specific criterion]

## Shortlist

1. **<option name>** — [2-3 sentence rationale for selection; any caveats]
2. **<option name>** (if applicable) — [2-3 sentence rationale]

## Decision

**Status:** GO / NO-GO

**Carry forward:** <option name(s)>

[If GO: "Proceed to `/lp-do-assessment-04-candidate-names --business <BIZ>` with the option(s) above."]
[If NO-GO: Kill gate language — see Step 5.]
```

**Downstream consumer:** `/lp-do-assessment-04-candidate-names --business <BIZ>` (ASSESSMENT-04) reads this file to scope the naming research to the selected option(s).

## Quality Gate

Before saving, verify:

- [ ] All options from results file appear in the evaluation matrix
- [ ] Every score has a documented rationale — no unexplained Pass/Flag/Fail
- [ ] Elimination log contains one entry per eliminated option with specific criterion cited
- [ ] Shortlist contains 1–2 options (not zero unless kill gate applies, not more than 2)
- [ ] Kill gate applied if no viable options remain
- [ ] `## Decision` section contains explicit GO/NO-GO verdict
- [ ] Shortlisted options align with the problem statement from `<YYYY-MM-DD>-problem-statement.user.md`
- [ ] Artifact saved to correct path before completion message

## Red Flags

Invalid outputs — do not emit:

- Evaluation matrix with unexplained scores ("it seemed weak")
- Elimination rationale of "not interesting" or "too crowded" without citing specific criteria
- Shortlist of zero options without triggering the kill gate
- Decision section missing or containing only "TBD"
- Kill gate suppressed — if no viable option exists, the gate MUST fire; do not advance the operator to ASSESSMENT-04

## Integration

**Upstream (ASSESSMENT-02):** Reads `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-solution-profile-results.user.md` from the operator's deep research run via `/lp-do-assessment-02-solution-profiling`.

**Downstream (ASSESSMENT-04):** `/lp-do-assessment-04-candidate-names --business <BIZ>` reads `<YYYY-MM-DD>-solution-decision.user.md` to scope naming research to the shortlisted option(s). The naming skill should be run with the shortlisted option names provided as context.
