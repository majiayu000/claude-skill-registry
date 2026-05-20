# Source Adapters

Exact recipes per source. Detect first, query second, degrade always.
`$SINCE_ISO` / `$SINCE_DATE` come from `time-window.md`.

## Detection (run before any query)

```bash
command -v gh   >/dev/null && gh auth status >/dev/null 2>&1   # github ON
git rev-parse --is-inside-work-tree >/dev/null 2>&1            # git ON
```

Linear / Calendar are MCP: source is ON only if a tool whose name
contains `linear` / `calendar` is in your available tool list. Do not
guess server names — inspect what is actually present this session.
Anything OFF → one line in the brief's Risks/assumptions block.

## GitHub (`gh`)

Identity + repo:

```bash
ME=$(gh api user --jq .login)
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
DEFBR=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)
```

**Scoping (important).** Default `--scope repo`: EVERY GitHub signal
below is filtered to `$REPO`. A brief run inside one repo must never
silently list another repo's reviews or notifications. `--scope all`
is opt-in and its cross-repo hits go in a separate **Other repos**
subsection, never mixed into this repo's lists.

**Timestamp discipline.** GitHub times are UTC (`Z`). Judge each item
on *its own* controlling timestamp ≥ `SINCE_EPOCH` — never promote a
pre-window object because a related object moved in-window; a standing
review request is "pre-window, for completeness", not a Top priority.
Convert `Z` → `LOCAL_TZ` before printing a clock time; never label a
UTC value with a local TZ (`06:36:23Z` is `08:36 CEST`).

The four signals that matter on return:

1. **Pinged you while away** — repo-scoped notifications endpoint:

   ```bash
   gh api "/repos/$REPO/notifications?since=$SINCE_ISO&all=true" \
     --jq '.[] | {reason, title: .subject.title, type: .subject.type, url: .subject.url}'
   ```

   `reason` ∈ `review_requested`, `mention`, `assign`, `comment`,
   `team_mention`. This is "what asked for me, here". Lead with it.
   `--scope all` also: `gh api "/notifications?since=$SINCE_ISO&all=true"`
   then `select(.repository.full_name != $REPO)` for the Other-repos
   subsection.

2. **Review requested of you (open), in this repo:**

   ```bash
   gh pr list --repo "$REPO" --search "review-requested:@me" \
     --state open --json number,title,url,updatedAt --limit 30
   ```

   `--scope all` also: `gh search prs --review-requested=@me
   --state=open --json number,title,repository,url --limit 30`, then
   filter out `$REPO` rows into the Other-repos subsection.

3. **Your PRs with new activity / CI state:**

   ```bash
   gh pr list --repo "$REPO" --author @me --state open \
     --search "updated:>=$SINCE_DATE" \
     --json number,title,url,reviewDecision,statusCheckRollup,updatedAt --limit 30
   ```

   `reviewDecision=APPROVED` + green checks → "ready to merge".
   `statusCheckRollup` with `conclusion=FAILURE` → "CI broke while away".

4. **PRs others moved in this repo (context, not action):**

   ```bash
   gh pr list --repo "$REPO" --state all \
     --search "updated:>=$SINCE_DATE -author:$ME" \
     --json number,title,author,state,url,mergedAt --limit 40
   ```

Drop bot authors (`dependabot`, `renovate`, `github-actions`) unless
`--focus` explicitly asks for them. `--depth quick` → counts + top 3
only, skip calls 3–4.

OFF (no `gh`/auth): skip the whole GitHub source, note it. Do not try
to scrape GitHub over the web.

## Git (always available in a repo — the floor)

```bash
GME_E=$(git config user.email); GME_N=$(git config user.name)
DEFBR=${DEFBR:-$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')}
DEFBR=${DEFBR:-main}
git fetch --quiet origin "$DEFBR" 2>/dev/null || true
```

Commits by **others** on the default branch in the window:

```bash
# TAB sep (%x09): commit subjects often contain '|' (e.g.
# "feat(a|b):") — '|' as -F would shift fields. Tab never appears in
# a git subject; macOS awk handles -F'\t' but NOT -F'\x1f'.
git log "origin/$DEFBR" --since="$SINCE_ISO" --no-merges \
  --pretty=format:'%h%x09%an%x09%ae%x09%ad%x09%s' --date=short \
  | awk -F'\t' -v me="$GME_E" '$3 != me'
```

Risk scan — migrations / lockfiles / CI config touched while away
(these are the "may conflict with my branch" items):

```bash
git log "origin/$DEFBR" --since="$SINCE_ISO" --name-only --pretty=format:'%h %s' \
  | grep -iE 'migrations?/|\.lock$|mix\.lock|package-lock|go\.(mod|sum)|Cargo\.lock|\.github/workflows/' \
  | sort -u
```

Your local branches that diverged from an updated default:

```bash
for b in $(git for-each-ref --format='%(refname:short)' refs/heads); do
  base=$(git merge-base "$b" "origin/$DEFBR" 2>/dev/null) || continue
  behind=$(git rev-list --count "$b..origin/$DEFBR" 2>/dev/null)
  [ "${behind:-0}" -gt 0 ] && echo "$b is $behind behind origin/$DEFBR"
done
```

