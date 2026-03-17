---
name: ln-310-story-validator
description: Validates Stories/Tasks with GO/NO-GO verdict, Readiness Score (1-10), Penalty Points, and Anti-Hallucination verification. Auto-fixes to reach 0 points, delegates to ln-002 for docs. Use when reviewing Stories before execution or when user requests validation.
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Story Verification Skill

Validate Stories/Tasks with explicit GO/NO-GO verdict, Readiness Score, and Anti-Hallucination verification.

## Purpose & Scope

- Validate Story plus child Tasks against industry standards and project patterns
- Calculate Penalty Points for violations, then auto-fix to reach 0 points
- Delegate to ln-002-best-practices-researcher for creating documentation (guides, manuals, ADRs, research)
- Support Plan Mode: show audit results, wait for approval, then fix
- Approve Story after fixes (Backlog -> Todo) with tabular output summary

## When to Use

- Reviewing Stories before approval (Backlog -> Todo)
- Validating implementation path across Story and Tasks
- Ensuring standards, architecture, and solution fit
- Optimizing or correcting proposed approaches

## Penalty Points System

**Goal:** Quantitative assessment of Story/Tasks quality. Target = 0 penalty points after fixes.

| Severity | Points | Description |
|----------|--------|-------------|
| CRITICAL | 10 | RFC/OWASP/security violations |
| HIGH | 5 | Outdated libraries, architecture issues |
| MEDIUM | 3 | Best practices violations |
| LOW | 1 | Structural/cosmetic issues |

**Workflow:**
1. Audit: Calculate penalty points for all 22 criteria
2. Fix: Auto-fix and zero out points
3. Report: Total Before -> 0 After

## Mode Detection

Detect operating mode at startup:

**Plan Mode Active:**
- Phase 1-2: Full audit (discovery + research + penalty calculation)
- Phase 3: Show results + fix plan -> WAIT for user approval
- Phase 4-6: After approval -> execute fixes

**Normal Mode:**
- Phase 1-6: Standard workflow without stopping
- Automatically fix and approve

## Plan Mode: Progress Tracking with TodoWrite

When operating in any mode, skill MUST create detailed todo checklist tracking ALL phases and steps.

**Rules:**
1. Create todos IMMEDIATELY before Phase 1
2. Each phase step = separate todo item
3. Mark `in_progress` before starting step, `completed` after finishing

**Todo Template (~21 items):**

```
Phase 1: Discovery & Loading
  - Auto-discover configuration (Team ID, docs)
  - Load Story metadata (ID, title, status, labels)
  - Load Tasks metadata (1-8 implementation tasks)

Phase 2: Research & Audit
  - Extract technical domains from Story/Tasks
  - Delegate documentation creation to ln-002
  - Research via MCP Ref (RFC, OWASP, library versions)
  - Verify technical claims (Anti-Hallucination)
  - Calculate Penalty Points (22 criteria)

Phase 3: Audit Results & Fix Plan
  - Display Penalty Points table and fix plan
  - Wait for user approval (Plan Mode only)

Phase 4: Auto-Fix (8 groups)
  - Fix Structural violations (#1-#4)
  - Fix Standards violations (#5)
  - Fix Solution violations (#6, #21)
  - Fix Workflow violations (#7-#13)
  - Fix Quality violations (#14-#15)
  - Fix Dependencies violations (#18-#19/#19b)
  - Fix Risk violations (#20)
  - Fix Traceability violations (#16-#17)

Phase 5: Agent Review (MANDATORY — delegated to ln-311)
  - [MANDATORY] Invoke ln-311-agent-reviewer with story_ref + tasks_ref
  - [MANDATORY] Process and apply accepted suggestions to Story/Tasks

Phase 6: Approve & Notify
  - Set Story/Tasks to Todo status in Linear
  - Update kanban_board.md with APPROVED marker
  - Add Linear comment with validation summary
  - Display tabular output to terminal
```

## Workflow

### Phase 1: Discovery & Loading

**Step 1: Configuration & Metadata Loading**
- Auto-discover configuration: Team ID (`docs/tasks/kanban_board.md`), project docs (`CLAUDE.md`), epic from Story.project
- Load metadata only: Story ID/title/status/labels, child Task IDs/titles/status/labels
- Expect 1-8 implementation tasks; record parentId for filtering
- Rationale: keep loading light; full descriptions arrive in Phase 2

### Phase 2: Research & Audit

**MANDATORY READ:** Load `references/phase2_research_audit.md` for complete research and audit procedure:
- Domain extraction from Story/Tasks
- Documentation delegation to ln-002 (guides/manuals/ADRs)
- MCP research (RFC/OWASP/library versions via Ref + Context7)
- Anti-Hallucination verification (evidence-based claims)
- Penalty Points calculation (22 criteria, see Auto-Fix Actions Reference in same file)

**Always execute for every Story - no exceptions.**

### Phase 3: Audit Results & Fix Plan

**Display audit results:**
- Penalty Points table (criterion, severity, points, description)
- Total: X penalty points
- Fix Plan: list of fixes for each criterion

