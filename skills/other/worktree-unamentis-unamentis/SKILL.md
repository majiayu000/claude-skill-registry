---
name: worktree
description: Manage git worktrees for parallel Claude Code development sessions
---

# /worktree - Parallel Development Management

## Purpose

Manages isolated development environments using git worktrees. Each worktree provides a separate working directory for independent Claude Code sessions, enabling 2-4 parallel development tasks.

**Key Benefit:** Complete file isolation between parallel tasks. No stashing or branch switching needed.

## Why Worktrees?

Git worktrees solve the problem of context switching during parallel development:

| Without Worktrees | With Worktrees |
|-------------------|----------------|
| `git stash` before switching branches | Each branch in its own directory |
| Risk of losing uncommitted work | Work preserved in each worktree |
| One task at a time | 2-4 tasks truly in parallel |
| Must wait for builds to finish | Each worktree builds independently |
| Single Claude Code session | Multiple independent sessions |

**How it works:** All worktrees share the same `.git` repository data (commits, branches, history) but have separate working directories. This means:
- Lightweight creation (no full clone needed)
- Changes in one worktree don't affect others
- All worktrees stay in sync with `git fetch`

## When to Use

| Scenario | Recommendation |
|----------|----------------|
| Working on feature while reviewing PR | Create worktree for review |
| Bug fix needed while mid-feature | Create worktree for fix |
| Experimenting with risky changes | Create worktree for experiment |
| Running long build while coding | Build in one worktree, code in another |
| Multiple related tasks for sprint | One worktree per task |

## Usage

```
/worktree list                    # List all worktrees with status
/worktree create <name>           # Create worktree with inferred branch
/worktree create <name> <branch>  # Create worktree for existing branch
/worktree open <name>             # Reopen worktree in VS Code
/worktree remove <name>           # Remove worktree (with safety checks)
/worktree status                  # Show current worktree context
/worktree cleanup                 # Clean DerivedData from inactive worktrees
```

## Naming Convention

Worktrees are created as siblings to the main repo with `unamentis-<name>` naming:

```
/Users/ramerman/dev/
├── unamentis/                    # Main repo
├── unamentis-kb-feature/         # Worktree: /worktree create kb-feature
└── unamentis-fix-crash/          # Worktree: /worktree create fix-crash
```

## Workflow

### `/worktree list`

1. Run `git worktree list -v`
2. For each worktree, show:
   - Path
   - Branch name
   - Whether it's the current worktree (marked with `*`)
   - DerivedData size if present
3. Show total count and disk usage

**Commands:**
```bash
git worktree list -v
# For each worktree path, check DerivedData:
du -sh <worktree>/DerivedData 2>/dev/null
```

### `/worktree create <name> [branch]`

1. **Validate name:** alphanumeric and hyphens only
2. **Infer branch** (if not specified):
   - `fix-*` → `fix/<rest>` (e.g., `fix-crash` → `fix/crash`)
   - `feat-*` or `feature-*` → `feature/<rest>`
   - `docs-*` → `docs/<rest>`
   - `refactor-*` → `refactor/<rest>`
   - `test-*` → `test/<rest>`
   - Default: `feature/<name>`
3. **Determine repo name:** Extract from current directory (e.g., `unamentis`)
4. **Create worktree:**
   ```bash
   git worktree add -b <branch> ../<repo>-<name>
   # Or for existing branch:
   git worktree add ../<repo>-<name> <branch>
   ```
5. **Auto-open in VS Code:**
   ```bash
   code ../<repo>-<name>
   ```
6. **Remind user:** "Run `/mcp-setup ios` in the new session"

### `/worktree open <name>`

1. Verify worktree exists at `../<repo>-<name>`
2. Open in VS Code:
   ```bash
   code ../<repo>-<name>
   ```
3. Remind about `/mcp-setup ios`

### `/worktree remove <name>`

