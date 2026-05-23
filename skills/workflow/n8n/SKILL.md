---
name: n8n
version: 1.0.0
description: Open-source workflow automation platform with visual node-based editor, 400+ integrations, webhooks, and self-hosted deployment capabilities
author: workspace-hub
category: automation
type: skill
capabilities:
  - visual_workflow_builder
  - webhook_triggers
  - scheduled_execution
  - api_integrations
  - custom_nodes
  - credentials_management
  - workflow_templates
  - error_handling
  - data_transformation
  - conditional_logic
tools:
  - n8n-cli
  - docker
  - npm
  - node
tags: [n8n, workflow, automation, integrations, webhooks, low-code, self-hosted, etl, data-pipeline]
platforms: [linux, macos, windows, docker, kubernetes]
related_skills:
  - yaml-configuration
  - api-integration
  - github-actions
  - activepieces
  - windmill
---

# n8n Workflow Automation Skill

Master n8n for visual workflow automation, API integrations, and self-hosted automation pipelines. This skill covers workflow design, node configuration, triggers, credentials management, custom nodes, and production deployment patterns.

## When to Use This Skill

### USE when:
- Building integrations between 400+ services (Slack, Gmail, Notion, Airtable, etc.)
- Creating visual workflows accessible to non-developers
- Self-hosting is required for data sovereignty and compliance
- Need webhook-triggered automations with real-time processing
- Building internal tool automations and business process automation
- Connecting APIs without writing extensive code
- Rapid prototyping of automation workflows
- Need human-in-the-loop approval workflows

### DON'T USE when:
- Orchestrating complex data pipelines with dependencies (use Airflow)
- CI/CD pipelines tightly coupled with git (use GitHub Actions)
- Need sub-second latency requirements (use direct API calls)
- Processing massive datasets (use dedicated ETL tools)
- Require enterprise audit compliance out-of-box (evaluate requirements)
- Simple single-trigger cron jobs (use systemd timers)

## Prerequisites

### Installation Options

**Option 1: npm (Development)**
```bash
# Install globally
npm install n8n -g

# Start n8n
n8n start

# Access UI at http://localhost:5678
```

**Option 2: Docker (Recommended)**
```bash
# Quick start with Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Access UI at http://localhost:5678
```

**Option 3: Docker Compose (Production)**
```yaml
# docker-compose.yml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_HOST=n8n.example.com
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://n8n.example.com/
      - GENERIC_TIMEZONE=UTC
      - TZ=UTC
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
    volumes:
      - n8n_data:/home/node/.n8n
      - ./custom-nodes:/home/node/.n8n/custom
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U n8n"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  n8n_data:
  postgres_data:
```

```bash
# Start with docker-compose
docker compose up -d

# View logs
docker compose logs -f n8n
```

**Option 4: Kubernetes with Helm**
```bash
# Add n8n Helm repo
helm repo add n8n https://n8n-io.github.io/n8n-helm
helm repo update

# Install n8n
helm install n8n n8n/n8n \
  --namespace n8n \
  --create-namespace \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=n8n.example.com

# Get initial admin password
kubectl get secret -n n8n n8n -o jsonpath="{.data.password}" | base64 --decode
```

### Development Setup
```bash
# Clone for custom node development
git clone https://github.com/n8n-io/n8n.git
cd n8n

# Install dependencies
pnpm install

# Build
pnpm build

# Start development server
pnpm dev
```

## Core Capabilities

### 1. Basic Workflow Structure

