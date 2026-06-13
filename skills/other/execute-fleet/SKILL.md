---
name: execute-fleet
description: >-
  Phase execution skill for licensed Atlas Fleet runs. Use when HANDOFF has
  selected Atlas Fleet and the project should be executed across isolated
  launcher worktrees with inbox-based result collection, verified CDD cards,
  sequential integration merges, and one final PR.
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Skill
  - ToolSearch
  - mcp__atlas-engine
  - mcp__plugin_prd_go
  - mcp__plugin_prd-taskmaster_go
  - mcp__plugin_atlas-go_go
---

# execute-fleet

Atlas Fleet is the premium parallel sibling of `execute-task`. It keeps the
same proof discipline, but the orchestrator owns the scoreboard while workers
only build inside isolated worktrees.

## Hard Gates

Before the first wave, all gates must pass. If any gate fails, report the gap
and stop; do not fall back to solo execution from inside this skill.

1. `mcp__plugin_prd_go__detect_capabilities()` reports
   `tier: "premium"` and atlas-launcher MCP registration/aliveness.
2. `mcp__atlas-launcher__inbox_read` is callable for this session.
3. `.taskmaster/tasks/tasks.json` exists.
4. `.taskmaster/reports/task-complexity-report.json` exists.
5. `git status --short` is empty. Fleet starts only from a committed base.
6. The integration branch policy is clear: use `fleet-integration`; main is never auto-touched.

**SOLE-WRITER RULE:** only this orchestrator writes
`.taskmaster/tasks/tasks.json` and `.atlas-ai/state/pipeline.json`. Workers
must never edit those files. The orchestrator may update task state only
through TaskMaster or the plugin pipeline MCP, and only after verification.

## Wave Loop

Repeat until no runnable tasks remain:

1. Call `mcp__plugin_prd_go__compute_fleet_waves(concurrency=<N>, tag=<tag>)`.
   Use the returned frontier as the only dispatch source. If it reports a
   deadlock, render status, mark the blocked set, and stop dispatching those
   tasks.
2. For each chunk in the current wave, spawn exactly one worker:
   `mcp__atlas-launcher__session_spawn(isolation="worktree", report_to=<this session>, model=<routing[task_id] model part>, prompt=<worker prompt>)`.
   **Model is NEVER left default**: `compute_fleet_waves` returns a `routing`
   map (task id -> backend:model) from the capability ladder — Fable for the
   hardest/longest-running (frontier tier), down the cost-efficiency curve to
   haiku for trivial tasks. Pass the model part explicitly; non-claude backends
   require experimental_backends=true and the launcher backend param.
   The prompt must include the full task JSON inline; never tell workers to
   read shared `tasks.json`.
3. Inspect the spawn result. If `prompt_injected` is false, re-kick once with
   `mcp__atlas-launcher__session_send` using the same worker prompt, then
   confirm injection/readiness. If it is still false, treat that worker as
   failed and apply the retry policy below.
4. Render the fleet status view after the wave starts and after each wave
   transition.
5. Poll `mcp__atlas-launcher__inbox_read` for terminal worker messages. The
   only accepted terminal status vocabulary is `DONE`, `DONE_WITH_CONCERNS`,
   `NEEDS_CONTEXT`, or `BLOCKED`; any other terminal word is a protocol
   failure and counts as a worker failure.
6. On a completion message, verify the branch, never the narration:
   - The worker branch contains `.atlas-ai/cdd/task-<id>.json`.
   - No `.atlas-ai/evidence/` file in that branch contains a non-zero
     `Exit status N` line.
   - The branch changed only its own worktree scope and did not edit
     `.taskmaster/tasks/tasks.json` or `.atlas-ai/state/pipeline.json`.
7. Never mark a task done without the CDD card. Missing card means the worker
   did not satisfy the contract, regardless of any `DONE` message.
8. Merge verified worker branches into `fleet-integration` sequentially, one
   at a time. After each merge, run the checker/build gate expected for the
   project before merging the next branch.
9. Mark the task done only after the merge gate passes:
   `python3 script.py set-status --id <id> --status done`.
10. Recompute waves after every accepted merge. Do not keep dispatching from a
    stale frontier.

## Worker Prompt Template

Embed this template verbatim for each worker, replacing placeholders before
dispatch:

