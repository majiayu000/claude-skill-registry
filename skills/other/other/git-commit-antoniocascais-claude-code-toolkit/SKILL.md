---
name: git-commit
description: Plans and executes git commits with optional TICKET_ID prefix. Analyzes staged changes, proposes optimal commit structure (single or multiple), generates descriptive messages with technical context, and executes after user approval. Use when committing code changes, creating atomic commits, or splitting large changesets.
allowed-tools: Bash(git diff:*) Bash(git status:*) Bash(git log:*) Bash(git show:*)
---

# Git Commit Planning

Analyze staged changes and create optimal commit plan, then execute after user approval.

## Arguments

`$ARGUMENTS` may contain a TICKET_ID (e.g., `JIRA-123`, `GH-456`).
- If provided: prefix all commit messages with `TICKET_ID: `
- If empty: omit prefix, use descriptive message only

## Workflow

### 1. Confirm Commit Scope

```bash
git status --porcelain
```

Show user:
- Staged files (ready to commit)
- Unstaged changes (not included)
- Untracked files

Ask user to confirm scope:
- **Proceed with staged** - commit only what's staged
- **Add specific files** - stage additional files before commit
- **Stage all changes** - add all modified/untracked files
- **Let me stage manually** - exit and let user stage

If nothing to commit (no staged + no changes) → inform and exit.

### 2. Analyze Changes

Run in parallel:
```bash
git diff --staged --stat
git diff --staged --name-only
git log --oneline -5  # for message style reference
```

Assess:
- File count and types
- Lines changed
- Logical groupings (features, fixes, refactors)
- Whether changes should be split into multiple commits

### 3. Plan Commits

**Single commit** when:
- 1-3 related files
- Single logical change
- Coherent unit of work

**Multiple commits** when:
- Unrelated changes mixed together
- Multiple features/fixes in one staging
- Cross-functional changes (code + tests + docs should sometimes split)

### 4. Generate Messages

**Title format** (max 60 chars):
- With TICKET_ID: `TICKET-123: Add user authentication`
- Without: `Add user authentication middleware`

**Prefixes**: Add, Fix, Update, Refactor, Remove, Implement

**Body** (technical context for future readers):

Target ~50-150 words. Audience: technical people reading git history to understand WHY.

Style:
- Prose or bullets with substance (not terse lists)
- Explain the problem and why this solution
- Skip obvious details (diff shows what changed)

Anti-patterns:
- Single sentence ("Fixed the bug")
- Terse bullets ("- Added X", "- Removed Y")
- Multi-paragraph essays

**Example:**
```
TICKET-123: Fix memory leak in cache service

Cache entries weren't being cleaned up when TTL expired, causing
memory to grow unbounded under sustained load. This adds reference
counting to track active cache users and a cleanup routine in the
TTL handler that only removes entries with zero references.
```

### 5. Present Plan

Format:
```
COMMIT PLAN
===========

Files: X | Lines: +Y/-Z

Commit 1: [message title]
  file1.js (new)
  file2.ts (modified)

Body:
[technical explanation]

[If multiple commits, show each]

Approve? (yes/no/modify)
```

### 6. Execute

After approval:

**Single commit:**
```bash
git commit -m "title" -m "body"
```

**Multiple commits:**
1. `git reset` (unstage all)
2. For each commit:
   - `git add [specific files]`
   - `git commit -m "title" -m "body"`

### 7. Report

```bash
git log --oneline -3
git log -1 --format=medium
```

Show:
- Commits created
- Next steps (push, PR)

## Error Handling

- **Nothing to commit**: No staged or unstaged changes, inform and exit
- **Commit failure**: Show error, suggest fix
- **Title too long**: Truncate or split
