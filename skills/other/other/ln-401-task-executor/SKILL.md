---
name: ln-401-task-executor
description: "Executes implementation tasks through Todo, In Progress, To Review. Use when task needs coding with KISS/YAGNI. Not for test tasks."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-line__outline, mcp__hex-line__read_file, mcp__hex-line__edit_file, mcp__hex-line__write_file, mcp__hex-line__verify, mcp__hex-line__changes, mcp__hex-line__inspect_path, mcp__hex-graph__index_project, mcp__hex-graph__find_symbols, mcp__hex-graph__inspect_symbol, mcp__hex-graph__analyze_edit_region
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Implementation Task Executor

**Type:** L3 Worker

Executes a single implementation (or refactor) task from Todo to To Review using the task description and linked guides.

## Purpose & Scope
- Handle one selected task only; never touch other tasks.
- Follow task Technical Approach/plan/AC; apply KISS/YAGNI and guide patterns.
- Update tracker/kanban for this task: Todo -> In Progress -> To Review.
- Run typecheck/lint; update docs/tests/config per task instructions.
- Not for test tasks (label "tests" goes to ln-404-test-executor).

**Hex MCP acceleration (if available):** Use narrow `inspect_path(path=<relevant dir>)` and `outline(file_path)` before reading large code files; avoid repo-root wildcard inventories unless you intentionally need one. Use `grep_search(output_mode="summary")` first for search/discovery, then escalate to `output_mode="content", edit_ready=true` only when you need canonical hunks for follow-up edits; use `allow_large_output=true` only as an explicit last resort. Use `read_file()` in discovery mode for structure and targeted ranges; when you need `revision` and checksums for a follow-up edit, refresh that file with `read_file(edit_ready=true, verbosity="full")` before `edit_file()`. For edits to existing code, run `index_project(path=project_root)` once and use `analyze_edit_region(...)` before non-trivial edits. After edits: `edit_file(base_revision=rev)` -> `verify(checksums)`. Before handoff: `changes()` to review diff.
## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `taskId` | Yes | args, parent Story, kanban, user | Task to execute |

**Resolution:** Task Resolution Chain.
**Status filter:** Todo

## Task Storage Mode

**MANDATORY READ:** Load `references/environment_state_contract.md`, `references/storage_mode_detection.md`, `references/tracker_provider_contract.md`, `references/provider_file.md`, and `references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider (`linear` | `github` | `file`). Operations stay provider-agnostic in this skill — see `references/tracker_provider_contract.md` for the canonical operation set and `provider_*.md` for transport binding.


Tool policy: follow host AGENTS.md MCP preferences; load `references/mcp_tool_preferences.md` and `references/mcp_integration_patterns.md` only when host policy is absent or MCP behavior is unclear. — use hex-line MCP for code files when available and hex-graph for semantic edit-risk questions.

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
  - Complete 4 questions from references/goal_articulation_gate.md (<=25 tokens each)

Step 2c: Implementation Blueprint
  - From task "Affected Components": extract file paths (Glob/Grep or narrow `inspect_path(path=<component dir>)` to find actual paths)
  - Read each file (or key sections) to understand current structure
  - IF modifying existing code in supported languages: `index_project(path=project_root)` once, then use path-scoped `find_symbols` / `inspect_symbol` for exact symbol identity and `analyze_edit_region` before editing non-trivial ranges
  - IF `find_symbols` returns `partial ... truncated=1` or a broad candidate set: refine to `name + file` or `workspace_qualified_name` before planning from it
  - Output:
    ## Implementation Blueprint: {taskId}
    **Files to create:** [list with brief purpose]
    **Files to modify:** [list with what changes]
    **Change order (dependencies first):**
    1. {file} — {what and why first}
    2. {file} — {depends on step 1}
    **Risks:** {shared files with parallel tasks, if any}
  - Scope: ONLY files of this task. Do not analyze other tasks.

  - **Checkpoint:** Emit PHASE_3 checkpoint with structured `blueprint` payload:
    `{ "blueprint": { "change_order": [{ "file": "...", "action": "create|modify", "reason": "..." }] } }`
    Guard blocks PHASE_4 if blueprint is missing from the checkpoint.

Step 3: Start Work
  - Set task to In Progress, update kanban

Step 4: Implement
  - 4a Pattern Reuse: IF creating new file/utility, Grep src/ for existing similar patterns
    (error handlers, validators, HTTP wrappers, config loaders). Reuse if found.
  - 4b Follow task plan/AC, apply KISS/YAGNI
  - 4c Architecture Guard: IF creating service function: (1) 3+ side-effect categories in **leaf** function → split (EXCEPT orchestrator functions that delegate sequentially — these are expected to have 3+ categories);
    (2) get_*/find_*/check_* naming → verify no hidden writes; (3) 3+ service imports in **leaf** function → flatten (orchestrator imports are expected)
    (4) **Frontend Guard (conditional):** IF affected files include `.tsx/.vue/.svelte/.html/.css` → **MANDATORY READ:** Load `references/frontend_design_guide.md`. Load project's design_guidelines.md if exists (design tokens source of truth). Verify: one composition per viewport; max 2 typefaces + 1 accent color; cards only when interaction requires; motion max 2-3 purposeful; WCAG 2.1 AA contrast (4.5:1 text, 3:1 UI elements)
  - Update docs and existing tests if impacted
  - Execute verify: methods from task AC (test/command/inspect)

Step 5: Quality
  - Run typecheck and lint (or project equivalents)
  - 5b Blueprint Completion: compare actual changes to blueprint; emit blueprint_status in PHASE_6 checkpoint

Step 6: Finish
  - Set task to To Review, update kanban
  - Add summary comment (changes, tests, docs)
```

