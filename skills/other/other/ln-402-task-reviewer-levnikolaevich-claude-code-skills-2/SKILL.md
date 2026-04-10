---
name: ln-402-task-reviewer
description: "Reviews task implementation for quality, code standards, and test coverage. Use when task is in To Review. Sets task Done or To Rework."
allowed-tools: Read, Grep, Glob, Bash, WebFetch, mcp__context7, mcp__hex-graph__audit_workspace, mcp__hex-graph__find_references, mcp__hex-graph__analyze_changes, mcp__hex-line__changes
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

**Type:** L3 Worker
**Category:** 4XX Execution

# Task Reviewer

**MANDATORY after every task execution.** Reviews a single task in To Review and decides Done vs To Rework with immediate fixes or clear rework notes.

> **This skill is NOT optional.** Every executed task MUST be reviewed immediately. No exceptions, no batching, no skipping.

## Purpose & Scope
- Resolve task ID (per Input Resolution Chain); load full task and parent Story independently (Linear: get_issue; File: Read task file).
- Check architecture, correctness, configuration hygiene, docs, and tests.
- For test tasks, verify risk-based limits and priority (≤15) per planner template.
- Update only this task: accept (Done) or send back (To Rework) with explicit reasons and fix suggestions tied to best practices.

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `taskId` | Yes | args, parent Story, kanban, user | Task to review |

**Resolution:** Task Resolution Chain.
**Status filter:** To Review

## Phase 0: Tools Config

**MANDATORY READ:** Load `shared/references/environment_state_contract.md`, `shared/references/storage_mode_detection.md`, and `shared/references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider (`linear` | `file`).

## Task Storage Mode

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Load task** | `get_issue(task_id)` | `Read("docs/tasks/epics/.../tasks/T{NNN}-*.md")` |
| **Load Story** | `get_issue(parent_id)` | `Read("docs/tasks/epics/.../story.md")` |
| **Update status** | `save_issue(id, state: "Done"/"To Rework")` | `Edit` the `**Status:**` line in file |
| **Add comment** | `create_comment({issueId, body})` | `Write` comment to `.../comments/{ISO-timestamp}.md` |
| **Create [BUG] task** | `save_issue({title, parentId, team, labels, state})` | `Write("docs/tasks/.../T{NNN}-bug-{slug}.md")` |

**File Mode status values:** Done, To Rework (only these two outcomes from review)

## Mode Detection

Detect operating mode at startup:

**Plan Mode Active:**
- Steps 1-3: Resolve task and load context (read-only, OK in plan mode)
- Generate REVIEW PLAN (files, checks) → write to plan file
- Call ExitPlanMode → STOP. Do NOT execute review.
- Steps 4-9: After approval → execute full review

**Normal Mode:**
- Steps 1-9: Standard workflow without stopping

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
| 12 | Destructive ops | Safety guards from destructive_operation_safety.md (loaded in step 4) |
| 13 | Algorithm correctness | Loop invariants, collection keys, unbounded ops, shared state leaks |
| 14 | Event channels | Channel name consistency in diff |
| 15 | CI Checks | lint/typecheck pass per ci_tool_detection.md |

Expected output: Verdict (`Done | To Rework`) + Issues + Fix actions
```

## Progress Tracking with TodoWrite

When operating in any mode, skill MUST create detailed todo checklist tracking ALL steps.

**Rules:**
1. Create todos IMMEDIATELY before Step 1
2. Each workflow step = separate todo item; multi-check steps get sub-items
3. Mark `in_progress` before starting step, `completed` after finishing

**Todo Template (~11 items):**

```
Step 1: Resolve taskId
  - Resolve via args / Story context / kanban / AskUserQuestion (To Review filter)

Step 2: Load Task
  - Load task by ID, detect type

Step 3: Read Context
  - Load full task + parent Story + affected components

Step 3b: Goal Articulation Gate
  - State what specific quality question this review must answer (<=25 tokens each)

Step 4: Review Checks
  - Verify approach alignment with Story Technical Approach
  - Check clean code: no dead code, no backward compat shims
  - Cross-file DRY: Grep src/ for new function/class names (count mode). 3+ similar → CONCERN
  - Check config hygiene, error handling, logging
  - Check comments, naming, docs updates
  - Verify tests updated/run (risk-based limits for test tasks)

Step 5: AC Validation
  - Validate implementation against 4 AC criteria

Step 6: Side-Effect Bug Detection
  - Scan for bugs outside task scope, create [BUG] tasks

Step 7: Decision
  - Apply minor fixes or set To Rework with guidance

Step 8: Mechanical Verification
  - Run lint/typecheck per ci_tool_detection.md (only if verdict=Done)

Step 9: Update & Commit
  - Set task status, update kanban, post review comment
  - If Done: leave branch changes uncommitted for downstream branch ownership rules
```

