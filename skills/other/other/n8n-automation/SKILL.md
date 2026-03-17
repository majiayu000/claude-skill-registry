---
name: n8n-automation
description: Complete n8n workflow automation skill - build, optimize, deploy, and manage n8n workflows. Covers workflow JSON structure, node configuration, expressions, triggers, integrations, Docker/cloud deployment, queue mode scaling, CLI operations, REST API, error handling, and best practices. Use when building automation workflows, setting up n8n instances, optimizing performance, or integrating services. (project)
---

# n8n Workflow Automation - Complete Management & Development

The ultimate comprehensive skill for n8n workflow automation platform covering:
- **Workflow Building**: Create, import, export, and manage workflows programmatically
- **Node Configuration**: 400+ integrations including HTTP, webhooks, code, AI/LLM nodes
- **Expressions & Data**: Master $json, $input, $items, and transformation functions
- **Deployment**: Docker, npm, cloud, queue mode with Redis/PostgreSQL
- **Optimization**: Performance tuning, batch processing, error handling
- **CLI & API**: Automate n8n operations via command line and REST API

## Session Configuration

**CRITICAL: Connection Setup**

When the user first requests an n8n operation, determine the access method:

```
I need n8n connection details. Please provide what applies:

**For Self-Hosted n8n:**
1. **n8n URL**: (e.g., http://localhost:5678 or https://n8n.example.com)
2. **API Key**: (Settings > API > Create API Key)
3. **SSH/File Access**: For direct workflow file manipulation

**For n8n Cloud:**
1. **Instance URL**: (e.g., https://your-instance.app.n8n.cloud)
2. **API Key**: (Settings > API > Create API Key)

**For Local Development:**
1. **Installation Type**: Docker or npm
2. **Data Directory**: (e.g., ~/.n8n or Docker volume path)

Example response:
- URL: http://localhost:5678
- API Key: n8n_api_xxxxxxxxxxxxx
```

After receiving details:
- Store them in working memory for the session
- Use for ALL subsequent n8n operations without re-prompting
- NEVER write API keys to files or logs

---

## Quick Reference

### n8n Architecture Overview

```
n8n Instance
├── Workflows           # Automation definitions (JSON)
│   ├── Nodes          # Individual operations
│   ├── Connections    # Data flow between nodes
│   └── Settings       # Execution config, timezone
├── Credentials        # Encrypted service auth
├── Executions         # Workflow run history
├── Variables          # Global variables
└── Tags               # Organization labels
```

### Workflow JSON Structure

```json
{
  "id": "workflow-uuid",
  "name": "My Workflow",
  "active": true,
  "nodes": [
    {
      "id": "node-uuid",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300],
      "parameters": {
        "httpMethod": "POST",
        "path": "my-webhook",
        "responseMode": "responseNode"
      },
      "webhookId": "webhook-uuid"
    },
    {
      "id": "node-uuid-2",
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [450, 300],
      "parameters": {
        "url": "https://api.example.com/data",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "data",
              "value": "={{ $json.body }}"
            }
          ]
        }
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "HTTP Request",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1",
    "timezone": "America/New_York",
    "saveManualExecutions": true,
    "callerPolicy": "workflowsFromSameOwner"
  },
  "staticData": null,
  "pinData": {},
  "versionId": "version-uuid",
  "triggerCount": 1
}
```

### Node Structure Requirements

Each node MUST include:
- `id`: Unique identifier (UUID format)
- `name`: Display name in workflow
- `type`: Node type (e.g., `n8n-nodes-base.webhook`)
- `typeVersion`: Version number (integer)
- `position`: [x, y] coordinates for UI placement
- `parameters`: Node-specific configuration object

### Connection Schema

```json
{
  "connections": {
    "SourceNodeName": {
      "main": [
        [
          { "node": "TargetNodeName", "type": "main", "index": 0 }
        ]
      ]
    }
  }
}
```

