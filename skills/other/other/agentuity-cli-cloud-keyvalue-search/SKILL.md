---
name: agentuity-cli-cloud-keyvalue-search
description: Search for keys matching a keyword in a keyvalue namespace. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<name> <keyword>"
metadata:
  command: "agentuity cloud keyvalue search"
  tags: "read-only slow requires-auth"
---

# Cloud Keyvalue Search

Search for keys matching a keyword in a keyvalue namespace

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud keyvalue search <name> <keyword>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | Yes | - |
| `<keyword>` | string | Yes | - |

## Examples

Find all user-related keys:

```bash
bunx @agentuity/cli kv search production user
```

Find all session keys in cache:

```bash
bunx @agentuity/cli kv search cache session
```

Find all config keys:

```bash
bunx @agentuity/cli kv search staging config
```

## Output

Returns JSON object:

```json
{
  "namespace": "string",
  "keyword": "string",
  "results": "array"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `namespace` | string | Namespace name |
| `keyword` | string | Search keyword used |
| `results` | array | - |