## Workflow (concise)
1) **Resolve taskId:** Run Task Resolution Chain per guide (status filter: [To Review]).
2) **Load task:** Load full task and parent Story independently. Detect type (label "tests" -> test task, else implementation/refactor).
3) **Read context:** Full task + parent Story; load affected components/docs; review diffs if available.
   **Hex MCP acceleration:** Prefer `analyze_changes(path=project_root, base_ref="HEAD~1")` for semantic risk snapshot when graph is indexed; use `changes(path="src/", compare_against="HEAD~1")` for AST-level diff review of structural changes.
3b) **Goal gate:** **MANDATORY READ:** `shared/references/goal_articulation_gate.md` — Before reviewing, state: (1) REAL GOAL: what specific quality question must this review answer for THIS task? (2) DONE: what evidence proves quality is sufficient? (3) NOT THE GOAL: what would a surface-level rubber-stamp look like? (4) INVARIANTS: what non-obvious constraint exists (side-effects on other modules, implicit AC)?
4) **Review checks:**
   > **Spec-first gate:** Quick AC pre-check: scan task AC against implementation. If any AC is clearly unmet (BLOCKER-level) → immediate To Rework, skip remaining quality checks. Full AC validation still runs in Step 5.
   **MANDATORY READ:** `shared/references/clean_code_checklist.md`, `shared/references/destructive_operation_safety.md`
   - **Goal validation (Recovery Paradox):** If executor articulated a REAL GOAL (visible in task comments or implementation), validate it matches the Story's target deliverable. If executor framed the goal around a secondary subject (e.g., "implement the endpoint" instead of "enable user data export") → CONCERN: `GOAL-MISFRAME: executor goal targets secondary subject, may miss hidden constraints.`
   - Approach: diff aligned with Technical Approach in Story. If different → rationale documented in code comments.
   - **Clean code:** Per checklist — verify all 4 categories. Replaced implementations fully removed. If refactoring changed API — callers updated, old signatures removed. <!-- Defense-in-depth: also checked by ln-511 MNT-DC- -->
   - **Cross-file DRY:** For each NEW function/class/handler created by task, Grep `src/` for similar names/patterns (count mode). If 3+ files contain similar logic → add CONCERN: `MNT-DRY-CROSS: {pattern} appears in {count} files — consider extracting to shared module.` This catches cross-story duplication that per-task review misses. <!-- Defense-in-depth: also checked by ln-511 MNT-DRY- -->
   - **Cross-file DRY preferred (hex-graph):** If hex-graph indexed, use `audit_workspace(path=scan_path, verbosity="full")` and inspect returned `clones`. Filter groups where any member is in task-modified files. Each match = CONCERN: `MNT-DRY-CROSS`. Fall back to Grep name search above if hex-graph unavailable.
   - No hardcoded creds/URLs/magic numbers; config in env/config.
   - Destructive operation guards: use code-level guards table from destructive_operation_safety.md (loaded above). CRITICAL/HIGH severity → BLOCKER: SEC-DESTR-{ID}. MEDIUM severity → CONCERN: SEC-DESTR-{ID}.
   - Error handling: all external calls (API, DB, file I/O) wrapped in try/catch or equivalent. No swallowed exceptions. Layering respected; reuse existing components. <!-- Defense-in-depth: layers also checked by ln-511 ARCH-LB- -->
   - Side-effect breadth: **leaf** service functions with 3+ side-effect categories → CONCERN: `ARCH-AI-SEB`. Exception: orchestrator/coordinator functions (imports 3+ services AND delegates sequentially) are EXPECTED to have multiple side-effect categories — do NOT flag. <!-- Defense-in-depth: also ln-511, ln-624 Rule 10 -->
   - Interface honesty: read-named functions (get_/find_/check_) with write side-effects → CONCERN: `ARCH-AI-AH` <!-- Defense-in-depth: also ln-511, ln-643 Rule 6 -->
   - Logging: errors at ERROR; auth/payment events at INFO; debug data at DEBUG. No sensitive data in logs.
   - Comments: explain WHY not WHAT; no commented-out code; docstrings on public methods.
   - Naming: follows project's existing convention (check 3+ similar files). No abbreviations except domain terms. No single-letter variables (except loops).
   - Entity Leakage: ORM entities must NOT be returned directly from API endpoints. Use DTOs/response models. (BLOCKER for auth/payment, CONCERN for others) <!-- Defense-in-depth: also checked by ln-511 ARCH-DTO- -->
   - Method Signature: no boolean flag parameters in public methods (use enum/options object); no more than 5 parameters without DTO. (NIT) <!-- Defense-in-depth: also checked by ln-511 MNT-SIG- -->
   - **Algorithm correctness (loops, collections, boundaries):** Does `break`/`continue`/`return` inside loops handle ALL matching items, not just the first? Do dict/set comprehensions handle duplicate keys correctly (last-wins may lose data)? Any `list(query.all())` or unbounded loop on user-controlled data without LIMIT? Any mutable shared state (connection pool GUCs, session globals) that leaks across requests? (BLOCKER if data loss/corruption, CONCERN otherwise) <!-- Prefix: ALGO- -->
   - **Event channel consistency (task-scoped):** When task diff touches event-related code (NOTIFY/LISTEN/emit/subscribe/publish/on), verify: (1) channel name string in publisher matches channel name string in subscriber; (2) if channel name is a new string literal, Grep `src/` for matching listener/publisher counterpart. Mismatch → CONCERN: `ARCH-EVENT-MISMATCH: publisher '{pub_name}' has no matching subscriber`. Orphan → CONCERN: `ARCH-EVENT-ORPHAN: subscriber '{sub_name}' has no matching publisher`. <!-- Defense-in-depth: also checked by ln-652 Rule 6, ln-511 ARCH-EVENT- -->
   - **Simplicity criterion (task-scoped):** **MANDATORY READ:** `references/simplicity_criterion.md` — Check MNT-KISS-SCOPE (effort-S task with 3+ new abstractions) and MNT-YAGNI-SCOPE (refactoring added new dependencies or created 2x more files than modified). Advisory CONCERNs only. <!-- Defense-in-depth: also checked by ln-511 KISS/YAGNI -->
   - **Code efficiency (task-scoped):** Spot-check 2-3 key functions from diff for unnecessary intermediates, verbose patterns where idioms exist, or boilerplate framework handles. If found → CONCERN: `MNT-EFF-SCOPE: {pattern} in {file}`. Advisory only. (`shared/references/code_efficiency_criterion.md`) <!-- Defense-in-depth: executor self-checks via same reference -->
   - **Frontend review (conditional):** IF reviewed files include `.tsx/.vue/.svelte/.html/.css`: **MANDATORY READ:** `shared/references/frontend_design_guide.md`. (a) WCAG 2.1 AA: contrast ratios, keyboard nav, ARIA labels, focus management → BLOCKER: `A11Y-{ID}`. (b) Composition: single-purpose sections, no dashboard card mosaics → CONCERN: `UI-COMP-{ID}`. (c) Typography restraint: max 2 typefaces, 1 accent → CONCERN: `UI-TYPE`. (d) Copy quality: product language, no placeholder text → NIT: `UI-COPY`. (e) Motion justification: each animation serves hierarchy/atmosphere → NIT: `UI-MOTION`. (f) Design system adherence: if project has design_guidelines.md, verify tokens match → CONCERN: `UI-SYSTEM`.
   - Docs: if public API changed → API docs updated. If new env var → .env.example updated. If new concept → README/architecture doc updated.
   - Tests updated/run: for impl/refactor ensure affected tests adjusted; for test tasks verify risk-based limits and priority (≤15) per planner template.
