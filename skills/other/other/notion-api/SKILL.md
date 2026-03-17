---
name: notion-api
description: This skill should be used when the user asks to "search Notion", "find in Notion", "search my Notion workspace", "create Notion page", "make a Notion page", "update Notion page", "edit Notion page", "query Notion database", "get Notion database", "read Notion page", "get page content from Notion", "list Notion pages", or mentions Notion integration, Notion workspace, or Notion API access.
version: 0.1.0
---

# Notion API Integration

Access Notion pages, databases, and content through TypeScript scripts executed via Bun.

## Overview

This skill provides access to the Notion API for:
- **Search**: Find pages and databases across your workspace
- **Pages**: Get, create, and update pages
- **Databases**: Query database entries with filters and sorting
- **Blocks**: Read page content as blocks

All scripts return JSON and require a `NOTION_TOKEN` environment variable.

## Response Format

All scripts output JSON with a consistent structure:

### Success
```json
{"status": "success", "data": {...}}
```

### Authentication Required
```json
{
  "status": "auth_required",
  "message": "Set NOTION_TOKEN environment variable with your integration token...",
  "setupUrl": "https://www.notion.so/my-integrations"
}
```

When you receive `auth_required`, display to the user:
```
To access Notion, you need to set up an integration:
1. Go to: https://www.notion.so/my-integrations
2. Create a new integration for your workspace
3. Copy the "Internal Integration Secret"
4. Set the NOTION_TOKEN environment variable with this token
5. Share your pages/databases with the integration (click "..." menu > "Add connections")

Let me know when you've completed setup.
```

### Error
```json
{"status": "error", "error": "Error description"}
```

## Search

Search for pages and databases across your Notion workspace.

All scripts are located at `${CLAUDE_PLUGIN_ROOT}/skills/notion/scripts/`.

```bash
# Search for pages/databases matching a query
bun run ${CLAUDE_PLUGIN_ROOT}/skills/notion/scripts/search.ts --query "meeting notes"

# Search only pages
bun run search.ts --query "project" --filter page

# Search only databases
bun run search.ts --filter database --top 20

# List all accessible items (no query)
bun run search.ts --top 10
```

## Pages

Get, create, and update Notion pages.

### Get Page

```bash
bun run ${CLAUDE_PLUGIN_ROOT}/skills/notion/scripts/pages.ts get --id <page-id>
```

### Create Page

```bash
# Create as child of another page
bun run pages.ts create --parent-id <page-id> --title "New Page"

# Create as child of another page with icon
bun run pages.ts create --parent-id <page-id> --title "New Page" --icon "📝"

# Create as database entry
bun run pages.ts create --parent-id <database-id> --parent-type database --title "New Entry"

# Create database entry with properties
bun run pages.ts create --parent-id <db-id> --parent-type database --title "Task" \
  --properties '{"Status": {"select": {"name": "To Do"}}, "Priority": {"select": {"name": "High"}}}'
```

### Update Page

```bash
# Update title
bun run pages.ts update --id <page-id> --title "Updated Title"

# Update icon
bun run pages.ts update --id <page-id> --icon "🎉"

# Archive page
bun run pages.ts update --id <page-id> --archived true

# Restore archived page
bun run pages.ts update --id <page-id> --archived false

# Update database page properties
bun run pages.ts update --id <page-id> --properties '{"Status": {"select": {"name": "Done"}}}'
```

## Databases

Query and get information about Notion databases.

### Get Database Schema

```bash
bun run ${CLAUDE_PLUGIN_ROOT}/skills/notion/scripts/databases.ts get --id <database-id>
```

Returns the database title, description, and all property definitions.

### Query Database

```bash
# Query all entries
bun run databases.ts query --id <database-id>

# Query with limit
bun run databases.ts query --id <db-id> --top 20

# Query with filter
bun run databases.ts query --id <db-id> --filter '{"property": "Status", "select": {"equals": "Done"}}'

# Query with multiple conditions (AND)
bun run databases.ts query --id <db-id> --filter '{"and": [
  {"property": "Status", "select": {"equals": "In Progress"}},
  {"property": "Priority", "select": {"equals": "High"}}
]}'

# Query with sorting
bun run databases.ts query --id <db-id> --sorts '[{"property": "Created", "direction": "descending"}]'

# Sort by last edited time
bun run databases.ts query --id <db-id> --sorts '[{"timestamp": "last_edited_time", "direction": "descending"}]'
```

### Common Filter Examples

```bash
# Text contains
--filter '{"property": "Name", "rich_text": {"contains": "project"}}'

# Checkbox is checked
--filter '{"property": "Done", "checkbox": {"equals": true}}'

# Date is after
--filter '{"property": "Due Date", "date": {"after": "2024-01-01"}}'

# Number greater than
--filter '{"property": "Score", "number": {"greater_than": 80}}'

# OR conditions
--filter '{"or": [
  {"property": "Status", "select": {"equals": "Done"}},
  {"property": "Status", "select": {"equals": "Archived"}}
]}'
```

## Blocks (Page Content)

Read page content as blocks.

### List Page Blocks

```bash
# Get blocks from a page
bun run ${CLAUDE_PLUGIN_ROOT}/skills/notion/scripts/blocks.ts list --id <page-id>

# Get blocks with limit
bun run blocks.ts list --id <page-id> --top 100

# Get blocks recursively (includes nested content)
bun run blocks.ts list --id <page-id> --recursive
```

### Get Specific Block

```bash
bun run blocks.ts get --id <block-id>
```

### Block Types

Blocks can be: paragraph, heading_1, heading_2, heading_3, bulleted_list_item, numbered_list_item, to_do, toggle, code, quote, callout, divider, table, image, bookmark, and more.

Each block includes:
- `id`: Block identifier
- `type`: Block type
- `content`: Text content (if applicable)
- `hasChildren`: Whether block has nested blocks
- `children`: Nested blocks (when using --recursive)

## Authentication Setup

1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Give it a name and select the workspace
4. Copy the "Internal Integration Secret"
5. Set the environment variable:
   ```bash
   export NOTION_TOKEN=secret_xxxxx
   ```
6. Share pages/databases with the integration:
   - Open the page or database in Notion
   - Click the "..." menu in the top right
   - Select "Add connections"
   - Find and select your integration

## Important Notes

- **Sharing required**: Pages and databases must be shared with your integration before they can be accessed
- **Rate limits**: Notion API allows ~3 requests per second on average
- **Page IDs**: Can be found in the page URL (the 32-character string after the page name)
- **Database IDs**: Same format as page IDs, found in the database URL

## Script Reference

| Script | Purpose |
|--------|---------|
| `search.ts` | Search pages and databases across workspace |
| `pages.ts` | Get, create, update pages |
| `databases.ts` | Get database schema, query entries |
| `blocks.ts` | Read page content as blocks |

## Additional Resources

For detailed API reference, see:
- **`references/notion-api.md`** - Notion API endpoints and parameters
