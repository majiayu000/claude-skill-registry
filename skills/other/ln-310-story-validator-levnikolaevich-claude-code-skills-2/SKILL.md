---
name: ln-310-story-validator
description: Validates Stories/Tasks with GO/NO-GO verdict, Readiness Score (1-10), Penalty Points, and Anti-Hallucination verification. Auto-fixes to reach 0 points, delegates to ln-002 for docs. Use when reviewing Stories before execution or when user requests validation.
---

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
1. Audit: Calculate penalty points for all 19 criteria
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
  - Load Tasks metadata (3-8 implementation tasks)

Phase 2: Research & Audit
  - Extract technical domains from Story/Tasks
  - Delegate documentation creation to ln-002
  - Research via MCP Ref (RFC, OWASP, library versions)
  - Verify technical claims (Anti-Hallucination)
  - Calculate Penalty Points (19 criteria)

Phase 3: Audit Results & Fix Plan
  - Display Penalty Points table and fix plan
  - Wait for user approval (Plan Mode only)

Phase 4: Auto-Fix (7 groups)
  - Fix Structural violations (#1-#4)
  - Fix Standards violations (#5)
  - Fix Solution violations (#6)
  - Fix Workflow violations (#7-#13)
  - Fix Quality violations (#14-#15)
  - Fix Dependencies violations (#18-#19)
  - Fix Traceability violations (#16-#17)

Phase 5: Agent Review (delegated to ln-311)
  - Invoke ln-311-agent-reviewer with story_ref + tasks_ref
  - Apply accepted suggestions to Story/Tasks

Phase 6: Approve & Notify
  - Set Story/Tasks to Todo status in Linear
  - Update kanban_board.md with APPROVED marker
  - Add Linear comment with validation summary
  - Display tabular output to terminal
```

## Workflow Overview

### Phase 1: Discovery & Loading

**Step 1: Configuration & Metadata Loading**
- Auto-discover configuration: Team ID (`docs/tasks/kanban_board.md`), project docs (`CLAUDE.md`), epic from Story.project
- Load metadata only: Story ID/title/status/labels, child Task IDs/titles/status/labels
- Expect 3-8 implementation tasks; record parentId for filtering
- Rationale: keep loading light; full descriptions arrive in Phase 2

### Phase 2: Research & Audit

**Always execute for every Story - no exceptions.**

**Step 1: Domain Extraction**
- Extract technical domains from Story title + Technical Notes + Implementation Tasks
- Load pattern registry from `references/domain_patterns.md`
- Scan Story content for pattern matches via keyword detection
- Build list of detected domains requiring documentation

**Step 2: Documentation Delegation**
- For EACH detected pattern, delegate to ln-002:
  ```
  Skill(skill="ln-002-best-practices-researcher",
        args="doc_type=[guide|manual|adr] topic='[pattern]'")
  ```
- Receive file paths to created documentation (`docs/guides/`, `docs/manuals/`, `docs/adrs/`, `docs/research/`)

**Step 3: Research via MCP**
- Query MCP Ref for industry standards: `ref_search_documentation(query="[topic] RFC OWASP best practices 2025")`
- Query Context7 for library versions: `resolve-library-id` + `query-docs`
- Extract: standards (RFC numbers, OWASP rules), library versions, patterns

**Step 4: Anti-Hallucination Verification**
- Scan Story/Tasks for technical claims (RFC references, library versions, security requirements)
- Verify each claim has MCP Ref/Context7 evidence
- Flag unverified claims for correction
- Status: VERIFIED (all sourced) or FLAGGED (list unverified)

**Step 5: Penalty Points Calculation**
- Evaluate all 19 criteria against Story/Tasks
- Assign penalty points per violation (CRITICAL=10, HIGH=5, MEDIUM=3, LOW=1)
- Calculate total penalty points
- Build fix plan for each violation

### Phase 3: Audit Results & Fix Plan

**Display audit results:**
- Penalty Points table (criterion, severity, points, description)
- Total: X penalty points
- Fix Plan: list of fixes for each criterion

**Mode handling:**
- **IF Plan Mode:** Show results + "After your approval, changes will be applied" -> WAIT
- **ELSE (Normal Mode):** Proceed to Phase 4 immediately

### Phase 4: Auto-Fix

**Execute fixes for ALL 19 criteria on the spot.**

- Execution order (7 groups):
  1. **Structural (#1-#4)** — Story/Tasks template compliance + AC completeness/specificity
  2. **Standards (#5)** — RFC/OWASP compliance FIRST (before YAGNI/KISS!)
  3. **Solution (#6)** — Library versions
  4. **Workflow (#7-#13)** — Test strategy, docs integration, size, cleanup, YAGNI, KISS, task order, Database Creation
  5. **Quality (#14-#15)** — Documentation complete, hardcoded values
  6. **Dependencies (#18-#19)** — Story/Task independence (no forward dependencies)
  7. **Traceability (#16-#17)** — Story-Task alignment, AC coverage quality (LAST, after all fixes)
- Use Auto-Fix Actions table below as authoritative checklist
- Zero out penalty points as fixes applied
- Test Strategy section must exist but remain empty (testing handled separately)

### Phase 5: Agent Review (Delegated)

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

### Structural (#1-#4)

| # | Criterion | What it checks | Penalty | Auto-fix actions |
|---|-----------|----------------|---------|------------------|
| 1 | Story Structure | 8 sections per template | LOW (1) | Add/reorder sections with TODO placeholders; update Linear |
| 2 | Tasks Structure | Each Task has 7 sections | LOW (1) | Load each Task; add/reorder sections; update Linear |
| 3 | Story Statement | As a/I want/So that clarity | LOW (1) | Rewrite using persona/capability/value; update Linear |
| 4 | Acceptance Criteria | Given/When/Then, 3-5 items | MEDIUM (3) | Normalize to G/W/T; add edge cases; update Linear |

### Standards (#5)

| # | Criterion | What it checks | Penalty | Auto-fix actions |
|---|-----------|----------------|---------|------------------|
| 5 | Standards Compliance | Each technical decision references specific RFC/OWASP/REST standard by number | CRITICAL (10) | Query MCP Ref; update Technical Notes with compliant approach |

### Solution (#6)

| # | Criterion | What it checks | Penalty | Auto-fix actions |
|---|-----------|----------------|---------|------------------|
| 6 | Library & Version | Libraries are latest stable | HIGH (5) | Query Context7; update to recommended versions |

### Workflow (#7-#13)

| # | Criterion | What it checks | Penalty | Auto-fix actions |
|---|-----------|----------------|---------|------------------|
| 7 | Test Strategy | Section exists but empty | LOW (1) | Ensure section present; leave empty (testing handled separately) |
| 8 | Documentation Integration | No standalone doc tasks | MEDIUM (3) | Remove doc-only tasks; fold into implementation DoD |
| 9 | Story Size | 3-8 tasks; 3-5h each | MEDIUM (3) | If <3 or >8, add TODO; flag task size issues |
| 10 | Test Task Cleanup | No premature test tasks | MEDIUM (3) | Remove test tasks before final; testing appears later |
| 11 | YAGNI | Each Task maps to ≥1 Story AC; no tasks without AC justification | MEDIUM (3) | Move speculative items to Out of Scope unless standards require |
| 12 | KISS | No task requires >3 new abstractions; if >3 → split or simplify | MEDIUM (3) | Simplify unless standards require complexity |
| 13 | Task Order | DB→Service→API→UI | MEDIUM (3) | Reorder Tasks foundation-first |

### Quality (#14-#15)

| # | Criterion | What it checks | Penalty | Auto-fix actions |
|---|-----------|----------------|---------|------------------|
| 14 | Documentation Complete | Pattern docs exist + referenced | HIGH (5) | Delegate to ln-002; add all doc links to Technical Notes |
| 15 | Code Quality Basics | No hardcoded values | MEDIUM (3) | Add TODOs for constants/config/env |

### Traceability (#16-#17)

| # | Criterion | What it checks | Penalty | Auto-fix actions |
|---|-----------|----------------|---------|------------------|
| 16 | Story-Task Alignment | Each Task title contains keyword from Story AC; grep verification | MEDIUM (3) | Add TODO to misaligned Tasks; warn user |
| 17 | AC-Task Coverage | Coverage matrix: each AC row has ≥1 Task; no empty rows | MEDIUM (3) | Add TODO for uncovered ACs; suggest missing Tasks |

### Dependencies (#18-#19)

| # | Criterion | What it checks | Penalty | Auto-fix actions |
|---|-----------|----------------|---------|------------------|
| 18 | Story Dependencies | No forward Story dependencies | CRITICAL (10) | Flag forward dependencies; suggest reorder |
| 19 | Task Dependencies | No forward Task dependencies | MEDIUM (3) | Flag forward dependencies; reorder Tasks |

**Maximum Penalty:** 60 points

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

| Score | Status | Gate |
|-------|--------|------|
| 9-10 | Excellent | GO |
| 7-8 | Good | GO |
| 5-6 | Acceptable | GO (with notes) |
| 3-4 | Concerns | NO-GO (requires review) |
| 1-2 | Critical | NO-GO (major issues) |

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

Verify all 19 criteria (#1-#19) from Auto-Fix Actions pass with concrete evidence (doc path, MCP result, Linear update) before proceeding to Phase 6.

## Definition of Done

- Phases 1-6 completed: metadata loaded, research done, penalties calculated, fixes applied, agent review done, Story approved.
- Penalty Points = 0 (all 19 criteria fixed). Readiness Score ≥ 5.
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
  - `references/dependency_validation.md` (criteria #18-#19)
  - `references/traceability_validation.md` (criteria #16-#17)
  - `references/domain_patterns.md` (pattern registry for ln-002 delegation)
  - `references/penalty_points.md` (penalty system details)
- **Linear integration:** `../shared/templates/linear_integration.md`

---
**Version:** 7.0.0 (BREAKING: Added 2 new criteria #18-#19 for Story/Task dependencies per BMAD Method. Expanded criterion #4 with AC completeness/specificity, #9 with Database Creation Principle, #13 with forward dependency checks, #17 with STRONG/WEAK/MISSING coverage quality. Total 19 criteria, max 60 penalty points.)
**Last Updated:** 2026-02-03