## Workflow (concise)
1) **Resolve taskId:** Run Task Resolution Chain per guide (status filter: [Todo]).
2) **Load context:** Fetch full task description via the configured tracker provider (`getTask`); read linked guides/manuals/ADRs/research; auto-discover team/config if needed.
2b) **Goal gate:** **MANDATORY READ:** Load `references/goal_articulation_gate.md` — Complete the 4-question gate (<=25 tokens each). State REAL GOAL (deliverable as subject), DONE LOOKS LIKE, NOT THE GOAL, INVARIANTS & HIDDEN CONSTRAINTS.
2c) **Implementation Blueprint:** From task "Affected Components", find actual file paths via Glob/Grep or narrow `inspect_path(path=<component dir>)`. Read key sections of each file. If task changes existing code in supported languages, build graph context once (`index_project`) and use path-scoped `find_symbols` / `inspect_symbol` for exact symbol identity plus `analyze_edit_region` before editing non-trivial ranges. If symbol discovery is truncated, refine to `name + file` or `workspace_qualified_name` before planning from it. Output structured plan: files to create/modify, change order (dependencies first), risks (shared files with parallel tasks, external callers, public API surfaces). Scope: this task only.
3) **Start work:** Update this task to In Progress via the configured tracker provider (`updateStatus`); move it in kanban (keep Epic/Story indent).
4) **Implement (with verification loop):** **Before writing new utilities/handlers**, Grep `src/` for existing patterns (error handling, validation, config access). Reuse if found; if not reusable, document rationale in code comment. For edits to existing functions, classes, routes, or middleware, run `analyze_edit_region` first and account for external callers, clone siblings, downstream flow, and public API risk. Follow checkboxes/plan; keep it simple; avoid hardcoded values; reuse existing components; update docs noted in Affected Components; update existing tests if impacted (no new tests here). Before creating service functions, apply Architecture Guard (cascade depth, interface honesty, flat orchestration; for frontend files: **MANDATORY READ** `references/frontend_design_guide.md`, load design_guidelines.md if exists, verify composition/typography/WCAG rules). After implementation, execute `verify:` methods from task AC: test → run specified test; command → execute and check output; inspect → verify file/content exists. If any verify fails → fix before proceeding.
5) **Quality:** Run typecheck and lint (or project equivalents); ensure instructions in Existing Code Impact are addressed. **Blueprint Completion:** compare actual changes against blueprint from Step 2c — for each planned file mark completed or skipped (with justification), for each unplanned file mark added (with justification). Emit PHASE_6 checkpoint: `{ "blueprint_status": { "planned_count": N, "completed": [...], "skipped": [{"file":"...","justification":"..."}], "added": [{"file":"...","justification":"..."}], "completion_pct": N } }`. Guard blocks PHASE_7 if missing.
6) **Finish:** Mark task To Review via the configured tracker provider (`updateStatus`); update kanban to To Review; add summary comment (what changed, tests run, docs touched).

