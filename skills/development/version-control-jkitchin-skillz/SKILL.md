---
name: version-control
description: |
  Expert guidance for Git version control, trunk-based development workflows, and GitHub best practices.
  Emphasizes Conventional Commits for clean history, short-lived feature branches, frequent integration,
  and professional collaboration patterns. Use when users need help with git commands, branching strategies,
  commit messages, PRs, merge conflicts, or git troubleshooting. Triggers include 'git,' 'commit,' 'branch,'
  'merge,' 'rebase,' 'PR,' 'pull request,' or version control questions.
allowed-tools: "*"
---

# Version Control & Git Workflow Skill

Guide users through professional version control practices using Git with trunk-based development, Conventional Commits, and GitHub integration.

## Core Philosophy

**Trunk-Based Development:**
- Keep main branch always deployable
- Short-lived feature branches (days, not weeks)
- Frequent integration to main
- Small, incremental changes
- Continuous integration mindset

**Conventional Commits:**
- Structured, semantic commit messages
- Enables automated tooling (changelogs, versioning)
- Clear intent and scope in history
- Searchable, filterable commits

**GitHub Integration:**
- Pull requests for code review
- Branch protection for main
- CI/CD with GitHub Actions
- Clear PR descriptions and discussions

## Trunk-Based Development Workflow

### The Main Branch
- **Always deployable** - Main branch should always be in working state
- **Protected** - Require PRs, reviews, passing CI
- **Source of truth** - All branches stem from and merge back to main
- **No long-lived branches** - Avoid develop, staging branches

### Feature Branch Workflow

**1. Start from main:**
```bash
git checkout main
git pull origin main
git checkout -b feat/user-authentication
```

**2. Make small, focused changes:**
- One feature/fix per branch
- Commit frequently with Conventional Commits
- Keep branch lifespan short (1-3 days ideal)

**3. Stay synchronized:**
```bash
# Update from main frequently
git checkout main
git pull origin main
git checkout feat/user-authentication
git rebase main  # Keep history linear
```

**4. Push and create PR:**
```bash
git push -u origin feat/user-authentication
# Create PR on GitHub
```

**5. After PR approval:**
```bash
# Squash merge or merge commit to main
# Delete feature branch immediately
git checkout main
git pull origin main
git branch -d feat/user-authentication
```

### Branch Naming Conventions

**Pattern: `<type>/<short-description>`**

Types match Conventional Commit types:
- `feat/add-oauth-login` - New feature
- `fix/authentication-timeout` - Bug fix
- `refactor/database-queries` - Code refactoring
- `docs/api-endpoints` - Documentation
- `test/user-service` - Tests only
- `chore/update-dependencies` - Maintenance

Keep descriptions short, lowercase, hyphen-separated.

## Conventional Commits

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Required:** type, subject
**Optional:** scope, body, footer

### Types

**feat:** New feature for users
```
feat(auth): add OAuth2 authentication
```

**fix:** Bug fix
```
fix(api): handle null response in user endpoint
```

**docs:** Documentation changes
```
docs(readme): update installation instructions
```

**style:** Code style/formatting (no logic change)
```
style(components): fix indentation in Button
```

**refactor:** Code restructuring (no behavior change)
```
refactor(database): extract query builder class
```

**perf:** Performance improvement
```
perf(images): implement lazy loading
```

**test:** Adding or updating tests
```
test(auth): add integration tests for login flow
```

**build:** Build system or dependencies
```
build(deps): upgrade React to v18.2
```

**ci:** CI/CD configuration
```
ci(github): add automated deployment workflow
```

**chore:** Maintenance tasks
```
chore(deps): update development dependencies
```

**revert:** Revert previous commit
```
revert: revert "feat(auth): add OAuth2 authentication"
```

### Scope

Optional but recommended. Indicates what part of codebase changed:
- `feat(api):` - API changes
- `fix(ui):` - UI fix
- `refactor(database):` - Database refactoring
- `feat(auth):` - Authentication feature

Use project-specific scopes that make sense for your codebase.

### Subject Rules

