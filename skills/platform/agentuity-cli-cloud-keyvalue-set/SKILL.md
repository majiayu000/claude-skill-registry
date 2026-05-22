---
name: agentuity-cli-cloud-keyvalue-set
description: Set a key and value in the keyvalue storage. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.110"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<namespace> <key> <value> [ttl]"
metadata:
  command: "agentuity cloud keyvalue set"
  tags: "mutating updates-resource slow requires-auth"
---

# Cloud Keyvalue Set

Set a key and value in the keyvalue storage

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud keyvalue set <namespace> <key> <value> [ttl]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<namespace>` | string | Yes | - |
| `<key>` | string | Yes | - |
| `<value>` | string | Yes | - |
| `<ttl>` | string | No | - |

## Examples

Store user data:

```bash
bunx @agentuity/cli kv set production user:123 '{"name":"Alice","email":"alice@example.com"}'
```

Store session with 1h TTL:

```bash
bunx @agentuity/cli kv set cache session:abc "session-data-here" --ttl 3600
```

Cache homepage for 10m:

```bash
bunx @agentuity/cli kv set staging cache:homepage "<!DOCTYPE html>..." --ttl 600
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "namespace": "string",
  "key": "string",
  "contentType": "string",
  "durationMs": "number",
  "ttl": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `namespace` | string | Namespace name |
| `key` | string | Key name |
| `contentType` | string | Content type (application/json or text/plain) |
| `durationMs` | number | Operation duration in milliseconds |
| `ttl` | number | TTL in seconds if set |
