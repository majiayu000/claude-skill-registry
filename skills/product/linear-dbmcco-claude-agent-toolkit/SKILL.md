---
name: linear
description: Use when managing Linear issues, creating tasks from conversations, tracking work items, or querying project status - provides bash scripts to interact with Linear's GraphQL API without writing queries directly (project, gitignored)
---

# Linear Integration

## Overview

Comprehensive Linear API integration through simple bash scripts. All scripts handle GraphQL API calls internally - you just provide arguments. Covers the full API: issues, comments, labels, cycles, projects, attachments, and team management.

**Core principle:** Agents manage Linear without learning GraphQL syntax or API details.

## When to Use

- Creating issues from conversation context
- Documenting implementation progress via comments
- Organizing work with labels and cycles
- Tracking projects and sprint planning
- Linking external resources (PRs, docs, designs)
- Querying team structure and workflow states

## Environment Setup

Required variables (set in `/experiments/skills/.env`):
```bash
LINEAR_API_KEY=lin_api_xxx
LINEAR_TEAM_ID=xxx-xxx-xxx
LINEAR_TEAM_KEY=LFW
LINEAR_ORG_URL=lightforgeworks
```

Scripts automatically source the `.env` file from parent directory.

## Quick Reference

### Issue Management
| Script | Purpose | Key Arguments |
|--------|---------|---------------|
| `linear-create-issue.sh` | Create new issue | `--title`, `--description`, `--priority` |
| `linear-list-issues.sh` | List team issues with pagination | `--state`, `--assignee-id`, `--after` |
| `linear-update-issue.sh` | Update issue | `--issue-id`, `--state-id`, `--title` |
| `linear-search.sh` | Search issues with pagination | `--query`, `--after` |

### Comments (Essential for AI Documentation)
| Script | Purpose | Key Arguments |
|--------|---------|---------------|
| `linear-create-comment.sh` | Add comment to issue | `--issue-id`, `--body` |
| `linear-list-comments.sh` | List issue comments | `--issue-id`, `--limit` |
| `linear-update-comment.sh` | Update comment | `--comment-id`, `--body` |
| `linear-delete-comment.sh` | Delete comment | `--comment-id` |

### Labels (Organization)
| Script | Purpose | Key Arguments |
|--------|---------|---------------|
| `linear-create-label.sh` | Create team label | `--name`, `--description`, `--color` |
| `linear-list-labels.sh` | List team labels | `--limit` |
| `linear-assign-label.sh` | Add label to issue | `--issue-id`, `--label-id` |
| `linear-remove-label.sh` | Remove label from issue | `--issue-id`, `--label-id` |

### Cycles (Sprint Planning)
| Script | Purpose | Key Arguments |
|--------|---------|---------------|
| `linear-create-cycle.sh` | Create sprint cycle | `--starts-at`, `--ends-at`, `--name` |
| `linear-list-cycles.sh` | List team cycles | `--include-completed`, `--limit` |
| `linear-update-cycle.sh` | Update cycle | `--cycle-id`, `--completed-at` |

### Projects
| Script | Purpose | Key Arguments |
|--------|---------|---------------|
| `linear-create-project.sh` | Create project | `--name`, `--description`, `--color` |
| `linear-list-projects.sh` | List team projects | `--limit` |

### Attachments (External Links)
| Script | Purpose | Key Arguments |
|--------|---------|---------------|
| `linear-create-attachment.sh` | Link external resource | `--issue-id`, `--url`, `--title` |
| `linear-list-attachments.sh` | List issue attachments | `--issue-id` |
| `linear-delete-attachment.sh` | Delete attachment | `--attachment-id` |

### ID Discovery (Essential)
| Script | Purpose | Key Arguments |
|--------|---------|---------------|
| `linear-list-states.sh` | Get workflow state IDs | `--limit` |
| `linear-list-users.sh` | Get team member IDs | `--limit` |
| `linear-get-viewer.sh` | Get authenticated user info | None |

## Common Workflows

### Create Issue from Conversation
```bash
# Create issue with conversation context
scripts/linear-create-issue.sh \
  --title "Implement user authentication" \
  --description "Based on discussion: Need OAuth2 integration with Google and GitHub providers" \
  --priority 2
```

### Document Implementation Progress
```bash
# Add progress comment to issue
scripts/linear-create-comment.sh \
  --issue-id "abc-123" \
  --body "Implemented OAuth2 flow. Tests passing. Ready for review."

# Link PR as attachment
scripts/linear-create-attachment.sh \
  --issue-id "abc-123" \
  --url "https://github.com/org/repo/pull/456" \
  --title "PR: OAuth2 Implementation"
```

### Organize Work
```bash
# Get label IDs
scripts/linear-list-labels.sh

# Assign labels to categorize
scripts/linear-assign-label.sh \
  --issue-id "abc-123" \
  --label-id "label-backend"

scripts/linear-assign-label.sh \
  --issue-id "abc-123" \
  --label-id "label-security"
```

### Update Issue State
```bash
# First get state IDs
scripts/linear-list-states.sh

# Then update to "In Progress"
scripts/linear-update-issue.sh \
  --issue-id "abc-123" \
  --state-id "state-in-progress-id"
```

