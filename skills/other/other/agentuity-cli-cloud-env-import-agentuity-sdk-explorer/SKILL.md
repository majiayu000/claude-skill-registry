---
name: agentuity-cli-cloud-env-import
description: Import environment variables from a file to cloud and local .env. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<file>"
metadata:
  command: "agentuity cloud env import"
  tags: "mutating creates-resource slow api-intensive requires-auth requires-project"
---

# Cloud Env Import

Import environment variables from a file to cloud and local .env

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud env import <file>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<file>` | string | Yes | - |

## Examples

Import environment variables from .env file:

```bash
bunx @agentuity/cli cloud env import .env
```

Import from .env.local file:

```bash
bunx @agentuity/cli cloud env import .env.local
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "imported": "number",
  "skipped": "number",
  "path": "string",
  "file": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether import succeeded |
| `imported` | number | Number of items imported |
| `skipped` | number | Number of items skipped |
| `path` | string | Local file path where variables were saved |
| `file` | string | Source file path |
