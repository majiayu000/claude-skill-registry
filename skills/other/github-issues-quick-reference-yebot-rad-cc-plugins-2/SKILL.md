---
description: Quick reference for GitHub Issues management via gh CLI with priority workflow
disable-model-invocation: false
---

# GitHub Issues Quick Reference

## Overview

Manage GitHub Issues using the gh CLI with priority-based workflow. All issue operations should use the gh CLI to ensure consistency and proper metadata management.

**Reference Commands**: Use `/gh-create-issue`, `/gh-close-issue`, `/gh-triage`, `/gh-status-report` for guided workflows.

---

## Priority System

### Three-Tier Priority Labels

- **P1 (Critical)**: Blocks core functionality, security issues, affects all users, data loss
- **P2 (High)**: Significant impact but has workaround, affects some users
- **P3 (Normal)**: Standard workflow items, minor bugs, feature requests

### Setting Up Priority Labels

```bash
gh label create P1 --description "Critical priority - blocks core functionality" --color d73a4a
gh label create P2 --description "High priority - significant impact" --color fbca04
gh label create P3 --description "Normal priority - standard workflow" --color 0e8a16
```

---

## Essential Commands

### Viewing Issues

**IMPORTANT**: Use `--json` format for structured, parseable output:

```bash
gh issue view 59 --json title,body,labels,state,number,author,assignees,createdAt,updatedAt
```

**Recommended JSON fields**:
- `title` - Issue title
- `body` - Full description
- `labels` - All labels (including priority)
- `state` - OPEN or CLOSED
- `number` - Issue number
- `author` - Creator
- `assignees` - Assigned users
- `createdAt` - Creation timestamp
- `updatedAt` - Last modified

**Basic Commands**:

| Action                     | Command                                      |
|----------------------------|----------------------------------------------|
| List all issues            | `gh issue list`                              |
| List open issues           | `gh issue list --state open`                 |
| Filter by priority         | `gh issue list --label P1`                   |
| Filter by assignee         | `gh issue list --assignee @me`               |
| View specific issue        | `gh issue view 42 --json title,body,labels,state,number` |
| Search issues              | `gh issue list --search "keyword"`           |

### Creating Issues

```bash
# Basic issue
gh issue create --title "Issue title" --body "Description"

# With priority and labels
gh issue create \
  --title "Authentication fails" \
  --body "Users cannot log in with SSO" \
  --label "P1,bug" \
  --assignee "@alice"

# Interactive creation
gh issue create
```

### Updating Issues

| Action                     | Command                                      |
|----------------------------|----------------------------------------------|
| Add label                  | `gh issue edit 42 --add-label "P2"`          |
| Remove label               | `gh issue edit 42 --remove-label "P3"`       |
| Change title               | `gh issue edit 42 --title "New title"`       |
| Assign to user             | `gh issue edit 42 --add-assignee "@bob"`     |
| Add to milestone           | `gh issue edit 42 --milestone "v1.0"`        |

### Comments

```bash
# Add comment (ALWAYS include -cc signature)
gh issue comment 42 --body "Update here

-cc"

# Add comment with file
gh issue comment 42 --body-file comment.md
```

**CRITICAL**: Always end comments with `-cc` signature on its own line.

### Closing Issues

```bash
# Close with comment
gh issue close 42 --comment "Fixed in PR #43

Tested locally and in staging

-cc"

# Close without comment (not recommended)
gh issue close 42
```

### Reopening Issues

```bash
gh issue reopen 42 --comment "Issue has resurfaced

-cc"
```

---

## Workflow Examples

### Report a Bug (P1)

```bash
gh issue create \
  --title "Login fails with SSO for all users" \
  --body "## Description
Users cannot authenticate using SSO since deployment.

## Steps to Reproduce
1. Go to login page
2. Click 'Login with SSO'
3. Redirected to error page

## Expected Behavior
User should be authenticated and redirected to dashboard

## Actual Behavior
Error: 'Invalid OAuth state'

## Environment
- Production environment
- All users affected
- Started after deployment at 2pm" \
  --label "P1,bug"
```

### Create Feature Request (P3)

```bash
gh issue create \
  --title "Add dark mode to dashboard" \
  --body "## Feature Description
Support dark mode theme in the user dashboard.

## Problem Statement
Users working at night find the bright interface uncomfortable.

## Proposed Solution
Add theme toggle in user settings.

## Acceptance Criteria
- [ ] User can toggle between light and dark mode
- [ ] Preference is saved per user
- [ ] All dashboard components support dark mode" \
  --label "P3,enhancement"
```

