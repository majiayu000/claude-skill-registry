---
name: n8n API Integration
description: Programmatic n8n control - REST API, workflow management, executions, credentials, automation
allowed-tools: Read, Write, Edit, WebFetch, Bash
---

# n8n API Integration

Programmatic control of n8n via REST API.

## Authentication

### API Key Setup
1. Settings → API → Create API Key
2. Store key securely (shown once)

### Request Headers
```bash
curl -X GET "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: your-api-key"
```

### Base URL
- Self-hosted: `http://localhost:5678/api/v1`
- Cloud: `https://your-instance.n8n.cloud/api/v1`

## Workflow Management

### List All Workflows
```bash
GET /api/v1/workflows

# Response
{
  "data": [
    {
      "id": "1",
      "name": "My Workflow",
      "active": true,
      "createdAt": "2024-01-01T00:00:00.000Z",
      "updatedAt": "2024-01-02T00:00:00.000Z"
    }
  ]
}
```

### Get Workflow by ID
```bash
GET /api/v1/workflows/{id}

# Response includes full workflow definition
{
  "id": "1",
  "name": "My Workflow",
  "active": true,
  "nodes": [...],
  "connections": {...},
  "settings": {...}
}
```

### Create Workflow
```bash
POST /api/v1/workflows
Content-Type: application/json

{
  "name": "New Workflow",
  "nodes": [
    {
      "id": "uuid",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [250, 300],
      "parameters": {}
    },
    {
      "id": "uuid2",
      "name": "Set",
      "type": "n8n-nodes-base.set",
      "position": [450, 300],
      "parameters": {
        "values": {
          "string": [{"name": "message", "value": "Hello"}]
        }
      }
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [[{"node": "Set", "type": "main", "index": 0}]]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

### Update Workflow
```bash
PATCH /api/v1/workflows/{id}
Content-Type: application/json

{
  "name": "Updated Name",
  "active": true,
  "nodes": [...],
  "connections": {...}
}
```

### Delete Workflow
```bash
DELETE /api/v1/workflows/{id}
```

### Activate/Deactivate Workflow
```bash
PATCH /api/v1/workflows/{id}
Content-Type: application/json

{"active": true}   # Activate
{"active": false}  # Deactivate
```

## Execution Management

### Execute Workflow
```bash
POST /api/v1/workflows/{id}/execute

# With input data
{
  "data": {
    "email": "user@example.com",
    "name": "John"
  }
}

# Response
{
  "data": {
    "executionId": "123",
    "finished": true,
    "mode": "manual",
    "startedAt": "2024-01-01T12:00:00.000Z",
    "stoppedAt": "2024-01-01T12:00:01.000Z",
    "data": {
      "resultData": {...}
    }
  }
}
```

### List Executions
```bash
GET /api/v1/executions

# Query parameters
?workflowId=1           # Filter by workflow
&status=success         # success, error, waiting
&limit=20               # Results per page
&cursor=abc123          # Pagination cursor
```

### Get Execution Details
```bash
GET /api/v1/executions/{id}

# Response includes full execution data
{
  "id": "123",
  "finished": true,
  "mode": "webhook",
  "data": {
    "startData": {...},
    "resultData": {
      "runData": {...}
    }
  }
}
```

### Delete Execution
```bash
DELETE /api/v1/executions/{id}
```

### Retry Execution
```bash
POST /api/v1/executions/{id}/retry
```

## Credentials

### List Credentials
```bash
GET /api/v1/credentials