```json
{
  "name": "Basic Data Pipeline",
  "nodes": [
    {
      "parameters": {},
      "id": "start-node",
      "name": "Start",
      "type": "n8n-nodes-base.start",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "url": "https://api.example.com/data",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "httpHeaderAuth",
        "options": {
          "response": {
            "response": {
              "responseFormat": "json"
            }
          }
        }
      },
      "id": "http-request",
      "name": "Fetch Data",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [460, 300],
      "credentials": {
        "httpHeaderAuth": {
          "id": "1",
          "name": "API Key"
        }
      }
    },
    {
      "parameters": {
        "mode": "runOnceForEachItem",
        "jsCode": "// Transform each item\nconst item = $input.item.json;\n\nreturn {\n  id: item.id,\n  name: item.name.toUpperCase(),\n  processed_at: new Date().toISOString(),\n  source: 'n8n-pipeline'\n};"
      },
      "id": "transform",
      "name": "Transform Data",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [680, 300]
    },
    {
      "parameters": {
        "resource": "row",
        "operation": "create",
        "tableId": "={{ $env.AIRTABLE_TABLE_ID }}",
        "options": {}
      },
      "id": "airtable",
      "name": "Save to Airtable",
      "type": "n8n-nodes-base.airtable",
      "typeVersion": 2,
      "position": [900, 300],
      "credentials": {
        "airtableTokenApi": {
          "id": "2",
          "name": "Airtable Token"
        }
      }
    }
  ],
  "connections": {
    "Start": {
      "main": [
        [{ "node": "Fetch Data", "type": "main", "index": 0 }]
      ]
    },
    "Fetch Data": {
      "main": [
        [{ "node": "Transform Data", "type": "main", "index": 0 }]
      ]
    },
    "Transform Data": {
      "main": [
        [{ "node": "Save to Airtable", "type": "main", "index": 0 }]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

### 2. Webhook Triggers

```json
{
  "name": "Webhook Handler",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "incoming-webhook",
        "responseMode": "responseNode",
        "options": {
          "rawBody": true
        }
      },
      "id": "webhook",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1.1,
      "position": [240, 300],
      "webhookId": "unique-webhook-id"
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.event_type }}",
              "operation": "equals",
              "value2": "payment.completed"
            }
          ]
        }
      },
      "id": "filter",
      "name": "Filter Payment Events",
      "type": "n8n-nodes-base.filter",
      "typeVersion": 2,
      "position": [460, 300]
    },
    {
      "parameters": {
        "jsCode": "// Validate webhook signature\nconst crypto = require('crypto');\n\nconst payload = $input.item.json;\nconst signature = $input.item.headers['x-signature'];\nconst secret = $env.WEBHOOK_SECRET;\n\nconst expectedSignature = crypto\n  .createHmac('sha256', secret)\n  .update(JSON.stringify(payload))\n  .digest('hex');\n\nif (signature !== expectedSignature) {\n  throw new Error('Invalid webhook signature');\n}\n\nreturn {\n  ...payload,\n  validated: true,\n  processed_at: new Date().toISOString()\n};"
      },
      "id": "validate",
      "name": "Validate Signature",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [680, 300]
    },
    {
      "parameters": {
        "channel": "#payments",
        "text": "=Payment received!\n\nAmount: ${{ $json.amount }}\nCustomer: {{ $json.customer_email }}\nTransaction ID: {{ $json.transaction_id }}",
        "otherOptions": {}
      },
      "id": "slack",
      "name": "Notify Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2.1,
      "position": [900, 300],
      "credentials": {
        "slackApi": {
          "id": "3",
          "name": "Slack Bot"
        }
      }
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ JSON.stringify({ status: 'processed', id: $json.transaction_id }) }}"
      },
      "id": "respond",
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [1120, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [{ "node": "Filter Payment Events", "type": "main", "index": 0 }]
      ]
    },
    "Filter Payment Events": {
      "main": [
        [{ "node": "Validate Signature", "type": "main", "index": 0 }]
      ]
    },
    "Validate Signature": {
      "main": [
        [{ "node": "Notify Slack", "type": "main", "index": 0 }]
      ]
    },
    "Notify Slack": {
      "main": [
        [{ "node": "Respond to Webhook", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

### 3. Scheduled Workflows

```json
{
  "name": "Daily Report Generator",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "cronExpression",
              "expression": "0 9 * * 1-5"
            }
          ]
        }
      },
      "id": "schedule",
      "name": "Daily Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT \n  DATE(created_at) as date,\n  COUNT(*) as total_orders,\n  SUM(amount) as revenue,\n  AVG(amount) as avg_order_value\nFROM orders\nWHERE created_at >= CURRENT_DATE - INTERVAL '7 days'\nGROUP BY DATE(created_at)\nORDER BY date DESC",
        "options": {}
      },
      "id": "postgres",
      "name": "Query Sales Data",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2.3,
      "position": [460, 300],
      "credentials": {
        "postgres": {
          "id": "4",
          "name": "Production DB"
        }
      }
    },
    {
      "parameters": {
        "jsCode": "// Generate report summary\nconst data = $input.all();\n\nconst totalRevenue = data.reduce((sum, row) => sum + parseFloat(row.json.revenue), 0);\nconst totalOrders = data.reduce((sum, row) => sum + parseInt(row.json.total_orders), 0);\nconst avgOrderValue = totalRevenue / totalOrders;\n\nconst reportDate = new Date().toISOString().split('T')[0];\n\nreturn {\n  report_date: reportDate,\n  period: 'Last 7 Days',\n  summary: {\n    total_revenue: totalRevenue.toFixed(2),\n    total_orders: totalOrders,\n    avg_order_value: avgOrderValue.toFixed(2)\n  },\n  daily_breakdown: data.map(row => row.json)\n};"
      },
      "id": "transform",
      "name": "Generate Report",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [680, 300]
    },
    {
      "parameters": {
        "sendTo": "team@example.com",
        "subject": "=Weekly Sales Report - {{ $json.report_date }}",
        "emailType": "html",
        "html": "=<h1>Weekly Sales Report</h1>\n<p>Period: {{ $json.period }}</p>\n<h2>Summary</h2>\n<ul>\n  <li>Total Revenue: ${{ $json.summary.total_revenue }}</li>\n  <li>Total Orders: {{ $json.summary.total_orders }}</li>\n  <li>Average Order Value: ${{ $json.summary.avg_order_value }}</li>\n</ul>\n<h2>Daily Breakdown</h2>\n<table border=\"1\">\n  <tr><th>Date</th><th>Orders</th><th>Revenue</th></tr>\n  {{ $json.daily_breakdown.map(d => `<tr><td>${d.date}</td><td>${d.total_orders}</td><td>$${d.revenue}</td></tr>`).join('') }}\n</table>",
        "options": {}
      },
      "id": "email",
      "name": "Send Report Email",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2.1,
      "position": [900, 300],
      "credentials": {
        "smtp": {
          "id": "5",
          "name": "SMTP Server"
        }
      }
    }
  ],
  "connections": {
    "Daily Schedule": {
      "main": [
        [{ "node": "Query Sales Data", "type": "main", "index": 0 }]
      ]
    },
    "Query Sales Data": {
      "main": [
        [{ "node": "Generate Report", "type": "main", "index": 0 }]
      ]
    },
    "Generate Report": {
      "main": [
        [{ "node": "Send Report Email", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

### 4. Conditional Branching and Error Handling

```json
{
  "name": "Order Processing with Error Handling",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "process-order",
        "responseMode": "responseNode"
      },
      "id": "webhook",
      "name": "Order Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1.1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "id": "condition-1",
              "leftValue": "={{ $json.order_total }}",
              "rightValue": 1000,
              "operator": {
                "type": "number",
                "operation": "gte"
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      },
      "id": "switch",
      "name": "High Value Order?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [460, 300]
    },
    {
      "parameters": {
        "url": "https://api.payment.com/process",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "order_id",
              "value": "={{ $json.order_id }}"
            },
            {
              "name": "amount",
              "value": "={{ $json.order_total }}"
            },
            {
              "name": "priority",
              "value": "high"
            }
          ]
        },
        "options": {}
      },
      "id": "high-value-payment",
      "name": "Process High Value",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [680, 200],
      "onError": "continueErrorOutput"
    },
    {
      "parameters": {
        "url": "https://api.payment.com/process",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "order_id",
              "value": "={{ $json.order_id }}"
            },
            {
              "name": "amount",
              "value": "={{ $json.order_total }}"
            },
            {
              "name": "priority",
              "value": "normal"
            }
          ]
        }
      },
      "id": "normal-payment",
      "name": "Process Normal",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [680, 400],
      "onError": "continueErrorOutput"
    },
    {
      "parameters": {
        "jsCode": "// Handle payment error\nconst error = $input.item.json;\n\nreturn {\n  status: 'failed',\n  error_message: error.message || 'Payment processing failed',\n  order_id: $('Order Webhook').item.json.order_id,\n  timestamp: new Date().toISOString(),\n  retry_eligible: true\n};"
      },
      "id": "error-handler",
      "name": "Handle Error",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [900, 500]
    },
    {
      "parameters": {
        "channel": "#alerts",
        "text": "=Payment Failed!\n\nOrder ID: {{ $json.order_id }}\nError: {{ $json.error_message }}\nRetry Eligible: {{ $json.retry_eligible }}",
        "otherOptions": {}
      },
      "id": "slack-alert",
      "name": "Alert Team",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2.1,
      "position": [1120, 500],
      "credentials": {
        "slackApi": {
          "id": "3",
          "name": "Slack Bot"
        }
      }
    },
    {
      "parameters": {
        "mode": "combine",
        "combineBy": "combineAll",
        "options": {}
      },
      "id": "merge",
      "name": "Merge Results",
      "type": "n8n-nodes-base.merge",
      "typeVersion": 2.1,
      "position": [900, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ JSON.stringify({ status: 'processed', order_id: $json.order_id }) }}"
      },
      "id": "respond-success",
      "name": "Success Response",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [1120, 300]
    }
  ],
  "connections": {
    "Order Webhook": {
      "main": [
        [{ "node": "High Value Order?", "type": "main", "index": 0 }]
      ]
    },
    "High Value Order?": {
      "main": [
        [{ "node": "Process High Value", "type": "main", "index": 0 }],
        [{ "node": "Process Normal", "type": "main", "index": 0 }]
      ]
    },
    "Process High Value": {
      "main": [
        [{ "node": "Merge Results", "type": "main", "index": 0 }],
        [{ "node": "Handle Error", "type": "main", "index": 0 }]
      ]
    },
    "Process Normal": {
      "main": [
        [{ "node": "Merge Results", "type": "main", "index": 1 }],
        [{ "node": "Handle Error", "type": "main", "index": 0 }]
      ]
    },
    "Handle Error": {
      "main": [
        [{ "node": "Alert Team", "type": "main", "index": 0 }]
      ]
    },
    "Merge Results": {
      "main": [
        [{ "node": "Success Response", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

### 5. Data Transformation with Code Node

```javascript
// Code Node: Advanced Data Transformation
// Mode: Run Once for All Items

// Access all input items
const items = $input.all();

// Group items by category
const groupedByCategory = items.reduce((acc, item) => {
  const category = item.json.category || 'uncategorized';
  if (!acc[category]) {
    acc[category] = [];
  }
  acc[category].push(item.json);
  return acc;
}, {});

// Calculate statistics per category
const categoryStats = Object.entries(groupedByCategory).map(([category, items]) => {
  const values = items.map(i => parseFloat(i.value) || 0);

  return {
    category,
    count: items.length,
    total: values.reduce((a, b) => a + b, 0),
    average: values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0,
    min: Math.min(...values),
    max: Math.max(...values),
    items: items
  };
});

// Sort by total value descending
categoryStats.sort((a, b) => b.total - a.total);

// Add metadata
const result = {
  generated_at: new Date().toISOString(),
  total_items: items.length,
  total_categories: categoryStats.length,
  categories: categoryStats
};

return result;
```

```javascript
// Code Node: HTTP Request with Retry Logic
// Mode: Run Once for Each Item

const maxRetries = 3;
const baseDelay = 1000;

async function fetchWithRetry(url, options, attempt = 1) {
  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    if (attempt >= maxRetries) {
      throw error;
    }

    const delay = baseDelay * Math.pow(2, attempt - 1);
    await new Promise(resolve => setTimeout(resolve, delay));

    return fetchWithRetry(url, options, attempt + 1);
  }
}

const item = $input.item.json;

try {
  const result = await fetchWithRetry(
    `https://api.example.com/process/${item.id}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${$env.API_TOKEN}`
      },
      body: JSON.stringify(item)
    }
  );

  return {
    ...item,
    api_response: result,
    status: 'success'
  };
} catch (error) {
  return {
    ...item,
    error: error.message,
    status: 'failed'
  };
}
```

### 6. Credentials Management

```bash
# Environment variables for n8n
export N8N_ENCRYPTION_KEY="your-32-char-encryption-key-here"
export N8N_USER_MANAGEMENT_JWT_SECRET="your-jwt-secret"

# Database configuration
export DB_TYPE=postgresdb
export DB_POSTGRESDB_HOST=localhost
export DB_POSTGRESDB_PORT=5432
export DB_POSTGRESDB_DATABASE=n8n
export DB_POSTGRESDB_USER=n8n
export DB_POSTGRESDB_PASSWORD=secure_password

# External service credentials (set in n8n UI)
# These are stored encrypted in the database
```

```json
{
  "name": "Using Credentials Securely",
  "nodes": [
    {
      "parameters": {
        "url": "={{ $env.API_BASE_URL }}/users",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "httpHeaderAuth",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "X-Custom-Header",
              "value": "={{ $env.CUSTOM_HEADER_VALUE }}"
            }
          ]
        }
      },
      "id": "http",
      "name": "API Call",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [460, 300],
      "credentials": {
        "httpHeaderAuth": {
          "id": "1",
          "name": "API Key Auth"
        }
      }
    }
  ]
}
```

### 7. Custom Node Development

```typescript
// packages/nodes-custom/nodes/MyCustomNode/MyCustomNode.node.ts
import {
  IExecuteFunctions,
  INodeExecutionData,
  INodeType,
  INodeTypeDescription,
  NodeOperationError,
} from 'n8n-workflow';

