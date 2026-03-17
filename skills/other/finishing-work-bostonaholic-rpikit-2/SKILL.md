---
name: finishing-work
description: >-
  Structured completion workflow for implementation work. Use when
  implementation is complete, all tests pass, and you need to decide how to
  integrate the work. Guides merge, PR creation, or cleanup decisions.
---

# Finishing Work

Verify tests, present options, execute chosen workflow, clean up.

## Purpose

Implementation without proper completion leaves work in limbo. This skill
provides structured options for finishing work: merge locally, create PR,
defer for later, or discard. Each option has specific procedures and cleanup
requirements.

## Prerequisites

Before using this skill, verify:

1. All implementation steps completed
2. All verifications passed
3. Code review completed (if applicable)
4. Security review completed (if applicable)

**Do not proceed with failing tests.** Fix them first.

## The Completion Workflow

### Step 1: Verify Tests Pass

Run the full test suite:

```text
Run: [project test command]
Verify: Exit code 0, all tests pass
```

**If tests fail**: Stop. Do not proceed until tests pass.

### Step 2: Identify Base Branch

Determine the target branch for integration:

```text
Common targets:
- main (most common)
- master (legacy naming)
- develop (gitflow)
- [feature-branch] (nested features)
```

Check git configuration or ask if unclear.

### Step 3: Present Options

Present exactly four options without elaboration:

1. **Merge locally** - Merge to base branch on local machine
2. **Create pull request** - Push and open PR for review
3. **Keep for later** - Leave branch as-is to continue later
4. **Discard work** - Delete branch and changes

Use AskUserQuestion to get user's choice.

### Step 4: Execute Chosen Option

#### Option 1: Merge Locally

```text
1. Checkout base branch
   git checkout [base-branch]

2. Pull latest changes
   git pull origin [base-branch]

3. Merge feature branch
   git merge [feature-branch]

4. Run tests on merged result
   [project test command]

5. If tests pass, push
   git push origin [base-branch]

6. Delete feature branch
   git branch -d [feature-branch]
   git push origin --delete [feature-branch]
```

**Never merge without verifying tests pass on the result.**

#### Option 2: Create Pull Request

```text
1. Push feature branch
   git push -u origin [feature-branch]

2. Create PR using gh CLI
   gh pr create --title "[title]" --body "[description]"

3. Report PR URL to user

4. Keep branch active for PR review
```

Do NOT delete the branch after creating PR.

#### Option 3: Keep for Later

```text
1. Commit any uncommitted changes
   git add -A && git commit -m "WIP: [description]"

2. Push to remote (backup)
   git push -u origin [feature-branch]

3. Note current state for later
   - Branch name
   - What's done
   - What remains
```

Do NOT delete the branch.

#### Option 4: Discard Work

```text
1. Confirm with user (require typed confirmation)
   "Type 'DISCARD' to confirm deletion of all changes"

2. If confirmed:
   git checkout [base-branch]
   git branch -D [feature-branch]
   git push origin --delete [feature-branch] (if pushed)

3. Clean up any worktree if applicable
```

**Require explicit confirmation.** This is destructive.

### Step 5: Clean Up

Cleanup depends on the chosen option:

| Option | Cleanup Action |
|--------|----------------|
| Merge locally | Delete feature branch, remove worktree if used |
| Create PR | Keep branch, keep worktree if used |
| Keep for later | Keep branch, keep worktree if used |
| Discard work | Delete branch, remove worktree if used |

#### Worktree Cleanup (if applicable)

If work was done in a git worktree:

```text
1. Exit the worktree directory
   cd [main-repository]

2. Remove the worktree
   git worktree remove [worktree-path]

3. Verify removal
   git worktree list
```

Only remove worktree for merge (Option 1) and discard (Option 4).

## Integration with Implement Phase

This skill is the natural endpoint of the implement phase:

```text
Implementation complete
→ Code review passed
→ Security review passed
→ Use finishing-work skill
→ Choose completion option
→ Execute and clean up
```

## Safety Guardrails

### Never Merge with Failing Tests

```text
If tests fail after merge:
1. Do NOT push
2. Reset the merge: git merge --abort
3. Investigate failures
4. Fix before attempting merge again
```

### Never Force Push to Shared Branches

```text
Avoid: git push --force origin main
This rewrites history and breaks collaborators.

If needed, use: git push --force-with-lease
This fails if remote has new commits.
```

### Confirm Before Discarding

```text
Discard is permanent. Require typed confirmation:
"Type 'DISCARD' to confirm"

Do not accept:
- "yes"
- "y"
- "confirm"

Only exact match: "DISCARD"
```

## Status Reporting

After completing the chosen option, report:

```text
Option 1 (Merge):
"Merged [feature-branch] to [base-branch].
Branch deleted. [N] commits integrated."

Option 2 (PR):
"Pull request created: [PR-URL]
Branch [feature-branch] pushed to origin."

Option 3 (Keep):
"Branch [feature-branch] saved for later.
Pushed to origin as backup."

Option 4 (Discard):
"Branch [feature-branch] deleted.
All changes discarded."
```

## Anti-Patterns

### Merging Without Tests

**Wrong**: Merge and hope tests pass
**Right**: Run tests, then merge only if passing

### Leaving Branches Dangling

**Wrong**: Finish work, forget to clean up branches
**Right**: Execute appropriate cleanup for chosen option

### Skipping Confirmation for Discard

**Wrong**: Delete branch immediately when user says "discard"
**Right**: Require explicit "DISCARD" confirmation

### Merging Unreviewed Code

**Wrong**: Merge without code review
**Right**: Complete review process before finishing

### Force Pushing to Shared Branches

**Wrong**: Force push to fix mistakes
**Right**: Use safe alternatives or coordinate with team

## Checklist Before Finishing

- [ ] All implementation steps complete
- [ ] All tests pass
- [ ] Code review completed (if required)
- [ ] Security review completed (if required)
- [ ] Base branch identified
- [ ] Option chosen by user
- [ ] Tests pass after merge (if merging)
- [ ] Appropriate cleanup performed
- [ ] Status reported to user
