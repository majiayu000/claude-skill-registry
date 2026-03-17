---
name: agentuity-cli-cloud-vector-list-namespaces
description: List all vector namespaces. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud vector list-namespaces"
  tags: "read-only fast requires-auth"
---

# Cloud Vector List-namespaces

List all vector namespaces

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud vector list-namespaces
```

## Examples

List all namespaces:

```bash
bunx @agentuity/cli vector list-namespaces
```

List namespaces (using alias):

```bash
bunx @agentuity/cli vector namespaces
```

List namespaces (short alias):

```bash
bunx @agentuity/cli vector ns
```

## Output

Returns: `array`
