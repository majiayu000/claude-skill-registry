---
name: agentuity-cli-cloud-eval-run-get
description: Get details about a specific eval run. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<eval_run_id>"
metadata:
  command: "agentuity cloud eval-run get"
  tags: "read-only fast requires-auth"
---

# Cloud Eval-run Get

Get details about a specific eval run

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud eval-run get <eval_run_id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<eval_run_id>` | string | Yes | - |

## Examples

Get an eval run by ID:

```bash
bunx @agentuity/cli cloud eval-run get evalrun_abc123xyz
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "eval_id": "string",
  "eval_name": "unknown",
  "agent_identifier": "unknown",
  "session_id": "string",
  "created_at": "string",
  "updated_at": "string",
  "project_id": "string",
  "org_id": "string",
  "deployment_id": "unknown",
  "devmode": "boolean",
  "pending": "boolean",
  "success": "boolean",
  "error": "unknown",
  "result": "unknown"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Eval run ID |
| `eval_id` | string | Eval ID |
| `eval_name` | unknown | Eval name |
| `agent_identifier` | unknown | Agent identifier |
| `session_id` | string | Session ID |
| `created_at` | string | Creation timestamp |
| `updated_at` | string | Last updated timestamp |
| `project_id` | string | Project ID |
| `org_id` | string | Organization ID |
| `deployment_id` | unknown | Deployment ID |
| `devmode` | boolean | Whether this is a devmode run |
| `pending` | boolean | Whether the eval run is pending |
| `success` | boolean | Whether the eval run succeeded |
| `error` | unknown | Error message if failed |
| `result` | unknown | Eval run result |
