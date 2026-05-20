---
name: elnora-search
description: >
  This skill should be used when the user asks to "search tasks", "find a protocol",
  "search files", "search file content", "search inside files", "find tasks about",
  "look up", "query Elnora", "search Elnora", "full text search",
  or any task involving searching the Elnora Platform for tasks or files by keyword.
---

# Elnora Search

Full-text search across tasks and files on the Elnora AI Platform. Search by keyword to find protocols, conversations, and documents across all projects you have access to.

## Organization Context

All search tools accept an optional `org_id` parameter (UUID). When provided,
the search targets that organization instead of the user's active org. The user
must be a member of the target org.

## Concepts

- **Search results** include a `snippet` with HTML-bold highlighted matches and a `rank` score for relevance sorting.
- **Search is read-only.** Use search to find resources, then use domain-specific tools (`elnora_get_task`, `elnora_get_file_content`, etc.) to act on them.
- Results span all projects you have access to. There is no project filter on search -- use `elnora_list_tasks` or `elnora_list_files` with `project_id` to browse within a single project.

## MCP Tools

### elnora_search_all

Full-text search across all resource types (tasks, files, etc.) in a single call.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query (min: 1, max: 1,000 chars) |
| `page` | integer | No | 1 | Page number (min: 1) |
| `page_size` | integer | No | 25 | Results per page (min: 1, max: 100) |

Returns paginated results:

```json
{
  "items": [
    {
      "type": "task",
      "id": "<UUID>",
      "title": "PCR Protocol for BRCA1",
      "snippet": "...amplify <b>BRCA1</b> exon 11 using standard <b>PCR</b>...",
      "projectId": "<UUID>",
      "createdAt": "...",
      "rank": 0.85
    },
    {
      "type": "file",
      "id": "<UUID>",
      "title": "brca1-protocol-v2.md",
      "snippet": "...<b>PCR</b> amplification protocol for...",
      "projectId": "<UUID>",
      "createdAt": "...",
      "rank": 0.72
    }
  ],
  "page": 1,
  "totalCount": 8,
  "hasNextPage": false
}
```

Use the `type` field to distinguish between tasks and files in results.

### elnora_search_tasks

Full-text search scoped to tasks only.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query (min: 1, max: 1,000 chars) |
| `page` | integer | No | 1 | Page number (min: 1) |
| `page_size` | integer | No | 25 | Results per page (min: 1, max: 100) |

Same response shape as `elnora_search_all` but only returns task results. Use this when you know you are looking for a conversation thread.

### elnora_search_files

Full-text search scoped to files only.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query (min: 1, max: 1,000 chars) |
| `page` | integer | No | 1 | Page number (min: 1) |
| `page_size` | integer | No | 25 | Results per page (min: 1, max: 100) |

Same response shape as `elnora_search_all` but only returns file results. Use this when you know you are looking for a document or protocol output.

### elnora_search_file_content

Full-text search inside file bodies (protocols, documents). Unlike `elnora_search_files` which searches metadata, this searches the actual content of files.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query (min: 1, max: 1,000 chars) |
| `page` | integer | No | 1 | Page number (min: 1) |
| `page_size` | integer | No | 25 | Results per page (min: 1, max: 100) |

Same response shape as other search tools. Use this to find specific protocol steps, reagent mentions, or methods within generated protocols.

## Token Efficiency

All search tools support optional `compact` and `fields` parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `compact` | boolean | false | Strip null/empty values (~30-40% token savings) |
| `fields` | string | all | Comma-separated field names (e.g., "id,name,snippet") |

## Choosing the Right Search Tool

| Goal | Tool |
|------|------|
| Find anything matching a keyword | `elnora_search_all` |
| Find a conversation about a topic | `elnora_search_tasks` |
| Find a protocol document by name | `elnora_search_files` |
| Find content INSIDE file bodies | `elnora_search_file_content` |
| Browse all files in a specific project | `elnora_list_files` (not search) |
| Browse all tasks in a specific project | `elnora_list_tasks` (not search) |

## Pagination

Search results use page-based pagination:

```json
{
  "items": [...],
  "page": 1,
  "totalCount": 50,
  "hasNextPage": true
}
```

If `hasNextPage` is true, increment `page` and call again.

## Agent Workflow Recipes

### Find a task by topic, then read the conversation

1. Call `elnora_search_tasks` with a keyword query (e.g., "BRCA1")
2. Pick the best match by `rank`
3. Call `elnora_get_task_messages` with the task's `id` to read the full conversation

### Find a protocol file and read its content

1. Call `elnora_search_files` with a keyword query (e.g., "gel electrophoresis")
2. Pick the best match by `rank`
3. Call `elnora_get_file_content` with the file's `id` to read the protocol

### Search across everything, then route by type

1. Call `elnora_search_all` with a broad query
2. For each result, check the `type` field:
   - `"task"` -- use `elnora_get_task` or `elnora_get_task_messages`
   - `"file"` -- use `elnora_get_file` or `elnora_get_file_content`
