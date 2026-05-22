---
name: activepieces
version: 1.0.0
description: Self-hosted no-code automation platform with visual flow builder, type-safe custom pieces, API integrations, and event-driven triggers
author: workspace-hub
category: automation
type: skill
capabilities:
  - visual_flow_builder
  - custom_pieces
  - api_integration
  - event_triggers
  - scheduled_runs
  - branching_logic
  - loops_iterations
  - data_mapping
  - webhook_handling
  - approval_flows
tools:
  - activepieces-cli
  - docker
  - npm
  - node
tags: [activepieces, automation, no-code, workflow, integrations, self-hosted, open-source, typescript]
platforms: [linux, macos, windows, docker, kubernetes]
related_skills:
  - n8n
  - yaml-configuration
  - api-integration
  - windmill
---

# Activepieces Workflow Automation Skill

Master Activepieces for self-hosted no-code automation with type-safe custom pieces, visual flow building, and enterprise-ready workflow orchestration. This skill covers flow design, piece development, triggers, connections management, and production deployment patterns.

## When to Use This Skill

### USE when:
- Building business automations with type-safe custom components
- Self-hosting is required for data sovereignty and compliance
- Need modular, reusable automation pieces
- Creating approval workflows with human-in-the-loop
- Connecting APIs with visual flow builder
- Teams need both no-code and code-first options
- Require MIT-licensed open-source automation
- Building internal tool automations

### DON'T USE when:
- Complex DAG-based data pipeline orchestration (use Airflow)
- CI/CD pipelines tightly coupled with git (use GitHub Actions)
- Need 400+ pre-built integrations immediately (use n8n)
- Sub-second latency requirements (use direct API calls)
- Simple single-trigger cron jobs (use systemd timers)

## Prerequisites

### Installation Options

**Option 1: Docker Compose (Recommended)**
```yaml
# docker-compose.yml
version: '3.8'

services:
  activepieces:
    image: activepieces/activepieces:latest
    restart: always
    ports:
      - "8080:80"
    environment:
      - AP_ENGINE_EXECUTABLE_PATH=dist/packages/engine/main.js
      - AP_ENVIRONMENT=prod
      - AP_FRONTEND_URL=http://localhost:8080
      - AP_WEBHOOK_TIMEOUT_SECONDS=30
      - AP_TRIGGER_DEFAULT_POLL_INTERVAL=5
      - AP_POSTGRES_DATABASE=activepieces
      - AP_POSTGRES_HOST=postgres
      - AP_POSTGRES_PORT=5432
      - AP_POSTGRES_USERNAME=activepieces
      - AP_POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - AP_ENCRYPTION_KEY=${AP_ENCRYPTION_KEY}
      - AP_JWT_SECRET=${AP_JWT_SECRET}
      - AP_QUEUE_MODE=MEMORY
      - AP_REDIS_HOST=redis
      - AP_REDIS_PORT=6379
      - AP_SANDBOX_RUN_TIME_SECONDS=600
      - AP_TELEMETRY_ENABLED=false
    depends_on:
      - postgres
      - redis
    volumes:
      - ./data:/root/.activepieces

  postgres:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_USER=activepieces
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=activepieces
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U activepieces"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7
    restart: always
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

```bash
# Generate required secrets
export POSTGRES_PASSWORD=$(openssl rand -hex 32)
export AP_ENCRYPTION_KEY=$(openssl rand -hex 16)
export AP_JWT_SECRET=$(openssl rand -hex 32)

# Start services
docker compose up -d

# Access UI at http://localhost:8080
```

**Option 2: Kubernetes with Helm**
```bash
# Add Activepieces Helm repo
helm repo add activepieces https://activepieces.github.io/activepieces
helm repo update

# Create namespace
kubectl create namespace activepieces

# Create secrets
kubectl create secret generic activepieces-secrets \
  --namespace activepieces \
  --from-literal=encryption-key=$(openssl rand -hex 16) \
  --from-literal=jwt-secret=$(openssl rand -hex 32) \
  --from-literal=postgres-password=$(openssl rand -hex 32)

# Install Activepieces
helm install activepieces activepieces/activepieces \
  --namespace activepieces \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=activepieces.example.com

# Get initial setup URL
kubectl get ingress -n activepieces
```

**Option 3: Local Development**
```bash
# Clone repository
git clone https://github.com/activepieces/activepieces.git
cd activepieces

# Install dependencies
npm install

# Setup environment
cp .env.example .env

# Start development server
npm run dev

# Access at http://localhost:4200
```

### Development Setup for Custom Pieces
```bash
# Install Activepieces CLI
npm install -g @activepieces/cli

# Create new piece project
ap create-piece my-custom-piece

# Navigate to piece directory
cd pieces/my-custom-piece

# Install dependencies
npm install

# Build piece
npm run build

