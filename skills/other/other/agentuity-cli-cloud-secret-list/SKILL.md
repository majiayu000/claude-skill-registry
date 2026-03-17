---
name: agentuity-cli-cloud-secret-list
description: List all secrets. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud secret list"
  tags: "read-only fast requires-auth requires-project"
---

# Cloud Secret List

List all secrets

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud secret list [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--mask` | boolean | No | `true` | mask the values in output (default: true in TTY for secrets) |

## Examples

List items:

```bash
bunx @agentuity/cli secret list
```

Use no mask option:

```bash
bunx @agentuity/cli secret list --no-mask
```

## Output

Returns: `object`
