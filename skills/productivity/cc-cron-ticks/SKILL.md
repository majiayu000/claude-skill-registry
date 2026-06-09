---
name: cc-cron-ticks
user-invocable: false
description: |-
  Use when scheduling autonomous in-session flywheel ticks with Claude Code cron routines.
  Triggers:
practices:
- agile-manifesto
- continuous-delivery
hexagonal_role: driving-adapter
consumes:
- evolve
- autodev
produces:
- scheduled-tick
context_rel:
- kind: customer-of
  with: evolve
skill_api_version: 1
user-invocable: true
context:
  window: inherit
  intent:
    mode: none
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: orchestration
  dependencies: [evolve, autodev]
  stability: stable
output_contract: A live cron job (job ID returned) plus a tick-design note; no files unless durable:true persists .claude/scheduled_tasks.json
---

# cc-cron-ticks

Schedule autonomous flywheel ticks from inside a Claude Code session. The Claude-native scheduler (`CronCreate`/`CronList`/`CronDelete` and the /schedule routine surface) re-enqueues a prompt on a wall-clock cadence so a loop binary or harness keeps driving without you babysitting the REPL.

## Overview / When to Use

Two distinct schedulers exist; pick deliberately:

- **In-session cron (`CronCreate` tools).** Lives in *this* Claude session. Re-enqueues a prompt every cron match. Fires only while the REPL is idle (never mid-query). Default in-memory: dies when Claude exits. This is the engine for the **1-minute in-session drive loop**.
- **/schedule routines (durable remote agents).** Cron-scheduled remote agents that run independent of any open session. Use for routines that must run when no session is attached. List/create/update/run via the /schedule skill.

Use cron ticks when an autonomous loop (evolve, factory, control-plane `tick.sh`, burndown) must be re-fired on a cadence. Use a one-shot (`recurring: false`) for "do Y at time X." Use **Monitor**, not cron, when you need to react the instant something changes — cron polls on fixed intervals; Monitor streams events live.

## ⚠️ Critical Constraints

- **Never use `claude -p` / `--print` as the tick body.** **Why:** `-p` bills the API per-token, not the Max subscription — an overnight loop silently burns real money. A tick prompt should drive NTM panes (interactive Claude on OAuth = sub) or `codex exec` (Pro sub), or do work directly in this session. (Memory: never-claude-p-for-workers.)
- **Ticks must be idempotent.** **Why:** the scheduler adds jitter and fires only on idle, so two ticks can overlap or a tick can land twice. Each tick must claim work atomically (e.g. `bd ready`/`bd update --claim`, a lockfile, or an Agent Mail reservation) and no-op cleanly when there is nothing to do. A non-idempotent tick double-executes and corrupts state.
- **Recurring jobs auto-expire after 7 days.** **Why:** the scheduler fires one final time at the 7-day mark then deletes the job. Tell the user this when scheduling recurring work; for longer-lived loops re-create on a cadence or move to launchd/systemd.
- **In-memory by default; `durable: true` only on explicit request.** **Why:** non-durable jobs vanish when Claude exits — correct for a session-bound drive loop. `durable: true` writes `.claude/scheduled_tasks.json` and survives restarts; only set it when the user asks the task to outlive the session.
- **Ticks fire only while the REPL is idle.** **Why:** a tick will not interrupt an in-flight query. A long-running foreground task starves the loop — keep tick bodies short, or dispatch the heavy work to a background pane/process and let the tick just poll-and-claim.
- **Avoid `:00` and `:30` minute marks for approximate cadences.** **Why:** every fleet job that asks for "9am" lands on `0 9` and hits the API at the same instant worldwide. For approximate times pick an off-minute (`57 8`, `7 * * * *`). Only pin `:00`/`:30` when the user means an exact clock time.

## Workflow / Methodology

### Phase 1: Choose the shape
Decide along two axes before touching a tool:
- **Recurring vs one-shot.** Loop/poll → `recurring: true` (default). "At time X do Y" → `recurring: false` with pinned `minute hour day-of-month month`.
- **Session-bound vs durable.** Drive-this-session → default in-memory. Must survive restart → `durable: true`, or escalate to /schedule routine / OS cron.

**Checkpoint:** Confirm the tick body does NOT use `claude -p`, and that the work it triggers is claimable/idempotent. Do not proceed otherwise.

### Phase 2: Design the cadence
Standard 5-field cron in **local time**: `minute hour day-of-month month day-of-week`.

| Cadence | Expression | Note |
|---|---|---|
| Every 1 min (drive loop) | `* * * * *` | the canonical in-session flywheel tick |
| Every 5 min | `*/5 * * * *` | lighter loop / queue drain |
| Hourly (approx) | `7 * * * *` | off the `:00` mark |
| Weekday morning (approx) | `57 8 * * 1-5` | off `:00`; not `0 9` |
| One-shot today 2:30pm | `30 14 <today_dom> <today_month> *` | with `recurring: false` |

Jitter: recurring ticks fire up to 10% of period late (max 15 min); `:00`/`:30` one-shots up to 90s early. A `* * * * *` loop is effectively "about once a minute," which is the intended drive-loop behavior — the loop body itself, not the cron precision, carries correctness.

