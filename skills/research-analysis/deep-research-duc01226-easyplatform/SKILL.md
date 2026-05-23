---
name: deep-research
version: 1.0.0
description: '[Research] Deep-dive into top sources from web-research. Extract key findings, cross-validate claims, build evidence base.'
allowed-tools: Read, Write, WebFetch, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/web-research-protocol.md`

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

## Quick Summary

**Goal:** Deep-dive into top sources, extract key findings, cross-validate claims, build structured evidence base.

**Workflow:**

1. **Read source map** — Load output from web-research step
2. **Fetch top sources** — WebFetch top 5-8 Tier 1-2 sources
3. **Extract findings** — Pull key facts, data points, quotes
4. **Cross-validate** — Compare findings across sources
5. **Build evidence base** — Structured findings with confidence scores

**Key Rules:**

- Maximum 8 WebFetch calls per invocation
- Every finding must cite specific source
- Conflicting claims → present both, flag discrepancy

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Deep Research

## Step 1: Load Source Map

Read the source map from `.claude/tmp/_sources-{slug}.md` (output of web-research step).

Prioritize sources for deep-dive:

1. Tier 1-2 sources first
2. High-relevance sources
3. Sources covering identified gaps

## Step 2: Fetch Top Sources

For each priority source (max 8):

1. Run `WebFetch` with the URL
2. Extract: key claims, data points, quotes, methodology
3. Note: publication date, author credentials, source type

## Step 3: Extract Findings

For each source, extract:

- **Key claims** — factual statements with specific data
- **Data points** — numbers, percentages, dates
- **Quotes** — notable expert statements
- **Methodology** — how data was gathered (for market reports)

## Step 4: Cross-Validate

Compare findings across sources:

- **Agreement** — 2+ sources say the same thing → high confidence
- **Discrepancy** — sources disagree → note both positions
- **Unique** — only 1 source → mark as "single source, unverified"

## Step 5: Build Evidence Base

Write to `.claude/tmp/_evidence-{slug}.md`:

```markdown
# Evidence Base: {Topic}

**Date:** {date}
**Sources analyzed:** {count}

## Findings

### Finding 1: {Title}

**Confidence:** {95%|80%|60%|<60%}
**Sources:** [1], [3]
**Content:** {finding with inline citations}
**Cross-validation:** {agreement/discrepancy notes}

## Unresolved Discrepancies

- {claim X from source A vs claim Y from source B}

## Gaps Remaining

- {what couldn't be verified}
```

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `research` workflow** (Recommended) — web-research → deep-research → synthesis → review
> 2. **Execute `/deep-research` directly** — run this skill standalone

---

## Next Steps

**MANDATORY IMPORTANT MUST** after completing this skill, use `AskUserQuestion` to recommend:

- **"/business-evaluation (Recommended)"** — Evaluate business viability from research
- **"/knowledge-synthesis"** — If synthesizing research report
- **"Skip, continue manually"** — user decides

## Closing Reminders

**MANDATORY IMPORTANT MUST** break work into small todo tasks using `TaskCreate` BEFORE starting.
**MANDATORY IMPORTANT MUST** validate decisions with user via `AskUserQuestion` — never auto-decide.
**MANDATORY IMPORTANT MUST** add a final review todo task to verify work quality.
