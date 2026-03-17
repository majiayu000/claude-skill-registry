---
name: agentuity-cli-cloud-keyvalue-keys
description: List all keys in a keyvalue namespace. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<name>"
metadata:
  command: "agentuity cloud keyvalue keys"
  tags: "read-only slow requires-auth"
---

# Cloud Keyvalue Keys

List all keys in a keyvalue namespace

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud keyvalue keys <name>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | Yes | - |

## Examples

List all keys in production:

```bash
bunx @agentuity/cli kv keys production
```

List all cached keys (using alias):

```bash
bunx @agentuity/cli kv ls cache
```

List all staging keys:

```bash
bunx @agentuity/cli kv list staging
```

## Output

Returns JSON object:

```json
{
  "namespace": "string",
  "keys": "array"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `namespace` | string | Namespace name |
| `keys` | array | List of keys in the namespace |
