---
name: azure-devops
description: Complete Azure DevOps automation - boards, repos, pipelines, artifacts
version: 2.0.0
type: skill
auto_activate_keywords:
  - azure devops
  - work item
  - boards
  - wiql
  - ado
  - ado boards
  - devops work item
  - azure repos
  - pull request
  - azure pipelines
  - azure artifacts
tools_required:
  - .claude/scenarios/az-devops-tools/auth_check.py
  - .claude/scenarios/az-devops-tools/create_work_item.py
  - .claude/scenarios/az-devops-tools/update_work_item.py
  - .claude/scenarios/az-devops-tools/delete_work_item.py
  - .claude/scenarios/az-devops-tools/get_work_item.py
  - .claude/scenarios/az-devops-tools/list_work_items.py
  - .claude/scenarios/az-devops-tools/link_parent.py
  - .claude/scenarios/az-devops-tools/query_wiql.py
  - .claude/scenarios/az-devops-tools/format_html.py
  - .claude/scenarios/az-devops-tools/list_types.py
  - .claude/scenarios/az-devops-tools/list_repos.py
  - .claude/scenarios/az-devops-tools/create_pr.py
references:
  - name: "Azure DevOps CLI Documentation"
    url: "https://learn.microsoft.com/en-us/cli/azure/devops"
  - name: "az boards work-item Commands"
    url: "https://learn.microsoft.com/en-us/cli/azure/boards/work-item"
  - name: "Work Items REST API"
    url: "https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items"
  - name: "WIQL Syntax Reference"
    url: "https://learn.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax"
  - name: "Work Item Fields"
    url: "https://learn.microsoft.com/en-us/azure/devops/boards/work-items/work-item-fields"
  - name: "Link Types Reference"
    url: "https://learn.microsoft.com/en-us/azure/devops/boards/queries/link-type-reference"
supporting_docs:
  - authentication.md
  - work-items.md
  - queries.md
  - html-formatting.md
  - repos.md
  - pipelines.md
  - artifacts.md
  - HOW_TO_CREATE_YOUR_OWN.md
---

# Azure DevOps Skill

Complete Azure DevOps integration covering boards, repositories, pipelines, and artifacts.

**Auto-activates when:** User mentions Azure DevOps, ADO, work items, boards, repos, pipelines, artifacts, or Azure DevOps URLs.

## Purpose

This skill provides comprehensive guidance for Azure DevOps automation through purpose-built Python CLI tools that handle:

### Work Items (Boards)
- Work item creation with HTML-formatted descriptions
- Work item updates (state, assignments, fields)
- Work item deletion with confirmation
- Parent-child relationship linking
- WIQL query execution
- Work item type and field discovery

### Repositories
- Repository listing with details
- Pull request creation with reviewers and work items
- Branch validation
- Clone URL access

### Pipelines
- Pipeline listing and execution
- Build monitoring and logs
- Deployment management

### Artifacts
- Package feed management
- Package publishing and downloading
- Version management

## Quick Start

### 1. Authentication First

**ALWAYS start by checking authentication:**

```bash
python .claude/scenarios/az-devops-tools/auth_check.py --auto-fix
```

This verifies Azure CLI is installed, you're logged in, org/project are configured, and you have access.

See: [@authentication.md]

### 2. Common Operations

#### Create Work Item
```bash
python .claude/scenarios/az-devops-tools/create_work_item.py \
  --type "User Story" \
  --title "Implement feature" \
  --description @story.md
```

#### Query Work Items
```bash
python .claude/scenarios/az-devops-tools/list_work_items.py --query mine
```

#### Create Pull Request
```bash
python .claude/scenarios/az-devops-tools/create_pr.py \
  --source feature/branch \
  --target main \
  --title "Add feature"
```

## Progressive Loading References

For detailed guidance on specific operations, see:

- [@authentication.md] - Authentication methods (PAT, OAuth, environment variables)
- [@work-items.md] - Work item CRUD operations, field updates, state transitions
- [@queries.md] - WIQL query patterns, filtering, sorting
- [@html-formatting.md] - HTML formatting in work item descriptions/comments
- [@repos.md] - Repository operations, pull request workflows
- [@pipelines.md] - Pipeline triggers, build monitoring, deployment
- [@artifacts.md] - Package management, artifact publishing
- [@HOW_TO_CREATE_YOUR_OWN.md] - Template for creating similar integration tools

## Available Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `auth_check.py` | Verify authentication | Before any operations |
| `create_work_item.py` | Create work items | Add User Stories, Tasks, Bugs, etc. |
| `update_work_item.py` | Update work items | Change state, assignee, fields |
| `delete_work_item.py` | Delete work items | Remove work items (with confirmation) |
| `get_work_item.py` | Get work item details | View complete work item info |
| `list_work_items.py` | Query work items | Find, filter, and list work items |
| `link_parent.py` | Link parent-child | Create Epic → Feature → Story hierarchies |
| `query_wiql.py` | Execute WIQL queries | Complex filtering with WIQL |
| `format_html.py` | Convert to HTML | Format rich descriptions |
| `list_types.py` | Discover types/fields | Explore available options |
| `list_repos.py` | List repositories | View all repositories in project |
| `create_pr.py` | Create pull request | Submit code for review |

