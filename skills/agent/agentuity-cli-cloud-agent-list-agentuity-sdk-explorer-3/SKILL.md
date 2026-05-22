---
name: agentuity-cli-cloud-agent-list
description: List agents for a project. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud agent list"
---

# Cloud Agent List

List agents for a project

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)

## Usage

```bash
agentuity cloud agent list [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--deploymentId` | string | Yes | - | Filter by deployment ID |
| `--verbose` | boolean | No | `false` | Show full descriptions |

## Examples

List items:

```bash
bunx @agentuity/cli cloud agent list
```

Use verbose option:

```bash
bunx @agentuity/cli cloud agent list --verbose
```

Show output in JSON format:

```bash
bunx @agentuity/cli --json cloud agent list
```

## Output

Returns: `array`
