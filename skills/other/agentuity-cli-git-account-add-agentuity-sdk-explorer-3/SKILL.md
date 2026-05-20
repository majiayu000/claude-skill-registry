---
name: agentuity-cli-git-account-add
description: Add a GitHub account to your organization. Requires authentication
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity git account add"
  tags: "mutating creates-resource slow api-intensive"
---

# Git Account Add

Add a GitHub account to your organization

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity git account add [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--org` | string | Yes | - | Organization ID to add the account to |

## Examples

Add a GitHub account to your organization:

```bash
bunx @agentuity/cli git account add
```

Add to a specific organization:

```bash
bunx @agentuity/cli git account add --org org_abc123
```

## Output

Returns JSON object:

```json
{
  "connected": "boolean",
  "orgId": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `connected` | boolean | Whether the account was connected |
| `orgId` | string | Organization ID |