**Mode handling:**
- **IF Plan Mode:** Show results + "After your approval, changes will be applied" -> WAIT
- **ELSE (Normal Mode):** Proceed to Phase 4 immediately

### Phase 4: Auto-Fix

**Execute fixes for ALL 22 criteria on the spot.**

- Execution order (8 groups):
  1. **Structural (#1-#4)** — Story/Tasks template compliance + AC completeness/specificity
  2. **Standards (#5)** — RFC/OWASP compliance FIRST (before YAGNI/KISS!)
  3. **Solution (#6, #21)** — Library versions, alternative solutions
  4. **Workflow (#7-#13)** — Test strategy, docs integration, size, cleanup, YAGNI, KISS, task order
  5. **Quality (#14-#15)** — Documentation complete, hardcoded values
  6. **Dependencies (#18-#19/#19b)** — Story/Task independence (no forward deps), parallel group validity
  7. **Risk (#20)** — Implementation risk analysis (after dependencies resolved, before traceability)
  8. **Verification (#22)** — AC verify methods exist for all task ACs (test/command/inspect)
  9. **Traceability (#16-#17)** — Story-Task alignment, AC coverage quality (LAST, after all fixes)
- Use Auto-Fix Actions table below as authoritative checklist
- Zero out penalty points as fixes applied
- Test Strategy section must exist but remain empty (testing handled separately)

### Phase 5: Agent Review (MANDATORY — DO NOT SKIP)

> **MANDATORY STEP:** This phase MUST execute regardless of Phase 4 results. Skipping agent review is a workflow violation. If agents unavailable, ln-311 returns SKIPPED — acceptable. But invocation MUST happen.

Invoke `Skill(skill="ln-311-agent-reviewer", args="{storyId}")`.
- ln-311 gets Story/Task references from Linear, builds prompt with references, runs agents in parallel, persists prompts and results in `.agent-review/{agent}/`.
- If verdict = `SUGGESTIONS` → apply ACCEPTED suggestions to Story/Tasks text.
- If verdict = `SKIPPED` (no agents or all failed) → proceed to Phase 6 unchanged.
- **Display:** agent stats from ln-311 output: `"Agent Review: {agent_stats summary}"`

### Phase 6: Approve & Notify

- Set Story + all Tasks to Todo (Linear); update `kanban_board.md` with APPROVED marker
- **Add Linear comment** with full validation summary:
  - Penalty Points table (Before -> After = 0)
  - Auto-Fixes Applied table
  - Documentation Created table (docs created via ln-002)
  - Standards Compliance Evidence table
- **Display tabular output** (Unicode box-drawing) to terminal
- Final: Total Penalty Points = 0
- **Recommended next step:** `ln-400-story-executor` to start Story execution

## Auto-Fix Actions Reference

**MANDATORY READ:** Load `references/phase2_research_audit.md` for complete 21-criteria table with:
- Structural (#1-#4): Story/Task template compliance
- Standards (#5): RFC/OWASP compliance
- Solution (#6, #21): Library versions, alternatives
- Workflow (#7-#13): Test strategy, docs, size, YAGNI/KISS, task order
- Quality (#14-#15): Documentation, hardcoded values
- Traceability (#16-#17): Story-Task alignment, AC coverage
- Dependencies (#18-#19/#19b): No forward dependencies
- Risk (#20): Implementation risk analysis

**Maximum Penalty:** 88 points (sum of all 22 criteria; #20 capped at 15)

## Final Assessment Model

**Outputs after all fixes applied:**

| Metric | Value | Meaning |
|--------|-------|---------|
| **Gate** | GO / NO-GO | Final verdict for execution readiness |
| **Readiness Score** | 1-10 | Quality confidence level |
| **Penalty Points** | 0 (after fixes) | Validation completeness |
| **Anti-Hallucination** | VERIFIED / FLAGGED | Technical claims verified |
| **AC Coverage** | 100% (N/N) | All ACs mapped to Tasks |

### Readiness Score Calculation

```
Readiness Score = 10 - (Penalty Points / 5)
```

**Before/After diagnostic:** Phase 3 calculates initial Penalty Points and Readiness Score (Before). Phase 4 auto-fixes reduce penalties to 0, yielding Readiness Score = 10 (After). Both values reported in Final Assessment for transparency.

| Gate | Condition |
|------|-----------|
| GO | Penalty Points = 0 after Phase 4 (Readiness Score = 10) |
| NO-GO | Any criterion FLAGGED as unfixable (see Critical Rules) |

### Anti-Hallucination Verification

Verify technical claims have evidence:

| Claim Type | Verification |
|------------|--------------|
| RFC/Standard reference | MCP Ref search confirms existence |
| Library version | Context7 query confirms version |
| Security requirement | OWASP/CWE reference exists |
| Performance claim | Benchmark/doc reference |

**Status:** VERIFIED (all claims sourced) or FLAGGED (unverified claims listed)

### Task-AC Coverage Matrix

Output explicit mapping:

```
| AC | Task(s) | Coverage |
|----|---------|----------|
| AC1: Given/When/Then | T-001, T-002 | ✅ |
| AC2: Given/When/Then | T-003 | ✅ |
| AC3: Given/When/Then | — | ❌ UNCOVERED |
```

**Coverage:** `{covered}/{total} ACs` (target: 100%)

## Self-Audit Protocol (Mandatory)

Verify all 22 criteria (#1-#22) from Auto-Fix Actions pass with concrete evidence (doc path, MCP result, Linear update) before proceeding to Phase 6.

## Critical Rules
- All 22 criteria MUST be verified with concrete evidence (doc path, MCP result, Linear update) before Phase 6 (Self-Audit Protocol)
- Fix execution order is strict: Structural -> Standards -> Solution -> Workflow -> Quality -> Dependencies -> Risk -> Traceability (standards before YAGNI/KISS)
- Never approve with Penalty Points > 0; all violations must be auto-fixed to zero. If auto-fix is impossible for a criterion (e.g., MCP Ref unavailable, external dependency), mark as FLAGGED with reason — penalty stays, Gate = NO-GO, user must resolve manually
- Test Strategy section must exist but remain empty (testing handled separately by other skills)
- In Plan Mode, MUST stop after Phase 3 and wait for user approval before applying any fixes

## Definition of Done

- Phases 1-6 completed: metadata loaded, research done, penalties calculated, fixes applied, agent review done, Story approved.
- Penalty Points = 0 (all 22 criteria fixed). Readiness Score ≥ 5.
- Anti-Hallucination: VERIFIED (all claims sourced via MCP).
- AC Coverage: 100% (each AC mapped to ≥1 Task).
- Agent Review: ln-311 invoked; suggestions aggregated, validated, accepted applied (or SKIPPED if no agents).
- Story/Tasks set to Todo; kanban updated; Linear comment with Final Assessment posted.

## Example Workflow

**Story:** "Create user management API with rate limiting"

1. **Phase 1:** Load metadata (5 Tasks, status Backlog)
2. **Phase 2:**
   - Domain extraction: REST API, Rate Limiting
   - Delegate ln-002: creates Guide-05 (REST patterns), Guide-06 (Rate Limiting)
   - MCP Ref: RFC 7231 compliance, OWASP API Security
   - Context7: Express v4.19 (current v4.17)
   - Penalty Points: 18 total (version=5, missing docs=5, structure=3, standards=5)
3. **Phase 3:**
   - Show Penalty Points table
   - IF Plan Mode: "18 penalty points found. Fix plan ready. Approve?"
4. **Phase 4:**
   - Fix #6: Update Express v4.17 -> v4.19
   - Fix #5: Add RFC 7231 compliance notes
   - Fix #13: Add Guide-05, Guide-06 references
   - Fix #17: Docs already created by ln-002
   - All fixes applied, Penalty Points = 0
5. **Phase 5:** Agent review (delegated to ln-311-agent-reviewer → apply accepted suggestions)
6. **Phase 6:** Story -> Todo, tabular report

## Template Loading

**Templates:** `story_template.md`, `task_template_implementation.md`

**Loading Logic:**
1. Check if `docs/templates/{template}.md` exists in target project
2. IF NOT EXISTS:
   a. Create `docs/templates/` directory if missing
   b. Copy `shared/templates/{template}.md` → `docs/templates/{template}.md`
   c. Replace placeholders in the LOCAL copy:
      - `{{TEAM_ID}}` → from `docs/tasks/kanban_board.md`
      - `{{DOCS_PATH}}` → "docs" (standard)
3. Use LOCAL copy (`docs/templates/{template}.md`) for all validation operations

**Rationale:** Templates are copied to target project on first use, ensuring:
- Project independence (no dependency on skills repository)
- Customization possible (project can modify local templates)
- Placeholder replacement happens once at copy time

## Reference Files

- **AC validation rules:** `shared/references/ac_validation_rules.md`
- **Plan mode behavior:** `shared/references/plan_mode_pattern.md`
- **Final Assessment:** `references/readiness_scoring.md` (GO/NO-GO rules, Readiness Score calculation)
- **Templates (centralized):** `shared/templates/story_template.md`, `shared/templates/task_template_implementation.md`
- **Local copies:** `docs/templates/` (in target project)
- **Validation Checklists (Progressive Disclosure):**
  - `references/structural_validation.md` (criteria #1-#4)
  - `references/standards_validation.md` (criterion #5)
  - `references/solution_validation.md` (criterion #6)
  - `references/workflow_validation.md` (criteria #7-#13)
  - `references/quality_validation.md` (criteria #14-#15)
  - `references/dependency_validation.md` (criteria #18-#19/#19b)
  - `references/risk_validation.md` (criterion #20)
  - `references/traceability_validation.md` (criteria #16-#17)
  - `references/domain_patterns.md` (pattern registry for ln-002 delegation)
  - `references/penalty_points.md` (penalty system details)
- **Prevention checklist:** `shared/references/creation_quality_checklist.md` (creator-facing mapping of 22 criteria)
- **Linear integration:** `../shared/templates/linear_integration.md`

---
**Version:** 7.0.0
**Last Updated:** 2026-02-03
