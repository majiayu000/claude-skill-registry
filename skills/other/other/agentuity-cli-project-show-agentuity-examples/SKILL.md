---
name: agentuity-cli-project-show
description: Show project detail. Requires authentication. Use for project management operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<id>"
metadata:
  command: "agentuity project show"
  tags: "read-only fast requires-auth requires-project"
---

# Project Show

Show project detail

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity project show <id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<id>` | string | Yes | - |

## Examples

Show details:

```bash
bunx @agentuity/cli project show proj_abc123def456
```

Show output in JSON format:

```bash
bunx @agentuity/cli --json project show proj_abc123def456
```

Get item details:

```bash
bunx @agentuity/cli project get proj_abc123def456
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "name": "string",
  "description": "unknown",
  "tags": "unknown",
  "orgId": "string",
  "secrets": "object",
  "env": "object"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Project ID |
| `name` | string | Project name |
| `description` | unknown | Project description |
| `tags` | unknown | Project tags |
| `orgId` | string | Organization ID |
| `secrets` | object | Project secrets (masked) |
| `env` | object | Environment variables |