1. **Check for uncommitted changes:**
   ```bash
   cd ../<repo>-<name> && git status --porcelain
   ```
   If dirty, warn and ask for confirmation.

2. **Check for unpushed commits:**
   ```bash
   cd ../<repo>-<name> && git log @{u}..HEAD --oneline 2>/dev/null
   ```
   If ahead of remote, warn and ask for confirmation.

3. **Remove worktree:**
   ```bash
   git worktree remove ../<repo>-<name>
   git worktree prune -v
   ```

### `/worktree status`

1. Detect if running in a worktree vs main repo:
   ```bash
   git rev-parse --is-inside-work-tree
   cat .git  # If file (not dir), this is a worktree
   ```
2. Show current branch
3. Show path to main repo
4. List sibling worktrees

### `/worktree cleanup`

1. List all worktrees with DerivedData:
   ```bash
   for wt in $(git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2); do
     if [ -d "$wt/DerivedData" ]; then
       du -sh "$wt/DerivedData"
     fi
   done
   ```
2. Identify inactive worktrees (not current)
3. Ask for confirmation
4. Remove DerivedData from confirmed worktrees:
   ```bash
   rm -rf <worktree>/DerivedData
   ```
5. Report space recovered

## Examples

**Create worktree for a feature:**
```
User: /worktree create kb-improvements
Claude: Creating worktree for parallel development...

Branch: feature/kb-improvements (inferred from name)
Path: /Users/ramerman/dev/unamentis-kb-improvements/

✓ Worktree created
✓ Opening in VS Code...

New window opened. Run /mcp-setup ios in the new session to configure MCP.
```

**Create worktree for a bug fix:**
```
User: /worktree create fix-answer-validation
Claude: Creating worktree for parallel development...

Branch: fix/answer-validation (inferred from 'fix-' prefix)
Path: /Users/ramerman/dev/unamentis-fix-answer-validation/

✓ Worktree created
✓ Opening in VS Code...

New window opened. Run /mcp-setup ios in the new session.
```

**Create worktree for existing branch:**
```
User: /worktree create review feature/knowledge-bowl-2
Claude: Creating worktree for parallel development...

Branch: feature/knowledge-bowl-2 (existing)
Path: /Users/ramerman/dev/unamentis-review/

✓ Worktree created
✓ Opening in VS Code...

New window opened. Run /mcp-setup ios in the new session.
```

**List all worktrees:**
```
User: /worktree list
Claude: Git Worktrees:

  * /Users/ramerman/dev/unamentis (main) ← current
    /Users/ramerman/dev/unamentis-kb-ui (feature/kb-ui)
      DerivedData: 2.3 GB
    /Users/ramerman/dev/unamentis-fix-crash (fix/crash)
      DerivedData: 1.8 GB

Total: 3 worktrees, 4.1 GB DerivedData
```

**Check current status:**
```
User: /worktree status
Claude: Worktree Status:

Location: /Users/ramerman/dev/unamentis-kb-ui (worktree)
Branch: feature/kb-ui
Main repo: /Users/ramerman/dev/unamentis

Sibling worktrees:
- unamentis-fix-crash (fix/crash)
```

**Remove a worktree:**
```
User: /worktree remove kb-ui
Claude: Checking worktree status...

⚠️  Warning: 2 uncommitted changes detected
⚠️  Warning: 3 commits not pushed to remote

Are you sure you want to remove unamentis-kb-ui? (This cannot be undone)
[After confirmation]
✓ Worktree removed
✓ Stale references pruned
```

**Clean up DerivedData:**
```
User: /worktree cleanup
Claude: Checking DerivedData in worktrees...

Worktrees with DerivedData:
- unamentis-kb-ui: 2.3 GB (inactive)
- unamentis-fix-crash: 1.8 GB (inactive)

Clean DerivedData from inactive worktrees? (4.1 GB)
[After confirmation]
✓ Cleaned 4.1 GB from 2 worktrees
```

## Typical Workflow

Here's a complete example of parallel development with 3 tasks:

