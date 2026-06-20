---
name: task-forest
description: Maintains a repo-local task forest or task DAG for the current workspace. Use when the user asks to initialize, update, close a session, summarize evolving project tasks, decide whether a new request is a global task or subtask, track task progress/history/deviations/todos, export a task graph HTML, or provide task data for gap-router/local-agent-control-room. Do not use for executing the tasks themselves.
---

# Task Forest

## Language Policy

Write skill instructions in English. When interacting with the user or generating task titles, node fields, proposals, reports, or exported user-facing content, use the user's language. Default to Chinese when the user's language is unknown.

## Role

Maintain repo-local task structure. Record long-running goals, subtasks, dependencies, progress, deviations, todos, and session history under the current workspace. Export an offline HTML view of the task graph.

## Portability

Resolve paths from the directory that contains this `SKILL.md`. Use the available Python command on the host (`python3`, `python`, or `py -3`). The scripts are intended for macOS, Windows, and Linux with Python 3 and the standard library. In portable builds, agents may set `COMPASS_AGENT_NAME` or `AGENT_NAME` when they want graph history to record the calling agent.

## Core Principles

1. Write task-forest data only through `scripts/task_forest.py`; never edit files under `.agent-workbench/task-forest/` directly.
2. The internal model is a DAG. The default presentation is a forest: one primary `child_of` parent per node, `contributes_to` for secondary ownership, and `depends_on` for execution prerequisites.
3. If user intent is unclear, apply `$task-clarifier` before task graph work. If intent is clear enough, present a proposal and wait for confirmation before applying it.
4. Keep unconfirmed assumptions in proposals. Write formal graph changes only after confirmation.
5. When execution diverges from the user's requirement, record a deviation and move related tasks to `review_needed` or wait for user confirmation.
6. Store canonical data in the current workspace at `.agent-workbench/task-forest/`. Store only lightweight registry data in the global SQLite index.
7. In concurrent sessions, read and write through the CLI so locking and stale-hash checks can run.
8. Treat HTML export as a primary product surface. Changes to the HTML template must satisfy `references/html-visualization-contract.md` and pass `scripts/validate_task_forest_export.py`.

## CLI

Resolve `<skill-dir>` to the directory that contains this `SKILL.md`. Use the available Python command for the host (`python3`, `python`, or `py -3`). Examples use `python3`; adapt only the Python executable name when needed.

```bash
python3 <skill-dir>/scripts/task_forest.py --help
```

The default workspace is the current working directory. To target a specific workspace:

```bash
python3 <skill-dir>/scripts/task_forest.py init \
  --workspace /path/to/repo
```

Common commands:

```bash
python3 <skill-dir>/scripts/task_forest.py init

python3 <skill-dir>/scripts/task_forest.py add-node \
  --kind global_task \
  --title "Maintain the local agent workbench" \
  --requirement "Task data stays inside the workspace" \
  --acceptance "The task graph can be exported to HTML"

python3 <skill-dir>/scripts/task_forest.py add-node \
  --title "Implement task graph HTML export" \
  --parent TF-0001 \
  --estimate 120 \
  --difficulty medium

python3 <skill-dir>/scripts/task_forest.py todo
python3 <skill-dir>/scripts/task_forest.py export
python3 <skill-dir>/scripts/task_forest.py validate
```

## Session Close Workflow

When the user asks to update the task forest, close the current session, or maintain the task list from the conversation:

1. Run `init` to ensure the data directory exists.
2. Run `list --json` and `todo --json` to read current nodes and open work.
3. Analyze the session and create candidate changes only: new nodes, node updates, edges, deprecations, deviations, or questions.
4. If the session goal is unclear, ask which goal this conversation mainly served.
5. If the goal is clear enough, show the proposal: where each new node goes, how it relates to existing tasks, and which fields would change.
6. Save the candidate changes as a proposal. Apply with `proposal-apply --yes` only after user confirmation.
7. After applying, run `validate` and `export`, inspect the HTML against `references/html-visualization-contract.md`, and tell the user the HTML path.

Proposal JSON fields and invariants live in `references/schema.md`. Complex session-close reasoning lives in `references/session-close-workflow.md`.

Read `references/goal-alignment.md` when judging how a task serves a global goal, whether it can achieve the user's purpose, or which candidate task plan to offer. Clarification methods come from `$task-clarifier`; task-forest owns graph meaning, candidate task structure, and proposal writes.

Read `references/node-types.md` only when adding or classifying nodes.

Concurrency and multi-session rules live in `references/concurrency.md`. Proposals store `base_graph_hash`; application rejects stale proposals by default. Use `--allow-stale` only after manual conflict review.

## Outputs And Integration

Exports are fixed at:

```text
.agent-workbench/task-forest/exports/task-forest.graph.json
.agent-workbench/task-forest/exports/task-forest.todos.json
.agent-workbench/task-forest/exports/task-forest.timeline.json
.agent-workbench/task-forest/exports/task-forest.html
```

`gap-router` and `local-agent-control-room` read these exports. They must leave canonical task-forest data unchanged. Field contracts live in `references/integration-contract.md`.

The CLI updates a lightweight global registry when possible during `init`, `export`, `validate`, `proposal-save`, and `proposal-apply`:

```text
~/.agent-workbench/agent-workbench.sqlite3
```

The registry stores workspace paths, task-forest paths, export paths, export hashes, node/edge/status counts, command status, and error summaries. It omits node bodies, edge bodies, history snapshots, HTML, proposal content, and full conversation summaries. Use `AGENT_WORKBENCH_DB` to set another registry path. Set `TASK_FOREST_DISABLE_GLOBAL_REGISTRY=1` to disable the global registry.

Full rebuild regression:

```bash
python3 <skill-dir>/scripts/validate_task_forest_export.py --skill-dir <skill-dir>
```

The validator creates a temporary workspace, initializes task-forest, builds a sample DAG with multiple states and edge types, runs `validate/export`, and checks exported JSON and HTML behavior.

## Boundaries

- Explicit invocation is the reliable way to run this skill at session end.
- Low-confidence goal inference must become a question or stay in a proposal.
- Prefer `deprecated` for removed tasks so history remains reviewable.
- Estimates must include confidence. Use `unknown` or low confidence when evidence is thin.