# Test piece locally
npm run test
```

## Core Capabilities

### 1. Basic Flow Structure

```typescript
// Flow definition structure
interface Flow {
  id: string;
  projectId: string;
  folderId?: string;
  status: 'ENABLED' | 'DISABLED';
  schedule?: {
    cronExpression: string;
    timezone: string;
  };
  trigger: Trigger;
  steps: Step[];
}

// Example flow JSON
const basicFlow = {
  "displayName": "New Customer Onboarding",
  "trigger": {
    "name": "webhook",
    "type": "WEBHOOK",
    "settings": {
      "inputUiInfo": {}
    },
    "valid": true,
    "displayName": "Webhook Trigger"
  },
  "steps": [
    {
      "name": "validate_data",
      "type": "CODE",
      "settings": {
        "input": {
          "customer": "{{trigger.body.customer}}"
        },
        "sourceCode": {
          "code": "export const code = async (inputs) => {\n  const { customer } = inputs;\n  \n  if (!customer.email || !customer.name) {\n    throw new Error('Missing required fields');\n  }\n  \n  return {\n    valid: true,\n    customer: {\n      ...customer,\n      email: customer.email.toLowerCase().trim(),\n      created_at: new Date().toISOString()\n    }\n  };\n};"
        }
      },
      "displayName": "Validate Customer Data"
    },
    {
      "name": "create_crm_contact",
      "type": "PIECE",
      "settings": {
        "pieceName": "@activepieces/piece-hubspot",
        "pieceVersion": "~0.5.0",
        "actionName": "create_contact",
        "input": {
          "email": "{{validate_data.customer.email}}",
          "firstName": "{{validate_data.customer.name.split(' ')[0]}}",
          "lastName": "{{validate_data.customer.name.split(' ').slice(1).join(' ')}}",
          "properties": {
            "source": "activepieces_onboarding",
            "created_via": "automation"
          }
        }
      },
      "displayName": "Create HubSpot Contact"
    },
    {
      "name": "send_welcome_email",
      "type": "PIECE",
      "settings": {
        "pieceName": "@activepieces/piece-sendgrid",
        "pieceVersion": "~0.3.0",
        "actionName": "send_email",
        "input": {
          "to": "{{validate_data.customer.email}}",
          "subject": "Welcome to Our Platform!",
          "html": "<h1>Welcome, {{validate_data.customer.name}}!</h1><p>We're excited to have you on board.</p>"
        }
      },
      "displayName": "Send Welcome Email"
    },
    {
      "name": "notify_team",
      "type": "PIECE",
      "settings": {
        "pieceName": "@activepieces/piece-slack",
        "pieceVersion": "~0.6.0",
        "actionName": "send_message",
        "input": {
          "channel": "#new-customers",
          "text": "New customer onboarded: {{validate_data.customer.name}} ({{validate_data.customer.email}})"
        }
      },
      "displayName": "Notify Sales Team"
    }
  ]
};
```

### 2. Webhook Triggers

```typescript
// Webhook trigger configuration
const webhookFlow = {
  "displayName": "Payment Webhook Handler",
  "trigger": {
    "name": "webhook",
    "type": "WEBHOOK",
    "settings": {
      "inputUiInfo": {
        "customizedInputs": {}
      }
    },
    "displayName": "Payment Webhook"
  },
  "steps": [
    {
      "name": "verify_signature",
      "type": "CODE",
      "settings": {
        "input": {
          "payload": "{{trigger.body}}",
          "signature": "{{trigger.headers['x-signature']}}",
          "secret": "{{connections.payment_webhook_secret}}"
        },
        "sourceCode": {
          "code": `
import crypto from 'crypto';

export const code = async (inputs) => {
  const { payload, signature, secret } = inputs;

  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(JSON.stringify(payload))
    .digest('hex');

  if (signature !== expectedSignature) {
    throw new Error('Invalid webhook signature');
  }

  return {
    verified: true,
    event: payload.event_type,
    data: payload.data
  };
};`
        }
      },
      "displayName": "Verify Webhook Signature"
    },
    {
      "name": "route_by_event",
      "type": "BRANCH",
      "settings": {
        "conditions": [
          {
            "name": "payment_completed",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{verify_signature.event}} === 'payment.completed'"
            }
          },
          {
            "name": "payment_failed",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{verify_signature.event}} === 'payment.failed'"
            }
          },
          {
            "name": "refund_initiated",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{verify_signature.event}} === 'refund.initiated'"
            }
          }
        ]
      },
      "displayName": "Route by Event Type"
    }
  ]
};
```

### 3. Scheduled Flows

```typescript
// Scheduled flow with cron expression
const scheduledFlow = {
  "displayName": "Daily Sales Report",
  "schedule": {
    "cronExpression": "0 9 * * 1-5",  // 9 AM Mon-Fri
    "timezone": "America/New_York"
  },
  "trigger": {
    "name": "schedule",
    "type": "SCHEDULE",
    "settings": {},
    "displayName": "Daily Schedule"
  },
  "steps": [
    {
      "name": "get_date_range",
      "type": "CODE",
      "settings": {
        "sourceCode": {
          "code": `
export const code = async () => {
  const now = new Date();
  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);

  return {
    start_date: yesterday.toISOString().split('T')[0],
    end_date: now.toISOString().split('T')[0],
    report_date: now.toISOString()
  };
};`
        }
      },
      "displayName": "Calculate Date Range"
    },
    {
      "name": "fetch_sales_data",
      "type": "PIECE",
      "settings": {
        "pieceName": "@activepieces/piece-http",
        "pieceVersion": "~0.4.0",
        "actionName": "send_request",
        "input": {
          "method": "GET",
          "url": "{{connections.sales_api.base_url}}/api/v1/sales",
          "headers": {
            "Authorization": "Bearer {{connections.sales_api.api_key}}"
          },
          "queryParams": {
            "start_date": "{{get_date_range.start_date}}",
            "end_date": "{{get_date_range.end_date}}"
          }
        }
      },
      "displayName": "Fetch Sales Data"
    },
    {
      "name": "generate_report",
      "type": "CODE",
      "settings": {
        "input": {
          "sales": "{{fetch_sales_data.body.data}}",
          "report_date": "{{get_date_range.report_date}}"
        },
        "sourceCode": {
          "code": `
export const code = async (inputs) => {
  const { sales, report_date } = inputs;

  const totalRevenue = sales.reduce((sum, sale) => sum + sale.amount, 0);
  const totalOrders = sales.length;
  const avgOrderValue = totalOrders > 0 ? totalRevenue / totalOrders : 0;

  const byCategory = sales.reduce((acc, sale) => {
    const cat = sale.category || 'Other';
    acc[cat] = (acc[cat] || 0) + sale.amount;
    return acc;
  }, {});

  return {
    report_date,
    summary: {
      total_revenue: totalRevenue.toFixed(2),
      total_orders: totalOrders,
      avg_order_value: avgOrderValue.toFixed(2)
    },
    by_category: Object.entries(byCategory)
      .map(([category, amount]) => ({ category, amount }))
      .sort((a, b) => b.amount - a.amount),
    top_products: sales
      .sort((a, b) => b.amount - a.amount)
      .slice(0, 5)
  };
};`
        }
      },
      "displayName": "Generate Report Summary"
    },
    {
      "name": "send_report",
      "type": "PIECE",
      "settings": {
        "pieceName": "@activepieces/piece-gmail",
        "pieceVersion": "~0.5.0",
        "actionName": "send_email",
        "input": {
          "to": ["sales-team@example.com", "management@example.com"],
          "subject": "Daily Sales Report - {{get_date_range.start_date}}",
          "body": "<h1>Daily Sales Report</h1><h2>Summary</h2><ul><li>Total Revenue: ${{generate_report.summary.total_revenue}}</li><li>Total Orders: {{generate_report.summary.total_orders}}</li><li>Average Order Value: ${{generate_report.summary.avg_order_value}}</li></ul>"
        }
      },
      "displayName": "Send Report Email"
    }
  ]
};
```

### 4. Branching and Conditional Logic

```typescript
// Branch step with multiple conditions
const branchingFlow = {
  "displayName": "Lead Qualification Flow",
  "trigger": {
    "name": "webhook",
    "type": "WEBHOOK",
    "settings": {},
    "displayName": "New Lead"
  },
  "steps": [
    {
      "name": "enrich_lead",
      "type": "PIECE",
      "settings": {
        "pieceName": "@activepieces/piece-clearbit",
        "pieceVersion": "~0.2.0",
        "actionName": "enrich_company",
        "input": {
          "domain": "{{trigger.body.company_domain}}"
        }
      },
      "displayName": "Enrich Lead Data"
    },
    {
      "name": "calculate_score",
      "type": "CODE",
      "settings": {
        "input": {
          "lead": "{{trigger.body}}",
          "enriched": "{{enrich_lead}}"
        },
        "sourceCode": {
          "code": `
export const code = async (inputs) => {
  const { lead, enriched } = inputs;
  let score = 0;

  // Company size scoring
  if (enriched.metrics?.employees > 1000) score += 30;
  else if (enriched.metrics?.employees > 100) score += 20;
  else if (enriched.metrics?.employees > 10) score += 10;

  // Industry scoring
  const highValueIndustries = ['technology', 'finance', 'healthcare'];
  if (highValueIndustries.includes(enriched.category?.industry?.toLowerCase())) {
    score += 25;
  }

  // Title scoring
  const seniorTitles = ['ceo', 'cto', 'vp', 'director', 'head'];
  if (seniorTitles.some(t => lead.title?.toLowerCase().includes(t))) {
    score += 20;
  }

  // Budget scoring
  if (lead.budget > 100000) score += 25;
  else if (lead.budget > 50000) score += 15;
  else if (lead.budget > 10000) score += 10;

  return {
    score,
    tier: score >= 70 ? 'hot' : score >= 40 ? 'warm' : 'cold',
    lead: { ...lead, enriched }
  };
};`
        }
      },
      "displayName": "Calculate Lead Score"
    },
    {
      "name": "route_by_tier",
      "type": "BRANCH",
      "settings": {
        "conditions": [
          {
            "name": "hot_lead",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{calculate_score.tier}} === 'hot'"
            },
            "steps": [
              {
                "name": "notify_sales_urgent",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-slack",
                  "actionName": "send_message",
                  "input": {
                    "channel": "#hot-leads",
                    "text": "HOT LEAD: {{calculate_score.lead.name}} from {{calculate_score.lead.company}} (Score: {{calculate_score.score}})"
                  }
                }
              },
              {
                "name": "create_salesforce_lead",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-salesforce",
                  "actionName": "create_record",
                  "input": {
                    "objectName": "Lead",
                    "fields": {
                      "FirstName": "{{calculate_score.lead.first_name}}",
                      "LastName": "{{calculate_score.lead.last_name}}",
                      "Company": "{{calculate_score.lead.company}}",
                      "Email": "{{calculate_score.lead.email}}",
                      "LeadSource": "Website",
                      "Rating": "Hot"
                    }
                  }
                }
              },
              {
                "name": "schedule_demo",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-calendly",
                  "actionName": "create_scheduling_link",
                  "input": {
                    "event_type": "sales-demo",
                    "invitee_email": "{{calculate_score.lead.email}}"
                  }
                }
              }
            ]
          },
          {
            "name": "warm_lead",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{calculate_score.tier}} === 'warm'"
            },
            "steps": [
              {
                "name": "add_to_nurture",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-mailchimp",
                  "actionName": "add_subscriber",
                  "input": {
                    "list_id": "{{connections.mailchimp.nurture_list_id}}",
                    "email": "{{calculate_score.lead.email}}",
                    "tags": ["warm-lead", "nurture-sequence"]
                  }
                }
              }
            ]
          },
          {
            "name": "cold_lead",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{calculate_score.tier}} === 'cold'"
            },
            "steps": [
              {
                "name": "add_to_drip",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-mailchimp",
                  "actionName": "add_subscriber",
                  "input": {
                    "list_id": "{{connections.mailchimp.general_list_id}}",
                    "email": "{{calculate_score.lead.email}}",
                    "tags": ["cold-lead"]
                  }
                }
              }
            ]
          }
        ]
      },
      "displayName": "Route by Lead Tier"
    }
  ]
};
```

### 5. Loop and Iteration

```typescript
// Loop over items
const loopFlow = {
  "displayName": "Batch Order Processing",
  "trigger": {
    "name": "webhook",
    "type": "WEBHOOK",
    "settings": {},
    "displayName": "Batch Orders"
  },
  "steps": [
    {
      "name": "process_orders",
      "type": "LOOP_ON_ITEMS",
      "settings": {
        "items": "{{trigger.body.orders}}",
        "steps": [
          {
            "name": "validate_order",
            "type": "CODE",
            "settings": {
              "input": {
                "order": "{{loop.item}}"
              },
              "sourceCode": {
                "code": `
export const code = async (inputs) => {
  const { order } = inputs;

  const errors = [];

  if (!order.customer_id) errors.push('Missing customer_id');
  if (!order.items || order.items.length === 0) errors.push('No items in order');
  if (!order.total || order.total <= 0) errors.push('Invalid total');

  return {
    valid: errors.length === 0,
    errors,
    order: errors.length === 0 ? order : null
  };
};`
              }
            },
            "displayName": "Validate Order"
          },
          {
            "name": "check_inventory",
            "type": "PIECE",
            "settings": {
              "pieceName": "@activepieces/piece-http",
              "actionName": "send_request",
              "input": {
                "method": "POST",
                "url": "{{connections.inventory_api.base_url}}/api/check-availability",
                "headers": {
                  "Authorization": "Bearer {{connections.inventory_api.api_key}}"
                },
                "body": {
                  "items": "{{validate_order.order.items}}"
                }
              }
            },
            "displayName": "Check Inventory"
          },
          {
            "name": "process_payment",
            "type": "PIECE",
            "settings": {
              "pieceName": "@activepieces/piece-stripe",
              "actionName": "create_charge",
              "input": {
                "amount": "{{validate_order.order.total}}",
                "currency": "usd",
                "customer": "{{validate_order.order.stripe_customer_id}}",
                "description": "Order {{validate_order.order.id}}"
              }
            },
            "displayName": "Process Payment"
          },
          {
            "name": "create_shipment",
            "type": "PIECE",
            "settings": {
              "pieceName": "@activepieces/piece-shippo",
              "actionName": "create_shipment",
              "input": {
                "address_from": "{{connections.shippo.warehouse_address}}",
                "address_to": "{{validate_order.order.shipping_address}}",
                "parcels": "{{validate_order.order.items}}"
              }
            },
            "displayName": "Create Shipment"
          }
        ]
      },
      "displayName": "Process Each Order"
    },
    {
      "name": "summarize_results",
      "type": "CODE",
      "settings": {
        "input": {
          "results": "{{process_orders}}"
        },
        "sourceCode": {
          "code": `
export const code = async (inputs) => {
  const { results } = inputs;

  const successful = results.filter(r => r.success);
  const failed = results.filter(r => !r.success);

  return {
    total_processed: results.length,
    successful: successful.length,
    failed: failed.length,
    failed_orders: failed.map(f => ({
      order_id: f.order_id,
      error: f.error
    })),
    total_revenue: successful.reduce((sum, r) => sum + r.amount, 0)
  };
};`
        }
      },
      "displayName": "Summarize Results"
    }
  ]
};
```

### 6. Custom Piece Development

```typescript
// pieces/my-custom-api/src/index.ts
import { createPiece, PieceAuth } from '@activepieces/pieces-framework';
import { createCustomResource } from './lib/actions/create-resource';
import { getCustomResource } from './lib/actions/get-resource';
import { listCustomResources } from './lib/actions/list-resources';
import { resourceCreatedTrigger } from './lib/triggers/resource-created';

