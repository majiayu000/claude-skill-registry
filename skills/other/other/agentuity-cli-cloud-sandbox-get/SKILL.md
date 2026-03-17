---
name: agentuity-cli-cloud-sandbox-get
description: Get information about a sandbox. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<sandboxId>"
metadata:
  command: "agentuity cloud sandbox get"
  tags: "read-only fast requires-auth"
---

# Cloud Sandbox Get

Get information about a sandbox

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox get <sandboxId>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<sandboxId>` | string | Yes | - |

## Examples

Get sandbox information:

```bash
bunx @agentuity/cli cloud sandbox get abc123
```

## Output

Returns JSON object:

```json
{
  "sandboxId": "string",
  "status": "string",
  "createdAt": "string",
  "region": "string",
  "snapshotId": "string",
  "snapshotTag": "string",
  "executions": "number",
  "stdoutStreamUrl": "string",
  "stderrStreamUrl": "string",
  "dependencies": "array",
  "metadata": "object",
  "resources": "object"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `sandboxId` | string | Sandbox ID |
| `status` | string | Current status |
| `createdAt` | string | Creation timestamp |
| `region` | string | Region where sandbox is running |
| `snapshotId` | string | Snapshot ID sandbox was created from |
| `snapshotTag` | string | Snapshot tag sandbox was created from |
| `executions` | number | Number of executions |
| `stdoutStreamUrl` | string | URL to stdout output stream |
| `stderrStreamUrl` | string | URL to stderr output stream |
| `dependencies` | array | Apt packages installed |
| `metadata` | object | User-defined metadata |
| `resources` | object | Resource limits |
