---
name: n8n
description: n8n workflow automation patterns and API integration. This skill should
  be used when creating n8n workflows, using webhooks, managing workflows via REST
  API, or integrating n8n with MCP servers. Covers workflow JSON structure, node patterns,
  and automation best practices.
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# n8n Workflow Automation Skill

This skill enables creating and managing n8n workflows for automation tasks.

## Prerequisites

n8n instance running with API access:

```bash
N8N_HOST=localhost
N8N_PORT=5678
N8N_API_KEY=your-api-key
```

## Core Concepts

### Workflow Structure

Every n8n workflow is JSON with this structure:

```json
{
  "name": "Workflow Name",
  "nodes": [],
  "connections": {},
  "settings": {
    "executionOrder": "v1"
  }
}
```

### Node Structure

Each node has:

```json
{
  "id": "unique-id",
  "name": "Display Name",
  "type": "n8n-nodes-base.nodetype",
  "typeVersion": 1,
  "position": [x, y],
  "parameters": {},
  "credentials": {}
}
```

### Connection Structure

Connections define data flow between nodes:

```json
{
  "Source Node": {
    "main": [
      [{"node": "Target Node", "type": "main", "index": 0}]
    ]
  }
}
```

## Common Workflow Patterns

### 1. Webhook-Triggered Workflow

Creates an HTTP endpoint that triggers workflow execution:

```json
{
  "name": "Webhook Handler",
  "nodes": [
    {
      "id": "webhook",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300],
      "webhookId": "my-webhook",
      "parameters": {
        "path": "my-endpoint",
        "httpMethod": "POST",
        "responseMode": "responseNode"
      }
    },
    {
      "id": "respond",
      "name": "Respond",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [450, 300],
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $json }}"
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{"node": "Respond", "type": "main", "index": 0}]]
    }
  }
}
```

Access at: `http://localhost:5678/webhook/my-endpoint`

### 2. HTTP Request Pattern

Make external API calls:

```json
{
  "id": "http",
  "name": "HTTP Request",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [450, 300],
  "parameters": {
    "method": "POST",
    "url": "https://api.example.com/endpoint",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "myApiCredential",
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify($json) }}"
  },
  "credentials": {
    "myApiCredential": {"id": "cred-id", "name": "My Credential"}
  }
}
```

### 3. Conditional Branching (IF Node)

Route data based on conditions:

```json
{
  "id": "if",
  "name": "IF",
  "type": "n8n-nodes-base.if",
  "typeVersion": 2,
  "position": [450, 300],
  "parameters": {
    "conditions": {
      "options": {
        "caseSensitive": true,
        "leftValue": "",
        "typeValidation": "strict"
      },
      "conditions": [
        {
          "leftValue": "={{ $json.status }}",
          "rightValue": "success",
          "operator": {
            "type": "string",
            "operation": "equals"
          }
        }
      ],
      "combinator": "and"
    }
  }
}
```

### 4. Loop Over Items (SplitInBatches)

Process items in batches:

```json
{
  "id": "batch",
  "name": "Loop Over Items",
  "type": "n8n-nodes-base.splitInBatches",
  "typeVersion": 3,
  "position": [450, 300],
  "parameters": {
    "batchSize": 10,
    "options": {}
  }
}
```

## n8n REST API

### List Workflows

```bash
curl -s "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

### Get Workflow

```bash
curl -s "http://localhost:5678/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

### Create Workflow

```bash
curl -s -X POST "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Workflow", "nodes": [...], "connections": {...}}'
```

### Update Workflow

```bash
curl -s -X PUT "http://localhost:5678/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated", "nodes": [...], "connections": {...}}'
```

### Activate/Deactivate

```bash
curl -s -X POST "http://localhost:5678/api/v1/workflows/{id}/activate" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"

curl -s -X POST "http://localhost:5678/api/v1/workflows/{id}/deactivate" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

### Get Executions

```bash
curl -s "http://localhost:5678/api/v1/executions?workflowId={id}&limit=10&includeData=true" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

## Expression Syntax

n8n uses expressions for dynamic values:

| Syntax | Description |
|--------|-------------|
| `={{ $json.field }}` | Access current item field |
| `={{ $json.body.param }}` | Access nested field |
| `={{ $('Node Name').item.json.field }}` | Access output from specific node |
| `={{ $input.first().json }}` | First input item |
| `={{ $input.all() }}` | All input items |
| `={{ JSON.stringify($json) }}` | Convert to JSON string |

## Common Node Types

| Node | Type | Purpose |
|------|------|---------|
| Webhook | `n8n-nodes-base.webhook` | HTTP trigger |
| HTTP Request | `n8n-nodes-base.httpRequest` | API calls |
| Respond to Webhook | `n8n-nodes-base.respondToWebhook` | Return HTTP response |
| IF | `n8n-nodes-base.if` | Conditional branching |
| Switch | `n8n-nodes-base.switch` | Multi-way branching |
| Set | `n8n-nodes-base.set` | Transform data |
| Code | `n8n-nodes-base.code` | Custom JavaScript |
| Split In Batches | `n8n-nodes-base.splitInBatches` | Loop processing |
| Merge | `n8n-nodes-base.merge` | Combine branches |

## MCP Integration

n8n can expose workflows as MCP tools via the built-in MCP server:

1. Enable MCP in workflow settings: `"availableInMCP": true`
2. Access MCP endpoint: `http://localhost:5678/mcp-server/http`
3. Use supergateway for Claude Code integration

## Tips

1. **Webhook Response**: Use `responseMode: "responseNode"` with Respond node for control
2. **Credentials**: Store API keys in n8n credentials, reference by ID
3. **Error Handling**: Add Error Trigger node for failure notifications
4. **Testing**: Use `/webhook-test/` path during development
5. **ADF Format**: Jira/Confluence require Atlassian Document Format for rich text
