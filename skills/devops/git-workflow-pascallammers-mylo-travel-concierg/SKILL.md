---
name: git-workflow
description: Manage source control effectively with Git including branching strategies, commit conventions, merge conflict resolution, rebasing, and collaboration workflows like GitHub Flow or GitFlow. Use when managing feature branches, creating meaningful commits, resolving merge conflicts, rebasing branches, squashing commits, using interactive rebase, implementing branch naming conventions, following commit message standards, managing pull requests, or collaborating in team environments.
---

# Git Workflow - Professional Version Control

## When to use this skill

- Managing feature branches and branch strategies
- Creating clear, meaningful commit messages
- Resolving merge conflicts effectively
- Rebasing branches to maintain clean history
- Squashing commits before merging
- Using interactive rebase to clean up history
- Implementing branch naming conventions
- Following commit message standards (Conventional Commits)
- Managing pull requests and code reviews
- Collaborating in team Git workflows
- Recovering from Git mistakes (reset, revert, reflog)
- Managing release branches and hotfixes

## When to use this skill

- Managing code changes, collaborating with teams, creating branches, handling conflicts, and maintaining clean git history.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Managing code changes, collaborating with teams, creating branches, handling conflicts, and maintaining clean git history.

## Core Principles

1. **Commit Often, Push When Stable** - Small, focused commits are easier to review and revert
2. **Main Branch is Sacred** - Always deployable, never commit directly
3. **Clear History Tells a Story** - Future developers read commit messages to understand why
4. **Review Before Sharing** - Check `git diff` before committing

## Essential Commands

### Starting Work

```bash
# Update local repository
git fetch origin
git pull origin main

# Create feature branch
git checkout -b feature/user-authentication
# Or: git switch -c feature/user-authentication

# Branch naming conventions:
# feature/description  - new feature
# fix/description      - bug fix
# refactor/description - code improvement
# docs/description     - documentation
```

### Making Changes

```bash
# Check what changed
git status                    # Overview
git diff                      # Unstaged changes
git diff --staged             # Staged changes
git diff main...HEAD          # All changes since branching

# Stage changes
git add path/to/file          # Specific file
git add path/to/directory     # Entire directory
git add -p                    # Interactive staging (recommended!)

# Commit with good message
git commit -m "feat: add user authentication endpoint

- Implement JWT token generation
- Add password hashing with bcrypt
- Create middleware for auth verification

Closes #123"
```

### Commit Message Format

**Use Conventional Commits:**

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code change that neither fixes a bug nor adds a feature
- `docs:` Documentation only
- `style:` Formatting, missing semicolons, etc.
- `test:` Adding tests
- `chore:` Maintenance tasks
- `perf:` Performance improvement

**Examples:**

```bash
# Good commits
git commit -m "feat: add user avatar upload"
git commit -m "fix: prevent race condition in order processing"
git commit -m "refactor: extract validation logic into separate module"

# Bad commits (too vague)
git commit -m "fix stuff"        # What stuff?
git commit -m "WIP"              # Never push WIP commits
git commit -m "asdf"             # Meaningless
```

### Viewing History

```bash
# Recent commits
git log --oneline -10

# Commits with diffs
git log -p -2

# Visual branch graph
git log --graph --oneline --all

# Find who changed a line
git blame path/to/file

# Search commit messages
git log --grep="authentication"

# Find commits by author
git log --author="alice"
```

### Branching & Merging

```bash
# List branches
git branch                    # Local
git branch -r                 # Remote
git branch -a                 # All

# Switch branches
git checkout main
# Or: git switch main

# Merge feature branch
git checkout main
git merge feature/user-auth   # Creates merge commit
git merge --squash feature/user-auth  # Squashes into one commit

# Delete branch after merge
git branch -d feature/user-auth       # Safe delete (merged only)
git branch -D feature/user-auth       # Force delete
git push origin --delete feature/user-auth  # Delete remote
```

### Handling Conflicts

```bash
# When merge conflict occurs:

# 1. See conflicted files
git status

# 2. Open files, resolve conflicts manually
# Look for: <<<<<<< HEAD, =======, >>>>>>> branch

# 3. Mark as resolved
git add path/to/resolved-file

# 4. Complete merge
git commit  # Will use default merge message

# Or abort merge
git merge --abort
```

**Conflict Example:**
```javascript
<<<<<<< HEAD
const apiUrl = 'https://api.prod.example.com';
=======
const apiUrl = 'https://api-v2.example.com';
>>>>>>> feature/update-api

// After resolution (choose appropriate version):
const apiUrl = 'https://api-v2.example.com';
```

### Undoing Changes

```bash
# Undo working directory changes (NOT staged)
git checkout -- path/to/file
# Or: git restore path/to/file

# Unstage file (keep changes)
git reset HEAD path/to/file
# Or: git restore --staged path/to/file

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) ⚠️ DANGEROUS
git reset --hard HEAD~1

# Revert a commit (creates new commit)
git revert abc123

# Amend last commit (before pushing)
git commit --amend
git commit --amend --no-edit  # Keep message
```

### Stashing

```bash
# Save work in progress
git stash

# Stash with message
git stash save "WIP: working on user profile"

# List stashes
git stash list

# Apply most recent stash
git stash apply

# Apply and remove from stash list
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Delete stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

### Rebasing

```bash
# Update branch with main changes
git checkout feature/user-auth
git rebase main

# Interactive rebase (clean up history)
git rebase -i HEAD~5

# During rebase:
# - pick: keep commit
# - reword: change commit message
# - squash: combine with previous commit
# - fixup: like squash but discard message
# - drop: remove commit

