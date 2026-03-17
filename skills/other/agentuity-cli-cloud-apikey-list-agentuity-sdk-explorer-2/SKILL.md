---
name: agentuity-cli-cloud-apikey-list
description: List all API keys. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud apikey list"
  tags: "read-only fast requires-auth"
---

# Cloud Apikey List

List all API keys

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud apikey list [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--orgId` | string | Yes | - | filter by organization id |
| `--projectId` | string | Yes | - | filter by project id |

## Examples

List items:

```bash
bunx @agentuity/cli cloud apikey list
```

List items:

```bash
bunx @agentuity/cli cloud apikey ls
```