**Checkpoint:** Cadence matches the work's natural period (don't tick faster than a tick can finish-and-claim). Confirm with the user before creating a `* * * * *` loop — it is the highest-frequency option.

### Phase 3: Create the tick
Call `CronCreate` with `cron`, `prompt`, and explicit `recurring`/`durable`. The `prompt` is the tick body re-enqueued each fire. Keep it a thin driver:

> "Run one tick of the control-plane loop: `bash ~/dev/control-plane/tick.sh`. If it claims and completes a bead, commit. If the queue is dry, no-op and report 'queue dry'."

Capture the returned **job ID** — it is the handle for `CronDelete`.

**Checkpoint:** Verify with `CronList` that the job is registered with the intended expression.

### Phase 4: Operate the loop
- `CronList` — inspect all session cron jobs.
- `CronDelete { id }` — stop a loop (use the captured job ID).
- For durable/remote routines, manage via the /schedule skill (list/update/run-now).

**Checkpoint:** When the loop's goal is met or the session is wrapping, `CronDelete` every active drive tick so it doesn't keep firing on a stale objective.

## Output Specification

**Format:** a live scheduler job (no file artifact) unless `durable: true`.
**Filename:** none by default; `durable: true` writes/updates `.claude/scheduled_tasks.json` (relative to project root).
**Structure:** report back, per tick created — `job_id`, cron expression, `recurring`, `durable`, the 7-day expiry note (if recurring), and a one-line statement of what each tick does and how it claims work idempotently.

## Quality Rubric

- [ ] Tick body never uses `claude -p` / `--print`.
- [ ] Work the tick triggers is idempotent / atomically claimed; double-fire is safe.
- [ ] `recurring` and `durable` set explicitly and intentionally (not relying on silent defaults).
- [ ] User was told about the 7-day auto-expiry for recurring jobs.
- [ ] Approximate cadences avoid `:00`/`:30`; exact times only when the user means them.
- [ ] Job ID captured and reported so the loop can be stopped.
- [ ] Monitor considered and rejected in favor of cron (or vice versa) — right tool for poll vs stream.
- [ ] A stop/cleanup path is named (`CronDelete <id>` at session wrap).

## Examples

**1-minute in-session drive loop:**
`CronCreate { cron: "* * * * *", prompt: "Tick the flywheel: bash ~/dev/control-plane/tick.sh; claim+complete one ready bead, commit, else report 'dry'.", recurring: true }` → returns `job_abc`. Tell the user it expires in 7 days. Stop with `CronDelete { id: "job_abc" }`.

**One-shot reminder/action:** "run the smoke test tomorrow at 8:57am" → `CronCreate { cron: "57 8 <tomorrow_dom> <tomorrow_month> *", prompt: "Run the smoke test and report PASS/FAIL.", recurring: false }`.

**Hourly health check, off the mark:** `CronCreate { cron: "13 * * * *", prompt: "Run bash bin/health-check.sh; if non-green, summarize the failing check.", recurring: true }`.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Tick never fires | REPL was busy mid-query, or no idle window | Keep ticks short; dispatch heavy work to a background pane and poll |
| Loop stopped after a week | Recurring 7-day auto-expiry | Re-create the job, or move to launchd/systemd for indefinite loops |
| Job gone after restart | In-memory default | Re-create, or set `durable: true` if it must survive restarts |
| Surprise API bill from a loop | Tick body used `claude -p` | Replace with NTM pane / `codex exec` / in-session work |
| Two ticks corrupted state | Non-idempotent tick + jitter/overlap | Add atomic claim (`bd --claim`/lock/mail reservation); no-op when dry |
| Needed instant reaction, cron was laggy | Used cron for live watching | Switch to the Monitor tool — it streams change events |
| Everyone's jobs hit the API at once | Used `:00`/`:30` for an approximate time | Use an off-minute (`7`, `13`, `57`) |

## See Also / References

| I need to… | Use |
|---|---|
| Read the loop contract a tick reads each fire | `agentops:autodev` (PROGRAM.md/AUTODEV.md) |
| Drive an autonomous improvement loop from a tick | `agentops:evolve` |
| Schedule a routine that runs with NO session attached | /schedule skill (durable remote routines) |
| React the instant something changes (not poll) | Monitor tool (live event stream) |
| Self-pace a recurring prompt without cron precision | `loop` skill |
| Confirm the Claude Code cron/scheduler surface is current | `claude-code-latest-features.md` contract |

**Currency anchor:** Claude Code feature contract — `../shared/references/claude-code-latest-features.md` (verified family 2.1.x). The `CronCreate`/`CronList`/`CronDelete`/`Monitor` tool behaviors in this skill (idle-only firing, 10%/15-min recurring jitter, 90s one-shot skew, 7-day recurring auto-expiry, in-memory-vs-`durable` to `.claude/scheduled_tasks.json`) were verified against the live tool schemas on 2026-06-06.

**Memory:** never-claude-p-for-workers; ACFS bootstrap node 1-min in-session drive loop (control-plane `tick.sh`).