- `main` array contains output branches
- Multiple outputs (like IF node) have multiple inner arrays
- `index` specifies which input of target node to connect to

---

## Installation & Deployment

### Docker Installation (Recommended)

**Basic Setup:**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

**Docker Compose - Development:**
```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=securepassword
      - N8N_ENCRYPTION_KEY=your-32-char-encryption-key
      - GENERIC_TIMEZONE=America/New_York
      - TZ=America/New_York
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

**Docker Compose - Production with PostgreSQL & Redis (Queue Mode):**
```yaml

x-shared: &shared
  restart: unless-stopped
  image: docker.n8n.io/n8nio/n8n
  environment:
    - DB_TYPE=postgresdb
    - DB_POSTGRESDB_HOST=postgres
    - DB_POSTGRESDB_PORT=5432
    - DB_POSTGRESDB_DATABASE=n8n
    - DB_POSTGRESDB_USER=n8n
    - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
    - N8N_ENCRYPTION_KEY=${ENCRYPTION_KEY}
    - EXECUTIONS_MODE=queue
    - QUEUE_BULL_REDIS_HOST=redis
    - QUEUE_HEALTH_CHECK_ACTIVE=true
    - N8N_PROTOCOL=https
    - N8N_HOST=${N8N_HOST}
    - WEBHOOK_URL=https://${N8N_HOST}/
    - GENERIC_TIMEZONE=America/New_York
  depends_on:
    postgres:
      condition: service_healthy
    redis:
      condition: service_healthy

services:
  postgres:
    image: postgres:16
    restart: unless-stopped
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U n8n"]
      interval: 5s
      timeout: 5s
      retries: 10

  redis:
    image: redis:6-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 10

  n8n:
    <<: *shared
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n

  n8n-worker:
    <<: *shared
    command: worker
    depends_on:
      - n8n

volumes:
  postgres_data:
  redis_data:
  n8n_data:
```

### npm Installation

```bash
# Install globally
npm install n8n -g

# Start n8n
n8n start

# Start with tunnel (development)
n8n start --tunnel

# Start with specific port
n8n start --port 5678
```

### Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `N8N_ENCRYPTION_KEY` | 32-char key for credential encryption | Required |
| `N8N_BASIC_AUTH_ACTIVE` | Enable basic auth | false |
| `N8N_HOST` | Public hostname | localhost |
| `N8N_PORT` | HTTP port | 5678 |
| `N8N_PROTOCOL` | http or https | http |
| `WEBHOOK_URL` | External webhook URL | - |
| `DB_TYPE` | Database: sqlite, postgresdb, mysqldb | sqlite |
| `EXECUTIONS_MODE` | regular or queue | regular |
| `GENERIC_TIMEZONE` | Default timezone | America/New_York |
| `N8N_LOG_LEVEL` | debug, info, warn, error | info |
| `N8N_METRICS` | Enable Prometheus metrics | false |
| `N8N_DIAGNOSTICS_ENABLED` | Send anonymous telemetry | true |

---

## Expressions & Data Access

### Built-in Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `$json` | Current item's JSON data | `{{ $json.email }}` |
| `$input` | Input data object | `{{ $input.first().json.name }}` |
| `$items()` | All items from a node | `{{ $items('NodeName') }}` |
| `$node` | Access other nodes' data | `{{ $node['NodeName'].json.id }}` |
| `$workflow` | Workflow metadata | `{{ $workflow.name }}` |
| `$execution` | Current execution info | `{{ $execution.id }}` |
| `$now` | Current datetime (Luxon) | `{{ $now.toISO() }}` |
| `$today` | Today's date (Luxon) | `{{ $today.toFormat('yyyy-MM-dd') }}` |
| `$vars` | Global variables | `{{ $vars.apiKey }}` |
| `$env` | Environment variables | `{{ $env.MY_VAR }}` |
| `$runIndex` | Current run index in loop | `{{ $runIndex }}` |
| `$itemIndex` | Current item index | `{{ $itemIndex }}` |

### Expression Syntax

**Basic Access:**
```javascript
// Dot notation
{{ $json.user.name }}

