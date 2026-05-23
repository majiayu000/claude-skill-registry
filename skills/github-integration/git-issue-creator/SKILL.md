---
name: git-issue-creator
description: GitHub issue creation with semantic commit formatting and automatic label assignment, extending git-issue-labeler, git-semantic-commits, git-issue-updater, and ticket-branch-workflow
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: github-issue-branch
---

## What I do

I implement GitHub issue creation with automatic label assignment and semantic commit formatting by extending framework skills:

1. **Analyze Request**: Parse the user's statement to determine issue type and content
2. **Assign Labels**: Use `git-issue-labeler` framework to assign GitHub default labels (bug, enhancement, documentation, duplicate, good first issue, help wanted, invalid, question, wontfix)
3. **Format Commits**: Use `git-semantic-commits` framework for semantic commit message formatting (Conventional Commits specification)
4. **Create GitHub Issue**: Use `gh issue create` with title, description, assigned labels, and assignee
5. **Update Issue Progress**: Use `git-issue-updater` framework to add progress comments with user, date, time, and commit details
6. **Delegate to Framework**: Use `ticket-branch-workflow` for branch creation, PLAN.md, commit (using git-semantic-commits), and push
7. **Display Summary**: Show issue URL, branch name, and framework completion status

## When to use me

**Frameworks Used**: This skill extends multiple framework skills:
- `git-issue-labeler` - For GitHub default label assignment (bug, enhancement, documentation, duplicate, good first issue, help wanted, invalid, question, wontfix)
- `git-semantic-commits` - For semantic commit message formatting (Conventional Commits specification)
- `git-issue-updater` - For updating issues with commit progress including user, date, time
- `ticket-branch-workflow` - For core workflow (branch creation, PLAN.md, commit, push)

Use this workflow when:
- You need to create a GitHub issue with automatic label assignment
- You want semantic commit message formatting (Conventional Commits)
- You want automatic issue progress updates with consistent documentation
- You want the complete workflow: issue → branch → PLAN.md → commit → issue update → push
- You prefer GitHub CLI (`gh`) for issue creation over manual entry

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Git repository initialized
- Write access to the GitHub repository
- Valid `GITHUB_TOKEN` or `gh` authentication setup
- `git-issue-labeler` skill available in skills/ directory
- `git-semantic-commits` skill available in skills/ directory
- `git-issue-updater` skill available in skills/ directory
- `ticket-branch-workflow` skill available in skills/ directory

## Steps

### Step 1: Analyze the Request
- Read the user's statement describing the issue
- Extract title and description for issue creation
- Identify any specific requirements or constraints mentioned

### Step 2: Assign Labels Using git-issue-labeler
- Use `git-issue-labeler` framework to determine appropriate GitHub default labels
- Analyze user statement for issue type indicators
- Assign labels from GitHub defaults: bug, enhancement, documentation, duplicate, good first issue, help wanted, invalid, question, wontfix
- Let git-issue-labeler handle keyword matching and label detection

**Label Detection Logic** (Delegated to git-issue-labeler):
```bash
# git-issue-labeler will analyze the statement
# and determine appropriate GitHub default labels
# Example: "Fix login error" → labels: bug
# Example: "Add dark mode" → labels: enhancement, good first issue
```

### Step 3: Create GitHub Issue
- Get the current authenticated GitHub user:
  ```bash
  gh api user --jq '.login'
  ```
- Use `gh issue create` command with labels from git-issue-labeler:
  ```bash
  gh issue create --title "<Issue Title>" --body "<Issue Description>" --label "<label1>,<label2>" --assignee @me
  ```
- Format the issue body:
  ```markdown
  ## Description
  <Detailed description of the issue>

  ## Type
  <Primary label>

  ## Labels
  - <label1>
  - <label2>

  ## Context
  <Additional context or background information>

  ## Acceptance Criteria
  - <Criteria 1>
  - <Criteria 2>
  ```
- Store the issue number, URL, and assignee for reference

### Step 4: Execute Ticket-Branch-Workflow
- Use `ticket-branch-workflow` for the following steps:
  - Create GitHub branch: `git checkout -b issue-<issue-number>` or `feature/<issue-number>-<short-title>`
  - Create PLAN.md with issue reference
  - Format commit using git-semantic-commits: `docs(plan): add PLAN.md for #<issue-number>`
  - Commit PLAN.md: `git commit -m "$(git-semantic-commits --type docs --scope plan --subject 'Add PLAN.md for #<issue-number>')"`
  - Push branch: `git push -u origin <branch-name>`

### Step 5: Update Issue with Commit Progress Using git-issue-updater
- Use `git-issue-updater` framework to add progress comment to GitHub issue
- Extract commit details: hash, message, author, date, time, files changed
- Format comment with consistent documentation including user, date, time
- Add comment to GitHub issue with link to commit

