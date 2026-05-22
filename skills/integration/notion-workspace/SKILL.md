---
name: notion-workspace
description: Notion workspace operations - pages, databases, blocks, and search. Use for managing Notion pages, databases, and content.
allowed-tools: bash, read, webfetch
---

# Notion Workspace Skill

## Overview

This skill provides access to Notion API operations using progressive disclosure for optimal context usage.

**Context Savings**: ~90% reduction

- **Direct API Mode**: Loading all API documentation and examples
- **Skill Mode**: ~300 tokens metadata + on-demand tool loading

## Requirements

- `NOTION_API_KEY` environment variable set (Notion integration token)
- `NOTION_VERSION` optional (default: 2022-06-28)

## Toolsets

The skill provides tools across 5 categories:

| Toolset     | Description                                 |
| ----------- | ------------------------------------------- |
| `pages`     | Page creation, updates, retrieval           |
| `databases` | Database queries, creation, row management  |
| `blocks`    | Block content and hierarchy management      |
| `search`    | Workspace search across pages and databases |
| `users`     | User management and information             |

## Quick Reference

```bash
# Get page content
python executor.py --tool get-page --args '{"page_id": "abc123"}'

# Create page
python executor.py --tool create-page --args '{"parent": {"page_id": "parent123"}, "properties": {"title": [{"text": {"content": "New Page"}}]}}'

# Query database
python executor.py --tool query-database --args '{"database_id": "db123", "filter": {}}'

# Search workspace
python executor.py --tool search --args '{"query": "meeting notes", "filter": {"property": "object", "value": "page"}}'

# List users
python executor.py --tool list-users --args '{}'
```

## Common Tools (Default Toolsets)

### Pages

| Tool           | Description                          | Confirmation Required |
| -------------- | ------------------------------------ | --------------------- |
| `get-page`     | Retrieve page content and properties | No                    |
| `create-page`  | Create a new page                    | Yes                   |
| `update-page`  | Update page properties and content   | Yes                   |
| `archive-page` | Archive or delete a page             | Yes                   |

**get-page**:

```bash
python executor.py --tool get-page --args '{"page_id": "abc123def456"}'
```

**create-page**:

```bash
python executor.py --tool create-page --args '{
  "parent": {"page_id": "parent_page_id"},
  "properties": {
    "title": [{"text": {"content": "Project Plan"}}]
  }
}'
```

**update-page**:

```bash
python executor.py --tool update-page --args '{
  "page_id": "abc123",
  "properties": {
    "Status": {"select": {"name": "In Progress"}}
  }
}'
```

**archive-page**:

```bash
python executor.py --tool archive-page --args '{"page_id": "abc123", "archived": true}'
```

### Databases

| Tool              | Description                           | Confirmation Required |
| ----------------- | ------------------------------------- | --------------------- |
| `list-databases`  | List accessible databases             | No                    |
| `query-database`  | Query database with filters and sorts | No                    |
| `create-database` | Create a new database                 | Yes                   |
| `add-row`         | Add a row to a database               | Yes                   |
| `update-database` | Update database properties            | Yes                   |

**query-database**:

```bash
python executor.py --tool query-database --args '{
  "database_id": "db123",
  "filter": {
    "property": "Status",
    "select": {"equals": "Done"}
  },
  "sorts": [{"property": "Created", "direction": "descending"}]
}'
```

**add-row**:

```bash
python executor.py --tool add-row --args '{
  "database_id": "db123",
  "properties": {
    "Name": {"title": [{"text": {"content": "New Task"}}]},
    "Status": {"select": {"name": "To Do"}},
    "Priority": {"select": {"name": "High"}}
  }
}'
```

**create-database**:

```bash
python executor.py --tool create-database --args '{
  "parent": {"page_id": "parent123"},
  "title": [{"text": {"content": "Project Tracker"}}],
  "properties": {
    "Name": {"title": {}},
    "Status": {"select": {"options": [{"name": "To Do"}, {"name": "Done"}]}},
    "Due": {"date": {}}
  }
}'
```

### Blocks

| Tool            | Description                         | Confirmation Required |
| --------------- | ----------------------------------- | --------------------- |
| `get-block`     | Get block content                   | No                    |
| `get-children`  | Get child blocks of a page or block | No                    |
| `append-blocks` | Append blocks to a page             | Yes                   |
| `update-block`  | Update block content                | Yes                   |
| `delete-block`  | Delete a block                      | Yes                   |

**get-children**:

```bash
python executor.py --tool get-children --args '{"block_id": "page_or_block_id"}'
```

**append-blocks**:

```bash
python executor.py --tool append-blocks --args '{
  "block_id": "page123",
  "children": [
    {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "New paragraph"}}]}},
    {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Section Title"}}]}}
  ]
}'
```

### Search

| Tool     | Description                         | Confirmation Required |
| -------- | ----------------------------------- | --------------------- |
| `search` | Search pages and databases by title | No                    |

**search**:

```bash
python executor.py --tool search --args '{
  "query": "project plan",
  "filter": {"property": "object", "value": "page"},
  "sort": {"direction": "descending", "timestamp": "last_edited_time"}
}'
```

### Users