// Bracket notation (for special characters)
{{ $json['user-name'] }}
{{ $json['nested']['field'] }}

// Array access
{{ $json.items[0].id }}
{{ $json.users[$itemIndex].email }}
```

**Conditional Logic:**
```javascript
// Ternary operator
{{ $json.status === 'active' ? 'Yes' : 'No' }}

// Null coalescing (fallback values)
{{ $json.email || 'no-email@example.com' }}
{{ $json.count || 0 }}

// Optional chaining
{{ $json.user?.address?.city }}
```

**Transformations:**
```javascript
// String methods
{{ $json.name.toUpperCase() }}
{{ $json.email.split('@')[0] }}
{{ $json.text.trim().substring(0, 100) }}

// Array methods
{{ $json.items.length }}
{{ $json.items.map(i => i.name).join(', ') }}
{{ $json.items.filter(i => i.active) }}

// JSON operations
{{ JSON.stringify($json) }}
{{ JSON.parse($json.data) }}
```

**Date/Time (Luxon):**
```javascript
// Current time
{{ $now.toISO() }}
{{ $now.toFormat('yyyy-MM-dd HH:mm:ss') }}

// Date math
{{ $now.plus({ days: 7 }).toISO() }}
{{ $now.minus({ hours: 2 }).toFormat('HH:mm') }}

