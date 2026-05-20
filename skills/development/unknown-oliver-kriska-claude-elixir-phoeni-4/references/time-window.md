# Time Window Resolution

Turn `--since` into an unambiguous instant, then derive everything else
from it. **Epoch seconds is the single pivot** — it is timezone-free,
and both GNU (`date -d`) and BSD/macOS (`date -v`/`-r`) can read and
write it. Never resolve calendar words straight to UTC; that is the
timezone bug.

- `SINCE_EPOCH` — Unix seconds. The one source of truth.
- `SINCE_ISO` — `date -u` of `SINCE_EPOCH`, e.g. `2026-05-12T22:00:00Z`
  (for `gh api` / MCP filters; compares on absolute time).
- `SINCE_DATE` — UTC `YYYY-MM-DD` of `SINCE_EPOCH` (for `gh search`).
- `SINCE_LABEL` — human, with the anchor TZ shown so it is
  unambiguous: `since Fri May 13 00:00 CEST (3 days)`.

## The timezone model (read this)

The person running `/catchup` is on their own machine, so the machine's
**local timezone is the user's timezone**. Calendar words resolve in
that local TZ:

- `--since "friday"` → the user's most recent Friday, **00:00 local**.
- `--since "yesterday"` → start of yesterday, **local**.
- `--since "2026-05-13"` → that date **00:00 local**.

That local wall-clock is converted **once** to `SINCE_EPOCH` (an
absolute instant). Every source (git author/commit time, GitHub API
UTC timestamps, Linear/Calendar) is then compared on that absolute
instant. Consequence — and this is the desired behaviour:

> A colleague in another timezone whose own "Friday" begins at a
> different absolute moment is included **iff their event's absolute
> timestamp ≥ the user's Friday instant**. "Since Friday" means *since
> the user's Friday started*, not "since each author's local Friday".
> Their Friday-morning commit counts only if it happened at/after the
> user's Friday 00:00 in real time — which is exactly right.

Relative durations (`2h`, `3d`) are TZ-agnostic deltas: `now - N`.

## Grammar for `--since`

| Input              | Resolution                                          |
|--------------------|-----------------------------------------------------|
| `last-active`      | (default) smartest: latest evidence *you* were here  |
| `last-session`     | newest Claude session mtime, this repo only          |
| `last-commit` / `last-mine` | your last own commit / PR / review, whichever newest |
| `2h`, `90m`, `3d`  | `now - duration` (TZ-agnostic delta)                |
| `yesterday`        | yesterday 00:00 **local TZ**                         |
| `friday`, `monday` | most recent past occurrence, 00:00 **local TZ**      |
| `"2026-05-13"`     | that date 00:00 **local TZ**                         |
| `"last week"`      | `now - 7d`                                           |

Validate `--since` against this grammar **before** it touches a shell.
No match → fall back to 24h and note the assumption in the brief's
Risks block.

## Resolving each form to `SINCE_EPOCH`

```bash
LOCAL_TZ=$(date +%Z)                       # user's TZ abbrev, for the label
NOW=$(date +%s)

# relative duration: now - N (TZ-agnostic)
#   parse 2h/90m/3d -> seconds, SINCE_EPOCH=$((NOW - secs))

# yesterday / explicit date: local midnight -> epoch
#   GNU : date -d 'yesterday 00:00' +%s
#         date -d '2026-05-13 00:00:00' +%s
#   BSD : date -v-1d -v0H -v0M -v0S +%s
#         date -j -f '%Y-%m-%d %H:%M:%S' '2026-05-13 00:00:00' +%s

# weekday name: most-recent-past occurrence at local 00:00.
# Use day-of-week arithmetic (do NOT rely on `date -d 'last friday'` —
# GNU/BSD disagree, and behaviour on the named day itself differs):
TARGET=5                                   # Mon=1..Sun=7 (here: Friday)
DOW=$(date +%u)
BACK=$(( (DOW - TARGET + 7) % 7 ))         # 0 if today IS that weekday
#   GNU : date -d "$BACK days ago 00:00" +%s
#   BSD : date -v-"${BACK}"d -v0H -v0M -v0S +%s
# BACK=0 ⇒ today 00:00 local ("since friday" said on a Friday = today).
```

Then derive the rest from the pivot (portable both ways):

