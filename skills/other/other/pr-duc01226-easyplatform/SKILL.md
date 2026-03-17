---
name: pr
version: 1.0.0
description: '[Git] Create pull request with standard format'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Create a pull request with standardized format (summary, test plan, changes list).

**Workflow:**
1. **Analyze** -- Review all commits and changes on the branch
2. **Draft** -- Create PR title (<70 chars) and body with summary + test plan
3. **Create** -- Push branch and create PR via `gh pr create`

**Key Rules:**
- PR title under 70 characters; use body for details
- Include summary bullets and test plan checklist
- Push to remote with `-u` flag before creating PR

# Create Pull Request: $ARGUMENTS

Create a pull request with the standard project format.

## Steps

1. **Check current branch status:**
    - Run `git status` to see all changes
    - Run `git diff` to review modifications
    - Ensure all changes are committed

2. **Analyze commits:**
    - Run `git log --oneline -10` to see recent commits
    - Identify all commits to include in the PR

3. **Create PR with standard format:**

    ```
    gh pr create --title "[Type] Brief description" --body "$(cat <<'EOF'
    ## Summary
    - Bullet points describing changes

    ## Changes
    - List of specific changes made

    ## Test Plan
    - [ ] Unit tests added/updated
    - [ ] Manual testing completed
    - [ ] No regressions introduced

    ## Related Issues
    - Closes #issue_number (if applicable)

    Generated with Claude Code
    EOF
    )"
    ```

4. **PR Title Format:**
    - `[Feature]` - New functionality
    - `[Fix]` - Bug fix
    - `[Refactor]` - Code improvement
    - `[Docs]` - Documentation only
    - `[Test]` - Test changes only

## Notes

- Ensure branch is pushed before creating PR
- Target branch is usually `develop` or `master`
- Add reviewers if specified in $ARGUMENTS

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
