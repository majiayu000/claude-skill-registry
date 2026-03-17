---
name: agentuity-cli-git-status
description: Show GitHub connection status for current project. Requires authentication
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity git status"
  tags: "read-only"
---

# Git Status

Show GitHub connection status for current project

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity git status
```

## Examples

Show GitHub status for current project:

```bash
bunx @agentuity/cli git status
```

Get status in JSON format:

```bash
bunx @agentuity/cli --json git status
```

## Output

Returns JSON object:

```json
{
  "orgId": "string",
  "connected": "boolean",
  "integrations": "array",
  "projectId": "string",
  "linked": "boolean",
  "repoFullName": "string",
  "branch": "string",
  "directory": "string",
  "autoDeploy": "boolean",
  "previewDeploy": "boolean"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `orgId` | string | Organization ID |
| `connected` | boolean | Whether GitHub is connected to the org |
| `integrations` | array | Connected GitHub accounts |
| `projectId` | string | Project ID |
| `linked` | boolean | Whether the project is linked to a repo |
| `repoFullName` | string | Full repository name |
| `branch` | string | Branch |
| `directory` | string | Directory |
| `autoDeploy` | boolean | Auto-deploy enabled |
| `previewDeploy` | boolean | Preview deploys enabled |
