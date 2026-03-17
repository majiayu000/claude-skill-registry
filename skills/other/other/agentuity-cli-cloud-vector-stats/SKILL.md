---
name: agentuity-cli-cloud-vector-stats
description: Get statistics for vector storage. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "[name]"
metadata:
  command: "agentuity cloud vector stats"
  tags: "read-only fast requires-auth"
---

# Cloud Vector Stats

Get statistics for vector storage

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud vector stats [name]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | No | - |

## Examples

Show stats for all namespaces:

```bash
bunx @agentuity/cli vector stats
```

Show detailed stats for products namespace:

```bash
bunx @agentuity/cli vector stats products
```

Show stats for embeddings:

```bash
bunx @agentuity/cli vector stats embeddings
```
