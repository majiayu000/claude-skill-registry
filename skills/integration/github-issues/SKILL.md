---
name: agent-github-issues
description: GitHub Issues expert for gh issue create, gh issue list, labels, milestones, epics, features, tasks, bugs, priorities, mvp-blocker, critical, high-priority, issue tracking, project management, issue queries, workflows, acceptance criteria, task breakdown
allowed-tools: Read, Bash
---

# GitHub Issues Management Skill

Expert in GitHub Issues organization and workflow management.

## When to Use This Skill

Use this skill when:

- Creating new issues (bugs, features, tasks)
- Organizing issues with labels and milestones
- Querying and filtering work items
- Tracking project progress
- Managing issue lifecycle

## Issue Creation Workflow

### 1. Determine Issue Type

**Epic** - Large initiative spanning multiple features (weeks/months)

- Label: `epic`
- Create milestone for tracking
- Examples: "User Management System", "Analytics Dashboard"

**Feature** - User-facing functionality (days to 2 weeks)

- Label: `feature`
- Link to epic milestone
- Examples: "Password Reset Flow", "Export Reports"

**Task** - Technical implementation work (hours to 3 days)

- Label: `task`
- Add area labels: `frontend`, `backend`, `database`
- Reference parent feature: "Part of #XXX"
- Examples: "Create users table", "Build login form"

**Bug** - Defect or broken functionality

- Label: `bug`
- Add priority: `critical`, `high-priority`, `mvp-blocker`
- Include reproduction steps

### 2. Create Issue with Proper Structure

```bash
# Create feature
gh issue create \
  --title "Feature: User Profile Management" \
  --body "## Description
Allow users to view and edit their profile information.

## Requirements
- View profile page with user details
- Edit form for updating information
- Email verification for email changes
- Avatar upload functionality

## Acceptance Criteria
- [ ] Users can view their profile
- [ ] Users can edit first/last name
- [ ] Email changes require verification
- [ ] Avatar uploads work with image validation
- [ ] All changes persist correctly

## Tasks
Will be broken down into implementation tasks." \
  --label "feature" \
  --milestone "MVP Launch"
```

```bash
# Create task
gh issue create \
  --title "Task: Create user profiles database table" \
  --body "## Description
Create database migration for user profiles table.

Part of #105 (User Profile Management)

## Requirements
- Add firstName, lastName, avatarUrl columns to users table
- Create migration file with idempotency
- Update init.sql

## Acceptance Criteria
- [ ] Migration file created
- [ ] camelCase column names
- [ ] Idempotency tested
- [ ] init.sql updated" \
  --label "task,database" \
  --milestone "MVP Launch"
```

```bash
# Create bug
gh issue create \
  --title "Bug: Login button not working on mobile" \
  --body "## Description
Login button does not respond to taps on mobile devices.

## Reproduction Steps
1. Open app on mobile device
2. Navigate to login page
3. Tap login button
4. Nothing happens

## Expected Behavior
Login button should submit form and navigate to dashboard.

## Actual Behavior
Button does not respond to touch events.

## Environment
- Device: iPhone 12
- OS: iOS 16
- Browser: Safari" \
  --label "bug,frontend,mvp-blocker"
```

### 3. Organize with Labels

**Issue Types:**

- `epic` - Large initiatives
- `feature` - User-facing features
- `task` - Implementation work
- `bug` - Defects

**Areas:**

- `frontend` - Angular UI work
- `backend` - Fastify API work
- `database` - Schema/migration work

**Priority:**

- `mvp-blocker` - Must fix before launch
- `critical` - Blocks core functionality
- `high-priority` - Important for current milestone
- `medium-priority`, `low-priority`

**Workflow:**

- `in-progress` - Currently being worked on
- `blocked` - Waiting on dependency

## Querying and Filtering

### Find Next Priority Work

```bash
# Find MVP blockers
gh issue list --label "mvp-blocker" --state open

# Find critical bugs
gh issue list --label "bug,critical" --state open

# Find high-priority features
gh issue list --label "feature,high-priority" --state open
```

### Check Milestone Progress

```bash
# List all milestones
gh milestone list

# View issues in milestone
gh issue list --milestone "MVP Launch" --state open

# See completed work
gh issue list --milestone "MVP Launch" --state closed
```

### Filter by Area

```bash
# Frontend tasks
gh issue list --label "frontend,task" --state open

# Backend work
gh issue list --label "backend" --state open

# Database migrations needed
gh issue list --label "database" --state open
```

### Find Work to Start

