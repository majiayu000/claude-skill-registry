---
name: agentuity-cli-project-list
description: List all projects. Requires authentication. Use for project management operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity project list"
  tags: "read-only slow requires-auth"
---

# Project List

List all projects

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity project list
```

## Examples

List projects (human-readable):

```bash
bunx @agentuity/cli project list
```

List projects in JSON format:

```bash
bunx @agentuity/cli --json project list
```

Alias for "project list" — list projects (human-readable):

```bash
bunx @agentuity/cli project ls
```

## Output

Returns: `array`
