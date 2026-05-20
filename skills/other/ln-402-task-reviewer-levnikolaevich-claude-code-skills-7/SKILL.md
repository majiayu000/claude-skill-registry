---
name: ln-402-task-reviewer
description: "L3 Worker. Reviews task implementation for quality, code standards, test coverage. Creates [BUG] tasks for side-effect issues found outside task scope. Sets task Done or To Rework. Runs inline (Skill tool) from ln-400 main flow."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Task Reviewer

**MANDATORY after every task execution.** Reviews a single task in To Review and decides Done vs To Rework with immediate fixes or clear rework notes.

> **This skill is NOT optional.** Every task executed by ln-401/ln-403/ln-404 MUST be reviewed by ln-402 immediately. No exceptions, no batching, no skipping.

## Purpose & Scope
- Receive task ID from orchestrator (ln-400); load full task and parent Story independently (Linear: get_issue; File: Read task file).
- Check architecture, correctness, configuration hygiene, docs, and tests.
- For test tasks, verify risk-based limits and priority (≤15) per planner template.
- Update only this task: accept (Done) or send back (To Rework) with explicit reasons and fix suggestions tied to best practices.

## Task Storage Mode

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Load task** | `get_issue(task_id)` | `Read("docs/tasks/epics/.../tasks/T{NNN}-*.md")` |
| **Load Story** | `get_issue(parent_id)` | `Read("docs/tasks/epics/.../story.md")` |
| **Update status** | `update_issue(id, state: "Done"/"To Rework")` | `Edit` the `**Status:**` line in file |
| **Add comment** | Linear comment API | Append to task file or kanban |

**File Mode status values:** Done, To Rework (only these two outcomes from review)

## Mode Detection

Detect operating mode at startup:

**Plan Mode Active:**
- Steps 1-2: Load task context (read-only, OK in plan mode)
- Generate REVIEW PLAN (files, checks) → write to plan file
- Call ExitPlanMode → STOP. Do NOT execute review.
- Steps 3-8: After approval → execute full review

**Normal Mode:**
- Steps 1-8: Standard workflow without stopping

## Plan Mode Support

**MANDATORY READ:** Load `shared/references/plan_mode_pattern.md` Workflow A (Preview-Only) for plan mode behavior.

**CRITICAL: In Plan Mode, plan file = REVIEW PLAN (what will be checked). NEVER write review findings or verdicts to plan file.**

**Review Plan format:**

```
REVIEW PLAN for Task {ID}: {Title}

| Field | Value |
|-------|-------|
| Task | {ID}: {Title} |
| Status | {To Review} |
| Type | {impl/test/refactor} |
| Story | {Parent ID}: {Parent Title} |

Files to review:
- {file1} (deliverable)
- {file2} (affected component)

| # | Check | Will Verify |
|---|-------|-------------|
| 1 | Approach | Technical Approach alignment |
| 2 | Clean Code | No dead code, no backward compat shims |
| 3 | Config | No hardcoded creds/URLs |
| 4 | Errors | try/catch on external calls |
| 5 | Logging | ERROR/INFO/DEBUG levels |
| 6 | Comments | WHY not WHAT, docstrings |
| 7 | Naming | Project conventions |
| 8 | Docs | API/env/README updates |
| 9 | Tests | Updated/risk-based limits |
| 10 | AC | 4 criteria validation |
| 11 | Side-effects | Pre-existing bugs in touched files |
| 12 | CI Checks | lint/typecheck pass per ci_tool_detection.md |

Expected output: Verdict (Done/To Rework) + Issues + Fix actions
```

## Progress Tracking with TodoWrite

When operating in any mode, skill MUST create detailed todo checklist tracking ALL steps.

**Rules:**
1. Create todos IMMEDIATELY before Step 1
2. Each workflow step = separate todo item; multi-check steps get sub-items
3. Mark `in_progress` before starting step, `completed` after finishing

**Todo Template (~11 items):**

```
Step 1: Receive Task
  - Load task by ID

Step 2: Read Context
  - Load full task + parent Story + affected components

Step 2b: Goal Articulation Gate
  - State what specific quality question this review must answer (<=25 tokens each)

Step 3: Review Checks
  - Verify approach alignment with Story Technical Approach
  - Check clean code: no dead code, no backward compat shims
  - Cross-file DRY: Grep src/ for new function/class names (count mode). 3+ similar → CONCERN
  - Check config hygiene, error handling, logging
  - Check comments, naming, docs updates
  - Verify tests updated/run (risk-based limits for test tasks)

Step 4: AC Validation
  - Validate implementation against 4 AC criteria

Step 5: Side-Effect Bug Detection
  - Scan for bugs outside task scope, create [BUG] tasks

Step 6: Decision
  - Apply minor fixes or set To Rework with guidance

Step 7: Mechanical Verification
  - Run lint/typecheck per ci_tool_detection.md (only if verdict=Done)

Step 8: Update & Commit
  - Set task status, update kanban, post review comment
  - If Done: commit ALL uncommitted changes in branch (git add -A)
```

