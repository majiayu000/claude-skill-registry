---
name: agentuity-cli-cloud-sandbox-execution-list
description: List executions for a sandbox. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<sandboxId>"
metadata:
  command: "agentuity cloud sandbox execution list"
  tags: "read-only fast requires-auth"
---

# Cloud Sandbox Execution List

List executions for a sandbox

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox execution list <sandboxId> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<sandboxId>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--limit` | number | Yes | - | Maximum number of results (default: 50, max: 100) |

## Examples

List executions for a sandbox:

```bash
bunx @agentuity/cli cloud sandbox execution list snbx_abc123
```

List with a limit:

```bash
bunx @agentuity/cli cloud sandbox execution list snbx_abc123 --limit 10
```

## Output

Returns JSON object:

```json
{
  "executions": "array"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `executions` | array | List of executions |
