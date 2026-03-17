---
name: gtasks-todo-manager
description: Manages to-do items across multiple Google accounts using the Google Tasks API. Use when the user needs to create, update, complete, or organize tasks in Google Tasks, manage task lists, or view tasks across multiple Google accounts. Supports personal Gmail, Google Workspace, and organization-provisioned accounts with secure OAuth authentication.
---

# gtasks-todo-manager

## Overview

This skill enables Claude Code agents to manage to-do items across multiple Google accounts through the Google Tasks API. It provides comprehensive task management including creating, updating, completing, and organizing tasks, as well as managing task lists and aggregating views across accounts.

The skill uses a BYOC (Bring Your Own Credentials) model where users provide their own Google Cloud OAuth credentials, ensuring security and privacy.

## CLI Location

The CLI is located in the `scripts` subdirectory of this skill's base directory. When this skill is loaded, you receive a "Base directory for this skill" path. The CLI path is:

```
{base_directory}/scripts/cli.js
```

**All CLI commands in this skill's documentation assume you are running them from the scripts directory or using the full path.**

## Before Any Operation

**IMPORTANT**: Before performing any operation with this skill, you MUST complete the following checks in order:

### 1. Verify Authentication

Always verify authentication first:

```bash
node scripts/cli.js auth validate
```

If this command fails, proceed to the **Setup** operation.

### 2. Check for Config Migrations

After authentication succeeds, check if the config needs migration:

```bash
cat ~/.config/gtasks-todo-manager/config.json | jq -r '.schemaVersion // "unversioned"'
```

**Current schema version**: `0.3.2`

If the result is `unversioned` or an older version, proceed to the **Migrations** operation before continuing with the requested operation.

## Operations

| User Intent | Operation Reference |
|-------------|---------------------|
| Migrate config schema after skill update | [Migrations](references/operations/migrations.md) |
| Set up OAuth, add/remove accounts, fix auth issues | [Setup](references/operations/setup.md) |
| Create, update, complete, delete, or move tasks | [Tasks](references/operations/tasks.md) |
| Create, rename, delete, or list task lists | [Task Lists](references/operations/tasklists.md) |
| View tasks across accounts, get summary statistics | [Aggregation](references/operations/aggregate.md) |
| Get prioritized task suggestions for today | [Suggestions](references/operations/suggestions.md) |
| Associate task lists with git projects, manage project associations | [Projects](references/operations/projects.md) |

**IMPORTANT**: You MUST read the appropriate operation reference before executing any operation. Do not improvise instructions.

## Supported Capabilities

| Category | Operations |
|----------|------------|
| **Authentication** | OAuth setup, credential validation, token refresh |
| **Account Management** | Add, remove, list accounts; set default; check status |
| **Task Lists** | List, create, rename, delete task lists |
| **Tasks** | List, create, update, complete, delete, move, reparent tasks |
| **Subtasks** | Create, reparent, view hierarchy, move with subtasks |
| **Cross-Account** | Aggregate views, filter by account, summary statistics |
| **Task Suggestions** | Prioritized task suggestions for daily focus |
| **Projects** | Associate task lists with git repos, cross-workstation sync |

## Reference Documentation

- [Google Tasks API Reference](references/api/google-tasks-api.md) - SDK reference and code examples
- [Config Schema](references/schemas/config.schema.json) - Configuration file structure
- [Task Schema](references/schemas/task.schema.json) - Task and TaskList data structures
