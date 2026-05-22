---
name: agentuity-cli-cloud-queue-sources-list
description: List sources for a queue. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<queue_name>"
metadata:
  command: "agentuity cloud queue sources list"
  tags: "read-only fast requires-auth"
---

# Cloud Queue Sources List

List sources for a queue

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud queue sources list <queue_name>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<queue_name>` | string | Yes | - |

## Examples

List queue sources:

```bash
bunx @agentuity/cli cloud queue sources list my-queue
```

## Output

Returns JSON object:

```json
{
  "sources": "array"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `sources` | array | - |
