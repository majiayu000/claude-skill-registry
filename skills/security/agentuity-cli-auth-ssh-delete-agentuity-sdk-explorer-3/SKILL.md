---
name: agentuity-cli-auth-ssh-delete
description: Delete an SSH key from your account. Requires authentication. Use for managing authentication credentials
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "[fingerprints...]"
metadata:
  command: "agentuity auth ssh delete"
  tags: "destructive deletes-resource slow requires-auth"
---

# Auth Ssh Delete

Delete an SSH key from your account

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity auth ssh delete [fingerprints...] [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<fingerprints...>` | array | No | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--confirm` | boolean | No | `true` | prompt for confirmation before deletion |

## Examples

Delete item:

```bash
bunx @agentuity/cli auth ssh delete
```

Delete item:

```bash
bunx @agentuity/cli auth ssh delete <fingerprint>
```

Delete item:

```bash
bunx @agentuity/cli --explain auth ssh delete abc123
```

Delete item:

```bash
bunx @agentuity/cli --dry-run auth ssh delete abc123
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "removed": "number",
  "fingerprints": "array"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `removed` | number | Number of keys removed |
| `fingerprints` | array | Fingerprints of removed keys |