### 1. Start Your Session

```
# In main repo, check current worktrees
/worktree list

Git Worktrees:
  * /Users/ramerman/dev/unamentis (main) ← current

Total: 1 worktree
```

### 2. Create Worktrees for Each Task

```
# Task 1: Knowledge Bowl UI improvements
/worktree create kb-ui

# Task 2: Fix answer validation bug
/worktree create fix-validation

# Task 3: Add regional config feature
/worktree create kb-regional
```

You now have 4 VS Code windows (main + 3 worktrees).

### 3. Configure Each Session

In each new VS Code window:
```
/mcp-setup ios
```

### 4. Work in Parallel

Each Claude Code session works independently:
- **Window 1 (main):** Coordination, PRs, main branch work
- **Window 2 (kb-ui):** UI implementation
- **Window 3 (fix-validation):** Bug investigation and fix
- **Window 4 (kb-regional):** Feature development

### 5. Merge and Cleanup

When a task is complete:
```
# In the worktree, push the branch
git push -u origin feature/kb-ui

# Create PR (from any worktree)
gh pr create

# After PR is merged, remove worktree
/worktree remove kb-ui
```

### 6. Periodic Maintenance

```
# Check disk usage
/worktree list

# Clean up build artifacts from inactive worktrees
/worktree cleanup
```

## Integration

- **Run `/mcp-setup ios`** in each new worktree session to configure MCP
- Each worktree has **independent MCP connections**
- `CLAUDE.md` is shared (read from the repo, same across all worktrees)
- Each VS Code window runs its own Claude Code session

## Disk Space Considerations

Each worktree accumulates its own build artifacts:

| Artifact | Typical Size | Location |
|----------|--------------|----------|
| Xcode DerivedData | 2-5 GB | `<worktree>/DerivedData/` |
| node_modules | 500 MB - 2 GB | `<worktree>/server/*/node_modules/` |
| Cargo target | 500 MB - 1 GB | `<worktree>/server/usm-core/target/` |

With 3-4 active worktrees, this can consume 10-20 GB. Use `/worktree cleanup` regularly.

## Troubleshooting

### "fatal: '<branch>' is already checked out"

You cannot have the same branch checked out in multiple worktrees. Solutions:
1. Use a different branch name for the new worktree
2. Switch the existing worktree to a different branch first

### "Worktree not found" when using `/worktree open`

The worktree directory may have been manually deleted. Run:
```bash
git worktree prune -v
```
Then create a new worktree.

### VS Code doesn't open new window

Ensure VS Code CLI is in your PATH:
```bash
which code
# Should return: /usr/local/bin/code or similar
```

If not found, open VS Code and run "Shell Command: Install 'code' command in PATH" from the command palette.

### MCP tools not working in worktree

Run `/mcp-setup ios` in each new worktree session. MCP connections are per-session, not shared.

### Worktree has stale .git reference

If a worktree's parent repo was moved, repair the reference:
```bash
git worktree repair
```

### Disk space running low

Run `/worktree cleanup` to remove DerivedData from inactive worktrees. For more aggressive cleanup:
```bash
# Remove all DerivedData across all worktrees
for wt in $(git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2); do
  rm -rf "$wt/DerivedData"
done
```

### Branch conflicts between worktrees

Each branch can only be checked out in one worktree at a time. Use `/worktree list` to see which worktree has which branch.

## Quick Reference

```bash
# Git worktree commands (for reference)
git worktree add -b <branch> <path>    # Create with new branch
git worktree add <path> <branch>       # Create for existing branch
git worktree list -v                   # List all worktrees
git worktree remove <path>             # Remove worktree
git worktree prune -v                  # Clean stale references
git worktree repair                    # Fix broken worktree references
```

## Related Skills

- `/mcp-setup` - Configure MCP for each worktree session
- `/validate` - Run before committing in any worktree
- `/service` - Services are shared across all worktrees (same ports)