```bash
# Tasks not yet started (no in-progress label)
gh issue list --label "task" --state open --search "-label:in-progress -label:blocked"

# Features ready for breakdown
gh issue list --label "feature" --state open --search "NOT linked:issue"
```

## Issue Lifecycle Management

### Mark as In Progress

```bash
gh issue edit <NUMBER> --add-label "in-progress"
```

### Add Progress Updates

```bash
gh issue comment <NUMBER> --body "Progress update: Completed database migration, working on API endpoint now."
```

### Link Related Issues

```bash
gh issue comment <NUMBER> --body "Part of #105"
# Or in issue description:
# Depends on #102
# Blocks #110
```

### Close via PR

```bash
# In PR description, use:
# "Closes #NUMBER"
# Issue automatically closes when PR merges
```

### Close Manually

```bash
gh issue close <NUMBER> --comment "Completed via PR #123"
```

## Daily Workflow Checklist

### Morning: Find Next Work

```bash
# 1. Check mvp-blockers
gh issue list --label "mvp-blocker" --state open

# 2. Check current milestone
gh issue list --milestone "MVP Launch" --state open --label "high-priority"

# 3. Find unstarted tasks
gh issue list --label "task" --state open --search "-label:in-progress"
```

### During Work: Update Status

```bash
# Mark started
gh issue edit <NUMBER> --add-label "in-progress"

# Add updates
gh issue comment <NUMBER> --body "Update: [progress details]"

# Mark blocked if needed
gh issue edit <NUMBER> --add-label "blocked"
gh issue comment <NUMBER> --body "Blocked by: [reason]"
```

### After Completion: Close and Move On

```bash
# Create PR with "Closes #NUMBER"
gh pr create --title "..." --body "Closes #NUMBER\n\n..."

# After merge, issue auto-closes
# Find next work
gh issue list --label "mvp-blocker" --state open
```

## Integration with Orchestrator

The orchestrator uses GitHub Issues for work discovery:

1. **Query** for next priority (mvp-blocker > critical > high-priority)
2. **Read** issue details with `gh issue view <NUMBER>`
3. **Break down** features into tasks if needed
4. **Mark** as in-progress when starting
5. **Update** with progress comments
6. **Close** via PR with "Closes #XXX"

## Creating Milestones

```bash
# Create milestone
gh milestone create "MVP Launch" \
  --description "Core features needed for initial launch" \
  --due-date "2025-03-01"

# List milestones
gh milestone list

# Add issue to milestone
gh issue edit <NUMBER> --milestone "MVP Launch"
```

## Workflow Patterns

### Epic → Features → Tasks

```bash
# 1. Create epic issue
gh issue create --title "Epic: User Management" --label "epic"

# 2. Create milestone for epic
gh milestone create "User Management"

# 3. Create feature issues in milestone
gh issue create --title "Feature: Registration" --label "feature" --milestone "User Management"

# 4. Break down features into tasks
gh issue create --title "Task: Create users table" --label "task,database" --milestone "User Management"
# In body: "Part of #[FEATURE_NUMBER]"
```

## Success Metrics

### Healthy Issue Management

- ✅ All work tracked in GitHub Issues
- ✅ Issues properly labeled
- ✅ Clear priority system
- ✅ In-progress items updated regularly
- ✅ Issues closed via PRs

### Problem Indicators

- ❌ Work done without issues
- ❌ Issues missing labels
- ❌ Unclear priorities
- ❌ Stale in-progress issues
- ❌ Issues manually closed without PR

## Reference Files

For detailed patterns:

- `.claude/agents/agent-github-issues.md` - Complete agent specification
- `.claude/agents/agent-orchestrator.md` - Integration with orchestrator workflow

## Common Commands Quick Reference

```bash
# Create issue
gh issue create --title "..." --body "..." --label "..." --milestone "..."

# List issues
gh issue list --label "..." --state open

# View issue
gh issue view <NUMBER>

# Edit issue
gh issue edit <NUMBER> --add-label "..." --milestone "..."

# Comment on issue
gh issue comment <NUMBER> --body "..."

# Close issue
gh issue close <NUMBER>

# Create milestone
gh milestone create "Name" --due-date "YYYY-MM-DD"

# List milestones
gh milestone list
```

## Success Criteria

Before marking issue work complete:

- [ ] Issue created with proper labels
- [ ] Description includes requirements and acceptance criteria
- [ ] Linked to appropriate milestone
- [ ] Area labels applied (frontend/backend/database)
- [ ] Priority set if applicable
- [ ] Related issues linked
