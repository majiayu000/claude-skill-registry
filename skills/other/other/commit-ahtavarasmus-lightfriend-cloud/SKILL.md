---
name: commit
description: Validate code with lints and tests, then commit and push
---

# Validated Commit and Push

This skill ensures code quality before committing by running all checks, then commits and pushes.

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

Review what will be committed. If there are no changes, inform the user and stop.

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

Commit message format:
```bash
git commit -m "Short description of changes"
```

For multi-line messages:
```bash
git commit -m "$(cat <<'EOF'
Short summary

Longer description if needed
EOF
)"
```

### Step 7: Push to Remote

```bash
git push origin HEAD
```

If push fails due to upstream changes, pull first:
```bash
git pull --rebase origin HEAD && git push origin HEAD
```

## Failure Handling

If ANY step fails (fmt, clippy, or tests):
1. Stop immediately
2. Report the failure to the user
3. Do NOT proceed to commit
4. Help fix the issues if requested

## Quick Commands Reference

```bash
# Full validation + commit + push
cd backend && cargo fmt --check && cargo clippy --workspace --all-targets --all-features -- -D warnings && cargo test --workspace && cd .. && git add -A && git commit -m "message" && git push

# Auto-fix formatting
cd backend && cargo fmt

# Check only (no commit)
cd backend && cargo fmt --check && cargo clippy --workspace --all-targets --all-features -- -D warnings && cargo test --workspace
```