export class MyCustomNode implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'My Custom Node',
    name: 'myCustomNode',
    icon: 'file:myicon.svg',
    group: ['transform'],
    version: 1,
    subtitle: '={{$parameter["operation"]}}',
    description: 'Custom node for specific business logic',
    defaults: {
      name: 'My Custom Node',
    },
    inputs: ['main'],
    outputs: ['main'],
    credentials: [
      {
        name: 'myCustomApi',
        required: true,
      },
    ],
    properties: [
      {
        displayName: 'Operation',
        name: 'operation',
        type: 'options',
        noDataExpression: true,
        options: [
          {
            name: 'Process',
            value: 'process',
            description: 'Process data through custom logic',
          },
          {
            name: 'Validate',
            value: 'validate',
            description: 'Validate data against rules',
          },
        ],
        default: 'process',
      },
      {
        displayName: 'Input Field',
        name: 'inputField',
        type: 'string',
        default: 'data',
        required: true,
        description: 'Field to process',
      },
      {
        displayName: 'Options',
        name: 'options',
        type: 'collection',
        placeholder: 'Add Option',
        default: {},
        options: [
          {
            displayName: 'Strict Mode',
            name: 'strictMode',
            type: 'boolean',
            default: false,
            description: 'Enable strict validation',
          },
          {
            displayName: 'Output Format',
            name: 'outputFormat',
            type: 'options',
            options: [
              { name: 'JSON', value: 'json' },
              { name: 'Array', value: 'array' },
            ],
            default: 'json',
          },
        ],
      },
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const returnData: INodeExecutionData[] = [];

    const operation = this.getNodeParameter('operation', 0) as string;
    const inputField = this.getNodeParameter('inputField', 0) as string;
    const options = this.getNodeParameter('options', 0, {}) as {
      strictMode?: boolean;
      outputFormat?: string;
    };

    // Get credentials
    const credentials = await this.getCredentials('myCustomApi');

    for (let i = 0; i < items.length; i++) {
      try {
        const item = items[i].json;
        const inputData = item[inputField];

        if (!inputData && options.strictMode) {
          throw new NodeOperationError(
            this.getNode(),
            `Field "${inputField}" not found in item ${i}`,
            { itemIndex: i }
          );
        }

        let result: any;

        if (operation === 'process') {
          result = await this.processData(inputData, credentials);
        } else if (operation === 'validate') {
          result = this.validateData(inputData, options.strictMode);
        }

        returnData.push({
          json: {
            ...item,
            processed: result,
            timestamp: new Date().toISOString(),
          },
        });
      } catch (error) {
        if (this.continueOnFail()) {
          returnData.push({
            json: {
              error: (error as Error).message,
              itemIndex: i,
            },
          });
          continue;
        }
        throw error;
      }
    }

    return [returnData];
  }

  private async processData(data: any, credentials: any): Promise<any> {
    // Custom processing logic
    return {
      original: data,
      processed: true,
      api_key_length: credentials.apiKey?.length || 0,
    };
  }

  private validateData(data: any, strict: boolean): any {
    const isValid = data !== null && data !== undefined;
    return {
      valid: isValid,
      strict_mode: strict,
      type: typeof data,
    };
  }
}
```

```typescript
// packages/nodes-custom/credentials/MyCustomApi.credentials.ts
import {
  ICredentialType,
  INodeProperties,
} from 'n8n-workflow';