**Issue Update Logic** (Delegated to git-issue-updater):
```bash
# After committing PLAN.md, update issue with progress
git-issue-updater --issue <issue-number> --platform github

# This will:
# 1. Extract latest commit details
# 2. Format comment with user, date, time
# 3. Add comment to GitHub issue
# 4. Link to commit for reference
```

### Step 5: Display Summary
- Display issue and framework completion status:
  ```
  ✅ GitHub Issue #<issue-number> created successfully!
  ✅ Labels assigned: <labels> (via git-issue-labeler)
  ✅ Branch created and checked out: <branch-name>
  ✅ PLAN.md created with semantic commit (via git-semantic-commits)
  ✅ Issue updated with progress comment (via git-issue-updater)
  ✅ Branch pushed to remote (via ticket-branch-workflow)

  **Issue Details**:
  - Title: <issue-title>
  - URL: <issue-url>
  - Labels: <labels> (assigned by git-issue-labeler)
  - Assignee: <current-user>

  **Branch**:
  - Name: <branch-name>
  - Base Branch: <previous-branch>
  - Remote: origin/<branch-name>

  **PLAN.md**:
  - Created at: ./PLAN.md
  - Committed with semantic format: docs(plan): add PLAN.md
  - Pushed: Yes

  **Issue Update**:
  - Comment added: Yes (via git-issue-updater)
  - User: <commit-author>
  - Date: <commit-date>
  - Time: <commit-time>

  You're now on the new branch and ready to start implementation!
  ```

## Examples

### Example 1: Bug Fix with Automatic Labeling

**User Input**: "Fix the login error when user enters invalid credentials"

**Workflow Execution**:
1. **git-issue-labeler**: Analyzes statement → assigns `bug` label
2. **GitHub Issue Creation**: Creates issue #123 with title and bug label
3. **ticket-branch-workflow**: Creates branch `issue-123`, PLAN.md
4. **git-semantic-commits**: Formats commit as `docs(plan): add PLAN.md for #123`
5. **git-issue-updater**: Adds progress comment with user, date, time
6. **Push**: Branch pushed to remote

**Result**:
```
✅ GitHub Issue #123 created successfully!
✅ Labels assigned: bug (via git-issue-labeler)
✅ Branch created and checked out: issue-123
✅ PLAN.md created with semantic commit: docs(plan): add PLAN.md for #123
✅ Issue updated with progress comment (via git-issue-updater)
✅ Branch pushed to remote

Issue Details:
- Title: Fix the login error when user enters invalid credentials
- URL: https://github.com/org/repo/issues/123
- Labels: bug
- Assignee: @john-doe

Issue Update:
- Comment added: Yes
- User: John Doe (john.doe@example.com)
- Date: 2024-01-25
- Time: 14:30 UTC+08:00
```

### Example 2: New Feature with Multiple Labels

**User Input**: "Add support for dark mode in the dashboard and make it good for newcomers"

**Workflow Execution**:
1. **git-issue-labeler**: Analyzes statement → assigns `enhancement`, `good first issue` labels
2. **GitHub Issue Creation**: Creates issue #124 with title and labels
3. **ticket-branch-workflow**: Creates branch `issue-124`, PLAN.md
4. **git-semantic-commits**: Formats commit as `docs(plan): add PLAN.md for #124`
5. **git-issue-updater**: Adds progress comment with user, date, time
6. **Push**: Branch pushed to remote

**Result**:
```
✅ GitHub Issue #124 created successfully!
✅ Labels assigned: enhancement, good first issue (via git-issue-labeler)
✅ Branch created and checked out: issue-124
✅ PLAN.md created with semantic commit: docs(plan): add PLAN.md for #124
✅ Issue updated with progress comment (via git-issue-updater)
✅ Branch pushed to remote

Issue Details:
- Title: Add support for dark mode in the dashboard
- URL: https://github.com/org/repo/issues/124
- Labels: enhancement, good first issue
- Assignee: @jane-smith
```

### Example 3: Documentation Update

**User Input**: "Document the API endpoints for the authentication module"

**Workflow Execution**:
1. **git-issue-labeler**: Analyzes statement → assigns `documentation` label
2. **GitHub Issue Creation**: Creates issue #125 with title and documentation label
3. **ticket-branch-workflow**: Creates branch `issue-125`, PLAN.md
4. **git-semantic-commits**: Formats commit as `docs(plan): add PLAN.md for #125`
5. **git-issue-updater**: Adds progress comment with user, date, time
6. **Push**: Branch pushed to remote

**Result**:
```
✅ GitHub Issue #125 created successfully!
✅ Labels assigned: documentation (via git-issue-labeler)
✅ Branch created and checked out: issue-125
✅ PLAN.md created with semantic commit: docs(plan): add PLAN.md for #125
✅ Issue updated with progress comment (via git-issue-updater)
✅ Branch pushed to remote
```

