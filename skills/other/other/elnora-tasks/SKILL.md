---
name: elnora-tasks
description: >
  This skill should be used when the user asks to "create a task", "send a message",
  "generate a protocol", "list tasks", "read task messages", "update task status",
  "archive a task", "talk to Elnora", "ask Elnora to generate", "protocol conversation",
  or any task involving Elnora Platform task management and protocol generation.
---

# Elnora Tasks

Tasks are conversation threads with the Elnora AI Platform. Each task is a chat where you send messages and receive AI-generated protocol responses. Use tasks to generate, iterate on, and refine bioprotocols.

## Organization Context

All list and create tools accept an optional `org_id` parameter (UUID). When
provided, the operation targets that organization instead of the user's active
org. The user must be a member of the target org.

## Concepts

- **Task**: A conversation thread tied to a project. Has a title, status, and message history.
- **Message**: A single turn in the conversation. Each has a `role` (user or assistant), `sequence` number, optional `attachments`, and `content`.
- **Protocol generation**: Create a task, send a message describing what you need, and the assistant responds with a generated protocol. Iterate by sending follow-up messages.
- **All IDs are UUIDs** (e.g., `bfdc6fbd-40ed-4042-9ea7-c79a5ec90085`).

## MCP Tools

### elnora_list_tasks

List tasks, optionally filtered by project or status.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `project_id` | uuid | No | - | Filter by project UUID |
| `status` | string | No | - | Filter by status (e.g., "active", "completed") |
| `page` | integer | No | 1 | Page number (min: 1) |
| `page_size` | integer | No | 25 | Results per page (min: 1, max: 100) |

Returns paginated results:

```json
{
  "items": [
    {
      "id": "<UUID>",
      "projectId": "<UUID>",
      "title": "...",
      "status": "active",
      "messageCount": 4,
      "lastMessageAt": "...",
      "createdAt": "..."
    }
  ],
  "page": 1,
  "pageSize": 25,
  "totalCount": 12,
  "totalPages": 1,
  "hasNextPage": false
}
```

### elnora_get_task

Get full details for a single task.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | uuid | Yes | Task UUID |

Returns task detail including metadata, status, and associated project. Use this to inspect a task before reading its messages.

### elnora_create_task

Create a new task (conversation thread).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | uuid | No | Project UUID to create the task in |
| `title` | string | No | Task title (max 200 chars; auto-generated if omitted) |
| `initial_message` | string | No | Initial message to start the conversation (max 50,000 chars) |
| `context_file_ids` | uuid[] | No | File UUIDs to attach as context |

Returns the created task object with its `id`. Use this ID for all subsequent operations (send messages, get messages, update, archive).

To start protocol generation immediately, provide `initial_message`. To create an empty task for later use, omit it.

### elnora_send_message

Send a message to a task and receive the AI response. **May take 30-120 seconds** for complex protocol generation requests.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | uuid | Yes | Task UUID |
| `message` | string | Yes | Message content, markdown supported (min: 1, max: 50,000 chars) |
| `file_ids` | uuid[] | No | File UUIDs to attach as context |

Returns the AI response. Use `file_ids` to reference uploaded files (templates, datasets) that should inform the protocol generation.

### elnora_get_task_messages

Get message history for a task. Uses cursor-based pagination.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `task_id` | uuid | Yes | - | Task UUID |
| `limit` | integer | No | 50 | Max messages to return (min: 1, max: 100) |
| `cursor` | string | No | - | Cursor from previous response for pagination |

Returns:

```json
{
  "items": [
    {
      "id": "<UUID>",
      "role": "user",
      "content": "Generate a PCR protocol for BRCA1 exon 11",
      "sequence": 1,
      "createdAt": "...",
      "attachments": []
    },
    {
      "id": "<UUID>",
      "role": "assistant",
      "content": "# PCR Protocol for BRCA1 Exon 11\n...",
      "metadata": "{\"status\":\"completed\"}",
      "sequence": 2,
      "createdAt": "...",
      "attachments": []
    }
  ],
  "nextCursor": null,
  "hasMore": false
}
```

Messages are ordered by `sequence`. If `hasMore` is true, pass `nextCursor` as `cursor` in the next call.

### elnora_update_task

Update a task's title or status.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | uuid | Yes | Task UUID |
| `title` | string | No | New title (max 200 chars) |
| `status` | string | No | New status |

Must provide at least one of `title` or `status`.

### elnora_archive_task

Archive (permanently delete) a task. **This is destructive and cannot be undone.** Always confirm with the user before calling.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | uuid | Yes | Task UUID |

## Agent Workflow Recipes

### Generate a protocol (full flow)

1. Find or create a project:
   - Call `elnora_list_projects` to get a project ID
   - Or call `elnora_create_project` if needed
2. Create a task with an initial prompt:
   - Call `elnora_create_task` with `project_id`, `title`, and `initial_message`
   - Save the returned task `id`
3. Read the AI response:
   - Call `elnora_get_task_messages` with the task ID
   - Look for the message with `role: "assistant"`
4. Iterate on the output:
   - Call `elnora_send_message` with refinement instructions
   - Read updated messages to see the new response

### Quick protocol generation (shortcut)

For simple one-shot generation, use `elnora_generate_protocol` instead:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `description` | string | Yes | Protocol description (min: 10, max: 5,000 chars) |
| `title` | string | No | Task title (max 200 chars) |

This creates a task, sends the description, waits for the response, and returns the result in one call. Takes 30-120 seconds. Use the full flow above when you need to iterate.

### Check the latest assistant response

1. Call `elnora_get_task_messages` with `limit: 2`
2. Find the message where `role` is `"assistant"` -- this is the most recent AI output

### Iterate on a protocol with file context

1. Get the file ID from `elnora_list_files` or `elnora_search_files`
2. Call `elnora_send_message` with the task ID, your refinement message, and `file_ids` containing the reference file
3. The AI will use the file content to inform its response

### Pagination for long conversations

1. Call `elnora_get_task_messages` with `limit: 50`
2. If `hasMore` is `true`, call again with `cursor` set to `nextCursor`
3. Repeat until `hasMore` is `false`
