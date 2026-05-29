---
name: managing-jira-issues
description: Jira issue management using the jira CLI with JSON output. Use for creating, viewing, updating, searching issues, fetching complete hierarchies, and managing sprints.
---

# Jira Integration Skill

**Purpose**: Issue management for Jira Cloud using the `jira` CLI with JSON output optimized for LLM agents.

**Tool**: `jira` CLI (installed globally via npm link from `~/utils/atlassian`)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Decision Tree](#decision-tree)
3. [Quick Command Reference](#quick-command-reference)
4. [Pattern Recognition - Auto-Invocation](#pattern-recognition---auto-invocation)
5. [Workflow Examples](#workflow-examples)
6. [Error Handling](#error-handling)
7. [JSON Output Handling](#json-output-handling)
8. [Comparison: Quick Read vs Fetch](#comparison-quick-read-vs-fetch)
9. [Version History](#version-history)

---

## Prerequisites

### Verify Installation

```bash
# Check CLI installed
jira --version  # Expects: 1.0.0
```

### Authentication

**Config location**: `~/utils/atlassian/.env`

```env
ATLASSIAN_CLOUD_ID=your-cloud-id
ATLASSIAN_AUTH_TOKEN=email@domain.com:API_TOKEN
ATLASSIAN_SITE_URL=https://your-site.atlassian.net
```

Get API token from: https://id.atlassian.com/manage-profile/security/api-tokens

---

## Decision Tree

### Issue Operations

```
User wants to...
├── View issue details
│   └── jira issues read <ISSUE-KEY>
├── List recent issues
│   └── jira issues list [--limit N] [--project KEY]
├── Search issues
│   └── jira issues search "query" [--project KEY]
├── Create new issue
│   └── jira issues create "Title" --project KEY [options]
├── Update existing issue
│   └── jira issues update <ISSUE-KEY> [--status|--assignee|--priority]
├── Fetch complete hierarchy
│   └── jira issues fetch <ISSUE-KEY> --output ./spec
└── Get available transitions
    └── jira issues transitions <ISSUE-KEY>
```

### Metadata Operations

```
User wants to...
├── List projects
│   └── jira projects list
└── List users
    └── jira users list [--query NAME]
```

### Comments

```
├── Add comment
│   └── jira comments create <ISSUE-KEY> --body "Comment text"
└── List comments
    └── jira comments list <ISSUE-KEY>
```

---

## Quick Command Reference

### Issues CRUD

| Operation | Command | Example |
|-----------|---------|---------|
| **Read** | `jira issues read <KEY>` | `jira issues read VA-2228` |
| **List** | `jira issues list` | `jira issues list --limit 10 --project VA` |
| **Search** | `jira issues search "query"` | `jira issues search "auth bug"` |
| **Create** | `jira issues create "Title"` | `jira issues create "Fix login" --project VA --type Bug` |
| **Update** | `jira issues update <KEY>` | `jira issues update VA-123 --status "In Review"` |
| **Fetch** | `jira issues fetch <KEY>` | `jira issues fetch VA-123 --output ./spec` |

### Create Issue Options

```bash
jira issues create "Title" \
  --project VA \
  --type Story \
  --description "Detailed description" \
  --assignee "account-id" \
  --priority High \
  --labels "Bug,Critical" \
  --parent VA-100
```

**Issue types**: Epic, Story, Task, Bug, Sub-task
**Priority values**: Highest, High, Medium, Low, Lowest

### Update Issue Options

```bash
jira issues update VA-123 \
  --status "In Review" \
  --assignee "account-id" \
  --priority High \
  --labels "Bug,P1" \
  --summary "New title"
```

### Fetch (Comprehensive Hierarchy)

```bash
# Fetch epic with ALL children + linked Confluence pages
jira issues fetch VA-2522 --output ./spec

# Output structure:
# ./spec/
# ├── jira/
# │   ├── VA-2522.json
# │   ├── VA-2522.md
# │   ├── VA-2228.json  (child)
# │   └── ...
# ├── confluence/
# │   ├── 12345678.json
# │   └── ...
# └── summary.json
```

**When to use `fetch`**:
- Implementing a feature from Jira epic/story
- Need complete requirements with all children
- Building offline reference materials
- Want all linked Confluence pages automatically

### Metadata Queries

```bash
# Projects
jira projects list

# Users
jira users list
jira users list --query "john"
```

### Comments

```bash
# Add comment
jira comments create VA-123 --body "This is a comment"

# List comments
jira comments list VA-123
```

---

## Pattern Recognition - Auto-Invocation

### High Confidence Triggers (invoke immediately)

```yaml
Issue Operations:
  - "Create a Jira issue for..."
  - "Open a ticket in Jira..."
  - "Log this as a Jira bug..."
  - "Check Jira issue VA-123"
  - "What's the status of VA-123?"
  - "Update VA-123 to..."
  - "Move VA-123 to In Review"
  - "Assign VA-123 to..."
  - "Search Jira for..."
  - "Find issues about..."

Fetch Operations (comprehensive):
  - "Fetch VA-2228"
  - "Pull down VA-2522"
  - "Get complete data for VA-2228"
  - "Implement from VA-2228"
  - "Get requirements for VA-2228"

Metadata:
  - "List Jira projects"
  - "Who can I assign this to?"
```

### Issue ID Detection

```regex
# Jira issue ID pattern
[A-Z]{2,10}-\d+

# Examples: VA-123, DEV-456, BACKEND-789
```

---

## Workflow Examples

### Create Issue from Bug Report

```yaml
User: "Create a Jira issue for the login timeout bug"

Steps:
  1. Parse request: title=login timeout bug
  2. Execute: jira issues create "Login timeout bug" --project VA --type Bug
  3. Return: Issue key and details from JSON
```

### Check Issue Status

```yaml
User: "What's the status of VA-123?"

Steps:
  1. Parse issue ID: VA-123
  2. Execute: jira issues read VA-123
  3. Return: Issue title, state, assignee, priority from JSON
```

### Update Issue State

```yaml
User: "Move VA-123 to In Review and assign to John"

Steps:
  1. Get users: jira users list --query john
  2. Find John's account ID from JSON
  3. Update: jira issues update VA-123 --status "In Review" --assignee john-account-id
```

### Implement from Jira Epic

```yaml
User: "Implement VA-2522"

Steps:
  1. Check if reference exists: ls ./spec/jira/VA-2522.json
  2. If not: jira issues fetch VA-2522 --output ./spec
  3. Read requirements from ./spec/jira/*.md
  4. Begin implementation
  5. Update progress: jira issues update VA-2228 --status "In Progress"
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `command not found: jira` | CLI not installed | `cd ~/utils/atlassian && npm link` |
| `Missing ATLASSIAN_AUTH_TOKEN` | No credentials | Configure `~/utils/atlassian/.env` |
| `Authentication failed` | Invalid token | Regenerate API token |
| `Resource not found` | Invalid issue key | Verify issue exists |
| `Status not available` | Invalid transition | Run `jira issues transitions VA-123` to see options |
| `Rate limited` | Too many requests | CLI auto-retries with backoff |

---

## JSON Output Handling

All commands output JSON. Parse with jq:

```bash
# Get issue title
jira issues read VA-123 | jq -r '.summary'

# Get issue status
jira issues read VA-123 | jq -r '.status'

# List issue keys and titles
jira issues list --limit 10 | jq -r '.[] | "\(.key): \(.summary)"'

# Get created issue key
jira issues create "Title" --project VA | jq -r '.key'
```

---

## Comparison: Quick Read vs Fetch

| Need | Use `read` | Use `fetch` |
|------|-----------|-------------|
| Quick status check | **Yes** | No |
| Get single issue | **Yes** | Overkill |
| Get issue + ALL children | No | **Yes** |
| Get linked Confluence | No | **Yes (automatic)** |
| Offline reference | No | **Yes** |
| Implementation context | No | **Yes** |
| Real-time current data | **Yes** | Snapshot |

---

## Version History

- **v1.0** (2025-12-29): CLI-first architecture replacing MCP-based approach
  - Full CRUD operations via `jira` CLI
  - Comprehensive fetch with hierarchy traversal
  - JSON output for LLM parsing
  - Mirrors Linear skill pattern
