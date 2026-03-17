---
name: agentuity-cli-cloud-db-list
description: List database resources. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud db list"
  tags: "read-only fast requires-auth"
---

# Cloud Db List

List database resources

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud db list [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--showCredentials` | boolean | Yes | - | Show credentials in plain text (default: masked in terminal, unmasked in JSON) |
| `--nameOnly` | boolean | Yes | - | Print the name only |

## Examples

List items:

```bash
bunx @agentuity/cli cloud db list
```

Show output in JSON format:

```bash
bunx @agentuity/cli --json cloud db list
```

List items:

```bash
bunx @agentuity/cli cloud db ls
```

Use show credentials option:

```bash
bunx @agentuity/cli cloud db list --show-credentials
```

## Output

Returns JSON object:

```json
{
  "databases": "array"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `databases` | array | List of database resources |
