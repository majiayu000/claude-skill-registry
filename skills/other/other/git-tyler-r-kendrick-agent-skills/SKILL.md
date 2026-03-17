---
name: git
description: |
    Use when working with Git version control — branching strategies, common workflows, conflict resolution, history manipulation, hooks, and configuration. Covers everyday commands through advanced operations like rebase, cherry-pick, bisect, and worktrees.
    USE FOR: git, version control, branching, merging, rebasing, git hooks, git workflows, Gitflow, trunk-based development, cherry-pick, bisect, stash, worktrees, git configuration, .gitignore, git aliases
    DO NOT USE FOR: GitHub/GitLab platform features (use platform-specific skills), CI/CD pipeline configuration, Git LFS administration
license: MIT
metadata:
  displayName: "Git"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Git Documentation"
    url: "https://git-scm.com/doc"
  - title: "Pro Git Book (Official)"
    url: "https://git-scm.com/book/en/v2"
  - title: "Git GitHub Repository"
    url: "https://github.com/git/git"
---

# Git

## Overview

Git is the universal version control system. Mastering it means understanding not just the commands but the model -- commits are snapshots (not diffs), branches are lightweight pointers to commits, and the staging area (index) separates what you have changed from what you intend to commit. Every operation in Git manipulates this underlying graph of commits, and once you internalize that model, even advanced operations become intuitive.

## Configuration

Set up Git globally after installation. These settings live in `~/.gitconfig`:

```bash
# Identity
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Line endings (critical for cross-platform teams)
git config --global core.autocrlf input    # macOS/Linux
git config --global core.autocrlf true     # Windows

# Default branch name
git config --global init.defaultBranch main

# Pull strategy
git config --global pull.rebase true       # Rebase instead of merge on pull

# Useful aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.unstage "reset HEAD --"
```

Verify your configuration:

```bash
git config --list --show-origin
```

## Everyday Commands

### Starting a Repository

```bash
# Create a new repository
git init my-project
cd my-project

# Clone an existing repository
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git          # SSH
git clone --depth 1 https://github.com/user/repo.git  # Shallow clone (latest commit only)
```

### Working with Changes

```bash
# Check status of working directory and staging area
git status
git status -s                        # Short format

# View changes
git diff                             # Unstaged changes
git diff --staged                    # Staged changes (about to be committed)
git diff HEAD                        # All changes since last commit

# Stage changes
git add file.txt                     # Stage a specific file
git add src/                         # Stage an entire directory
git add -p                           # Interactively stage hunks (partial file staging)

# Commit
git commit -m "feat: add user authentication"
git commit -am "fix: correct null check"   # Stage tracked files + commit in one step

# Undo changes
git restore file.txt                 # Discard unstaged changes to a file
git restore --staged file.txt        # Unstage a file (keep changes in working directory)

# Stash work in progress
git stash                            # Save current changes
git stash push -m "WIP: auth feature"  # Save with a description
git stash list                       # View all stashes
git stash pop                        # Apply most recent stash and remove it
git stash apply stash@{2}            # Apply a specific stash (keep it in the list)
git stash drop stash@{0}             # Remove a specific stash
git stash clear                      # Remove all stashes
```

### Branching

```bash
# List branches
git branch                           # Local branches
git branch -r                        # Remote branches
git branch -a                        # All branches

# Create and switch
git branch feature/auth              # Create a branch
git switch feature/auth              # Switch to it (modern)
git switch -c feature/auth           # Create and switch in one step
git checkout -b feature/auth         # Older equivalent

# Delete branches
git branch -d feature/auth           # Delete (only if merged)
git branch -D feature/auth           # Force delete (even if not merged)

# Merge
git switch main
git merge feature/auth               # Merge feature into main
git merge --no-ff feature/auth       # Force a merge commit (no fast-forward)

# Rebase
git switch feature/auth
git rebase main                      # Replay feature commits on top of main
```

### Working with Remotes

```bash
# View remotes
git remote -v

# Fetch latest changes (does NOT modify working directory)
git fetch origin
git fetch --all                      # Fetch from all remotes

# Pull (fetch + merge/rebase)
git pull                             # Fetch and merge (or rebase if configured)
git pull --rebase                    # Explicitly rebase on pull

# Push
git push origin main
git push -u origin feature/auth      # Push and set upstream tracking
git push --force-with-lease          # Safe force push (fails if remote has new commits)

# Add a remote
git remote add upstream https://github.com/original/repo.git
```

### Inspecting History

```bash
# Log
git log                              # Full log
git log --oneline                    # Compact one-line format
git log --oneline --graph --all      # Visual branch graph
git log --since="2 weeks ago"        # Time-based filter
git log --author="Alice"             # Filter by author
git log -- path/to/file.txt          # History of a specific file

# Show a specific commit
git show abc1234

# Blame — who changed each line
git blame src/app.py
git blame -L 10,20 src/app.py       # Blame specific line range

# Diff between branches
git diff main..feature/auth
git diff main...feature/auth         # Changes since branch diverged
```