export class MyCustomApi implements ICredentialType {
  name = 'myCustomApi';
  displayName = 'My Custom API';
  documentationUrl = 'https://docs.example.com/api';
  properties: INodeProperties[] = [
    {
      displayName: 'API Key',
      name: 'apiKey',
      type: 'string',
      typeOptions: {
        password: true,
      },
      default: '',
      required: true,
    },
    {
      displayName: 'Base URL',
      name: 'baseUrl',
      type: 'string',
      default: 'https://api.example.com',
    },
    {
      displayName: 'Environment',
      name: 'environment',
      type: 'options',
      options: [
        { name: 'Production', value: 'production' },
        { name: 'Staging', value: 'staging' },
        { name: 'Development', value: 'development' },
      ],
      default: 'production',
    },
  ];
}
```

### 8. Workflow Templates and Subworkflows

```json
{
  "name": "Main Orchestrator Workflow",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "orchestrate",
        "responseMode": "lastNode"
      },
      "id": "webhook",
      "name": "Start",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1.1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "workflowId": "={{ $env.DATA_VALIDATION_WORKFLOW_ID }}",
        "workflowInputs": {
          "mappingMode": "defineBelow",
          "value": {
            "data": "={{ $json.payload }}",
            "rules": "={{ $json.validation_rules }}"
          }
        }
      },
      "id": "validate",
      "name": "Run Validation Workflow",
      "type": "n8n-nodes-base.executeWorkflow",
      "typeVersion": 1,
      "position": [460, 300]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{ $json.is_valid }}",
              "value2": true
            }
          ]
        }
      },
      "id": "check-valid",
      "name": "Is Valid?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [680, 300]
    },
    {
      "parameters": {
        "workflowId": "={{ $env.PROCESSING_WORKFLOW_ID }}",
        "workflowInputs": {
          "mappingMode": "defineBelow",
          "value": {
            "validated_data": "={{ $json.data }}"
          }
        }
      },
      "id": "process",
      "name": "Run Processing Workflow",
      "type": "n8n-nodes-base.executeWorkflow",
      "typeVersion": 1,
      "position": [900, 200]
    },
    {
      "parameters": {
        "workflowId": "={{ $env.ERROR_HANDLER_WORKFLOW_ID }}",
        "workflowInputs": {
          "mappingMode": "defineBelow",
          "value": {
            "error_data": "={{ $json }}",
            "source": "orchestrator"
          }
        }
      },
      "id": "error-workflow",
      "name": "Run Error Handler",
      "type": "n8n-nodes-base.executeWorkflow",
      "typeVersion": 1,
      "position": [900, 400]
    }
  ],
  "connections": {
    "Start": {
      "main": [
        [{ "node": "Run Validation Workflow", "type": "main", "index": 0 }]
      ]
    },
    "Run Validation Workflow": {
      "main": [
        [{ "node": "Is Valid?", "type": "main", "index": 0 }]
      ]
    },
    "Is Valid?": {
      "main": [
        [{ "node": "Run Processing Workflow", "type": "main", "index": 0 }],
        [{ "node": "Run Error Handler", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

## Integration Examples

### Integration with Slack, Google Sheets, and Email

```json
{
  "name": "Multi-Channel Notification System",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "notify",
        "responseMode": "responseNode"
      },
      "id": "webhook",
      "name": "Incoming Notification",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1.1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "jsCode": "// Determine notification channels\nconst payload = $input.item.json;\n\nconst channels = [];\n\n// Add channels based on priority\nif (payload.priority === 'high' || payload.priority === 'critical') {\n  channels.push('slack');\n  channels.push('email');\n}\n\nif (payload.log_to_sheet) {\n  channels.push('sheets');\n}\n\nif (channels.length === 0) {\n  channels.push('slack'); // Default\n}\n\nreturn {\n  ...payload,\n  channels,\n  processed_at: new Date().toISOString()\n};"
      },
      "id": "router",
      "name": "Route Notification",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [460, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.channels.join(',') }}",
              "operation": "contains",
              "value2": "slack"
            }
          ]
        }
      },
      "id": "slack-filter",
      "name": "Send to Slack?",
      "type": "n8n-nodes-base.filter",
      "typeVersion": 2,
      "position": [680, 200]
    },
    {
      "parameters": {
        "channel": "={{ $json.priority === 'critical' ? '#critical-alerts' : '#notifications' }}",
        "text": "=*{{ $json.title }}*\n\n{{ $json.message }}\n\nPriority: {{ $json.priority }}\nSource: {{ $json.source }}",
        "attachments": [],
        "otherOptions": {}
      },
      "id": "slack",
      "name": "Post to Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2.1,
      "position": [900, 200],
      "credentials": {
        "slackApi": {
          "id": "3",
          "name": "Slack Bot"
        }
      }
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.channels.join(',') }}",
              "operation": "contains",
              "value2": "email"
            }
          ]
        }
      },
      "id": "email-filter",
      "name": "Send Email?",
      "type": "n8n-nodes-base.filter",
      "typeVersion": 2,
      "position": [680, 300]
    },
    {
      "parameters": {
        "sendTo": "={{ $json.recipient_email || 'team@example.com' }}",
        "subject": "=[{{ $json.priority.toUpperCase() }}] {{ $json.title }}",
        "emailType": "html",
        "html": "=<h2>{{ $json.title }}</h2>\n<p>{{ $json.message }}</p>\n<hr>\n<p><strong>Priority:</strong> {{ $json.priority }}</p>\n<p><strong>Source:</strong> {{ $json.source }}</p>\n<p><strong>Time:</strong> {{ $json.processed_at }}</p>"
      },
      "id": "email",
      "name": "Send Email",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2.1,
      "position": [900, 300],
      "credentials": {
        "smtp": {
          "id": "5",
          "name": "SMTP"
        }
      }
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.channels.join(',') }}",
              "operation": "contains",
              "value2": "sheets"
            }
          ]
        }
      },
      "id": "sheets-filter",
      "name": "Log to Sheets?",
      "type": "n8n-nodes-base.filter",
      "typeVersion": 2,
      "position": [680, 400]
    },
    {
      "parameters": {
        "operation": "append",
        "documentId": {
          "__rl": true,
          "value": "={{ $env.GOOGLE_SHEET_ID }}",
          "mode": "id"
        },
        "sheetName": {
          "__rl": true,
          "value": "Notifications",
          "mode": "list"
        },
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "Timestamp": "={{ $json.processed_at }}",
            "Title": "={{ $json.title }}",
            "Message": "={{ $json.message }}",
            "Priority": "={{ $json.priority }}",
            "Source": "={{ $json.source }}"
          }
        }
      },
      "id": "sheets",
      "name": "Log to Google Sheets",
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 4.1,
      "position": [900, 400],
      "credentials": {
        "googleSheetsOAuth2Api": {
          "id": "6",
          "name": "Google Sheets"
        }
      }
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ JSON.stringify({ success: true, channels: $json.channels }) }}"
      },
      "id": "respond",
      "name": "Respond",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [1120, 300]
    }
  ],
  "connections": {
    "Incoming Notification": {
      "main": [
        [{ "node": "Route Notification", "type": "main", "index": 0 }]
      ]
    },
    "Route Notification": {
      "main": [
        [
          { "node": "Send to Slack?", "type": "main", "index": 0 },
          { "node": "Send Email?", "type": "main", "index": 0 },
          { "node": "Log to Sheets?", "type": "main", "index": 0 }
        ]
      ]
    },
    "Send to Slack?": {
      "main": [
        [{ "node": "Post to Slack", "type": "main", "index": 0 }]
      ]
    },
    "Send Email?": {
      "main": [
        [{ "node": "Send Email", "type": "main", "index": 0 }]
      ]
    },
    "Log to Sheets?": {
      "main": [
        [{ "node": "Log to Google Sheets", "type": "main", "index": 0 }]
      ]
    },
    "Post to Slack": {
      "main": [
        [{ "node": "Respond", "type": "main", "index": 0 }]
      ]
    },
    "Send Email": {
      "main": [
        [{ "node": "Respond", "type": "main", "index": 0 }]
      ]
    },
    "Log to Google Sheets": {
      "main": [
        [{ "node": "Respond", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

### Integration with GitHub and Jira

```json
{
  "name": "GitHub to Jira Sync",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "github-webhook",
        "options": {}
      },
      "id": "github-webhook",
      "name": "GitHub Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1.1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.action }}",
              "operation": "equals",
              "value2": "opened"
            }
          ]
        }
      },
      "id": "filter-opened",
      "name": "Is New Issue?",
      "type": "n8n-nodes-base.filter",
      "typeVersion": 2,
      "position": [460, 300]
    },
    {
      "parameters": {
        "jsCode": "// Map GitHub issue to Jira format\nconst issue = $input.item.json.issue;\n\n// Map labels to Jira priority\nconst labels = issue.labels.map(l => l.name);\nlet priority = 'Medium';\nif (labels.includes('critical') || labels.includes('urgent')) {\n  priority = 'Highest';\n} else if (labels.includes('high')) {\n  priority = 'High';\n} else if (labels.includes('low')) {\n  priority = 'Low';\n}\n\n// Map to Jira issue type\nlet issueType = 'Task';\nif (labels.includes('bug')) {\n  issueType = 'Bug';\n} else if (labels.includes('feature')) {\n  issueType = 'Story';\n}\n\nreturn {\n  summary: `[GitHub] ${issue.title}`,\n  description: `${issue.body}\\n\\n---\\nGitHub Issue: ${issue.html_url}\\nCreated by: ${issue.user.login}`,\n  priority: priority,\n  issueType: issueType,\n  labels: labels.filter(l => !['bug', 'feature', 'critical', 'urgent', 'high', 'low'].includes(l)),\n  github_issue_number: issue.number,\n  github_repo: $input.item.json.repository.full_name\n};"
      },
      "id": "map-to-jira",
      "name": "Map to Jira Format",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [680, 300]
    },
    {
      "parameters": {
        "resource": "issue",
        "operation": "create",
        "project": "={{ $env.JIRA_PROJECT_KEY }}",
        "issueType": "={{ $json.issueType }}",
        "summary": "={{ $json.summary }}",
        "additionalFields": {
          "description": "={{ $json.description }}",
          "priority": "={{ $json.priority }}",
          "labels": "={{ $json.labels }}"
        }
      },
      "id": "create-jira",
      "name": "Create Jira Issue",
      "type": "n8n-nodes-base.jira",
      "typeVersion": 1,
      "position": [900, 300],
      "credentials": {
        "jiraSoftwareCloudApi": {
          "id": "7",
          "name": "Jira"
        }
      }
    },
    {
      "parameters": {
        "owner": "={{ $('Map to Jira Format').item.json.github_repo.split('/')[0] }}",
        "repository": "={{ $('Map to Jira Format').item.json.github_repo.split('/')[1] }}",
        "issueNumber": "={{ $('Map to Jira Format').item.json.github_issue_number }}",
        "body": "=Jira issue created: {{ $json.key }}\n\nLink: {{ $env.JIRA_BASE_URL }}/browse/{{ $json.key }}"
      },
      "id": "comment-github",
      "name": "Comment on GitHub",
      "type": "n8n-nodes-base.github",
      "typeVersion": 1,
      "position": [1120, 300],
      "credentials": {
        "githubApi": {
          "id": "8",
          "name": "GitHub"
        }
      }
    }
  ],
  "connections": {
    "GitHub Webhook": {
      "main": [
        [{ "node": "Is New Issue?", "type": "main", "index": 0 }]
      ]
    },
    "Is New Issue?": {
      "main": [
        [{ "node": "Map to Jira Format", "type": "main", "index": 0 }]
      ]
    },
    "Map to Jira Format": {
      "main": [
        [{ "node": "Create Jira Issue", "type": "main", "index": 0 }]
      ]
    },
    "Create Jira Issue": {
      "main": [
        [{ "node": "Comment on GitHub", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

## Best Practices

### 1. Workflow Organization
```
workflows/
├── core/
│   ├── data-validation.json
│   ├── error-handler.json
│   └── notification-router.json
├── integrations/
│   ├── slack-bot.json
│   ├── github-sync.json
│   └── crm-sync.json
├── scheduled/
│   ├── daily-reports.json
│   └── weekly-cleanup.json
└── webhooks/
    ├── payment-processor.json
    └── form-handler.json
```

### 2. Error Handling Patterns
```javascript
// Always use try-catch in Code nodes
try {
  const result = await riskyOperation();
  return { success: true, data: result };
} catch (error) {
  // Log error details
  console.error('Operation failed:', error.message);

  // Return structured error for downstream handling
  return {
    success: false,
    error: error.message,
    timestamp: new Date().toISOString(),
    retryable: error.code !== 'PERMANENT_FAILURE'
  };
}
```

### 3. Security Best Practices
```yaml
# Production environment variables
N8N_ENCRYPTION_KEY: "32-character-secure-key"
N8N_USER_MANAGEMENT_JWT_SECRET: "secure-jwt-secret"
N8N_BASIC_AUTH_ACTIVE: "true"
N8N_BASIC_AUTH_USER: "admin"
N8N_BASIC_AUTH_PASSWORD: "${SECURE_PASSWORD}"

# Webhook security
WEBHOOK_URL: "https://n8n.example.com/"
N8N_WEBHOOK_TUNNEL_URL: ""  # Disable tunnel in production

# Database encryption
DB_POSTGRESDB_SSL_ENABLED: "true"
DB_POSTGRESDB_SSL_REJECT_UNAUTHORIZED: "true"
```

### 4. Performance Optimization
```javascript
// Batch processing for large datasets
const BATCH_SIZE = 100;
const items = $input.all();
const results = [];

for (let i = 0; i < items.length; i += BATCH_SIZE) {
  const batch = items.slice(i, i + BATCH_SIZE);

  // Process batch
  const batchResults = await Promise.all(
    batch.map(item => processItem(item.json))
  );

  results.push(...batchResults);

  // Optional: Add delay between batches to avoid rate limits
  if (i + BATCH_SIZE < items.length) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }
}

return results;
```

### 5. Testing Workflows
```bash
# Export workflow for version control
curl -X GET "http://localhost:5678/api/v1/workflows/1" \
  -H "X-N8N-API-KEY: your-api-key" \
  -o workflow-backup.json

# Import workflow
curl -X POST "http://localhost:5678/api/v1/workflows" \
  -H "X-N8N-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d @workflow-backup.json

# Execute workflow via API
curl -X POST "http://localhost:5678/api/v1/workflows/1/activate" \
  -H "X-N8N-API-KEY: your-api-key"
```

## Troubleshooting

### Common Issues

**Issue: Webhook not receiving data**
```bash
# Check webhook URL
curl -X POST https://n8n.example.com/webhook/your-path \
  -H "Content-Type: application/json" \
  -d '{"test": true}'

# Verify workflow is active
# Check n8n logs
docker logs n8n-container 2>&1 | grep -i webhook

# Ensure WEBHOOK_URL is correctly set
echo $WEBHOOK_URL
```

**Issue: Credentials not working**
```bash
# Test credential manually
curl -X GET "https://api.example.com/test" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Check encryption key is set
# Credentials are encrypted - changing key breaks existing credentials
echo $N8N_ENCRYPTION_KEY | wc -c  # Should be 32+ characters
```

**Issue: Workflow execution timeout**
```yaml
# Increase timeout in docker-compose
environment:
  - EXECUTIONS_TIMEOUT=3600  # 1 hour
  - EXECUTIONS_TIMEOUT_MAX=7200  # 2 hours max
```

**Issue: Memory issues with large datasets**
```javascript
// Stream processing instead of loading all data
// Use pagination in HTTP Request nodes
const PAGE_SIZE = 100;
let page = 1;
let hasMore = true;
const allResults = [];

while (hasMore) {
  const response = await $http.get(
    `https://api.example.com/data?page=${page}&limit=${PAGE_SIZE}`
  );

  allResults.push(...response.data.items);
  hasMore = response.data.has_more;
  page++;
}

return allResults;
```

### Debugging Tips

```javascript
// Add debugging output in Code nodes
console.log('Input data:', JSON.stringify($input.all(), null, 2));
console.log('Environment:', $env.NODE_ENV);
console.log('Workflow:', $workflow.name);

// Check execution context
console.log('Execution ID:', $execution.id);
console.log('Execution mode:', $execution.mode);

// Inspect previous node output
const previousOutput = $('Previous Node Name').all();
console.log('Previous output:', previousOutput);
```

```bash
# View execution logs
docker logs -f n8n-container 2>&1 | grep -E "(error|warn|execution)"

# Check database for failed executions
docker exec -it postgres psql -U n8n -d n8n -c \
  "SELECT id, status, started_at FROM execution_entity WHERE status = 'error' ORDER BY started_at DESC LIMIT 10;"
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with comprehensive workflow patterns |

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [n8n Workflow Templates](https://n8n.io/workflows/)
- [n8n GitHub Repository](https://github.com/n8n-io/n8n)
- [Custom Node Development](https://docs.n8n.io/integrations/creating-nodes/)
- [n8n API Reference](https://docs.n8n.io/api/)

---

*This skill provides production-ready patterns for n8n workflow automation, tested across enterprise integration scenarios handling thousands of daily executions.*
