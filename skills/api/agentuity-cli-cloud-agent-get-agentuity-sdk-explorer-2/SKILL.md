---
name: agentuity-cli-cloud-agent-get
description: Get details about a specific agent. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<agent_id>"
metadata:
  command: "agentuity cloud agent get"
---

# Cloud Agent Get

Get details about a specific agent

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud agent get <agent_id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<agent_id>` | string | Yes | - |

## Examples

Get item details:

```bash
bunx @agentuity/cli cloud agent get agent_abc123
```

Show output in JSON format:

```bash
bunx @agentuity/cli --json cloud agent get agent_abc123
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "name": "string",
  "description": "unknown",
  "identifier": "string",
  "deploymentId": "unknown",
  "devmode": "boolean",
  "metadata": "unknown",
  "createdAt": "string",
  "updatedAt": "string",
  "evals": "array"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | - |
| `name` | string | - |
| `description` | unknown | - |
| `identifier` | string | - |
| `deploymentId` | unknown | - |
| `devmode` | boolean | - |
| `metadata` | unknown | - |
| `createdAt` | string | - |
| `updatedAt` | string | - |
| `evals` | array | - |