// Parse dates
{{ DateTime.fromISO($json.date).toFormat('MMMM d, yyyy') }}
{{ DateTime.fromMillis($json.timestamp).toISO() }}
```

**IIFE for Complex Logic:**
```javascript
{{
  (() => {
    const items = $json.data || [];
    const filtered = items.filter(i => i.status === 'active');
    return filtered.length;
  })()
}}
```

---

## Core Nodes Reference

### Trigger Nodes

**Webhook Trigger:**
```json
{
  "name": "Webhook",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2,
  "parameters": {
    "httpMethod": "POST",
    "path": "my-endpoint",
    "responseMode": "responseNode",
    "options": {
      "allowedOrigins": "*"
    }
  }
}
```

**Schedule Trigger (Cron):**
```json
{
  "name": "Schedule Trigger",
  "type": "n8n-nodes-base.scheduleTrigger",
  "typeVersion": 1.2,
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "cronExpression",
          "expression": "0 9 * * 1-5"
        }
      ]
    }
  }
}
```

**Manual Trigger:**
```json
{
  "name": "Manual Trigger",
  "type": "n8n-nodes-base.manualTrigger",
  "typeVersion": 1,
  "parameters": {}
}
```

### HTTP & API Nodes

**HTTP Request:**
```json
{
  "name": "HTTP Request",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "parameters": {
    "url": "https://api.example.com/data",
    "method": "POST",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        { "name": "Content-Type", "value": "application/json" }
      ]
    },
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify($json) }}",
    "options": {
      "timeout": 30000,
      "retry": {
        "enabled": true,
        "maxTries": 3,
        "waitBetweenTries": 1000
      }
    }
  }
}
```

**Respond to Webhook:**
```json
{
  "name": "Respond to Webhook",
  "type": "n8n-nodes-base.respondToWebhook",
  "typeVersion": 1.1,
  "parameters": {
    "respondWith": "json",
    "responseBody": "={{ { success: true, data: $json } }}",
    "options": {
      "responseCode": 200,
      "responseHeaders": {
        "entries": [
          { "name": "X-Custom-Header", "value": "value" }
        ]
      }
    }
  }
}
```

### Data Transformation Nodes

**Code Node (JavaScript):**
```json
{
  "name": "Code",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "parameters": {
    "mode": "runOnceForAllItems",
    "jsCode": "// Access all input items\nconst items = $input.all();\n\n// Transform data\nconst results = items.map(item => {\n  return {\n    json: {\n      id: item.json.id,\n      name: item.json.name.toUpperCase(),\n      processed: true,\n      timestamp: new Date().toISOString()\n    }\n  };\n});\n\nreturn results;"
  }
}
```

**Code Node (Python):**
```json
{
  "name": "Python Code",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "parameters": {
    "mode": "runOnceForAllItems",
    "language": "python",
    "pythonCode": "import json\nfrom datetime import datetime\n\nresults = []\nfor item in _input.all():\n    data = item.json\n    results.append({\n        'json': {\n            'id': data.get('id'),\n            'name': data.get('name', '').upper(),\n            'processed': True,\n            'timestamp': datetime.now().isoformat()\n        }\n    })\n\nreturn results"
  }
}
```

**Set Node (Edit Fields):**
```json
{
  "name": "Set",
  "type": "n8n-nodes-base.set",
  "typeVersion": 3.4,
  "parameters": {
    "mode": "manual",
    "duplicateItem": false,
    "assignments": {
      "assignments": [
        {
          "id": "uuid",
          "name": "fullName",
          "value": "={{ $json.firstName }} {{ $json.lastName }}",
          "type": "string"
        },
        {
          "id": "uuid-2",
          "name": "isActive",
          "value": true,
          "type": "boolean"
        }
      ]
    },
    "includeOtherFields": true
  }
}
```

### Flow Control Nodes

**IF Node (Conditional):**
```json
{
  "name": "IF",
  "type": "n8n-nodes-base.if",
  "typeVersion": 2.2,
  "parameters": {
    "conditions": {
      "options": {
        "leftValue": "",
        "caseSensitive": true,
        "typeValidation": "strict"
      },
      "combinator": "and",
      "conditions": [
        {
          "id": "uuid",
          "leftValue": "={{ $json.status }}",
          "rightValue": "active",
          "operator": {
            "type": "string",
            "operation": "equals"
          }
        }
      ]
    }
  }
}
```

**Switch Node:**
```json
{
  "name": "Switch",
  "type": "n8n-nodes-base.switch",
  "typeVersion": 3.2,
  "parameters": {
    "mode": "rules",
    "rules": {
      "values": [
        {
          "outputKey": "premium",
          "conditions": {
            "combinator": "and",
            "conditions": [
              {
                "leftValue": "={{ $json.tier }}",
                "rightValue": "premium",
                "operator": { "type": "string", "operation": "equals" }
              }
            ]
          }
        },
        {
          "outputKey": "standard",
          "conditions": {
            "combinator": "and",
            "conditions": [
              {
                "leftValue": "={{ $json.tier }}",
                "rightValue": "standard",
                "operator": { "type": "string", "operation": "equals" }
              }
            ]
          }
        }
      ],
      "fallbackOutput": "extra"
    }
  }
}
```

**Loop Over Items:**
```json
{
  "name": "Loop Over Items",
  "type": "n8n-nodes-base.splitInBatches",
  "typeVersion": 3,
  "parameters": {
    "batchSize": 10,
    "options": {
      "reset": false
    }
  }
}
```

**Merge Node:**
```json
{
  "name": "Merge",
  "type": "n8n-nodes-base.merge",
  "typeVersion": 3,
  "parameters": {
    "mode": "combine",
    "combineBy": "combineByPosition",
    "options": {}
  }
}
```

### Error Handling

**Error Trigger:**
```json
{
  "name": "Error Trigger",
  "type": "n8n-nodes-base.errorTrigger",
  "typeVersion": 1,
  "parameters": {}
}
```

**Stop and Error:**
```json
{
  "name": "Stop and Error",
  "type": "n8n-nodes-base.stopAndError",
  "typeVersion": 1,
  "parameters": {
    "errorMessage": "Validation failed: {{ $json.error }}"
  }
}
```

---

## CLI Commands

### Workflow Operations

```bash
# Export all workflows
n8n export:workflow --all --output=./workflows/