## Workflow (concise)
1) **Receive task:** Get task ID from orchestrator (ln-400). Load full task and parent Story independently. Detect type (label "tests" -> test task, else implementation/refactor).
2) **Read context:** Full task + parent Story; load affected components/docs; review diffs if available.
2b) **Goal gate:** **MANDATORY READ:** `shared/references/goal_articulation_gate.md` — Before reviewing, state: (1) REAL GOAL: what specific quality question must this review answer for THIS task? (2) DONE: what evidence proves quality is sufficient? (3) NOT THE GOAL: what would a surface-level rubber-stamp look like? (4) INVARIANTS: what non-obvious constraint exists (side-effects on other modules, implicit AC)?
3) **Review checks:**
   **MANDATORY READ:** `shared/references/clean_code_checklist.md`
   - **Goal validation (Recovery Paradox):** If executor articulated a REAL GOAL (visible in task comments or implementation), validate it matches the Story's target deliverable. If executor framed the goal around a secondary subject (e.g., "implement the endpoint" instead of "enable user data export") → CONCERN: `GOAL-MISFRAME: executor goal targets secondary subject, may miss hidden constraints.`
   - Approach: diff aligned with Technical Approach in Story. If different → rationale documented in code comments.
   - **Clean code:** Per checklist — verify all 4 categories. Replaced implementations fully removed. If refactoring changed API — callers updated, old signatures removed. <!-- Defense-in-depth: also checked by ln-511 MNT-DC- -->
   - **Cross-file DRY:** For each NEW function/class/handler created by task, Grep `src/` for similar names/patterns (count mode). If 3+ files contain similar logic → add CONCERN: `MNT-DRY-CROSS: {pattern} appears in {count} files — consider extracting to shared module.` This catches cross-story duplication that per-task review misses. <!-- Defense-in-depth: also checked by ln-511 MNT-DRY- -->
   - No hardcoded creds/URLs/magic numbers; config in env/config.
   - Error handling: all external calls (API, DB, file I/O) wrapped in try/catch or equivalent. No swallowed exceptions. Layering respected; reuse existing components. <!-- Defense-in-depth: layers also checked by ln-511 ARCH-LB- -->
   - Side-effect breadth: service functions with 3+ side-effect categories → CONCERN: `ARCH-AI-SEB` <!-- Defense-in-depth: also ln-511, ln-624 Rule 10 -->
   - Interface honesty: read-named functions (get_/find_/check_) with write side-effects → CONCERN: `ARCH-AI-AH` <!-- Defense-in-depth: also ln-511, ln-643 Rule 6 -->
   - Logging: errors at ERROR; auth/payment events at INFO; debug data at DEBUG. No sensitive data in logs.
   - Comments: explain WHY not WHAT; no commented-out code; docstrings on public methods; Task ID present in new code blocks (`// See PROJ-123`).
   - Naming: follows project's existing convention (check 3+ similar files). No abbreviations except domain terms. No single-letter variables (except loops).
   - Entity Leakage: ORM entities must NOT be returned directly from API endpoints. Use DTOs/response models. (BLOCKER for auth/payment, CONCERN for others) <!-- Defense-in-depth: also checked by ln-511 ARCH-DTO- -->
   - Method Signature: no boolean flag parameters in public methods (use enum/options object); no more than 5 parameters without DTO. (NIT) <!-- Defense-in-depth: also checked by ln-511 MNT-SIG- -->
   - Docs: if public API changed → API docs updated. If new env var → .env.example updated. If new concept → README/architecture doc updated.
   - Tests updated/run: for impl/refactor ensure affected tests adjusted; for test tasks verify risk-based limits and priority (≤15) per planner template.
4) **AC Validation (MANDATORY for implementation tasks):**
   **MANDATORY READ:** Load `references/ac_validation_checklist.md`. Verify implementation against 4 criteria:
   - **AC Completeness:** All AC scenarios covered (happy path + errors + edge cases).
   - **AC Specificity:** Exact requirements met (HTTP codes 200/401/403, timing <200ms, exact messages).
   - **Task Dependencies:** Task N uses ONLY Tasks 1 to N-1 (no forward dependencies on N+1, N+2).
   - **Database Creation:** Task creates ONLY tables in Story scope (no big-bang schema).
   If ANY criterion fails → To Rework with specific guidance from checklist.
