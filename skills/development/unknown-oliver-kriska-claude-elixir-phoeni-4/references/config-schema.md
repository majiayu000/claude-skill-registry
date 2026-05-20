# v2 Surface — Designed, NOT Built at MVP

This file pins the **stable interface** for v2 features so MVP users
don't build workflows on a surface that will churn. None of this is
implemented at MVP. `/catchup` ignores all of it today.

## 1. Per-project config — `.claude/catchup.local.md`

Follows the standard plugin-settings pattern: YAML frontmatter +
markdown notes, committed-optional, per-repo. Read at the top of the
skill when present; CLI flags override file values.

```markdown
---
since_default: "last-session"
sources: [github, git, linear, calendar]
focus: [reviews-requested]
exclude_authors: [dependabot, renovate, github-actions]
linear:
  team: ENA
  assignee: me
slack:                 # v2 opt-in source
  watch_channels: ["#eng-platform", "#incidents"]
gmail:                 # v2 opt-in source
  labels: ["inbox", "team"]
quiet:
  bots: true           # drop bot PRs unless --focus asks
  own_merged: true     # drop your own already-merged work
---

# Notes
Repo-specific catch-up guidance, e.g. "ignore the `release/*`
branches; the mobile team owns those."
```

Resolution order: **CLI flag → `.claude/catchup.local.md` → built-in
default**. The file never enables Slack/Gmail implicitly — those
require both a config block *and* the source MCP present (privacy).

## 2. Scheduling — `--schedule`

```
/catchup --schedule "monday 8am"
/catchup --schedule "weekdays 8am" --deliver imessage
/catchup --schedule off
```

Implemented via `CronCreate` (one routine per repo, named
`catchup:<repo-slug>`). The routine re-runs the same skill and
**delivers** the inline summary to a sink:

- `daily-note` (default) — append the brief to today's note / drop file
- `imessage` — send the summary to the user's self-chat
- `stdout` — just run, leave the file

Missed-run policy: a scheduled run uses `--since last-session` so a
skipped Monday still covers the full gap on Tuesday. `--schedule off`
deletes the routine via `CronDelete`.

## 3. Cross-project rollup — `--all-repos`

```
/catchup --all-repos
```

Walks a configured project root (default: `~/Projects`), runs the
`git`/`gh` adapters per repo with activity in the window, and emits
**one** brief with a per-repo section, globally ranked by "needs you" (reviews
requested > red CI on your PR > assigned ticket moved > FYI). Repos
with zero signal are collapsed to a single "quiet: foo, bar" line.

Guardrails: hard cap on repos scanned (default 25), `git` only by
default (`gh` per-repo is rate-limit-sensitive — opt in with
`--all-repos --github`), and a wall-clock budget so the rollup can't
run unbounded.

## 4. v2 sources — Slack / Gmail

Strict opt-in, double-gated (config block **and** MCP present).
Excerpt-only is **non-negotiable**: subjects, sender, one-line gist,
permalink. Never the message body, never a thread dump, never piped to
a remote model. This is the Privacy element of the brief, enforced in
code, not left to prompt discretration.

## Why pin this now

The MVP ships the narrow, reliable core (`gh` + `git`, optional
Linear/Calendar, one brief). Pinning the v2 grammar means a user who
writes a `.claude/catchup.local.md` today, or scripts around the flag
names, won't be broken when v2 lands. The surface is a contract; the
implementation is deferred.
