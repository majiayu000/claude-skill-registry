---
name: git-worktree-clone
description: Clone a Git repository as bare repo and set it up for git worktrees workflow. Use when the user says "clone as bare repo", "setup git worktrees", "worktree clone", or asks to clone a repo for worktree usage.
allowed-tools: Bash, AskUserQuestion
---

# Git Worktree Clone

Clone a Git repository as a bare repository and configure it for git worktrees workflow.

## Arguments

The skill accepts optional arguments in the format:

- `/git-worktree-clone <repo-url>` - Clone with auto-detected directory name
- `/git-worktree-clone <repo-url> <directory-name>` - Clone with custom directory name

## Instructions

1. **Parse arguments:**
   - If args provided: extract repo URL (first arg) and optional directory name (second arg)
   - If no args: ask for repository URL
   - Directory name: use provided name, or derive from repo URL (last part without .git)
2. **Determine directory name** if not provided (default: derive from repo URL)
3. **Create directory structure** (use absolute path for `<repo-path>`):
   ```bash
   mkdir -p <repo-path>
   git clone --bare <repo-url> <repo-path>/.git
   ```
4. **Configure remote tracking** (use `-C` to target the repo):
   ```bash
   git -C <repo-path> config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
   ```
5. **Delete local branches** created during clone:
   ```bash
   git -C <repo-path> branch | sed 's/^[* ]*//' | xargs -r git -C <repo-path> branch -D
   ```
6. **Fetch remote branches:**
   ```bash
   git -C <repo-path> fetch
   ```
7. **Verify setup:**
   ```bash
   git -C <repo-path> branch -a  # Should show only remotes/origin/* branches
   git -C <repo-path> worktree list  # Should show only bare repo
   ```
8. **Create main worktree with tracking:**
   ```bash
   git -C <repo-path> worktree add -b main main origin/main
   ```
9. **Ask user if they want to create additional worktree(s)**
   - If yes, create with: `git worktree add -b <branch> <path> origin/<branch>`

## Workflow explanation

This setup creates:

- **Bare repo** in `<directory-name>/.git` - central git database
- **Worktrees** as subdirectories - actual working copies of branches
- **Benefits:**
  - Multiple branches checked out simultaneously
  - Each branch in its own directory
  - No need to stash changes when switching branches
  - Shared git database saves space

## Example usage

```bash
# Clone with auto-detected name
/git-worktree-clone git@ssh.code.roche.com:rmd-devops/infrastructure/rmd-devops-networking.git

# Clone with custom directory name
/git-worktree-clone git@ssh.code.roche.com:rmd-devops/infrastructure/rmd-devops-networking.git my-network-repo
```

## Example structure

```
rmd-devops-networking/
├── .git/                    # Bare repository
├── main/                    # Worktree for main branch
└── feat/                    # Worktree for feature branch
```

## Rules

- MUST use absolute paths and `git -C <repo-path>` instead of `cd`
- MUST delete all local branches after clone (keep only remotes)
- MUST configure remote fetch before fetching
- MUST use `-b` flag when creating worktrees to create tracking branches
- MUST always create a main worktree tracking origin/main
- Ask before creating additional worktrees beyond main
- Verify the setup shows `(bare)` in `git worktree list`