5) **Side-Effect Bug Detection (MANDATORY):**
   While reviewing affected code, actively scan for bugs/issues NOT related to current task:
   - Pre-existing bugs in touched files
   - Broken patterns in adjacent code
   - Security issues in related components
   - Deprecated APIs, outdated dependencies
   - Missing error handling in caller/callee functions

   **For each side-effect bug found:**
   - Create new task in same Story (Linear: create_issue with parentId=Story.id; File: create task file)
   - Title: `[BUG] {Short description}`
   - Description: Location, issue, suggested fix
   - Label: `bug`, `discovered-in-review`
   - Priority: based on severity (security → 1 Urgent, logic → 2 High, style → 4 Low)
   - **Do NOT defer** — create task immediately, reviewer catches what executor missed

6) **Decision (for current task only):**
   - If only nits: apply minor fixes and set Done.
   - If issues remain: set To Rework with comment explaining why (best-practice ref) and how to fix.
   - Side-effect bugs do NOT block current task's Done status (they are separate tasks).
   - **If Done:** commit ALL uncommitted changes in the branch (not just task-related files): `git add -A && git commit -m "Implement {task_id}: {task_title}"`. This includes any changes from previous tasks, auto-fixes, or generated files — everything currently unstaged/staged goes into this commit.
7) **Mechanical Verification (if Done):**
   **MANDATORY READ:** `shared/references/ci_tool_detection.md`
   IF verdict == Done:
   - Detect lint/typecheck commands per discovery hierarchy in ci_tool_detection.md
   - Run detected checks (timeouts per guide: 2min linters, 5min typecheck)
   - IF any FAIL → override verdict to To Rework with last 50 lines of output
   - IF no tooling detected → SKIP with info message
8) **Update:** Set task status in Linear; update kanban: if Done → **remove task from kanban** (Done section tracks Stories only, not individual Tasks); if To Rework → move task to To Rework section; add review comment with findings/actions. If side-effect bugs created, mention them in comment.

## Review Quality Score

**Context:** Quantitative review result helps ln-400 orchestrator make data-driven decisions and tracks review consistency.

**Formula:** `Quality Score = 100 - (20 × BLOCKER_count) - (10 × CONCERN_count) - (3 × NIT_count)`

**Classify each finding from Steps 3-5:**

| Category | Weight | Examples |
|----------|--------|----------|
| BLOCKER | -20 | AC not met, security issue, missing error handling, wrong approach |
| CONCERN | -10 | Suboptimal pattern, missing docs, test gaps |
| NIT | -3 | Naming, style, minor cleanup |

**Verdict mapping:**

| Score | Verdict | Action |
|-------|---------|--------|
| 90-100 | Done | Accept, apply nit fixes inline |
| 70-89 | Done (with notes) | Accept, document concerns for future |
| <70 | To Rework | Send back with fix guidance per finding |

**Note:** Side-effect bugs (Step 5) do NOT affect current task's quality score — they become separate [BUG] tasks.

## Critical Rules
- One task at a time; side-effect bugs → separate [BUG] tasks (not scope creep).
- Quality gate: all in-scope issues resolved before Done, OR send back with clear fix guidance.
- Test-task violations (limits/priority ≤15) → To Rework.
- Keep task language (EN/RU) in edits/comments.
- Mechanical checks (lint/typecheck) run ONLY when verdict is Done; skip for To Rework.

## Definition of Done
- Steps 1-8 completed: context loaded, review checks passed, AC validated, side-effect bugs created, mechanical verification passed, decision applied.
- If Done: ALL uncommitted changes committed (`git add -A`) with task ID; task removed from kanban. If To Rework: task moved with fix guidance.
- Review comment posted (findings + [BUG] list if any).

## Reference Files
- **[MANDATORY] Problem-solving approach:** `shared/references/problem_solving.md`
- **AC validation rules:** `shared/references/ac_validation_rules.md`
- AC Validation Checklist: `references/ac_validation_checklist.md` (4 criteria: Completeness, Specificity, Dependencies, DB Creation)
- **Clean code checklist:** `shared/references/clean_code_checklist.md`
- **CI tool detection:** `shared/references/ci_tool_detection.md`
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 5.0.0
**Last Updated:** 2026-02-07
