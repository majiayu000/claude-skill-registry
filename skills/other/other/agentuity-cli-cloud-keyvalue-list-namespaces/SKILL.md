---
name: agentuity-cli-cloud-keyvalue-list-namespaces
description: List all keyvalue namespaces. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud keyvalue list-namespaces"
  tags: "read-only fast requires-auth"
---

# Cloud Keyvalue List-namespaces

List all keyvalue namespaces

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud keyvalue list-namespaces
```

## Examples

List all namespaces:

```bash
bunx @agentuity/cli kv list-namespaces
```

List namespaces (using alias):

```bash
bunx @agentuity/cli kv namespaces
```

List namespaces (short alias):

```bash
bunx @agentuity/cli kv ns
```

## Output

Returns: `array`
