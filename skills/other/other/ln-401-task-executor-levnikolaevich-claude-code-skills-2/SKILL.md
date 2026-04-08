---
name: ln-401-task-executor
description: "Executes implementation tasks through Todo, In Progress, To Review. Use when task needs coding with KISS/YAGNI. Not for test tasks."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-line__outline, mcp__hex-line__read_file, mcp__hex-line__edit_file, mcp__hex-line__write_file, mcp__hex-line__verify, mcp__hex-line__changes, mcp__hex-line__inspect_path, mcp__hex-graph__index_project, mcp__hex-graph__find_symbols, mcp__hex-graph__inspect_symbol, mcp__hex-graph__analyze_edit_region
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Implementation Task Executor

**Type:** L3 Worker

Executes a single implementation (or refactor) task from Todo to To Review using the task description and linked guides.

## Purpose & Scope
- Handle one selected task only; never touch other tasks.
- Follow task Technical Approach/plan/AC; apply KISS/YAGNI and guide patterns.
- Update Linear/kanban for this task: Todo -> In Progress -> To Review.
- Run typecheck/lint; update docs/tests/config per task instructions.
- Not for test tasks (label "tests" goes to ln-404-test-executor).

**Hex MCP acceleration (if available):** Use `inspect_path()` and `outline(path)` before reading large code files. Use `read_file()` in discovery mode for structure and targeted ranges; when you need `revision` and checksums for a follow-up edit, refresh that file with `read_file(edit_ready=true, verbosity="full")` before `edit_file()`. For edits to existing code, run `index_project(path=project_root)` once and use `analyze_edit_region(...)` before non-trivial edits. After edits: `edit_file(base_revision=rev)` -> `verify(checksums)`. Before handoff: `changes()` to review diff.
## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `taskId` | Yes | args, parent Story, kanban, user | Task to execute |

**Resolution:** Task Resolution Chain.
**Status filter:** Todo

## Task Storage Mode

**MANDATORY READ:** Load `shared/references/environment_state_contract.md`, `shared/references/storage_mode_detection.md`, and `shared/references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider (`linear` | `file`).

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Load task** | `get_issue(task_id)` | `Read("docs/tasks/epics/.../tasks/T{NNN}-*.md")` |
| **Update status** | `save_issue(id, state)` | `Edit` the `**Status:**` line in file |
| **Kanban** | Updated by Linear sync | Must update `kanban_board.md` manually |

**File Mode status format:**
```markdown
## Status
**Status:** In Progress | **Priority:** High | **Estimate:** 4h
```

**MANDATORY READ:** Load `shared/references/mcp_tool_preferences.md` and `shared/references/mcp_integration_patterns.md` — use hex-line MCP for code files when available and hex-graph for semantic edit-risk questions.

## Mode Detection

Detect operating mode at startup:

**Plan Mode Active:**
- Steps 1-2: Load task context (read-only, OK in plan mode)
- Generate EXECUTION PLAN (files to create/modify, approach) → write to plan file
- Call ExitPlanMode → STOP. Do NOT implement.
- Steps 3-6: After approval → execute implementation

**Normal Mode:**
- Steps 1-6: Standard workflow without stopping

## Progress Tracking with TodoWrite

When operating in any mode, skill MUST create detailed todo checklist tracking ALL steps.

**Rules:**
1. Create todos IMMEDIATELY before Step 1
2. Each workflow step = separate todo item; implementation step gets sub-items
3. Mark `in_progress` before starting step, `completed` after finishing

**Todo Template (10 items):**

```
Step 1: Resolve taskId
  - Resolve via args / Story context / kanban / AskUserQuestion (Todo filter)

Step 2: Load Context
  - Fetch full task description + linked guides/manuals/ADRs

Step 2b: Goal Articulation Gate
  - Complete 4 questions from shared/references/goal_articulation_gate.md (<=25 tokens each)