## Branching Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| **Trunk-Based Development** | Short-lived feature branches (hours to a few days), merge to `main` frequently. Often paired with feature flags. | Teams practicing CI/CD, high-velocity delivery |
| **Gitflow** | Long-lived `develop` branch plus `feature/*`, `release/*`, and `hotfix/*` branches. Structured and formal. | Teams with scheduled releases, enterprise projects |
| **GitHub Flow** | Feature branches off `main`, open a PR, code review, merge. Simple and effective. | Small to mid-size teams, continuous deployment |
| **GitLab Flow** | Environment branches (`main` -> `staging` -> `production`). Merges promote code through environments. | Teams needing environment tracking and approvals |

> **Modern default:** Trunk-based development is the recommended approach for most teams today. It reduces merge conflicts, encourages small incremental changes, and aligns with continuous integration and delivery practices.

## Merge vs Rebase

| Aspect | Merge | Rebase |
|--------|-------|--------|
| History | Preserves branch topology with a merge commit | Linear, clean history — as if work happened sequentially |
| Safety | Safe for shared branches | **Dangerous on shared branches** — rewrites commit hashes |
| Conflict resolution | Resolve once at merge time | Potentially resolve at each replayed commit |
| When to use | Merging feature branches into main (public) | Cleaning up local feature branch before merging |
| Command | `git merge feature` | `git rebase main` (from feature branch) |

> **Golden Rule:** Never rebase commits that have been pushed to a shared branch. Rebasing rewrites commit history, and if others have based work on the original commits, you will create divergent histories and cause significant confusion. Rebase is for local cleanup only.

```bash
# Typical rebase workflow (local feature branch)
git switch feature/auth
git fetch origin
git rebase origin/main          # Replay your commits on top of latest main
# Resolve any conflicts at each step
git switch main
git merge feature/auth          # Now it's a clean fast-forward
```

## Advanced Operations

### Cherry-Pick

Apply specific commits from one branch to another without merging the entire branch:

```bash
git cherry-pick abc1234                  # Apply a single commit
git cherry-pick abc1234 def5678          # Apply multiple commits
git cherry-pick abc1234 --no-commit      # Apply changes but don't commit (stage only)
```

### Bisect

Binary search to find the commit that introduced a bug:

```bash
git bisect start
git bisect bad                           # Current commit is broken
git bisect good v1.0.0                   # This tag/commit was known good

# Git checks out a midpoint commit. Test it, then:
git bisect good                          # If this commit works
git bisect bad                           # If this commit is broken

# Repeat until Git identifies the first bad commit
# When done:
git bisect reset                         # Return to original branch
```

Automate bisect with a test script:

```bash
git bisect start HEAD v1.0.0
git bisect run ./test-script.sh          # Script exits 0 for good, 1 for bad
```

### Worktrees

Work on multiple branches simultaneously without stashing or switching:

```bash
# Create a new worktree for a branch
git worktree add ../hotfix-branch hotfix/urgent-fix

# List all worktrees
git worktree list

# Remove a worktree when done
git worktree remove ../hotfix-branch
```

### Reflog

The reflog records every change to HEAD. It is your safety net for recovering "lost" commits:

```bash
# View reflog
git reflog

# Recover a "lost" commit after a bad reset or rebase
git reflog
# Find the commit hash you want to return to
git reset --hard abc1234

# Recover a deleted branch
git reflog
git branch recovered-branch abc1234
```

> The reflog keeps entries for approximately 90 days by default. If you made a mistake, you almost certainly can recover from it.

### Interactive Rebase (Local Only)

Squash, reorder, edit, or drop commits before pushing:

```bash
# Rebase the last 4 commits interactively
git rebase -i HEAD~4
```

In the editor, change `pick` to:
- `squash` (or `s`) — combine with previous commit
- `reword` (or `r`) — change commit message
- `edit` (or `e`) — pause to amend the commit
- `drop` (or `d`) — remove the commit entirely

> Only use interactive rebase on commits that have **not** been pushed to a shared branch.

## Conflict Resolution

When Git cannot automatically merge changes, it marks conflicts in the affected files:

### Step-by-Step

1. **Identify conflicted files:**
   ```bash
   git status    # Lists files with "both modified" status
   ```

2. **Open the file and understand the conflict markers:**
   ```
   <<<<<<< HEAD
   // Your changes on the current branch
   const timeout = 5000;
   =======
   // Their changes from the incoming branch
   const timeout = 10000;
   >>>>>>> feature/update-timeout
   ```

3. **Decide which changes to keep** (yours, theirs, or a combination). Edit the file to the correct final state and remove all conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).

4. **Stage the resolved file and continue:**
   ```bash
   git add src/config.js
   git commit                            # For merge conflicts
   # or
   git rebase --continue                 # For rebase conflicts
   ```

