---
name: agentuity-cli-cloud-keyvalue-create-namespace
description: Create a new keyvalue namespace. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<name>"
metadata:
  command: "agentuity cloud keyvalue create-namespace"
  tags: "mutating creates-resource slow requires-auth"
---

# Cloud Keyvalue Create-namespace

Create a new keyvalue namespace

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud keyvalue create-namespace <name>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<name>` | string | Yes | - |

## Examples

Create production namespace:

```bash
bunx @agentuity/cli kv create-namespace production
```

Create staging namespace (using alias):

```bash
bunx @agentuity/cli kv create staging
```

Create cache namespace:

```bash
bunx @agentuity/cli kv create cache
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "namespace": "string",
  "message": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `namespace` | string | Namespace name |
| `message` | string | Success message |
