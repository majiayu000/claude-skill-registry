---
name: agentuity-cli-cloud-session-get
description: Get details about a specific session. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<session_id>"
metadata:
  command: "agentuity cloud session get"
  tags: "read-only fast requires-auth"
---

# Cloud Session Get

Get details about a specific session

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud session get <session_id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<session_id>` | string | Yes | - |

## Examples

Get a session by ID:

```bash
bunx @agentuity/cli cloud session get sess_abc123xyz
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "created_at": "string",
  "start_time": "string",
  "end_time": "unknown",
  "duration": "unknown",
  "org_id": "string",
  "project_id": "string",
  "deployment_id": "string",
  "agent_ids": "array",
  "trigger": "string",
  "env": "string",
  "devmode": "boolean",
  "pending": "boolean",
  "success": "boolean",
  "error": "unknown",
  "method": "string",
  "url": "string",
  "route_id": "string",
  "thread_id": "string",
  "agents": "array",
  "eval_runs": "array",
  "timeline": "unknown",
  "route": "unknown"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Session ID |
| `created_at` | string | Creation timestamp |
| `start_time` | string | Start time |
| `end_time` | unknown | End time |
| `duration` | unknown | Duration in nanoseconds |
| `org_id` | string | Organization ID |
| `project_id` | string | Project ID |
| `deployment_id` | string | Deployment ID |
| `agent_ids` | array | Agent IDs |
| `trigger` | string | Trigger type |
| `env` | string | Environment |
| `devmode` | boolean | Dev mode |
| `pending` | boolean | Pending |
| `success` | boolean | Success |
| `error` | unknown | Error message |
| `method` | string | HTTP method |
| `url` | string | Request URL |
| `route_id` | string | Route ID |
| `thread_id` | string | Thread ID |
| `agents` | array | Agents |
| `eval_runs` | array | Eval runs |
| `timeline` | unknown | Session timeline |
| `route` | unknown | Route information |
