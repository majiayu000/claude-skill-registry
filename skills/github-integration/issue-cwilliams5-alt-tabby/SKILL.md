---
name: issue
description: Create a GitHub issue documenting the work done in this session
user-invocable: true
disable-model-invocation: true
---
Create a GitHub issue that documents the work from this session. Synthesize from all available context — don't just parrot a single source.

## Sources (in order of reliability)

1. **Plan** (if one exists) — the original intent, motivation, and scope
2. **Diff** (`git diff main...HEAD`) — what actually changed (always available)
3. **Surviving conversation context** — decisions, pivots, lessons (may be compacted)

The plan says what we set out to do. The diff says what we did. The delta between them is often the most interesting part.

## Content guidance

Include what's relevant from these categories, skip what isn't:

- **Goal** — what problem this solves or what it adds, and why
- **What changed** — summarize the diff meaningfully (not a file list)
- **Key decisions** — non-obvious choices worth documenting
- **Deviations** — where work diverged from the plan, and why
- **Surprises / lessons** — things discovered that weren't anticipated
- **Scope additions** — work added mid-session that wasn't in the original plan

Not every issue needs every section. A simple fix might just need goal + what changed. A complex feature might have all of them.

## Quality bar

Distill — do not dump. Omit rejected candidates, false positives, exploration noise, and investigation dead ends. Include investigation notes only if they have lasting documentation value or provide needed context for a future reader.

The test: would someone reading this in 3 months understand why this change exists and what's notable about it?

## After creating the issue

Report the issue number and URL. The subsequent PR must reference `Closes #N`.

If not already in a worktree, create one using the EnterWorktree tool and proceed with any remaining work.
