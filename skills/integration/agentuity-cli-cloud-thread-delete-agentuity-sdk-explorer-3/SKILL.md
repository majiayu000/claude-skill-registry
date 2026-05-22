---
name: agentuity-cli-cloud-thread-delete
description: Delete a thread. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<thread_id>"
metadata:
  command: "agentuity cloud thread delete"
  tags: "destructive requires-auth"
---

# Cloud Thread Delete

Delete a thread

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity cloud thread delete <thread_id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<thread_id>` | string | Yes | - |

## Examples

Delete a thread by ID:

```bash
bunx @agentuity/cli cloud thread delete thrd_abc123xyz
```
