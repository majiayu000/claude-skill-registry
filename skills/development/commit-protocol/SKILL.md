---
name: commit-protocol
description: Use when user asks to commit changes or when finishing significant work. Enforces quality gates, testing verification, and explicit user approval before any git commit.
---

# Commit Protocol Skill

Use this skill whenever the user asks to commit changes or when you've completed significant work.

## 🚨 Critical Rule

**NEVER COMMIT without explicit user confirmation after manual testing.**

The user MUST:
1. Manually test the changes
2. Verify everything works as expected
3. Explicitly say "commit" or "create commit"

## Pre-Commit Quality Gates

Before asking for commit approval, ALWAYS run:

```bash
pnpm lint && pnpm type-check
```

**All errors must be fixed** before proceeding. Do not ask for commit if quality gates fail.

### If Quality Gates Fail:

1. **Report the errors clearly** with file paths and line numbers
2. **Fix all errors** before proceeding
3. **Re-run quality gates** to verify fixes
4. Only proceed when all checks pass

## Commit Workflow

### Step 1: Run Quality Gates (in parallel)

```bash
# Run both commands
pnpm lint
pnpm type-check
```

### Step 2: Review Changes

```bash
git status
git diff
```

Analyze what changed:
- New features vs bug fixes vs refactoring
- Files modified and why
- Scope of changes (single feature or multiple)

### Step 3: Provide Testing Instructions

Give the user **specific, actionable testing steps**:

**Example for mobile feature:**
```
Please test the following:
1. Open the app and navigate to [specific screen]
2. Test [specific interaction/feature]
3. Verify [expected behavior]
4. Edge cases to check:
   - When count is 0, verify no '0' renders
   - Check both light and dark mode
   - Test with different translations (EN, FR, DE, AR)
```

**Example for API changes:**
```
Please test:
1. Run the affected API endpoint: [example curl command]
2. Verify response structure matches type definitions
3. Test error cases: [specific scenarios]
4. Check database state after operations
```

### Step 4: Wait for User Approval

**STOP HERE** and wait for the user to:
- Test the changes
- Confirm everything works
- Explicitly request commit

**Do NOT proceed** until user confirms.

### Step 5: Create Commit (only after approval)

Use conventional commit format per `commitlint.config.js`:

```bash
git add [relevant-files]

git commit -m "$(cat <<'EOF'
type(scope): brief description

Optional detailed explanation of changes.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 6: Verify Commit

```bash
git log -1 --stat
git status
```

Confirm commit was created successfully.

## Conventional Commit Format

Follow the project's commit convention (see [commitlint.config.js](../../../commitlint.config.js)):

```
type(scope): subject

[optional body]

[optional footer]
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring (no feature change)
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, tooling
- `ci`: CI/CD configuration

### Scopes (examples):
- `mobile`: React Native app
- `web`: Next.js web app
- `admin`: Admin portal
- `ui`: UI package
- `lib`: Shared library
- `i18n`: Internationalization
- `api`: API changes
- `db`: Database/Supabase
- `monorepo`: Workspace configuration

### Examples:

```bash
# New feature in mobile app
feat(mobile): add user profile screen with avatar upload

# Bug fix in UI package
fix(ui): prevent Button from rendering 0 in loading state

# Database migration
feat(db): add posts table with RLS policies

# Refactoring shared logic
refactor(lib): extract auth logic to dedicated hook

# Multiple scopes
feat(mobile,web): implement dark mode theme switching
```

## Pre-Commit Hook Handling

If pre-commit hooks modify files:

1. **Check authorship**: `git log -1 --format='%an %ae'`
2. **Check push status**: Verify not already pushed
3. **If both true**: Safe to amend commit
4. **Otherwise**: Create new commit (never amend others' commits)

```bash
# Safe to amend
git add [modified-files]
git commit --amend --no-edit

# Not safe - new commit
git add [modified-files]
git commit -m "style: apply pre-commit hook fixes"
```

## What NOT to Commit

**Never commit files with secrets:**
- `.env` files (unless `.env.example`)
- `credentials.json`
- API keys or tokens
- Service role keys
- Private keys

**Warn the user** if they request to commit sensitive files.

## Commit Checklist

Before any commit:

- [ ] Quality gates passed (`pnpm lint && pnpm type-check`)
- [ ] All errors fixed
- [ ] Testing instructions provided to user
- [ ] User explicitly confirmed testing complete
- [ ] User explicitly requested commit
- [ ] Conventional commit format used
- [ ] No sensitive files included
- [ ] Commit verified with `git log -1`

## Common Scenarios

### Scenario: User says "I'm done testing, looks good"

**Response:**
```
Great! I'll create a commit now.

[Run git add + git commit]
[Show git log output]

Commit created successfully.
```

### Scenario: Quality gates fail

**Response:**
```
Quality gates failed. Found [N] errors:

[List errors with file:line references]

Let me fix these issues before we can commit.

[Fix errors]
[Re-run quality gates]
```

### Scenario: User asks to commit without testing

**Response:**
```
Before I can commit, please test the following changes:

[Provide specific testing instructions]

Once you've verified everything works, let me know and I'll create the commit.
```

## Never Skip Steps

**Do NOT:**
- Commit without running quality gates
- Commit without user testing and approval
- Assume testing is complete
- Use `--no-verify` flag (skips hooks)
- Force push to main/master
- Amend commits from other developers

**Always:**
- Run `pnpm lint && pnpm type-check`
- Wait for explicit user approval
- Provide clear testing instructions
- Use conventional commit format
- Verify commit was created

## References

- Main config: [CLAUDE.md](../../../CLAUDE.md)
- Commit config: [commitlint.config.js](../../../commitlint.config.js)
- Quality scripts: [package.json](../../../package.json)
