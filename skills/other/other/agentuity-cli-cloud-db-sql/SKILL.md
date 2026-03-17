---
name: agentuity-cli-cloud-db-sql
description: Execute SQL query on a database. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<name> <query>"
metadata:
  command: "agentuity cloud db sql"
  tags: "slow requires-auth"
---

# Cloud Db Sql

Execute SQL query on a database

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud db sql <name> <query>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | Yes | - |
| `<query>` | string | Yes | - |

## Examples

Execute SQL query:

```bash
bunx @agentuity/cli cloud db sql my-database "SELECT * FROM users LIMIT 10"
```

Execute query with JSON output:

```bash
bunx @agentuity/cli cloud db exec my-database "SELECT COUNT(*) FROM orders" --json
```

Query with filter:

```bash
bunx @agentuity/cli cloud db query my-database "SELECT * FROM products WHERE price > 100"
```

## Output

Returns JSON object:

```json
{
  "rows": "array",
  "rowCount": "number",
  "truncated": "boolean"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `rows` | array | Query results |
| `rowCount` | number | Number of rows returned |
| `truncated` | boolean | Whether results were truncated |
