---
name: agentuity-cli-cloud-eval-get
description: Get details about a specific eval. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<eval_id>"
metadata:
  command: "agentuity cloud eval get"
  tags: "read-only fast requires-auth"
---

# Cloud Eval Get

Get details about a specific eval

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud eval get <eval_id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<eval_id>` | string | Yes | - |

## Examples

Get an eval by ID:

```bash
bunx @agentuity/cli cloud eval get eval_abc123xyz
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "name": "string",
  "identifier": "unknown",
  "agent_identifier": "string",
  "created_at": "string",
  "updated_at": "string",
  "project_id": "string",
  "org_id": "string",
  "description": "unknown",
  "devmode": "boolean"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Eval ID |
| `name` | string | Eval name |
| `identifier` | unknown | Stable eval identifier |
| `agent_identifier` | string | Agent identifier |
| `created_at` | string | Creation timestamp |
| `updated_at` | string | Last updated timestamp |
| `project_id` | string | Project ID |
| `org_id` | string | Organization ID |
| `description` | unknown | Eval description |
| `devmode` | boolean | Whether this is a devmode eval |
