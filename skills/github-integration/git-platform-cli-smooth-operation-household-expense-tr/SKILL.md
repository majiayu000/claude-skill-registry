---
name: git-platform-cli
description: "MANDATORY: Use gh (GitHub) or glab (GitLab) CLI for ALL issue/task management. Unified workflow across platforms."
---

# Git Platform CLI (MANDATORY)

## The Iron Law

**NO manual issue creation. ALWAYS use `gh` or `glab` CLI.**

This skill is **MANDATORY** for:
- Creating issues from tasks
- Linking commits to issues
- Managing project boards
- Creating pull/merge requests
- Reviewing code

## Why This Is Mandatory

**Authority**: Professional teams use CLI tools for:
- Automation and consistency
- Integration with workflows
- Traceability (commits ↔ issues)
- Faster than web UI
- Scriptable and repeatable

**Social Proof**: GitHub CLI has 34K+ stars, GitLab CLI has 2.8K+ stars. Industry standard.

## When to Use This Skill

- **ALWAYS** when creating tasks (TodoWrite)
- **ALWAYS** when committing code
- **ALWAYS** when creating PR/MR
- **ALWAYS** when managing project work

## Installation (MANDATORY)

### Check if installed

```bash
gh --version
glab --version
```

If either missing, **STOP** and install:

### GitHub CLI (gh)

**Windows**:
```bash
winget install GitHub.cli
```

**macOS**:
```bash
brew install gh
```

**Linux**:
```bash
# Debian/Ubuntu
sudo apt install gh

# Fedora/RHEL
sudo dnf install gh
```

### GitLab CLI (glab)

**Windows**:
```bash
# Download from https://gitlab.com/gitlab-org/cli/-/releases
# Or use scoop: scoop install glab
```

**macOS**:
```bash
brew install glab
```

**Linux**:
```bash
# Debian/Ubuntu
sudo apt install glab

# Fedora/RHEL
sudo dnf install glab
```

### Authenticate (REQUIRED)

```bash
# GitHub
gh auth login

# GitLab
glab auth login
```

## Core Workflow: Tasks → Issues

### Pattern: TodoWrite Creates GitHub/GitLab Issues

**MANDATORY**: When using TodoWrite for tasks, ALWAYS create corresponding issues.

**Example Workflow**:

```markdown
User: "Add authentication feature to the API"

Agent:
1. I'm using the brainstorming skill to discuss the approach
2. I'm using the writing-plans skill to break into tasks:

   Tasks:
   - Create User model with authentication fields
   - Add JWT token generation
   - Implement login/register endpoints
   - Write authentication middleware
   - Add tests

3. I'm using the git-platform-cli skill to create issues:

For GitHub repo:
```bash
gh issue create --title "Add User model with authentication fields" \
  --body "Part of authentication feature. Create User model with email, password_hash, etc." \
  --label "feature,backend" \
  --milestone "v1.0"

gh issue create --title "Add JWT token generation" \
  --body "Implement JWT signing and verification for authentication" \
  --label "feature,backend,security"

# Repeat for all tasks...
```

For GitLab repo:
```bash
glab issue create --title "Add User model with authentication fields" \
  --description "Part of authentication feature..." \
  --label "feature,backend"

glab issue create --title "Add JWT token generation" \
  --description "Implement JWT signing..." \
  --label "feature,backend,security"

# Repeat for all tasks...
```

4. Issues created:
   ✅ #42: Add User model
   ✅ #43: Add JWT token generation
   ✅ #44: Implement login/register endpoints
   ✅ #45: Write authentication middleware
   ✅ #46: Add tests

5. Now implementing tasks, linking commits to issues...
```

## Linking Commits to Issues (MANDATORY)

### GitHub (gh)

**In commit messages, reference issues**:

```bash
git commit -m "feat(auth): add User model with authentication fields

Implements password hashing with bcrypt, email validation.

Closes #42"
```

