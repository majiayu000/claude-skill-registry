---
name: agentuity-cli-cloud-env-list
description: List all environment variables. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud env list"
  tags: "read-only fast requires-auth requires-project"
---

# Cloud Env List

List all environment variables

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud env list [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--mask` | boolean | No | `false` | mask the values in output (default: false for env vars) |

## Examples

List items:

```bash
bunx @agentuity/cli env list
```

Use mask option:

```bash
bunx @agentuity/cli env list --mask
```

## Output

Returns: `object`
