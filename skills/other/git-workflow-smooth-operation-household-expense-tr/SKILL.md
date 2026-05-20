---
name: git-workflow
description: "Use when making commits, creating branches, or managing Git operations. Ensures consistent Git practices and proper commit messages."
---

# Git Workflow

## Core Principle

Maintain clean, readable Git history with meaningful commits and consistent branching practices.

## When to Use This Skill

- Creating new branches
- Making commits
- Writing commit messages
- Merging branches
- Creating pull/merge requests
- Any Git operation

## The Iron Laws

### 1. NO AI CO-AUTHOR ATTRIBUTION IN COMMITS

This is a firm policy. Commits represent human accountability.

### 2. NO COMMITS WITHOUT VERIFICATION

**MANDATORY**: Use `verification-before-completion` skill before EVERY commit.

Never commit without:
- ✅ All tests passing (unit, integration, e2e)
- ✅ Code quality checks passed
- ✅ Pre-commit hooks successful
- ✅ Self-review completed
- ✅ Verification checklist complete

### 3. SMALL, PRECISE COMMITS

**One logical change per commit.**

✅ **Good commits:**
- `feat(auth): add email validation to login form`
- `fix(api): handle null values in user profile endpoint`
- `test(checkout): add e2e tests for payment flow`

❌ **Bad commits:**
- `feat: add login, fix bugs, update tests, refactor code`
- Large commits with multiple unrelated changes
- Commits without running tests

**Why small commits:**
- 🔍 Easier to review
- 🐛 Easier to find bugs (git bisect)
- ⏪ Easier to revert
- 📖 Clearer history

### 4. FRONTEND + BACKEND = BOTH TESTS REQUIRED

**When changes affect both frontend and backend:**

```
MANDATORY before commit:
1. ✅ Backend tests pass (unit + integration)
2. ✅ E2E tests pass (full user flow)
3. ✅ API tests pass (if API changed)
4. ✅ Frontend tests pass (component + integration)
```

**Never commit:**
- ❌ Backend changes without backend tests
- ❌ Frontend changes without e2e tests
- ❌ API changes without both backend AND e2e tests
- ❌ Changes that break existing tests

### 5. PRE-COMMIT HOOKS ARE MANDATORY

**Every project MUST have pre-commit hooks.**

Minimum hooks required:
- Code formatting (Prettier, Black, PHP CS Fixer)
- Linting (ESLint, Ruff, PHPStan)
- Type checking (TypeScript, mypy, Psalm)
- Test execution (if files changed)
- No secrets/credentials check

**See**: `.claude/skills/safety/pre-commit-hooks/SKILL.md` for setup

## Git Commit Message Format

### Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

Must be one of:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, missing semi-colons, etc)
- `refactor`: Code refactoring (no functional changes)
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system or dependencies
- `ci`: CI/CD changes
- `chore`: Other changes (gitignore, etc)

### Scope (Optional)

Component or module affected:
- `auth`: Authentication
- `api`: API endpoints
- `database`: Database changes
- `ui`: User interface
- `tests`: Test files

### Subject

- Use imperative mood: "add" not "added" or "adds"
- Don't capitalize first letter
- No period at end
- Max 50 characters
- Be specific and concise

### Body (Optional but Recommended)

- Explain WHAT and WHY, not HOW
- Wrap at 72 characters
- Separate from subject with blank line
- Use bullet points if multiple items

### Footer (Optional)

- Breaking changes: `BREAKING CHANGE: description`
- Issue references: `Closes #123`, `Fixes #456`
- **NO AI co-author attribution**

## Commit Message Examples

### Good Examples

```
feat(auth): add JWT token-based authentication

Implement stateless authentication using Laravel Sanctum:
- User registration with email/password
- Login returns bearer token
- Protected routes use auth:sanctum middleware
- Token revocation on logout

Closes #45
```

```
fix(api): resolve N+1 query in user list endpoint

Added eager loading for user relationships to prevent
multiple database queries per user.

Performance improvement: 50+ queries → 2 queries

Fixes #78
```

```
docs: update README with authentication setup

Add step-by-step guide for:
- Installing Sanctum
- Configuring .env variables
- Running migrations
- Testing authentication
```

### Bad Examples

```
❌ Updated stuff
   - Too vague, no context

❌ Added authentication.
   - Capitalized, has period, no detail

❌ feat: add auth with JWT and social login and fix bugs and update docs
   - Too long, multiple unrelated changes

❌ WIP
   - Meaningless, what is in progress?

❌ fix: fixed the bug
   - Redundant, no detail about which bug
```

## Branching Strategy

### Branch Naming Convention

```
<type>/<short-description>
```

**Types:**
- `feature/` - New features
- `fix/` - Bug fixes
- `hotfix/` - Urgent production fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation
- `test/` - Test-related work

**Examples:**
- `feature/jwt-authentication`
- `fix/login-validation-error`
- `hotfix/security-patch-xss`
- `refactor/user-controller`
- `docs/api-documentation`

### Branch Workflow

#### Creating a New Branch

```bash
# Ensure you're on main/master and up to date
git checkout main
git pull origin main

# Create and switch to new branch
git checkout -b feature/authentication

# Or create from specific branch
git checkout -b fix/login-bug develop
```

#### Working on a Branch

```bash
# Make changes
[edit files]

# Stage changes
git add path/to/file.php

# Or stage all changes (careful!)
git add .

# Commit with good message
git commit -m "feat(auth): add user registration endpoint

Implement registration with email/password validation.
Returns JWT token on successful registration.

Closes #23"

# Push to remote
git push -u origin feature/authentication
```

