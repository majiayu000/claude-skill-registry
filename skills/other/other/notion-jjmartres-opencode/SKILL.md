---
name: notion
description: Manage Notion pages and databases from the CLI using notion-cli. Create, read, search, and update pages. Query databases, add entries, and manage blocks and properties.
license: MIT
compatibility: opencode
---

This skill manages Notion workspaces using the `notion-cli` tool.

## Pages

```bash
notion-cli page list                        # List recent pages
notion-cli page search "query"              # Search pages by title/content
notion-cli page get <page-id>              # Get page content
notion-cli page create --title "Title" --parent <page-id>
notion-cli page create --title "Title" --content "Body text"
notion-cli page update <page-id> --title "New Title"
notion-cli page delete <page-id>
notion-cli page append <page-id> "Additional content"
```

## Databases

```bash
notion-cli db list                          # List all databases
notion-cli db query <db-id>                # Query all entries
notion-cli db query <db-id> --filter "Status=Done"
notion-cli db query <db-id> --sort "Created" --desc
notion-cli db add <db-id> --props "Name=Task,Status=In Progress"
notion-cli db update <page-id> --props "Status=Done"
notion-cli db get <db-id>                  # Get database schema
```

## Blocks

```bash
notion-cli block list <page-id>            # List blocks in a page
notion-cli block append <page-id> --type "paragraph" --text "Hello"
notion-cli block append <page-id> --type "todo" --text "Task item"
notion-cli block delete <block-id>
```

## Usage Guidelines

- Use `notion-cli page search` to find pages before creating duplicates.
- Page and database IDs can be found in the Notion URL after the workspace slug.
- The `--props` flag uses `Key=Value` pairs separated by commas.
- Notion API token must be configured: `notion-cli auth` or via `NOTION_TOKEN` env var.

## Notes

- Requires a Notion integration token with appropriate permissions.
