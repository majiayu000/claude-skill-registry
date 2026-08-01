---
name: phx-full
description: Run a portable sequential plan-work-verify-review-compound lifecycle.
  Use optional generic workers only when the runtime supports them.
---
# Full Phoenix Feature Development

Run the portable lifecycle: discover → plan → work → verify → read-only review →
compound. The filesystem is the state machine; no task API or named orchestrator
is required.

## Usage

```text
/phx-full Add user authentication with magic links
/phx-full Background email jobs --max-cycles 5 --max-retries 2
```

If input is an existing `.claude/plans/*/plan.md`, do not re-plan. Ask for the
native `phx-work` workflow or execute its portable behavior in this session.
Defaults are `--max-cycles 10`, `--max-retries 3`, and `--max-blockers 5`.

## Lifecycle

1. **DISCOVERING** — inspect relevant code, tests, prior solutions, and optional
   Tidewave evidence. Tidewave is optional; local files, logs, and `mix` commands
   are the complete fallback. Record complexity and proposed depth, then wait for
   the user's plan/implementation gate. Never auto-select a path that bypasses it.
2. **PLANNING** — invoke the runtime's native `phx-plan` skill when available, or
   execute its portable research checklist and artifact format in this session.
   Require `.claude/plans/{slug}/plan.md`. Present it and wait for approval before
   implementation unless the user already explicitly authorized the full run.
3. **WORKING** — execute the plan sequentially. Task selection occurs only here.
   The full-run limits override any baseline workflow retry defaults. Before every
   attempt persist cycle, task retry, and blocker counters; if the next attempt
   exceeds a limit, do not run it. `--max-retries N` means at most N retries after
   the initial attempt (N+1 total attempts for that task). Mark `[BLOCKED]` and
   stop at `--max-blockers`.
4. **VERIFYING** — run `mix format --check-formatted`, compile with warnings as
   errors, focused tests during work, and the full relevant suite at this gate.
   A failed gate appends FAIL and returns to WORKING only within the cycle limit.
5. **REVIEWING** — invoke portable `phx-review`, or perform the same read-only,
   changed-file review sequentially. Generic workers are optional. Review never
   edits. Findings or failures become plan tasks and return to WORKING.
6. **COMPOUNDING** — only after verification and a clean/accepted review. Do not
   invoke `phx-compound`. Inline contract: write a solution artifact under
   `.claude/solutions/` only when the run produced a non-obvious, reusable learning,
   including problem, root cause, solution, and verification. Otherwise append
   `COMPOUNDING SKIPPED: no reusable learning` to progress. Never edit CLAUDE.md.

Track `INITIALIZING → DISCOVERING → PLANNING → WORKING → VERIFYING → REVIEWING →
COMPOUNDING → COMPLETED`, with `BLOCKED` reachable from every phase. A cycle is
one `WORKING → VERIFYING → REVIEWING` pass; increment and persist it before
entering VERIFYING. At `--max-cycles`, do not begin another pass: stop INCOMPLETE with remaining tasks,
failed evidence, and a concrete resume command for this runtime.

## Iron Laws

1. **Honor user gates** — discovery and plan approval are not automatic transitions.
2. **Never skip verification or the read-only review phase.**
3. **Only WORKING edits code**; review findings become explicit plan tasks.
4. **Respect every cycle, retry, and blocker limit; stop when exhausted.**
5. **Persist state before stopping** so plan checkboxes and progress evidence resume.
6. **Do not require hooks, MCP, named agents, background tasks, or a task UI.**

## Resume Ledger

`progress.md` is the sole state authority. It is append-only: never overwrite or
maintain a competing authoritative current-state record. Every event has monotonic
`seq`, `phase_visit`, `phase`, `cycle`, `task`, `task_attempt`, cumulative
`blockers`, `outcome`, and an `evidence` or `artifact` path. On resume, validate the
last valid event against evidence, plan checkboxes, artifacts, and git state, then
enter only its legal successor. Any WORKING edit after a VERIFYING or REVIEWING
pass invalidates both passes; the next legal phase is VERIFYING.

Completion requires all required plan tasks checked, no unresolved `[BLOCKED]`,
the latest VERIFYING PASS after the last edit, the latest accepted REVIEWING after
that verify, and COMPOUNDING passed or explicitly skipped.

## References

- `references/execution-steps.md` — portable phase gates and outputs
- `references/example-run.md` — example lifecycle
- `references/safety-recovery.md` — resume and blocker recovery
- `references/cycle-patterns.md` — bounded cycle patterns
