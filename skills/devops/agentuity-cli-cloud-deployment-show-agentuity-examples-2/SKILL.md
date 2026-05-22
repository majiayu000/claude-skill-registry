---
name: agentuity-cli-cloud-deployment-show
description: Show details about a specific deployment. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
argument-hint: "<deployment_id>"
metadata:
  command: "agentuity cloud deployment show"
  tags: "read-only fast requires-auth requires-deployment"
---

# Cloud Deployment Show

Show details about a specific deployment

## Prerequisites

- Authenticated with `agentuity auth login`
- cloud deploy

## Usage

```bash
agentuity cloud deployment show <deployment_id> [options]
```

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `<deployment_id>` | string | Yes | - |

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--project-id` | string | Yes | - | Project ID |

## Examples

Show deployment details by ID:

```bash
bunx @agentuity/cli cloud deployment show dep_abc123xyz
```

Show deployment for specific project:

```bash
bunx @agentuity/cli cloud deployment show deployment-2024-11-20 --project-id=proj_abc123xyz
```

## Output

Returns JSON object:

```json
{
  "id": "string",
  "state": "string",
  "active": "boolean",
  "createdAt": "string",
  "updatedAt": "string",
  "message": "string",
  "tags": "array",
  "customDomains": "array",
  "cloudRegion": "string",
  "resourceDb": "unknown",
  "resourceStorage": "unknown",
  "deploymentLogsURL": "unknown",
  "buildLogsURL": "unknown",
  "metadata": "object"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Deployment ID |
| `state` | string | Deployment state |
| `active` | boolean | Whether deployment is active |
| `createdAt` | string | Creation timestamp |
| `updatedAt` | string | Last update timestamp |
| `message` | string | Deployment message |
| `tags` | array | Deployment tags |
| `customDomains` | array | Custom domains |
| `cloudRegion` | string | Cloud region |
| `resourceDb` | unknown | the database name |
| `resourceStorage` | unknown | the storage name |
| `deploymentLogsURL` | unknown | the url to the deployment logs |
| `buildLogsURL` | unknown | the url to the build logs |
| `metadata` | object | Deployment metadata |
