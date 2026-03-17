---
name: agentuity-cli-git-unlink
description: Unlink a project from its GitHub repository. Requires authentication
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity git unlink"
  tags: "mutating destructive"
---

# Git Unlink

Unlink a project from its GitHub repository

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity git unlink [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--confirm` | boolean | Yes | - | Skip confirmation prompt |

## Examples

Unlink current project from GitHub:

```bash
bunx @agentuity/cli git unlink
```

Unlink without confirmation prompt:

```bash
bunx @agentuity/cli git unlink --confirm
```

Unlink and return JSON result:

```bash
bunx @agentuity/cli --json git unlink --confirm
```

## Output

Returns JSON object:

```json
{
  "unlinked": "boolean",
  "repoFullName": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `unlinked` | boolean | Whether the project was unlinked |
| `repoFullName` | string | Repository that was unlinked |