| Tool         | Description                      | Confirmation Required |
| ------------ | -------------------------------- | --------------------- |
| `list-users` | List all users in the workspace  | No                    |
| `get-user`   | Get user details by ID           | No                    |
| `get-me`     | Get current bot user information | No                    |

**list-users**:

```bash
python executor.py --tool list-users --args '{}'
```

**get-user**:

```bash
python executor.py --tool get-user --args '{"user_id": "user123"}'
```

## Configuration

### Environment Variables

| Variable         | Required | Description                                      |
| ---------------- | -------- | ------------------------------------------------ |
| `NOTION_API_KEY` | Yes      | Notion integration token (starts with `secret_`) |
| `NOTION_VERSION` | No       | API version (default: 2022-06-28)                |

### Getting a Notion API Key

1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Configure integration name and workspace
4. Copy the "Internal Integration Token"
5. Share pages/databases with your integration

### Limiting Toolsets

To reduce context and improve tool selection, enable only needed toolsets:

```bash
# Only pages and search
NOTION_TOOLSETS=pages,search python executor.py --list

# Only databases
NOTION_TOOLSETS=databases python executor.py --list
```

## Agent Integration

**Primary Agents**:

- `pm` - Project management, task tracking
- `technical-writer` - Documentation management

**Secondary Agents**:

- `analyst` - Research, note-taking
- `developer` - Technical documentation
- `orchestrator` - Workflow coordination

## Security

**API Key Protection**:

- Never expose `NOTION_API_KEY` in logs or output
- Store API key securely using environment variables
- Use integration-level permissions to limit access

**Confirmation Required**:

- All page mutations (create, update, archive)
- All database mutations (create, add rows, update)
- All block mutations (append, update, delete)

**Read-Only Mode**:
Set `NOTION_READ_ONLY=1` to disable all mutation operations:

```bash
NOTION_READ_ONLY=1 python executor.py --tool create-page --args '{...}'
# Error: Operation not allowed in read-only mode
```

## Common Patterns

### Project Management

```bash
# Create project database
python executor.py --tool create-database --args '{
  "parent": {"page_id": "workspace_page"},
  "title": [{"text": {"content": "Projects"}}],
  "properties": {
    "Name": {"title": {}},
    "Status": {"select": {"options": [{"name": "Planning"}, {"name": "Active"}, {"name": "Done"}]}},
    "Owner": {"people": {}},
    "Due Date": {"date": {}}
  }
}'

# Add project
python executor.py --tool add-row --args '{
  "database_id": "projects_db",
  "properties": {
    "Name": {"title": [{"text": {"content": "Q1 Launch"}}]},
    "Status": {"select": {"name": "Planning"}},
    "Due Date": {"date": {"start": "2025-03-31"}}
  }
}'

# Query active projects
python executor.py --tool query-database --args '{
  "database_id": "projects_db",
  "filter": {"property": "Status", "select": {"equals": "Active"}}
}'
```

### Documentation

```bash
# Create documentation page
python executor.py --tool create-page --args '{
  "parent": {"page_id": "docs_parent"},
  "properties": {"title": [{"text": {"content": "API Reference"}}]}
}'

# Add content blocks
python executor.py --tool append-blocks --args '{
  "block_id": "api_ref_page",
  "children": [
    {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [{"text": {"content": "API Reference"}}]}},
    {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "This document describes the API endpoints."}}]}},
    {"object": "block", "type": "code", "code": {"language": "javascript", "rich_text": [{"text": {"content": "fetch('/api/users')"}}]}}
  ]
}'
```

### Meeting Notes

```bash
# Create meeting notes page
python executor.py --tool create-page --args '{
  "parent": {"database_id": "meetings_db"},
  "properties": {
    "Name": {"title": [{"text": {"content": "Team Sync - 2025-01-05"}}]},
    "Date": {"date": {"start": "2025-01-05"}},
    "Attendees": {"people": [{"id": "user1"}, {"id": "user2"}]}
  }
}'

# Search for meeting notes
python executor.py --tool search --args '{
  "query": "Team Sync",
  "filter": {"property": "object", "value": "page"}
}'
```

## Error Handling

If tool execution fails:

1. Verify `NOTION_API_KEY` is set and valid
2. Ensure integration has access to the page/database
3. Check API version compatibility (`NOTION_VERSION`)
4. Review executor.py output for specific error details
5. Verify page/database IDs are correct (32-character hex strings without hyphens)

**Common Errors**:

- `object_not_found`: Page/database not shared with integration
- `validation_error`: Invalid request parameters
- `unauthorized`: Invalid API key or insufficient permissions
- `rate_limited`: Too many requests, retry with exponential backoff

## Rate Limits

Notion API has rate limits:

- **Rate limit**: ~3 requests per second
- **Burst limit**: Up to 10 requests in a short burst
- **Best practice**: Add delays between batch operations

```bash
# Batch operation with delay
for page_id in page_ids; do
  python executor.py --tool get-page --args "{\"page_id\": \"$page_id\"}"
  sleep 0.5  # 500ms delay
done
```

## Related

- Official Notion API Documentation: https://developers.notion.com
- Notion API Reference: https://developers.notion.com/reference
- Integration Setup Guide: https://www.notion.so/help/create-integrations-with-the-notion-api
