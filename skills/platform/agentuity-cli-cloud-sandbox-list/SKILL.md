---
name: agentuity-cli-cloud-sandbox-list
description: List sandboxes with optional filtering. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.24"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud sandbox list"
  tags: "read-only slow requires-auth"
---

# Cloud Sandbox List

List sandboxes with optional filtering

## Prerequisites

- Authenticated with `agentuity auth login`
- Organization context required (`--org-id` or default org)

## Usage

```bash
agentuity cloud sandbox list [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--status` | string | Yes | - | Filter by status |
| `--projectId` | string | Yes | - | Filter by project ID |
| `--all` | boolean | Yes | - | List all sandboxes regardless of project context |
| `--limit` | number | Yes | - | Maximum number of results (default: 50, max: 100) |
| `--offset` | number | Yes | - | Pagination offset |

## Examples

List all sandboxes:

```bash
bunx @agentuity/cli cloud sandbox list
```

List running sandboxes:

```bash
bunx @agentuity/cli cloud sandbox list --status running
```

List sandboxes for a specific project:

```bash
bunx @agentuity/cli cloud sandbox list --project-id proj_123
```

List with pagination:

```bash
bunx @agentuity/cli cloud sandbox list --limit 10 --offset 20
```

List all sandboxes regardless of project context:

```bash
bunx @agentuity/cli cloud sandbox list --all
```

## Output

Returns JSON object:

```json
{
  "sandboxes": "array",
  "total": "number"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `sandboxes` | array | List of sandboxes |
| `total` | number | Total count |