## Common Patterns

### Pattern 1: Create Work Item with Parent

```bash
# Create parent work item
python .claude/scenarios/az-devops-tools/create_work_item.py \
  --type "Epic" \
  --title "Q1 Planning Initiative" \
  --description @epic_desc.md

# Output: Created work item #12345

# Create child and link to parent
python .claude/scenarios/az-devops-tools/create_work_item.py \
  --type "Feature" \
  --title "Authentication System" \
  --description @feature_desc.md \
  --parent-id 12345

# Output: Created work item #12346 and linked to parent #12345
```

### Pattern 2: Query and Update Work Items

```bash
# Find your active work items
python .claude/scenarios/az-devops-tools/list_work_items.py \
  --query mine \
  --format ids-only

# Update work item state
python .claude/scenarios/az-devops-tools/update_work_item.py \
  --id 12345 \
  --state "Active" \
  --comment "Starting work on this"
```

### Pattern 3: Feature Branch to Pull Request

```bash
# List repositories
python .claude/scenarios/az-devops-tools/list_repos.py

# Create pull request
python .claude/scenarios/az-devops-tools/create_pr.py \
  --source feature/auth \
  --target main \
  --title "Add authentication" \
  --description @pr_desc.md \
  --reviewers "user1@domain.com,user2@domain.com" \
  --work-items "12345,12346"
```

### Pattern 4: Discover Available Types

```bash
# List all work item types in your project
python .claude/scenarios/az-devops-tools/list_types.py

# Show fields for specific type
python .claude/scenarios/az-devops-tools/list_types.py \
  --type "User Story" \
  --fields
```

## Critical Learnings

### HTML Formatting Required

Azure DevOps work item descriptions use HTML, not Markdown or plain text.

**The tools handle this automatically:**

- `create_work_item.py` converts markdown to HTML by default
- Use `--no-html` to disable conversion
- Or use `format_html.py` directly for custom formatting

See: [@html-formatting.md]

### Two-Step Parent Linking

You cannot specify a parent during work item creation via CLI (Azure limitation).

**The tools provide two approaches:**

**Option A:** Use `--parent-id` flag (recommended):

```bash
python .claude/scenarios/az-devops-tools/create_work_item.py \
  --type "Task" \
  --title "My Task" \
  --parent-id 12345
```

**Option B:** Link separately:

```bash
# Step 1: Create
TASK_ID=$(python .claude/scenarios/az-devops-tools/create_work_item.py \
  --type "Task" \
  --title "My Task" \
  --json | jq -r '.id')

# Step 2: Link
python .claude/scenarios/az-devops-tools/link_parent.py \
  --child $TASK_ID \
  --parent 12345
```

### Area Path and Work Item Types

- Area path format: `ProjectName\TeamName\SubArea`
- Work item types vary by project (standard + custom types)
- Use `list_types.py` to discover what's available in your project

## Error Recovery

| Error | Tool to Use | Example |
|-------|-------------|---------|
| Authentication failed | `auth_check.py --auto-fix` | Auto-login and configure |
| Invalid work item type | `list_types.py` | See available types |
| Field validation error | `list_types.py --type "Type" --fields` | See valid fields |
| Parent link failed | Check IDs exist, verify hierarchy rules | Epic → Feature → Story → Task |
| Branch does not exist | Verify with `git branch -a` | Push branch first |

## Tool Implementation

All tools are in `.claude/scenarios/az-devops-tools/`:

- Standalone Python programs (can run independently)
- Importable modules (can use in other scripts)
- Comprehensive error handling
- Tests in `tests/` directory

See: [Tool README](.claude/scenarios/az-devops-tools/README.md)

## Philosophy

These tools follow amplihack principles:

- **Ruthless Simplicity**: Each tool does one thing well
- **Zero-BS**: Every function works, no stubs or TODOs
- **Reusable**: Importable and composable
- **Fail-Fast**: Clear errors with actionable guidance
- **Self-Contained**: Standard library + azure CLI wrapper only

## Quick Reference

```bash
# Setup (first time)
python .claude/scenarios/az-devops-tools/auth_check.py --auto-fix

# Create work item
python .claude/scenarios/az-devops-tools/create_work_item.py \
  --type "User Story" \
  --title "Title" \
  --description @desc.md

# Update work item
python .claude/scenarios/az-devops-tools/update_work_item.py \
  --id 12345 \
  --state "Active"

# Query work items
python .claude/scenarios/az-devops-tools/list_work_items.py --query mine

# Create pull request
python .claude/scenarios/az-devops-tools/create_pr.py \
  --source feature/branch \
  --target main \
  --title "Add feature"

# Discover types
python .claude/scenarios/az-devops-tools/list_types.py
```
