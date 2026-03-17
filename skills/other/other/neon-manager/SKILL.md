---
name: Neon Database Manager
description: Tool for managing Neon Postgres databases. Use for listing projects, inspecting schema, and running queries.
---

# Neon Database Manager Skill

This skill grants access to the `neon` MCP tools. Use this to manage your Serverless Postgres instances.

## When to use

- Inspecting Neon projects and branches.
- Querying tables in a Neon database.
- Checking database schema.

## Available Tools (Context Loaded)

The following tools are available via the `neon` MCP server:

### Management

- `mcp__neon__list_projects`: View available Neon projects.

### Inspection & Querying

- `mcp__neon__get_database_tables`: List tables in a specific branch/database.
- `mcp__neon__run_sql`: Execute SQL queries against the database.

## Best Practices

1. **Read-Only First**: Prefer `run_sql` for SELECT statements. Be cautious with data modification.
2. **Schema Awareness**: Use `get_database_tables` before constructing complex queries to ensure column names are correct.

## Example Workflow

1. User: "Check the users table in the dev branch."
2. Agent: Calls `list_projects` to find the project ID.
3. Agent: Calls `get_database_tables` to verify the table exists.
4. Agent: Calls `run_sql` to select data.