### Sprint Planning
```bash
# Create cycle
scripts/linear-create-cycle.sh \
  --name "Sprint 42" \
  --starts-at "2025-11-01" \
  --ends-at "2025-11-14" \
  --description "Q4 authentication features"

# Assign issue to cycle
scripts/linear-update-issue.sh \
  --issue-id "abc-123" \
  --cycle-id "cycle-id-from-above"
```

### Pagination for Large Teams
```bash
# Get first page
RESULT=$(scripts/linear-list-issues.sh --state "Backlog" --limit 50)

# Check if more pages
HAS_NEXT=$(echo "$RESULT" | jq -r '.pageInfo.hasNextPage')

if [ "$HAS_NEXT" = "true" ]; then
  CURSOR=$(echo "$RESULT" | jq -r '.pageInfo.endCursor')

  # Get next page
  scripts/linear-list-issues.sh --state "Backlog" --limit 50 --after "$CURSOR"
fi
```

## Output Format

All scripts return JSON with relevant data:

**Create/Update Operations:**
```json
{
  "success": true,
  "id": "entity-id",
  "identifier": "LFW-123",
  "title": "Entity title",
  "url": "https://linear.app/..."
}
```

**List Operations with Pagination:**
```json
{
  "issues": [...],
  "pageInfo": {
    "hasNextPage": true,
    "endCursor": "cursor-string-for-next-page"
  }
}
```

## Common Patterns

### AI Agent Workflow
1. **Create issue** from user conversation
2. **Add comment** documenting implementation approach
3. **Update state** to "In Progress"
4. **Add attachment** linking to PR/branch
5. **Add comment** with completion notes
6. **Update state** to "Done"

### ID Discovery Pattern
```bash
# Always get IDs first before operations
STATES=$(scripts/linear-list-states.sh)
IN_PROGRESS_ID=$(echo "$STATES" | jq -r '.[] | select(.name=="In Progress") | .id')

USERS=$(scripts/linear-list-users.sh)
MY_ID=$(echo "$USERS" | jq -r '.[] | select(.email=="me@example.com") | .id')

# Then use in operations
scripts/linear-update-issue.sh \
  --issue-id "abc-123" \
  --state-id "$IN_PROGRESS_ID" \
  --assignee-id "$MY_ID"
```

## Common Mistakes

**Missing environment variables**
- Scripts check for `LINEAR_API_KEY` and `LINEAR_TEAM_ID`
- Error message shows which variables are missing

**Using Linear CLI syntax**
- ❌ Don't: `linear issue create "Title"`
- ✅ Do: `linear-create-issue.sh --title "Title"`

**Forgetting to get IDs first**
- State IDs, project IDs, user IDs, label IDs must be fetched
- Use list scripts to discover IDs before operations

**Not handling pagination**
- Teams with 100+ issues need pagination
- Always check `pageInfo.hasNextPage` in list operations
- Use `--after` parameter with `endCursor` for next page

**Not documenting work**
- Comments are essential for AI agents to track progress
- Always add comments when making significant changes
- Link related resources (PRs, docs) via attachments

## Anti-Patterns

**Creating issues without context**
```bash
# ❌ Bad: Minimal context
scripts/linear-create-issue.sh --title "Fix bug"

# ✅ Good: Rich context from conversation
scripts/linear-create-issue.sh \
  --title "Fix authentication timeout on mobile Safari" \
  --description "Users report auth timeout after 30s on iOS Safari. Need to increase token TTL and add retry logic." \
  --priority 1
```

**Silent updates**
```bash
# ❌ Bad: Update state without documentation
scripts/linear-update-issue.sh --issue-id "abc-123" --state-id "done"

# ✅ Good: Document completion
scripts/linear-create-comment.sh \
  --issue-id "abc-123" \
  --body "Implemented fix. Increased token TTL to 120s and added exponential backoff. All tests passing."

scripts/linear-update-issue.sh --issue-id "abc-123" --state-id "done"
```

**Ignoring pagination**
```bash
# ❌ Bad: Only get first 50 issues
scripts/linear-list-issues.sh --limit 50

# ✅ Good: Handle all pages
while true; do
  RESULT=$(scripts/linear-list-issues.sh --limit 50 ${CURSOR:+--after "$CURSOR"})
  echo "$RESULT" | jq -r '.issues[]'

  HAS_NEXT=$(echo "$RESULT" | jq -r '.pageInfo.hasNextPage')
  [ "$HAS_NEXT" = "false" ] && break

  CURSOR=$(echo "$RESULT" | jq -r '.pageInfo.endCursor')
done
```

## Script Location

All scripts in: `/Users/braydon/projects/experiments/skills/linear/scripts/`

Can be called from any directory - they auto-source the parent `.env` file.

## API Coverage

This skill covers the full Linear GraphQL API:
- ✅ Issues (CRUD, search, filtering)
- ✅ Comments (CRUD)
- ✅ Labels (CRUD, assignment)
- ✅ Cycles (CRUD, sprint management)
- ✅ Projects (CRUD)
- ✅ Attachments (CRUD, external linking)
- ✅ Workflow States (query)
- ✅ Team Members (query)
- ✅ Authenticated User (query)
- ✅ Pagination (cursor-based)
