---
name: monday-com
description: "Monday.com workspace management via official MCP server. This skill should be used when creating, updating, moving, archiving, or deleting items/boards/groups on Monday.com, managing columns, adding comments, or querying workspace data. Supports both hosted and local MCP deployment with interactive setup guidance."
---

# Monday.com Workspace Manager

Manage Monday.com workspaces through the official MCP server — create items, update statuses, move tasks between groups, archive/delete items, manage boards & columns, and add comments.

## When to Use

Invoke when:
- Creating, updating, or deleting items/tasks on Monday.com
- Managing boards, groups, or columns
- Moving items between groups or boards
- Adding comments/updates to items
- Querying board structure, items, or users
- Setting up Monday.com MCP integration
- Any Monday.com workspace automation

## Prerequisites & Setup

### First-Time Setup Flow

On first use, check if Monday.com MCP is configured. If not, guide the user through setup using AskUserQuestion:

```
Question: "How would you like to connect to Monday.com?"
Options:
  - "Hosted MCP (Recommended)" — No local install, auto-updates, OAuth auth
  - "Local MCP via npx" — Requires Node.js 20+, API token
  - "Direct API (curl/scripts)" — Manual GraphQL calls, no MCP dependency
```

### Option A: Hosted MCP (Recommended)

Add to Claude Code MCP settings (`~/.claude/settings.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "monday-mcp": {
      "url": "https://mcp.monday.com/mcp"
    }
  }
}
```

OAuth handles auth automatically — no API token needed.

### Option B: Local MCP via npx

1. **Get API Token**: Monday.com → Avatar → Developers → My access tokens
2. **Configure MCP** in Claude Code settings:

```json
{
  "mcpServers": {
    "monday-api-mcp": {
      "command": "npx",
      "args": ["@mondaydotcomorg/monday-api-mcp@latest"],
      "env": {
        "MONDAY_TOKEN": "<your_token>"
      }
    }
  }
}
```

**Useful flags:**

| Flag | Values | Purpose |
|------|--------|---------|
| `--read-only` / `-ro` | `true` | Read-only mode |
| `--enable-dynamic-api-tools` / `-edat` | `true` / `only` | Full GraphQL access (beta) |
| `--version` / `-v` | `2025-07` | API version |

### Option C: Direct API (No MCP)

For environments w/o MCP support. Set `MONDAY_API_TOKEN` in `.env` or `.env.local` at project root:

```
MONDAY_API_TOKEN=your_token_here
```

The script auto-loads from `.env.local` (priority) or `.env`. Alternatively, export the env var directly.

Use `scripts/monday_api.sh` for direct GraphQL calls.

## Tool Selection: MCP vs API Script

On every Monday.com request, determine which tool to use:

```
1. Check: Are Monday.com MCP tools available? (ToolSearch "monday")
   → YES: Use MCP tools — go to decision table below
   → NO:  Go to step 2

2. Check: Does .env or .env.local have MONDAY_API_TOKEN?
   → YES: Use scripts/monday_api.sh with GraphQL queries
   → NO:  Ask user to set up (AskUserQuestion with setup options above)
```

### MCP vs API Decision Table

| Operation | Best Tool | Why |
|-----------|-----------|-----|
| **Single item CRUD** (create, update, delete) | MCP | One tool call, handles auth, structured params |
| **Get board schema/info** | MCP (`get_board_info`) | Returns columns, groups, filtering guidelines in one call |
| **Get items w/ filters** | MCP (`get_board_items_page`) | Built-in filtering, ordering, pagination, `includeColumns` toggle |
| **Search items by text** | MCP (`get_board_items_page` w/ `searchTerm`) | Fuzzy search built-in |
| **Assign owner** | MCP (`change_item_column_values`) | Single call w/ `personsAndTeams` JSON |
| **List users/teams** | MCP (`list_users_and_teams`) | Supports `getMe`, name search, team members |
| **Create board/group/column** | MCP | Type-safe params, enum validation |
| **Get column type info** | MCP (`get_column_type_info`) | Returns JSON schema for column settings |
| **Board activity logs** | MCP (`get_board_activity`) | Date range filtering built-in |
| **Move board/folder** | MCP (`move_object`) | Handles positioning |
| **Workspace management** | MCP | Create, update, list workspaces |
| **Forms** | MCP | Create and get forms |
| **Multi-board dashboard** | API script | MCP queries one board at a time; script queries all boards in one GraphQL call |
| **Batch updates (5+ items)** | API script | One GraphQL mutation w/ aliases vs 5+ separate MCP calls |
| **Batch deletes** | API script | Same — aliases batch multiple deletes into one call |
| **Webhooks** | API script | MCP has no webhook tools |
| **Archive item/board** | API script | MCP has no archive mutation |
| **Duplicate item** | MCP (`create_item` w/ `duplicateFromItemId`) | Built-in duplicate support |
| **Subitems** | MCP (`create_item` w/ `parentItemId`) | Native subitem creation |

### Performance Rules

1. **Single operations** → always MCP (faster, no shell overhead, structured errors)
2. **Bulk operations (5+ items)** → API script w/ aliases (1 HTTP call vs N MCP calls)
3. **Cross-board reads** → API script (query multiple boards in one request)
4. **Filtered reads** → MCP (built-in filter operators: `any_of`, `between`, `contains_text`, `greater_than`, etc.)
5. **MCP unavailable** → API script for everything

## Safety Classification

| Tier | Operations | Behavior |
|------|-----------|----------|
| **Safe** | List boards, get items, get schema, list users | Execute immediately |
| **Write** | Create item, update columns, add comment, create group/column | Inform user → execute |
| **Destructive** | Delete item, delete column, archive board | AskUserQuestion → confirm → execute |

### Decision Flow

```
Request received
  → Classify tier (see table above)
  → Safe?        Execute immediately, show results
  → Write?       Show what will change → execute
  → Destructive? AskUserQuestion w/ confirm/cancel → execute or abort
```

### Destructive Operation Confirmation

For delete/archive operations, always confirm:

```
Question: "Delete item 'Task Name' (ID: 123456) from board 'Project Board'?"
Options:
  - "Delete permanently" — Item cannot be recovered
  - "Cancel" — Keep item unchanged
```

## Available MCP Tools

### Item Operations

| Tool | Tier | Description |
|------|------|-------------|
| `create_item` | Write | Create item w/ column values |
| `change_item_column_values` | Write | Update item columns |
| `move_item_to_group` | Write | Move item between groups |
| `delete_item` | Destructive | Permanently delete item |
| `get_board_items_by_name` | Safe | Search items by name |
| `create_update` | Write | Add comment to item |

### Board Operations

| Tool | Tier | Description |
|------|------|-------------|
| `create_board` | Write | Create new board |
| `get_board_schema` | Safe | Get columns, groups, structure |
| `create_group` | Write | Add group to board |
| `create_column` | Write | Add column to board |
| `delete_column` | Destructive | Remove column from board |

### Account Operations

| Tool | Tier | Description |
|------|------|-------------|
| `list_users_and_teams` | Safe | Get workspace users & teams |

### Dynamic API Tools (Beta)

Enable w/ `--enable-dynamic-api-tools true` for full GraphQL access:

| Tool | Description |
|------|-------------|
| `all_monday_api` | Execute any GraphQL query/mutation |
| `get_graphql_schema` | Explore API schema |
| `get_type_details` | View type information |

## Common Workflows

### CRITICAL: Always Discover Board Schema First

Column IDs are **unique per board** (e.g. `status` vs `project_status`, `person` vs `project_owner`). Never assume column IDs — always query the board schema first.

```
Step 0 (always): Get board schema to discover column IDs, group IDs, and user IDs
  → query: { boards(ids: [BOARD_ID]) { columns { id title type } groups { id title } } }
  → query: { users { id name email } }
```

### Create Item w/ Owner & Status

```
1. Get board schema → find column IDs for people, status, date, etc.
2. Get user ID → query { users { id name } } or { me { id } }
3. Create item using discovered column IDs:
```

```graphql
mutation {
  create_item(
    board_id: BOARD_ID,
    group_id: "GROUP_ID",
    item_name: "Task name",
    column_values: "{\"PEOPLE_COL_ID\": {\"personsAndTeams\": [{\"id\": USER_ID, \"kind\": \"person\"}]}, \"STATUS_COL_ID\": \"Working on it\"}"
  ) { id name }
}
```

### Assign Owner to Existing Items

```
1. Get board schema → find the people column ID (type: "people")
2. Get user ID → { users { id name } }
3. Update:
```

```graphql
mutation {
  change_multiple_column_values(
    board_id: BOARD_ID,
    item_id: ITEM_ID,
    column_values: "{\"PEOPLE_COL_ID\": {\"personsAndTeams\": [{\"id\": USER_ID, \"kind\": \"person\"}]}}"
  ) { id }
}
```

### Update Item Status

```
1. Get board schema → find the status column ID (type: "status")
2. Find item → get_board_items_by_name or query items
3. Update:
```

```graphql
mutation {
  change_simple_column_value(
    board_id: BOARD_ID,
    item_id: ITEM_ID,
    column_id: "STATUS_COL_ID",
    value: "Done"
  ) { id }
}
```

### Move Item to Different Group

```
1. get_board_schema → get target group ID
2. move_item_to_group → item_id, group_id
```

### Batch Operations (Multiple Items)

Use GraphQL aliases to batch mutations in a single request:

```graphql
mutation {
  t1: change_multiple_column_values(board_id: BID, item_id: ID1, column_values: "...") { id }
  t2: change_multiple_column_values(board_id: BID, item_id: ID2, column_values: "...") { id }
  t3: change_multiple_column_values(board_id: BID, item_id: ID3, column_values: "...") { id }
}
```

Rate limit: 10,000,000 complexity points/min per account.

## Column Value Formats

Column IDs vary per board. Always query schema first to find the correct ID.

| Column Type | API Type | Format | Example |
|-------------|----------|--------|---------|
| Status | `status` | String label | `"Done"` |
| Text | `text` | Plain string | `"Hello"` |
| Number | `numeric` | Numeric string | `"42"` |
| Date | `date` | YYYY-MM-DD | `"2026-02-07"` |
| People | `people` | JSON w/ personsAndTeams | `{"personsAndTeams": [{"id": 12345, "kind": "person"}]}` |
| Dropdown | `dropdown` | JSON w/ IDs | `{"ids": [3, 5]}` |
| Email | `email` | JSON w/ email+text | `{"email": "a@b.com", "text": "Name"}` |
| Phone | `phone` | JSON w/ phone+country | `{"phone": "+1234567890", "countryShortName": "US"}` |
| Timeline | `timeline` | JSON w/ from+to | `{"from": "2026-01-01", "to": "2026-01-31"}` |
| Link | `link` | JSON w/ url+text | `{"url": "https://...", "text": "Link"}` |

For complete column type reference, see `references/column-types.md`.

## Advanced Workflows

### Workspace Dashboard

To build a dashboard, fetch all boards w/ items in a single query, then parse:
1. Query all boards w/ `items_page` and `column_values`
2. Filter out "Subitems of *" boards (auto-generated)
3. Group items by board, status, and owner
4. Present as markdown tables w/ summary stats

### Understanding Fields

Column IDs are unique per board and must be discovered via schema query. Key patterns:
- **Status** and **Priority** share the same `status` type — distinguish by `title`
- **People** column holds user assignments — always use `personsAndTeams` JSON format
- **`text` field** on `column_values` = human-readable value; `value` field = raw JSON
- Status labels (Done, Working on it, Stuck) come from `settings_str` in column schema

### Cross-Board Operations

When moving items between boards, column IDs differ. Use `columns_mapping` in `move_item_to_board` to map source → target column IDs.

For complete examples, see `references/advanced-workflows.md`.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Not Authenticated` | Invalid/expired token | Regenerate token: Avatar → Developers → My access tokens |
| `429 Too Many Requests` | Rate limit hit | Wait 60s, reduce query complexity |
| `400 Bad Request` | Invalid column ID/value | Run `get_board_schema` to verify column IDs |
| `403 Forbidden` | Insufficient permissions | Check user role & board permissions |
| MCP tools not found | MCP not configured | Run setup flow (see Prerequisites) |

When credentials are missing:
```
MISSING: MONDAY_TOKEN
ASK_USER: Please provide your Monday.com API token.
LOCATION: Monday.com → Avatar (bottom-left) → Developers → My access tokens
```

## Direct API Fallback

If MCP is unavailable, use `scripts/monday_api.sh` for direct GraphQL calls:

```bash
bash .claude/skills/monday-com/scripts/monday_api.sh query '{ boards(limit:5) { id name } }'
```

```bash
bash .claude/skills/monday-com/scripts/monday_api.sh mutation \
  'mutation { create_item(board_id: 123, item_name: "New Task") { id } }'
```

## References

| Topic | File |
|-------|------|
| Column value formats | `references/column-types.md` |
| GraphQL query examples | `references/graphql-examples.md` |
| Dashboards, fields, batch ops, webhooks | `references/advanced-workflows.md` |

## Integration

Pairs with:
- `system-architect` — Board/workspace structure design
- `brainstorm` — Feature planning before task creation