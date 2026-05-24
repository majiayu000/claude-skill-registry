---
name: agent-ops-git
description: "Manage git operations safely. Includes stale state detection, branch/commit management. Never pushes without explicit user confirmation."
category: git
invokes: [agent-ops-tasks]
invoked_by: [agent-ops-state, agent-ops-implementation, agent-ops-validation]
state_files:
  read: [constitution.md, focus.md, issues/*.md]
  write: [focus.md]
---

# Git Workflow (active-safe)

**Works with or without `aoc` CLI installed.** Issue tracking can be done via direct file editing.

## Git Commands

| Operation | Command | Notes |
|-----------|---------|-------|
| Check current branch | `git branch --show-current` | |
| Check current commit | `git rev-parse --short HEAD` | |
| Check uncommitted changes | `git status --porcelain` | |
| Create branch | `git checkout -b <branch>` | From constitution branch policy |
| Stage changes | `git add <files>` | |
| Commit | `git commit -m "..."` | Use structured message format |
| Stash work | `git stash push -m "..."` | |
| Unstash work | `git stash pop` | |
| View stash | `git stash list` | |
| Revert commit | `git revert <commit>` | Requires confirmation |

## Issue Integration (File-Based — Default)

| Operation | How to Do It |
|-----------|--------------|
| Start work | Edit issue in `.agent/issues/{priority}.md`: set `status: in_progress` |
| Close issue | Set `status: done`, add log entry with commit hash |

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`:

```bash
# Update issue when starting work
aoc issues update <ID> --status in-progress --log "Started work"

# Close issue when committing
aoc issues close <ID> --log "Fixed in commit abc123"
```

## Never Auto-Execute

```bash
# These require explicit user confirmation:
git push           # Never auto-push
git push --force   # Never force push
git branch -D      # Never delete branches
```

## Scope

- ✅ Detect stale state (authoritative source)
- ✅ Create feature branches
- ✅ Commit checkpoints with structured messages
- ✅ Detect uncommitted changes
- ✅ Stash/unstash work in progress
- ✅ Revert agent's own commits (with confirmation)
- ❌ Never push without explicit user request
- ❌ Never force push
- ❌ Never delete remote branches

## Stale State Detection (authoritative)

Called by `agent-ops-state` at session start. This is the single source of truth for staleness.

### Procedure

1. Read `.agent/focus.md` session info:
   - `branch`: expected branch name
   - `last_commit`: expected HEAD commit (short hash)
   - `last_updated`: timestamp

2. Get current git state:
   ```bash
   git branch --show-current    # current branch
   git rev-parse --short HEAD   # current commit
   git status --porcelain       # uncommitted changes
   ```

3. Compare and categorize:

   | Check | Mismatch | Severity | Action |
   |-------|----------|----------|--------|
   | Branch changed | focus says `main`, now on `feature-x` | ⚠️ WARN | Ask user |
   | Commit changed | focus says `abc123`, HEAD is `def456` | ⚠️ WARN | Ask user |
   | Uncommitted changes | `git status` shows changes | ℹ️ INFO | Note, may continue |
   | All match | — | ✅ OK | Continue |

4. If any WARN:
   ```
   ⚠️ State may be stale.
   - Expected branch: X, actual: Y
   - Expected commit: A, actual: B
   
   Options:
   A) Continue anyway (I made these changes)
   B) Update focus.md to current state
   C) Stop and investigate
   ```

## Branch Strategy

Read `.agent/constitution.md` for project-specific rules:
- Branch naming pattern
- When to create branches
- Whether to work on main directly

## Commit Message Format

Follow constitution format. Default:
```
[AgentOps] <type>: <short summary>

<body - what and why>

Task: T-XXXX
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

## Issue Reference in Commits

**Every commit should reference an issue ID:**

```
[AgentOps] fix: Resolve login timeout

Fixed the session expiry logic that was causing premature logouts.

Issue: BUG-0023@efa54f
```

If no issue exists for the work being committed:
```
⚠️ No issue found for this commit.

Create an issue first? [Y]es / [N]o, commit without issue

Note: All work should be tracked for auditability.
```

## Checkpoint Commits

Create commits at these moments:
- Before risky changes (labeled `[checkpoint]`)
- After each implementation step completes successfully
- Before switching tasks

## Rollback Procedure

When rolling back:
1. List commits made by agent (search for `[AgentOps]` prefix)
2. Show user what will be reverted
3. Ask for confirmation
4. Use `git revert` (not reset) to preserve history
