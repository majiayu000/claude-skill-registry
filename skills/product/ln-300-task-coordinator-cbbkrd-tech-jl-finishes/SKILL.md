---
name: ln-300-task-coordinator
description: Orchestrates task operations. Analyzes Story, builds optimal plan (1-8 implementation tasks), delegates to ln-301-task-creator (CREATE/ADD) or ln-302-task-replanner (REPLAN). Auto-discovers team ID.
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Linear Task Planner (Orchestrator)

Coordinates creation or replanning of implementation tasks for a Story. Builds the ideal plan first, then routes to workers.

## Purpose & Scope
- Auto-discover Team ID, load Story context (AC, Technical Notes, Context)
- Build optimal implementation task plan (1-8 implementation tasks; NO test/refactoring tasks) in Foundation-First order
- Detect mode and delegate: CREATE/ADD -> ln-301-task-creator, REPLAN -> ln-302-task-replanner
- Strip any Non-Functional Requirements; only functional scope becomes tasks
- Never creates/updates Linear or kanban directly (workers do)

## Task Storage Mode

**MANDATORY READ:** Load `shared/references/storage_mode_detection.md` for Linear vs File mode detection and operations.

Workers (ln-301, ln-302) handle the actual Linear/File operations based on detected mode.

## When to Use
- Need tasks for a Story with clear AC/Technical Notes
- Story requirements changed and existing tasks must be updated
- Only for implementation tasks (test tasks → ln-404, refactoring → quality gate)

## Quality Criteria

**MANDATORY READ:** Load `shared/references/creation_quality_checklist.md` §Task Creation Checklist for validation criteria that ln-310 will enforce.

## Workflow (concise)
- **Phase 1 Discovery:** Auto-discover Team ID (docs/tasks/kanban_board.md); parse Story ID from request.
- **Phase 2 Decompose (always):** **MANDATORY READ:** `shared/references/goal_articulation_gate.md` — Before building IDEAL plan, state REAL GOAL of this Story in one sentence (the deliverable, not the process). Verify: does the decomposition serve THIS goal? Then: Load Story (AC, Technical Notes, Context), assess complexity, build IDEAL plan (1-8 implementation tasks only), **scan for reusable patterns** (Grep `src/` for error handlers, validators, utilities relevant to task categories — count only; if found, append `**Pattern Hint:** {count} existing {category} patterns in src/. Review for reuse before creating new (Step 4a in ln-401).` to relevant task descriptions), apply Foundation-First execution order, **validate Task Independence**, **assign Parallel Groups**, **define verification methods for each task AC**, extract guide links.
- **Phase 3 Check & Detect Mode:** Query Linear for existing tasks (metadata only). Detect mode by count + user keywords (add/replan).
- **Phase 4 Delegate:** Call the right worker with Story data, IDEAL plan/append request, guide links, existing task IDs if any; autoApprove=true.
- **Phase 5 Verify:** Ensure worker returns URLs/summary and updated kanban_board.md; report result.

## Task Plan Readiness Score

**Context:** Validates plan quality before delegation to workers, preventing rework.

After building IDEAL plan (Phase 2), score 5 criteria:

| # | Criterion | Check |
|---|-----------|-------|
| 1 | **Independence** | No forward dependencies between tasks (Task N uses only 1..N-1) |
| 2 | **AC clarity** | Each task AC has measurable outcome AND verification method (test/command/inspect) |
| 3 | **Tech confidence** | All referenced technologies/patterns are known or researched |
| 4 | **Scope isolation** | Tasks don't overlap with other Stories' scope |
| 5 | **Architecture compliance** | Tasks reference correct layers (DB→Repo→Service→API), no planned cross-layer violations (e.g., API task doing direct DB calls) |
| 6 | **Parallel groups valid** | Tasks in same group have no mutual dependencies; all deps point to earlier groups; numbers sequential |

**Score = count of PASS criteria (0-6)**
- 5-6/6: Delegate to worker
- 3-4/6: Show warnings to user, fix or proceed
- <3/6: Rework plan before delegation

## Verification Methods for Task AC

**Context:** Goal-Driven Execution pattern — define HOW to verify each AC at planning time so executor (ln-401) can loop through verifications after implementation.

When building IDEAL plan (Phase 2), each task AC must include a `verify:` method:

| Method | When to Use | Example |
|--------|-------------|---------|
| **test** | Existing test covers AC | `verify: test (test_auth.py::test_login_success)` |
| **command** | CLI command validates outcome | `verify: command (curl -X POST /users → 201)` |
| **inspect** | File/output check | `verify: inspect (migration file has email column)` |

**Rule:** At least 1 AC per task must use `test` or `command` (not all `inspect`).

**See also:** `shared/references/ac_validation_rules.md` §5 for full format and examples.

## Task Independence Validation

Rules per `creation_quality_checklist.md` #19 (dependencies) and #13 (Foundation-First order).

**Examples:**
- ❌ WRONG: "Task 2: Validate token (requires Task 3 to generate keys)"
- ✅ RIGHT: "Task 1: Generate keys" → "Task 2: Validate token (uses Task 1 keys)"

