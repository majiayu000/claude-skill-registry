---
name: agentuity-cli-cloud-machine-deployments
description: List deployments running on a specific organization managed machine. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<machine_id>"
metadata:
  command: "agentuity cloud machine deployments"
  tags: "read-only slow requires-auth"
---

# Cloud Machine Deployments

List deployments running on a specific organization managed machine

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud machine deployments <machine_id>
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<machine_id>` | string | Yes | - |

## Examples

List deployments on a machine:

```bash
bunx @agentuity/cli cloud machine deployments machine_abc123xyz
```

## Output

Returns: `array`
