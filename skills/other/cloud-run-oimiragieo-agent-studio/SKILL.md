---
name: cloud-run
description: Google Cloud Run deployment, service management, traffic splitting, and log inspection. Use when deploying containerized apps to Cloud Run, managing services, or inspecting Cloud Run logs.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash, Grep]
agents: [devops, cloud-devops-expert]
category: deployment
tags: [gcloud, cloud-run, gcp, containers, serverless, deployment]
best_practices:
  - Always specify --region for all gcloud run commands
  - Use --allow-unauthenticated only for public services
  - Set memory and CPU limits explicitly
  - Use Cloud Build for production container builds
error_handling: graceful
streaming: supported
verified: false
---

# Cloud Run

Deploy and manage containerized applications on Google Cloud Run. Covers service deployment, revision management, traffic splitting, and log inspection.

## When to Use

- Deploying containerized web applications or APIs to Google Cloud
- Managing Cloud Run services (scaling, traffic, revisions)
- Setting up serverless container deployments
- Inspecting Cloud Run service logs and metrics
- Configuring environment variables and secrets for Cloud Run services

## Prerequisites

- Google Cloud SDK (`gcloud`) installed and authenticated
- Docker or Cloud Build for container image building
- A GCP project with Cloud Run API enabled

## Core Commands

### Deploy a Service

```bash
# Deploy from source (Cloud Build auto-builds)
gcloud run deploy SERVICE_NAME \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

# Deploy from container image
gcloud run deploy SERVICE_NAME \
  --image gcr.io/PROJECT_ID/IMAGE:TAG \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10
```

### List Services

```bash
gcloud run services list --region us-central1 --format json
```

### Get Service Details

```bash
gcloud run services describe SERVICE_NAME \
  --region us-central1 \
  --format json
```

### View Logs

```bash
gcloud run services logs read SERVICE_NAME \
  --region us-central1 \
  --limit 100

# Tail logs in real-time
gcloud run services logs tail SERVICE_NAME \
  --region us-central1
```

### Traffic Splitting

```bash
# Route 50% to latest, 50% to previous revision
gcloud run services update-traffic SERVICE_NAME \
  --region us-central1 \
  --to-revisions LATEST=50,REVISION_NAME=50

# Route all traffic to latest
gcloud run services update-traffic SERVICE_NAME \
  --region us-central1 \
  --to-latest
```

### Environment Variables and Secrets

```bash
# Set env vars
gcloud run services update SERVICE_NAME \
  --region us-central1 \
  --set-env-vars KEY1=VALUE1,KEY2=VALUE2

# Mount secret as env var
gcloud run services update SERVICE_NAME \
  --region us-central1 \
  --set-secrets ENV_NAME=SECRET_NAME:latest
```

### Delete a Service

```bash
gcloud run services delete SERVICE_NAME \
  --region us-central1 \
  --quiet
```

## Workflow

### Step 1: Prepare Container

Either use a Dockerfile or let Cloud Build auto-detect:

```bash
# Option A: Build and push manually
docker build -t gcr.io/PROJECT_ID/SERVICE_NAME:latest .
docker push gcr.io/PROJECT_ID/SERVICE_NAME:latest

# Option B: Deploy from source (Cloud Build handles it)
gcloud run deploy SERVICE_NAME --source .
```

### Step 2: Deploy

```bash
gcloud run deploy SERVICE_NAME \
  --image gcr.io/PROJECT_ID/SERVICE_NAME:latest \
  --region us-central1 \
  --port 8080 \
  --memory 512Mi \
  --cpu 1
```

### Step 3: Verify

```bash
# Get service URL
gcloud run services describe SERVICE_NAME \
  --region us-central1 \
  --format "value(status.url)"

# Test the endpoint
curl $(gcloud run services describe SERVICE_NAME \
  --region us-central1 \
  --format "value(status.url)")
```

### Step 4: Monitor

```bash
gcloud run services logs read SERVICE_NAME --region us-central1 --limit 20
```

## Iron Laws

1. **ALWAYS specify --region** for all `gcloud run` commands — omitting region causes interactive prompts that break automation.
2. **NEVER use --allow-unauthenticated** for internal services — use IAM-based authentication for service-to-service communication.
3. **ALWAYS set memory and CPU limits explicitly** — default limits may be too low for production workloads.
4. **NEVER store secrets in environment variables directly** — use Secret Manager with `--set-secrets` flag.
5. **ALWAYS test deployments with traffic splitting** before routing 100% to a new revision.

## Anti-Patterns

| Anti-Pattern                          | Why It Fails                      | Correct Approach                                       |
| ------------------------------------- | --------------------------------- | ------------------------------------------------------ |
| Missing --region flag                 | Interactive prompt breaks CI/CD   | Always specify region explicitly                       |
| Public endpoints for internal APIs    | Security exposure                 | Use IAM auth + Cloud Run invoker role                  |
| Hardcoded secrets in env vars         | Secrets visible in service config | Use Secret Manager integration                         |
| No min-instances for latency-critical | Cold start adds 2-10s latency     | Set --min-instances 1+ for critical paths              |
| Single revision (no traffic split)    | No rollback path                  | Always keep previous revision, split traffic gradually |

## MCP Tool Reference (cloud-run-mcp)

When the `cloud-run-mcp` MCP server is configured, these tools are available:

| Tool                   | Description                            | Key Params                         |
| ---------------------- | -------------------------------------- | ---------------------------------- |
| `deploy-file-contents` | Deploy code directly from file content | service_name, region, source_files |
| `list-services`        | List all Cloud Run services            | project_id, region                 |
| `get-service`          | Get service details + URL              | service_name, project_id, region   |
| `get-service-log`      | Fetch recent logs                      | service_name, project_id, limit    |
| `deploy-local-folder`  | Deploy from local directory            | folder_path, service_name, region  |
| `list-projects`        | List GCP projects                      | —                                  |
| `create-project`       | Create new GCP project                 | project_id, project_name           |

**MCP setup**: `npx @google-cloud/cloud-run-mcp` or configure in Claude Desktop settings.json
**Auth**: Application Default Credentials (`gcloud auth application-default login`)
**When to use MCP vs CLI**: Use MCP tools when user asks "deploy this code" or "what services are running"; use gcloud CLI for advanced operations (IAM, VPC, secrets).

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
