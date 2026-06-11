---
name: objective-loop
description: "Loop /do cycles until done-criteria verify or budget stops."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Skill
  - Task
routing:
  not_for: "one-off tasks that finish in a single dispatch, the harness '/loop 5m /cmd' command, installing system cron jobs (headless-cron-creator), implementing retry/backoff code inside a program (condition-based-waiting), single-condition waits (Monitor tool)"
  triggers:
    - "keep working until"
    - "keep going until"
    - "iterate until done"
    - "loop on this until"
    - "until the tests pass"
    - "until CI is green"
    - "until all PRs are merged"
    - "drive this to done"
    - "objective with done criteria"
    - "work this until verified"
    - "reschedule yourself until"
  complexity: Complex
  category: meta
  pairs_with:
    - verification-before-completion
    - condition-based-waiting
    - feature-lifecycle
---

# Objective Loop

The toolkit's iterate-until-verified-done loop. A user states an objective with verifiable done-criteria; each iteration routes one /do cycle, verifies the criteria by executing them, and reschedules itself via `ScheduleWakeup` until verified-done or budget-stop. This skill is a planner/verifier wrapped around the /do router — it executes no work inline. Objectives over tasks: describe what done looks like and how to verify it; the loop finds the path.

## Phase 1: SPEC

Gather the objective spec from the request. Interview only for missing fields.

| Field | Required | Default |
|---|---|---|
| Objective statement | yes | — |
| DONE-CRITERIA | yes | — |
| Iteration budget | no | 5 |
| Token-budget note | no | `orchestration.token_budget` from `.claude/settings.json` (500000 when absent) |
| NOT-DONE-YET guardrails | no | empty |

**DONE-CRITERIA are verifiable checks.** Each criterion has a `type`: `command` (default, preferred) or `rubric`.

- `command` — a deterministic command with an expected exit code/output: `pytest -q` exits 0; `gh pr view N --json state -q .state` prints `MERGED`; `validate-doc-counts.py` reports zero drifts. A criterion the model reasons about is not a criterion; each needs a command plus an expected observable.
- `rubric` — allowed only where no mechanical check exists, per the PHILOSOPHY.md verification ranking (exit code > fresh-context grader > self-critique). Store the rubric verbatim in the state file at SPEC time: pass conditions plus the evidence the grader must cite. Frozen once the loop starts — changes require the user, same as a guardrail.

**NOT-DONE-YET guardrails** name what may never be done to satisfy a criterion (e.g. "never weaken a gate to make it pass"). They bind every iteration: inject them verbatim into each /do dispatch.

Gate: spec complete. Proceed to Phase 2.

## Phase 2: STATE

Write `.objective/<slug>/state.md` from the template in `references/state-file.md`: objective, criteria table, guardrails, per-iteration log, next planned step.

- Wakeups resume FROM THE STATE FILE, never from conversation memory — the wakeup prompt carries only a pointer.
- `.objective/` mirrors `.feature/`'s ephemerality but stays separate: `.feature/` is feature-lifecycle's phase machine, managed only by `feature-state.py`, and its presence reroutes /do into feature phases. Objectives are arbitrary goals.
- State is session working memory — keep `.objective/` unstaged; stage repo files by name only.

Gate: state file written. Proceed to Phase 3.

## Phase 3: ITERATE — one /do cycle

Plan the smallest next step toward the unmet criteria, then route it through the /do phases: classify → route → dispatch agents → evaluate. The loop dispatches work exclusively through /do — catching yourself editing or analyzing inline means stop and route. Multi-part objectives may dispatch parallel agents per /do's rules.

**Learning capture is automatic.** Every iteration dispatches through /do, so routing rows and outcomes record via the /do learning hooks. Add no manual capture.

Gate: dispatch evaluated, iteration log updated in the state file. Proceed to Phase 4.

## Phase 4: VERIFY (execution, not reasoning)

Run every done-criterion check. A worker's "criterion passes" claim never substitutes for the re-run.

- `command` — run the command; paste the exit code and the decisive output line into the iteration log.
- `rubric` — dispatch a fresh-context sub-agent that did NOT produce the work. Input is the artifact plus the rubric, nothing else — no iteration history. It returns PASS/FAIL plus cited evidence (file:line or output excerpt), pasted into the iteration log exactly like an exit code.

Then:

- All criteria pass → write the final report (per-criterion evidence), STOP. The loop ends by not calling `ScheduleWakeup`.
- Any criterion unmet → Phase 5.

**Criteria-gaming guard (hard rule).** A criterion may never be satisfied by weakening a hook, gate, test, or safety control — and a rubric is never weakened to pass. When the only visible path to "pass" weakens a control or the rubric text, stop the loop and report the conflict to the user.

## Phase 5: RESCHEDULE or STOP

| State | Action |
|---|---|
| All criteria pass | Final report; stop — no wakeup call |
| Unmet + iterations remain | Update state file (log, next planned step); call `ScheduleWakeup {delaySeconds, reason, prompt}` with `prompt` = "Read `.objective/<slug>/state.md`, then resume the objective-loop skill from that state file." |
| Budget exhausted | Honest NOT-DONE report: per-criterion status with last evidence, remaining gaps, suggested next step; stop — no wakeup call |

**Delay table (prompt-cache aware; `ScheduleWakeup` clamps 60–3600s):**

| Wait type | Delay | Cache economics |
|---|---|---|
| Active polling (CI run, PR merge expected soon) | 270s or less | Keeps the Anthropic prompt cache warm (5-min TTL) |
| Idle / long agent work | 1200s+ | Pays one cache miss; right for long gaps |
| ~300s band | skip it | Worst case — pays the miss with none of the idle benefit |

**Harness fallback.** When `ScheduleWakeup` is absent from your tool list, run iterations sequentially in-session against the same state file and budgets. For a single until-condition wait inside an iteration, the `Monitor` tool fits; loop boundaries use `ScheduleWakeup`.

## Safety stance (binding)

- **Default mode is `ScheduleWakeup`**: session-scoped, dies with the session, zero persistence.
- **Cron mode is persistence.** `CronCreate` or system crontab survives the session and requires the owner's explicit `OWNER-APPROVED-PERSISTENCE` phrase per the home CLAUDE.md. Stop and ask before any cron-mode loop; on approval, route to `headless-cron-creator`.
- **Criteria-gaming guard** (Phase 4) and **NOT-DONE-YET guardrails** (Phase 1) bind every iteration.

## Error Handling

| Error | Cause | Solution |
|---|---|---|
| State file missing on wakeup | `.objective/<slug>/` removed mid-loop | Report and stop; ask the user to restate the objective rather than re-deriving it from memory |
| Criterion command fails to run (not just non-zero) | Tool missing, bad path | Fix the check command in the state file first; a broken check verifies nothing |
| Unmet-criteria set unchanged across 2 iterations (read from the Last result column, not judged from memory) | Plan stuck | Change approach: re-route through /do with a different agent or skill; unchanged after a third iteration, spend the report on what blocked progress and stop |
| Wakeup arrives with fresh context | Normal — wakeups carry only the prompt | Resume entirely from the state file per `references/state-file.md` |

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Writing or resuming the state file | `state-file.md` | Template, slug rules, resume protocol |

## References

- `${CLAUDE_SKILL_DIR}/references/state-file.md` — state-file template, slug rules, and the wakeup resume protocol
