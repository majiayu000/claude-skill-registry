---
name: agentuity-cli-git-account-list
description: List GitHub accounts connected to your organizations. Requires authentication
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity git account list"
  tags: "read-only"
---

# Git Account List

List GitHub accounts connected to your organizations

## Prerequisites

- Authenticated with `agentuity auth login`

## Usage

```bash
agentuity git account list
```

## Examples

List all connected GitHub accounts:

```bash
bunx @agentuity/cli git account list
```

List accounts in JSON format:

```bash
bunx @agentuity/cli --json git account list
```

## Output

Returns: `array`
