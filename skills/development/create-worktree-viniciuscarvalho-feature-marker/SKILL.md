---
name: create-worktree
description: Create and bootstrap a git worktree for isolated development work.
argument-hint: <name> [--spec=<path>] [--base=<branch>] [--no-bootstrap]
allowed-tools:
  - Bash(git worktree *)
  - Bash(git branch *)
  - Read
  - Write
---

# Create Worktree

Creates and bootstraps a git worktree for isolated development work.

## Arguments

- `name` (required): Name for the worktree directory and branch
- `--spec=<path>`: Path to a spec file to copy into the worktree's specs directory
- `--base=<branch>`: Base branch to create worktree from (default: current branch or configured default)
- `--no-bootstrap`: Skip the onBootstrap hook

## Configuration

Check for `.claude/spec-workflow/config.yaml`:

```yaml
paths:
  worktrees: "./worktrees"      # Where worktrees are created
  specs: "./specs"              # Where specs live (for copying)

worktree:
  branchNaming: "{name}"        # Branch naming pattern
  defaultBase: null             # Default base branch (null = current)
  onBootstrap: null             # Hook script to run after creation
```

### Branch Naming

The `branchNaming` pattern supports these tokens:
- `{name}` - The worktree name
- `{date}` - Current date (YYYY-MM-DD)

Examples:
- `"{name}"` → `my-feature`
- `"feature/{name}"` → `feature/my-feature`
- `"{date}-{name}"` → `2024-01-15-my-feature`

### Bootstrap Hook

If `worktree.onBootstrap` is configured, it runs after worktree creation with these environment variables:

| Variable | Description |
|----------|-------------|
| `WORKTREE_PATH` | Absolute path to the new worktree |
| `WORKTREE_NAME` | Name of the worktree |
| `SPEC_FILE` | Path to spec file (if --spec was provided) |
| `BASE_BRANCH` | Branch the worktree was created from |

Example hook script:
```bash
#!/bin/bash
cd "$WORKTREE_PATH"
npm install
# ... any other setup
```

---

## Steps

1. **Check if worktree exists**
   - Check if a worktree with the given name already exists at the configured path
   - If it does, respond with "Worktree already exists at [path]" and exit
   - If it does not exist, proceed

2. **Determine paths and branch name**
   - Worktree path: `{config.paths.worktrees}/{name}` (default: `./worktrees/{name}`)
   - Branch name: Apply `branchNaming` pattern (default: `{name}`)
   - Base branch: `--base` argument, or `worktree.defaultBase`, or current branch

3. **Create the worktree**
   ```bash
   git worktree add -b [branch-name] [worktree-path] [base-branch]
   ```

4. **Notify the user**
   ```
   Worktree created at [path] on branch [branch-name].
   ```

5. **Handle spec file** (if --spec provided)
   - Copy the spec file to the worktree's specs directory
   - Update spec frontmatter with worktree and branch info

6. **Run bootstrap hook** (unless --no-bootstrap)
   - If `worktree.onBootstrap` is configured, run it with environment variables
   - If not configured, skip this step
   - Report success or failure

7. **Final confirmation**
   ```
   Worktree ready at [path].

   To work in this worktree:
   - Open a new terminal in [path]
   - Or use: cd [path]
   ```

---

## Example Usage

```bash
# Basic worktree creation
/create-worktree feature-login

# Create worktree with a spec file
/create-worktree user-notifications --spec=specs/2024-01-15-notifications-spec.md

# Create worktree from a different base branch
/create-worktree hotfix-auth --base=release/v2.0

# Create worktree without running bootstrap
/create-worktree quick-fix --no-bootstrap
```

---

## Notes

- Worktrees are typically gitignored (add `worktrees/` to `.gitignore`)
- Each worktree has its own working directory but shares git history
- Worktrees allow parallel work on different features without stashing
- Use `/worktree-cleanup` (if available) to remove stale worktrees