- Use imperative mood: "add" not "added" or "adds"
- No capitalization of first letter
- No period at the end
- Keep under 50 characters
- Complete the sentence: "If applied, this commit will..."

**Good:**
```
feat(api): add user profile endpoint
fix(auth): prevent token expiration race condition
```

**Bad:**
```
feat(api): Added user profile endpoint.
fix(auth): Fixes a bug
Update stuff
```

### Body (Optional)

- Explain **what** and **why**, not **how**
- Wrap at 72 characters
- Separate from subject with blank line
- Use bullet points for multiple points

```
feat(search): implement full-text search

- Add PostgreSQL full-text search indexes
- Create search API endpoint with pagination
- Implement search result ranking by relevance

This enables users to search across all content with better
performance than previous LIKE queries.
```

### Footer (Optional)

**Breaking changes:**
```
feat(api): change authentication endpoint

BREAKING CHANGE: /auth/login moved to /api/v2/auth/login
```

**Issue references:**
```
fix(ui): prevent modal from closing on backdrop click

Fixes #123
Closes #456
```

### Examples

**Simple feature:**
```
feat(dashboard): add user activity chart
```

**Bug fix with details:**
```
fix(api): handle network timeout errors

Previously, network timeouts would crash the application.
Now we catch timeout errors and return appropriate error
response to client.

Fixes #789
```

**Breaking change:**
```
feat(api)!: redesign user authentication

BREAKING CHANGE: Auth tokens now expire after 1 hour instead
of 24 hours. Clients must implement token refresh logic.
```

**Multiple changes:**
```
refactor(database): optimize query performance

- Add indexes on frequently queried columns
- Implement connection pooling
- Cache common queries with Redis
- Update ORM configuration for better performance

These changes reduce average query time from 200ms to 50ms.
```

See `references/conventional-commits.md` for comprehensive guide.

## Essential Git Commands

### Daily Commands

**Check status:**
```bash
git status                    # See working tree status
git diff                      # Show unstaged changes
git diff --staged            # Show staged changes
```

**Make commits:**
```bash
git add <file>               # Stage specific file
git add .                    # Stage all changes
git commit -m "type: message" # Commit with message
git commit                   # Open editor for commit message
```

**Sync with remote:**
```bash
git pull origin main         # Fetch and merge from main
git push origin <branch>     # Push branch to remote
git fetch origin            # Fetch without merging
```

**Branch management:**
```bash
git branch                   # List local branches
git branch -a               # List all branches (including remote)
git checkout -b <branch>    # Create and switch to branch
git checkout <branch>       # Switch to existing branch
git branch -d <branch>      # Delete local branch
```

### Workflow Commands

**Update feature branch from main:**
```bash
git checkout main
git pull origin main
git checkout feat/my-feature
git rebase main             # Keep linear history
# Resolve conflicts if any
git push --force-with-lease origin feat/my-feature
```

**Amend last commit:**
```bash
git commit --amend          # Edit last commit message/content
git commit --amend --no-edit # Add changes to last commit
```

**Unstage changes:**
```bash
git reset HEAD <file>       # Unstage file
git reset HEAD .           # Unstage all
```

**Discard changes:**
```bash
git checkout -- <file>      # Discard changes in file
git restore <file>         # Modern alternative
git clean -fd              # Remove untracked files/dirs
```

**Stash changes:**
```bash
git stash                   # Stash working changes
git stash push -m "message" # Stash with message
git stash list             # List stashes
git stash apply            # Apply most recent stash
git stash pop              # Apply and remove stash
git stash drop             # Remove stash
```

**View history:**
```bash
git log                     # Show commit history
git log --oneline          # Compact history
git log --graph            # Visual branch graph
git log -p                 # Show patches
git log --follow <file>    # Follow file history
```

**Compare branches:**
```bash
git diff main..feat/branch  # Changes in branch vs main
git log main..feat/branch   # Commits in branch not in main
```

See `references/git-commands.md` for complete command reference.

## GitHub Pull Request Workflow

### Creating a PR

**1. Push branch:**
```bash
git push -u origin feat/user-authentication
```