# Export specific workflow
n8n export:workflow --id=<workflow-id> --output=./workflow.json

# Import workflow
n8n import:workflow --input=./workflow.json

# Import all workflows from directory
n8n import:workflow --input=./workflows/ --separate

# Execute workflow
n8n execute --id=<workflow-id>

# Execute with input data
n8n execute --id=<workflow-id> --rawInput='{"key": "value"}'
```

### Credential Operations

```bash
# Export all credentials (encrypted)
n8n export:credentials --all --output=./credentials/

# Export specific credential
n8n export:credentials --id=<credential-id> --output=./cred.json

# Import credentials
n8n import:credentials --input=./credentials/

# Decrypt credentials on export (requires encryption key)
n8n export:credentials --all --decrypted --output=./creds-plain/
```

### User Management

```bash
# Create owner user
n8n user-management:reset

# List users
n8n user-management:list

# Reset user password
n8n user-management:reset --email=user@example.com
```

### Database Operations

```bash
# Prune execution data
n8n prune:executions --days-to-keep=30

# Update database schema
n8n db:revert

# Check license
n8n license:info
```

---

## REST API

### Authentication

```bash
# Create API key in n8n: Settings > API > Create API Key
# Use header: X-N8N-API-KEY: your-api-key
```

### Workflow Endpoints

```bash
# List all workflows
curl -X GET "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: $API_KEY"

# Get specific workflow
curl -X GET "http://localhost:5678/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $API_KEY"

# Create workflow
curl -X POST "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d @workflow.json

# Update workflow
curl -X PATCH "http://localhost:5678/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"active": true}'

# Delete workflow
curl -X DELETE "http://localhost:5678/api/v1/workflows/{id}" \
  -H "X-N8N-API-KEY: $API_KEY"

# Activate workflow
curl -X POST "http://localhost:5678/api/v1/workflows/{id}/activate" \
  -H "X-N8N-API-KEY: $API_KEY"

# Deactivate workflow
curl -X POST "http://localhost:5678/api/v1/workflows/{id}/deactivate" \
  -H "X-N8N-API-KEY: $API_KEY"
```

### Execution Endpoints

```bash
# List executions
curl -X GET "http://localhost:5678/api/v1/executions?limit=20" \
  -H "X-N8N-API-KEY: $API_KEY"

# Get execution details
curl -X GET "http://localhost:5678/api/v1/executions/{id}" \
  -H "X-N8N-API-KEY: $API_KEY"

# Delete execution
curl -X DELETE "http://localhost:5678/api/v1/executions/{id}" \
  -H "X-N8N-API-KEY: $API_KEY"
```

### Credential Endpoints

```bash
# List credentials
curl -X GET "http://localhost:5678/api/v1/credentials" \
  -H "X-N8N-API-KEY: $API_KEY"

# Create credential
curl -X POST "http://localhost:5678/api/v1/credentials" \
  -H "X-N8N-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My API Key",
    "type": "httpHeaderAuth",
    "data": {
      "name": "Authorization",
      "value": "Bearer token123"
    }
  }'
```

---

## Common Workflow Patterns

### API Gateway Pattern

```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "httpMethod": "={{ $json.method }}",
        "path": "api/v1/:resource/:action",
        "responseMode": "responseNode"
      }
    },
    {
      "name": "Router",
      "type": "n8n-nodes-base.switch",
      "parameters": {
        "rules": {
          "values": [
            { "outputKey": "users", "conditions": { "conditions": [{ "leftValue": "={{ $json.params.resource }}", "rightValue": "users" }] } },
            { "outputKey": "orders", "conditions": { "conditions": [{ "leftValue": "={{ $json.params.resource }}", "rightValue": "orders" }] } }
          ]
        }
      }
    },
    {
      "name": "Response",
      "type": "n8n-nodes-base.respondToWebhook",
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $json }}"
      }
    }
  ]
}
```

### Retry with Exponential Backoff

```javascript
// Code node for retry logic
const maxRetries = 3;
const baseDelay = 1000;

