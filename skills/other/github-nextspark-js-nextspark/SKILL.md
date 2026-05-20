---
name: github
description: |
  GitHub workflow patterns for branch management, commits, and pull requests.
  Covers gitflow, branch naming conventions, commit messages, and PR creation.
  Use this skill for any Git/GitHub operations following project conventions.
allowed-tools: Read, Glob, Grep, Bash
version: 1.0.0
---

# GitHub Workflow Skill

Git and GitHub workflow patterns with configurable conventions.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     GITHUB WORKFLOW                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐     │
│  │   Claude    │────►│  github.json │────►│   gh CLI     │     │
│  │   Session   │     │   (config)   │     │  (commands)  │     │
│  └─────────────┘     └──────────────┘     └──────────────┘     │
│         │                    │                    │             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐     │
│  │  Task       │     │  Gitflow     │     │   GitHub     │     │
│  │  Manager    │◄───►│  Branches    │────►│   Remote     │     │
│  │  (ClickUp)  │     │              │     │              │     │
│  └─────────────┘     └──────────────┘     └──────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Creating feature, bugfix, or hotfix branches
- Making commits with proper conventions
- Creating pull requests with correct format
- Promoting code between environments (develop → qa → main)
- Understanding project's gitflow configuration

---

## Configuration

### Config Files

| File | Purpose |
|------|---------|
| `.claude/config/github.json` | Git workflow, branches, commits, PRs |
| `.claude/config/team.json` | Team members, roles, permissions |
| `.claude/config/workspace.json` | Task manager integration |

### Issue Key Integration

The issue key format comes from the task manager configured in `.claude/config/workspace.json`:

```javascript
// Read task manager provider
const workspace = await Read('.claude/config/workspace.json')
const provider = workspace.taskManager.provider // "clickup", "jira", etc.

// Issue key formats by provider:
// - ClickUp: "CU-abc123" or task ID
// - Jira: "PROJECT-123"
// - GitHub Issues: "#123"
```

---

## Gitflow Configuration

### Default Flow

```
feature/* ──► develop ──► qa ──► main
                │
hotfix/*  ─────┴─────────────────► main
```

### Environment Branches

| Branch | Purpose | Protected By |
|--------|---------|--------------|
| `main` | Production | qa |
| `qa` | QA/Staging | develop |
| `develop` | Integration | feature branches |

### Configuration Example

```json
{
  "gitflow": {
    "environments": ["develop", "qa", "main"],
    "featureBranch": {
      "baseBranch": "main",
      "targetBranch": "develop"
    },
    "hotfixBranch": {
      "baseBranch": "main",
      "targetBranch": "main",
      "skipEnvironments": true
    },
    "promotionFlow": {
      "develop": "qa",
      "qa": "main"
    }
  }
}
```

---

## Branch Operations

### Creating a Branch

**Step 1: Read Configuration**

```javascript
const github = await Read('.claude/config/github.json')
const team = await Read('.claude/config/team.json')

// Resolve active user: git config → CLAUDE_USER env → single-member auto
const gitName = exec('git config user.name')
const gitEmail = exec('git config user.email')
let activeUser = team.members.find(m => m.name === gitName || m.email === gitEmail)
if (!activeUser) {
  const envUser = process.env.CLAUDE_USER
  if (envUser) activeUser = team.members.find(m => m.name === envUser)
}
if (!activeUser && team.members.length === 1) activeUser = team.members[0]
const initials = activeUser.initials // "pc"

const branchType = "feature" // or "bugfix", "hotfix", "chore"
const typeConfig = github.branches.types[branchType]
const baseBranch = typeConfig.base // "main"
```

**Step 2: Get Issue Key**

```javascript
// From active session or ask user
const issueKey = session.taskId || await AskUser("Issue key?")
```

**Step 3: Build Branch Name**

Pattern: `{type}/{issue-key}-{description}-{initials}`

```bash
# Example
git checkout main
git pull origin main
git checkout -b feature/CU-abc123-add-user-auth-pc
```

### Branch Naming Convention

| Component | Required | Example |
|-----------|----------|---------|
| Type | Yes | `feature`, `bugfix`, `hotfix`, `chore` |
| Issue Key | Yes* | `CU-abc123`, `PROJ-456` |
| Description | Yes | `add-user-auth` (max 4-5 words, hyphens) |
| Initials | Yes | `pc` (from team config) |

*If `commits.requireIssueKey` is false, can be omitted.

### Valid Examples

```
feature/CU-abc123-add-user-authentication-pc
bugfix/CU-def456-fix-login-validation-jd
hotfix/CU-ghi789-critical-security-patch-pc
chore/CU-jkl012-update-dependencies-jd
```

### Invalid Examples

```
feature/add-auth                    # Missing issue key and initials
CU-abc123-new-feature              # Missing type prefix
feature/CU-abc123_add_auth_pc      # Underscores instead of hyphens
```

---

## Commit Operations

### Commit Message Convention

Pattern: `[{issue-key}] {description}`

**Step 1: Stage Changes**

```bash
git add .
# Or specific files
git add src/components/Login.tsx
```

**Step 2: Create Commit**

```bash
git commit -m "[CU-abc123] Add user authentication form"
```

### Suggested Prefixes