**Keywords that close issues**:
- `Closes #42`
- `Fixes #42`
- `Resolves #42`

### GitLab (glab)

**Same syntax**:

```bash
git commit -m "feat(auth): add User model

Closes #42"
```

**Also supports**:
- `Implements #42`
- `Closes #42`
- `Fixes #42`

## Creating Pull/Merge Requests (MANDATORY)

### GitHub (gh)

```bash
# Create PR from current branch
gh pr create --title "Add authentication feature" \
  --body "$(cat <<'EOF'
## Summary
- ✅ User model with bcrypt hashing
- ✅ JWT token generation
- ✅ Login/register endpoints
- ✅ Authentication middleware
- ✅ Tests (100% coverage)

## Test Plan
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Manual testing completed

## Closes
- Closes #42
- Closes #43
- Closes #44
- Closes #45
- Closes #46
EOF
)" \
  --assignee @me \
  --label "feature" \
  --reviewer "team-lead"

# Get PR URL
gh pr view --web
```

### GitLab (glab)

```bash
# Create MR from current branch
glab mr create --title "Add authentication feature" \
  --description "$(cat <<'EOF'
## Summary
- ✅ User model with bcrypt hashing
- ✅ JWT token generation
- ✅ Login/register endpoints

## Closes
- Closes #42
- Closes #43
EOF
)" \
  --assignee @me \
  --label "feature" \
  --remove-source-branch

# Get MR URL
glab mr view --web
```

## Task Management Integration

### Workflow: TodoWrite → Issues → Commits → PR/MR

**MANDATORY Sequence**:

1. **TodoWrite creates tasks**:
   ```
   - Task 1: Add User model
   - Task 2: Add JWT generation
   - Task 3: Implement endpoints
   ```

2. **Create issues immediately** (git-platform-cli skill):
   ```bash
   # GitHub
   gh issue create --title "Task 1: Add User model" ...
   gh issue create --title "Task 2: Add JWT generation" ...

   # GitLab
   glab issue create --title "Task 1: Add User model" ...
   ```

3. **Work on tasks, commit with issue refs**:
   ```bash
   git commit -m "feat(auth): add User model

   Closes #42"
   ```

4. **Create PR/MR linking all issues**:
   ```bash
   gh pr create --title "Feature" --body "Closes #42, #43, #44"
   ```

## Checking Issue Status

### GitHub (gh)

```bash
# List open issues
gh issue list

# View specific issue
gh issue view 42

# Close issue
gh issue close 42 --comment "Completed in PR #50"

# Reopen issue
gh issue reopen 42
```

### GitLab (glab)

```bash
# List open issues
glab issue list

# View specific issue
glab issue view 42

# Close issue
glab issue close 42 --note "Completed in MR !50"

# Reopen issue
glab issue reopen 42
```

## Project Board Management

### GitHub (gh)

```bash
# List projects
gh project list

# Add issue to project
gh project item-add <project-number> --owner @me --url <issue-url>

# Update issue status
gh project item-edit --id <item-id> --field-id <field-id> --project-id <project-id> --text "In Progress"
```

### GitLab (glab)

```bash
# GitLab boards managed via web UI or API
# Use glab api for advanced board management
```

## Common Patterns

### Pattern 1: Feature Branch Workflow

```bash
# 1. Create feature branch
git checkout -b feature/auth

# 2. Create issues for all tasks
gh issue create --title "Task 1" --label "feature"
gh issue create --title "Task 2" --label "feature"

# 3. Work on tasks, commit with issue refs
git commit -m "feat: task 1

Closes #42"

# 4. Push and create PR
git push -u origin feature/auth
gh pr create --fill

# 5. Merge PR (closes all linked issues automatically)
gh pr merge --squash --delete-branch
```

### Pattern 2: Bug Fix Workflow