**If forward dependency detected:** Reorder, refactor to remove dependency, or split into sequential parts.

## Parallel Group Assignment

After building IDEAL plan and validating independence, assign **Parallel Group** numbers to enable concurrent execution in ln-400.

**Algorithm:**
```
group = 1
FOR EACH task T IN ordered_plan:
  deps = tasks that T depends on (from Related/Context)
  IF any dep is in CURRENT group:
    group++
  T.parallel_group = group
```

**Example:**
| Task | Dependencies | Group |
|------|-------------|-------|
| T1: DB migration | none | 1 |
| T2: UserRepo | T1 | 2 |
| T3: ProductRepo | T1 | 2 |
| T4: UserService | T2 | 3 |
| T5: API endpoint | T4 | 4 |

**Rules:**
- Tasks in the same group have NO mutual dependencies (only depend on previous groups)
- Group numbers are sequential (1, 2, 3...), no gaps
- Single-task groups are valid (sequential execution, same as current behavior)
- Write `**Parallel Group:** {N}` in each task document (per `shared/templates/task_template_implementation.md`)
- **Backward compatibility:** if task lacks `**Parallel Group:**` field, ln-400 treats it as its own group (sequential)

## Mode Matrix
| Condition | Mode | Delegate | Payload |
|-----------|------|----------|---------|
| Count = 0 | CREATE | ln-301-task-creator | taskType=implementation, Story data, IDEAL plan, guideLinks |
| Count > 0 AND "add"/"append" | ADD | ln-301-task-creator | taskType=implementation, appendMode=true, newTaskDescription, guideLinks |
| Count > 0 AND replan keywords | REPLAN | ln-302-task-replanner | taskType=implementation, Story data, IDEAL plan, guideLinks, existingTaskIds |
| Count > 0 AND ambiguous | ASK | Clarify with user | — |

## Plan Mode Behavior
When invoked in Plan Mode (read-only):
- Execute Phases 1-3 normally (Discovery, Decompose, Check Existing)
- Phase 4: DO NOT delegate to workers — instead show IDEAL plan preview:
  - Task titles, goals, estimates, Foundation-First order
  - Mode detected (CREATE/ADD/REPLAN)
  - What worker WOULD be invoked (ln-301 or ln-302)
- Phase 5: Write plan summary to plan file (not Linear)
- NO Linear API calls, NO kanban updates, NO worker invocations

**TodoWrite format (mandatory):**
Add phases to todos before starting:
```
- Phase 1: Discovery (in_progress)
- Phase 2: Decompose & Build IDEAL Plan (pending)
- Phase 3: Check Existing & Detect Mode (pending)
- Phase 4: Delegate to ln-301/ln-302 (pending)
- Phase 5: Verify worker result (pending)
```
Mark each as in_progress when starting, completed when done.

## Critical Rules
- Decompose-first: always build IDEAL plan before looking at existing tasks.
- Foundation-First execution order per `creation_quality_checklist.md` #13.
- Task limits: 1-8 implementation tasks, 3-5h each (3-5 tasks optimal). Test task created later by test planner.
- Linear creation must be sequential: create one task, confirm success, then create the next (no bulk) to catch errors early.
- **HARD CONSTRAINT:** This skill creates ONLY implementation tasks (taskType=implementation). NEVER include test tasks, manual testing tasks, or refactoring tasks in the plan. Test tasks are created LATER by test planner (after manual testing passes). Refactoring tasks are created by quality gate when code quality issues found.
- No code snippets in descriptions; workers own task documents and Linear/kanban updates.
- Language preservation: keep Story language (EN/RU) in any generated content by workers.

## Definition of Done (orchestrator)
- Team ID discovered; Story ID parsed.
- Story loaded; IDEAL plan built (1-8 implementation tasks only) with Foundation-First order and guide links.
- **NO test or refactoring tasks** in IDEAL plan (only taskType=implementation).
- Existing tasks counted; mode selected (CREATE/ADD/REPLAN or ask).
- Worker invoked with correct payload and autoApprove=true.
- Worker summary received (Linear URLs/operations) and kanban update confirmed.
- Next steps returned (ln-310-story-validator, then orchestrator continues).

## Reference Files
- **[MANDATORY] Problem-solving approach:** `shared/references/problem_solving.md`
- **Orchestrator lifecycle:** `shared/references/orchestrator_pattern.md`
- **Auto-discovery patterns:** `shared/references/auto_discovery_pattern.md`
- **Decompose-first pattern:** `shared/references/decompose_first_pattern.md`
- **Plan mode behavior:** `shared/references/plan_mode_pattern.md`
- **Numbering conventions:** `shared/references/numbering_conventions.md` (Task per-Story numbering)
- **Storage mode detection:** `shared/references/storage_mode_detection.md`
- Templates (centralized): `shared/templates/task_template_implementation.md`
- Local copies: `docs/templates/task_template_implementation.md` (in target project, created by workers)
- Replan algorithm details: `ln-302-task-replanner/references/replan_algorithm.md`
- Auto-discovery notes: `CLAUDE.md`, `docs/tasks/kanban_board.md`

---
**Version:** 4.0.0
**Last Updated:** 2026-02-03