async function fetchWithRetry(url, attempt = 1) {
  try {
    const response = await $http.request({
      method: 'GET',
      url: url,
      timeout: 10000
    });
    return response.data;
  } catch (error) {
    if (attempt >= maxRetries) throw error;
    const delay = baseDelay * Math.pow(2, attempt - 1);
    await new Promise(r => setTimeout(r, delay));
    return fetchWithRetry(url, attempt + 1);
  }
}

const result = await fetchWithRetry($json.url);
return [{ json: result }];
```

### Batch Processing Pattern

```javascript
// Code node for batch processing
const items = $input.all();
const batchSize = 50;
const results = [];

for (let i = 0; i < items.length; i += batchSize) {
  const batch = items.slice(i, i + batchSize);

  // Process batch
  const processed = batch.map(item => ({
    json: {
      ...item.json,
      batchIndex: Math.floor(i / batchSize),
      processedAt: new Date().toISOString()
    }
  }));

  results.push(...processed);

  // Rate limiting delay between batches
  if (i + batchSize < items.length) {
    await new Promise(r => setTimeout(r, 1000));
  }
}

return results;
```

### Parallel Execution Pattern

Use the Split In Batches node with parallel branches:

```json
{
  "nodes": [
    {
      "name": "Split In Batches",
      "type": "n8n-nodes-base.splitInBatches",
      "parameters": { "batchSize": 1 }
    },
    {
      "name": "HTTP Request 1",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": { "url": "https://api1.example.com/{{ $json.id }}" }
    },
    {
      "name": "HTTP Request 2",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": { "url": "https://api2.example.com/{{ $json.id }}" }
    },
    {
      "name": "Merge",
      "type": "n8n-nodes-base.merge",
      "parameters": { "mode": "combine" }
    }
  ],
  "connections": {
    "Split In Batches": {
      "main": [
        [{ "node": "HTTP Request 1" }, { "node": "HTTP Request 2" }]
      ]
    }
  }
}
```

---

## Error Handling Patterns

### Global Error Handler

Create a separate workflow with Error Trigger:

```json
{
  "name": "Global Error Handler",
  "nodes": [
    {
      "name": "Error Trigger",
      "type": "n8n-nodes-base.errorTrigger",
      "parameters": {}
    },
    {
      "name": "Format Error",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "return [{\n  json: {\n    workflow: $json.workflow.name,\n    node: $json.execution.lastNodeExecuted,\n    error: $json.execution.error.message,\n    timestamp: new Date().toISOString(),\n    executionId: $json.execution.id\n  }\n}];"
      }
    },
    {
      "name": "Slack Notification",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#errors",
        "text": ":x: Workflow Error\nWorkflow: {{ $json.workflow }}\nNode: {{ $json.node }}\nError: {{ $json.error }}"
      }
    }
  ]
}
```

### Try-Catch in Code Node

```javascript
try {
  const response = await $http.request({
    method: 'POST',
    url: $json.apiUrl,
    body: $json.payload
  });

  return [{
    json: {
      success: true,
      data: response.data
    }
  }];
} catch (error) {
  return [{
    json: {
      success: false,
      error: error.message,
      originalData: $json
    }
  }];
}
```

---

## Performance Optimization

### Best Practices

1. **Use Queue Mode for Heavy Workloads**
   - Separate main instance from workers
   - Scale workers horizontally
   - Use Redis for job queue

2. **Optimize Data Handling**
   - Limit returned fields with expressions
   - Use pagination for large datasets
   - Process items in batches

3. **Reduce Execution Time**
   - Enable HTTP request timeouts
   - Use caching for repeated requests
   - Parallelize independent operations

4. **Database Optimization**
   - Use PostgreSQL for production
   - Enable execution data pruning
   - Index frequently queried fields

### Memory Management

```javascript
// Avoid loading large arrays into memory
// BAD: Loading all items at once
const allItems = $input.all();

