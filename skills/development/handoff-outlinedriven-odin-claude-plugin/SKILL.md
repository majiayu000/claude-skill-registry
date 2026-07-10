---
name: handoff
description: Snapshot the current session into a resumable handoff artifact so a cold session, agent, or person continues without replaying context. Use when the user says "write a handoff", "hand off", "snapshot this session", "I'm running low on context", "pause and pack this up for the next session", or "resume this later".
metadata:
  short-description: Snapshot the current session into a resumable handoff artifact
---

# Handoff: resumable session snapshot

Write one artifact that lets a cold session — the same person tomorrow, a fresh agent, or a
colleague — resume this work without replaying the conversation. Chat is ephemeral; this file is the
persistence layer for a single hand-off point.

`handoff` writes exactly one surface: `.outline/handoffs/<slug>-<ts>.md`. It does not commit, does
not delegate, and does not open a PR.

## When to apply / NOT

Apply:
- Context is running low and the task is unfinished.
- End of a work block, or pausing mid-task.
- Switching agents (Claude → agy/codex/grok) and the next one needs the state, not the transcript.

Do NOT:
- Delegate a task to another AI — `antigravity`, `codex`, and `grok` own that.
- Package a branch for review — `commit-push-pr` and `pr-review` own that.

## Write procedure

1. Resolve the workspace and self-ignore it (mirrors `subagent-driven`'s `sd-workspace`):
   ```bash
   root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)   # cwd fallback outside a repo
   mkdir -p "$root/.outline/handoffs"
   printf '*\n' > "$root/.outline/handoffs/.gitignore"          # `*` also ignores the .gitignore itself
   ```
   The handoff stays **local and gitignored** — it never enters `git status` or a commit. To hand
   off to a colleague on another machine, copy the file out (paste it, or attach it to a PR/issue).

2. Name it. `slug` = kebab-case of the task title; `ts=$(date +%Y%m%d-%H%M%S)` (seconds included so
   two runs in the same minute can't collide). Write `$root/.outline/handoffs/<slug>-<ts>.md`. Runs
   leave a **trail** of timestamped files rather than overwriting one. Stale snapshots are yours to prune.

3. Fill the format below. Omit any section that is empty — an empty heading is noise. Echo the
   **absolute** path of the written file to chat (relative paths are not clickable in most terminals).

## To resume

A cold session finds the active handoff by recency, not by knowing the slug:

```bash
root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
eza -1 -s modified -r "$root"/.outline/handoffs/*.md 2>/dev/null | head -1   # newest by mtime; read it
```

## Format

Purpose-built for cold resume. Terse `field: value` header, then only the sections that carry
signal:

```
# Handoff: <one-line task title>
branch: <name @ short-sha> (<clean | dirty: N files>)

## Goal
<1-2 lines: what we're achieving and why>

## Done
- <completed step + evidence: commit sha / passing check>

## In flight
- <the half-built thing: file:line, what's written, what's still missing>

## Next
1. <the single next concrete action>

## Key files
- path:line — why it matters

## Decisions & constraints
- <decision + the why, so the next session does not relitigate it>

## Blockers / open questions
- <what is stuck; what needs a human or an answer>

## Verify
<exact command(s) to confirm state; last known result>
```

## Edge cases

- **No git repo** — `$root` falls back to cwd; `branch:` reads `(no repo)`.
- **Detached HEAD / dirty tree** — that is the state worth capturing; record it in `branch:`.
- **Nothing in flight** — omit the section. A thin handoff (Goal + Next) is still a valid handoff.
