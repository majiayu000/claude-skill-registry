---
name: sdv-session-start
description: ALWAYS invoke this skill FIRST at session start, after context reset/compaction, or when user mentions "reset", "new session", "where were we", "what was I working on". Do NOT skip this for specific task requests—orient first, then execute. This is Rule 0.
version: 1.1.0
---

# SDV Session Orientation

Quick ramp-up at the start of a development session. Gather context from journals, git state, and build status to understand where work left off.

## When to Use

1. Starting a new development session
2. After context compaction/reset
3. Resuming work after a break
4. Switching branches
5. When uncertain about current state

## Orientation Checklist

### 1. Identify Current Branch

```bash
git branch --show-current
```

Use the branch name to find the relevant journal file.

### 2. Read Branch Journal

```bash
# Journal files are named: YYYY-MM-DD_branch-name.md
ls Docs/journals/
```

Read the most recent journal for the current branch to understand:
- What work has been done
- What's in progress
- Known issues or blockers
- Build status from last session

### 3. Check Git Status

```bash
git status
git log --oneline -5
```

Understand:
- Uncommitted changes
- Recent commits
- Relationship to main branch

### 4. Verify Build Status

```bash
dotnet build
```

Confirm the project builds successfully before starting work.

### 5. Check for Pending Work

Review:
- Journal entries for incomplete tasks
- `Docs/ROADMAP.md` for planned features
- `Docs/BUGS.md` for known issues

## Orientation Report Template

Generate a brief orientation report:

```markdown
## Session Orientation

**Branch:** liminalwarmth/feature-name
**Date:** YYYY-MM-DD
**Build Status:** Passing / Failing

### Recent Activity
- [Summary of last journal entry]
- Last commit: [hash] [message]

### Current State
- [What's working]
- [What's in progress]
- [Any blockers]

### Next Steps
1. [Immediate task]
2. [Following task]

### Notes
- [Any context that might be forgotten]
```

## Quick Commands

```bash
# Full orientation
git branch --show-current && \
git status --short && \
git log --oneline -3 && \
dotnet build --verbosity quiet

# Find journal for current branch
BRANCH=$(git branch --show-current | sed 's/.*\///') && \
ls Docs/journals/*${BRANCH}*.md 2>/dev/null || echo "No journal found"
```

## Context Recovery

If context was compacted or reset:

1. **Read CLAUDE.md** - Always read the handbook first
2. **Read branch journal** - Understand what was being worked on
3. **Check git diff** - See what changes exist
4. **Run build** - Verify current state compiles
5. **Ask the user** - If unclear, ask for context

## Journal Location Convention

```
Docs/journals/
├── 2025-12-27_random-outfit-names.md
├── 2025-12-26_dresser-sharing.md
├── 2025-12-25_rings-config.md
└── _archive.md  (historical entries)
```

Journals are named with date and branch name for easy lookup.

## Branch Naming Convention

Branch names typically follow:
- `liminalwarmth/feature-name` for features
- `liminalwarmth/fix-name` for bug fixes
- `master` for main branch

The journal file uses the portion after the last `/`.
