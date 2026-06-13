---
name: execute-task
description: >-
  Execute the next TaskMaster task using the implementation plan with CDD
  verification. Picks the next ready task, matches it to the plan step,
  implements via a dispatched subagent, verifies subtasks with evidence,
  marks the task done, and loops until every task is complete.

  Wraps the TaskMaster next -> in-progress -> done lifecycle with CDD
  GREEN / RED / BLUE verification and the plugin's triple-verification
  rule. Autonomous by design — no user prompts inside the loop.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Skill
  - Agent
  - ToolSearch
  - mcp__atlas-engine
  - mcp__plugin_prd_go
  - mcp__plugin_prd-taskmaster_go
  - mcp__plugin_atlas-go_go
---

# execute-task

The execution loop. Three sources converge:

- **Plan** (HOW) — `docs/superpowers/plans/*.md` produced by GENERATE
- **TaskMaster** (WHAT) — `.taskmaster/tasks/tasks.json` with
  dependencies and complexity scores
- **CDD** (PROOF) — acceptance cards per task, evidence-gated

execute-task is the single skill that runs the full build from "tasks are
ready" to SHIP_CHECK_OK. It is autonomous — no AskUserQuestion inside the
loop. Any gap that would require user input is surfaced through the recon
escalation ladder (step 11) or the inbox (steps 4 and 8), never via a modal
prompt.

## Entry

This skill is invoked either:

1. Directly by the user once HANDOFF has completed and a task-execution
   mode (A/B/C) has been dispatched, **or**
2. By the `prd-taskmaster` orchestrator when `current_phase` is `EXECUTE`.

On entry, confirm that:

- `.atlas-ai/state/pipeline.json` exists and records `phase: EXECUTE`
- `.taskmaster/tasks/tasks.json` exists with at least one ready task
- `.atlas-ai/customizations/system-prompt-template.md` is present (may be
  empty — absence is a setup bug, empty is fine)

If any of the above are missing, report the gap and halt. Do NOT attempt to
bootstrap the missing artifact from inside this loop — that is the
orchestrator's job.

## Cycle (per iteration)

Each pass through this cycle moves exactly one TaskMaster task from `pending`
to `done`. Do the 13 steps in order. Do not skip.

1. **Heartbeat check**: verify the execute-task heartbeat timer is running.
   If missing, register one via `CronCreate("execute-task-heartbeat", "* * * * *", "echo heartbeat")`.
   Abort the iteration if the timer cannot be created — a missing heartbeat
   means a missing stuck-session detector, and that is load-bearing.

2. **Inbox reconciliation**: read `.atlas-ai/state/pipeline.json`,
   `.taskmaster/tasks/tasks.json`, and the current TodoWrite list.
   Diff them. If the three are stale by more than 5 tasks (i.e. TodoWrite
   says 10 done but tasks.json says 3 done), report the diff and halt — do
   not paper over bookkeeping drift by silently reconciling.

3. **Pick next task**: run backend op `next` with the plugin's project-root
   pointer. Use exactly this invocation:

   ```bash
   python3 script.py next-task
   ```

   Parse the JSON result.
   - If no ready tasks and all tasks are `done`, run `.atlas-ai/ship-check.py`,
     emit SHIP_CHECK_OK on success, exit the loop.
   - If no ready tasks but pending tasks exist, the dependency graph is
     deadlocked — report and halt.

