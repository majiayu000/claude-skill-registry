---
name: coda
description: General-purpose Coda document manager via REST API v1. Supports listing/creating/updating/deleting docs, managing tables/rows/pages, triggering automations, and exploring doc structure. Requires CODA_API_TOKEN environment variable. Delete operations require explicit confirmation; publishing and permission changes require explicit user intent.
---

# Coda API Skill

Interact with the Coda REST API v1 to manage docs, tables, rows, pages, and automations.

## When to Use

Use this skill when the user wants to:
- List, search, create, or delete Coda docs
- Read from or write to tables (insert, upsert, update, delete rows)
- Explore doc structure (pages, tables, columns, formulas, controls)
- Trigger automations (push buttons)
- Export doc content or analytics

## When NOT to Use

- **Do NOT use** for general document editing advice unrelated to the API
- **Do NOT use** for Pack development (this skill covers Doc management, not Pack creation)
- **Do NOT use** for operations requiring Doc Maker permissions unless confirmed the user has them

## Prerequisites

1. **API Token**: Set environment variable `CODA_API_TOKEN` with your Coda API token
   - Get token at: https://coda.io/account -> API Settings
2. **Python 3.7+** with `requests` library installed
3. **Permissions**: Some operations (create doc, update doc title, create page) require Doc Maker role in the workspace

## CLI Tool Usage

The skill includes a Python CLI tool at `scripts/coda_cli.py`:

```bash
# Setup
export CODA_API_TOKEN="your_token_here"

# List docs
python scripts/coda_cli.py docs list --query "Project"

# Get doc info
python scripts/coda_cli.py docs get <doc-id>

# Create doc
python scripts/coda_cli.py docs create --title "My New Doc"

# List tables in doc
python scripts/coda_cli.py tables list <doc-id>

# List rows in table
python scripts/coda_cli.py rows list <doc-id> <table-id>

# Insert row
python scripts/coda_cli.py rows insert <doc-id> <table-id> --data '{"Name": "Task 1", "Status": "Done"}'

# Update row
python scripts/coda_cli.py rows update <doc-id> <table-id> <row-id> --data '{"Status": "In Progress"}'

# Delete row (requires confirmation)
python scripts/coda_cli.py rows delete <doc-id> <table-id> <row-id>

# List pages
python scripts/coda_cli.py pages list <doc-id>

# Trigger automation (push button)
python scripts/coda_cli.py automations trigger <doc-id> <button-id>

# Force delete without confirmation (use with caution)
python scripts/coda_cli.py docs delete <doc-id> --force
```

## Workflow Guidelines

### 1. Doc ID Extraction
Coda doc IDs can be extracted from browser URLs:
- URL: `https://coda.io/d/_dAbCDeFGH/Project-Tracker`
- Doc ID: `AbCDeFGH` (remove `_d` prefix)

The CLI tool accepts both full URLs and raw IDs.

### 2. Rate Limit Handling
The API has strict rate limits:
- **Read**: 100 requests per 6 seconds
- **Write (POST/PUT/PATCH)**: 10 requests per 6 seconds
- **Write doc content**: 5 requests per 10 seconds
- **List docs**: 4 requests per 6 seconds

The CLI tool automatically implements exponential backoff for 429 responses.

### 3. Asynchronous Operations
Write operations return HTTP 202 with a `requestId`. The CLI tool optionally polls for completion using `--wait` flag.

### 4. Safety Guardrails

**Delete Operations** (rows, docs, pages, folders):
- Always requires explicit user confirmation in interactive mode
- Use `--force` flag only in automation/scripts
- Shows preview of what will be deleted

**Publishing** (`docs publish`):
- Requires explicit `--confirm-publish` flag
- Cannot be combined with `--force`

**Permissions** (`acl` commands):
- Requires explicit `--confirm-permissions` flag for any changes
- Read operations (list permissions) are always allowed

**Automation Triggers**:
- Allowed without special flags but logged
- User should be aware that automations may trigger notifications or external actions

### 5. Pagination
List commands support:
- `--limit`: Maximum results (default 25, max varies by endpoint)
- `--page-token`: For fetching subsequent pages
- CLI auto-follows pages with `--all` flag

## Common Patterns

### Batch Row Operations
```bash
# Insert multiple rows from JSON file
python scripts/coda_cli.py rows insert-batch <doc-id> <table-id> --file rows.json

# Upsert rows (update if exists, insert if not) using key columns
python scripts/coda_cli.py rows upsert <doc-id> <table-id> --file rows.json --keys "Email"
```

### Sync Between Docs
```bash
# Export from source
python scripts/coda_cli.py rows list <source-doc> <table-id> --format json > export.json

# Import to destination
python scripts/coda_cli.py rows insert-batch <dest-doc> <table-id> --file export.json
```

### Explore Structure
```bash
# Get full doc structure
python scripts/coda_cli.py docs structure <doc-id>

# List all formulas
python scripts/coda_cli.py formulas list <doc-id>

# List all controls
python scripts/coda_cli.py controls list <doc-id>
```

## Error Handling

Common HTTP status codes:
- `400`: Bad request (invalid parameters)
- `401`: Invalid/expired API token
- `403`: Insufficient permissions (need Doc Maker role)
- `404`: Resource not found
- `429`: Rate limited (implement backoff)
- `202`: Accepted but not yet processed (async operation)

## Security Considerations

1. **Token Storage**: Never commit `CODA_API_TOKEN` to version control
2. **Token Scope**: The token has full access to all docs the user can access
3. **Workspace Restrictions**: Creating docs requires Doc Maker role in target workspace
4. **Data Exposure**: Row data may contain sensitive information; handle exports carefully

## Examples

### List and Filter Docs
```bash
python scripts/coda_cli.py docs list --is-owner --query "Project"
```

### Create Doc from Template
```bash
python scripts/coda_cli.py docs create --title "Q4 Planning" --source-doc "template-doc-id"
```

### Update Row Status
```bash
python scripts/coda_cli.py rows update AbCDeFGH grid-xyz row-123 \
  --data '{"Status": "Complete", "Completed Date": "2024-01-15"}'
```

### Delete Multiple Rows (with confirmation)
```bash
python scripts/coda_cli.py rows delete-batch AbCDeFGH grid-xyz \
  --filter '{"Status": "Archived"}' \
  --confirm "Delete all archived rows?"
```

### Export Table to CSV
```bash
python scripts/coda_cli.py rows list AbCDeFGH grid-xyz --format csv > export.csv
```

## Reference

- API Documentation: https://coda.io/developers/apis/v1
- OpenAPI Spec: https://coda.io/apis/v1/openapi.yaml
- Rate Limits: https://coda.io/developers/apis/v1#section/Rate-Limiting