## Impact — your in-flight scope ∩ what moved

The differentiator (issue #47, druyang): not just "what did I miss" but
"how do these changes impact *my* current/future work". Three steps.

**A. Files that moved upstream by others** in the window:

```bash
# DO NOT use `git log --name-only` here: log history-simplification
# silently drops the file list for many commits (verified on a busy
# real repo — one-pass gave 44 files, the true union was 140). Get the non-me
# commit hashes first (no --name-only, tab sep — hashes/emails never
# contain a tab), then union per-commit `git diff-tree`, which is
# exact and parent-aware.
MOVED=$(git log "origin/$DEFBR" --since="$SINCE_ISO" --no-merges \
  --pretty=format:'%H%x09%ae' \
  | awk -F'\t' -v me="$GME_E" '$2!=me{print $1}' \
  | while read -r h; do git diff-tree --no-commit-id --name-only -r "$h"; done \
  | sort -u)
```

**B. Your in-flight scope** — the union of:

```bash
# 1. files in your open PRs (GitHub ON)
for n in $(gh pr list --repo "$REPO" --author @me --state open \
            --json number --jq '.[].number'); do
  gh pr diff "$n" --name-only 2>/dev/null
done
# 2. local branches — BOUNDED to your own, active in the last 60d.
#    Never iterate every branch: big repos have hundreds of stale
#    ones (real repos: 400+) → unbounded scan is a firehose and slow.
CUT=$(( $(date +%s) - 60*86400 ))
for b in $(git for-each-ref --sort=-committerdate refs/heads \
     --format='%(refname:short)%09%(committerdate:unix)%09%(authoremail)' \
   | awk -F'\t' -v me="$GME_E" -v def="$DEFBR" -v cut="$CUT" \
       '$1!=def && $2>cut && index($3,me)>0 {print $1}' | head -15); do
  mb=$(git merge-base "$b" "origin/$DEFBR" 2>/dev/null) || continue
  git diff --name-only "$mb" "$b"
done
# always include the current branch + working tree (even if older)
cur=$(git branch --show-current)
[ -n "$cur" ] && [ "$cur" != "$DEFBR" ] && \
  git diff --name-only "$(git merge-base "$cur" origin/$DEFBR)" "$cur"
# 3. uncommitted working tree
git status --porcelain | awk '{print $2}'
```

Collect all of B into `MINE` (sorted unique). State the bound in the
brief: *"scanned your N branches active in 60d, not all 400."*

**C. Intersect and classify:**

```bash
comm -12 <(printf '%s\n' "$MOVED" | sort -u) <(printf '%s\n' "$MINE" | sort -u)  # DIRECT
```

- **Direct overlap** (exact path in both) → name the incoming
  commit/PR/ticket *and* which of your PRs/branches owns the file. This
  is a real conflict/semantic risk — promote it into Top priorities.
- **Adjacent** — no exact match but a shared top-level dir/module
  (`dirname` to 2 levels) → "may affect your work", lower rank.
- At `--depth deep`: for each direct-overlap file, read the incoming
  change and write one semantic line — what *about* your work it
  affects (API/schema/signature/behavior), not just "it changed".

If your scope is empty (no open PRs, on default branch, clean tree),
say so in one line and skip the Impact block — don't fabricate risk.

## Linear

**MCP ON:** use the available Linear tool(s) to fetch, scoped to
`updatedAt >= $SINCE_ISO`:

- issues assigned to the current user
- issues whose state changed in the window
- new comments on issues you're assigned to or created

Keep each to one line: `PROJ-1234 "title" → InProgress (by @x)`. Never
dump full descriptions/comment threads (Iron Law 2).

**MCP OFF (no-Linear proxy):** harvest ticket refs from the GitHub/git
output you already have:

```bash
grep -oE '[A-Z]{2,}-[0-9]+' <<<"$ALL_PR_AND_COMMIT_TITLES" | sort -u
```

Present them as *"tickets referenced in recent merges (unverified — no
Linear MCP): PROJ-412, PROJ-449…"*. This still tells the user which
work areas moved, without Linear access.

## Calendar

**MCP ON:** list events from `$SINCE_ISO` to end of today in the user's
TZ. Split by `now`:

- **Missed** — ended during the window (flag if you were an organizer
  or required attendee).
- **Today** — upcoming, with start time in local TZ for the Timeline.

**MCP OFF:** skip; note *"Calendar MCP absent — meeting signal not
included."* Do not attempt ICS/web fallback at MVP.

## Cross-source linking (depth: standard/deep)

When a PR title and a Linear ticket (or harvested ref) share an
`XXX-####` token, link them in the brief: `PR #1093 ↔ PROJ-318`. This
is the bit generic digests cannot do and is the plugin's differentiator
— a unified view, not four parallel inboxes.

## Failure policy

Any single command failing (network, auth scope, rate limit) →
`echo` a one-line degraded note for that signal and continue. The brief
must still render from whatever succeeded. `git log` alone is a valid
(minimum) brief.
