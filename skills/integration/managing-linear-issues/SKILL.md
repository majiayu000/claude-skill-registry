---
name: managing-linear-issues
description: Linear.app issue management using Linearis CLI with JSON output and smart ID resolution. Use when creating, viewing, updating, or searching Linear issues, managing sprints/cycles, or listing teams/projects.
---

# Linear Integration Skill

**Purpose**: Issue management for Linear.app using Linearis CLI with JSON output optimized for LLM agents.

**Tool**: [Linearis CLI](https://github.com/czottmann/linearis) - npm package `linearis`

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Decision Tree](#decision-tree)
3. [Quick Command Reference](#quick-command-reference)
4. [Pattern Recognition - Auto-Invocation](#pattern-recognition---auto-invocation)
5. [Workflow Examples](#workflow-examples)
6. [Error Handling](#error-handling)
7. [Authentication Strategy](#authentication-strategy)
8. [JSON Output Handling](#json-output-handling)

---

## Prerequisites

### Verify Installation

```bash
# Check CLI installed
linearis --version
```

### Authentication (Priority Order)

**IMPORTANT**: Always check for project-specific credentials first. Different projects may use different Linear workspaces.

1. **Project .env** (PREFERRED - project-specific):
   ```bash
   # Check project .env for LINEAR_API_KEY
   grep LINEAR_API_KEY .env

   # Run commands with project token
   export LINEAR_API_TOKEN="$(grep LINEAR_API_KEY .env | cut -d= -f2)"
   linearis teams list
   ```

2. **Environment Variable** (session override):
   ```bash
   export LINEAR_API_TOKEN="lin_api_xxx"
   ```

### Running Commands with Project Credentials

```bash
# Inline token from project .env (recommended)
LINEAR_API_TOKEN=$(grep LINEAR_API_KEY .env | cut -d= -f2) linearis <command>

# Or export for session
export LINEAR_API_TOKEN=$(grep LINEAR_API_KEY .env | cut -d= -f2)
linearis <command>
```

---

## Decision Tree

### Issue Operations

```
User wants to...
├── View issue details
│   └── linearis issues read <ISSUE-ID>
├── Create new issue
│   └── linearis issues create "Title" --team <Team> [options]
├── Update existing issue
│   └── linearis issues update <ISSUE-ID> [--state|--assignee|--priority]
├── Search issues
│   └── linearis issues search "query" [--team|--limit]
├── List recent issues
│   └── linearis issues list [--limit N] [--team Name]
└── Delete issue (soft)
    └── linearis issues update <ISSUE-ID> --trashed
```

### Metadata Operations

```
User wants to...
├── List teams
│   └── linearis teams list
├── List projects
│   └── linearis projects list
├── List cycles/sprints
│   └── linearis cycles list [--team Name] [--active]
├── List labels
│   └── linearis labels list [--team Name]
└── List users
    └── linearis users list [--active]
```

### Comments

```
Add a comment to an issue
└── linearis comments create <ISSUE-ID> --body "Comment text"
```

---

## Quick Command Reference

### Issues CRUD

| Operation | Command | Example |
|-----------|---------|---------|
| **List** | `linearis issues list` | `linearis issues list --limit 10 --team TractionBD` |
| **Search** | `linearis issues search "query"` | `linearis issues search "auth bug"` |
| **Read** | `linearis issues read <ID>` | `linearis issues read TBD-456` |
| **Create** | `linearis issues create "Title"` | `linearis issues create "Fix login" --team TractionBD --priority 1` |
| **Update** | `linearis issues update <ID>` | `linearis issues update TBD-123 --state "In Review"` |

### Create Issue Options

```bash
linearis issues create "Title" \
  --team "TractionBD" \
  --assignee "user-id-or-name" \
  --labels "Bug,Critical" \
  --priority 1 \
  --project "Project Name" \
  --description "Detailed description" \
  --parent-ticket TBD-100
```

**Priority values**: 0 (none), 1 (urgent), 2 (high), 3 (medium), 4 (low)

### Update Issue Options

```bash
linearis issues update TBD-123 \
  --state "In Review" \
  --assignee "new-user" \
  --priority 2 \
  --labels "Bug,P1" \
  --clear-labels \
  --parent-ticket TBD-200 \
  --trashed
```

### Metadata Queries

```bash
# Teams
linearis teams list

# Projects
linearis projects list

# Labels (optionally by team)
linearis labels list --team TractionBD

# Users
linearis users list --active

# Cycles/Sprints
linearis cycles list --team TractionBD --active
linearis cycles list --team TractionBD --around-active 3
```

### Comments

```bash
linearis comments create TBD-123 --body "This is a comment"
```

---

## Pattern Recognition - Auto-Invocation

### High Confidence Triggers (invoke immediately)

```yaml
Issue Operations:
  - "Create a Linear issue for..."
  - "Open a ticket in Linear..."
  - "Log this as a Linear bug..."
  - "Check Linear issue TBD-123"
  - "What's the status of TBD-123?"
  - "Update TBD-123 to..."
  - "Move TBD-123 to In Review"
  - "Assign TBD-123 to..."
  - "Close Linear issue..."
  - "Search Linear for..."
  - "Find issues about..."

Sprint/Cycle Operations:
  - "What's in the current sprint?"
  - "Show active cycle for..."
  - "List team's cycles"

Metadata:
  - "List Linear teams"
  - "Show all projects in Linear"
  - "What labels are available?"
  - "Who can I assign this to?"
```

### Issue ID Detection

```regex
# Linear issue ID pattern
[A-Z]{2,10}-\d+

# Examples: TBD-123, DEV-456, BACKEND-789
```

### Context Signals

```yaml
Strong indicators:
  - .env contains LINEAR_API_KEY
  - Recent messages mention "Linear"
  - Issue IDs in ABC-123 format present
  - User mentions "sprint", "cycle", "backlog"
```

---

## Workflow Examples

### Create Issue from Bug Report

```yaml
User: "Create a Linear issue for the login timeout bug"

Steps:
  1. Parse request: title=login timeout bug
  2. Execute: linearis issues create "Login timeout bug" --team TractionBD --labels "Bug"
  3. Return: Issue ID and details from JSON response
```

### Check Issue Status

```yaml
User: "What's the status of TBD-123?"

Steps:
  1. Parse issue ID: TBD-123
  2. Execute: linearis issues read TBD-123
  3. Return: Issue title, state, assignee, priority from JSON
```

### Update Issue State

```yaml
User: "Move TBD-123 to In Review and assign to John"

Steps:
  1. Get user list: linearis users list --active
  2. Find John's ID from JSON
  3. Update: linearis issues update TBD-123 --state "In Review" --assignee john-id
  4. Confirm: linearis issues read TBD-123
```

### Sprint Planning

```yaml
User: "What issues are in the current sprint?"

Steps:
  1. Get active cycle: linearis cycles list --team TractionBD --active
  2. Parse cycle from JSON
  3. List issues: linearis issues list --team TractionBD --limit 50
  4. Filter by cycle in results
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `command not found: linearis` | CLI not installed | `npm install -g linearis` |
| `No API token found` | Missing authentication | Add `LINEAR_API_KEY` to project `.env`, then export as `LINEAR_API_TOKEN` |
| `Unauthorized` | Invalid/expired token | Token may be for wrong workspace; check project `.env` |
| `Issue not found` | Invalid issue ID or wrong workspace | Verify ID format and that you're using the correct project token |
| `Team not found` | Invalid team name or wrong workspace | Run `linearis teams list` - may need different project token |
| `Rate limited` | Too many requests | Wait 60s, retry with backoff |

### Authentication Troubleshooting

```yaml
Wrong workspace issues:
  Problem: Commands return unexpected teams/issues
  Cause: Using global token instead of project-specific token
  Fix: Check project .env and use that token

  # Verify which workspace you're connected to
  LINEAR_API_TOKEN=$(grep LINEAR_API_KEY .env | cut -d= -f2) linearis teams list
```

### Graceful Fallback

```yaml
If Linearis unavailable:
  1. Log the error for visibility
  2. Provide web URL: https://linear.app/[workspace]/issue/ABC-123
  3. Suggest manual action with instructions
```

---

## Authentication Strategy

```yaml
Priority Order:
  1. Project .env (LINEAR_API_KEY) - project-specific workspaces
  2. LINEAR_API_TOKEN env var - session override

Before Running Commands:
  1. Check if project has .env with LINEAR_API_KEY
  2. Export token for session
  3. If no project .env, prompt user to add LINEAR_API_KEY

Example:
  export LINEAR_API_TOKEN="$(grep LINEAR_API_KEY .env | cut -d= -f2)"
  linearis teams list
```

---

## JSON Output Handling

Linearis outputs JSON. Parse and extract relevant fields:

```bash
# Get issue title
linearis issues read TBD-123 | jq -r '.title'

# Get issue state
linearis issues read TBD-123 | jq -r '.state.name'

# List issue identifiers and titles
linearis issues list --limit 10 | jq -r '.[] | "\(.identifier): \(.title)"'
```