**2. Create PR on GitHub with:**

**Title:** Use Conventional Commit format
```
feat(auth): add OAuth2 authentication
```

**Description template:**
```markdown
## Summary
Brief description of changes and motivation.

## Changes
- List key changes
- Use bullet points
- Be specific

## Testing
How to test these changes:
1. Step-by-step instructions
2. Expected behavior

## Screenshots (if UI changes)
[Add screenshots]

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Follows Conventional Commits
```

**3. Request reviewers**
**4. Link related issues**

### Reviewing PRs

**As reviewer:**
- Check code quality and style
- Verify tests are adequate
- Test functionality locally
- Ask questions, suggest improvements
- Approve or request changes

**PR review checklist:**
- [ ] Code follows project conventions
- [ ] Changes are well-tested
- [ ] No unnecessary changes included
- [ ] Documentation updated if needed
- [ ] Commit messages follow Conventional Commits
- [ ] No security vulnerabilities introduced
- [ ] Performance implications considered

### Addressing Review Feedback

**1. Make requested changes:**
```bash
# Make changes in your branch
git add .
git commit -m "fix(auth): address PR feedback"
git push origin feat/user-authentication
```

**2. Respond to comments**
**3. Mark conversations as resolved**
**4. Request re-review**

### Merging PRs

**Merge strategies:**

**Squash and merge (recommended for most features):**
- Combines all commits into one
- Clean main branch history
- Loses detailed commit history
- Good for: Features with many small commits

**Merge commit (for collaborative branches):**
- Preserves all commits
- Shows branch history
- Can clutter main history
- Good for: Complex features with meaningful commit history

**Rebase and merge (for clean branches):**
- Applies commits directly to main
- Linear history
- Requires clean branch history
- Good for: Branches with well-crafted commits

**After merge:**
```bash
# Delete remote branch (or use GitHub auto-delete)
git push origin --delete feat/user-authentication

# Update local main
git checkout main
git pull origin main

# Delete local branch
git branch -d feat/user-authentication
```

See `references/github-workflow.md` for detailed GitHub guidance.

## Branch Protection Rules

**Configure on GitHub for main branch:**

**Required:**
- [x] Require pull request before merging
- [x] Require approvals (at least 1)
- [x] Require status checks to pass
- [x] Require branches to be up to date

**Recommended:**
- [x] Require conversation resolution
- [x] Require linear history
- [x] Do not allow bypassing settings
- [x] Automatically delete head branches

**Optional (for teams):**
- [ ] Require review from Code Owners
- [ ] Restrict push access
- [ ] Require signed commits

## Handling Merge Conflicts

### When conflicts occur

**During merge:**
```bash
git merge main
# CONFLICT in file.py
```

**During rebase:**
```bash
git rebase main
# CONFLICT in file.py
```

### Resolution process

**1. View conflicts:**
```bash
git status  # Shows conflicted files
```

**2. Open conflicted file:**
```python
<<<<<<< HEAD
# Your changes
=======
# Their changes
>>>>>>> main
```

**3. Resolve manually:**
- Choose one version, or
- Combine both, or
- Write new solution

**4. Mark as resolved:**
```bash
git add file.py
```

**5. Continue operation:**
```bash
# For merge:
git commit

# For rebase:
git rebase --continue
```

**6. Abort if needed:**
```bash
# For merge:
git merge --abort

# For rebase:
git rebase --abort
```

### Preventing conflicts

- Pull/rebase from main frequently
- Keep branches short-lived
- Coordinate with team on overlapping work
- Make small, focused changes

See `references/troubleshooting.md` for complex conflict scenarios.

## Common Workflows

### Starting New Feature

```bash
# 1. Ensure main is current
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feat/new-feature

# 3. Make changes and commit
git add .
git commit -m "feat(module): add new functionality"

# 4. Push and create PR
git push -u origin feat/new-feature
# Create PR on GitHub
```

### Quick Bug Fix

```bash
# 1. Create fix branch from main
git checkout main
git pull origin main
git checkout -b fix/bug-description

# 2. Fix and commit
git add .
git commit -m "fix(module): resolve bug description"

# 3. Push and create PR
git push -u origin fix/bug-description
# Create PR with "Fixes #issue-number"
```

