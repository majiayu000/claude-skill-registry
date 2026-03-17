---
name: agentuity-cli-project-auth-init
description: Set up Agentuity Auth for your project. Requires authentication. Use for managing authentication credentials
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity project auth init"
  tags: "mutating slow requires-auth"
---

# Project Auth Init

Set up Agentuity Auth for your project

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity project auth init [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--skipMigrations` | boolean | Yes | - | Skip running database migrations (run `agentuity project auth generate` later) |

## Examples

Set up Agentuity Auth with database selection:

```bash
bunx @agentuity/cli project auth init
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "database": "string",
  "authFileCreated": "boolean",
  "migrationsRun": "boolean"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether setup succeeded |
| `database` | string | Database name used |
| `authFileCreated` | boolean | Whether auth.ts was created |
| `migrationsRun` | boolean | Whether migrations were run |
