---
name: agentuity-cli-cloud-keyvalue-stats
description: Get statistics for keyvalue storage. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "[name]"
metadata:
  command: "agentuity cloud keyvalue stats"
  tags: "read-only fast requires-auth"
---

# Cloud Keyvalue Stats

Get statistics for keyvalue storage

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud keyvalue stats [name]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | No | - |

## Examples

Show stats for all namespaces:

```bash
bunx @agentuity/cli kv stats
```

Show stats for production namespace:

```bash
bunx @agentuity/cli kv stats production
```

Show stats for cache namespace:

```bash
bunx @agentuity/cli kv stats cache
```