**Merge tools** can simplify visual conflict resolution:

```bash
git mergetool                            # Launch configured merge tool
git config --global merge.tool vscode    # Set VS Code as merge tool
```

## Git Hooks

Git hooks are scripts that run automatically at specific points in the Git workflow. They live in `.git/hooks/`.

| Hook | Trigger | Common Use |
|------|---------|------------|
| `pre-commit` | Before a commit is created | Linting, formatting, running quick tests |
| `commit-msg` | After commit message is written | Validate conventional commit format |
| `pre-push` | Before push to remote | Run full test suite, check for secrets |
| `prepare-commit-msg` | Before editor opens for message | Insert template, branch name, or ticket number |
| `post-merge` | After a merge completes | Install dependencies, rebuild |
| `pre-rebase` | Before rebase starts | Warn if rebasing published branch |

### Example: pre-commit Hook

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run linter
npm run lint
if [ $? -ne 0 ]; then
    echo "Linting failed. Fix errors before committing."
    exit 1
fi

# Check for debug statements
if grep -rn "console.log\|debugger\|binding.pry" --include="*.js" --include="*.ts" --include="*.rb" src/; then
    echo "Debug statements found. Remove them before committing."
    exit 1
fi
```

> **Husky** is the standard tool for managing Git hooks in Node.js projects. It lets you define hooks in `package.json` or `.husky/` and ensures all team members run the same hooks.

## .gitignore

The `.gitignore` file tells Git which files and directories to exclude from tracking.

### Pattern Syntax

```gitignore
# Comments start with #
*.log              # Ignore all .log files
!important.log     # But DO track this specific one
/build/            # Ignore build directory at repo root only
**/temp/           # Ignore temp directory at any depth
doc/**/*.pdf       # Ignore PDFs inside doc/ recursively
```

### Common Entries by Platform

```gitignore
# Dependencies
node_modules/
vendor/
.venv/
__pycache__/

# Build output
dist/
build/
bin/
obj/
*.dll
*.exe
*.o

# Environment and secrets
.env
.env.local
*.pem
credentials.json

# OS files
.DS_Store
Thumbs.db
Desktop.ini

# IDE files
.vscode/settings.json
.idea/
*.suo
*.user
*.swp
*~
```

### Global Gitignore

Set a global ignore file for files that should never be tracked on any repo on your machine:

```bash
git config --global core.excludesFile ~/.gitignore_global
```

Add OS-specific junk (`.DS_Store`, `Thumbs.db`) and editor temp files to the global file.

## Conventional Commits

A lightweight convention for writing structured commit messages that can be parsed by tooling:

### Format

```
type(scope): description

[optional body]

[optional footer(s)]
```

### Types

| Type | Purpose |
|------|---------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Formatting, white-space, semicolons (no logic change) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or correcting tests |
| `build` | Changes to build system or external dependencies |
| `ci` | Changes to CI configuration files and scripts |
| `chore` | Maintenance tasks, dependency bumps, tooling |

### Examples

```
feat(auth): add OAuth2 login with Google provider
fix(api): handle null response from payment gateway
docs(readme): add setup instructions for local development
refactor(db): extract connection pooling into separate module
test(auth): add integration tests for token refresh flow
build(deps): bump lodash from 4.17.20 to 4.17.21
ci(github): add CodeQL security scanning workflow
chore: update .gitignore for Python virtual environments
```

> Adding `!` after the type (e.g., `feat!: ...`) or including `BREAKING CHANGE:` in the footer signals a breaking change, which tools like `semantic-release` use to trigger major version bumps.

## Best Practices

- **Commit early and often.** Small, focused commits are easier to review, revert, and bisect than large monolithic ones. Each commit should represent a single logical change.
- **Write meaningful commit messages.** The subject line should explain *what* changed and *why* in imperative mood ("Add auth module", not "Added auth module" or "Adding auth module"). Use the body for context when needed.
- **Never force push to shared branches.** Force pushing rewrites history and can destroy teammates' work. Use `--force-with-lease` if you must, and only on your own feature branches.
- **Use .gitignore from day one.** Add it as the first file in any new repository. Include dependencies, build output, secrets, and OS artifacts. Use templates from gitignore.io or GitHub's collection.
- **Learn reflog for recovery.** Reflog is your undo history. Before panicking about a bad rebase or reset, check `git reflog` — the original commits are almost certainly still there.
- **Rebase local branches before merging.** Rebase your feature branch onto the latest `main` before creating a merge or pull request. This results in a clean, linear history and avoids unnecessary merge commits.
- **Sign commits in sensitive repositories.** Use GPG or SSH signing (`git config --global commit.gpgsign true`) for repositories where commit authorship integrity matters.
- **Review diffs before committing.** Always run `git diff --staged` before committing to verify you are committing exactly what you intend. Catching stray debug statements or unrelated changes at this stage saves time.