// GOOD: Process items in streaming fashion
for (const item of $input.all()) {
  // Process one at a time
  yield { json: processItem(item.json) };
}
```

### Execution Data Settings

```yaml
# In environment variables
EXECUTIONS_DATA_SAVE_ON_ERROR=all
EXECUTIONS_DATA_SAVE_ON_SUCCESS=none  # Reduce storage
EXECUTIONS_DATA_SAVE_ON_PROGRESS=false
EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS=true
EXECUTIONS_DATA_PRUNE=true
EXECUTIONS_DATA_MAX_AGE=168  # Hours (7 days)
```

---

## Security Best Practices

### Credential Management

1. **Use Credentials, Not Hardcoded Values**
   ```json
   {
     "parameters": {
       "authentication": "genericCredentialType",
       "genericAuthType": "httpHeaderAuth"
     },
     "credentials": {
       "httpHeaderAuth": { "id": "cred-id", "name": "API Key" }
     }
   }
   ```

2. **Environment Variables for Sensitive Config**
   ```javascript
   // Access in expressions
   {{ $env.API_SECRET }}
   ```

3. **Encrypt Credentials at Rest**
   - Always set `N8N_ENCRYPTION_KEY`
   - Use 32-character random string
   - Never commit to version control

### Webhook Security

```json
{
  "name": "Secure Webhook",
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "authentication": "headerAuth",
    "headerAuth": {
      "name": "X-Webhook-Secret",
      "value": "={{ $env.WEBHOOK_SECRET }}"
    },
    "options": {
      "allowedOrigins": "https://trusted-domain.com"
    }
  }
}
```

### IP Allowlisting

```yaml
# Environment variable
N8N_IP_ALLOW_LIST=10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```

---

## AI/LLM Integration

### OpenAI Node

```json
{
  "name": "OpenAI",
  "type": "@n8n/n8n-nodes-langchain.openAi",
  "typeVersion": 1.8,
  "parameters": {
    "resource": "chat",
    "model": "gpt-4o",
    "messages": {
      "values": [
        {
          "role": "system",
          "content": "You are a helpful assistant."
        },
        {
          "role": "user",
          "content": "={{ $json.prompt }}"
        }
      ]
    },
    "options": {
      "temperature": 0.7,
      "maxTokens": 1000
    }
  }
}
```

### AI Agent Pattern

```json
{
  "nodes": [
    {
      "name": "AI Agent",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "parameters": {
        "agent": "conversationalAgent",
        "options": {
          "systemMessage": "You are an automation assistant."
        }
      }
    },
    {
      "name": "HTTP Tool",
      "type": "@n8n/n8n-nodes-langchain.toolHttpRequest",
      "parameters": {
        "name": "searchAPI",
        "description": "Search for information",
        "url": "https://api.example.com/search?q={query}"
      }
    }
  ],
  "connections": {
    "HTTP Tool": {
      "ai_tool": [
        [{ "node": "AI Agent", "type": "ai_tool" }]
      ]
    }
  }
}
```

---

## Monitoring & Debugging

### Enable Debug Logging

```yaml
N8N_LOG_LEVEL=debug
N8N_LOG_OUTPUT=console,file
N8N_LOG_FILE_LOCATION=/var/log/n8n/
```

### Prometheus Metrics

```yaml
N8N_METRICS=true
N8N_METRICS_PREFIX=n8n_
# Metrics available at /metrics endpoint
```

### Execution Inspection

```javascript
// Log intermediate values in Code node
console.log('Input data:', JSON.stringify($json, null, 2));
console.log('Item count:', $input.all().length);

