---
name: phx:watch-pr
description: Watch an Elixir/Phoenix PR for new review comments (bot + human) and CI results via a background watcher that wakes Claude only on real events. Use after opening a PR or pushing, while waiting on CI or reviewers.
effort: medium
argument-hint: <PR number or URL> [--checks-only] [--fix]
---

# Watch PR (Token-Conscious)

Watch a PR's reviews, comments, and CI with a background watcher that
wakes Claude ONLY on real events — no foreground sleep loops, no context
bloat. The watcher polls quietly in its own process; nothing enters
context until something genuinely changed.

## Usage

```
/phx:watch-pr 42                 # watch reviews + comments + checks
/phx:watch-pr 42 --checks-only   # CI only (delegates to gh pr checks --watch)
/phx:watch-pr 42 --fix           # on actionable review, draft fixes too
```

## Iron Laws

1. **NEVER foreground-poll with `sleep` in the session** — use the
   background watcher (Monitor / run_in_background). Foreground polling
   bloats context and straddles the 5-min cache TTL
2. **Deltas ONLY enter context** — never dump full `gh` JSON. The watcher
   emits one-line events; read `.claude/watch/pr-{n}.jsonl` on demand
3. **Silence is not success** — the watcher MUST emit on PR closed/merged,
   CI failure, repeated gh errors, and watchdog timeout — not just "new
   comment". A silent watcher looks identical to a hung one
4. **NEVER auto-post replies or auto-push** — hand off to `/phx:pr-review`
   for responses; show drafts and get approval
5. **Bound every watch** — default MAX_DURATION 3600s; always stop on
   terminal state

## Workflow

### Step 1: Parse Arguments

Extract PR number (from number or URL — URL also yields the repo). Detect
`--checks-only` / `--fix`. Baseline timestamp = now; events are "new since
baseline", so old reviews don't re-fire.

### Step 2a: `--checks-only` Path

No custom poller needed — `gh pr checks --watch` blocks until all checks
finish, then exits. Run via Bash with `run_in_background: true`:

```bash
gh pr checks {n} --watch --fail-fast --interval 10
```

Exit code is the signal: `0` = pass, `1` = fail, `8` = pending. On exit,
report the conclusion; on failure, offer `/phx:investigate` with the
failing job log (`gh run view {run-id} --log-failed`).

### Step 2b: Full Watch Path

Start the **Monitor tool** (preferred — streams each event line back) on:

```
${CLAUDE_SKILL_DIR}/scripts/watch-pr.sh {n} reviews,comments,checks
```

with `timeout_ms` = MAX_DURATION × 1000. Where Monitor is unavailable
(Bedrock/Vertex/Foundry), run the same script via Bash
`run_in_background: true` — it exits on the first terminal event instead.
Stay idle or keep working until an event lands.

### Step 3: React Per Event

| Event | Action |
|-------|--------|
| `review` / `comment` (actionable) | Summarize the delta; with `--fix` draft fixes + `mix compile && mix test`; route reply drafting to `/phx:pr-review {n}` |
| `check` conclusion `failure` | Offer `/phx:investigate` on the failing job |
| `merged` / `pr_closed` / `watchdog` / `watch_error` | Stop, report final state |

### Step 4: Stop

The watcher self-terminates on terminal states. To stop early: `TaskStop`
the background task or cancel the monitor.

## Integration

```text
push / open PR → /phx:watch-pr {n} ──(new review)──► /phx:pr-review {n}
                              ├──────(CI fail)─────► /phx:investigate
                              └──────(merged)──────► done
```

## References

- `${CLAUDE_SKILL_DIR}/references/watcher-mechanics.md` — cache TTL math, Monitor vs run_in_background vs ScheduleWakeup, rate-limit notes