| Prefix | Use When |
|--------|----------|
| Add | New feature or file |
| Fix | Bug fix |
| Update | Modifying existing functionality |
| Refactor | Code restructuring without behavior change |
| Remove | Deleting code or features |
| Improve | Performance or UX enhancements |
| Implement | Completing a feature |

### Valid Examples

```
[CU-abc123] Add login form validation
[CU-abc123] Fix password reset flow
[CU-abc123] Update user profile API endpoint
[CU-abc123] Refactor authentication middleware
```

### Commit Locally by Default

**IMPORTANT:** Commits should be LOCAL ONLY unless user explicitly requests push.

```bash
# Local commit (default)
git commit -m "[CU-abc123] Add feature"

# Push only when requested
git push origin feature/CU-abc123-add-feature-pc
```

---

## Pull Request Operations

### Creating a PR

**Step 1: Push Branch**

```bash
git push -u origin feature/CU-abc123-add-user-auth-pc
```

**Step 2: Select Reviewer**

```javascript
// Read team from config
const team = await Read('.claude/config/team.json')
const reviewers = team.members.filter(m => m.permissions.canReview)

// Present options to user
const reviewer = await AskUser({
  question: "Who should review this PR?",
  options: reviewers.map(m => ({ label: m.name, value: m.ids.github }))
})
```

**Step 3: Create PR**

```bash
gh pr create \
  --title "[CU-abc123] Add user authentication" \
  --body "## Description
Add user authentication form with validation.

## Changes
- Add LoginForm component
- Add validation schema
- Add auth API endpoint

## Testing
- [ ] Test valid login
- [ ] Test invalid credentials
- [ ] Test password reset

## Related Issues
- CU-abc123" \
  --base develop \
  --reviewer "capellopablo"
```

**Step 4: Share PR Link**

```bash
PR_URL=$(gh pr view --json url -q .url)
echo "Pull Request created: $PR_URL"
```

### PR Title Convention

Pattern: `[{issue-key}] {description}`

| Valid | Invalid |
|-------|---------|
| `[CU-abc123] Add user auth` | `CU-abc123 - Add auth` |
| `[PROJ-456] Fix login bug` | `[proj-456] fix login` |

### PR Base Branch

| Branch Type | Base Branch |
|-------------|-------------|
| feature/* | develop |
| bugfix/* | develop |
| hotfix/* | main |
| chore/* | develop |

---

## Environment Promotion

### Promoting Code Between Environments

```
develop ──► qa ──► main
```

**Step 1: Create Promotion PR**

```bash
# From develop to qa
gh pr create \
  --title "Promote develop to qa" \
  --body "Environment promotion" \
  --base qa \
  --head develop

# From qa to main
gh pr create \
  --title "Promote qa to main" \
  --body "Environment promotion" \
  --base main \
  --head qa
```

**Step 2: Merge After Approval**

```bash
gh pr merge --squash
```

---

## Common Commands Reference

### Branch Operations

```bash
# List branches
git branch -a

# Switch branch
git checkout develop

# Delete local branch
git branch -d feature/CU-abc123-old-feature-pc

# Delete remote branch
git push origin --delete feature/CU-abc123-old-feature-pc
```

### PR Operations

```bash
# Check PR status
gh pr status

# View PR details
gh pr view

# Add reviewers
gh pr edit --add-reviewer "username1,username2"

# Merge PR
gh pr merge --squash

# Close PR without merging
gh pr close
```

### Commit Operations

```bash
# View recent commits
git log --oneline -10

# Amend last commit (only if not pushed)
git commit --amend -m "[CU-abc123] Updated message"

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

## Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│                    WHAT DO YOU NEED TO DO?                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Start new work?                                                │
│  └─► Create branch from main                                    │
│      └─► git checkout -b {type}/{issue}-{desc}-{initials}       │
│                                                                 │
│  Save progress?                                                 │
│  └─► Commit locally                                             │
│      └─► git commit -m "[{issue}] {description}"                │
│                                                                 │
│  Ready for review?                                              │
│  └─► Push & create PR                                           │
│      └─► git push -u origin {branch}                            │
│      └─► gh pr create --base develop                            │
│                                                                 │
│  Urgent fix needed?                                             │
│  └─► Create hotfix branch from main                             │
│      └─► git checkout -b hotfix/{issue}-{desc}-{initials}       │
│      └─► PR directly to main                                    │
│                                                                 │
│  Promote to next env?                                           │
│  └─► Create promotion PR                                        │
│      └─► gh pr create --base {next-env} --head {current-env}    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Checklist Templates

### Branch Creation Checklist

- [ ] On latest main: `git checkout main && git pull`
- [ ] Branch name follows pattern
- [ ] Issue key is valid
- [ ] Description is concise (4-5 words max)
- [ ] Initials match team config

### Commit Checklist

- [ ] Message follows pattern: `[{issue}] {description}`
- [ ] Description starts with verb (Add, Fix, Update...)
- [ ] Changes are related to single issue
- [ ] No secrets or credentials committed

### PR Checklist

- [ ] Branch pushed to remote
- [ ] Title follows pattern
- [ ] Description filled with changes
- [ ] Testing steps documented
- [ ] Reviewer selected
- [ ] Base branch is correct (develop/main)