const authDescription = `
To get your API key:
1. Go to Settings > API Keys in your dashboard
2. Click "Create New Key"
3. Copy the generated key
`;

export const customApiAuth = PieceAuth.SecretText({
  displayName: 'API Key',
  required: true,
  description: authDescription,
  validate: async ({ auth }) => {
    // Validate the API key
    const response = await fetch('https://api.example.com/validate', {
      headers: { Authorization: `Bearer ${auth}` }
    });

    if (!response.ok) {
      return {
        valid: false,
        error: 'Invalid API key'
      };
    }

    return { valid: true };
  }
});

export const myCustomApi = createPiece({
  displayName: 'My Custom API',
  auth: customApiAuth,
  minimumSupportedRelease: '0.20.0',
  logoUrl: 'https://example.com/logo.png',
  authors: ['your-name'],
  description: 'Connect to My Custom API for resource management',
  actions: [createCustomResource, getCustomResource, listCustomResources],
  triggers: [resourceCreatedTrigger]
});
```

```typescript
// pieces/my-custom-api/src/lib/actions/create-resource.ts
import { createAction, Property } from '@activepieces/pieces-framework';
import { customApiAuth } from '../../index';

export const createCustomResource = createAction({
  name: 'create_resource',
  displayName: 'Create Resource',
  description: 'Create a new resource in My Custom API',
  auth: customApiAuth,
  props: {
    name: Property.ShortText({
      displayName: 'Resource Name',
      required: true,
      description: 'The name of the resource'
    }),
    type: Property.Dropdown({
      displayName: 'Resource Type',
      required: true,
      refreshers: [],
      options: async () => ({
        options: [
          { label: 'Document', value: 'document' },
          { label: 'Image', value: 'image' },
          { label: 'Video', value: 'video' }
        ]
      })
    }),
    tags: Property.Array({
      displayName: 'Tags',
      required: false,
      description: 'Tags to categorize the resource'
    }),
    metadata: Property.Object({
      displayName: 'Metadata',
      required: false,
      description: 'Additional metadata for the resource'
    }),
    content: Property.LongText({
      displayName: 'Content',
      required: true,
      description: 'The content of the resource'
    })
  },
  async run(context) {
    const { auth, propsValue } = context;

    const response = await fetch('https://api.example.com/resources', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${auth}`
      },
      body: JSON.stringify({
        name: propsValue.name,
        type: propsValue.type,
        tags: propsValue.tags || [],
        metadata: propsValue.metadata || {},
        content: propsValue.content
      })
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Failed to create resource: ${error}`);
    }

    const result = await response.json();

    return {
      id: result.id,
      name: result.name,
      type: result.type,
      created_at: result.created_at,
      url: result.url
    };
  }
});
```

```typescript
// pieces/my-custom-api/src/lib/triggers/resource-created.ts
import {
  createTrigger,
  TriggerStrategy,
  Property
} from '@activepieces/pieces-framework';
import { customApiAuth } from '../../index';

