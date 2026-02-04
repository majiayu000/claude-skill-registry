---
name: commit-push-pr
description: Validate code, commit, push, and create PR if needed
---

# Validated Commit, Push, and PR

This skill ensures code quality, commits, pushes, and creates a PR if one doesn't exist.

## Process

### Step 1: Run Formatting Check

```bash
cd backend && cargo fmt --check
```

If this fails, run `cargo fmt` to auto-fix, then re-check.

### Step 2: Run Clippy Lints

```bash
cd backend && cargo clippy --workspace --all-targets --all-features -- -D warnings
```

If clippy fails, fix the issues before proceeding. Do NOT commit code with clippy warnings.

### Step 3: Run Tests

```bash
cd backend && cargo test --workspace
```

If tests fail, fix the failing tests before proceeding. Do NOT commit code with failing tests.

### Step 4: Check for Changes

```bash
git status
```

Review what will be committed. If there are no changes to commit, skip to Step 8 (PR creation).

### Step 5: Stage Changes

```bash
git add -A
```

### Step 6: Create Commit

Ask the user for a commit message, or generate one based on the changes.

**IMPORTANT**: Never include:
- "Generated with Claude Code"
- "Co-Authored-By: Claude"
- Any AI/Claude attribution

### Step 7: Push to Remote

```bash
git push origin HEAD
```

If push fails due to upstream changes:
```bash
git pull --rebase origin HEAD && git push origin HEAD
```

### Step 8: Check for Existing PR

```bash
gh pr list --head $(git branch --show-current) --state open
```

If a PR already exists for this branch, inform the user and provide the PR URL. Done.

### Step 9: Create PR (if none exists)

Get the current branch and base branch:
```bash
CURRENT_BRANCH=$(git branch --show-current)
```

Create the PR:
```bash
gh pr create --title "PR title here" --body "$(cat <<'EOF'
## Summary
- Brief description of changes

## Test plan
- [ ] Tests pass
- [ ] Lints pass

EOF
)"
```

**PR Title**: Generate from the commit message or ask user.

**PR Body**: Include:
- Summary of changes (2-3 bullet points)
- Test plan checklist

Do NOT include "Generated with Claude Code" or similar.

### Step 10: Report Success

Provide the PR URL to the user.

## Failure Handling

If ANY step fails (fmt, clippy, or tests):
1. Stop immediately
2. Report the failure to the user
3. Do NOT proceed to commit
4. Help fix the issues if requested

## Quick Reference

```bash
# Full validation
cd backend && cargo fmt --check && cargo clippy --workspace --all-targets --all-features -- -D warnings && cargo test --workspace

# Check for existing PR
gh pr list --head $(git branch --show-current) --state open

# Create PR
gh pr create --title "Title" --body "Body"
```
