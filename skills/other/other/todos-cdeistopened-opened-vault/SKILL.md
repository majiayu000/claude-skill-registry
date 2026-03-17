---
name: todos
description: Manages project todos via REST API. Use when the user asks to create, view, update, or delete todos, list tasks by project, check task status, or filter by due date. Requires the Nomendex app to be running.
version: 2
---

# Todos Management

## Overview

Manages todos via the Nomendex REST API. The API handles all validation, ID generation, timestamps, and ordering automatically.

Todos are displayed in a kanban board UI with columns for each status. Users can drag and drop todos between columns to change their status, or use the API to update status programmatically.

## Todo Status

Each todo has a status field that controls which kanban column it appears in. The available statuses are:

| Status | Description |
|--------|-------------|
| `todo` | Not started - the default status for new todos |
| `in_progress` | Currently being worked on |
| `done` | Completed |
| `later` | Deferred or backlogged for future consideration |

When creating a todo, status defaults to `todo` if not specified. When updating a todo's status, the system automatically assigns a new order position at the end of the target column.

## Port Discovery

The server writes its port to a discoverable location. Extract it with:

```bash
PORT=$(cat ~/Library/Application\ Support/com.firstloop.nomendex/serverport.json | grep -o '"port":[0-9]*' | cut -d: -f2)
```

## API Endpoints

All endpoints use POST with JSON body at `http://localhost:$PORT`:

| Endpoint | Description |
|----------|-------------|
| `/api/todos/create` | Create a new todo |
| `/api/todos/list` | List todos (with optional project filter) |
| `/api/todos/get` | Get a single todo by ID |
| `/api/todos/update` | Update a todo |
| `/api/todos/delete` | Delete a todo |
| `/api/todos/projects` | List all projects |
| `/api/todos/tags` | List all tags |
| `/api/todos/archive` | Archive a todo |
| `/api/todos/unarchive` | Unarchive a todo |
| `/api/todos/archived` | List archived todos |

## Create Todo

```bash
curl -s -X POST "http://localhost:$PORT/api/todos/create" \
  -H "Content-Type: application/json" \
  -d '{"title": "My todo", "project": "work"}'

# With explicit status
curl -s -X POST "http://localhost:$PORT/api/todos/create" \
  -H "Content-Type: application/json" \
  -d '{"title": "My todo", "status": "in_progress", "project": "work"}'
```

## List Todos

```bash
# All active todos
curl -s -X POST "http://localhost:$PORT/api/todos/list" \
  -H "Content-Type: application/json" \
  -d '{}'

# Todos for a specific project
curl -s -X POST "http://localhost:$PORT/api/todos/list" \
  -H "Content-Type: application/json" \
  -d '{"project": "work"}'
```

## Update Todo

```bash
# Update status
curl -s -X POST "http://localhost:$PORT/api/todos/update" \
  -H "Content-Type: application/json" \
  -d '{"todoId": "todo-123", "updates": {"status": "done"}}'

# Update multiple fields
curl -s -X POST "http://localhost:$PORT/api/todos/update" \
  -H "Content-Type: application/json" \
  -d '{"todoId": "todo-123", "updates": {"title": "New title", "status": "in_progress"}}'
```

## How Claude Should Use This Skill

Always start by getting the server port, then use the appropriate endpoint.