## PLAN.md Template Structure

The framework generates PLAN.md with this structure:
```markdown
# Plan: <Issue Title>

## Overview
Brief description of what this issue implements or fixes.

## Issue Reference
- Issue: #<issue-number>
- URL: <issue-url>
- Labels: <label1>, <label2>, <label3>

## Files to Modify
1. `src/path/to/file1.ts` - Description of changes
2. `src/path/to/file2.tsx` - Description of changes
3. `README.md` - Documentation updates

## Approach
Detailed steps or methodology for implementation:

1. **Step 1**: Description
2. **Step 2**: Description
3. **Step 3**: Description

## Success Criteria
- [ ] All files modified correctly
- [ ] No build errors
- [ ] All tests pass
- [ ] Code review completed

## Notes
Any additional notes, constraints, or considerations.
```

## Best Practices

- Always provide clear, descriptive issue titles
- Include sufficient context in issue description
- Assign issues to yourself (`--assignee @me`) for accountability
- Let `git-issue-labeler` framework handle label detection (GitHub default labels: bug, enhancement, documentation, duplicate, good first issue, help wanted, invalid, question, wontfix)
- Let `git-semantic-commits` framework handle commit message formatting (Conventional Commits specification)
- Let `git-issue-updater` framework handle issue progress updates with user, date, time
- Use semantic branch names that reference the issue number
- Confirm the issue URL is accessible
- The frameworks handle branch creation, PLAN.md, commit, and push automatically
- Keep issue titles concise (under 72 characters preferred)
- Update the issue with a comment linking to the PR when ready
- Framework delegation reduces code duplication and improves maintainability

## Common Issues

### GitHub CLI Not Authenticated
**Issue**: `gh issue create` fails with authentication error

**Solution**: Run `gh auth login` to authenticate with GitHub

### Repository Not Initialized
**Issue**: Git commands fail with "not a git repository"

**Solution**: Initialize the repository: `git init` and set up remote: `git remote add origin <repo-url>`

### Branch Already Exists
**Issue**: Branch checkout fails due to existing branch

**Solution**: The framework handles this with `-B` flag to force branch creation

### No Labels Detected
**Issue**: Issue created without labels

**Solution**: Default to `enhancement` label (via git-issue-labeler)
Note: git-issue-labeler should still be called to ensure consistent label assignment even when no keywords match

### PLAN.md Already Exists
**Issue**: PLAN.md file already exists in the branch

**Solution**: The framework handles this by asking if you want to overwrite or append

## Troubleshooting Checklist

Before creating the issue:
- [ ] GitHub CLI is installed: `gh --version`
- [ ] GitHub CLI is authenticated: `gh auth status`
- [ ] Git repository is initialized: `git status`
- [ ] Current branch is clean (no uncommitted changes)
- [ ] Remote repository is set up: `git remote -v`

After issue creation:
- [ ] Issue number is captured
- [ ] Issue URL is accessible
- [ ] Labels are correctly applied
- [ ] Issue is assigned to current user
- [ ] Framework completes successfully: branch created, PLAN.md committed, branch pushed

## Related Commands

```bash
# View current authenticated GitHub user
gh api user --jq '.login'

# List issues in the repository
gh issue list

# View issue details
gh issue view <issue-number>

# Edit an issue
gh issue edit <issue-number> --title "New Title" --body "New Description"

# Assign issue to yourself
gh issue edit <issue-number> --add-assignee @me

# Delete an issue
gh issue delete <issue-number>

# Format commit message using git-semantic-commits
git-semantic-commits --type docs --scope plan --subject "Add PLAN.md for #123"

# Update issue with commit progress using git-issue-updater
git-issue-updater --issue 123 --platform github
```

## Related Skills

- **Frameworks**:
  - `ticket-branch-workflow` - Provides core workflow (branch creation, PLAN.md, commit, push)
  - `git-issue-labeler` - Provides GitHub default label assignment (bug, enhancement, documentation, duplicate, good first issue, help wanted, invalid, question, wontfix)
  - `git-semantic-commits` - Provides semantic commit message formatting (Conventional Commits specification)
  - `git-issue-updater` - Provides issue progress updates with user, date, time
- `jira-git-integration` - Provides JIRA-specific operations when working with JIRA tickets

- **Related Workflows**:
  - `nextjs-pr-workflow`: For creating PRs after completing the issue
  - `jira-git-workflow`: For JIRA-integrated workflows (uses same ticket-branch-workflow framework)
  - `git-pr-creator`: For creating PRs with optional JIRA integration
  - `pr-creation-workflow`: For generic PR creation with configurable quality checks
