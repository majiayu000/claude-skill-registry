---
name: agentuity-cli-cloud-deploy
description: Deploy project to the Agentuity Cloud. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud deploy"
  tags: "mutating creates-resource slow api-intensive requires-auth requires-project"
---

# Cloud Deploy

Deploy project to the Agentuity Cloud

## Prerequisites

- Authenticated with `agentuity auth login`
- Project context required (run from project directory or use `--project-id`)
- auth login

## Usage

```bash
agentuity cloud deploy [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--logsUrl` | string | Yes | - | The url to the CI build logs |
| `--trigger` | string | No | `"cli"` | The trigger that caused the build |
| `--commitUrl` | string | Yes | - | The url to the CI commit |
| `--message` | string | Yes | - | The message to associate with this deployment |
| `--commit` | string | Yes | - | The commit SHA for this deployment |
| `--branch` | string | Yes | - | The git branch for this deployment |
| `--provider` | string | Yes | - | The CI provider name (attempts to autodetect) |
| `--repo` | string | Yes | - | The repo url |
| `--event` | string | No | `"manual"` | The event that triggered the deployment |
| `--pullRequestNumber` | number | Yes | - | the pull request number |
| `--pullRequestUrl` | string | Yes | - | the pull request url |
| `--reportFile` | string | Yes | - | file path to save build report JSON with errors, warnings, and diagnostics |
| `--childMode` | boolean | No | `false` | Internal: run as forked child process |

## Examples

Deploy current project:

```bash
bunx @agentuity/cli cloud deploy
```

Deploy with verbose output:

```bash
bunx @agentuity/cli cloud deploy --log-level=debug
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "deploymentId": "string",
  "projectId": "string",
  "logs": "array",
  "urls": "object"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether deployment succeeded |
| `deploymentId` | string | Deployment ID |
| `projectId` | string | Project ID |
| `logs` | array | The deployment startup logs |
| `urls` | object | Deployment URLs |
