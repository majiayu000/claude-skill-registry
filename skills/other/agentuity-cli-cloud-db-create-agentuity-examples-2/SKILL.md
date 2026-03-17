---
name: agentuity-cli-cloud-db-create
description: Create a new database resource. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud db create"
  tags: "mutating creates-resource slow requires-auth requires-deployment"
---

# Cloud Db Create

Create a new database resource

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud db create [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--name` | string | Yes | - | Custom database name |

## Examples

Create new item:

```bash
bunx @agentuity/cli cloud db create
```

Run new command:

```bash
bunx @agentuity/cli cloud db new
```

Create new item:

```bash
bunx @agentuity/cli cloud db create --name my-db
```

Create new item:

```bash
bunx @agentuity/cli --dry-run cloud db create
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "name": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether creation succeeded |
| `name` | string | Created database name |
