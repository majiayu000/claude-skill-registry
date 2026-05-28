---
name: safe-push
description: Safely push changes to remote with protection against pushing to important branches like main, master, production, testing, etc. Use when the user asks to push changes.
allowed-tools: Bash(git push:*), Bash(git branch:*), Bash(git status:*), Bash(git rev-parse:*), Read, AskUserQuestion
model: haiku
---

# Safe Push Skill

This skill helps you safely push changes to remote repositories while preventing accidental pushes to protected branches.

## Instructions

When the user asks to push changes, follow these steps:

### 1. Check Current Branch

Determine the current branch:
```bash
git rev-parse --abbrev-ref HEAD
```

### 2. Load Protected Branches List

Read the protected branches configuration:
```bash
Read: .claude/protected-branches.json
```

### 3. Check if Branch is Protected

Compare the current branch against the protected branches list. Protected branches typically include:
- **Deployment**: main, master, production, prod, staging, stage
- **Development**: dev, develop, development
- **Release**: release
- **Quality Assurance**: qa, uat
- **Testing**: test, testing, integration, e2e

### 4. Handle Protected Branches

**If the current branch is protected:**

1. **STOP** - Do not push
2. Inform the user that the branch is protected
3. Explain why direct pushes are prevented (these branches typically require PRs)
4. Suggest alternatives:
   - Create a feature branch: `git checkout -b feat/your-feature`
   - Create a PR instead: Use the PR creation workflow
   - If they really need to push (emergency), ask for explicit confirmation

**If the user insists on pushing to a protected branch:**

Use the AskUserQuestion tool to confirm:
```
Question: "You're about to push to a protected branch ({branch-name}). This is typically not recommended as it bypasses PR workflows. Are you sure you want to continue?"
Options:
- "No, create a feature branch instead"
- "No, I'll create a PR"
- "Yes, I understand the risks (emergency only)"
```

Only proceed if they explicitly choose the third option.

### 5. Push to Safe Branches

**If the branch is NOT protected:**

1. Check the git status to see if there are any unpushed commits:
```bash
git status
```

2. Push to the remote:
```bash
git push
```

3. If the branch doesn't have an upstream set, use:
```bash
git push -u origin <branch-name>
```

4. Confirm success and show the output

### 6. After Pushing

After a successful push:
1. Confirm the push was successful
2. Show the branch name and commit count pushed
3. If appropriate, ask if they want to create a PR

## Protected Branch Categories

These patterns indicate a protected branch:

**Deployment Branches:**
- `main`, `master` - Primary production branches
- `production`, `prod` - Production environment
- `staging`, `stage` - Staging environment

**Development Branches:**
- `dev`, `develop`, `development` - Main development branches

**Release Branches:**
- `release` - Release preparation

**Quality Assurance Branches:**
- `qa`, `uat` - Quality assurance and user acceptance testing

**Testing Branches:**
- `test`, `testing` - General testing environments
- `integration` - Integration testing
- `e2e` - End-to-end testing

## Examples

### Example 1: Pushing to a safe branch
```
User: "Push my changes"
Assistant: [Checks current branch: feat/add-authentication]
Assistant: "Pushing changes from 'feat/add-authentication' to remote..."
Command: git push -u origin feat/add-authentication
Output: Successfully pushed 3 commits
Response: "Successfully pushed 3 commits to 'feat/add-authentication'. Would you like to create a PR?"
```

### Example 2: Attempting to push to protected branch
```
User: "Push to remote"
Assistant: [Checks current branch: main]
Response: "⚠️ You're currently on the 'main' branch, which is protected. Direct pushes to 'main' are not recommended as they bypass the PR workflow.

I suggest:
1. Create a feature branch for your changes
2. Push to that branch
3. Create a PR to merge into main

Would you like me to create a feature branch for you?"
```

### Example 3: Attempting to push to testing branch
```
User: "Push these changes"
Assistant: [Checks current branch: integration]
Response: "⚠️ You're on the 'integration' branch, which is protected for testing purposes. Direct pushes may interfere with automated testing workflows.

Would you like to:
1. Create a feature branch instead
2. Create a PR to merge into integration
3. Continue anyway (if you manage the testing infrastructure)"
```

### Example 4: Emergency push to protected branch
```
User: "I need to push a hotfix to production"
Assistant: [Checks current branch: production]
Assistant: [Uses AskUserQuestion]
Question: "You're about to push to 'production', which is a protected branch. This bypasses the normal PR workflow. Are you sure?"
User: "Yes, it's an emergency hotfix"
Assistant: "Understood. Pushing to production..."
Command: git push
Response: "✅ Pushed to production. Remember to create a PR to document this change."
```

### Example 5: Branch not set up with remote
```
User: "Push my changes"
Assistant: [Checks current branch: feat/new-feature]
Assistant: [Detects no upstream branch]
Response: "This branch doesn't have an upstream set. Setting up and pushing..."
Command: git push -u origin feat/new-feature
Response: "Successfully pushed and set up tracking for 'feat/new-feature'."
```

## Error Handling

- **Not a git repository**: Inform user they need to be in a git repository
- **No commits to push**: Inform user there are no new commits to push
- **Remote not configured**: Help user set up a remote
- **Authentication issues**: Inform user to check their git credentials
- **Push rejected**: Check if they need to pull first or if there are conflicts
- **Protected branch**: Block push and suggest alternatives

## Best Practices

- **Never push directly to protected branches** without explicit confirmation
- **Always suggest feature branches** for new work
- **Encourage PR workflows** for protected branches
- **Set upstream on first push** to avoid future issues
- **Verify push success** before confirming to user
- **Respect testing infrastructure** by not pushing directly to testing branches

## Integration with Other Skills

This skill works with:
- **commit skill**: After committing, suggest pushing with this skill
- **checkout-branch skill**: After creating a branch, mention safe pushing
- **PR creation skills**: Suggest creating PRs instead of pushing to protected branches

## Configuration

Protected branches are defined in `.claude/protected-branches.json`. To add or remove protected branches, update that file.

Default protected branches include:
- Deployment: main, master, production, prod, staging, stage
- Development: dev, develop, development
- Release: release
- QA: qa, uat
- Testing: test, testing, integration, e2e