4. **Load plan step**: search for the matching task ID in this priority
   order, halting only after all three fail:

   1. `docs/superpowers/plans/*.md` (the superpowers GENERATE default output)
   2. `.taskmaster/docs/plan.md` (the prd-taskmaster HANDOFF default output,
      whose path is also recorded in
      `pipeline.json:phase_evidence.HANDOFF.plan_file_path`)
   3. Any custom path declared in
      `pipeline.json:phase_evidence.HANDOFF.plan_file_path` (in case
      a future handoff variant writes elsewhere)

   If none of the three contains the matching task ID, the task was
   invented downstream of the plan — mark the task `blocked`, inbox the
   parent orchestrator with `message_type="blocker"`, and continue to the
   next iteration.

   (Codified 2026-06-04 — yesterday's ai-human-tasker run had its plan at
   `.taskmaster/docs/plan.md` only, while this step previously read
   `docs/superpowers/plans/*.md` exclusively. The controller silently
   improvised; a cold-start successor would have hit the `blocked` path on
   every task.)

5. **Generate CDD card**: convert the task's `subtasks` field into a
   `testing_plan`. Each subtask becomes a verifiable check with a concrete
   evidence path (file, command output, or test name). Write the card to
   `.atlas-ai/cdd/task-<id>.json`. A task without subtasks is treated as a
   single RED card.

6. **Set in-progress**: run backend op `set-status` from the current project
   root:

   ```bash
   python3 script.py set-status --id <N> --status in-progress
   ```

   This flip is
   observable by watchers and anchors the iteration in TaskMaster itself.

7. **Dispatch implementer subagent** — NEVER in-session. The controller
   must:

   - Provide the FULL task text to the subagent. Never tell the subagent to
     "read tasks.json" — per spec §12, the controller serialises the task
     into the dispatch prompt.
   - Inject the plugin customisation block at `.atlas-ai/customizations/system-prompt-template.md`
     into the subagent's system prompt. If the file is empty, inject nothing
     and continue.
   - Tier the model by TaskMaster complexity score:
     - `1-4 fast` — use the fast tier (Haiku-class)
     - `5-7 standard` — use the standard tier (Sonnet-class)
     - `8-10 capable` — use the capable tier (Opus-class)
   - Wait for the subagent to return a terminal status: `DONE`,
     `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`.

   Rationale: complexity-tiered dispatch keeps the dollars-per-task curve
   sensible. A complexity-2 boilerplate task does not need Opus; a
   complexity-9 architectural task should not be given to Haiku.

8. **Route by status**: the subagent's return status drives the next move.

   - **DONE** — proceed to the spec gate, then the quality gate. If both
     pass, advance to step 9.
   - **DONE_WITH_CONCERNS** — the subagent completed but flagged concerns.
     Address each concern before advancing; re-dispatch if needed.
   - **NEEDS_CONTEXT** — the subagent requested more context. Provide the
     requested context and re-dispatch. Retry cap at 2 — if the subagent
     still returns NEEDS_CONTEXT after two re-dispatches, escalate via the
     recon ladder (step 11).
   - **BLOCKED** — the subagent cannot proceed. Try one model-tier upgrade
     first (e.g. standard -> capable). If still blocked, break the task
     into smaller subtasks via backend op `expand`
     (`python3 script.py expand --id <N>`). If still
     blocked, set status=blocked, inbox parent, halt this iteration.

   Do NOT invent new status values. The four above are the only terminal
   returns. Any other string from the subagent is a protocol violation and
   should be logged + treated as BLOCKED.

9. **Triple verification** — the plugin's core quality gate, per spec §11.4.
   Three independent checks must agree.

   **Hard exit-code gate (MANDATORY — bypasses agreement count).** Before
   invoking the three checkers, run `.atlas-ai/ship-check.py --dry-run`. If
   it reports any non-zero `Exit status N` in evidence files, the task
   FAILS regardless of how the agent narratives read. SHIP_CHECK_FAIL is
   NOT a warning. Narrative claiming the exit code is "expected" or
   "infrastructure noise" does NOT override this gate — write a separate
   `task-fix-N` to address the underlying failure instead. Override only
   via `--override SHIP_CHECK_OVERRIDE_ADMIN`, which is logged to
   `execute-log.jsonl` as an audit event. (Codified 2026-06-04 after T12
   in ai-human-tasker was marked DONE while `pnpm test` exited 1 with 11
   failing tests.)

   The three checks (run only if the hard gate passes):

   - Plugin-native check: evidence file count vs declared subtask count
     (from the CDD card in step 5). Missing evidence = fail.
   - `/doubt` skill — adversarial doubt sweep on the claimed completion.
   - `/validate` skill — deterministic validation pass (lint / tests / exit
     codes).
   - External `Opus subagent` sanity pass — asks a fresh subagent "would
     you merge this?" with the task spec + diff + evidence.

   3+ agree pass -> task passes. Disagreement -> halt this iteration,
   surface to inbox.

