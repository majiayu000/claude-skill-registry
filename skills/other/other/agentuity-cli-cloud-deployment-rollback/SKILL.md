---
name: agentuity-cli-cloud-deployment-rollback
description: Rollback the latest to the previous deployment. Requires authentication. Use for Agentuity cloud platform operations
version: "0.1.2"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud deployment rollback"
  tags: "destructive deletes-resource updates-resource slow api-intensive requires-auth requires-deployment"
---

# Cloud Deployment Rollback

Rollback the latest to the previous deployment

## Prerequisites

- Authenticated with `agentuity auth login`
- cloud deploy

## Usage

```bash
agentuity cloud deployment rollback [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--project-id` | string | Yes | - | Project ID |

## Examples

Rollback to previous deployment:

```bash
bunx @agentuity/cli cloud deployment rollback
```

Rollback specific project:

```bash
bunx @agentuity/cli cloud deployment rollback --project-id=proj_abc123xyz
```

## Output

Returns JSON object:

```json
{
  "success": "boolean",
  "projectId": "string",
  "targetDeploymentId": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the rollback succeeded |
| `projectId` | string | Project ID |
| `targetDeploymentId` | string | Deployment ID that was rolled back to |