Step 2c: Implementation Blueprint
  - From task "Affected Components": extract file paths (Glob/Grep to find actual paths)
  - Read each file (or key sections) to understand current structure
  - IF modifying existing code in supported languages: `index_project(path=project_root)` once, then use `find_symbols` / `inspect_symbol` for exact symbol identity and `analyze_edit_region` before editing non-trivial ranges
  - Output:
    ## Implementation Blueprint: {taskId}
    **Files to create:** [list with brief purpose]
    **Files to modify:** [list with what changes]
    **Change order (dependencies first):**
    1. {file} — {what and why first}
    2. {file} — {depends on step 1}
    **Risks:** {shared files with parallel tasks, if any}
  - Scope: ONLY files of this task. Do not analyze other tasks.

Step 3: Start Work
  - Set task to In Progress, update kanban

Step 4: Implement
  - 4a Pattern Reuse: IF creating new file/utility, Grep src/ for existing similar patterns
    (error handlers, validators, HTTP wrappers, config loaders). Reuse if found.
  - 4b Follow task plan/AC, apply KISS/YAGNI
  - 4c Architecture Guard: IF creating service function: (1) 3+ side-effect categories in **leaf** function → split (EXCEPT orchestrator functions that delegate sequentially — these are expected to have 3+ categories);
    (2) get_*/find_*/check_* naming → verify no hidden writes; (3) 3+ service imports in **leaf** function → flatten (orchestrator imports are expected)
    (4) **Frontend Guard (conditional):** IF affected files include `.tsx/.vue/.svelte/.html/.css` → **MANDATORY READ:** `shared/references/frontend_design_guide.md`. Load project's design_guidelines.md if exists (design tokens source of truth). Verify: one composition per viewport; max 2 typefaces + 1 accent color; cards only when interaction requires; motion max 2-3 purposeful; WCAG 2.1 AA contrast (4.5:1 text, 3:1 UI elements)
  - Update docs and existing tests if impacted
  - Execute verify: methods from task AC (test/command/inspect)

Step 5: Quality
  - Run typecheck and lint (or project equivalents)

Step 6: Finish
  - Set task to To Review, update kanban
  - Add summary comment (changes, tests, docs)