5) **AC Validation (MANDATORY for implementation tasks):**
   **MANDATORY READ:** Load `references/ac_validation_checklist.md`. Verify implementation against 4 criteria:
   - **AC Completeness:** All AC scenarios covered (happy path + errors + edge cases).
   - **AC Specificity:** Exact requirements met (HTTP codes 200/401/403, timing <200ms, exact messages).
   - **Task Dependencies:** Task N uses ONLY Tasks 1 to N-1 (no forward dependencies on N+1, N+2).
   - **Database Creation:** Task creates ONLY tables in Story scope (no big-bang schema).
   If ANY criterion fails → To Rework with specific guidance from checklist.
6) **Side-Effect Bug Detection (MANDATORY):**
   While reviewing affected code, actively scan for bugs/issues NOT related to current task:
   - Pre-existing bugs in touched files
   - Broken patterns in adjacent code
   - Security issues in related components
   - Deprecated APIs, outdated dependencies
   - Missing error handling in caller/callee functions

   **For each side-effect bug found:**
   - Create new task in same Story:
     - IF `task_provider` = `linear`: `save_issue({title: "[BUG] {desc}", description, parentId: Story.id, team: teamId, labels: ["bug", "discovered-in-review"], state: "Backlog", priority})`
     - IF `task_provider` = `file`: `Write("docs/tasks/epics/.../tasks/T{NNN}-bug-{slug}.md")` with `**Status:** Backlog`, `**Labels:** bug, discovered-in-review`, `**Story:** US{NNN}`, `**Created:** {date}`
   - Title: `[BUG] {Short description}`
   - Description: Location, issue, suggested fix
   - Label: `bug`, `discovered-in-review`
   - Priority: based on severity (security → 1 Urgent, logic → 2 High, style → 4 Low)
   - **Do NOT defer** — create task immediately, reviewer catches what executor missed