```text
WORKER_CONTRACT_ORCHESTRATOR_REPORT_TO
You are an Atlas Fleet worker. Your orchestrator is <ORCHESTRATOR_ID>. Report every question, blocker, and terminal result to <REPORT_TO_SESSION>.

WORKER_CONTRACT_FULL_TASK_JSON_INLINE
Your assigned task JSON is inline below. Treat this as the source of truth. Do not read shared .taskmaster/tasks/tasks.json.
<FULL_TASK_JSON>

WORKER_CONTRACT_WORKTREE_BRANCH
Work only in this isolated worktree and branch:
worktree: <WORKTREE_PATH>
branch: <WORKER_BRANCH>

WORKER_CONTRACT_CDD_CARD
Before reporting any terminal status, write this CDD card in your worktree: .atlas-ai/cdd/task-<id>.json. The card must list the checks you ran and the evidence paths that prove them. Evidence files under .atlas-ai/evidence/ must contain the FINAL verification run ONLY (one green run, one exit-status line) — intermediate TDD red runs go to .atlas-ai/logs/, never evidence/ (ship-check Gate 5 reads every Exit status line in evidence/ as final-state proof).

WORKER_CONTRACT_TERMINAL_STATUS
End with exactly one terminal status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED.
Report it via mcp__atlas-launcher__inbox_send(target_session=<REPORT_TO_SESSION>, message_type="task_handoff", payload=<JSON string with at least {"task_id": <id>, "status": "<terminal status>", "branch": "<worktree branch>", "cdd_card": ".atlas-ai/cdd/task-<id>.json"}>, sender_session=<your session name>). The launcher message_type allowlist is task_handoff | notification | data | request | heartbeat — terminal reports use task_handoff; the status lives INSIDE the payload JSON.

WORKER_CONTRACT_HARD_RULES
Hard rules: never edit .taskmaster/tasks/tasks.json or .atlas-ai/state/pipeline.json; never git push; commit only in your own worktree branch.

WORKER_CONTRACT_QUESTIONS_INBOX
Ask questions before building if context is missing: use mcp__atlas-launcher__inbox_send(target_session=<REPORT_TO_SESSION>, message_type="request", payload=<your question as a string>, sender_session=<your session name>). ("question"/"completion"/"blocker" are template intents, not runtime message types — see docs/INTEGRATION-prd-taskmaster.md in the atlas-launcher repo, contract v1.)
```

## Failure Paths

- Silent/dead worker: if there is no inbox message and the session is gone,
  re-queue the task ONCE with a fresh worker prompt. On the second failure,
  mark the task `BLOCKED` in the orchestrator scoreboard and continue with
  remaining tasks.
- `NEEDS_CONTEXT`: answer through `mcp__atlas-launcher__inbox_send`, then let
  the same worker continue. If it cannot continue, count it under the same
  retry cap.
- Worker `BLOCKED`: record the blocker, mark the task `BLOCKED`, and continue
  with independent tasks.
- Merge conflict: do not force. Do not resolve by guessing. Create a fix task
  that captures the conflict and continue with remaining non-conflicting work.
- Evidence failure: do not merge, do not mark done, and do not rewrite the
  worker's CDD card on their behalf.

## Status Rendering

After every wave transition, render the terminal status view with the UX-SPEC
grammar. Use model plus index names such as `claude-1`, `codex-1`, and
`claude-2`. Keep the gate line in plain English every time.

```text
┌─ atlas fleet ── wave 2 of 3 ──────────────── ▶ running 12m ┐
│  wave 1  ✓ merged     3 tasks · 18m · integration green    │
│  wave 2  ▶ running                                         │
│    claude-1   task 6  API endpoints      ▰▰▰▱  3/4         │
│    codex-1    task 7  UI components      ▰▰▱▱  2/4         │
│    claude-2   task 9  DB migrations      ✓ done — waiting  │
│  wave 3  ○ queued     4 tasks · starts when wave 2 merges  │
│                                                            │
│  Gate: a wave merges only after the checker approves it    │
│        and the integration branch builds green.            │
│                                                            │
│  watch:  atlas fleet status        logs: .atlas-ai/fleet/  │
└────────────────────────────────────────────────────────────┘
```

## Termination

When all waves are done, or all remaining tasks are `BLOCKED`, switch to
`fleet-integration` and run:

```bash
python3 skel/ship-check.py
```

If it exits non-zero, report the failing gate and stop. If it exits 0, emit
`SHIP_CHECK_OK` exactly once, then open one final PR from `fleet-integration`.
Do not print the token anywhere else. Do not merge the PR yourself.

## Non-Exits

This skill never kills the shell and never pushes. Halt conditions are reported
to the caller and, when relevant, to the launcher inbox.
