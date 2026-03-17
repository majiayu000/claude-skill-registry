---
name: todoist-api
description: Manage Todoist tasks, projects, sections, labels, and comments via the REST API v2 using curl and jq. Covers authentication, CRUD operations, filter queries, pagination, completed task history, and natural language due dates. Use when the user wants to read, create, update, or delete Todoist data via the API.
---

# Todoist API Skill

Interact with the Todoist REST API v2 via `curl` and `jq`.

## Authentication

Resolve the API token in order:

1. Environment variable `TODOIST_API_TOKEN`
2. User-provided token in conversation
3. Ask the user (token is at: Todoist Settings → Integrations → Developer)

```bash
[ -n "$TODOIST_API_TOKEN" ] && echo "Token available" || echo "Token not set"
```

All requests use Bearer auth:

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/ENDPOINT"
```

POST requests add Content-Type:

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}' \
  "https://api.todoist.com/rest/v2/ENDPOINT"
```

## Base URL

`https://api.todoist.com/rest/v2/`

## Confirmation Requirement

**Before executing any destructive action (DELETE, close, update, archive), ask the user for confirmation.** A single confirmation covers a logical group of related actions.

Destructive: delete, close/complete, update, archive.
Read-only (GET): no confirmation needed.

## Priority Mapping

⚠️ **The API and UI use inverted priority numbers:**

| UI Label | API `priority` field | Filter syntax |
|----------|---------------------|---------------|
| P1 (urgent, red) | `4` | `p1` |
| P2 (high, orange) | `3` | `p2` |
| P3 (medium, blue) | `2` | `p3` |
| P4 (normal, none) | `1` | `p4` |

When creating/updating tasks, use the **API value** (4 = urgent).
When using filter queries, use the **UI label** (`p1` = urgent).

## Task Links (v2 IDs)

⚠️ **The REST API `url` field uses deprecated numeric IDs.** Todoist deprecated `/app/task/<numeric_id>` URLs (end of 2025). The new format uses alphanumeric v2 IDs.

**New URL format:** `https://app.todoist.com/app/task/<v2_id>`

The REST API v2 does NOT return `v2_id`. Use the Sync API v9 to get it:

### Get v2_id for a single task

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "TASK_ID"}' \
  "https://api.todoist.com/sync/v9/items/get" | jq '.item.v2_id'
```

Works with both numeric IDs and v2_ids as input.

### Get v2_ids for all tasks (bulk)

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sync_token": "*", "resource_types": ["items"]}' \
  "https://api.todoist.com/sync/v9/sync" | jq '[.items[] | {id, v2_id, content}]'
```

### Build a task link

```bash
# After getting v2_id from Sync API:
TASK_ID="9971910530"
V2_ID=$(curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"item_id\": \"$TASK_ID\"}" \
  "https://api.todoist.com/sync/v9/items/get" | jq -r '.item.v2_id')
echo "https://app.todoist.com/app/task/$V2_ID"
```

### Efficient bulk pattern (REST + Sync combo)

When listing multiple tasks, do ONE Sync call for the v2_id map instead of N individual lookups:

```bash
# 1. Get tasks via REST API (for filtering)
TASKS=$(curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=today")

# 2. Build v2_id lookup from Sync API (one call)
V2_MAP=$(curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sync_token": "*", "resource_types": ["items"]}' \
  "https://api.todoist.com/sync/v9/sync" | jq '[.items[] | {(.id): .v2_id}] | add')

# 3. Merge: replace URLs with v2 format
echo "$TASKS" | jq --argjson map "$V2_MAP" '
  [.[] | . + {link: "https://app.todoist.com/app/task/\($map[.id])"}]
'
```

**When presenting task links to the user, always use v2_id URLs.** Never use the `url` field from the REST API directly.

## Task Response Object

The REST API returns tasks with this structure:

```json
{
  "id": "123456789",
  "content": "Task name",
  "description": "Additional details",
  "comment_count": 0,
  "is_completed": false,
  "order": 1,
  "priority": 1,
  "project_id": "987654321",
  "section_id": null,
  "parent_id": null,
  "labels": [],
  "creator_id": "111",
  "created_at": "2024-01-15T10:30:00.000000Z",
  "assignee_id": null,
  "assigner_id": null,
  "url": "https://app.todoist.com/app/task/123456789",
  "duration": null,
  "deadline": null,
  "due": {
    "date": "2024-01-20",
    "string": "every monday",
    "lang": "en",
    "is_recurring": true
  }
}
```

**Note:** The `url` field uses deprecated numeric IDs. See "Task Links (v2 IDs)" above for the correct URL format.

### The `due` object

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | `YYYY-MM-DD` or RFC3339 datetime |
| `string` | string | Human-readable recurrence/date text |
| `lang` | string | Language code |
| `is_recurring` | boolean | Whether the task recurs |

`due` is `null` if no due date is set.

### The `deadline` field