# Response
{
  "data": [
    {
      "id": "1",
      "name": "My API Key",
      "type": "httpHeaderAuth",
      "createdAt": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

### Create Credential
```bash
POST /api/v1/credentials
Content-Type: application/json

{
  "name": "Slack OAuth",
  "type": "slackOAuth2Api",
  "data": {
    "clientId": "xxx",
    "clientSecret": "xxx"
  }
}
```

### Get Credential Schema
```bash
GET /api/v1/credentials/schema/{credentialType}

# Returns required fields for credential type
```

### Delete Credential
```bash
DELETE /api/v1/credentials/{id}
```

## Tags

### List Tags
```bash
GET /api/v1/tags
```

### Create Tag
```bash
POST /api/v1/tags
Content-Type: application/json

{"name": "production"}
```

### Update Tag
```bash
PATCH /api/v1/tags/{id}
Content-Type: application/json

{"name": "production-v2"}
```

### Tag a Workflow
```bash
PATCH /api/v1/workflows/{id}
Content-Type: application/json

{
  "tags": [
    {"id": "1"},
    {"id": "2"}
  ]
}
```

## Users (Enterprise)

### List Users
```bash
GET /api/v1/users
```

### Create User
```bash
POST /api/v1/users
Content-Type: application/json

{
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "role": "member"
}
```

### Update User Role
```bash
PATCH /api/v1/users/{id}/role
Content-Type: application/json

{"newRole": "admin"}
```

## Code Examples

### JavaScript/Node.js
```javascript
const N8N_URL = 'http://localhost:5678/api/v1';
const API_KEY = process.env.N8N_API_KEY;

async function executeWorkflow(workflowId, inputData) {
  const response = await fetch(`${N8N_URL}/workflows/${workflowId}/execute`, {
    method: 'POST',
    headers: {
      'X-N8N-API-KEY': API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ data: inputData })
  });

  if (!response.ok) {
    throw new Error(`Execution failed: ${response.status}`);
  }

  return response.json();
}

// Usage
const result = await executeWorkflow('workflow-id', {
  email: 'user@example.com',
  action: 'notify'
});
console.log('Execution ID:', result.data.executionId);
```

### Python
```python
import requests
import os

N8N_URL = "http://localhost:5678/api/v1"
API_KEY = os.environ["N8N_API_KEY"]

def execute_workflow(workflow_id: str, input_data: dict) -> dict:
    headers = {
        "X-N8N-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{N8N_URL}/workflows/{workflow_id}/execute",
        headers=headers,
        json={"data": input_data}
    )
    response.raise_for_status()
    return response.json()

def list_workflows() -> list:
    headers = {"X-N8N-API-KEY": API_KEY}
    response = requests.get(f"{N8N_URL}/workflows", headers=headers)
    response.raise_for_status()
    return response.json()["data"]

# Usage
workflows = list_workflows()
result = execute_workflow("workflow-id", {"user": "test"})
```

### cURL Scripts
```bash
#!/bin/bash
N8N_URL="http://localhost:5678/api/v1"
API_KEY="your-api-key"

# List workflows
list_workflows() {
  curl -s -X GET "${N8N_URL}/workflows" \
    -H "X-N8N-API-KEY: ${API_KEY}" | jq '.data[] | {id, name, active}'
}

# Execute workflow
execute_workflow() {
  local workflow_id=$1
  local data=$2

  curl -s -X POST "${N8N_URL}/workflows/${workflow_id}/execute" \
    -H "X-N8N-API-KEY: ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d "${data}"
}

# Activate workflow
activate_workflow() {
  local workflow_id=$1
  curl -s -X PATCH "${N8N_URL}/workflows/${workflow_id}" \
    -H "X-N8N-API-KEY: ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d '{"active": true}'
}

# Example usage
execute_workflow "abc123" '{"data": {"email": "test@example.com"}}'
```

## Integration Patterns

### CI/CD Integration
```yaml
# GitHub Actions example
name: Deploy n8n Workflows

on:
  push:
    branches: [main]
    paths: ['workflows/*.json']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy Workflows
        env:
          N8N_API_KEY: ${{ secrets.N8N_API_KEY }}
          N8N_URL: ${{ secrets.N8N_URL }}
        run: |
          for file in workflows/*.json; do
            workflow_id=$(jq -r '.id' "$file")
            if [ "$workflow_id" != "null" ]; then
              # Update existing
              curl -X PATCH "${N8N_URL}/api/v1/workflows/${workflow_id}" \
                -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
                -H "Content-Type: application/json" \
                -d @"$file"
            else
              # Create new
              curl -X POST "${N8N_URL}/api/v1/workflows" \
                -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
                -H "Content-Type: application/json" \
                -d @"$file"
            fi
          done
```

### Webhook Relay
```javascript
// Express.js relay to n8n webhook
const express = require('express');
const app = express();

app.post('/relay/:workflowId', async (req, res) => {
  const { workflowId } = req.params;

  // Execute via API instead of webhook
  const result = await executeWorkflow(workflowId, req.body);
  res.json(result);
});
```

### Monitoring Integration
```javascript
// Check workflow health
async function checkWorkflowHealth() {
  const workflows = await listWorkflows();
  const active = workflows.filter(w => w.active);

  // Check recent executions
  for (const workflow of active) {
    const executions = await fetch(
      `${N8N_URL}/executions?workflowId=${workflow.id}&limit=1`,
      { headers: { 'X-N8N-API-KEY': API_KEY } }
    ).then(r => r.json());

    const lastExec = executions.data[0];
    if (lastExec?.status === 'error') {
      // Alert on failure
      console.error(`Workflow ${workflow.name} failed`);
    }
  }
}
```

## Error Handling

### Common Errors
| Code | Meaning | Solution |
|------|---------|----------|
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Check workflow/execution ID |
| 422 | Validation Error | Check request body |
| 500 | Server Error | Check n8n logs |

### Retry Logic
```javascript
async function executeWithRetry(workflowId, data, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await executeWorkflow(workflowId, data);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
}
```

## Output Format
```
API CALL:
  Method: [GET/POST/PATCH/DELETE]
  Endpoint: /api/v1/[path]
  Headers: X-N8N-API-KEY: [key]
  Body: [JSON if applicable]

RESPONSE:
  Status: [200/201/etc]
  Body: [JSON response]

CODE EXAMPLE:
  [Language-specific implementation]
```