### Updating Branch from Main

```bash
# Option 1: Rebase (preferred for clean history)
git checkout feat/my-feature
git fetch origin
git rebase origin/main
# Resolve conflicts if any
git push --force-with-lease origin feat/my-feature

# Option 2: Merge (preserves branch history)
git checkout feat/my-feature
git fetch origin
git merge origin/main
git push origin feat/my-feature
```

### Splitting Large Branch

```bash
# If branch too large, split into smaller PRs:

# 1. Create first sub-feature
git checkout -b feat/user-auth-part1 feat/user-auth
git rebase -i main  # Mark only first commits as pick
git push -u origin feat/user-auth-part1
# Create PR for part 1

# 2. After part 1 merges, continue with part 2
git checkout main
git pull origin main
git checkout -b feat/user-auth-part2 feat/user-auth
# Continue with remaining commits
```

## Git Best Practices

### Commit Practices

✅ **Do:**
- Commit frequently (multiple times per day)
- Keep commits focused (one logical change)
- Write meaningful commit messages
- Follow Conventional Commits format
- Test before committing
- Review changes before committing (`git diff`)

❌ **Don't:**
- Commit broken code to main
- Make giant commits with unrelated changes
- Write vague messages ("fix stuff", "updates")
- Commit commented-out code
- Commit sensitive data (secrets, credentials)
- Force push to main

### Branch Practices

✅ **Do:**
- Keep branches short-lived (days not weeks)
- One feature/fix per branch
- Use descriptive branch names
- Delete branches after merging
- Rebase/merge from main frequently
- Keep main always deployable

❌ **Don't:**
- Create long-lived feature branches
- Mix multiple features in one branch
- Push directly to main (without PR)
- Leave stale branches
- Let branches get too far behind main

### Collaboration Practices

✅ **Do:**
- Pull before starting work
- Communicate about overlapping work
- Review others' PRs promptly
- Provide constructive feedback
- Respond to review comments
- Use PR templates
- Link issues in PRs

❌ **Don't:**
- Work on main directly
- Force push to shared branches (without communication)
- Approve PRs without reviewing
- Ignore CI failures
- Merge your own PRs without review

### Repository Hygiene

✅ **Do:**
- Use `.gitignore` properly
- Keep repository clean
- Document in README
- Tag releases
- Archive old branches
- Use GitHub releases

❌ **Don't:**
- Commit build artifacts
- Commit dependencies (unless necessary)
- Commit IDE-specific files
- Commit large binary files
- Let main branch diverge from production

## Troubleshooting Common Issues

### "I committed to wrong branch"

```bash
# Move commit to new branch
git branch feat/new-branch    # Create branch at current commit
git reset --hard HEAD~1       # Remove commit from current branch
git checkout feat/new-branch  # Switch to new branch
```

### "I need to undo last commit"

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Undo commit and changes
git reset --hard HEAD~1

# Undo but keep as uncommitted
git reset HEAD~1
```

### "I committed sensitive data"

```bash
# Remove from last commit
git rm --cached <file>
git commit --amend
git push --force-with-lease

# Remove from history (use tools like BFG Repo-Cleaner)
# Then rotate any exposed secrets!
```

### "My branch diverged from main"

```bash
# Rebase to fix
git fetch origin
git rebase origin/main
# Resolve conflicts
git push --force-with-lease origin feat/my-branch
```

### "I need to change commit message"

```bash
# Last commit only
git commit --amend

# Older commits
git rebase -i HEAD~3  # For last 3 commits
# Change 'pick' to 'reword' for commits to change
```

### "Rebase went wrong"

```bash
# Abort and start over
git rebase --abort

# Or if already messed up
git reflog  # Find previous state
git reset --hard <previous-commit>
```

See `references/troubleshooting.md` for more scenarios.

## Advanced Git Topics

### Interactive Rebase

```bash
# Rebase last 3 commits interactively
git rebase -i HEAD~3

