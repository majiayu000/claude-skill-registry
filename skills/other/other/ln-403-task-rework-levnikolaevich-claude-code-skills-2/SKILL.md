---
name: ln-403-task-rework
description: "Fixes tasks in To Rework by applying reviewer feedback, then returns to To Review. Use when task was rejected during review."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-line__outline, mcp__hex-line__read_file, mcp__hex-line__edit_file, mcp__hex-line__write_file, mcp__hex-line__verify, mcp__hex-line__changes, mcp__hex-line__inspect_path
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Task Rework Executor

**Type:** L3 Worker

Executes rework for a single task marked To Rework and hands it back for review.

## Purpose & Scope
- Load full task, reviewer comments, and parent Story; understand requested changes.
- Apply fixes per feedback, keep KISS/YAGNI, and align with guides/Technical Approach.
- Update only this task: To Rework -> In Progress -> To Review; no other tasks touched.

**Hex-line acceleration (if available):** Use `outline(path)` before reading large code files. Use `read_file()` for discovery and `read_file(edit_ready=true, verbosity="full")` before any edit that needs `revision` and checksums. After edits: `edit_file(base_revision=rev)` → `verify(checksums)`. Use `changes()` to show what was fixed.
## Inputs

Use `read_file()` and `edit_file()` as the primary path for code/config/script/test files during rework. Keep `read_file()` discovery-first by default; request `edit_ready=true, verbosity="full"` only when you are about to reuse its revision/checksum protocol. Built-in Read/Edit are fallback only when hex-line is unavailable.

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `taskId` | Yes | args, parent Story, kanban, user | Task to rework |

**Resolution:** Task Resolution Chain.
**Status filter:** To Rework

## Task Storage Mode

**MANDATORY READ:** Load `shared/references/environment_state_contract.md`, `shared/references/storage_mode_detection.md`, and `shared/references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider (`linear` | `file`).

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Load task** | `get_issue(task_id)` | `Read("docs/tasks/epics/.../tasks/T{NNN}-*.md")` |
| **Load review notes** | Linear comments | Review section in task file or kanban |
| **Update status** | `save_issue(id, state)` | `Edit` the `**Status:**` line in file |

**File Mode transitions:** To Rework → In Progress → To Review

**MANDATORY READ:** Load `shared/references/mcp_tool_preferences.md` — ALWAYS use hex-line MCP for code files when available. No fallback to standard Read/Edit unless hex-line is down.

## Workflow (concise)
1) **Resolve taskId:** Run Task Resolution Chain per guide (status filter: [To Rework]).
2) **Load task:** Read task (Linear: get_issue; File: Read task file), review notes, parent Story.
2b) **Goal gate:** **MANDATORY READ:** `shared/references/goal_articulation_gate.md` — State REAL GOAL of this rework (what was actually broken, not "apply feedback"). Combine with 5 Whys (`shared/references/problem_solving.md`) to ensure root cause is articulated alongside the rework goal. NOT THE GOAL: a superficial patch that addresses the symptom, not the cause.
3) **Plan fixes:** Map each comment to an action; confirm no new scope added.
4) **Implement:** **MANDATORY READ:** `shared/references/code_efficiency_criterion.md` — Follow task plan/checkboxes; address config/hardcoded issues; update docs/tests noted in Affected Components and Existing Code Impact. Before handoff, verify 3 efficiency self-checks.
5) **Quality:** Run typecheck/lint (or project equivalents); ensure fixes reflect guides/manuals/ADRs/research.
6) **Root Cause Analysis:** Ask "Why did the agent produce incorrect code?" Classify: missing context | wrong pattern | unclear AC | gap in docs/templates. If doc/template gap found → update the relevant file (guide, template, CLAUDE.md) to prevent recurrence.
7) **Handoff:** Set task to To Review (Linear: update_issue; File: Edit status line); move it in kanban; add summary comment referencing resolved feedback + root cause classification.

## Critical Rules
- Single-task only; never bulk update.
- Do not mark Done; only To Review (the reviewer decides Done).
- Keep language (EN/RU) consistent with task.
- No new tests/tasks created here; only update existing tests if impacted.
- **Do NOT commit.** Leave all changes uncommitted — the reviewer reviews and commits.

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`, `shared/references/worker_runtime_contract.md`, `shared/references/task_worker_runtime_contract.md`

Shared contract:
- emit `summary_kind=task-status`
- standalone mode omits `runId` and `summaryArtifactPath`
- managed mode passes both `runId` and exact `summaryArtifactPath` before the worker writes its validated summary

## Definition of Done
- [ ] Task and review feedback fully read; actions mapped.
- [ ] Fixes applied; docs/tests updated as required.
- [ ] Quality checks passed (typecheck/lint or project standards).
- [ ] Root cause classified (missing context | wrong pattern | unclear AC | doc gap); doc/template updated if gap found.
- [ ] Status set to To Review; kanban updated; summary comment with fixed items + root cause.
- [ ] Runtime summary artifact written to the shared task-status location.

## Reference Files
- **Environment state:** `shared/references/environment_state_contract.md`
- **Storage mode operations:** `shared/references/storage_mode_detection.md`
- **[MANDATORY] Problem-solving approach:** `shared/references/problem_solving.md`
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
