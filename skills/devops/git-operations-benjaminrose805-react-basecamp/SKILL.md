---
name: git-operations
description: Git command procedures for branch management, commits, and worktrees.
---

# Git Operations Skill

Git command procedures for branch management, commits, and worktrees.

## When Used

| Agent     | Phase       |
| --------- | ----------- |
| git-agent | All actions |

## CLI Tools

All operations use native git and GitHub CLI (`gh`):

```bash
# Verify gh CLI is authenticated
gh auth status

# If not authenticated, run:
gh auth login
```

**Note:** The github MCP server has been replaced with `gh` CLI commands. See pr-operations skill for PR-related commands.

## Procedures

### 1. Status

Show current git state:

```bash
git status
git log --oneline -5
git branch -vv
```

**Output:** Current branch, uncommitted changes, recent commits.

---

### 2. Branch Create

Create and switch to a new branch:

```bash
git checkout -b <type>/<name>
```

**Branch Types:**

| Prefix      | Use For           | Example                  |
| ----------- | ----------------- | ------------------------ |
| `feature/`  | New features      | `feature/prompt-manager` |
| `fix/`      | Bug fixes         | `fix/auth-timeout`       |
| `refactor/` | Code improvements | `refactor/api-cleanup`   |
| `docs/`     | Documentation     | `docs/api-reference`     |

**Validation:**

- Never create branch from dirty working directory
- Always branch from up-to-date main

```bash
git fetch origin
git checkout main
git pull origin main
git checkout -b <type>/<name>
```

---

### 3. Branch Switch

Switch to an existing branch:

```bash
git checkout <branch>
```

**With uncommitted changes:**

```bash
# Option 1: Stash changes
git stash
git checkout <branch>

# Option 2: Commit first
git add <files>
git commit -m "wip: save progress"
git checkout <branch>
```

---

### 4. Sync with Main

Update current branch with latest main:

```bash
git fetch origin
git rebase origin/main
```

**On conflict:**

```bash
# Fix conflicts in files
git add <resolved-files>
git rebase --continue
```

**If rebase is problematic:**

```bash
git rebase --abort
git merge origin/main
```

---

### 5. Commit

Create a conventional commit:

```bash
# Stage specific files (never use -A or .)
git add <file1> <file2>

# Commit with message
git commit -m "<type>: <description>

<optional body>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Commit Types:**

| Type       | Use For                                 |
| ---------- | --------------------------------------- |
| `feat`     | New feature                             |
| `fix`      | Bug fix                                 |
| `refactor` | Code change that neither fixes nor adds |
| `docs`     | Documentation only                      |
| `test`     | Adding or updating tests                |
| `chore`    | Maintenance, dependencies               |

**Pre-commit checks:**

```bash
pnpm lint && pnpm typecheck
```

---

### 6. Worktree Add

Create a new worktree for parallel development:

```bash
# Create worktree with new branch
git worktree add ../<repo>--<feature> -b feature/<feature>

# Create worktree from existing branch
git worktree add ../<repo>--<feature> feature/<feature>
```

**Example:**

```bash
git worktree add ../react-basecamp--prompt-manager -b feature/prompt-manager
```

**Directory structure:**

```
~/basecamp/
├── react-basecamp/                  # Main worktree (main branch)
├── react-basecamp--prompt-manager/  # Worktree for feature
└── react-basecamp--other-feature/   # Another worktree
```

---

### 7. Worktree Remove

Remove a worktree when done:

```bash
git worktree remove ../<repo>--<feature>
```

**If worktree has uncommitted changes:**

```bash
# Force remove (discards changes)
git worktree remove --force ../<repo>--<feature>

# Or commit/stash changes first
cd ../<repo>--<feature>
git stash
cd ../<repo>
git worktree remove ../<repo>--<feature>
```

---

### 8. Worktree List

Show all worktrees:

```bash
git worktree list
```

---

### 9. Cleanup

Delete merged branches:

```bash
# Delete local merged branches
git branch --merged main | grep -v "main" | xargs -r git branch -d

# Prune remote-tracking branches
git fetch --prune
```

## Error Handling

| Error             | How to Handle                            |
| ----------------- | ---------------------------------------- |
| Merge conflict    | Resolve manually, then continue          |
| Dirty working dir | Stash or commit before switching         |
| Branch exists     | Check if intentional, use different name |
| Worktree locked   | Remove lock file or use --force          |

## Output

Return operation result:

```markdown
## Git Operation: <action>

**Status:** SUCCESS / FAILED

**Details:**

- <operation-specific details>

**Current State:**

- Branch: `feature/prompt-manager`
- Uncommitted: 0 files
```
