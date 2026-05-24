---
name: agentuity-cli-git-link
description: Link a project to a GitHub repository. Requires authentication
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity git link"
  tags: "mutating creates-resource"
---

# Git Link

Link a project to a GitHub repository

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity git link [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--repo` | string | Yes | - | Repository full name (owner/repo) to link |
| `--deploy` | boolean | Yes | - | Enable automatic deployments on push (default: true) |
| `--preview` | boolean | Yes | - | Enable preview deployments on pull requests (default: true) |
| `--branch` | string | Yes | - | Branch to deploy from (default: repo default branch) |
| `--root` | string | Yes | - | Root directory containing agentuity.json (default: .) |
| `--confirm` | boolean | Yes | - | Skip confirmation prompts |

## Examples

Link current project to a GitHub repository:

```bash
bunx @agentuity/cli git link
```

Link to a specific repo non-interactively:

```bash
bunx @agentuity/cli git link --repo owner/repo --branch main --confirm
```

Link from the current directory:

```bash
bunx @agentuity/cli git link --root .
```

Link to a specific branch:

```bash
bunx @agentuity/cli git link --branch main
```

Enable preview deployments on PRs:

```bash
bunx @agentuity/cli git link --preview true
```

Disable automatic deployments on push:

```bash
bunx @agentuity/cli git link --deploy false
```

Link a subdirectory in a monorepo:

```bash
bunx @agentuity/cli git link --root packages/my-agent
```

Link and return JSON result:

```bash
bunx @agentuity/cli --json git link --repo owner/repo --branch main --confirm
```

## Output

Returns JSON object:

```json
{
  "linked": "boolean",
  "repoFullName": "string",
  "branch": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `linked` | boolean | Whether the project was linked |
| `repoFullName` | string | Repository that was linked |
| `branch` | string | Branch configured |
