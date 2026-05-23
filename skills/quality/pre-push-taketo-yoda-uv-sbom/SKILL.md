---
name: pre-push
description: Run all validations before pushing to remote
---

# /pre-push - Pre-push Validation Skill

Final validation before pushing commits to remote repository.

## Purpose

Ensure code quality and branch conventions are correct before pushing to prevent CI failures and maintain repository standards.

## ⚠️ CRITICAL: Always Use This Skill - Never Bypass

**This skill exists to ensure CI-equivalent checks are run locally.**

### NEVER run these commands directly:

| ❌ Wrong (Missing Flags) | ✅ Correct (Use This Skill) |
|--------------------------|----------------------------|
| `cargo clippy --all-targets` | `/pre-push` includes `-D warnings` |
| `cargo fmt --check` | `/pre-push` includes `--all` flag |
| `cargo test` | `/pre-push` includes `--all` flag |

### Why This Matters (Issue #59 Incident)

Running `cargo clippy` without `-D warnings` caused a CI failure:
1. Clippy showed warnings but exit code was 0 (success)
2. Push proceeded despite warnings
3. CI failed because it uses `-D warnings` which treats warnings as errors

**Prevention**: Always invoke `/pre-push` instead of running individual commands manually.

### Commands This Skill Runs

This skill ensures the following commands are run with **exact CI-matching flags**:

```bash
cargo test --all                                           # All tests
cargo fmt --all -- --check                                 # Format check
cargo clippy --all-targets --all-features -- -D warnings   # Clippy with warnings as errors
```

## Validation Checklist

All of the following MUST pass before pushing:

### 1. Full Test Suite

```bash
cargo test --all
```

**All tests must pass.**

### 2. Format Verification

```bash
cargo fmt --all -- --check
```

If this fails, run `cargo fmt --all` and commit the changes.

### 3. Clippy Verification

```bash
cargo clippy --all-targets --all-features -- -D warnings
```

**Zero warnings required.**

### 4. Branch Naming Convention

```bash
git branch --show-current
```

Verify branch name follows convention based on **Issue labels** (priority order):

| Priority | Issue Label | Branch Prefix | Example |
|----------|-------------|---------------|---------|
| 1 | `enhancement` | `feature/` | `feature/84-agent-skills` |
| 2 | `bug` | `bugfix/` | `bugfix/42-fix-parsing` |
| 3 | `refactor` | `refactor/` | `refactor/30-cleanup-code` |
| 4 | `documentation` | `doc/` | `doc/50-update-readme` |
| 5 | (no label) | `feature/` | `feature/99-misc-task` |

**Additional**: `hotfix/<issue>-<desc>` for critical production fixes

**FORBIDDEN branches for direct push:**

- `main` - Use PR only
- `develop` - Use PR only (if applicable)

### 5. Remote Branch Target

```bash
git remote -v
git branch -vv
```

Verify:

- [ ] Pushing to correct remote (typically `origin`)
- [ ] Not accidentally pushing to upstream/fork

## Steps

### Step 1: Run Full Test Suite

```bash
cargo test --all
```

If tests fail:

1. Fix the failing tests
2. Commit the fixes
3. Re-run tests

### Step 2: Verify Formatting

```bash
cargo fmt --all -- --check
```

If formatting issues found:

1. Run `cargo fmt --all`
2. Commit formatting changes
3. Re-run check

### Step 3: Run Clippy

```bash
cargo clippy --all-targets --all-features -- -D warnings
```

If warnings found:

1. Fix all warnings
2. Commit fixes
3. Re-run clippy

### Step 4: Check Branch Name

```bash
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"
```

Verify:

- [ ] Matches naming convention
- [ ] Not on `main` or `develop`
- [ ] Issue number in branch name (if applicable)

### Step 5: Verify Unpushed Commits

```bash
git log origin/$(git branch --show-current)..HEAD --oneline 2>/dev/null || git log --oneline -5
```

Review what will be pushed.

### Step 6: Final Confirmation

Before pushing, confirm:

- [ ] All tests pass
- [ ] Formatting is clean
- [ ] No clippy warnings
- [ ] Branch name is correct
- [ ] Commits are reviewed

### Step 7: Push

```bash
git push -u origin $(git branch --show-current)
```

## Error Handling

### Test Failures

```
STOP: Tests are failing. Fix all test failures before pushing.
```

1. Identify failing tests
2. Debug and fix
3. Commit fixes
4. Re-run `/pre-push`

### Format Failures

```
STOP: Code formatting issues detected. Running cargo fmt...
```

1. Run `cargo fmt --all`
2. Review changes
3. Commit formatting
4. Continue with push

### Clippy Warnings

```
STOP: Clippy warnings detected. Fix all warnings before pushing.
```

1. Read each warning
2. Fix the issues
3. Commit fixes
4. Re-run clippy

### Wrong Branch

```
WARNING: You are on branch 'main'. Direct pushes to main are not allowed.
```

**CRITICAL**: Always create branches from `origin/develop`:

```bash
git fetch origin
git checkout -b feature/<issue>-<description> origin/develop
```

1. Create a feature branch from origin/develop (not main!)
2. Push the feature branch
3. Create a PR targeting `develop`

## Example Usage

User: "pushする前にチェックして"

Claude executes /pre-push skill:

1. Runs `cargo test --all` - PASS
2. Runs `cargo fmt --all -- --check` - PASS
3. Runs `cargo clippy --all-targets --all-features -- -D warnings` - PASS
4. Checks branch: `feature/84-agent-skills` - VALID
5. Reviews unpushed commits
6. Reports: "All checks passed. Ready to push."
7. If user confirms, executes `git push -u origin feature/84-agent-skills`

## Summary Output

After all checks pass, output:

```
Pre-push Validation Complete
============================
[PASS] Tests: All X tests passed
[PASS] Format: Code is properly formatted
[PASS] Clippy: No warnings
[PASS] Branch: feature/84-agent-skills (valid naming)
[INFO] Commits to push: X commits

Ready to push to origin/feature/84-agent-skills
```
