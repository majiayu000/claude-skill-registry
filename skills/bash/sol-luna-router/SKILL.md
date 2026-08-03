---
name: sol-luna-router
description: Route coding work so GPT-5.6 Sol remains the commander and reviewer while a separate GPT-5.6 Luna Max Codex CLI session performs concrete implementation. Use when the user asks for Sol to direct, plan, supervise, or review work done by Luna Max; when native Sol-to-Luna subagent spawning is unavailable or incompatible; or when a task needs an auditable plan, bounded worker ownership, verification, and review loop.
---

# Sol-Luna Router

Keep Sol responsible for decisions and Luna Max responsible for implementation. Use the bundled
runner instead of native `spawn_agent`; current Sol and Luna releases can select different
multi-agent backends.

## Boundaries

- Treat the current Sol thread as commander and reviewer. Do not edit target product files from
  this thread.
- Delegate concrete implementation, fixes, and worker-owned test changes to Luna Max.
- Allow only one write-capable Luna worker in a worktree at a time. Parallelize read-only work, or
  use isolated worktrees with explicit, disjoint file ownership.
- Keep the parent approval and sandbox boundary intact. Never add bypass, full-access, force-push,
  credential, or secret-handling flags.
- Stop after three failed correction cycles on the same root cause and reassess the hypothesis.
- Never claim completion from the worker summary alone. Verify from the current session.

## Workflow

### 1. Preflight

1. Confirm the target working directory and resolve its Git root.
2. Inspect dirty and untracked state without modifying it. Preserve user changes.
3. Read applicable `AGENTS.md` files and repository verification commands.
4. State the goal, constraints, allowed file ownership, done-when conditions, and test commands.
5. If the task is ambiguous enough to change architecture or scope, clarify before delegation.

### 2. Prepare the worker task

Write a temporary UTF-8 task file outside the target repository. Include only task-local context:

```text
Role: implementation worker.
Objective: <one bounded outcome>
Target repository: <absolute path>
Allowed files: <explicit paths or one narrow subtree>
Do not touch: <user changes and out-of-scope paths>
Constraints: <applicable requirements>
Reproduction or evidence: <fresh evidence>
Done when: <observable conditions>
Verification: <repository commands to run>
Return: root cause, changed files, commands with outcomes, and remaining risks.
```

Do not leak an intended patch or diagnosis when Luna must independently determine the root cause.

### 3. Run Luna Max

Run the bundled script with an absolute target directory and task-file path:

```bash
python3 <skill-dir>/scripts/run_luna_worker.py run \
  --cwd /absolute/path/to/repo \
  --prompt-file /absolute/path/to/task.md \
  --sandbox workspace-write
```

The script fixes the worker to `gpt-5.6-luna` with `model_reasoning_effort="max"`, disables
native multi-agent tools for the worker, invokes Codex without a shell, and returns one JSON
object containing `thread_id`, `final_response`, usage, and repository metadata.

Use `--allow-non-git` only when the user explicitly wants work outside a Git repository. Use
`--events-file /absolute/path/events.jsonl` only when a durable raw trace is needed.

### 4. Verify and review

1. Inspect the actual diff and changed-file list. Reject out-of-ownership edits.
2. Run the repository's required build or type-check command in the current session.
3. Run the required tests in the current session. Never weaken assertions or test infrastructure.
4. Review correctness, security, data integrity, error handling, and missing coverage.
5. If everything passes, summarize the result and cite fresh verification output.

### 5. Request a correction

When verification or Sol review finds an actionable defect, write a new temporary prompt containing
the exact failure evidence and resume the same worker thread:

```bash
python3 <skill-dir>/scripts/run_luna_worker.py resume \
  --cwd /absolute/path/to/repo \
  --thread-id <thread_id> \
  --prompt-file /absolute/path/to/correction.md
```

Repeat verification after every correction. Do not open a new worker thread unless the previous
thread is unavailable or the task has materially changed.

## Failure handling

- If the runner reports an incompatible or unavailable model, stop and report the exact error.
- If Luna requests broader file ownership, network access, or permissions, return the request to
  the user or revise the plan; do not grant it silently.
- If JSONL is malformed, the process exits nonzero, or the final response is missing, treat the
  worker run as failed.
- If unrelated user changes block safe verification, report the boundary instead of reverting them.
