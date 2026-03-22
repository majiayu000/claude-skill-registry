---
name: knowledge-synthesis
version: 1.0.0
description: '[Research] Synthesize research findings into structured report using template. Final step of research workflow.'
allowed-tools: Read, Write, Edit, TaskCreate
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/web-research-protocol.md`

## Quick Summary

**Goal:** Synthesize evidence base into final structured report using enforced template.

**Workflow:**

1. **Load evidence** — Read evidence base from deep-research
2. **Load template** — Read enforced template from docs/templates/
3. **Synthesize** — Write report following template structure
4. **Citation check** — Verify every claim has citation
5. **Confidence summary** — Aggregate scores, flag gaps

**Key Rules:**

- MUST use enforced template structure — all sections required
- Every factual claim inline-cited: `[N]` referencing source table
- Knowledge gaps section mandatory

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Knowledge Synthesis

## Step 1: Load Evidence

Read `.claude/tmp/_evidence-{slug}.md` and `.claude/tmp/_sources-{slug}.md`.

Inventory:

- Total findings with confidence scores
- Unresolved discrepancies
- Remaining gaps

## Step 2: Load Template

Read the enforced template: `docs/templates/research-report-template.md`

Every section in the template MUST appear in the final report.

## Step 3: Synthesize Report

Write to `docs/knowledge/research/{slug}.md`:

For each template section:

1. Map relevant findings from evidence base
2. Write content with inline citations `[N]`
3. Declare confidence per finding
4. Note cross-cutting patterns and contradictions in Analysis section

## Step 4: Citation Audit

Verify:

- Every factual claim has at least one `[N]` citation
- Every source in the Sources table is referenced at least once
- No orphan citations (referencing non-existent source)

## Step 5: Confidence Summary

Calculate overall report confidence:

- Average of all finding confidence scores
- Weight by finding importance
- Flag any <60% findings prominently

## Output

Final report: `docs/knowledge/research/{descriptive-slug}.md`

Clean up working files from `.claude/tmp/` after successful synthesis.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