## Pre-Submission Checklist

**Context:** Self-assessment before To Review reduces review round-trips and catches obvious issues early.

**MANDATORY READ:** Load `references/code_efficiency_criterion.md` — self-check before submission.

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
| 7 | **Architecture guard** | Cascade depth <= 2 (leaf functions); no hidden writes in read-named functions; no service chains >= 3 in leaf functions (orchestrator imports exempt). Frontend files: composition, typography, WCAG per `references/frontend_design_guide.md` |
| 8 | **Destructive op safety** | If task has "Destructive Operation Safety" section: (1) backup step executed/planned before destructive code, (2) rollback mechanism exists in code, (3) environment guard present, (4) preview/dry-run evidence attached or referenced |
| 9 | **Code efficiency** | No unnecessary intermediates, verbose patterns replaced by language idioms, no boilerplate framework handles (per `references/code_efficiency_criterion.md`) |
| 10 | **Blueprint complete** | All blueprint items completed or skipped with justification; `blueprint_status` emitted in PHASE_6 checkpoint |

**MANDATORY READ:** Load `references/destructive_operation_safety.md` for severity classification and safety requirements.

**HITL Gate:** IF task severity = CRITICAL (per destructive_operation_safety.md loaded above): Use `AskUserQuestion` to confirm before marking To Review: "Task contains CRITICAL destructive operation: {operation}. Backup plan: {plan}. Proceed?" Do NOT mark To Review until user confirms.

**If any check fails:** Fix before setting To Review. Do not rely on reviewer to catch preventable issues.

## Critical Rules
- Single-task updates only; no bulk status changes.
- Keep language of the task (EN/RU) in edits/comments.
- No code snippets in the description; code lives in repo, not in the tracker description.
- No new test creation; only update existing tests if required.
- Preserve Foundation-First ordering from orchestrator; do not reorder tasks.
- **Do NOT commit.** Leave all changes uncommitted — the reviewer reviews and commits.
- Before non-trivial edits to existing code, use graph impact evidence when available instead of guessing blast radius from file names alone.

## Runtime Summary Artifact

**MANDATORY READ:** Load `references/coordinator_summary_contract.md`, `references/worker_runtime_contract.md`, `references/task_worker_runtime_contract.md`

Shared contract:
- emit `summary_kind=task-status`
- standalone mode omits `runId` and `summaryArtifactPath`
- managed mode passes both `runId` and exact `summaryArtifactPath` before the worker writes its validated summary

**Monitor (2.1.98+):** When verification commands expected >30s, use `Monitor`. Fallback: `Bash(run_in_background=true)`.

## Definition of Done
- [ ] Task selected and set to In Progress; kanban updated accordingly.
- [ ] Guides/manuals/ADRs/research read; approach aligned with task Technical Approach.
- [ ] Implementation completed per plan/AC; each AC `verify:` method executed with pass evidence.
- [ ] Docs and impacted tests updated.
- [ ] Typecheck and lint passed (or project quality commands) with evidence in comment.
- [ ] Task set to To Review; kanban moved to To Review; summary comment added.
- [ ] Runtime summary artifact written to the shared task-status location.

## Reference Files
- **Environment state:** `references/environment_state_contract.md`
- **Storage mode operations:** `references/storage_mode_detection.md`
- Guides/manuals/ADRs/research: `docs/guides/`, `docs/manuals/`, `docs/adrs/`, `docs/research/`
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
