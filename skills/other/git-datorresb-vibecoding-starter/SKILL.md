---
name: git
description: Git hygiene for multi-agent collaborative work. Use when performing version control operations, syncing with remote, committing changes, or ensuring work is properly shared with the team.
---

# Git Skill

This skill covers git hygiene for multi-agent collaborative work.

## Core Principle: Pull First, Always

**This is a multi-agent team environment with rapid, concurrent changes.**

Before doing ANY local work—reading files, making edits, or starting a task—you MUST sync with remote:

```bash
git pull --rebase
```

### Why This Matters

Multiple agents (human and AI) are working on this repository simultaneously. Without pulling first:
- You may be reading **stale files** that have already been modified
- Your edits may create **merge conflicts** with work that's already on remote
- You risk **overwriting someone else's changes**

**When in doubt, pull.** It's always safe to pull; it's never safe to assume you're current.

## Sync Cadence

| Event | Git Action |
|-------|------------|
| **FIRST thing—before any action** | `git pull --rebase` |
| Before starting any task | `git pull --rebase` |
| Before reading files for context | `git pull --rebase` (if not just pulled) |
| After each meaningful edit | `git add . && git commit -m "..."` |
| After completing a task | `git push` |
| Before ending any session | Full sync and push |

## Commit Message Format

```
<type> #<issue-id>: <short description>

Types: feat, fix, docs, refactor, chore
```

Examples:
- `docs #12: Add RaaS pricing section to whitepaper`
- `fix #7: Correct diagram alignment in Stage A`
- `refactor #15: Reorganize repository architecture section`

## Session Completion Workflow

When ending a work session, complete ALL steps:

```bash
git add .
git commit -m "chore: session checkpoint"
git pull --rebase
git push
```

Then verify:

```bash
git status  # MUST show "up to date with origin"
```

### Critical Rules

- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing—that leaves work stranded locally
- NEVER say "ready to push when you are"—YOU must push
- If push fails, resolve conflicts and retry until it succeeds

## Quick Reference

```bash
git pull --rebase                       # FIRST! Get latest before ANY work
git add . && git commit -m "msg"        # Save work
git push                                # Share work
git status                              # Check state
```