10. **Mark done + propagate state**:
    a. Run backend op `set-status` for the parent task:
       `python3 script.py set-status --id <N> --status done`.
    b. **Subtask writeback**: for each subtask `S` in `task.subtasks` whose
       evidence file (per the CDD card from step 5) exists, run
       `python3 script.py set-status --id <N>.<S> --status done`. Subtasks left
       `pending` while the parent is `done` are a data-integrity violation
       that breaks any tool computing progress from subtask state.
       (Codified 2026-06-04 — yesterday's run left all 39 subtasks
       `pending` despite 13/13 parent tasks `done`.)
    c. Update `.atlas-ai/state/pipeline.json` per-task: call
       `mcp__plugin_prd_go__update_pipeline_task_status(task_id=<N>,
       status="done")` if the MCP tool is available. If not, fall back to
       atomic read-modify-write using the pattern in
       `mcp-server/pipeline.py:locked_update()` — read, append `<N>` to
       `phase_evidence.EXECUTE.tasks_completed`, write to temp, rename.
       Never leave pipeline.json and tasks.json mutually inconsistent.
       (Codified 2026-06-04 — yesterday's run promised this write in
       SKILL.md but never executed it. pipeline.json froze at HANDOFF
       transition through all 85 minutes of execution.)

11. **Check stepback triggers**: if 15 minutes have passed with no task
    moving to done, OR 5 consecutive iterations have failed on the same
    task class, the recon escalation ladder is MANDATORY. Climb the ladder
    in this exact order, not out of order:

    `/stepback` -> `/research-before-coding` -> `/question` -> `pivot`

    - `/stepback` — reassess the architectural assumption. Was the plan
      wrong?
    - `/research-before-coding` — feed the blocker into the Perplexity +
      Context7 + GitHub pipeline for fresh external context.
    - `/question` — batch-research the unresolved unknowns in parallel.
    - `pivot` — the plan step itself is unsound; kick the task back to the
      plan author (inbox parent with `message_type="plan_pivot_requested"`).

    The ladder is append-only — if `/stepback` surfaces a fix, apply it and
    return to step 3. Only climb if the prior rung did not yield progress.

12. **Render gamify score** — emit the atlas-gamify one-line score for this
    iteration (tasks done / tasks total, complexity-weighted). This is the
    human-visible progress signal and also feeds the dogfood debrief.

13. **Loop**: back to step 1 until SHIP_CHECK_OK or a halt condition fires.

## Termination

The termination sequence is strict — three steps, in order, no shortcuts:

1. Run `.atlas-ai/ship-check.py`. If it does NOT exit 0, halt. Do NOT
   emit any completion signal. Investigate the gate failure, fix, retry.
2. **MANDATORY**: invoke `Skill(skill: "sync")` to refresh the memory
   bank (session-context/CLAUDE-*.md, MEMORY.md, capability inventory).
   This MUST happen BEFORE the SHIP_CHECK_OK token is printed.
   Orchestrators tail-watch the token; if the memory bank is stale when
   they react, successor sessions inherit a wrong picture of the world.
   (Codified 2026-06-04 — yesterday's ai-human-tasker run shipped 15.6k
   LOC while `session-context/CLAUDE-activeContext.md` still said
   "Scaffold complete. No application code yet".)