# Abort rebase if things go wrong
git rebase --abort

# Continue after resolving conflicts
git rebase --continue
```

**⚠️ Never rebase commits that have been pushed to shared branches!**

### Cherry-Picking

```bash
# Apply specific commit to current branch
git cherry-pick abc123

# Cherry-pick multiple commits
git cherry-pick abc123 def456

# Cherry-pick without committing (stage only)
git cherry-pick -n abc123
```

## Workflow Patterns

### Feature Branch Workflow

```bash
# 1. Create branch from main
git checkout main
git pull origin main
git checkout -b feature/new-feature

# 2. Make changes and commit
# ... work work work ...
git add .
git commit -m "feat: implement new feature"

# 3. Keep branch updated with main
git fetch origin
git rebase origin/main

# 4. Push to remote
git push origin feature/new-feature

# 5. Create pull request on GitHub/GitLab

# 6. After PR approved and merged, cleanup
git checkout main
git pull origin main
git branch -d feature/new-feature
```

### Gitflow Workflow

```bash
# Main branches:
# - main (production)
# - develop (integration)

# Supporting branches:
# - feature/* (new features)
# - release/* (release preparation)
# - hotfix/* (urgent fixes)

# Start feature
git checkout develop
git checkout -b feature/awesome-feature

# Finish feature
git checkout develop
git merge --no-ff feature/awesome-feature
git branch -d feature/awesome-feature

# Create release
git checkout develop
git checkout -b release/1.2.0
# ... bump version, update changelog ...
git checkout main
git merge --no-ff release/1.2.0
git tag -a v1.2.0 -m "Release 1.2.0"

# Hotfix
git checkout main
git checkout -b hotfix/critical-bug
# ... fix bug ...
git checkout main
git merge --no-ff hotfix/critical-bug
git checkout develop
git merge --no-ff hotfix/critical-bug
git tag -a v1.2.1 -m "Hotfix 1.2.1"
```

### Trunk-Based Development

```bash
# Everyone commits to main frequently
# Short-lived feature branches (<1 day)
# Feature flags for incomplete work

git checkout main
git pull origin main
git checkout -b feature/quick-change

# ... make small change ...
git commit -am "feat: add button"
git push origin feature/quick-change

# Create PR, get quick review, merge
# Delete branch immediately after merge
```

## Git Configuration

### Essential Config

```bash
# User identity
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Editor
git config --global core.editor "code --wait"  # VS Code
# Or: vim, nano, emacs, etc.

# Default branch name
git config --global init.defaultBranch main

# Helpful aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual 'log --graph --oneline --all'

# Auto-correct typos
git config --global help.autocorrect 20

# Colorful output
git config --global color.ui auto

# Push current branch only
git config --global push.default current

# Pull with rebase by default
git config --global pull.rebase true
```

### .gitignore

```bash
# Create global gitignore
git config --global core.excludesfile ~/.gitignore_global

# Common entries:
# OS files
.DS_Store
Thumbs.db

# Editor files
.vscode/
.idea/
*.swp
*.swo
*~

# Dependencies
node_modules/
venv/
vendor/

# Build outputs
dist/
build/
*.pyc
*.class

# Secrets
.env
.env.local
secrets.yml
*.pem

# Logs
*.log
logs/
```

## Advanced Techniques

### Git Worktrees

```bash
# Work on multiple branches simultaneously
git worktree add ../project-feature2 feature/feature2
cd ../project-feature2  # Separate directory, same repo

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../project-feature2
```

### Bisect (Find Breaking Commit)

```bash
# Binary search for bad commit
git bisect start
git bisect bad                # Current state is broken
git bisect good v1.0.0        # Last known good version

# Git checks out commit for testing
# Test manually or: git bisect run ./test.sh

git bisect good  # If test passes
git bisect bad   # If test fails

# Repeat until found
# git bisect reset to return to original state
```

### Reflog (Safety Net)

```bash
# See all recent actions (even after reset)
git reflog

# Recover "lost" commits
git checkout abc123  # From reflog

# Undo a bad reset
git reset --hard HEAD@{2}
```

## Best Practices

### ✅ Do

- Write clear, descriptive commit messages
- Commit logical units of change
- Review diffs before committing (`git diff --staged`)
- Pull before pushing
- Keep commits small and focused
- Use branches for all changes
- Delete branches after merging

### ❌ Don't

- Commit secrets or credentials
- Commit generated files (build artifacts)
- Commit directly to main
- Rewrite history on shared branches
- Create massive commits with unrelated changes
- Use vague commit messages
- Push broken code

## Troubleshooting

### Common Issues

**"Detached HEAD":**
```bash
# You checked out a commit directly
# To save work:
git checkout -b new-branch-name
```

**"Merge conflict in large file":**
```bash
# Use theirs or ours:
git checkout --theirs path/to/file  # Take their version
git checkout --ours path/to/file    # Keep our version
git add path/to/file
```

**"Accidentally committed to main":**
```bash
# Move commit to new branch
git branch feature/accidental
git reset --hard origin/main
git checkout feature/accidental
```

**"Pushed sensitive data":**
```bash
# Use BFG Repo Cleaner or git-filter-repo
# WARNING: Rewrites history, coordinate with team

# Then force push (⚠️ DANGEROUS)
git push --force-with-lease
```

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [Oh Shit, Git!?!](https://ohshitgit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**Remember**: Git is a time machine for your code. Use it to create checkpoints, explore alternative solutions safely, and maintain a clear history of why changes were made.
