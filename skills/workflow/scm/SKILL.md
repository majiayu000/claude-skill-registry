---
name: scm
description: Source code management workflow - nothing is ever lost
---

# Source Code Management

jj workflow for preserving all work. Nothing is ever lost.

## Core Principle

**Every change is automatically tracked.** In jj, working copy (`@`) is always a commit. No staging area. Every save is part of the current commit.

## Rules

1. **Commit after every testable change** - After each TDD cycle, run `jj commit -m "msg"`. Don't batch. Worktree gets squash-merged anyway.

2. **Finalize before destructive ops** - Before `jj restore`, `jj abandon`, or ending session: commit first.

3. **Experiments: commit, try, backout** - Commit the experiment, evaluate, then `jj backout -r @-` if discarding. History preserved.

4. **Unknown changes: preserve first** - Never `jj restore` unknown changes. Commit checkpoint, then investigate with `jj diff -r @-`.

5. **Deleting code: commit, then delete** - Checkpoint before removing so you can recover from history.

## Why This Matters

- **Recovery**: Any past state is one `jj edit` away
- **Confidence**: Experiment freely knowing nothing is lost
- **Squash merge**: All commits collapse to one clean commit at release

## Anti-patterns

| Don't | Do Instead |
|-------|------------|
| `jj restore` without thinking | Commit first |
| `jj abandon` without checking | Verify commit is unwanted |
| Batch changes in one commit | Commit after each testable change |
| Leave session without finalizing | Commit before stopping |
