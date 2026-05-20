---
name: agentuity-cli-project-create
description: Create a new project. Use for project management operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity project create"
  tags: "mutating creates-resource slow"
---

# Project Create

Create a new project

## Usage

```bash
agentuity project create [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--name` | string | Yes | - | Project name |
| `--dir` | string | Yes | - | Directory to create the project in |
| `--domains` | array | Yes | - | Array of custom domains |
| `--template` | string | Yes | - | Template to use |
| `--templateDir` | string | Yes | - | Local template directory for testing (e.g., ./packages/templates) |
| `--templateBranch` | string | Yes | - | GitHub branch to use for templates (default: main) |
| `--install` | boolean | No | `true` | Run bun install after creating the project (use --no-install to skip) |
| `--build` | boolean | No | `true` | Run bun run build after installing (use --no-build to skip) |
| `--confirm` | boolean | Yes | - | Skip confirmation prompts |
| `--register` | boolean | No | `true` | Register the project, if authenticated (use --no-register to skip) |

## Examples

Create new item:

```bash
bunx @agentuity/cli project create
```

Create new item:

```bash
bunx @agentuity/cli project create --name my-ai-agent
```

Create new item:

```bash
bunx @agentuity/cli project create --name customer-service-bot --dir ~/projects/agent
```

Use no install option:

```bash
bunx @agentuity/cli project create --template basic --no-install
```

Use no register option:

```bash
bunx @agentuity/cli project new --no-register
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "name": "string",
  "path": "string",
  "projectId": "string",
  "template": "string",
  "installed": "boolean",
  "built": "boolean",
  "domains": "array"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation succeeded |
| `name` | string | Project name |
| `path` | string | Project directory path |
| `projectId` | string | Project ID if registered |
| `template` | string | Template used |
| `installed` | boolean | Whether dependencies were installed |
| `built` | boolean | Whether the project was built |
| `domains` | array | Array of custom domains |
