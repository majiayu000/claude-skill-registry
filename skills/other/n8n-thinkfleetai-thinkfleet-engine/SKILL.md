---
name: n8n
description: "Manage n8n workflows — list, execute, activate/deactivate, and monitor executions via the n8n REST API."
metadata: {"thinkfleetbot":{"emoji":"⚡","requires":{"bins":["curl","jq"],"env":["N8N_API_URL","N8N_API_KEY"]}}}
---

# n8n Workflow Management

Manage your n8n automation platform: list workflows, trigger executions, check status, and activate/deactivate workflows.

## Setup

Set these environment variables:

```bash
N8N_API_URL="https://your-n8n-instance.com"   # Base URL (no trailing slash)
N8N_API_KEY="your-api-key-here"                # Settings → API → Create API Key
```

## List all workflows

```bash
curl -s "$N8N_API_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq '.data[] | {id, name, active}'
```

## Get workflow details

```bash
curl -s "$N8N_API_URL/api/v1/workflows/{WORKFLOW_ID}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq .
```

## Execute a workflow

```bash
curl -s -X POST "$N8N_API_URL/api/v1/workflows/{WORKFLOW_ID}/execute" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' | jq .
```

With input data:

```bash
curl -s -X POST "$N8N_API_URL/api/v1/workflows/{WORKFLOW_ID}/execute" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": {"key": "value"}}' | jq .
```

## Activate a workflow

```bash
curl -s -X PATCH "$N8N_API_URL/api/v1/workflows/{WORKFLOW_ID}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": true}' | jq .
```

## Deactivate a workflow

```bash
curl -s -X PATCH "$N8N_API_URL/api/v1/workflows/{WORKFLOW_ID}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": false}' | jq .
```

## List executions

```bash
curl -s "$N8N_API_URL/api/v1/executions" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq '.data[] | {id, workflowId, status, startedAt, stoppedAt}'
```

Filter by workflow:

```bash
curl -s "$N8N_API_URL/api/v1/executions?workflowId={WORKFLOW_ID}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq '.data[] | {id, status, startedAt}'
```

## Get execution details

```bash
curl -s "$N8N_API_URL/api/v1/executions/{EXECUTION_ID}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" | jq .
```

## Trigger via webhook

If a workflow has a Webhook trigger node, call its URL directly:

```bash
curl -s -X POST "https://your-n8n-instance.com/webhook/{WEBHOOK_PATH}" \
  -H "Content-Type: application/json" \
  -d '{"event": "deploy", "status": "success"}'
```

## Notes

- Replace `{WORKFLOW_ID}`, `{EXECUTION_ID}`, and `{WEBHOOK_PATH}` with actual values.
- Always list workflows first to find the correct ID before executing.
- Webhook URLs are separate from the API — they use the path configured in the Webhook node.
- n8n API uses pagination. Add `?limit=100&cursor=...` for large result sets.
- Be cautious activating workflows that have external triggers — they start listening immediately.
