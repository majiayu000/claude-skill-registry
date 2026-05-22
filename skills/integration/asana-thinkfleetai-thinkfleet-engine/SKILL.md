---
name: asana
description: "Manage Asana workspaces, projects, tasks, and comments via the REST API."
metadata: {"thinkfleetbot":{"emoji":"📌","requires":{"bins":["curl","jq"],"env":["ASANA_ACCESS_TOKEN"]}}}
---

# Asana

Manage Asana projects and tasks via the REST API.

## Environment Variables

- `ASANA_ACCESS_TOKEN` - Personal access token (generate at https://app.asana.com/0/developer-console)

## List workspaces

```bash
curl -s -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  "https://app.asana.com/api/1.0/workspaces" | jq '.data[] | {gid, name}'
```

## List projects

```bash
curl -s -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  "https://app.asana.com/api/1.0/projects?workspace=WORKSPACE_GID" | jq '.data[] | {gid, name}'
```

## List tasks

```bash
curl -s -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  "https://app.asana.com/api/1.0/tasks?project=PROJECT_GID&opt_fields=name,completed,assignee.name,due_on" | jq '.data[] | {gid, name, completed, assignee: .assignee.name, due_on}'
```

## Create task

```bash
curl -s -X POST -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://app.asana.com/api/1.0/tasks" \
  -d '{"data":{"workspace":"WORKSPACE_GID","projects":["PROJECT_GID"],"name":"New task title","notes":"Task description","assignee":"USER_GID","due_on":"2025-12-31"}}' | jq '.data | {gid, name, permalink_url}'
```

## Update task

```bash
curl -s -X PUT -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://app.asana.com/api/1.0/tasks/TASK_GID" \
  -d '{"data":{"completed":true,"name":"Updated task title"}}' | jq '.data | {gid, name, completed}'
```

## Get task

```bash
curl -s -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  "https://app.asana.com/api/1.0/tasks/TASK_GID?opt_fields=name,notes,completed,assignee.name,due_on,projects.name" | jq '.data | {gid, name, notes, completed, assignee: .assignee.name, due_on}'
```

## Add comment

```bash
curl -s -X POST -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://app.asana.com/api/1.0/tasks/TASK_GID/stories" \
  -d '{"data":{"text":"This is a comment on the task."}}' | jq '.data | {gid, text, created_at}'
```

## List sections

```bash
curl -s -H "Authorization: Bearer $ASANA_ACCESS_TOKEN" \
  "https://app.asana.com/api/1.0/projects/PROJECT_GID/sections" | jq '.data[] | {gid, name}'
```