A hard deadline separate from `due`. When both are set, `due` is the soft/scheduled date and `deadline` is the hard cutoff. Can be set via `deadline_date` (YYYY-MM-DD) or `deadline_datetime` (RFC3339) when creating/updating tasks.

## Endpoints Reference

### Tasks

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List active tasks | GET | `/tasks` |
| Get task | GET | `/tasks/{id}` |
| Create task | POST | `/tasks` |
| Update task | POST | `/tasks/{id}` |
| Close task | POST | `/tasks/{id}/close` |
| Reopen task | POST | `/tasks/{id}/reopen` |
| Delete task | DELETE | `/tasks/{id}` |

**Task filters** (query params for GET /tasks):
- `project_id` — filter by project
- `section_id` — filter by section
- `label` — filter by label name
- `filter` — Todoist filter query (e.g. `today`, `overdue`). See `references/filters.md`

**Task creation/update fields:**
- `content` (required for creation) — task text
- `description` — additional details
- `project_id`, `section_id`, `parent_id` — organization
- `priority` — 1 (normal) to 4 (urgent). **See Priority Mapping above**
- `due_string` — natural language ("tomorrow", "every monday")
- `due_date` — YYYY-MM-DD
- `due_datetime` — RFC3339
- `deadline_date` — YYYY-MM-DD hard deadline
- `deadline_datetime` — RFC3339 hard deadline
- `labels` — array of label names
- `assignee_id` — for shared projects
- `duration`, `duration_unit` — estimated time

### Projects

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List projects | GET | `/projects` |
| Get project | GET | `/projects/{id}` |
| Create project | POST | `/projects` |
| Update project | POST | `/projects/{id}` |
| Archive project | POST | `/projects/{id}/archive` |
| Unarchive project | POST | `/projects/{id}/unarchive` |
| Delete project | DELETE | `/projects/{id}` |
| List collaborators | GET | `/projects/{id}/collaborators` |

**Project fields:** `name` (required), `parent_id`, `color` (e.g. "berry_red", "blue"), `is_favorite`, `view_style` ("list" or "board")

### Sections

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List sections | GET | `/sections` |
| Get section | GET | `/sections/{id}` |
| Create section | POST | `/sections` |
| Update section | POST | `/sections/{id}` |
| Delete section | DELETE | `/sections/{id}` |

**Section fields:** `name` (required), `project_id` (required for creation), `order`

### Labels

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List personal labels | GET | `/labels` |
| Get label | GET | `/labels/{id}` |
| Create label | POST | `/labels` |
| Update label | POST | `/labels/{id}` |
| Delete label | DELETE | `/labels/{id}` |

**Label fields:** `name` (required), `color`, `order`, `is_favorite`

### Comments

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List comments | GET | `/comments` |
| Get comment | GET | `/comments/{id}` |
| Create comment | POST | `/comments` |
| Update comment | POST | `/comments/{id}` |
| Delete comment | DELETE | `/comments/{id}` |

**Comment query params:** `task_id` or `project_id` (one required for listing)
**Comment fields:** `content` (required, markdown supported), `task_id` or `project_id` (one required for creation)

## Pagination

**Most REST v2 endpoints (tasks, projects, sections, labels) return flat JSON arrays — no pagination needed.**

Pagination with cursors applies only to specific endpoints like completed tasks (API v1). See `references/completed-tasks.md` for the cursor-based pagination pattern.

## Common Patterns

### Create a task with due date

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Buy milk", "due_string": "tomorrow", "priority": 4}' \
  "https://api.todoist.com/rest/v2/tasks"
```

Note: `priority: 4` = urgent (P1 in UI).

### Get today's tasks

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=today" | jq '.'
```

### Get overdue tasks

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?filter=overdue" | jq '.'
```

### Complete a task

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks/TASK_ID/close"
```

### List all tasks in a project

```bash
curl -s -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks?project_id=PROJECT_ID" | jq '.'
```

## Error Handling

| Code | Meaning |
|------|---------|
| 200 | Success with body |
| 204 | Success, no content |
| 400 | Bad request |
| 401 | Auth failed |
| 403 | Forbidden |
| 404 | Not found |
| 429 | Rate limited (wait + retry) |
| 5xx | Server error (safe to retry) |

```bash
response=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  "https://api.todoist.com/rest/v2/tasks")

http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
  echo "$body" | jq '.'
else
  echo "Error: HTTP $http_code"
  echo "$body"
fi
```

## Idempotency

For safe retries on writes, include `X-Request-Id` (max 36 chars):

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Request-Id: $(uuidgen)" \
  -d '{"content": "New task"}' \
  "https://api.todoist.com/rest/v2/tasks"
```

## Completed Tasks

REST v2 `/tasks` returns only active tasks. For completed task history, see `references/completed-tasks.md`.

## Additional Reference

- `references/completed-tasks.md` — completed task history (API v1 endpoints, cursor pagination)
- `references/filters.md` — Todoist filter query syntax
