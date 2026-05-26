---
name: agentuity-cli-auth-machine-setup
description: "Set up machine authentication by uploading a public key for self-hosted infrastructure. Requires authentication. Use for managing authentication credentials"
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity auth machine setup"
  tags: "mutating slow requires-auth uses-stdin"
---

# Auth Machine Setup

Set up machine authentication by uploading a public key for self-hosted infrastructure

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity auth machine setup [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--file` | string | Yes | - | Path to the public key file (PEM format) |

## Examples

Upload ECDSA P-256 public key from file:

```bash
bunx @agentuity/cli auth machine setup --file ./public-key.pem
```

Upload public key from stdin:

```bash
cat public-key.pem | bunx @agentuity/cli auth machine setup
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "orgId": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the setup succeeded |
| `orgId` | string | The organization ID |
