---
name: sitrep
description: Start-of-session situational report for a research or code repository. Reads whatever handoff, log, or status artifacts the project actually keeps, checks live git state, and reports the current objective, verified baseline, open tasks, blockers, and next actions. Use when resuming work in a repository after time away, or when you need to know where a project stands before changing anything. Its end-of-session twin is finished.
---

# Situational report

Answer one question: **where does this project actually stand right now?** The value is in the gap between what the project's own documents claim and what the repository shows. Report the gap; never launder a stale document into a current fact.

## 0. Defer to the repository first

`Glob` for `.codex/prompts/*sitrep*.md`, `.codex/prompts/*status*.md`, and the same patterns under `.claude/commands/` — they catch variants such as `project-sitrep.md`. If one matches, `Read` it, follow its instructions instead of the steps below, and say which file you used. If several match, pick the closest name and say which. Otherwise continue here.

## 1. Learn the project's conventions

Read `AGENTS.md` and `CLAUDE.md` if present; they usually state the handoff or logging convention. Fall back to `README.md` for orientation. Then find the project's own memory: `HANDOFF.md`, `CODEX_HANDOFF.md`, `STATUS.md`, `SESSION_LOG.md`, `NOTES.md`, or a `logs/` directory with dated entries.

Use what the project has. If it keeps none, say so plainly — do not invent a format it does not use.

## 2. Check live state

```
git status --short
git log --oneline -n 8
git branch --show-current
git status -sb | head -1
```

Two failure modes are worth the extra commands. **A detached or behind branch:** if `git status -sb` shows divergence from the upstream, run `git fetch` and report the true position — a local branch can be many commits behind while the working tree looks clean. **Working-tree drift:** if the project syncs files outside git (Syncthing, Dropbox, a shared mount), a large uncommitted diff may be someone else's committed work that this clone's `.git` has not seen. Check before treating it as local change.

## 3. Confirm load-bearing artifacts, only if the project names them

If `AGENTS.md` or `README.md` names specific data files, build outputs, or directories as load-bearing, spot-check that they exist. Skip this entirely when the project states no such convention.

## 4. Report

Order by priority, not by discovery order. Cite concrete paths and commands.

- **Current objective** — from the handoff document if one exists, otherwise inferred from recent commits and `README.md`. Say which.
- **Completed baseline** — what is done *and verified*. Distinguish "committed" from "verified"; they are not the same claim.
- **Open tasks** — what is queued, with the file or command each would start from.
- **Risks and blockers** — anything stale, missing, half-finished, or contradicted by what the repository shows.
- **Immediate next actions** — a short numbered list the user can approve in one line.

## 5. Flag staleness explicitly

If a handoff file references commits, artifacts, branches, or versions the live repository no longer matches, say so and propose the exact fix. A sitrep that repeats an outdated document is worse than no sitrep, because it converts a stale claim into an apparently fresh one.
