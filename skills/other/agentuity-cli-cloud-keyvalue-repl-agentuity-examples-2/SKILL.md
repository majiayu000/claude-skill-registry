---
name: agentuity-cli-cloud-keyvalue-repl
description: Start an interactive repl for working with keyvalue database. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud keyvalue repl"
  tags: "slow requires-auth"
---

# Cloud Keyvalue Repl

Start an interactive repl for working with keyvalue database

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud keyvalue repl
```

## Examples

Start interactive KV session:

```bash
bunx @agentuity/cli kv repl
```