### Close Fixed Issue

```bash
gh issue close 42 --comment "Fixed by implementing new auth flow in PR #43

## Changes Made
- Updated OAuth state validation
- Added session persistence
- Improved error handling

## Testing
- Tested locally with all SSO providers
- Verified in staging environment
- Monitored production for 1 hour post-deployment

No issues detected.

-cc"
```

### Triage and Prioritize

```bash
# List unlabeled issues
gh issue list --state open

# View issue details with structured data
gh issue view 45 --json title,body,labels,state,number,author,assignees

# Assign priority after assessment
gh issue edit 45 --add-label "P2"
```

---

## Priority Assessment Guidelines

### When to Use P1

- System is down or unusable
- Security vulnerabilities discovered
- Data loss or corruption occurring
- All users blocked from core functionality
- Production outage in progress

### When to Use P2

- Significant feature broken but workaround exists
- Performance severely degraded
- Affects substantial subset of users
- Important business functionality impaired

### When to Use P3

- Minor bugs with minimal impact
- UI/UX improvements
- Feature requests
- Technical debt
- Documentation updates
- Refactoring tasks

---

## Comment Signature

**CRITICAL RULE**: Every comment you post MUST end with:

```
-cc
```

This signature must be on its own line at the end of every comment. It identifies comments as being written by Claude Code for transparency and accountability.

Example:
```
Fixed the authentication issue and deployed to production.

-cc
```

---

## Best Practices

### DO

- ✅ Always assign priority labels (P1/P2/P3)
- ✅ Write descriptive, action-oriented titles
- ✅ Include reproduction steps for bugs
- ✅ Add acceptance criteria for features
- ✅ Link related PRs and commits
- ✅ Use the `-cc` signature in all comments
- ✅ Update priority if circumstances change

### DON'T

- ❌ Create issues without priority labels
- ❌ Forget the `-cc` signature in comments
- ❌ Use vague titles like "Fix bug"
- ❌ Close issues without explaining resolution
- ❌ Leave P1 issues unassigned

---

## Guided Workflows

For step-by-step guidance, use these commands:

| Task                        | Command              |
|-----------------------------|----------------------|
| Create issue with guidance  | `/gh-create-issue`   |
| Close issue properly        | `/gh-close-issue`    |
| Triage open issues          | `/gh-triage`         |
| Generate status report      | `/gh-status-report`  |

---

## Common Patterns

### Check Status Before Work

```bash
# See what needs attention
gh issue list --label P1 --state open

# Check your assignments
gh issue list --assignee @me --state open
```

### After Fixing a Bug

```bash
# Close with summary
gh issue close 42 --comment "Fixed in PR #43

Changes: {summary}
Testing: {what was tested}

-cc"
```

### Weekly Review

```bash
# Generate status report
/gh-status-report

# Or manually:
gh issue list --label P1 --state open
gh issue list --label P2 --state open
gh issue list --state closed --limit 10
```

---

## Quick Filters

```bash
# Critical issues
gh issue list --label P1 --state open

# Unassigned issues
gh issue list --state open --json number,title,assignees | jq '.[] | select(.assignees == [])'

# Stale issues (older than 30 days)
gh issue list --state open --json number,title,createdAt

# My issues
gh issue list --assignee @me --state open

# Recent activity
gh issue list --state closed --limit 20
```

---

## Integration with Workflow

### After Code Changes

1. Search for related issues: `gh issue list --search "keyword"`
2. Add update comments with `-cc` signature
3. Close issues when resolved
4. Create follow-up issues if needed

### During Planning

1. Review open issues: `/gh-status-report`
2. Triage new issues: `/gh-triage`
3. Assign priorities and team members
4. Break down large issues into smaller tasks

### In Standups/Reviews

1. Filter by assignee to see progress
2. Check P1 issues for blockers
3. Review recently closed issues
4. Update priorities based on new information

---

## Golden Rules

1. **Always assign priority** (P1/P2/P3) when creating or triaging issues
2. **Always use `-cc` signature** in comments
3. **Be descriptive** in titles and descriptions
4. **Link related items** (PRs, commits, other issues)
5. **Document resolutions** when closing issues
6. **Use guided commands** for complex workflows

---

## Full Documentation

For complete documentation and advanced features:
- Use `/gh-create-issue` for guided issue creation
- Use `/gh-close-issue` for guided issue closure
- Use `/gh-triage` for priority management
- Use `/gh-status-report` for comprehensive reporting
