---
name: agentuity-cli-cloud-deploy
description: Deploy project to the Agentuity Cloud. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.104"
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
| `--tag` | array | No | `["latest"]` | One or more tags to add to the deployment |
| `--logsUrl` | string | Yes | - | The url to the CI build logs |
| `--trigger` | string | No | `"cli"` | The trigger that caused the build |
| `--commitUrl` | string | Yes | - | The url to the CI commit |
| `--message` | string | Yes | - | The message to associate with this deployment |
| `--provider` | string | Yes | - | The CI provider name (attempts to autodetect) |
| `--event` | string | No | `"manual"` | The event that triggered the deployment |
| `--pullRequestNumber` | number | Yes | - | the pull request number |
| `--pullRequestCommentId` | string | Yes | - | the pull request comment id |
| `--pullRequestURL` | string | Yes | - | the pull request url |

## Examples

Deploy current project:

```bash
bunx @agentuity/cli cloud deploy
```

Deploy with verbose output:

```bash
bunx @agentuity/cli cloud deploy --log-level=debug
```

Deploy with specific tags:

```bash
bunx @agentuity/cli cloud deploy --tag a --tag b
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
