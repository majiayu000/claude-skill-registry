---
name: fix-audit-issue
description: Fix a single audit issue in a git worktree. Creates a feature branch, follows fix-bug procedure, and creates a PR. Designed for parallel execution by spawned agents.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Fix Audit Issue (Worktree Workflow)

This skill wraps the `fix-bug` procedure for agents running in git worktrees.

## Step 1: Create branch

```bash
git checkout -b fix/{short-description}
```

Use a descriptive branch name based on the issue (e.g., `fix/redaction-policy-merge`, `fix/crewai-double-callback`).

## Step 2: Follow fix-bug procedure

Execute all 8 steps from the `fix-bug` skill:
1. Understand the bug
2. Root cause analysis
3. Write failing behavior test FIRST
4. Fix the source code
5. Verify the fix
6. Check regression scope
7. Docs-code sync check
8. Full verification

## Step 3: Commit and push

```bash
git add {specific files}
git commit -m "fix: {description}"
git push -u origin fix/{short-description}
```

## Step 4: Create PR

```bash
gh pr create --title "fix: {short description}" --body "$(cat <<'EOF'
## Summary
{one-line summary}

## Root Cause
{what the code did wrong and why tests didn't catch it}

## Fix
{what was changed}

## Test Plan
- [ ] Behavior test added in tests/test_behavior/
- [ ] Full test suite passes
- [ ] Lint passes
- [ ] Docs build passes
- [ ] Docs-code sync passes
EOF
)"
```

## Conventions

- One issue per branch, one issue per PR
- Conventional commit: `fix: {description}`
- No Co-Authored-By
- No banned terminology — check `.docs-style-guide.md` before writing any user-facing string
- Branch from `main`, target `main`