```bash
SINCE_ISO=$(date -u -d "@$SINCE_EPOCH" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
         || date -u -r "$SINCE_EPOCH"  +%Y-%m-%dT%H:%M:%SZ)
SINCE_DATE=${SINCE_ISO%%T*}
```

- **git**: pass the absolute instant — `git log --since="$SINCE_ISO"`
  (UTC `…Z`). Git filters on each commit's own absolute timestamp, so
  cross-timezone colleagues are handled correctly. Do **not** pass a
  bare `--since="friday"` to git: git would re-resolve it in the
  machine's local TZ *and* with its own weekday quirks — exactly the
  inconsistency this pivot removes.
- **`gh api` / notifications / MCP**: use full `SINCE_ISO` (exact,
  timestamp-granular).
- **`gh search` / `gh pr list --search`**: `updated:>=$SINCE_DATE`
  only — GitHub search is **UTC, date-granular**. Near a TZ/midnight
  boundary this can be off by up to a day, so treat search hits as a
  coarse pre-filter and confirm precise inclusion with the
  `SINCE_EPOCH`/`SINCE_ISO` timestamp on each item before it enters the
  brief.

## `last-active` auto-detect (default) — "since I was last here"

The default must answer "what changed **while I was away**", so the
anchor is *the most recent moment we have hard evidence the user was
working*. A commit or a PR is stronger proof of presence than a
session file (which can be a background/scheduled run). Take the
**MAX** of these absolute instants — the latest footprint is the
correct lower bound: you were definitely here then; everything after
is "while away". All are already absolute, so no TZ handling.

```bash
SLUG=$(pwd | sed 's@/@-@g'); SDIR="$HOME/.claude/projects/$SLUG"

# 1. newest Claude session mtime for THIS repo (skip the live session:
#    if newest mtime is within ~5 min of now, use the second-newest)
S1=$(ls -t "$SDIR"/*.jsonl 2>/dev/null | head -1)
E_SESS=$( [ -n "$S1" ] && { date -r "$S1" +%s 2>/dev/null || stat -c %Y "$S1"; } )

# 2. your last own commit anywhere in this repo (committer date, abs)
GME=$(git config user.email)
E_COMMIT=$(git log --all --author="$GME" -1 --format=%ct 2>/dev/null)

# 3. your last own PR activity IN THIS REPO (repo-scoped — a global
#    `gh search prs --author=@me` is wrong here: it would anchor to
#    activity in some *other* repo and miss a week of changes in this
#    one). Often empty (you commit but don't author PRs) → just skip.
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null)
E_PR=$( [ -n "$REPO" ] && gh pr list --repo "$REPO" --author @me \
        --state all --limit 1 --json updatedAt \
        --jq '.[0].updatedAt' 2>/dev/null \
        | { read d; [ -n "$d" ] && { date -u -d "$d" +%s 2>/dev/null \
            || date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "$d" +%s; }; })

# MAX of whatever resolved = "you were last here"
SINCE_EPOCH=$(printf '%s\n' "$E_SESS" "$E_COMMIT" "$E_PR" \
              | grep -E '^[0-9]+$' | sort -n | tail -1)
```

Record in the brief which signal won, e.g. *"window anchored to your
last commit `a1b2c3d` (Fri 18:42 CEST) — more recent than your last
session here."* That transparency lets the reader sanity-check the
boundary.

**Variants:** `last-session` = signal 1 only. `last-commit` /
`last-mine` = MAX of signals 2 and 3 only (ignore session files —
useful when you want "since I last *worked*", not "since Claude last
ran here"). No signal at all → `SINCE_EPOCH=$((NOW - 86400))` and note
*"No activity signal — defaulted to 24h."* in the Risks block.

Optional cross-check: if ccrider MCP is present, its
last-session-for-cwd timestamp can confirm signal 1. Not required.

## Producing `SINCE_LABEL`

```
days = round((NOW - SINCE_EPOCH) / 86400)
SINCE_LABEL = "since {Www Mmm DD} {HH:MM} {LOCAL_TZ} ({days}d)"
```

Sub-day windows use hours: `since 09:12 CEST today (5h)`. Always show
the anchor **in the user's local TZ with the TZ abbrev** — the reader
must see which Friday the brief means. Goes in the brief's **Intent**
line and **Timeline** block.