```bash
# 1. Create issue for bug
gh issue create --title "Bug: Login fails with empty email" \
  --label "bug" \
  --body "Steps to reproduce..."

# 2. Create bugfix branch
git checkout -b bugfix/login-validation

# 3. Fix bug, commit with issue ref
git commit -m "fix(auth): validate email before login

Fixes #43"

# 4. Create PR
gh pr create --title "Fix: Login validation" --body "Fixes #43"

# 5. Merge (auto-closes issue)
gh pr merge --squash
```

### Pattern 3: Multi-Task Feature

```bash
# 1. Brainstorm → create parent issue
gh issue create --title "Feature: Add authentication" \
  --body "Parent issue for authentication feature" \
  --label "epic"

# 2. Create sub-task issues
gh issue create --title "Sub-task: User model" --body "Part of #50"
gh issue create --title "Sub-task: JWT tokens" --body "Part of #50"
gh issue create --title "Sub-task: Endpoints" --body "Part of #50"

# 3. Work on each sub-task
git commit -m "feat(auth): add User model

Part of #50, closes #51"

# 4. Final PR references parent
gh pr create --body "Closes #50, #51, #52, #53"
```

## Issue Templates

### Feature Request Template

```bash
gh issue create --title "Feature: <title>" --body "$(cat <<'EOF'
## Problem Statement
[Describe the problem this feature solves]

## Proposed Solution
[Describe your proposed solution]

## Alternatives Considered
[Other approaches you considered]

## Additional Context
[Any other relevant information]
EOF
)"
```

### Bug Report Template

```bash
gh issue create --title "Bug: <title>" --label "bug" --body "$(cat <<'EOF'
## Bug Description
[Clear description of the bug]

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS:
- Version:
- Browser (if applicable):

## Additional Context
[Screenshots, logs, etc.]
EOF
)"
```

## Red Flags (Bad Practices)

- ❌ Creating issues manually in web UI → Use CLI
- ❌ Committing without issue references → Always link
- ❌ Creating PR without linking issues → Always link
- ❌ Not closing issues when merging → Use "Closes #X"
- ❌ Using TodoWrite without creating issues → Always create
- ❌ One giant issue for multiple tasks → Break into sub-tasks

## Integration with Other Skills

**Before git-platform-cli**:
- `brainstorming` - Understand feature scope
- `writing-plans` - Break into tasks

**During git-platform-cli**:
- Create issues for all tasks
- Link commits to issues
- Track progress on board

**After git-platform-cli**:
- `git-workflow` - Make commits with issue refs
- `finishing-a-development-branch` - Create PR/MR
- `code-review` - Review before merge

## Automation Examples

### Auto-create issues from TodoWrite

```bash
# Script: create-issues-from-tasks.sh

#!/bin/bash
# Parse TASKS.md and create GitHub issues

while IFS= read -r line; do
  if [[ $line =~ ^-\ \[\ \]\ (.+) ]]; then
    task="${BASH_REMATCH[1]}"
    gh issue create --title "$task" --label "task" --assignee @me
  fi
done < TASKS.md
```

### Auto-link commits to issues

```bash
# Git hook: prepare-commit-msg

#!/bin/bash
# Auto-add issue reference if branch name contains issue number

BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ $BRANCH =~ issue-([0-9]+) ]]; then
  ISSUE="${BASH_REMATCH[1]}"
  echo "" >> "$1"
  echo "Refs #$ISSUE" >> "$1"
fi
```

## Your Commitment

Before proceeding with ANY project work:

- [ ] I have `gh` installed and authenticated
- [ ] I have `glab` installed and authenticated (if using GitLab)
- [ ] I will create issues for ALL tasks
- [ ] I will reference issues in ALL commits
- [ ] I will link issues in ALL PRs/MRs
- [ ] I will close issues when merging

---

**Bottom Line**: Git platform CLIs (gh/glab) are MANDATORY for professional development. They provide automation, traceability, and integration that manual web UI usage cannot match.

**Use them for EVERYTHING**.
