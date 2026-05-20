---
name: agentuity-cli-cloud-deployment-undeploy
description: Undeploy the latest deployment. Requires authentication. Use for Agentuity cloud platform operations
version: "0.0.103"
license: Apache-2.0
allowed-tools: "Bash(agentuity:*)"
metadata:
  command: "agentuity cloud deployment undeploy"
  tags: "destructive deletes-resource slow requires-auth requires-deployment"
---

# Cloud Deployment Undeploy

Undeploy the latest deployment

## Prerequisites

- Authenticated with `agentuity auth login`
- cloud deploy

## Usage

```bash
agentuity cloud deployment undeploy [options]
```

## Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `--project-id` | string | Yes | - | Project ID |
| `--force` | boolean | No | `false` | Force undeploy without confirmation |

## Examples

Undeploy with confirmation:

```bash
bunx @agentuity/cli cloud deployment undeploy
```

Undeploy without confirmation:

```bash
bunx @agentuity/cli cloud deployment undeploy --force
```

Undeploy specific project:

```bash
bunx @agentuity/cli cloud deployment undeploy --project-id=proj_abc123xyz
```