// Return with debug info
return [{
  json: {
    ...$json,
    _debug: {
      processedAt: new Date().toISOString(),
      inputCount: $input.all().length
    }
  }
}];
```

---

## Version Control & Backup

### Export Workflows for Git

```bash
#!/bin/bash
# export-workflows.sh
BACKUP_DIR="./n8n-backups/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Export all workflows
n8n export:workflow --all --output="$BACKUP_DIR/workflows/"

# Export credentials (encrypted)
n8n export:credentials --all --output="$BACKUP_DIR/credentials/"

# Commit to git
cd "$BACKUP_DIR/.."
git add .
git commit -m "Backup $(date +%Y-%m-%d)"
git push
```

### Docker Backup

```bash
# Backup n8n data volume
docker run --rm \
  -v n8n_data:/data \
  -v $(pwd)/backup:/backup \
  alpine tar czf /backup/n8n-backup-$(date +%Y%m%d).tar.gz /data
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Webhook not responding | Tunnel not running | Start with `n8n start --tunnel` |
| Credentials error | Wrong encryption key | Ensure consistent `N8N_ENCRYPTION_KEY` |
| Memory issues | Large data processing | Use batch processing, increase limits |
| Slow executions | No queue mode | Enable Redis queue mode |
| Database locks | SQLite in production | Migrate to PostgreSQL |

### Health Check

```bash
# Check n8n status
curl http://localhost:5678/healthz

# Check webhook receiver
curl http://localhost:5678/webhook-test/test

# View logs
docker logs n8n --tail 100 -f
```

### Reset Instance

```bash
# Reset all data (DESTRUCTIVE)
docker-compose down -v
docker-compose up -d

# Reset specific user
n8n user-management:reset --email=admin@example.com
```

---

## Quick Start Templates

### Minimal Webhook to API

```json
{
  "name": "Webhook to API",
  "nodes": [
    {
      "id": "1",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300],
      "parameters": {
        "httpMethod": "POST",
        "path": "incoming",
        "responseMode": "responseNode"
      }
    },
    {
      "id": "2",
      "name": "Process",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [450, 300],
      "parameters": {
        "mode": "manual",
        "assignments": {
          "assignments": [
            { "name": "processed", "value": true, "type": "boolean" }
          ]
        }
      }
    },
    {
      "id": "3",
      "name": "Response",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [650, 300],
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ { success: true, data: $json } }}"
      }
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Process", "type": "main", "index": 0 }]] },
    "Process": { "main": [[{ "node": "Response", "type": "main", "index": 0 }]] }
  },
  "settings": { "executionOrder": "v1" }
}
```

### Scheduled Data Sync

```json
{
  "name": "Daily Data Sync",
  "nodes": [
    {
      "id": "1",
      "name": "Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.2,
      "position": [250, 300],
      "parameters": {
        "rule": { "interval": [{ "field": "cronExpression", "expression": "0 6 * * *" }] }
      }
    },
    {
      "id": "2",
      "name": "Fetch Data",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [450, 300],
      "parameters": {
        "url": "https://api.source.com/data",
        "method": "GET"
      }
    },
    {
      "id": "3",
      "name": "Transform",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [650, 300],
      "parameters": {
        "jsCode": "return $input.all().map(item => ({\n  json: {\n    ...item.json,\n    syncedAt: new Date().toISOString()\n  }\n}));"
      }
    },
    {
      "id": "4",
      "name": "Save Data",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [850, 300],
      "parameters": {
        "url": "https://api.destination.com/import",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ $json }}"
      }
    }
  ],
  "connections": {
    "Schedule": { "main": [[{ "node": "Fetch Data", "type": "main", "index": 0 }]] },
    "Fetch Data": { "main": [[{ "node": "Transform", "type": "main", "index": 0 }]] },
    "Transform": { "main": [[{ "node": "Save Data", "type": "main", "index": 0 }]] }
  },
  "settings": { "executionOrder": "v1" }
}
```
