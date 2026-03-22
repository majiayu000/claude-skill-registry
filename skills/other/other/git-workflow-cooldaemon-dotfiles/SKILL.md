---
name: git-workflow
description: Git workflow patterns including commit messages, rebase strategy, and pre-commit hooks. Use when committing, creating PRs, or managing git history. Do NOT use for code style or testing concerns -- use coding-style or testing-principles instead.
durability: encoded-preference
---

# Git Workflow Patterns

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| feat | New feature implementation |
| fix | Bug fixes |
| docs | Documentation changes only |
| style | Code formatting, missing semicolons, etc. |
| refactor | Code restructuring without behavior changes |
| perf | Performance improvements |
| test | Test additions or corrections |
| chore | Build process, auxiliary tools, dependencies |

### Rules

- Subject line: Max 50 characters, imperative mood, no period
- Body: Wrap at 72 characters, explain WHY not WHAT
- Write in English
- Be specific and descriptive

### Examples

```
feat(auth): add OAuth2 integration with Google

Implemented Google OAuth2 authentication flow to allow users
to sign in with their Google accounts. This includes:
- OAuth2 configuration and middleware setup
- User profile synchronization
- Session management with JWT tokens

Closes #123
```

```
fix(api): resolve race condition in payment processing

The payment webhook handler was not properly locking the
transaction record, causing duplicate charges when webhooks
arrived simultaneously. Added database-level locking to
ensure atomic transaction updates.
```

## Pre-commit Hook Handling

**CRITICAL: NEVER use `--no-verify` flag**

### Language-specific Checks

**JavaScript/TypeScript:**
- Linting: `npm run lint`, `eslint`
- Type checking: `npm run typecheck`, `tsc`
- Formatting: `prettier --check`, `npm run format`
- Tests: `npm test`, `jest`, `vitest`

**Python:**
- Linting: `ruff check`, `flake8`, `pylint`
- Type checking: `mypy`, `pyright`
- Formatting: `black --check`, `ruff format`
- Tests: `pytest`, `python -m unittest`

**Ruby:**
- Linting: `rubocop`
- Tests: `rspec`, `rake test`

**Go:**
- Formatting: `go fmt`, `gofmt`
- Linting: `golangci-lint run`
- Tests: `go test`

**General:**
- See `makefile-first` skill for command execution policy
- Check package.json scripts section
- Review project documentation

### Fixing Pre-commit Failures

1. Analyze the error message
2. Fix automatically if possible (formatting, linting)
3. For type errors: Modify code to fix
4. For test failures: Debug and fix
5. Stage fixed files and retry commit

## Rebase Strategy

### When to Rebase

Use `git pull --rebase` to maintain linear history:
- Before pushing local commits
- When local branch is behind remote

## Safety Checks

Before git operations:
- **Uncommitted changes**: Stash or commit before proceeding
- **Remote tracking**: Ensure branch tracks a remote
- **Network connectivity**: Verify connection to remote
- **Branch protection**: Check if branch has push restrictions

## Pull Request Workflow

1. Analyze full commit history (not just latest commit)
2. Use `git diff [base-branch]...HEAD` to see all changes
3. Draft comprehensive PR summary
4. Include test plan with TODOs
5. Push with `-u` flag if new branch

## Git Fixup Pattern

During TDD, each User Story produces a clean commit history through fixup commits:

1. **After GREEN phase**: Create a semantic commit
   ```bash
   git add -A && git commit -m "feat(scope): description"
   ```

2. **After REFACTOR phase**: Create a fixup commit targeting the GREEN commit
   ```bash
   git add -A && git commit --fixup HEAD
   ```

3. **After review fixes**: Create a fixup commit targeting the relevant US commit
   ```bash
   git add -A && git commit --fixup <target-sha>
   ```

4. **Before push**: Autosquash all fixup commits
   ```bash
   GIT_SEQUENCE_EDITOR=true git rebase --autosquash origin/<base-branch>
   ```

The result is one clean commit per US in the final history.

### Interleaved Commits

Git `fixup!` commits match their target by **commit message**, not by position in the log. This means interleaved normal and fixup commits from multiple USs are correctly handled by autosquash.

**Before autosquash:**
```
feat(auth): add login flow              <- US-1 GREEN
fixup! feat(auth): add login flow       <- US-1 REFACTOR
fixup! feat(auth): add login flow       <- US-1 review fix
feat(auth): add password reset          <- US-2 GREEN
fixup! feat(auth): add password reset   <- US-2 REFACTOR
```

**After `git rebase --autosquash`:**
```
feat(auth): add login flow              <- US-1 (REFACTOR + fix absorbed)
feat(auth): add password reset          <- US-2 (REFACTOR absorbed)
```

Each fixup is absorbed into the commit whose message it matches, regardless of intervening commits.

## Safe Force Push

**Rule**: Never use `git push --force`. Always use `git push --force-with-lease`.

## Parallel Work

Prefer `git worktree` over `git stash` for parallel work.

## Regression Hunting

Use `git bisect run <test-command>` for automated regression hunting.
