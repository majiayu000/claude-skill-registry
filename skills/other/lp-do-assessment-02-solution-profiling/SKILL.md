---
name: lp-do-assessment-02-solution-profiling
description: Solution space scanning for new startups (ASSESSMENT-02). Produces a structured deep-research-ready prompt covering 5-10 candidate product-type options with feasibility flags. Feasibility only — no demand scoring until S2.
---

# lp-do-assessment-02-solution-profiling — Solution Space Scan (ASSESSMENT-02)

Produces a structured research prompt for the operator to run in a deep research tool (OpenAI Deep Research or equivalent). The prompt surfaces 5–10 candidate product-type options with feasibility and regulatory flags. Demand scoring is explicitly excluded — that happens at S2.

## Invocation

```
/lp-do-assessment-02-solution-profiling --business <BIZ>
```

Required:
- `--business <BIZ>` — 3-4 character business identifier

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

SOLUTION SPACE PROMPT AUTHORING ONLY

This skill:
- Reads the problem statement artifact from ASSESSMENT-01
- Compiles a structured research prompt
- Does NOT generate candidate product recommendations
- Does NOT score demand or estimate market size
- Does NOT issue a verdict on which option to pursue
- Does NOT run the research itself

The operator runs the compiled prompt in an external research tool. The results file from that run is the input to `/lp-do-assessment-03-solution-selection`.

## Required Inputs (pre-flight)

Required:
- `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-problem-statement.user.md` — output from `/lp-do-assessment-01-problem-statement`

If this file is missing, stop and instruct the operator to run `/lp-do-assessment-01-problem-statement --business <BIZ>` first.

Optional (read if present, note gap if absent):
- Any existing business brief or market notes under `docs/business-os/strategy/<BIZ>/`
- Any existing competitive landscape notes

**If a STOP advisory is present in `## Kill Conditions` of the problem statement, surface it to the operator before proceeding. The operator must explicitly acknowledge it to continue.**

## Output

This skill produces two artifacts:

**1. Research prompt (written by this skill):**
`docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-solution-profiling-prompt.md`

This file contains the compiled deep-research-ready prompt.

**2. Results artifact slot (filled by the operator after running the prompt):**
`docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-solution-profile-results.user.md`

This file does not exist yet. After running the research prompt, the operator saves the tool's output to this path. The date prefix must match the prompt file.

## Prompt Structure

The compiled prompt must contain these sections in order:

### 1. Role and method

Instruct the researcher to act as a product-type landscape researcher. Frame the task as: map the range of viable product-type approaches to a specific customer problem — not to recommend a product, but to enumerate options with honest feasibility signals.

### 2. Problem context

Paste or paraphrase the `## Core Problem` and `## Affected User Groups` sections from `<YYYY-MM-DD>-problem-statement.user.md` directly. Do not reframe or abstract. If the problem statement uses specific language, preserve it.

### 3. Solution type landscape

Ask the researcher to enumerate 5–10 distinct product-type approaches that could address the stated problem. Options should differ in product category, not just features (e.g., physical product vs. digital tool vs. marketplace vs. service). Request that each option be treated independently.

### 4. Per-option feasibility criteria

For each option, request these feasibility signals:
- Can this be launched by a small team within 6 months?
- Are there proven distribution channels for this product type?
- What are the primary technical, operational, or capital constraints?
- Is there evidence of adjacent successful businesses in this space?

**Explicitly instruct:** Do NOT score demand, estimate market size, or assess whether customers want this. Feasibility flags only at this stage.

### 5. Regulatory and compliance flags

Request that the researcher flag any known regulatory, certification, or compliance requirements for each option (e.g., medical device classification, food safety, financial services licensing). Flag "unknown" rather than omitting.

### 6. Manufacturing and supply chain flags

For physical product options, request: typical MOQ ranges, lead times, key supplier geographies, and whether white-label options exist. For digital options, request infrastructure dependencies.

### 7. Deliverables format

Instruct the researcher to return results as a structured list: one entry per option, each containing option name, brief description (2-3 sentences), feasibility signals (bulleted), regulatory flags, supply chain flags. No comparison rankings, no recommendation, no verdict.

## Handoff Note

After running the compiled prompt in a deep research tool (OpenAI Deep Research or equivalent):

1. Save the full output to `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-solution-profile-results.user.md` (same date as the prompt file).
2. Run `/lp-do-assessment-03-solution-selection --business <BIZ>` — it reads the results file as its primary input.

Do not skip the results file. `/lp-do-assessment-03-solution-selection` requires it.

## Quality Gate

Before saving the compiled prompt, verify:

- [ ] Problem context section quotes or closely paraphrases `<YYYY-MM-DD>-problem-statement.user.md` — not reformulated
- [ ] Prompt requests 5–10 distinct product-type options (not feature variants)
- [ ] All 4 feasibility criteria are present for each option
- [ ] Prompt contains explicit instruction: no demand scoring, feasibility flags only
- [ ] Regulatory and supply chain flag sections are present
- [ ] Deliverables format section instructs structured output with no ranking or recommendation
- [ ] Prompt file saved to correct path with correct date prefix
- [ ] Handoff note section present in prompt file pointing to `/lp-do-assessment-03-solution-selection`

## Completion Message

> Research prompt saved to `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-solution-profiling-prompt.md`.
>
> Drop this prompt into a deep research tool (OpenAI Deep Research or equivalent). When complete, save the full output to `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-solution-profile-results.user.md` (same date), then run `/lp-do-assessment-03-solution-selection --business <BIZ>`.

## Integration

**Upstream (ASSESSMENT-01):** Reads `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-problem-statement.user.md` from `/lp-do-assessment-01-problem-statement`.

**Downstream (ASSESSMENT-03):** `/lp-do-assessment-03-solution-selection --business <BIZ>` reads the results artifact filled by the operator after the research run.

**Note on S2 boundary:** ASSESSMENT-02 establishes feasibility signals only. Demand scoring, willingness-to-pay assessment, and market size estimation all belong to S2 (Market Intelligence). Do not blur this boundary in the prompt or in guidance to the operator.
