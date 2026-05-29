---
name: agentuity-cli-cloud-apikey-get
description: Get a specific API key by id. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<id>"
metadata:
  command: "agentuity cloud apikey get"
  tags: "read-only fast requires-auth"
---

# Cloud Apikey Get

Get a specific API key by id

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud apikey get <id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<id>` | string | Yes | - |

## Examples

Get item details:

```bash
bunx @agentuity/cli cloud apikey get <id>
```