export const resourceCreatedTrigger = createTrigger({
  name: 'resource_created',
  displayName: 'Resource Created',
  description: 'Triggers when a new resource is created',
  auth: customApiAuth,
  props: {
    resourceType: Property.Dropdown({
      displayName: 'Resource Type',
      required: false,
      refreshers: [],
      options: async () => ({
        options: [
          { label: 'All Types', value: 'all' },
          { label: 'Document', value: 'document' },
          { label: 'Image', value: 'image' },
          { label: 'Video', value: 'video' }
        ]
      })
    })
  },
  type: TriggerStrategy.WEBHOOK,
  async onEnable(context) {
    const { auth, propsValue, webhookUrl, store } = context;

    // Register webhook with the external API
    const response = await fetch('https://api.example.com/webhooks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${auth}`
      },
      body: JSON.stringify({
        url: webhookUrl,
        events: ['resource.created'],
        filter: propsValue.resourceType !== 'all'
          ? { type: propsValue.resourceType }
          : undefined
      })
    });

    const webhook = await response.json();

    // Store webhook ID for cleanup
    await store.put('webhookId', webhook.id);
  },
  async onDisable(context) {
    const { auth, store } = context;

    const webhookId = await store.get('webhookId');
    if (webhookId) {
      await fetch(`https://api.example.com/webhooks/${webhookId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${auth}`
        }
      });
    }
  },
  async run(context) {
    const { payload } = context;

    return [
      {
        id: payload.body.data.id,
        name: payload.body.data.name,
        type: payload.body.data.type,
        created_at: payload.body.data.created_at,
        created_by: payload.body.data.created_by
      }
    ];
  },
  sampleData: {
    id: 'res_123456',
    name: 'Sample Resource',
    type: 'document',
    created_at: '2026-01-17T10:00:00Z',
    created_by: 'user_789'
  }
});
```

### 7. Approval Flows

```typescript
// Human approval workflow
const approvalFlow = {
  "displayName": "Expense Approval Workflow",
  "trigger": {
    "name": "webhook",
    "type": "WEBHOOK",
    "settings": {},
    "displayName": "New Expense Request"
  },
  "steps": [
    {
      "name": "validate_expense",
      "type": "CODE",
      "settings": {
        "input": {
          "expense": "{{trigger.body}}"
        },
        "sourceCode": {
          "code": `
export const code = async (inputs) => {
  const { expense } = inputs;

  return {
    ...expense,
    requires_approval: expense.amount > 500,
    approval_level: expense.amount > 5000 ? 'executive' : expense.amount > 500 ? 'manager' : 'auto',
    formatted_amount: new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(expense.amount)
  };
};`
        }
      },
      "displayName": "Validate Expense"
    },
    {
      "name": "check_approval_required",
      "type": "BRANCH",
      "settings": {
        "conditions": [
          {
            "name": "needs_approval",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{validate_expense.requires_approval}} === true"
            },
            "steps": [
              {
                "name": "send_approval_request",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-slack",
                  "actionName": "send_message",
                  "input": {
                    "channel": "#expense-approvals",
                    "blocks": [
                      {
                        "type": "header",
                        "text": {
                          "type": "plain_text",
                          "text": "Expense Approval Required"
                        }
                      },
                      {
                        "type": "section",
                        "fields": [
                          { "type": "mrkdwn", "text": "*Submitted by:*\n{{validate_expense.employee_name}}" },
                          { "type": "mrkdwn", "text": "*Amount:*\n{{validate_expense.formatted_amount}}" },
                          { "type": "mrkdwn", "text": "*Category:*\n{{validate_expense.category}}" },
                          { "type": "mrkdwn", "text": "*Description:*\n{{validate_expense.description}}" }
                        ]
                      },
                      {
                        "type": "actions",
                        "elements": [
                          {
                            "type": "button",
                            "text": { "type": "plain_text", "text": "Approve" },
                            "style": "primary",
                            "action_id": "approve_expense",
                            "value": "{{validate_expense.id}}"
                          },
                          {
                            "type": "button",
                            "text": { "type": "plain_text", "text": "Reject" },
                            "style": "danger",
                            "action_id": "reject_expense",
                            "value": "{{validate_expense.id}}"
                          }
                        ]
                      }
                    ]
                  }
                }
              },
              {
                "name": "wait_for_approval",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-approval",
                  "actionName": "wait_for_approval",
                  "input": {
                    "timeout_hours": 48,
                    "approval_link_text": "Click to review expense"
                  }
                }
              },
              {
                "name": "process_decision",
                "type": "BRANCH",
                "settings": {
                  "conditions": [
                    {
                      "name": "approved",
                      "expression": {
                        "type": "EXPRESSION",
                        "value": "{{wait_for_approval.status}} === 'APPROVED'"
                      },
                      "steps": [
                        {
                          "name": "process_reimbursement",
                          "type": "PIECE",
                          "settings": {
                            "pieceName": "@activepieces/piece-http",
                            "actionName": "send_request",
                            "input": {
                              "method": "POST",
                              "url": "{{connections.finance_api.base_url}}/reimbursements",
                              "body": {
                                "expense_id": "{{validate_expense.id}}",
                                "amount": "{{validate_expense.amount}}",
                                "employee_id": "{{validate_expense.employee_id}}",
                                "approved_by": "{{wait_for_approval.approved_by}}"
                              }
                            }
                          }
                        }
                      ]
                    },
                    {
                      "name": "rejected",
                      "expression": {
                        "type": "EXPRESSION",
                        "value": "{{wait_for_approval.status}} === 'REJECTED'"
                      },
                      "steps": [
                        {
                          "name": "notify_rejection",
                          "type": "PIECE",
                          "settings": {
                            "pieceName": "@activepieces/piece-gmail",
                            "actionName": "send_email",
                            "input": {
                              "to": "{{validate_expense.employee_email}}",
                              "subject": "Expense Request Rejected",
                              "body": "Your expense request for {{validate_expense.formatted_amount}} has been rejected."
                            }
                          }
                        }
                      ]
                    }
                  ]
                }
              }
            ]
          },
          {
            "name": "auto_approve",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{validate_expense.requires_approval}} === false"
            },
            "steps": [
              {
                "name": "auto_process",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-http",
                  "actionName": "send_request",
                  "input": {
                    "method": "POST",
                    "url": "{{connections.finance_api.base_url}}/reimbursements",
                    "body": {
                      "expense_id": "{{validate_expense.id}}",
                      "amount": "{{validate_expense.amount}}",
                      "auto_approved": true
                    }
                  }
                }
              }
            ]
          }
        ]
      },
      "displayName": "Check Approval Required"
    }
  ]
};
```

### 8. Error Handling and Retry Logic

```typescript
// Error handling patterns
const errorHandlingFlow = {
  "displayName": "Resilient API Integration",
  "trigger": {
    "name": "schedule",
    "type": "SCHEDULE",
    "settings": {
      "cronExpression": "*/15 * * * *"
    },
    "displayName": "Every 15 Minutes"
  },
  "steps": [
    {
      "name": "fetch_with_retry",
      "type": "CODE",
      "settings": {
        "input": {
          "api_url": "{{connections.external_api.base_url}}/data",
          "api_key": "{{connections.external_api.api_key}}"
        },
        "sourceCode": {
          "code": `
export const code = async (inputs) => {
  const { api_url, api_key } = inputs;
  const maxRetries = 3;
  const baseDelay = 1000;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(api_url, {
        headers: { Authorization: \`Bearer \${api_key}\` },
        signal: AbortSignal.timeout(30000)  // 30 second timeout
      });

      if (response.status === 429) {
        // Rate limited - wait and retry
        const retryAfter = parseInt(response.headers.get('Retry-After') || '60');
        if (attempt < maxRetries) {
          await new Promise(r => setTimeout(r, retryAfter * 1000));
          continue;
        }
      }

      if (!response.ok) {
        throw new Error(\`HTTP \${response.status}: \${response.statusText}\`);
      }

      const data = await response.json();
      return {
        success: true,
        data,
        attempts: attempt
      };

    } catch (error) {
      if (attempt === maxRetries) {
        return {
          success: false,
          error: error.message,
          attempts: attempt
        };
      }

      // Exponential backoff
      const delay = baseDelay * Math.pow(2, attempt - 1);
      await new Promise(r => setTimeout(r, delay));
    }
  }
};`
        }
      },
      "displayName": "Fetch with Retry"
    },
    {
      "name": "handle_result",
      "type": "BRANCH",
      "settings": {
        "conditions": [
          {
            "name": "success",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{fetch_with_retry.success}} === true"
            },
            "steps": [
              {
                "name": "process_data",
                "type": "CODE",
                "settings": {
                  "input": {
                    "data": "{{fetch_with_retry.data}}"
                  },
                  "sourceCode": {
                    "code": `
export const code = async (inputs) => {
  const { data } = inputs;
  // Process successful data
  return {
    processed: true,
    count: data.length,
    timestamp: new Date().toISOString()
  };
};`
                  }
                }
              }
            ]
          },
          {
            "name": "failure",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{fetch_with_retry.success}} === false"
            },
            "steps": [
              {
                "name": "alert_failure",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-slack",
                  "actionName": "send_message",
                  "input": {
                    "channel": "#alerts",
                    "text": "API Integration Failed after {{fetch_with_retry.attempts}} attempts. Error: {{fetch_with_retry.error}}"
                  }
                }
              },
              {
                "name": "log_failure",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-http",
                  "actionName": "send_request",
                  "input": {
                    "method": "POST",
                    "url": "{{connections.logging_api.base_url}}/errors",
                    "body": {
                      "flow": "Resilient API Integration",
                      "error": "{{fetch_with_retry.error}}",
                      "attempts": "{{fetch_with_retry.attempts}}",
                      "timestamp": "{{now}}"
                    }
                  }
                }
              }
            ]
          }
        ]
      },
      "displayName": "Handle Result"
    }
  ]
};
```

## Integration Examples

### Integration with Notion and Slack

```typescript
const notionSlackSync = {
  "displayName": "Notion to Slack Sync",
  "trigger": {
    "name": "notion_database_updated",
    "type": "PIECE_TRIGGER",
    "settings": {
      "pieceName": "@activepieces/piece-notion",
      "triggerName": "database_item_updated",
      "input": {
        "database_id": "{{connections.notion.task_database_id}}"
      }
    },
    "displayName": "Task Updated in Notion"
  },
  "steps": [
    {
      "name": "check_status_change",
      "type": "CODE",
      "settings": {
        "input": {
          "item": "{{trigger}}"
        },
        "sourceCode": {
          "code": `
export const code = async (inputs) => {
  const { item } = inputs;

  const statusProperty = item.properties?.Status;
  const currentStatus = statusProperty?.select?.name;

  return {
    task_name: item.properties?.Name?.title?.[0]?.plain_text || 'Unnamed Task',
    status: currentStatus,
    assignee: item.properties?.Assignee?.people?.[0]?.name || 'Unassigned',
    due_date: item.properties?.['Due Date']?.date?.start,
    url: item.url,
    is_completed: currentStatus === 'Done',
    is_blocked: currentStatus === 'Blocked'
  };
};`
        }
      },
      "displayName": "Extract Task Details"
    },
    {
      "name": "route_notification",
      "type": "BRANCH",
      "settings": {
        "conditions": [
          {
            "name": "task_completed",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{check_status_change.is_completed}} === true"
            },
            "steps": [
              {
                "name": "celebrate_completion",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-slack",
                  "actionName": "send_message",
                  "input": {
                    "channel": "#team-wins",
                    "text": "Task completed! {{check_status_change.task_name}} by {{check_status_change.assignee}}"
                  }
                }
              }
            ]
          },
          {
            "name": "task_blocked",
            "expression": {
              "type": "EXPRESSION",
              "value": "{{check_status_change.is_blocked}} === true"
            },
            "steps": [
              {
                "name": "alert_blockers",
                "type": "PIECE",
                "settings": {
                  "pieceName": "@activepieces/piece-slack",
                  "actionName": "send_message",
                  "input": {
                    "channel": "#blockers",
                    "text": "Task blocked: {{check_status_change.task_name}} - Assigned to {{check_status_change.assignee}}"
                  }
                }
              }
            ]
          }
        ]
      },
      "displayName": "Route Notification"
    }
  ]
};
```

## Best Practices

### 1. Flow Organization
```
flows/
├── onboarding/
│   ├── customer-onboarding.json
│   └── employee-onboarding.json
├── integrations/
│   ├── crm-sync.json
│   ├── inventory-sync.json
│   └── payment-webhooks.json
├── notifications/
│   ├── alert-routing.json
│   └── daily-reports.json
└── utilities/
    ├── data-validation.json
    └── error-handler.json