#### Updating Branch with Latest Changes

```bash
# Option 1: Merge (preserves history)
git checkout main
git pull origin main
git checkout feature/authentication
git merge main

# Option 2: Rebase (cleaner history)
git checkout feature/authentication
git fetch origin
git rebase origin/main
```

#### Finishing a Branch

See `finishing-a-development-branch` skill for complete checklist.

## Git Best Practices

### Commit Frequency

- **Commit often**: Small, focused commits
- **Commit working code**: Each commit should be functional
- **Commit before major refactors**: So you can rollback if needed

### What to Commit

✅ **DO commit:**
- Source code
- Configuration files (without secrets)
- Tests
- Documentation
- Migrations
- .env.example (template, no secrets)

❌ **DON'T commit:**
- .env (contains secrets)
- node_modules/, vendor/
- Build artifacts (dist/, build/)
- IDE-specific files (.idea/, .vscode/)
- Log files
- Database files (*.sqlite, backups/)
- Temporary files

### .gitignore

Ensure proper .gitignore for your framework:

**Laravel:**
```gitignore
/vendor/
/node_modules/
.env
.env.*.local
/storage/*.key
/public/hot
/public/storage
/storage/logs/
/bootstrap/cache/*.php
backups/
```

**Node.js:**
```gitignore
node_modules/
.env
.env.*.local
dist/
build/
*.log
.DS_Store
```

**Python:**
```gitignore
__pycache__/
*.pyc
.env
.venv/
venv/
*.log
.pytest_cache/
.coverage
```

## Commit Workflow Checklist

Before committing:
- [ ] Run tests (with database backup!)
- [ ] Verify all changes are intentional
- [ ] No debugging code (console.log, dd(), var_dump())
- [ ] No commented-out code
- [ ] No secrets in files
- [ ] Files properly formatted (run linter)
- [ ] Commit message follows format

## Advanced Git Operations

### Amending Last Commit

```bash
# Add forgotten files to last commit
git add forgotten-file.php
git commit --amend --no-edit

# Or change commit message
git commit --amend -m "new commit message"

# ⚠️ Only amend commits that haven't been pushed
```

### Undoing Changes

```bash
# Discard changes in working directory
git restore path/to/file.php

# Unstage changes (keep in working directory)
git restore --staged path/to/file.php

# Undo last commit (keep changes)
git reset HEAD~1

# Undo last commit (discard changes) ⚠️
git reset --hard HEAD~1
```

### Stashing Changes

```bash
# Save current changes temporarily
git stash

# List stashes
git stash list

# Apply most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{0}
```

### Cherry-picking Commits

```bash
# Apply specific commit from another branch
git cherry-pick <commit-hash>
```

## GitHub/GitLab Integration

### Creating Pull/Merge Request

**GitHub:**
```bash
# Using GitHub CLI
gh pr create --title "feat(auth): Add JWT authentication" --body "Implements user authentication with JWT tokens

- Registration endpoint
- Login endpoint
- Protected routes
- Tests included

Closes #45"
```

**GitLab:**
```bash
# Using GitLab CLI
glab mr create --title "feat(auth): Add JWT authentication" --description "Implements user authentication with JWT tokens

- Registration endpoint
- Login endpoint
- Protected routes
- Tests included

Closes #45"
```

### Commit Message in PR/MR

Use the same format as commit messages:

```markdown
## What

Implements JWT authentication for API

## Why

Needed stateless authentication for mobile app support

## Changes

- Added Laravel Sanctum
- User registration endpoint
- Login/logout endpoints
- Auth middleware on protected routes
- 15 tests covering auth flows

## Testing

- All tests pass (127 total)
- Manual testing completed
- API documentation updated

Closes #45
```

## Integration with Other Skills

**Use before committing:**
- `code-review` - Review your changes
- `verification-before-completion` - Ensure everything works
- `database-backup` - Before running tests

**Related skills:**
- `finishing-a-development-branch` - Complete checklist before PR/MR
- `git-worktrees` - Working on multiple branches

## Red Flags (Bad Git Practices)

- ❌ Committing directly to main/master
- ❌ Vague commit messages ("fix", "update", "WIP")
- ❌ Committing secrets (.env file)
- ❌ Committing broken code
- ❌ Huge commits with unrelated changes
- ❌ Not testing before committing
- ❌ Including AI co-author attribution

## Common Rationalizations to Reject

- ❌ "I'll write a proper message later" → Write it now
- ❌ "Just a quick fix, doesn't need good message" → All commits need good messages
- ❌ "I'll clean up history before merging" → Don't rely on it, do it right first time
- ❌ "Adding AI attribution gives credit" → Humans are accountable, not AI

## Authority

**This skill is based on:**
- Git best practices (Conventional Commits standard)
- Industry standard: All professional teams use consistent commit practices
- Legal/accountability: Commits represent human responsibility
- CodeAssist policy: NO AI attribution in commits

**Social Proof**: Companies like Google, Microsoft, and GitHub use commit message conventions.

## Your Commitment

Before making commits:
- [ ] I will write clear, meaningful commit messages
- [ ] I will follow the commit message format
- [ ] I will NOT include AI co-author attribution
- [ ] I will test before committing
- [ ] I will commit small, focused changes

---

**Bottom Line**: Git history is documentation. Write it for humans who will read it later (including future you). Clean Git history makes debugging, code review, and collaboration easier.
