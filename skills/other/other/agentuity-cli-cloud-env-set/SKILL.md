---
name: agentuity-cli-cloud-env-set
description: Set an environment variable. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<key> <value>"
metadata:
  command: "agentuity cloud env set"
  tags: "mutating updates-resource slow requires-auth requires-project"
---

# Cloud Env Set

Set an environment variable

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud env set <key> <value>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<key>` | string | Yes | - |
| `<value>` | string | Yes | - |

## Examples

Run production command:

```bash
bunx @agentuity/cli env set NODE_ENV production
```

Run 3000 command:

```bash
bunx @agentuity/cli env set PORT 3000
```

Run debug command:

```bash
bunx @agentuity/cli env set LOG_LEVEL debug
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "key": "string",
  "path": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `key` | string | Environment variable key |
| `path` | string | Local file path where env var was saved |
