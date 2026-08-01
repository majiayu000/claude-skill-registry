---
name: phx-watch-pr
description: Watch an Elixir/Phoenix PR for new review comments (bot + human) and
  CI results via a background watcher that wakes Claude only on real events. Use after
  opening a PR or pushing, while waiting on CI or reviewers.
---

# Watch PR (Token-Conscious)

Watch a PR's reviews, comments, and CI with a background watcher that
wakes Claude ONLY on real events — no foreground sleep loops, no context
bloat. The watcher polls quietly in its own process; nothing enters
context until something genuinely changed.

## Usage

```
$phx-watch-pr 42                 # watch reviews + comments + checks
$phx-watch-pr 42 --checks-only   # CI only (delegates to gh pr checks --watch)
$phx-watch-pr 42 --fix           # on actionable review, draft fixes too
$phx-watch-pr 42 --codex         # + request Codex cloud review, loop until clean
$phx-watch-pr 42 --codex --codex-rounds 2   # cap re-review rounds (default 3)
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
4. **NEVER auto-post replies or auto-push** — hand off to `$phx-pr-review`
   for responses; show drafts and get approval. ONE exception: passing
   `--codex` IS the consent to post the `@codex review` trigger comment
   (and its per-round re-requests) — nothing else is ever auto-posted
5. **Bound every watch** — default MAX_DURATION 3600s (7200s with
   `--codex`); always stop on terminal state. Codex rounds are bounded by
   `--codex-rounds` (default 3) — each round costs cloud quota

## Workflow

### Step 1: Parse Arguments

Extract PR number (from number or URL — URL also yields the repo). Detect
`--checks-only` / `--fix` / `--codex` / `--codex-rounds N`. Baseline
timestamp = now; events are "new since baseline", so old reviews don't
re-fire.

With `--codex`, the **default is to POST `@codex review`** — the flag IS
that consent (Iron Law 4). Skip the trigger ONLY when the connector bot
(`chatgpt-codex-connector[bot]`) has itself reacted to / reviewed the
current head SHA. The repo's CI "Codex" check and any local `codex exec` /
`$phx-review --codex` / `$phx-codex-loop` run are DIFFERENT mechanisms from
the GitHub connector — they NEVER satisfy the skip. When unsure, post. The
connector auto-registers PRs on ready (its absence surfaces later as
`codex_timeout`), so check ITS reactions before posting a redundant trigger:

```bash
HEAD_AT=$(gh api "repos/{owner}/{repo}/commits/$(gh pr view {n} --json headRefOid -q .headRefOid)" --jq .commit.committer.date)
BOT=$(gh api "repos/{owner}/{repo}/issues/{n}/reactions" | jq -r --arg t "$HEAD_AT" \
  '[.[] | select(.user.login == "chatgpt-codex-connector[bot]" and .created_at >= $t) | .content] | unique | join(",")')
```

(`gh api --jq` accepts no `--arg` — pipe through standalone `jq`.)

**Definitive check first**: a **connector-bot** comment or review containing
`Reviewed commit: {sha}` that matches the current head sha means that
state IS reviewed (clean if it says "Didn't find any major issues") —
trust it over timestamps, which are client-set and can skew. Then:

| Connector-bot signal on current head | Action |
|-------------------------------|--------|
| `+1` reaction | Connector already reviewed this head clean — no trigger, no codex round; watch CI/humans only |
| `eyes` + a codex review already submitted since `$HEAD_AT` | Findings already posted — skip the watch; run the `codex_review` action (Step 3) now |
| `eyes` only | Review in flight — do NOT post; export `WATCH_CODEX=1 WATCH_CODEX_SINCE=$HEAD_AT` (no trigger id) and watch |
| none (or reactions predate head) | Post the trigger and capture its id: |

```bash
TRIGGER_ID=$(gh api --method POST "repos/{owner}/{repo}/issues/${PR}/comments" \
  -f body="@codex review" --jq '.id')
```

Export `WATCH_CODEX=1 WATCH_CODEX_TRIGGER_ID=$TRIGGER_ID` to the watcher
env and set MAX_DURATION 7200. Round counter starts at 1.

### Step 2a: `--checks-only` Path

No custom poller needed — `gh pr checks --watch` blocks until all checks
finish, then exits. Run via Bash with `run_in_background: true`:

```bash
gh pr checks {n} --watch --fail-fast --interval 10
```

Exit code is the signal: `0` = pass, `1` = fail, `8` = pending. On exit,
report the conclusion; on failure, offer `$phx-investigate` with the
failing job log (`gh run view {run-id} --log-failed`).

### Step 2b: Full Watch Path

Start the **Monitor tool** (preferred — streams each event line back) on:

```
scripts/watch-pr.sh {n} reviews,comments,checks
```

Monitor is a deferred tool — load its schema FIRST via ToolSearch
(`select:Monitor`); calling it blind fails with InputValidationError
(params are `command`, `description`, `timeout_ms`, `persistent` — do
not invent others). Set `timeout_ms` = MAX_DURATION × 1000.
Where Monitor is unavailable
(Bedrock/Vertex/Foundry), run the same script via Bash
`run_in_background: true` — it exits on the first terminal event instead.
Stay idle or keep working until an event lands.

### Step 3: React Per Event

| Event | Action |
|-------|--------|
| `review` / `comment` (actionable) | Summarize the delta; with `--fix` draft fixes + `mix compile && mix test`; route reply drafting to `$phx-pr-review {n}` |
| `check` conclusion `failure` | Offer `$phx-investigate` on the failing job |
| `codex_ack` | Note "codex is reviewing (~15–20 min on large PRs)"; keep waiting |
| `codex_review` | Stop the watcher. Run `$phx-pr-review {n} --bots-only` (fix → reply → resolve; user approves and pushes). If rounds < `--codex-rounds`: post `@codex review` again, restart watcher with the new trigger id, round+1. Else: report remaining findings, stop |
| `codex_clean` | Codex is clean (👍 reaction OR a "Didn't find any major issues" bot comment). If checks also green → terminal success "codex + CI clean"; else keep watching CI |
| `codex_timeout` | Inform: repo likely lacks the Codex connector; continue as a plain watch |
| `merged` / `pr_closed` / `watchdog` / `watch_error` | Stop, report final state |

A `codex_review` whose `$phx-pr-review --bots-only` fetch finds zero
unresolved codex threads also counts as clean (summary-only review).

### Step 4: Stop

The watcher self-terminates on terminal states. To stop early: `TaskStop`
the background task or cancel the monitor.

## Integration

```text
push / open PR → $phx-watch-pr {n} ──(new review)──► $phx-pr-review {n}
                              ├──────(CI fail)─────► $phx-investigate
                              ├──(--codex: codex_review)─► $phx-pr-review --bots-only → push → re-request → watch (≤3 rounds)
                              ├──(--codex: codex_clean + CI green)─► done: codex + CI clean
                              └──────(merged)──────► done
```

## References

- `references/watcher-mechanics.md` — cache TTL math, Monitor vs run_in_background vs ScheduleWakeup, rate-limit notes