```

### 2. Error Handling Best Practices
```typescript
// Always wrap external calls in try-catch
try {
  const result = await externalApiCall();
  return { success: true, data: result };
} catch (error) {
  // Return structured error for downstream handling
  return {
    success: false,
    error: error.message,
    retryable: !error.message.includes('PERMANENT'),
    timestamp: new Date().toISOString()
  };
}
```

### 3. Security Best Practices
```yaml
# Environment variables
AP_ENCRYPTION_KEY: "32-character-secure-key"
AP_JWT_SECRET: "secure-jwt-secret"
AP_WEBHOOK_TIMEOUT_SECONDS: 30

# Use connections for all credentials
# Never hardcode API keys in flow definitions
```

### 4. Performance Tips
```typescript
// Batch operations when possible
const BATCH_SIZE = 50;
const items = inputs.items;

for (let i = 0; i < items.length; i += BATCH_SIZE) {
  const batch = items.slice(i, i + BATCH_SIZE);
  await processBatch(batch);
}

// Use appropriate timeouts
const controller = new AbortController();
setTimeout(() => controller.abort(), 30000);
```

## Troubleshooting

### Common Issues

**Issue: Flow not triggering**
```bash
# Check webhook URL is accessible
curl -X POST https://activepieces.example.com/api/v1/webhooks/your-flow-id \
  -H "Content-Type: application/json" \
  -d '{"test": true}'

# Verify flow is enabled
# Check logs in Activepieces UI
```

**Issue: Connection authentication failing**
```bash
# Test credentials manually
curl -X GET "https://api.service.com/test" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Re-authenticate connection in UI
```

**Issue: Code step timeout**
```yaml
# Increase sandbox timeout
AP_SANDBOX_RUN_TIME_SECONDS: 600
```

### Debugging Tips

```typescript
// Add logging in code steps
console.log('Input:', JSON.stringify(inputs, null, 2));
console.log('Processing step...');

// Return debug info
return {
  result: processedData,
  debug: {
    input_count: inputs.items.length,
    processing_time_ms: Date.now() - startTime
  }
};
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with comprehensive flow patterns |

## Resources

- [Activepieces Documentation](https://www.activepieces.com/docs)
- [Pieces Directory](https://www.activepieces.com/pieces)
- [GitHub Repository](https://github.com/activepieces/activepieces)
- [Community Discord](https://discord.gg/activepieces)
- [Custom Piece Development](https://www.activepieces.com/docs/developers/building-pieces)

---

*This skill provides production-ready patterns for Activepieces workflow automation, tested across enterprise integration scenarios.*