# Options:
# pick - keep commit
# reword - change commit message
# edit - pause to amend commit
# squash - combine with previous commit
# fixup - like squash but discard message
# drop - remove commit
```

### Cherry-Pick

```bash
# Apply specific commit to current branch
git cherry-pick <commit-hash>

# Cherry-pick multiple commits
git cherry-pick <commit1> <commit2>

# Cherry-pick range
git cherry-pick <start>..<end>
```

### Reflog (recover lost commits)

```bash
# View reference log
git reflog

# Find lost commit
git reflog show HEAD

# Restore to previous state
git reset --hard HEAD@{2}
```

### Bisect (find bug-introducing commit)

```bash
# Start bisect
git bisect start
git bisect bad              # Current commit is bad
git bisect good <commit>    # Last known good commit

# Git will checkout middle commit, test it
git bisect good  # If works
git bisect bad   # If broken

# Repeat until found
git bisect reset  # Return to original state
```

### Worktrees (work on multiple branches)

```bash
# Create worktree for different branch
git worktree add ../project-feature feat/feature

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../project-feature
```

See `references/advanced-git.md` for detailed coverage.

## GitHub Actions Integration

### Basic CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install
        run: npm ci
      - name: Test
        run: npm test
      - name: Lint
        run: npm run lint
```

### Conventional Commit Validation

```yaml
# .github/workflows/commit-lint.yml
name: Commit Lint

on: [pull_request]

jobs:
  lint-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: wagoid/commitlint-github-action@v5
```

See `examples/github-actions/` for more workflow examples.

## Tools and Resources

### Recommended Tools

**Commit message helpers:**
- `commitizen` - Interactive commit message builder
- `commitlint` - Validate commit messages
- `husky` - Git hooks for validation

**GitHub CLI:**
```bash
gh pr create --title "feat: add feature" --body "Description"
gh pr checkout 123
gh pr review --approve
gh pr merge --squash
```

**Visual tools:**
- `gitk` - Built-in Git GUI
- GitKraken, SourceTree - Full-featured GUIs
- VS Code Git integration
- GitHub Desktop

### Configuration

**Useful git config:**
```bash
# User info
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Editor
git config --global core.editor "vim"

# Default branch
git config --global init.defaultBranch main

# Rebase by default
git config --global pull.rebase true

# Helpful aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --oneline --graph --decorate"
```

### Learning Resources

- **references/conventional-commits.md** - Complete Conventional Commits guide
- **references/trunk-based-development.md** - Detailed TBD workflow
- **references/github-workflow.md** - GitHub-specific practices
- **references/git-commands.md** - Comprehensive command reference
- **references/troubleshooting.md** - Problem-solving guide
- **references/advanced-git.md** - Advanced techniques
- **examples/** - Example commit messages, PR templates, workflows
- **assets/templates/** - Templates for PRs, commits, checklists

## When to Use This Skill

Activate for requests involving:
- Git commands and operations
- Branching and merging strategies
- Commit message formatting
- Pull request creation and review
- Merge conflict resolution
- Repository management
- GitHub workflow questions
- Git troubleshooting
- Version control best practices
- Team collaboration with Git

## Quick Reference

**Daily Commands:**
```bash
git status                      # Check status
git add .                       # Stage changes
git commit -m "type: message"  # Commit
git pull origin main           # Update from main
git push origin branch         # Push changes
```

**Branch Workflow:**
```bash
git checkout main              # Switch to main
git pull origin main           # Update
git checkout -b feat/name      # Create branch
# ... make changes ...
git push -u origin feat/name   # Push and create PR
```

**Conventional Commit:**
```
type(scope): subject

- Use feat, fix, docs, style, refactor, test, chore
- Imperative mood in subject
- Optional body for details
- Optional footer for breaking changes/issues
```

**Stay Updated:**
```bash
git fetch origin               # Fetch updates
git rebase origin/main         # Rebase on main
git push --force-with-lease    # Force push safely
```

---

**Remember:** Small commits, frequent integration, clear messages, short-lived branches, and always keep main deployable. This is the path to professional version control.
