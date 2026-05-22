---
name: bl-submit
description: Submit git-branchless stack as PRs - create branches and push to remote
argument-hint: "[--all] [--update] [<branch-name>]"
---

# /bl-submit - Git-Branchless PR Submission

**Category:** Git Workflow

Submit commits from your stack as pull requests. Creates branches, pushes to remote, and guides stacked PR configuration.

## Usage

```
/bl-submit [options]
```

## Options

| Option | Description |
|--------|-------------|
| (none) | Submit current commit (creates branch if needed) |
| `--all` | Create branches and submit entire stack |
| `--update` | Update all existing PR branches |
| `<name>` | Specify branch name for current commit |

## Examples

```bash
# Submit current commit with auto-generated branch name
/bl-submit

# Submit current commit with custom branch name
/bl-submit pr/user-authentication

# Submit entire stack (creates branches for all commits)
/bl-submit --all

# Update all existing PRs after changes
/bl-submit --update
```

## Execution

This command delegates to the `bl-submit-expert` agent:

```
Task(subagent_type="git-workflow:bl-submit-expert",
     prompt="Execute submit: <options>")
```

## Execution Instructions

1. **Verify Prerequisites**
   - Check git-branchless is installed
   - Check remote is configured

2. **Show Current State**
   - Run `git sl` to display stack with branches
   - Identify commits without branches

3. **Execute Submission**
   - For single: Create branch at current commit, push
   - For all: Navigate stack, create branches, push each
   - For update: Force-push all existing branches

4. **Guide PR Configuration**
   - Explain stacked PR base branches
   - Provide table of branch → base relationships

5. **Confirm Result**
   - Show branches on remote
   - Display final state with `git sl`

## Interactive Flow

```
User: /bl-submit pr/user-auth

Agent: Submitting current commit...

Current position:
● def5678 feat: add user authentication

Creating branch...
git switch -c pr/user-auth

Pushing to remote...
git submit -c @

✓ Branch pr/user-auth pushed to origin

◆ abc1234 (main) initial commit
┃
● def5678 (ᐅ pr/user-auth) feat: add user authentication

You can now create a PR on GitHub:
  Base: main
  Compare: pr/user-auth
```

```
User: /bl-submit --all

Agent: Submitting entire stack (3 commits)...

◆ abc1234 (main) initial commit
┃
◯ def5678 feat: add User class
┃
◯ ghi9012 feat: add validation
┃
● jkl3456 feat: add repository

[1/3] Creating branch at "feat: add User class"...
  git switch -c pr/user-class
  git submit -c @
  ✓ pr/user-class pushed

[2/3] Creating branch at "feat: add validation"...
  git switch -c pr/validation
  git submit -c @
  ✓ pr/validation pushed

[3/3] Creating branch at "feat: add repository"...
  git switch -c pr/repository
  git submit -c @
  ✓ pr/repository pushed

◆ abc1234 (main) initial commit
┃
◯ (pr/user-class) feat: add User class
┃
◯ (pr/validation) feat: add validation
┃
● (ᐅ pr/repository) feat: add repository

All 3 branches pushed!

Create stacked PRs on GitHub:
┌─────────────────┬──────────────────┐
│ Branch          │ Base Branch      │
├─────────────────┼──────────────────┤
│ pr/user-class   │ main             │
│ pr/validation   │ pr/user-class    │
│ pr/repository   │ pr/validation    │
└─────────────────┴──────────────────┘
```

```
User: /bl-submit --update

Agent: Updating all PR branches...

Branches to update:
  - pr/user-class
  - pr/validation
  - pr/repository

Running git submit...

  pr/user-class:   abc123 → def456 (force-pushed)
  pr/validation:   ghi789 → jkl012 (force-pushed)
  pr/repository:   mno345 → pqr678 (force-pushed)

All 3 PR branches updated.
GitHub PRs will show new changes automatically.
```

## Stacked PRs Guide

When you submit a stack, you create **stacked PRs** on GitHub:

```
Commit Stack          GitHub PRs
─────────────         ──────────
pr/repository    →    PR #3: base = pr/validation
     ↓
pr/validation    →    PR #2: base = pr/user-class
     ↓
pr/user-class    →    PR #1: base = main
     ↓
    main
```

**Important:** On GitHub, set each PR's base branch to its parent branch, not `main`. This ensures reviewers see only the diff for that specific commit.

**After a PR is merged:**
1. GitHub may auto-update child PR base branches
2. Locally, run `/bl-sync --after-merge` to clean up
3. Then `/bl-submit --update` to push changes

## Error Handling

| Error | Resolution |
|-------|------------|
| No remote configured | `git remote add origin <url>` |
| "Skipped - not on remote" | Use `/bl-submit` (creates with `-c`) |
| Branch already exists | Delete old: `git branch -D <name>` |
| Force-push rejected | Check repo branch protection |
| Detached HEAD | Creates branch automatically |
