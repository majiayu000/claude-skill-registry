---
name: fix-parallel
version: 1.0.0
description: '[Implementation] Analyze & fix issues with parallel fullstack-developer agents'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` AND `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

> **Process Discipline:** MUST READ `.claude/skills/shared/red-flag-stop-conditions-protocol.md` — STOP after 3+ failed fix attempts or when each fix reveals a new problem.

> **Skill Variant:** Variant of `/fix` — parallel multi-issue resolution using subagents.

## Quick Summary

**Goal:** Fix multiple independent issues simultaneously using parallel fullstack-developer subagents.

**Workflow:**

1. **Triage** — Classify issues and verify independence (no shared files)
2. **Assign** — Distribute issues to parallel subagents with strict file ownership
3. **Execute** — Subagents fix issues independently
4. **Merge** — Review and integrate all fixes

**Key Rules:**

- Debug Mindset: every claim needs `file:line` evidence
- Issues MUST be independent (no overlapping file modifications)
- Each subagent owns specific files; no cross-boundary edits

### Frontend/UI Context (if applicable)

When this task involves frontend or UI changes, **MUST READ** `.claude/skills/shared/ui-system-context.md` and the following docs:

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

## Debug Mindset (NON-NEGOTIABLE)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

- Do NOT assume the first hypothesis is correct — verify with actual code traces
- Every root cause claim must include `file:line` evidence
- If you cannot prove a root cause with a code trace, state "hypothesis, not confirmed"
- Question assumptions: "Is this really the cause?" → trace the actual execution path
- Challenge completeness: "Are there other contributing factors?" → check related code paths
- No "should fix it" without proof — verify the fix addresses the traced root cause

## ⚠️ MANDATORY: Confidence & Evidence Gate

**MANDATORY IMPORTANT MUST** declare `Confidence: X%` with evidence list + `file:line` proof for EVERY claim.
**95%+** recommend freely | **80-94%** with caveats | **60-79%** list unknowns | **<60% STOP — gather more evidence.**

**Ultrathink parallel** to fix: <issues>$ARGUMENTS</issues>

**IMPORTANT:** Activate needed skills. Ensure token efficiency. Sacrifice grammar for concision.

## Workflow

### 1. Issue Analysis

- Use `debugger` subagent to analyze root causes
- Use `/scout-ext` to find related files
- Categorize issues by scope/area (frontend, backend, auth, payments, etc.)
- Identify dependencies between issues
- **External Memory**: Each parallel agent writes findings to `.ai/workspace/analysis/{issue-name}-{agent}.analysis.md`. Main agent re-reads all before coordinating fixes.

### 2. Parallel Fix Planning

- Trigger `/plan-parallel <detailed-fix-instructions>` for parallel-executable fix plan
- Wait for plan with dependency graph, execution strategy, file ownership matrix
- Group independent fixes for parallel execution
- Sequential fixes for dependent issues

### 3. Parallel Fix Implementation

- Read `plan.md` for dependency graph
- Launch multiple `fullstack-developer` agents in PARALLEL for independent fixes
    - Example: "Fix auth + Fix payments + Fix UI" → launch 3 agents simultaneously
    - Pass phase file path: `{plan-dir}/phase-XX-*.md`
    - Include environment info
- Wait for all parallel fixes complete before dependent fixes
- Sequential fixes: launch one agent at a time

**Subagent Context Discipline:**

- **Provide full task text** — paste task content into subagent prompt; don't make subagent read plan file
- **"Ask questions before starting"** — subagent should surface uncertainties before implementing
- **Self-review before reporting** — subagent checks completeness, quality, YAGNI before returning results

### 4. Testing

- Use `tester` subagent for full test suite
- NO fake data/mocks/cheats
- Verify all issues resolved
- If fail: use `debugger`, fix, repeat

### 5. Code Review

- **Two-stage review** (see `.claude/skills/shared/two-stage-task-review-protocol.md`):
    1. First: dispatch `spec-compliance-reviewer` to verify each fix matches its spec
    2. Only after spec passes: dispatch `code-reviewer` for quality review
- Verify fixes don't introduce regressions
- If critical issues: fix, retest

### 6. Project Management & Docs

- If approved: use `project-manager` + `docs-manager` in parallel
- Update plan files, docs, roadmap
- If rejected: fix and repeat

### 7. Prove Fix

- **MANDATORY:** Run `/prove-fix` for EACH parallel fix
- Build code proof traces per change with confidence scores
- If any change scores < 80%, return to debug for that fix

### 8. Final Report

- Summary of all fixes from parallel phases
- Verification status per issue (include prove-fix confidence scores)
- Ask to commit (use `git-manager` if yes)

**Example:** Fix 1 (auth) + Fix 2 (payments) + Fix 3 (UI) → Launch 3 fullstack-developer agents → Wait → Prove each fix → Fix 4 (integration) sequential

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
