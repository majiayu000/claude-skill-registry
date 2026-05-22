---
name: ln-310-story-validator
description: This skill should be used to validate and auto-fix Stories/Tasks against 2025 standards. Penalty Points system (goal = 0), delegates to ln-002 for documentation, Plan Mode support. Auto-discovers team/config.
---

# Story Verification Skill

Validate and auto-fix Stories and Tasks against 2025 standards before execution.

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
1. Audit: Calculate penalty points for all 17 criteria
2. Fix: Auto-fix and zero out points
3. Report: Total Before -> 0 After

## Mode Detection

Detect operating mode at startup:

**Plan Mode Active:**
- Phase 1-2: Full audit (discovery + research + penalty calculation)
- Phase 3: Show results + fix plan -> WAIT for user approval
- Phase 4-5: After approval -> execute fixes

**Normal Mode:**
- Phase 1-5: Standard workflow without stopping
- Automatically fix and approve

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

**Step 4: Penalty Points Calculation**
- Evaluate all 17 criteria against Story/Tasks
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

**Execute fixes for ALL 17 criteria on the spot.**

- Execution order (6 groups):
  1. **Structural (#1-#4)** — Story/Tasks template compliance
  2. **Standards (#5)** — RFC/OWASP compliance FIRST (before YAGNI/KISS!)
  3. **Solution (#6)** — Library versions
  4. **Workflow (#7-#13)** — Test strategy, docs integration, size, cleanup, YAGNI, KISS, task order
  5. **Quality (#14-#15)** — Documentation complete, hardcoded values
  6. **Traceability (#16-#17)** — Story-Task alignment, AC coverage (LAST, after all fixes)
- Use Auto-Fix Actions table below as authoritative checklist
- Zero out penalty points as fixes applied
- Test Strategy section must exist but remain empty (testing handled separately)

### Phase 5: Approve & Notify

- Set Story + all Tasks to Todo (Linear); update `kanban_board.md` with APPROVED marker
- **Add Linear comment** with full validation summary:
  - Penalty Points table (Before -> After = 0)
  - Auto-Fixes Applied table
  - Documentation Created table (docs created via ln-002)
  - Standards Compliance Evidence table
- **Display tabular output** (Unicode box-drawing) to terminal
- Final: Total Penalty Points = 0
- **Optional:** If `--execute` flag provided, delegate to ln-400-story-executor to start execution immediately after approval

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
| 5 | Standards Compliance | RFC, OWASP, REST, Security | CRITICAL (10) | Query MCP Ref; update Technical Notes with compliant approach |

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
| 11 | YAGNI | No premature features | MEDIUM (3) | Move speculative items to Out of Scope unless standards require |
| 12 | KISS | Simplest solution | MEDIUM (3) | Simplify unless standards require complexity |
| 13 | Task Order | DB→Service→API→UI | MEDIUM (3) | Reorder Tasks foundation-first |

### Quality (#14-#15)

| # | Criterion | What it checks | Penalty | Auto-fix actions |
|---|-----------|----------------|---------|------------------|
| 14 | Documentation Complete | Pattern docs exist + referenced | HIGH (5) | Delegate to ln-002; add all doc links to Technical Notes |
| 15 | Code Quality Basics | No hardcoded values | MEDIUM (3) | Add TODOs for constants/config/env |

### Traceability (#16-#17)

| # | Criterion | What it checks | Penalty | Auto-fix actions |
|---|-----------|----------------|---------|------------------|
| 16 | Story-Task Alignment | Tasks implement Story statement | MEDIUM (3) | Add TODO to misaligned Tasks; warn user |
| 17 | AC-Task Coverage | Each AC has implementing Task | MEDIUM (3) | Add TODO for uncovered ACs; suggest missing Tasks |

**Maximum Penalty:** 50 points

## Self-Audit Protocol (Mandatory)

Before marking any criterion as complete, provide concrete evidence (doc path, MCP result, Linear update).

| # | Self-Audit Question | Required Evidence |
|---|---------------------|-------------------|
| 1 | Validated all 8 Story sections? | Section list |
| 2 | Loaded full description for each Task? | Task validation count |
| 3 | Statement in As a/I want/So that? | Quoted statement |
| 4 | AC are G/W/T and testable? | AC count and format |
| 5 | Verified RFC/OWASP/REST compliance? | Standards list + MCP result |
| 6 | Checked library versions via Context7? | Context7 result |
| 7 | Test Strategy kept empty? | Note that testing deferred |
| 8 | Docs integrated, no standalone tasks? | Integration evidence |
| 9 | Task count 3-8 and 3-5h? | Task count/sizes |
| 10 | No premature test tasks? | Search result |
| 11 | Only current-scope features (YAGNI)? | Scope review |
| 12 | Simplest approach within standards (KISS)? | Simplicity justification |
| 13 | Tasks ordered Foundation-First? | Task order list |
| 14 | All pattern docs exist and referenced? | Doc paths from ln-002 |
| 15 | Hardcoded values handled? | TODO/config evidence |
| 16 | Each Task aligns with Story statement? | Alignment check result |
| 17 | Each AC has implementing Task? | Coverage matrix |

## Definition of Done

- **Phase 1:** Auto-discovery done; Story + Tasks metadata loaded; task count checked
- **Phase 2:** Domain extraction complete; ln-002 delegated for docs; MCP research done; Penalty Points calculated
- **Phase 3:** Audit results shown; IF Plan Mode: user approved
- **Phase 4:** All 17 criteria auto-fixed; Penalty Points = 0; Test Strategy empty; test tasks removed
- **Phase 5:** Story/Tasks set to Todo; `kanban_board.md` updated; Linear comment added; tabular output displayed
- **Optional:** If `--execute` flag, ln-400-story-executor invoked after approval

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
5. **Phase 5:** Story -> Todo, tabular report

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

- **Templates (centralized):** `shared/templates/story_template.md`, `shared/templates/task_template_implementation.md`
- **Local copies:** `docs/templates/` (in target project)
- **Validation Checklists (Progressive Disclosure):**
  - `references/verification_checklist_template.md` (overview of 6 categories)
  - `references/structural_validation.md` (criteria #1-#4)
  - `references/standards_validation.md` (criterion #5)
  - `references/solution_validation.md` (criterion #6)
  - `references/workflow_validation.md` (criteria #7-#13)
  - `references/quality_validation.md` (criteria #14-#15)
  - `references/traceability_validation.md` (criteria #16-#17)
  - `references/domain_patterns.md` (pattern registry for ln-002 delegation)
  - `references/penalty_points.md` (penalty system details)
- **Linear integration:** `../shared/templates/linear_integration.md`

---
**Version:** 5.0.0
**Last Updated:** 2025-01-07
