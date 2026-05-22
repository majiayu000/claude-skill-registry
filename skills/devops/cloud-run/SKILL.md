---
name: cloud-run
description: Google Cloud Run deployment and management. Deploy applications, list services, get logs, and manage GCP projects. Use for Cloud Run deployments, service monitoring, and GCP project management.
context:fork: true
allowed-tools: read, write, bash
---

# Cloud Run Skill

## Overview

This skill provides access to the Google Cloud Platform Cloud Run MCP server with progressive disclosure for optimal context usage.

**Context Savings**: ~90% reduction

- **MCP Mode**: ~15,000 tokens always loaded (7 tools + prompts)
- **Skill Mode**: ~300 tokens metadata + on-demand loading

## Requirements

- Node.js 18+ OR Docker installed and running
- Google Cloud credentials configured via `gcloud auth application-default login`
- Optional: `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_REGION` environment variables

## Tools

The server provides 8 tools across deployment and management categories:

### Deployment Tools

| Tool                     | Description                                              | Mode           |
| ------------------------ | -------------------------------------------------------- | -------------- |
| `deploy-file-contents`   | Deploy files to Cloud Run by providing contents directly | Local + Remote |
| `deploy-local-folder`    | Deploy a local folder to Cloud Run                       | Local only     |
| `deploy-container-image` | Deploy a container image URL to Cloud Run                | Local + Remote |

### Service Management Tools

| Tool              | Description                                  | Mode           |
| ----------------- | -------------------------------------------- | -------------- |
| `list-services`   | List Cloud Run services in a project/region  | Local + Remote |
| `get-service`     | Get details for a specific Cloud Run service | Local + Remote |
| `get-service-log` | Get logs and errors for a specific service   | Local + Remote |

### Project Management Tools (Local Only)

| Tool             | Description                                    |
| ---------------- | ---------------------------------------------- |
| `list-projects`  | List available GCP projects                    |
| `create-project` | Create a new GCP project and attach to billing |

## Quick Reference

```bash
# List available tools
python executor.py --list

# List Cloud Run services
python executor.py --tool list-services --args '{"projectId": "my-project", "region": "us-central1"}'

# Get service details
python executor.py --tool get-service --args '{"projectId": "my-project", "region": "us-central1", "serviceName": "my-service"}'

# Get service logs
python executor.py --tool get-service-log --args '{"projectId": "my-project", "region": "us-central1", "serviceName": "my-service"}'

# Deploy file contents
python executor.py --tool deploy-file-contents --args '{"projectId": "my-project", "region": "us-central1", "serviceName": "my-service", "files": [{"path": "main.py", "contents": "..."}]}'

# List GCP projects
python executor.py --tool list-projects
```

## Configuration

### Environment Variables

| Variable                 | Description                          | Default       |
| ------------------------ | ------------------------------------ | ------------- |
| `GOOGLE_CLOUD_PROJECT`   | Default GCP project ID               | None          |
| `GOOGLE_CLOUD_REGION`    | Default Cloud Run region             | `us-central1` |
| `DEFAULT_SERVICE_NAME`   | Default service name for deployments | None          |
| `SKIP_IAM_CHECK`         | Skip IAM permission validation       | `false`       |
| `ENABLE_HOST_VALIDATION` | Enable Host header validation        | `false`       |

### Setup

1. **Authenticate with GCP**:

   ```bash
   gcloud auth application-default login
   ```

2. **Set default project** (optional):

   ```bash
   export GOOGLE_CLOUD_PROJECT=my-project-id
   export GOOGLE_CLOUD_REGION=us-central1
   ```

3. **Use the skill**:
   ```bash
   python .claude/skills/cloud-run/executor.py --list
   ```

## Prompts

The MCP server also provides natural language prompts:

| Prompt   | Description                                   |
| -------- | --------------------------------------------- |
| `deploy` | Deploy current working directory to Cloud Run |
| `logs`   | Get logs for a Cloud Run service              |

## Tool Details

### deploy-file-contents

Deploy files to Cloud Run by providing their contents directly.

**Parameters**:

- `projectId` (string, required): GCP project ID
- `region` (string, required): Cloud Run region
- `serviceName` (string, required): Name for the Cloud Run service
- `files` (array, required): Array of file objects with `path` and `contents`

**Example**:

```json
{
  "projectId": "my-project",
  "region": "us-central1",
  "serviceName": "my-api",
  "files": [
    { "path": "main.py", "contents": "from flask import Flask\napp = Flask(__name__)\n..." },
    { "path": "requirements.txt", "contents": "flask==2.0.0\ngunicorn==20.1.0" }
  ]
}
```

### list-services

List Cloud Run services in a given project and region.

**Parameters**:

- `projectId` (string, required): GCP project ID
- `region` (string, optional): Cloud Run region (defaults to configured region)

### get-service

Get detailed information about a specific Cloud Run service.

**Parameters**:

- `projectId` (string, required): GCP project ID
- `region` (string, required): Cloud Run region
- `serviceName` (string, required): Cloud Run service name

### get-service-log

Get logs and error messages for a specific Cloud Run service.

**Parameters**:

- `projectId` (string, required): GCP project ID
- `region` (string, required): Cloud Run region
- `serviceName` (string, required): Cloud Run service name
- `limit` (number, optional): Maximum number of log entries

### deploy-local-folder

Deploy a local folder to a Cloud Run service (local mode only).

**Parameters**:

- `projectId` (string, required): GCP project ID
- `region` (string, required): Cloud Run region
- `serviceName` (string, required): Cloud Run service name
- `folderPath` (string, required): Path to local folder to deploy

### list-projects

List available GCP projects (local mode only).

**Parameters**: None

### create-project

Create a new GCP project and attach it to billing (local mode only).

**Parameters**:

- `projectId` (string, required): Desired project ID
- `projectName` (string, optional): Human-readable project name

## Integration with Agents

This skill integrates with the following agents:

- **devops**: For Cloud Run deployments and infrastructure management
- **developer**: For deploying applications during development
- **architect**: For service architecture decisions

## Troubleshooting

| Error               | Cause                   | Fix                                               |
| ------------------- | ----------------------- | ------------------------------------------------- |
| "Permission denied" | Missing GCP credentials | Run `gcloud auth application-default login`       |
| "Project not found" | Invalid project ID      | Verify project ID with `gcloud projects list`     |
| "Region not found"  | Invalid region          | Use valid Cloud Run regions (e.g., `us-central1`) |
| "Service not found" | Service doesn't exist   | Check service name with `list-services`           |