3. Print `SHIP_CHECK_OK` to stdout. This is the ONLY place in your
   output where the token may appear — emit it nowhere else, to avoid
   false-positive matches by log-watchers.

The ship-check script is deterministic. Its gates are documented at the
top of `${CLAUDE_PLUGIN_ROOT}/skel/ship-check.py` (copied to `.atlas-ai/ship-check.py` at setup):

- Gate 1: `pipeline.json current_phase == "EXECUTE"`
- Gate 2: every `master.tasks[].status == "done"`
- Gate 3: every task has a CDD card (`task-<id>.json` or combined variant)
- Gate 4: plan file exists at `.taskmaster/docs/plan.md` OR `docs/superpowers/plans/*.md`
- Gate 5 (HARD): no non-zero `Exit status N` line in any evidence file

Gate 5 is the convergent must-do from the 2026-06-04 audit — a "PASS"
label on a non-zero-exit test is structurally impossible after this
script runs (modulo the explicit `--override SHIP_CHECK_OVERRIDE_ADMIN`
audit-logged bypass).

Do not emit SHIP_CHECK_OK on a mere "DONE" keyword in a subagent reply.
Do not emit on "all tasks marked done" without the explicit ship-check.
Do not emit before `/sync` has been called.

## Red flags

These are the most common pressure points where the loop silently degrades
from "verified" to "performative". If you catch yourself thinking any of
them, stop and repair the gap.

- "Close enough, mark it done" -> NO. Evidence OR nothing.
- "Let me skip the doubt step this time" -> NO. Triple verification is non-negotiable.
- "I'll retry with same model+prompt" (BLOCKED) -> NO. Escalate.
- "The task says done, don't check evidence files" -> NO. Task status must reflect evidence.

## Observability

Every iteration appends a structured row to
`.atlas-ai/state/execute-log.jsonl`. Field types are strict — text
narrative in a typed field is a logging bug, not compliance. The schema:

- `iteration` (integer, or `"FINAL"` / `"OVERRIDE"` for terminal markers)
- `timestamp` (ISO 8601 string)
- `task_id` (string)
- `complexity` (integer or human label)
- `tier` (string: `"fast"` | `"standard"` | `"capable"`)
- `subagent_status` (string: `"DONE"` | `"DONE_WITH_CONCERNS"` | `"NEEDS_CONTEXT"` | `"BLOCKED"`)
- `retry_count` (integer)
- `triple_verify` (string: `"PASS"` / `"FAIL"` plus free-text rationale)
- `stepback_triggered` (boolean, REQUIRED — true iff `/stepback` was
  invoked this iteration). Putting narrative-text in this field is a
  violation; use `stepback_narrative` instead.
- `stepback_narrative` (string, nullable — explanation when
  `stepback_triggered: true`; `null` otherwise)
- `ladder_rung` (string, nullable — which rung was reached if escalated)
- `gamify` (string — atlas-gamify one-line score)

The stepback fields were split (2026-06-04) after a FINAL iteration entry
wrote a paragraph of narrative into the boolean `stepback` field and was
treated as compliance with the `stepback_mandatory` rule. Boolean trigger
+ nullable narrative is the correct schema.

This log is the dogfood artifact — debrief tools consume it, the
orchestrator greps it, and future runs read it for retrospective analysis.

## Composition

- **Orchestrator handoff**: this skill is invoked post-HANDOFF. It does
  not call `/handoff` — that direction is one-way.
- **Plan editing**: if the plan is unsound, the ladder escalates to
  `pivot`, which inboxes the plan author. This skill does not mutate the
  plan in place.
- **Ship-check**: `.atlas-ai/ship-check.py` is the terminal gate. This
  skill calls it; it does not reimplement the checks.

## Non-exits

This skill uses no explicit process termination. A halt condition reports
the reason in the structured log and returns control to the caller (the
user or the orchestrator). Never kill the shell — the caller owns the
session lifecycle.
