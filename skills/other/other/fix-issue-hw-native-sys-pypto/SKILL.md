---
name: fix-issue
description: Fix a GitHub issue by fetching content, creating a branch, planning the fix, and implementing it. Use when the user asks to fix a specific issue number or work on a GitHub issue.
---

# PyPTO Issue Fix Workflow

Fetch GitHub issue, create branch, plan, and implement the fix.

## Workflow

1. Check gh CLI authentication
2. Fetch issue content
3. Create issue branch
4. Enter plan mode to design fix
5. Implement the fix
6. Run tests (use `testing` skill)
7. Commit changes (use `git-commit` skill)

## Step 1: Check gh CLI Authentication

```bash
gh auth status
```

**If not authenticated**, prompt user:

```text
gh CLI is not authenticated. Please run: gh auth login
```

⚠️ **Stop here if not authenticated** - user must login first.

## Step 2: Fetch Issue Content

```bash
gh issue view ISSUE_NUMBER
gh issue view ISSUE_NUMBER --json number,title,body,state,labels
```

**Parse**: Issue number, title, description, state (open/closed), labels

**If issue is closed**: Ask user if they still want to work on it.

## Step 3: Create Issue Branch

**Branch naming**: `issue-{number}-{short-description}`

```bash
git checkout main && git pull upstream main
ISSUE_NUM=123
BRANCH_NAME="issue-${ISSUE_NUM}-fix-tensor-validation"
git checkout -b "$BRANCH_NAME"
```

## Step 4: Enter Plan Mode

Use `EnterPlanMode` to design the fix.

**Plan should cover**:

- Root cause analysis (for bugs)
- Files that need changes
- Implementation strategy
- Testing approach
- Documentation updates
- Cross-layer changes (C++, Python, type stubs)

## Step 5: Implement the Fix

After plan approval, follow PyPTO conventions:

1. Make code changes following plan
2. Follow `.claude/rules/` conventions
3. Update documentation if needed
4. Add/update tests
5. Maintain cross-layer sync (C++, Python, type stubs)

## Step 6: Run Tests

```text
/testing
```

Fix any failures before committing.

## Step 7: Commit Changes

```text
/git-commit
```

**Commit message format**:

```text
fix(scope): Brief description

Fixes #ISSUE_NUMBER

Detailed explanation of the fix.
```

## Step 8: Create PR (Optional)

```text
/github-pr
```

**PR must reference issue**: "Fixes #ISSUE_NUMBER"

## Common Issue Types

| Type | Approach |
| ---- | -------- |
| Bug fix | Reproduce, root cause, fix, add regression test |
| Feature request | Plan API design, implement, add tests and docs |
| Refactoring | Plan changes, ensure tests pass, maintain API |
| Documentation | Fix/improve docs, verify examples work |

## Checklist

- [ ] gh CLI authenticated
- [ ] Issue content fetched and understood
- [ ] Issue branch created from latest main
- [ ] Plan created and approved
- [ ] Fix implemented following PyPTO rules
- [ ] Tests added/updated and passing
- [ ] Changes committed with issue reference
- [ ] Documentation updated if needed

## Remember

**Reference the issue number** in commit messages and PR description using "Fixes #ISSUE_NUMBER" for auto-linking.