```

## Workflow (concise)
1) **Resolve taskId:** Run Task Resolution Chain per guide (status filter: [Todo]).
2) **Load context:** Fetch full task description (Linear: get_issue; File: Read task file); read linked guides/manuals/ADRs/research; auto-discover team/config if needed.
2b) **Goal gate:** **MANDATORY READ:** `shared/references/goal_articulation_gate.md` — Complete the 4-question gate (<=25 tokens each). State REAL GOAL (deliverable as subject), DONE LOOKS LIKE, NOT THE GOAL, INVARIANTS & HIDDEN CONSTRAINTS.
2c) **Implementation Blueprint:** From task "Affected Components", find actual file paths via Glob/Grep or `inspect_path`. Read key sections of each file. If task changes existing code in supported languages, build graph context once (`index_project`) and use `find_symbols` / `inspect_symbol` for exact symbol identity plus `analyze_edit_region` before editing non-trivial ranges. Output structured plan: files to create/modify, change order (dependencies first), risks (shared files with parallel tasks, external callers, public API surfaces). Scope: this task only.
3) **Start work:** Update this task to In Progress (Linear: update_issue; File: Edit status line); move it in kanban (keep Epic/Story indent).
4) **Implement (with verification loop):** **Before writing new utilities/handlers**, Grep `src/` for existing patterns (error handling, validation, config access). Reuse if found; if not reusable, document rationale in code comment. For edits to existing functions, classes, routes, or middleware, run `analyze_edit_region` first and account for external callers, clone siblings, downstream flow, and public API risk. Follow checkboxes/plan; keep it simple; avoid hardcoded values; reuse existing components; update docs noted in Affected Components; update existing tests if impacted (no new tests here). Before creating service functions, apply Architecture Guard (cascade depth, interface honesty, flat orchestration; for frontend files: **MANDATORY READ** `shared/references/frontend_design_guide.md`, load design_guidelines.md if exists, verify composition/typography/WCAG rules). After implementation, execute `verify:` methods from task AC: test → run specified test; command → execute and check output; inspect → verify file/content exists. If any verify fails → fix before proceeding.
5) **Quality:** Run typecheck and lint (or project equivalents); ensure instructions in Existing Code Impact are addressed.
6) **Finish:** Mark task To Review (Linear: update_issue; File: Edit status line); update kanban to To Review; add summary comment (what changed, tests run, docs touched).

## Pre-Submission Checklist

**Context:** Self-assessment before To Review reduces review round-trips and catches obvious issues early.

**MANDATORY READ:** Load `shared/references/code_efficiency_criterion.md` — self-check before submission.

Before setting To Review, verify all items:

| # | Check | Verify |
|---|-------|--------|
| 0 | **AC verified** | Each AC `verify:` method executed with pass evidence |
| 1 | **Approach alignment** | Implementation matches Story Technical Approach |
| 2 | **Clean code** | No dead code, no backward-compat shims, unused imports removed |
| 3 | **Config hygiene** | No hardcoded creds/URLs/magic numbers |
| 4 | **Docs updated** | Affected Components docs reflect changes |
| 5 | **Tests pass** | Existing tests still pass after changes |
| 6 | **Pattern reuse** | New utilities checked against existing codebase; no duplicate patterns introduced |
| 7 | **Architecture guard** | Cascade depth <= 2 (leaf functions); no hidden writes in read-named functions; no service chains >= 3 in leaf functions (orchestrator imports exempt). Frontend files: composition, typography, WCAG per `shared/references/frontend_design_guide.md` |
| 8 | **Destructive op safety** | If task has "Destructive Operation Safety" section: (1) backup step executed/planned before destructive code, (2) rollback mechanism exists in code, (3) environment guard present, (4) preview/dry-run evidence attached or referenced |
| 9 | **Code efficiency** | No unnecessary intermediates, verbose patterns replaced by language idioms, no boilerplate framework handles (per `shared/references/code_efficiency_criterion.md`) |

**MANDATORY READ:** Load `shared/references/destructive_operation_safety.md` for severity classification and safety requirements.

**HITL Gate:** IF task severity = CRITICAL (per destructive_operation_safety.md loaded above): Use `AskUserQuestion` to confirm before marking To Review: "Task contains CRITICAL destructive operation: {operation}. Backup plan: {plan}. Proceed?" Do NOT mark To Review until user confirms.

**If any check fails:** Fix before setting To Review. Do not rely on reviewer to catch preventable issues.

## Critical Rules
- Single-task updates only; no bulk status changes.
- Keep language of the task (EN/RU) in edits/comments.
- No code snippets in the description; code lives in repo, not in Linear.
- No new test creation; only update existing tests if required.
- Preserve Foundation-First ordering from orchestrator; do not reorder tasks.
- **Do NOT commit.** Leave all changes uncommitted — the reviewer reviews and commits.
- Before non-trivial edits to existing code, use graph impact evidence when available instead of guessing blast radius from file names alone.

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`, `shared/references/worker_runtime_contract.md`, `shared/references/task_worker_runtime_contract.md`

Shared contract:
- emit `summary_kind=task-status`
- standalone mode omits `runId` and `summaryArtifactPath`
- managed mode passes both `runId` and exact `summaryArtifactPath` before the worker writes its validated summary

## Definition of Done
- [ ] Task selected and set to In Progress; kanban updated accordingly.
- [ ] Guides/manuals/ADRs/research read; approach aligned with task Technical Approach.
- [ ] Implementation completed per plan/AC; each AC `verify:` method executed with pass evidence.
- [ ] Docs and impacted tests updated.
- [ ] Typecheck and lint passed (or project quality commands) with evidence in comment.
- [ ] Task set to To Review; kanban moved to To Review; summary comment added.
- [ ] Runtime summary artifact written to the shared task-status location.

## Reference Files
- **Environment state:** `shared/references/environment_state_contract.md`
- **Storage mode operations:** `shared/references/storage_mode_detection.md`
- Guides/manuals/ADRs/research: `docs/guides/`, `docs/manuals/`, `docs/adrs/`, `docs/research/`
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