7) **Decision (for current task only):**
   - If only nits: apply minor fixes and set Done.
   - If issues remain: set To Rework with comment explaining why (best-practice ref) and how to fix.
   - Side-effect bugs do NOT block current task's Done status (they are separate tasks).
   - **If Done:** leave branch changes uncommitted and hand off the accepted task state with review comment + summary artifact.
8) **Mechanical Verification (if Done):**
   **MANDATORY READ:** `shared/references/ci_tool_detection.md`
   IF verdict == Done:
   - Detect lint/typecheck commands per discovery hierarchy in ci_tool_detection.md
   - Run detected checks (timeouts per guide: 2min linters, 5min typecheck)
   **MANDATORY READ:** Load `shared/references/output_normalization.md`
   - IF any FAIL → apply output normalization per §1 normalize → §2 deduplicate → §4 truncate to 50 lines → override verdict to To Rework with normalized output
   - IF no tooling detected → SKIP with info message
9) **Update:** Set task status in Linear; update kanban: if Done → **remove task from kanban** (Done section tracks Stories only, not individual Tasks); if To Rework → move task to To Rework section; add review comment with findings/actions. If side-effect bugs created, mention them in comment.

## Review Quality Score

**Context:** Quantitative review results make downstream decisions auditable and track review consistency.

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

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`, `shared/references/worker_runtime_contract.md`, `shared/references/task_worker_runtime_contract.md`

Shared contract:
- emit `summary_kind=task-status`
- standalone mode omits `runId` and `summaryArtifactPath`
- managed mode passes both `runId` and exact `summaryArtifactPath` before the worker writes its validated review outcome

## Definition of Done
- [ ] Steps 1-9 completed: task resolved, context loaded, review checks passed, AC validated, side-effect bugs created, mechanical verification passed, decision applied.
- [ ] If Done: task removed from kanban after review acceptance. If To Rework: task moved with fix guidance.
- [ ] Review comment posted (findings + [BUG] list if any).
- [ ] Runtime summary artifact written to the shared task-status location.

## Reference Files
- **Environment state:** `shared/references/environment_state_contract.md`
- **Storage mode operations:** `shared/references/storage_mode_detection.md`
- **[MANDATORY] Problem-solving approach:** `shared/references/problem_solving.md`
- **AC validation rules:** `shared/references/ac_validation_rules.md`
- AC Validation Checklist: `references/ac_validation_checklist.md` (4 criteria: Completeness, Specificity, Dependencies, DB Creation)
- **Clean code checklist:** `shared/references/clean_code_checklist.md`
- **CI tool detection:** `shared/references/ci_tool_detection.md`
- **Output normalization:** `shared/references/output_normalization.md`
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 5.2.0
**Last Updated:** 2026-03-24
