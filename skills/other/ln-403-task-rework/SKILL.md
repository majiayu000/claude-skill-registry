---
name: ln-403-task-rework
description: "Fixes tasks in To Rework by applying reviewer feedback, then returns to To Review. Use when task was rejected during review."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-line__outline, mcp__hex-line__read_file, mcp__hex-line__edit_file, mcp__hex-line__write_file, mcp__hex-line__verify, mcp__hex-line__changes, mcp__hex-line__inspect_path
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Task Rework Executor

**Type:** L3 Worker

Executes rework for a single task marked To Rework and hands it back for review.

## Purpose & Scope
- Load full task, reviewer comments, and parent Story; understand requested changes.
- Apply fixes per feedback, keep KISS/YAGNI, and align with guides/Technical Approach.
- Update only this task: To Rework -> In Progress -> To Review; no other tasks touched.

**Hex-line acceleration (if available):** Use `outline(file_path)` before reading large code files. Use `read_file()` for discovery and `read_file(edit_ready=true, verbosity="full")` before any edit that needs `revision` and checksums. After edits: `edit_file(base_revision=rev)` → `verify(checksums)`. Use `changes()` to show what was fixed.
## Inputs

Use `read_file()` and `edit_file()` as the primary path for code/config/script/test files during rework. Keep `read_file()` discovery-first by default; request `edit_ready=true, verbosity="full"` only when you are about to reuse its revision/checksum protocol. Built-in Read/Edit are fallback only when hex-line is unavailable.

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `taskId` | Yes | args, parent Story, kanban, user | Task to rework |

**Resolution:** Task Resolution Chain.
**Status filter:** To Rework

## Task Storage Mode

**MANDATORY READ:** Load `references/environment_state_contract.md`, `references/storage_mode_detection.md`, `references/tracker_provider_contract.md`, and `references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider (`linear` | `github` | `file`). Operations stay provider-agnostic in this skill — see `references/tracker_provider_contract.md` for the canonical operation set and `provider_*.md` for transport binding.

Tracker operations used by this skill: `getTask`, `getStory`, `listComments`, `updateStatus` (To Rework → In Progress → To Review), `addComment`. Transport per provider lives in `references/provider_file.md, references/provider_github.md, references/provider_linear.md`.

**MANDATORY READ:** Load `references/mcp_tool_preferences.md` — ALWAYS use hex-line MCP for code files when available. No fallback to standard Read/Edit unless hex-line is down.

## Workflow (concise)
1) **Resolve taskId:** Run Task Resolution Chain per guide (status filter: [To Rework]).
2) **Load task:** Read task and review notes via the configured tracker provider (`getTask`, `listComments`); fetch parent Story via `getStory`.
2b) **Goal gate:** **MANDATORY READ:** Load `references/goal_articulation_gate.md` — State REAL GOAL of this rework (what was actually broken, not "apply feedback"). Combine with 5 Whys (`references/problem_solving.md`) to ensure root cause is articulated alongside the rework goal. NOT THE GOAL: a superficial patch that addresses the symptom, not the cause.
3) **Plan fixes:** Map each comment to an action; confirm no new scope added.
4) **Implement:** **MANDATORY READ:** Load `references/code_efficiency_criterion.md` — Follow task plan/checkboxes; address config/hardcoded issues; update docs/tests noted in Affected Components and Existing Code Impact. Before handoff, verify 3 efficiency self-checks.
5) **Quality:** Run typecheck/lint (or project equivalents); ensure fixes reflect guides/manuals/ADRs/research.
6) **Root Cause Analysis:** Ask "Why did the agent produce incorrect code?" Classify: missing context | wrong pattern | unclear AC | gap in docs/templates. If doc/template gap found → update the relevant file (guide, template, CLAUDE.md) to prevent recurrence.
7) **Handoff:** Set task to To Review via the configured tracker provider (`updateStatus`); move it in kanban; add summary comment referencing resolved feedback + root cause classification.

## Critical Rules
- Single-task only; never bulk update.
- Do not mark Done; only To Review (the reviewer decides Done).
- Keep language (EN/RU) consistent with task.
- No new tests/tasks created here; only update existing tests if impacted.
- **Do NOT commit.** Leave all changes uncommitted — the reviewer reviews and commits.

## Runtime Summary Artifact

**MANDATORY READ:** Load `references/coordinator_summary_contract.md`, `references/worker_runtime_contract.md`, `references/task_worker_runtime_contract.md`

Shared contract:
- emit `summary_kind=task-status`
- standalone mode omits `runId` and `summaryArtifactPath`
- managed mode passes both `runId` and exact `summaryArtifactPath` before the worker writes its validated summary

**Monitor (2.1.98+):** When verification commands expected >30s, use `Monitor`. Fallback: `Bash(run_in_background=true)`.

## Definition of Done
- [ ] Task and review feedback fully read; actions mapped.
- [ ] Fixes applied; docs/tests updated as required.
- [ ] Quality checks passed (typecheck/lint or project standards).
- [ ] Root cause classified (missing context | wrong pattern | unclear AC | doc gap); doc/template updated if gap found.
- [ ] Status set to To Review; kanban updated; summary comment with fixed items + root cause.
- [ ] Runtime summary artifact written to the shared task-status location.

## Reference Files
- **Environment state:** `references/environment_state_contract.md`
- **Storage mode operations:** `references/storage_mode_detection.md`
- **[MANDATORY] Problem-solving approach:** `references/problem_solving.md`
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
