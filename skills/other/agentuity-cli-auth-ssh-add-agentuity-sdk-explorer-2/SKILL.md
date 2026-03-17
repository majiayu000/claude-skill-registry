---
name: agentuity-cli-auth-ssh-add
description: Add an SSH public key to your account (reads from file or stdin). Requires authentication. Use for managing authentication credentials
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity auth ssh add"
  tags: "mutating creates-resource slow requires-auth"
---

# Auth Ssh Add

Add an SSH public key to your account (reads from file or stdin)

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity auth ssh add [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--file` | string | Yes | - | File containing the public key |

## Examples

Add SSH key interactively:

```bash
bunx @agentuity/cli auth ssh add
```

Add SSH key from file:

```bash
bunx @agentuity/cli auth ssh add --file ~/.ssh/id_ed25519.pub
```

Add deploy key from file:

```bash
bunx @agentuity/cli auth ssh add --file ./deploy_key.pub
```

Add SSH key from stdin:

```bash
cat ~/.ssh/id_rsa.pub | bunx @agentuity/cli auth ssh add
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "fingerprint": "string",
  "keyType": "string",
  "added": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `fingerprint` | string | SSH key fingerprint |
| `keyType` | string | SSH key type (e.g., ssh-rsa, ssh-ed25519) |
| `added` | number | Number of keys added |
