---
name: interactor-workflows
description: Build state-machine based automation with human-in-the-loop support through Interactor. Use when implementing approval flows, multi-step processes, automated pipelines, or any workflow requiring user input at specific stages.
author: Interactor Integration Guide
---

# Interactor Workflows Skill

Build state-machine based automations with human-in-the-loop support for multi-step business processes.

## When to Use

- **Approval Flows**: Multi-level approval processes (expense reports, purchase orders)
- **Onboarding Workflows**: Step-by-step user or employee onboarding
- **Order Processing**: Order fulfillment with status tracking
- **Support Escalation**: Ticket routing with human handoffs
- **Document Processing**: Review and approval pipelines
- **Any Multi-Step Process**: Processes requiring conditional logic and user input

## Prerequisites

- Interactor authentication configured (see `interactor-auth` skill)
- Understanding of state machines and workflow concepts
- Webhook endpoint for workflow notifications (recommended)

## Overview

Workflows consist of:

| Component | Description |
|-----------|-------------|
| **States** | Steps in your process (action, halting, terminal) |
| **Transitions** | Rules for moving between states |
| **Instances** | Running executions of a workflow |
| **Threads** | Parallel execution paths within an instance |

---

## Instructions

### Step 1: Create a Workflow Definition

```bash
curl -X POST https://core.interactor.com/api/v1/workflows \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "approval_workflow",
    "initial_state": "request",
    "ai_guidance": "This workflow handles approval requests. Route based on amount thresholds.",
    "states": {
      "request": {
        "type": "action",
        "logic": {
          "type": "script",
          "code": "return { request_id: input.id, amount: input.amount, status: \"pending\", submitted_at: new Date().toISOString() }"
        },
        "transitions": [
          { "target": "await_approval" }
        ]
      },
      "await_approval": {
        "type": "halting",
        "presentation": {
          "type": "form",
          "title": "Approval Required",
          "description": "Please review and approve or reject this request.",
          "fields": [
            { "name": "approved", "type": "boolean", "label": "Approve this request?" },
            { "name": "comment", "type": "string", "label": "Comment (optional)", "multiline": true }
          ]
        },
        "transitions": [
          { "target": "approved", "condition": { "field": "approved", "equals": true } },
          { "target": "rejected" }
        ]
      },
      "approved": {
        "type": "terminal",
        "on_enter": {
          "type": "http",
          "method": "POST",
          "url": "https://yourapp.com/api/webhooks/approval-complete",
          "body": { "request_id": "${workflow_data.request_id}", "status": "approved" }
        }
      },
      "rejected": {
        "type": "terminal",
        "on_enter": {
          "type": "http",
          "method": "POST",
          "url": "https://yourapp.com/api/webhooks/approval-complete",
          "body": { "request_id": "${workflow_data.request_id}", "status": "rejected" }
        }
      }
    }
  }'
```

**Response:**
```json
{
  "data": {
    "name": "approval_workflow",
    "version_id": "v_abc123",
    "status": "draft",
    "created_at": "2026-01-20T12:00:00Z"
  }
}
```

### State Types

| Type | Description | Behavior |
|------|-------------|----------|
| `action` | Executes logic automatically | Runs logic, then transitions immediately |
| `halting` | Pauses for external input | Waits for `resume` call with user input |
| `terminal` | End state | Workflow completes, no further transitions |

> **Note**: The `on_enter` property shown in terminal states (for triggering HTTP callbacks on completion) is an optional enhancement. Verify availability with your Interactor version.

### Step 2: Validate Without Saving

Test a workflow definition before creating it:

```bash
curl -X POST https://core.interactor.com/api/v1/workflows/validate \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_workflow",
    "initial_state": "start",
    "states": {
      "start": {
        "type": "action",
        "logic": { "type": "script", "code": "return { message: \"Hello\" }" },
        "transitions": [{ "target": "end" }]
      },
      "end": {
        "type": "terminal"
      }
    }
  }'
```

**Response (success):**
```json
{
  "data": {
    "valid": true
  }
}
```

**Response (error):**
```json
{
  "data": {
    "valid": false,
    "errors": [
      {
        "path": "states.start.transitions[0].target",
        "message": "Target state 'nonexistent' does not exist"
      }
    ]
  }
}
```

### Step 3: List Workflows

```bash
curl https://core.interactor.com/api/v1/workflows \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "workflows": [
      {
        "name": "approval_workflow",
        "latest_version_id": "v_abc123",
        "published_version_id": "v_abc123",
        "created_at": "2026-01-20T12:00:00Z"
      },
      {
        "name": "onboarding_workflow",
        "latest_version_id": "v_def456",
        "published_version_id": null,
        "created_at": "2026-01-19T10:00:00Z"
      }
    ]
  }
}
```

### Step 4: List Versions

```bash
curl https://core.interactor.com/api/v1/workflows/approval_workflow/versions \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "versions": [
      {
        "version_id": "v_abc123",
        "status": "draft",
        "created_at": "2026-01-20T12:00:00Z"
      },
      {
        "version_id": "v_def456",
        "status": "published",
        "created_at": "2026-01-19T10:00:00Z"
      }
    ]
  }
}
```

### Step 5: Publish a Version

Workflows must be published before they can be executed:

```bash
curl -X POST https://core.interactor.com/api/v1/workflows/approval_workflow/versions/v_abc123/publish \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "version_id": "v_abc123",
    "status": "published",
    "published_at": "2026-01-20T12:05:00Z"
  }
}
```

---

## Workflow Instances

Instances are running executions of a workflow.

### Create Instance

Start a new workflow execution:

```bash
curl -X POST https://core.interactor.com/api/v1/workflows/approval_workflow/instances \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "user_123",
    "input": {
      "id": "req_456",
      "amount": 5000,
      "requester": "john@example.com",
      "description": "New laptop for development"
    }
  }'
```

**Response:**
```json
{
  "data": {
    "id": "inst_xyz",
    "workflow_name": "approval_workflow",
    "version_id": "v_abc123",
    "namespace": "user_123",
    "status": "halted",
    "current_state": "await_approval",
    "workflow_data": {
      "request_id": "req_456",
      "amount": 5000,
      "status": "pending",
      "submitted_at": "2026-01-20T12:00:00Z"
    },
    "created_at": "2026-01-20T12:00:00Z"
  }
}
```

### Instance Status Values

| Status | Description |
|--------|-------------|
| `running` | Actively executing (in an action state) |
| `halted` | Paused, waiting for external input |
| `completed` | Finished successfully (reached terminal state) |
| `failed` | Terminated due to error |
| `cancelled` | Manually cancelled |

### List Instances

```bash
curl https://core.interactor.com/api/v1/workflows/instances \
  -H "Authorization: Bearer <token>"
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `namespace` | string | Filter by namespace |
| `workflow_name` | string | Filter by workflow |
| `status` | string | `running`, `halted`, `completed`, `failed`, `cancelled` |

**Example - List halted instances for a user:**
```bash
curl "https://core.interactor.com/api/v1/workflows/instances?namespace=user_123&status=halted" \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "instances": [
      {
        "id": "inst_xyz",
        "workflow_name": "approval_workflow",
        "status": "halted",
        "current_state": "await_approval",
        "created_at": "2026-01-20T12:00:00Z"
      },
      {
        "id": "inst_abc",
        "workflow_name": "onboarding_workflow",
        "status": "halted",
        "current_state": "verify_email",
        "created_at": "2026-01-19T15:30:00Z"
      }
    ]
  }
}
```

### Get Instance

```bash
curl https://core.interactor.com/api/v1/workflows/instances/inst_xyz \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "id": "inst_xyz",
    "workflow_name": "approval_workflow",
    "version_id": "v_abc123",
    "namespace": "user_123",
    "status": "halted",
    "current_state": "await_approval",
    "workflow_data": {
      "request_id": "req_456",
      "amount": 5000,
      "status": "pending"
    },
    "halting_presentation": {
      "type": "form",
      "title": "Approval Required",
      "description": "Please review and approve or reject this request.",
      "fields": [
        { "name": "approved", "type": "boolean", "label": "Approve this request?" },
        { "name": "comment", "type": "string", "label": "Comment (optional)", "multiline": true }
      ]
    },
    "threads": [
      {
        "id": "thread_main",
        "status": "halted",
        "current_state": "await_approval"
      }
    ],
    "history": [
      {
        "state": "request",
        "entered_at": "2026-01-20T12:00:00Z",
        "exited_at": "2026-01-20T12:00:01Z",
        "transition": "await_approval"
      },
      {
        "state": "await_approval",
        "entered_at": "2026-01-20T12:00:01Z"
      }
    ],
    "created_at": "2026-01-20T12:00:00Z"
  }
}
```

---

## Resuming Workflows

When a workflow reaches a halting state, it waits for external input.

### Resume with Input

```bash
curl -X POST https://core.interactor.com/api/v1/workflows/instances/inst_xyz/resume \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "approved": true,
      "comment": "Looks good, approved for Q1 budget"
    }
  }'
```

**Response:**
```json
{
  "data": {
    "id": "inst_xyz",
    "status": "completed",
    "current_state": "approved",
    "workflow_data": {
      "request_id": "req_456",
      "amount": 5000,
      "status": "pending",
      "approved": true,
      "comment": "Looks good, approved for Q1 budget"
    }
  }
}
```

The workflow continues execution based on the input and transition conditions.

### Cancel Instance

```bash
curl -X POST https://core.interactor.com/api/v1/workflows/instances/inst_xyz/cancel \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "id": "inst_xyz",
    "status": "cancelled",
    "cancelled_at": "2026-01-20T12:30:00Z"
  }
}
```

---

## Threads

Workflows can have parallel execution paths (threads).

### List Threads

```bash
curl https://core.interactor.com/api/v1/workflows/instances/inst_xyz/threads \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "threads": [
      {
        "id": "thread_main",
        "status": "halted",
        "current_state": "await_approval"
      },
      {
        "id": "thread_finance",
        "status": "completed",
        "current_state": "finance_approved"
      }
    ]
  }
}
```

### Resume Specific Thread

For workflows with multiple parallel threads:

```bash
curl -X POST https://core.interactor.com/api/v1/workflows/instances/inst_xyz/threads/thread_1/resume \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "department_approved": true
    }
  }'
```

**Response:**
```json
{
  "data": {
    "id": "inst_xyz",
    "status": "running",
    "threads": [
      {
        "id": "thread_1",
        "status": "completed",
        "current_state": "department_approved"
      },
      {
        "id": "thread_2",
        "status": "halted",
        "current_state": "await_finance_approval"
      }
    ]
  }
}
```

---

## History API

Query workflow execution history for debugging, monitoring, and audit.

### List History Events

```bash
curl https://core.interactor.com/api/v1/workflows/instances/inst_xyz/history \
  -H "Authorization: Bearer <token>"
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Max events (default: 100, max: 1000) |
| `cursor` | string | Pagination cursor |
| `types` | string | Filter by type: `transition`, `step`, `halt`, `error`, `lifecycle` |
| `since` | ISO8601 | Events after this timestamp |
| `until` | ISO8601 | Events before this timestamp |
| `thread` | string | Filter to specific thread |
| `include_data` | boolean | Include workflow_data snapshots |

**Response:**
```json
{
  "data": {
    "instance_id": "inst_xyz",
    "workflow_id": "wf_abc",
    "status": "completed",
    "events": [
      {
        "id": "evt_01HX...",
        "type": "lifecycle",
        "subtype": "created",
        "timestamp": "2026-01-20T12:00:00Z",
        "initial_state": "request"
      },
      {
        "id": "evt_01HX...",
        "type": "transition",
        "subtype": "state_change",
        "from_state": "request",
        "to_state": "processing",
        "trigger": "automatic",
        "changes": {
          "updated": {"status": {"from": "pending", "to": "processing"}}
        }
      }
    ],
    "pagination": {"has_more": false, "next_cursor": null}
  }
}
```

### Get Single Event

```bash
curl https://core.interactor.com/api/v1/workflows/instances/inst_xyz/events/evt_01HX... \
  -H "Authorization: Bearer <token>"
```

Add `?include_data=true` to include the `workflow_data` snapshot at that point.

### Error Dashboard

Query errors across all workflows:

```bash
curl "https://core.interactor.com/api/v1/workflows/errors?since=2026-01-20T00:00:00Z" \
  -H "Authorization: Bearer <token>"
```

---

## Halting Instructions

When a workflow halts, you can configure how the halting message is generated and presented to users.

### AI-Generated Instructions

Use AI to dynamically generate contextual messages based on workflow data:

```json
{
  "await_approval": {
    "type": "halting",
    "halting_instructions": {
      "type": "ai",
      "config": {
        "prompt": "Summarize this order and ask the user to approve or reject it.",
        "model": "claude-3-haiku-20240307",
        "include_data_paths": ["order", "customer", "risk_score"]
      }
    },
    "transition_mode": "selection",
    "transitions": [
      {"key": "approve", "to": "approved", "description": "Approve the order"},
      {"key": "reject", "to": "rejected", "description": "Reject the order"}
    ]
  }
}
```

**Simple format** - treats `instruction` as an AI prompt:

```json
{
  "halting_instructions": {
    "instruction": "Tell the user the strategy is ready for review. Highlight key metrics and risks.",
    "include_data": ["strategy", "benchmarks", "risk_assessment"]
  }
}
```

### Static Message Instructions

For static messages without AI generation:

```json
{
  "halting_instructions": {
    "type": "message",
    "config": {
      "title": "Approval Required",
      "message": "This order exceeds the automatic approval threshold and requires manual review."
    }
  }
}
```

### Halted Response

When halted, the API response includes `halted_options`:

```json
{
  "status": "halted",
  "halted_at_state": "await_approval",
  "halted_options": {
    "instruction": "Order #123 for $150.00 from Acme Corp is ready. Risk score: Low (23).",
    "include_data": ["order", "customer"],
    "transition_mode": "selection",
    "choices": [
      {"key": "approve", "description": "Approve the order", "to": "approved"},
      {"key": "reject", "description": "Reject the order", "to": "rejected"}
    ],
    "generated": true
  }
}
```

| Field | Description |
|-------|-------------|
| `instruction` | Message to display (AI-generated or static) |
| `generated` | `true` if AI-generated, `false` if static |
| `choices` | Available transitions for selection mode |

---

## Halting Presentations (Legacy)

> **Note**: The `presentation` format is still supported for backward compatibility. New workflows should use `halting_instructions` above.

When a workflow halts, specify how to present the required input to users.

> **Note**: The `title` and `description` fields shown in presentations are optional enhancements for better UX. The core API requires only `type` and the type-specific fields (`fields`, `options`, or `message`).

### Form Presentation

```json
{
  "type": "form",
  "title": "Approval Required",
  "description": "Please review the request details and provide your decision.",
  "fields": [
    {
      "name": "approved",
      "type": "boolean",
      "label": "Approve this request?",
      "required": true
    },
    {
      "name": "amount",
      "type": "number",
      "label": "Approved Amount",
      "default": "${workflow_data.amount}",
      "min": 0,
      "max": 100000
    },
    {
      "name": "notes",
      "type": "string",
      "label": "Notes",
      "multiline": true,
      "placeholder": "Add any notes or conditions..."
    },
    {
      "name": "priority",
      "type": "select",
      "label": "Priority",
      "options": [
        { "value": "low", "label": "Low" },
        { "value": "medium", "label": "Medium" },
        { "value": "high", "label": "High" }
      ],
      "default": "medium"
    }
  ]
}
```

### Choice Presentation

```json
{
  "type": "choice",
  "title": "Select Action",
  "message": "How would you like to proceed with this request?",
  "options": [
    {
      "value": "approve",
      "label": "Approve",
      "description": "Approve the request as submitted"
    },
    {
      "value": "reject",
      "label": "Reject",
      "description": "Reject the request"
    },
    {
      "value": "escalate",
      "label": "Escalate to Manager",
      "description": "Send to manager for review"
    },
    {
      "value": "request_info",
      "label": "Request More Information",
      "description": "Ask the requester for additional details"
    }
  ]
}
```

### Message Presentation

```json
{
  "type": "message",
  "title": "Processing",
  "message": "Waiting for external system response. This may take a few minutes.",
  "show_progress": true
}
```

> **Note**: The `show_progress` field is an optional UI hint. Client implementations may ignore it if not supported.

### Field Types

| Type | Description | Additional Properties |
|------|-------------|----------------------|
| `string` | Text input | `multiline`, `placeholder`, `maxLength` |
| `number` | Numeric input | `min`, `max`, `step` |
| `boolean` | Checkbox/toggle | - |
| `select` | Dropdown selection | `options` array |
| `date` | Date picker | `minDate`, `maxDate` |
| `file` | File upload | `accept`, `maxSize` |

> **Note**: Common field properties include `required`, `default`, and `label`. Additional properties like `placeholder`, `step`, `maxLength` may vary by Interactor version. Test with `/validate` endpoint to confirm supported properties.

---

## Workflow Logic

### Script Logic

Execute JavaScript code in action states:

```json
{
  "type": "script",
  "code": "const total = input.items.reduce((sum, item) => sum + item.price, 0); const needsApproval = total > 1000; return { ...workflow_data, total, needs_approval: needsApproval, calculated_at: new Date().toISOString() };"
}
```

**Available Variables:**
- `input` - The input provided when starting or resuming the workflow
- `workflow_data` - Current accumulated workflow data
- `context` - Additional context (namespace, instance_id, etc.)

### HTTP Logic

Make external API calls:

```json
{
  "type": "http",
  "method": "POST",
  "url": "https://api.yourservice.com/process",
  "headers": {
    "Authorization": "Bearer ${secrets.API_KEY}",
    "Content-Type": "application/json"
  },
  "body": {
    "order_id": "${workflow_data.order_id}",
    "amount": "${workflow_data.amount}",
    "customer_email": "${workflow_data.customer_email}"
  },
  "timeout": 30000,
  "retry": {
    "attempts": 3,
    "backoff": "exponential"
  }
}
```

> **Note**: The `timeout` and `retry` properties are optional enhancements. The core API requires only `type`, `method`, `url`, and optionally `headers` and `body`.

### Transition Conditions

Define conditions for state transitions:

```json
{
  "transitions": [
    {
      "target": "high_value_approval",
      "condition": {
        "field": "amount",
        "operator": "gt",
        "value": 10000
      }
    },
    {
      "target": "manager_approval",
      "condition": {
        "field": "amount",
        "operator": "gt",
        "value": 1000
      }
    },
    {
      "target": "auto_approve"
    }
  ]
}
```

**Operators:**

| Operator | Description | Example |
|----------|-------------|---------|
| `equals` | Exact match | `{ "field": "status", "equals": "approved" }` |
| `not_equals` | Not equal | `{ "field": "status", "not_equals": "rejected" }` |
| `gt` | Greater than | `{ "field": "amount", "operator": "gt", "value": 1000 }` |
| `gte` | Greater than or equal | `{ "field": "amount", "operator": "gte", "value": 1000 }` |
| `lt` | Less than | `{ "field": "amount", "operator": "lt", "value": 100 }` |
| `lte` | Less than or equal | `{ "field": "amount", "operator": "lte", "value": 100 }` |
| `contains` | String contains | `{ "field": "email", "operator": "contains", "value": "@company.com" }` |
| `in` | Value in array | `{ "field": "category", "operator": "in", "value": ["A", "B", "C"] }` |

### Complex Conditions

Use `and` / `or` for complex conditions:

```json
{
  "transitions": [
    {
      "target": "vp_approval",
      "condition": {
        "and": [
          { "field": "approved", "equals": true },
          { "field": "amount", "operator": "gt", "value": 10000 }
        ]
      }
    },
    {
      "target": "approved",
      "condition": {
        "or": [
          { "field": "amount", "operator": "lte", "value": 1000 },
          {
            "and": [
              { "field": "approved", "equals": true },
              { "field": "amount", "operator": "lte", "value": 10000 }
            ]
          }
        ]
      }
    },
    {
      "target": "rejected"
    }
  ]
}
```

---

## Complete Example: Multi-Level Approval

```json
{
  "name": "purchase_approval",
  "initial_state": "submit",
  "ai_guidance": "Multi-level purchase approval workflow. Amount thresholds: <$1000 auto-approve, $1000-$10000 manager, >$10000 VP required.",
  "states": {
    "submit": {
      "type": "action",
      "logic": {
        "type": "script",
        "code": "return { ...input, submitted_at: new Date().toISOString(), status: 'pending' }"
      },
      "transitions": [
        {
          "target": "auto_approved",
          "condition": { "field": "amount", "operator": "lte", "value": 1000 }
        },
        {
          "target": "manager_approval",
          "condition": { "field": "amount", "operator": "lte", "value": 10000 }
        },
        { "target": "manager_approval" }
      ]
    },

    "manager_approval": {
      "type": "halting",
      "presentation": {
        "type": "form",
        "title": "Manager Approval Required",
        "description": "Purchase request for ${workflow_data.description} - $${workflow_data.amount}",
        "fields": [
          { "name": "approved", "type": "boolean", "label": "Approve?", "required": true },
          { "name": "comment", "type": "string", "label": "Comment", "multiline": true }
        ]
      },
      "transitions": [
        {
          "target": "vp_approval",
          "condition": {
            "and": [
              { "field": "approved", "equals": true },
              { "field": "amount", "operator": "gt", "value": 10000 }
            ]
          }
        },
        {
          "target": "approved",
          "condition": { "field": "approved", "equals": true }
        },
        { "target": "rejected" }
      ]
    },

    "vp_approval": {
      "type": "halting",
      "presentation": {
        "type": "form",
        "title": "VP Approval Required",
        "description": "High-value purchase: ${workflow_data.description} - $${workflow_data.amount}",
        "fields": [
          { "name": "approved", "type": "boolean", "label": "VP Approval", "required": true },
          { "name": "budget_code", "type": "string", "label": "Budget Code" },
          { "name": "comment", "type": "string", "label": "Comment", "multiline": true }
        ]
      },
      "transitions": [
        {
          "target": "approved",
          "condition": { "field": "approved", "equals": true }
        },
        { "target": "rejected" }
      ]
    },

    "auto_approved": {
      "type": "action",
      "logic": {
        "type": "script",
        "code": "return { ...workflow_data, status: 'approved', approved_by: 'auto', approved_at: new Date().toISOString() }"
      },
      "transitions": [
        { "target": "notify_requester" }
      ]
    },

    "approved": {
      "type": "action",
      "logic": {
        "type": "script",
        "code": "return { ...workflow_data, status: 'approved', approved_at: new Date().toISOString() }"
      },
      "transitions": [
        { "target": "notify_requester" }
      ]
    },

    "rejected": {
      "type": "action",
      "logic": {
        "type": "script",
        "code": "return { ...workflow_data, status: 'rejected', rejected_at: new Date().toISOString() }"
      },
      "transitions": [
        { "target": "notify_requester" }
      ]
    },

    "notify_requester": {
      "type": "action",
      "logic": {
        "type": "http",
        "method": "POST",
        "url": "https://yourapp.com/api/notifications",
        "body": {
          "type": "purchase_decision",
          "email": "${workflow_data.requester}",
          "status": "${workflow_data.status}",
          "amount": "${workflow_data.amount}"
        }
      },
      "transitions": [
        { "target": "complete" }
      ]
    },

    "complete": {
      "type": "terminal"
    }
  }
}
```

---

## Implementation Examples

### Elixir Implementation (Phoenix)

> **Prerequisite**: This module requires the `MyApp.Interactor.Client` module from the `interactor-auth` skill. See that skill for the HTTP client implementation.

```elixir
defmodule MyApp.Interactor.Workflows do
  @moduledoc """
  Interactor Workflow management for state-machine based automations.

  Requires MyApp.Interactor.Client from interactor-auth skill.
  """

  alias MyApp.Interactor.Client

  # ============ Workflow Definitions ============

  @doc """
  Create a new workflow definition.
  """
  def create_workflow(definition) do
    Client.post("/workflows", definition)
  end

  @doc """
  Validate a workflow definition without saving.
  """
  def validate_workflow(definition) do
    Client.post("/workflows/validate", definition)
  end

  @doc """
  List all workflows.
  """
  def list_workflows do
    case Client.get("/workflows") do
      {:ok, %{"workflows" => workflows}} -> {:ok, workflows}
      error -> error
    end
  end

  @doc """
  List versions for a workflow.
  """
  def list_versions(workflow_name) do
    case Client.get("/workflows/#{workflow_name}/versions") do
      {:ok, %{"versions" => versions}} -> {:ok, versions}
      error -> error
    end
  end

  @doc """
  Publish a workflow version.
  """
  def publish_version(workflow_name, version_id) do
    Client.post("/workflows/#{workflow_name}/versions/#{version_id}/publish", %{})
  end

  # ============ Instances ============

  @doc """
  Create a new workflow instance.
  """
  def create_instance(workflow_name, user_id, input) do
    Client.post("/workflows/#{workflow_name}/instances", %{
      namespace: "user_#{user_id}",
      input: input
    })
  end

  @doc """
  Get a workflow instance by ID.
  """
  def get_instance(instance_id) do
    Client.get("/workflows/instances/#{instance_id}")
  end

  @doc """
  List workflow instances with optional filters.
  """
  def list_instances(filters \\ %{}) do
    query_params =
      filters
      |> Enum.map(fn
        {:user_id, id} -> {"namespace", "user_#{id}"}
        {:workflow_name, name} -> {"workflow_name", name}
        {:status, status} -> {"status", status}
      end)
      |> URI.encode_query()

    path = if query_params == "", do: "/workflows/instances", else: "/workflows/instances?#{query_params}"

    case Client.get(path) do
      {:ok, %{"instances" => instances}} -> {:ok, instances}
      error -> error
    end
  end

  @doc """
  Resume a halted workflow instance with input.
  """
  def resume_instance(instance_id, input) do
    Client.post("/workflows/instances/#{instance_id}/resume", %{input: input})
  end

  @doc """
  Cancel a workflow instance.
  """
  def cancel_instance(instance_id) do
    Client.post("/workflows/instances/#{instance_id}/cancel", %{})
  end

  # ============ Threads ============

  @doc """
  List threads for an instance.
  """
  def list_threads(instance_id) do
    case Client.get("/workflows/instances/#{instance_id}/threads") do
      {:ok, %{"threads" => threads}} -> {:ok, threads}
      error -> error
    end
  end

  @doc """
  Resume a specific thread.
  """
  def resume_thread(instance_id, thread_id, input) do
    Client.post(
      "/workflows/instances/#{instance_id}/threads/#{thread_id}/resume",
      %{input: input}
    )
  end

  # ============ Helpers ============

  @doc """
  Wait for a workflow to complete or halt.
  Returns {:ok, instance} when completed/halted, {:error, reason} on failure/timeout.
  """
  def wait_for_completion(instance_id, opts \\ []) do
    timeout_ms = Keyword.get(opts, :timeout, 300_000)
    poll_interval_ms = Keyword.get(opts, :poll_interval, 2_000)
    deadline = System.monotonic_time(:millisecond) + timeout_ms

    do_wait_for_completion(instance_id, deadline, poll_interval_ms)
  end

  defp do_wait_for_completion(instance_id, deadline, poll_interval_ms) do
    if System.monotonic_time(:millisecond) >= deadline do
      {:error, :timeout}
    else
      case get_instance(instance_id) do
        {:ok, %{"status" => "completed"} = instance} ->
          {:ok, instance}

        {:ok, %{"status" => "halted"} = instance} ->
          {:ok, instance}

        {:ok, %{"status" => "failed", "error" => error}} ->
          {:error, {:workflow_failed, error}}

        {:ok, %{"status" => "cancelled"}} ->
          {:error, :cancelled}

        {:ok, %{"status" => "running"}} ->
          Process.sleep(poll_interval_ms)
          do_wait_for_completion(instance_id, deadline, poll_interval_ms)

        {:error, _} = error ->
          error
      end
    end
  end
end
```

### Elixir Usage Example

```elixir
alias MyApp.Interactor.Workflows

# Create and publish a workflow
{:ok, version} = Workflows.create_workflow(purchase_approval_definition)
{:ok, _published} = Workflows.publish_version("purchase_approval", version["version_id"])

# Start a new instance
{:ok, instance} = Workflows.create_instance(
  "purchase_approval",
  "user_123",
  %{
    id: "PO-2026-001",
    amount: 5500,
    requester: "john@example.com",
    description: "Development laptop"
  }
)

IO.puts("Workflow started: #{instance["id"]}")
IO.puts("Current state: #{instance["current_state"]}")
IO.puts("Status: #{instance["status"]}")

# Handle halted state
case instance["status"] do
  "halted" ->
    IO.puts("Waiting for approval...")
    IO.inspect(instance["halting_presentation"], label: "Presentation")

    # Simulate manager approval
    {:ok, resumed} = Workflows.resume_instance(instance["id"], %{
      approved: true,
      comment: "Approved for Q1 budget"
    })

    IO.puts("New status: #{resumed["status"]}")
    IO.puts("New state: #{resumed["current_state"]}")

  _ ->
    :ok
end
```

### Elixir LiveView Integration

First, create a component to render workflow presentations dynamically:

```elixir
defmodule MyAppWeb.WorkflowComponents do
  use Phoenix.Component

  @doc """
  Renders a workflow form based on the halting presentation.
  """
  attr :presentation, :map, required: true
  attr :form, :any, required: true

  def workflow_form(assigns) do
    ~H"""
    <.form for={@form} phx-submit="submit_input" class="space-y-4">
      <%= if @presentation["title"] do %>
        <h2 class="text-xl font-semibold"><%= @presentation["title"] %></h2>
      <% end %>
      <%= if @presentation["description"] do %>
        <p class="text-gray-600"><%= @presentation["description"] %></p>
      <% end %>

      <%= case @presentation["type"] do %>
        <% "form" -> %>
          <%= for field <- @presentation["fields"] || [] do %>
            <.workflow_field field={field} form={@form} />
          <% end %>

        <% "choice" -> %>
          <p class="font-medium"><%= @presentation["message"] %></p>
          <div class="flex flex-wrap gap-2">
            <%= for option <- @presentation["options"] || [] do %>
              <button
                type="submit"
                name="input[choice]"
                value={option["value"]}
                class="px-4 py-2 bg-[#4CD964] hover:bg-[#3DBF55] text-white rounded-full"
              >
                <%= option["label"] %>
              </button>
            <% end %>
          </div>

        <% "message" -> %>
          <p><%= @presentation["message"] %></p>
      <% end %>

      <%= if @presentation["type"] == "form" do %>
        <button type="submit" class="px-6 py-2 bg-[#4CD964] hover:bg-[#3DBF55] text-white rounded-full">
          Submit
        </button>
      <% end %>
    </.form>
    """
  end

  attr :field, :map, required: true
  attr :form, :any, required: true

  defp workflow_field(assigns) do
    ~H"""
    <div class="space-y-1">
      <label class="block font-medium">
        <%= @field["label"] %>
        <%= if @field["required"], do: "*" %>
      </label>

      <%= case @field["type"] do %>
        <% "string" -> %>
          <%= if @field["multiline"] do %>
            <textarea
              name={"input[#{@field["name"]}]"}
              class="w-full border rounded-lg p-2"
              placeholder={@field["placeholder"]}
            ><%= @field["default"] %></textarea>
          <% else %>
            <input
              type="text"
              name={"input[#{@field["name"]}]"}
              value={@field["default"]}
              placeholder={@field["placeholder"]}
              class="w-full border rounded-lg p-2"
            />
          <% end %>

        <% "number" -> %>
          <input
            type="number"
            name={"input[#{@field["name"]}]"}
            value={@field["default"]}
            min={@field["min"]}
            max={@field["max"]}
            step={@field["step"]}
            class="w-full border rounded-lg p-2"
          />

        <% "boolean" -> %>
          <input
            type="checkbox"
            name={"input[#{@field["name"]}]"}
            value="true"
            checked={@field["default"] == true}
            class="h-5 w-5"
          />

        <% "select" -> %>
          <select name={"input[#{@field["name"]}]"} class="w-full border rounded-lg p-2">
            <%= for option <- @field["options"] || [] do %>
              <option value={option["value"]} selected={option["value"] == @field["default"]}>
                <%= option["label"] %>
              </option>
            <% end %>
          </select>

        <% "date" -> %>
          <input
            type="date"
            name={"input[#{@field["name"]}]"}
            value={@field["default"]}
            min={@field["minDate"]}
            max={@field["maxDate"]}
            class="w-full border rounded-lg p-2"
          />

        <% _ -> %>
          <input
            type="text"
            name={"input[#{@field["name"]}]"}
            value={@field["default"]}
            class="w-full border rounded-lg p-2"
          />
      <% end %>
    </div>
    """
  end
end
```

Then import it in your LiveView:

```elixir
defmodule MyAppWeb.WorkflowLive.Show do
  use MyAppWeb, :live_view

  import MyAppWeb.WorkflowComponents
  alias MyApp.Interactor.Workflows

  @impl true
  def mount(%{"id" => instance_id}, _session, socket) do
    if connected?(socket) do
      # Subscribe to workflow updates via PubSub
      Phoenix.PubSub.subscribe(MyApp.PubSub, "workflow:#{instance_id}")
    end

    case Workflows.get_instance(instance_id) do
      {:ok, instance} ->
        {:ok, assign(socket, instance: instance, form: to_form(%{}))}

      {:error, _} ->
        {:ok, push_navigate(socket, to: ~p"/workflows")}
    end
  end

  @impl true
  def handle_event("submit_input", %{"input" => input}, socket) do
    instance_id = socket.assigns.instance["id"]

    case Workflows.resume_instance(instance_id, input) do
      {:ok, updated_instance} ->
        {:noreply, assign(socket, instance: updated_instance)}

      {:error, reason} ->
        {:noreply, put_flash(socket, :error, "Failed to resume: #{inspect(reason)}")}
    end
  end

  @impl true
  def handle_event("cancel", _params, socket) do
    instance_id = socket.assigns.instance["id"]

    case Workflows.cancel_instance(instance_id) do
      {:ok, _} ->
        {:noreply, push_navigate(socket, to: ~p"/workflows")}

      {:error, reason} ->
        {:noreply, put_flash(socket, :error, "Failed to cancel: #{inspect(reason)}")}
    end
  end

  @impl true
  def handle_info({:workflow_updated, instance}, socket) do
    {:noreply, assign(socket, instance: instance)}
  end

  @impl true
  def render(assigns) do
    ~H"""
    <div class="workflow-instance">
      <h1>Workflow: <%= @instance["workflow_name"] %></h1>
      <p>Status: <span class={status_class(@instance["status"])}><%= @instance["status"] %></span></p>
      <p>Current State: <%= @instance["current_state"] %></p>

      <%= if @instance["status"] == "halted" do %>
        <.workflow_form
          presentation={@instance["halting_presentation"]}
          form={@form}
        />
      <% end %>

      <%= if @instance["status"] in ["running", "halted"] do %>
        <button phx-click="cancel" class="btn-secondary">Cancel Workflow</button>
      <% end %>
    </div>
    """
  end

  defp status_class("completed"), do: "text-green-600"
  defp status_class("failed"), do: "text-red-600"
  defp status_class("cancelled"), do: "text-gray-600"
  defp status_class("halted"), do: "text-yellow-600"
  defp status_class(_), do: "text-blue-600"
end
```

---

### TypeScript Implementation

```typescript
import { InteractorClient } from './interactor-client';

export class WorkflowManager {
  private client: InteractorClient;

  constructor(client: InteractorClient) {
    this.client = client;
  }

  // ============ Workflow Definitions ============

  async createWorkflow(definition: WorkflowDefinition): Promise<WorkflowVersion> {
    return this.client.request('POST', '/workflows', definition);
  }

  async validateWorkflow(definition: WorkflowDefinition): Promise<ValidationResult> {
    return this.client.request('POST', '/workflows/validate', definition);
  }

  async listWorkflows(): Promise<Workflow[]> {
    const result = await this.client.request<{ workflows: Workflow[] }>('GET', '/workflows');
    return result.workflows;
  }

  async listVersions(workflowName: string): Promise<WorkflowVersion[]> {
    const result = await this.client.request<{ versions: WorkflowVersion[] }>(
      'GET',
      `/workflows/${workflowName}/versions`
    );
    return result.versions;
  }

  async publishVersion(workflowName: string, versionId: string): Promise<WorkflowVersion> {
    return this.client.request(
      'POST',
      `/workflows/${workflowName}/versions/${versionId}/publish`
    );
  }

  // ============ Instances ============

  async createInstance(
    workflowName: string,
    userId: string,
    input: Record<string, any>
  ): Promise<WorkflowInstance> {
    return this.client.request('POST', `/workflows/${workflowName}/instances`, {
      namespace: `user_${userId}`,
      input
    });
  }

  async getInstance(instanceId: string): Promise<WorkflowInstance> {
    return this.client.request('GET', `/workflows/instances/${instanceId}`);
  }

  async listInstances(filters?: {
    userId?: string;
    workflowName?: string;
    status?: InstanceStatus;
  }): Promise<WorkflowInstance[]> {
    const params = new URLSearchParams();
    if (filters?.userId) params.set('namespace', `user_${filters.userId}`);
    if (filters?.workflowName) params.set('workflow_name', filters.workflowName);
    if (filters?.status) params.set('status', filters.status);

    const query = params.toString();
    const result = await this.client.request<{ instances: WorkflowInstance[] }>(
      'GET',
      `/workflows/instances${query ? '?' + query : ''}`
    );
    return result.instances;
  }

  async resumeInstance(
    instanceId: string,
    input: Record<string, any>
  ): Promise<WorkflowInstance> {
    return this.client.request('POST', `/workflows/instances/${instanceId}/resume`, {
      input
    });
  }

  async cancelInstance(instanceId: string): Promise<void> {
    await this.client.request('POST', `/workflows/instances/${instanceId}/cancel`);
  }

  // ============ Threads ============

  async listThreads(instanceId: string): Promise<WorkflowThread[]> {
    const result = await this.client.request<{ threads: WorkflowThread[] }>(
      'GET',
      `/workflows/instances/${instanceId}/threads`
    );
    return result.threads;
  }

  async resumeThread(
    instanceId: string,
    threadId: string,
    input: Record<string, any>
  ): Promise<WorkflowInstance> {
    return this.client.request(
      'POST',
      `/workflows/instances/${instanceId}/threads/${threadId}/resume`,
      { input }
    );
  }

  // ============ Helpers ============

  async waitForCompletion(
    instanceId: string,
    timeoutMs: number = 300000,
    pollIntervalMs: number = 2000
  ): Promise<WorkflowInstance> {
    const startTime = Date.now();

    while (Date.now() - startTime < timeoutMs) {
      const instance = await this.getInstance(instanceId);

      if (instance.status === 'completed') {
        return instance;
      }

      if (instance.status === 'failed') {
        throw new Error(`Workflow failed: ${instance.error}`);
      }

      if (instance.status === 'cancelled') {
        throw new Error('Workflow was cancelled');
      }

      if (instance.status === 'halted') {
        // Workflow is waiting for input
        return instance;
      }

      await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
    }

    throw new Error('Workflow completion timed out');
  }
}

// Types
interface WorkflowDefinition {
  name: string;
  initial_state: string;
  ai_guidance?: string;
  states: Record<string, StateDefinition>;
}

interface StateDefinition {
  type: 'action' | 'halting' | 'terminal';
  logic?: LogicDefinition;
  presentation?: PresentationDefinition;
  transitions?: TransitionDefinition[];
  on_enter?: LogicDefinition;  // Optional - verify availability with your Interactor version
}

interface LogicDefinition {
  type: 'script' | 'http';
  code?: string;           // For script type
  method?: string;         // For http type
  url?: string;            // For http type
  headers?: Record<string, string>;  // For http type
  body?: any;              // For http type
  timeout?: number;        // Optional - for http type
  retry?: { attempts: number; backoff: 'exponential' | 'linear' };  // Optional - for http type
}

interface PresentationDefinition {
  type: 'form' | 'choice' | 'message';
  title?: string;           // Optional - for better UX
  description?: string;     // Optional - for better UX
  message?: string;         // For choice and message types
  fields?: FieldDefinition[];  // For form type
  options?: OptionDefinition[];  // For choice type
  show_progress?: boolean;  // Optional - for message type (UI hint)
}

interface FieldDefinition {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'select' | 'date' | 'file';
  label: string;
  required?: boolean;
  default?: any;
  // String type properties
  multiline?: boolean;
  placeholder?: string;
  maxLength?: number;
  // Number type properties
  min?: number;
  max?: number;
  step?: number;
  // Select type properties
  options?: OptionDefinition[];
  // Date type properties
  minDate?: string;
  maxDate?: string;
  // File type properties
  accept?: string;
  maxSize?: number;
}

interface OptionDefinition {
  value: string;
  label: string;
  description?: string;
}

interface TransitionDefinition {
  target: string;
  condition?: ConditionDefinition;
}

interface ConditionDefinition {
  field?: string;
  operator?: 'equals' | 'not_equals' | 'gt' | 'gte' | 'lt' | 'lte' | 'contains' | 'in';
  equals?: any;
  not_equals?: any;
  value?: any;
  and?: ConditionDefinition[];
  or?: ConditionDefinition[];
}

interface Workflow {
  name: string;
  latest_version_id: string;
  published_version_id?: string;
  created_at: string;
}

interface WorkflowVersion {
  version_id: string;
  status: 'draft' | 'published';
  created_at: string;
  published_at?: string;
}

interface ValidationResult {
  valid: boolean;
  errors?: Array<{ path: string; message: string }>;
}

type InstanceStatus = 'running' | 'halted' | 'completed' | 'failed' | 'cancelled';

interface WorkflowInstance {
  id: string;
  workflow_name: string;
  version_id: string;
  namespace: string;
  status: InstanceStatus;
  current_state: string;
  workflow_data: Record<string, any>;
  halting_presentation?: PresentationDefinition;
  threads: WorkflowThread[];
  history: HistoryEntry[];
  error?: string;
  created_at: string;
}

interface WorkflowThread {
  id: string;
  status: 'running' | 'halted' | 'completed';
  current_state: string;
}

interface HistoryEntry {
  state: string;
  entered_at: string;
  exited_at?: string;
  transition?: string;
}
```

### Usage Example

```typescript
const workflowManager = new WorkflowManager(interactorClient);

// Create and publish a workflow
const version = await workflowManager.createWorkflow(purchaseApprovalDefinition);
await workflowManager.publishVersion('purchase_approval', version.version_id);

// Start a new instance
const instance = await workflowManager.createInstance(
  'purchase_approval',
  'user_123',
  {
    id: 'PO-2026-001',
    amount: 5500,
    requester: 'john@example.com',
    description: 'Development laptop'
  }
);

console.log(`Workflow started: ${instance.id}`);
console.log(`Current state: ${instance.current_state}`);
console.log(`Status: ${instance.status}`);

if (instance.status === 'halted') {
  console.log('Waiting for approval...');
  console.log('Presentation:', instance.halting_presentation);

  // Simulate manager approval
  const resumed = await workflowManager.resumeInstance(instance.id, {
    approved: true,
    comment: 'Approved for Q1 budget'
  });

  console.log(`New status: ${resumed.status}`);
  console.log(`New state: ${resumed.current_state}`);
}
```

---

## Error Handling

### Workflow-Specific Errors

Common workflow errors and their resolutions:

| Error Code | HTTP Status | Description | Resolution |
|------------|-------------|-------------|------------|
| `workflow_not_found` | 404 | Workflow definition doesn't exist | Check workflow name |
| `workflow_not_published` | 400 | No published version available | Publish a version first |
| `version_not_found` | 404 | Version doesn't exist | Check version ID |
| `instance_not_found` | 404 | Instance doesn't exist | Check instance ID |
| `instance_not_halted` | 400 | Cannot resume - not halted | Check instance status |
| `invalid_transition` | 400 | Input doesn't match any condition | Check transition conditions |
| `script_error` | 500 | Error executing workflow script | Check script syntax |
| `http_error` | 500 | HTTP action failed | Check endpoint and auth |

> **See Also**: The [API Reference](#api-reference) section contains the complete canonical error table with all endpoint-specific error codes.

---

## Webhook Events & Subscription Management

### Available Events

| Event | Description | Triggered When |
|-------|-------------|----------------|
| `workflow.instance.created` | New instance started | Instance created via API |
| `workflow.instance.halted` | Waiting for input | Instance reaches halting state |
| `workflow.instance.resumed` | Instance resumed | Resume called with input |
| `workflow.instance.completed` | Finished successfully | Instance reaches terminal state |
| `workflow.instance.failed` | Terminated with error | Script/HTTP error or invalid transition |
| `workflow.instance.cancelled` | Manually cancelled | Cancel endpoint called |

### Create Webhook Subscription

```bash
curl -X POST https://core.interactor.com/api/v1/webhooks/subscriptions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourapp.com/api/webhooks/workflows",
    "events": [
      "workflow.instance.halted",
      "workflow.instance.completed",
      "workflow.instance.failed"
    ],
    "secret": "whsec_your_webhook_secret_min_32_chars",
    "namespace_filter": "user_123"
  }'
```

**Response:**
```json
{
  "data": {
    "id": "whsub_abc123",
    "url": "https://yourapp.com/api/webhooks/workflows",
    "events": ["workflow.instance.halted", "workflow.instance.completed", "workflow.instance.failed"],
    "namespace_filter": "user_123",
    "status": "active",
    "created_at": "2026-01-20T12:00:00Z"
  }
}
```

### List Webhook Subscriptions

```bash
curl https://core.interactor.com/api/v1/webhooks/subscriptions \
  -H "Authorization: Bearer <token>"
```

### Delete Webhook Subscription

```bash
curl -X DELETE https://core.interactor.com/api/v1/webhooks/subscriptions/whsub_abc123 \
  -H "Authorization: Bearer <token>"
```

### Webhook Delivery Headers

Every webhook delivery includes these headers:

| Header | Description | Example |
|--------|-------------|---------|
| `X-Interactor-Event` | Event type | `workflow.instance.halted` |
| `X-Interactor-Signature` | HMAC-SHA256 signature | `sha256=abc123...` |
| `X-Interactor-Delivery` | Unique delivery ID | `del_01F8B6XY...` |
| `X-Interactor-Timestamp` | Unix timestamp | `1705752000` |
| `X-Interactor-Retry-Count` | Retry attempt (0-based) | `0` |
| `Content-Type` | Always JSON | `application/json` |

### Webhook Payload Example (`workflow.instance.halted`)

```json
{
  "event": "workflow.instance.halted",
  "delivery_id": "del_01F8B6XY...",
  "timestamp": "2026-01-20T12:00:01Z",
  "data": {
    "instance_id": "inst_xyz",
    "workflow_name": "approval_workflow",
    "version_id": "v_abc123",
    "namespace": "user_123",
    "current_state": "await_approval",
    "workflow_data": {
      "request_id": "req_456",
      "amount": 5000,
      "status": "pending"
    },
    "halting_presentation": {
      "type": "form",
      "title": "Approval Required",
      "fields": [
        {"name": "approved", "type": "boolean", "label": "Approve this request?"},
        {"name": "comment", "type": "string", "label": "Comment"}
      ]
    }
  }
}
```

### Webhook Payload Example (`workflow.instance.completed`)

```json
{
  "event": "workflow.instance.completed",
  "delivery_id": "del_02G9C7ZW...",
  "timestamp": "2026-01-20T12:05:00Z",
  "data": {
    "instance_id": "inst_xyz",
    "workflow_name": "approval_workflow",
    "version_id": "v_abc123",
    "namespace": "user_123",
    "current_state": "approved",
    "workflow_data": {
      "request_id": "req_456",
      "amount": 5000,
      "status": "approved",
      "approved_at": "2026-01-20T12:05:00Z"
    }
  }
}
```

### Webhook Signature Verification

**Always verify webhook signatures** to ensure requests are from Interactor.

**Node.js/TypeScript:**
```typescript
import crypto from 'crypto';

function verifyWebhookSignature(
  payload: string | Buffer,
  signature: string,
  secret: string,
  timestamp: string
): boolean {
  // Protect against replay attacks (reject if older than 5 minutes)
  const timestampAge = Math.floor(Date.now() / 1000) - parseInt(timestamp, 10);
  if (timestampAge > 300) {
    return false;
  }

  // Compute expected signature
  const signedPayload = `${timestamp}.${payload}`;
  const expectedSignature = 'sha256=' + crypto
    .createHmac('sha256', secret)
    .update(signedPayload)
    .digest('hex');

  // Constant-time comparison to prevent timing attacks
  return crypto.timingSafeEqual(
    Buffer.from(expectedSignature),
    Buffer.from(signature)
  );
}

// Express middleware example
app.post('/webhooks/workflows', express.raw({ type: 'application/json' }), (req, res) => {
  const signature = req.headers['x-interactor-signature'] as string;
  const timestamp = req.headers['x-interactor-timestamp'] as string;

  if (!verifyWebhookSignature(req.body, signature, process.env.WEBHOOK_SECRET!, timestamp)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  const event = JSON.parse(req.body.toString());
  // Process event...

  res.status(200).json({ received: true });
});
```

**Elixir/Phoenix:**
```elixir
defmodule MyAppWeb.WebhookController do
  use MyAppWeb, :controller

  @webhook_secret Application.compile_env(:my_app, :webhook_secret)
  @max_age_seconds 300

  def handle(conn, _params) do
    signature = get_req_header(conn, "x-interactor-signature") |> List.first()
    timestamp = get_req_header(conn, "x-interactor-timestamp") |> List.first()
    {:ok, body, conn} = read_body(conn)

    case verify_signature(body, signature, timestamp) do
      :ok ->
        event = Jason.decode!(body)
        process_event(event)
        json(conn, %{received: true})

      {:error, reason} ->
        conn
        |> put_status(401)
        |> json(%{error: reason})
    end
  end

  defp verify_signature(payload, signature, timestamp) do
    with :ok <- verify_timestamp(timestamp),
         :ok <- verify_hmac(payload, signature, timestamp) do
      :ok
    end
  end

  defp verify_timestamp(timestamp) do
    timestamp_int = String.to_integer(timestamp)
    age = System.system_time(:second) - timestamp_int

    if age <= @max_age_seconds do
      :ok
    else
      {:error, "Timestamp too old"}
    end
  end

  defp verify_hmac(payload, signature, timestamp) do
    signed_payload = "#{timestamp}.#{payload}"
    expected = "sha256=" <> Base.encode16(
      :crypto.mac(:hmac, :sha256, @webhook_secret, signed_payload),
      case: :lower
    )

    if Plug.Crypto.secure_compare(expected, signature) do
      :ok
    else
      {:error, "Invalid signature"}
    end
  end

  defp process_event(%{"event" => "workflow.instance.halted"} = event) do
    # Handle halted workflow - notify user, etc.
    IO.inspect(event, label: "Workflow halted")
  end

  defp process_event(%{"event" => "workflow.instance.completed"} = event) do
    # Handle completed workflow
    IO.inspect(event, label: "Workflow completed")
  end

  defp process_event(event) do
    IO.inspect(event, label: "Unknown event")
  end
end
```

### Webhook Retry Policy

| Attempt | Delay | Cumulative Time |
|---------|-------|-----------------|
| 1 | Immediate | 0s |
| 2 | 30 seconds | 30s |
| 3 | 2 minutes | 2m 30s |
| 4 | 8 minutes | 10m 30s |
| 5 | 30 minutes | 40m 30s |
| 6 | 2 hours | 2h 40m 30s |

- Webhooks are retried up to **6 times** with exponential backoff
- Return `2xx` status to acknowledge receipt
- Non-2xx responses or timeouts (30s) trigger retries
- After all retries fail, the event is moved to a dead-letter queue
- Use the webhook dashboard to replay failed events

See `interactor-webhooks` skill for complete webhook management.

---

## Authentication & Authorization

### Required OAuth Scopes

| Scope | Description | Required For |
|-------|-------------|--------------|
| `workflows:read` | Read workflow definitions and instances | GET endpoints |
| `workflows:write` | Create/modify workflows and instances | POST/PUT/DELETE endpoints |
| `workflows:execute` | Create and resume instances | Instance operations |
| `webhooks:manage` | Manage webhook subscriptions | Webhook endpoints |

### Token Format

```http
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Refresh

Tokens expire after 1 hour. Refresh before expiry:

```bash
curl -X POST https://auth.interactor.com/oauth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "refresh_token",
    "refresh_token": "<refresh_token>",
    "client_id": "<client_id>"
  }'
```

### Namespace Authorization

- Instances are isolated by `namespace`
- Tokens can only access instances in namespaces they own
- Use `user_{user_id}` convention for user-specific workflows
- Use `org_{org_id}` convention for organization-wide workflows
- Service accounts can access all namespaces within their account

See `interactor-auth` skill for complete authentication setup.

---

## Idempotency & Concurrency

### Idempotency Keys

Use `Idempotency-Key` header to prevent duplicate operations:

```bash
curl -X POST https://core.interactor.com/api/v1/workflows/approval_workflow/instances \
  -H "Authorization: Bearer <token>" \
  -H "Idempotency-Key: order_123_approval_v1" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "user_123",
    "input": {"order_id": "order_123", "amount": 5000}
  }'
```

**Behavior:**
- If the same `Idempotency-Key` is used within 24 hours, the original response is returned
- Keys are scoped to the authenticated account
- Use deterministic keys based on business identifiers (e.g., `{order_id}_approval`)

**Supported Endpoints:**
- `POST /workflows/{name}/instances` (create instance)
- `POST /workflows/instances/{id}/resume` (resume instance)
- `POST /workflows/instances/{id}/threads/{thread_id}/resume` (resume thread)

### Concurrent Resume Handling

When multiple resume requests arrive simultaneously:

| Scenario | Behavior |
|----------|----------|
| Same instance, same input | Second request returns same result (idempotent) |
| Same instance, different input | First request wins, second gets `409 Conflict` |
| Different threads, same instance | Both processed (parallel execution) |

**Conflict Response:**
```json
{
  "error": {
    "code": "concurrent_modification",
    "message": "Instance was modified by another request",
    "details": {
      "current_state": "approved",
      "expected_state": "await_approval"
    },
    "request_id": "req_01F8B6..."
  }
}
```

---

## Limits & Quotas

### Workflow Definition Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Max states per workflow | 100 | Including terminal states |
| Max transitions per state | 20 | Evaluated in order |
| Max workflow name length | 64 chars | Alphanumeric, underscores, hyphens |
| Max script code size | 64 KB | Per script logic block |
| Max presentation fields | 50 | Per halting state |
| Max workflow definition size | 1 MB | Total JSON size |

### Instance Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Max `workflow_data` size | 256 KB | Accumulated across states |
| Max input payload size | 64 KB | Per resume/create call |
| Max concurrent threads | 10 | Per instance |
| Instance TTL (running) | 30 days | Auto-cancelled after |
| Instance TTL (halted) | 90 days | Auto-cancelled after |
| Max instances per namespace | 10,000 | Active instances |

### File Upload Limits (for `file` field type)

| Limit | Value |
|-------|-------|
| Max file size | 10 MB |
| Allowed MIME types | Configurable per field |
| Max files per field | 5 |
| File retention | 7 days after instance completion |

### Rate Limits

| Endpoint Category | Limit | Window |
|-------------------|-------|--------|
| Read operations | 1000 req | per minute |
| Write operations | 100 req | per minute |
| Instance creation | 50 req | per minute |
| Webhook deliveries | 1000 events | per minute per subscription |

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705752060
```

---

## Script Execution Environment

### Runtime Specification

| Property | Value |
|----------|-------|
| Runtime | JavaScript (ES2020) |
| Engine | QuickJS sandbox |
| Execution timeout | 5 seconds |
| Memory limit | 16 MB |
| Network access | **Disabled** (use HTTP logic instead) |

### Available Globals

```javascript
// Available in script context
input          // Object: Input from create/resume call
workflow_data  // Object: Accumulated workflow data
context        // Object: { namespace, instance_id, workflow_name, state_name }

// Standard JavaScript
JSON           // JSON.parse, JSON.stringify
Date           // Date constructor and methods
Math           // Math utilities
console        // console.log (for debugging, logged to instance history)
Array          // Array methods
Object         // Object methods
String         // String methods
Number         // Number methods
Boolean        // Boolean type
RegExp         // Regular expressions

// NOT available (for security)
fetch          // Use HTTP logic instead
require        // No module imports
eval           // Disabled
Function       // Constructor disabled
setTimeout     // Async not supported
setInterval    // Async not supported
```

### Accessing Secrets in Scripts

Secrets are accessed via the `secrets` object (read-only):

```javascript
// In script logic
const apiKey = secrets.MY_API_KEY;
return { ...workflow_data, api_key_present: !!apiKey };
```

> **Security**: Secrets are injected at runtime and never logged. Use HTTP logic for external calls requiring secrets.

### Script Best Practices

- Keep scripts simple and fast (<100ms recommended)
- Avoid loops over large datasets
- Delegate heavy computation to HTTP endpoints
- Use `console.log` sparingly (logs are stored in instance history)
- Return plain objects (no functions or circular references)

---

## Observability & Tracing

### Correlation IDs

Every API request returns a unique request ID:

```http
X-Request-Id: req_01F8B6XY9Z...
```

Include this ID when contacting support or debugging issues.

### Propagating Trace Context

Pass trace context to correlate across services:

```bash
curl -X POST https://core.interactor.com/api/v1/workflows/approval_workflow/instances \
  -H "Authorization: Bearer <token>" \
  -H "X-Request-Id: your-correlation-id-123" \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

The `traceparent` header (W3C Trace Context) is propagated to HTTP logic actions.

### Instance History & Logs

Each instance maintains a detailed execution history:

```json
{
  "history": [
    {
      "state": "request",
      "entered_at": "2026-01-20T12:00:00Z",
      "exited_at": "2026-01-20T12:00:01Z",
      "transition": "await_approval",
      "logs": ["Processing request req_456"],
      "duration_ms": 45
    },
    {
      "state": "await_approval",
      "entered_at": "2026-01-20T12:00:01Z",
      "input_received": {"approved": true, "comment": "LGTM"},
      "resumed_at": "2026-01-20T12:05:00Z",
      "resumed_by": "user_789"
    }
  ]
}
```

### Metrics Available

| Metric | Description |
|--------|-------------|
| `workflow.instance.created` | Counter: instances created |
| `workflow.instance.completed` | Counter: instances completed |
| `workflow.instance.failed` | Counter: instances failed |
| `workflow.state.duration` | Histogram: time in each state |
| `workflow.script.duration` | Histogram: script execution time |
| `workflow.http.duration` | Histogram: HTTP action duration |

Access metrics via the Interactor dashboard or export to your observability platform.

---

## Best Practices

### DO

- **Start simple** - Begin with linear workflows, add complexity as needed
- **Use meaningful state names** - `await_manager_approval` over `state_3`
- **Validate early** - Use `/validate` endpoint during development
- **Version carefully** - Publish new versions rather than modifying existing ones
- **Handle all paths** - Ensure every state has a valid transition or is terminal
- **Use namespaces** - Isolate workflow instances per user
- **Add AI guidance** - Help AI assistants understand your workflow's purpose

### DON'T

- **Don't modify published versions** - Create new versions instead
- **Don't create orphan states** - Every state should be reachable
- **Don't forget error handling** - Add appropriate error states
- **Don't use complex scripts** - Keep logic simple, move complexity to HTTP endpoints

---

## Output Format

When implementing workflows, provide this summary:

```markdown
## Workflow Implementation Report

**Date**: YYYY-MM-DD
**Workflow**: purchase_approval

### Definition
| Property | Value |
|----------|-------|
| Name | purchase_approval |
| Version | v_abc123 |
| Status | Published |
| States | 7 |
| Halting States | 2 |

### State Flow
```
submit → manager_approval → [vp_approval] → approved → notify → complete
                        ↘ rejected → notify → complete
```

### Implementation Checklist
- [ ] Workflow definition created
- [ ] Validation passed
- [ ] Version published
- [ ] Instance creation tested
- [ ] Resume functionality tested
- [ ] All transitions verified
- [ ] Webhook handlers configured
- [ ] Error handling implemented

### Test Scenarios
| Scenario | Input | Expected Path | Status |
|----------|-------|---------------|--------|
| Auto-approve | amount: 500 | submit → auto_approved → complete | ✓ |
| Manager only | amount: 5000 | submit → manager → approved → complete | ✓ |
| VP required | amount: 15000 | submit → manager → vp → approved → complete | ✓ |
| Rejected | amount: 5000, approved: false | submit → manager → rejected → complete | ✓ |
```

---

## API Reference

### Endpoint Summary

| Method | Endpoint | Auth | Success | Description |
|--------|----------|------|---------|-------------|
| `POST` | `/workflows` | `workflows:write` | `201` | Create workflow definition |
| `POST` | `/workflows/validate` | `workflows:read` | `200` | Validate without saving |
| `GET` | `/workflows` | `workflows:read` | `200` | List all workflows |
| `GET` | `/workflows/{name}/versions` | `workflows:read` | `200` | List workflow versions |
| `POST` | `/workflows/{name}/versions/{id}/publish` | `workflows:write` | `200` | Publish a version |
| `POST` | `/workflows/{name}/instances` | `workflows:execute` | `201` | Create instance |
| `GET` | `/workflows/instances` | `workflows:read` | `200` | List instances |
| `GET` | `/workflows/instances/{id}` | `workflows:read` | `200` | Get instance details |
| `POST` | `/workflows/instances/{id}/resume` | `workflows:execute` | `200` | Resume halted instance |
| `POST` | `/workflows/instances/{id}/cancel` | `workflows:execute` | `200` | Cancel instance |
| `GET` | `/workflows/instances/{id}/threads` | `workflows:read` | `200` | List threads |
| `POST` | `/workflows/instances/{id}/threads/{tid}/resume` | `workflows:execute` | `200` | Resume thread |
| `POST` | `/webhooks/subscriptions` | `webhooks:manage` | `201` | Create webhook |
| `GET` | `/webhooks/subscriptions` | `webhooks:manage` | `200` | List webhooks |
| `DELETE` | `/webhooks/subscriptions/{id}` | `webhooks:manage` | `204` | Delete webhook |

### Error Response Format

All errors follow this standardized format:

```json
{
  "error": {
    "code": "workflow_not_found",
    "message": "Workflow 'invalid_workflow' not found",
    "details": null,
    "request_id": "req_01F8B6XY9Z..."
  }
}
```

### Error Codes by Endpoint

| Endpoint | Error Code | HTTP | Description |
|----------|------------|------|-------------|
| All | `unauthorized` | 401 | Missing or invalid token |
| All | `forbidden` | 403 | Insufficient scopes |
| All | `rate_limited` | 429 | Rate limit exceeded |
| All | `internal_error` | 500 | Server error |
| `POST /workflows` | `invalid_workflow` | 400 | Schema validation failed |
| `POST /workflows` | `workflow_exists` | 409 | Name already taken |
| `GET /workflows/{name}/*` | `workflow_not_found` | 404 | Workflow doesn't exist |
| `POST /.../publish` | `version_not_found` | 404 | Version doesn't exist |
| `POST /.../publish` | `already_published` | 400 | Version already published |
| `POST /.../instances` | `workflow_not_published` | 400 | No published version |
| `POST /.../instances` | `namespace_quota_exceeded` | 429 | Too many instances |
| `GET /instances/{id}` | `instance_not_found` | 404 | Instance doesn't exist |
| `POST /.../resume` | `instance_not_halted` | 400 | Instance not in halted state |
| `POST /.../resume` | `invalid_transition` | 400 | Input doesn't match conditions |
| `POST /.../resume` | `concurrent_modification` | 409 | Race condition |
| `POST /.../cancel` | `instance_not_active` | 400 | Already completed/failed |
| Script execution | `script_error` | 500 | Runtime error in script |
| Script execution | `script_timeout` | 500 | Script exceeded 5s limit |
| HTTP logic | `http_error` | 500 | External request failed |
| HTTP logic | `http_timeout` | 500 | External request timed out |

---

## React Component Example

Render `halting_presentation` in React applications:

```tsx
import React from 'react';

interface Field {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'select' | 'date' | 'file';
  label: string;
  required?: boolean;
  default?: any;
  multiline?: boolean;
  placeholder?: string;
  options?: { value: string; label: string }[];
  min?: number;
  max?: number;
}

interface Option {
  value: string;
  label: string;
  description?: string;
}

interface Presentation {
  type: 'form' | 'choice' | 'message';
  title?: string;
  description?: string;
  message?: string;
  fields?: Field[];
  options?: Option[];
  show_progress?: boolean;
}

interface WorkflowFormProps {
  presentation: Presentation;
  onSubmit: (input: Record<string, any>) => void;
  onCancel?: () => void;
  isSubmitting?: boolean;
}

export function WorkflowForm({
  presentation,
  onSubmit,
  onCancel,
  isSubmitting = false
}: WorkflowFormProps) {
  const [formData, setFormData] = React.useState<Record<string, any>>(() => {
    // Initialize with defaults
    const defaults: Record<string, any> = {};
    presentation.fields?.forEach(field => {
      if (field.default !== undefined) {
        defaults[field.name] = field.default;
      }
    });
    return defaults;
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleChoice = (value: string) => {
    onSubmit({ choice: value });
  };

  const updateField = (name: string, value: any) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="workflow-form bg-white rounded-2xl shadow-md p-6">
      {presentation.title && (
        <h2 className="text-xl font-semibold mb-2">{presentation.title}</h2>
      )}
      {presentation.description && (
        <p className="text-gray-600 mb-4">{presentation.description}</p>
      )}

      {presentation.type === 'form' && (
        <form onSubmit={handleSubmit} className="space-y-4">
          {presentation.fields?.map(field => (
            <FormField
              key={field.name}
              field={field}
              value={formData[field.name]}
              onChange={(value) => updateField(field.name, value)}
            />
          ))}
          <div className="flex gap-3 pt-4">
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-6 py-2 bg-[#4CD964] hover:bg-[#3DBF55] text-white rounded-full font-medium disabled:opacity-50"
            >
              {isSubmitting ? 'Submitting...' : 'Submit'}
            </button>
            {onCancel && (
              <button
                type="button"
                onClick={onCancel}
                className="px-6 py-2 border border-gray-300 rounded-full font-medium hover:bg-gray-50"
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      )}

      {presentation.type === 'choice' && (
        <div className="space-y-3">
          {presentation.message && (
            <p className="font-medium">{presentation.message}</p>
          )}
          <div className="flex flex-wrap gap-2">
            {presentation.options?.map(option => (
              <button
                key={option.value}
                onClick={() => handleChoice(option.value)}
                disabled={isSubmitting}
                className="px-4 py-2 bg-[#4CD964] hover:bg-[#3DBF55] text-white rounded-full disabled:opacity-50"
                title={option.description}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {presentation.type === 'message' && (
        <div className="text-center py-4">
          <p>{presentation.message}</p>
          {presentation.show_progress && (
            <div className="mt-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#4CD964] mx-auto" />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function FormField({
  field,
  value,
  onChange
}: {
  field: Field;
  value: any;
  onChange: (value: any) => void;
}) {
  const baseInputClass = "w-full border rounded-lg p-2 focus:ring-2 focus:ring-[#4CD964] focus:border-transparent";

  return (
    <div className="space-y-1">
      <label className="block font-medium text-gray-700">
        {field.label}
        {field.required && <span className="text-red-500 ml-1">*</span>}
      </label>

      {field.type === 'string' && !field.multiline && (
        <input
          type="text"
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          placeholder={field.placeholder}
          required={field.required}
          className={baseInputClass}
        />
      )}

      {field.type === 'string' && field.multiline && (
        <textarea
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          placeholder={field.placeholder}
          required={field.required}
          rows={4}
          className={baseInputClass}
        />
      )}

      {field.type === 'number' && (
        <input
          type="number"
          value={value ?? ''}
          onChange={(e) => onChange(e.target.valueAsNumber)}
          min={field.min}
          max={field.max}
          required={field.required}
          className={baseInputClass}
        />
      )}

      {field.type === 'boolean' && (
        <input
          type="checkbox"
          checked={value || false}
          onChange={(e) => onChange(e.target.checked)}
          className="h-5 w-5 text-[#4CD964] rounded focus:ring-[#4CD964]"
        />
      )}

      {field.type === 'select' && (
        <select
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          required={field.required}
          className={baseInputClass}
        >
          <option value="">Select...</option>
          {field.options?.map(opt => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
      )}

      {field.type === 'date' && (
        <input
          type="date"
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          required={field.required}
          className={baseInputClass}
        />
      )}

      {field.type === 'file' && (
        <input
          type="file"
          onChange={(e) => onChange(e.target.files?.[0])}
          required={field.required}
          className={baseInputClass}
        />
      )}
    </div>
  );
}

// Usage example
function ApprovalPage({ instanceId }: { instanceId: string }) {
  const [instance, setInstance] = React.useState<any>(null);
  const [isSubmitting, setIsSubmitting] = React.useState(false);

  React.useEffect(() => {
    fetch(`/api/workflows/instances/${instanceId}`)
      .then(res => res.json())
      .then(data => setInstance(data.data));
  }, [instanceId]);

  const handleSubmit = async (input: Record<string, any>) => {
    setIsSubmitting(true);
    try {
      const res = await fetch(`/api/workflows/instances/${instanceId}/resume`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input })
      });
      const updated = await res.json();
      setInstance(updated.data);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!instance) return <div>Loading...</div>;
  if (instance.status !== 'halted') return <div>Workflow not awaiting input</div>;

  return (
    <WorkflowForm
      presentation={instance.halting_presentation}
      onSubmit={handleSubmit}
      isSubmitting={isSubmitting}
    />
  );
}
```

---

## JSON Schema Appendix

### Workflow Definition Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://core.interactor.com/schemas/workflow-definition.json",
  "title": "Workflow Definition",
  "type": "object",
  "required": ["name", "initial_state", "states"],
  "properties": {
    "name": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_-]{0,63}$",
      "description": "Unique workflow identifier"
    },
    "initial_state": {
      "type": "string",
      "description": "Starting state name"
    },
    "ai_guidance": {
      "type": "string",
      "maxLength": 1000,
      "description": "Instructions for AI assistants"
    },
    "states": {
      "type": "object",
      "additionalProperties": { "$ref": "#/$defs/state" },
      "minProperties": 1,
      "maxProperties": 100
    }
  },
  "$defs": {
    "state": {
      "type": "object",
      "required": ["type"],
      "properties": {
        "type": { "enum": ["action", "halting", "terminal"] },
        "logic": { "$ref": "#/$defs/logic" },
        "presentation": { "$ref": "#/$defs/presentation" },
        "transitions": {
          "type": "array",
          "items": { "$ref": "#/$defs/transition" },
          "maxItems": 20
        },
        "on_enter": {
          "$ref": "#/$defs/logic",
          "description": "Optional (v2.0.0+): Logic to execute when entering this state"
        }
      }
    },
    "logic": {
      "type": "object",
      "required": ["type"],
      "oneOf": [
        {
          "properties": {
            "type": { "const": "script" },
            "code": { "type": "string", "maxLength": 65536 }
          },
          "required": ["type", "code"]
        },
        {
          "properties": {
            "type": { "const": "http" },
            "method": { "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"] },
            "url": { "type": "string", "format": "uri" },
            "headers": { "type": "object" },
            "body": {},
            "timeout": { "type": "integer", "minimum": 1000, "maximum": 30000 },
            "retry": {
              "type": "object",
              "properties": {
                "attempts": { "type": "integer", "minimum": 1, "maximum": 5 },
                "backoff": { "enum": ["linear", "exponential"] }
              }
            }
          },
          "required": ["type", "method", "url"]
        }
      ]
    },
    "presentation": {
      "type": "object",
      "required": ["type"],
      "oneOf": [
        {
          "properties": {
            "type": { "const": "form" },
            "title": { "type": "string" },
            "description": { "type": "string" },
            "fields": {
              "type": "array",
              "items": { "$ref": "#/$defs/field" },
              "maxItems": 50
            }
          },
          "required": ["type", "fields"]
        },
        {
          "properties": {
            "type": { "const": "choice" },
            "title": { "type": "string" },
            "message": { "type": "string" },
            "options": {
              "type": "array",
              "items": { "$ref": "#/$defs/option" },
              "minItems": 2,
              "maxItems": 20
            }
          },
          "required": ["type", "options"]
        },
        {
          "properties": {
            "type": { "const": "message" },
            "title": { "type": "string" },
            "message": { "type": "string" },
            "show_progress": { "type": "boolean" }
          },
          "required": ["type", "message"]
        }
      ]
    },
    "field": {
      "type": "object",
      "required": ["name", "type", "label"],
      "properties": {
        "name": { "type": "string", "pattern": "^[a-z][a-z0-9_]*$" },
        "type": { "enum": ["string", "number", "boolean", "select", "date", "file"] },
        "label": { "type": "string" },
        "required": { "type": "boolean", "default": false },
        "default": {},
        "placeholder": { "type": "string" },
        "multiline": { "type": "boolean" },
        "maxLength": { "type": "integer" },
        "min": { "type": "number" },
        "max": { "type": "number" },
        "step": { "type": "number" },
        "minDate": { "type": "string", "format": "date" },
        "maxDate": { "type": "string", "format": "date" },
        "accept": { "type": "string" },
        "maxSize": { "type": "integer" },
        "options": {
          "type": "array",
          "items": { "$ref": "#/$defs/option" }
        }
      }
    },
    "option": {
      "type": "object",
      "required": ["value", "label"],
      "properties": {
        "value": { "type": "string" },
        "label": { "type": "string" },
        "description": { "type": "string" }
      }
    },
    "transition": {
      "type": "object",
      "required": ["target"],
      "properties": {
        "target": { "type": "string" },
        "condition": { "$ref": "#/$defs/condition" }
      }
    },
    "condition": {
      "type": "object",
      "oneOf": [
        {
          "properties": {
            "field": { "type": "string" },
            "equals": {}
          },
          "required": ["field", "equals"]
        },
        {
          "properties": {
            "field": { "type": "string" },
            "not_equals": {}
          },
          "required": ["field", "not_equals"]
        },
        {
          "properties": {
            "field": { "type": "string" },
            "operator": { "enum": ["gt", "gte", "lt", "lte", "contains", "in"] },
            "value": {}
          },
          "required": ["field", "operator", "value"]
        },
        {
          "properties": {
            "and": {
              "type": "array",
              "items": { "$ref": "#/$defs/condition" }
            }
          },
          "required": ["and"]
        },
        {
          "properties": {
            "or": {
              "type": "array",
              "items": { "$ref": "#/$defs/condition" }
            }
          },
          "required": ["or"]
        }
      ]
    }
  }
}
```

### Instance Response Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://core.interactor.com/schemas/workflow-instance.json",
  "title": "Workflow Instance",
  "type": "object",
  "required": ["id", "workflow_name", "status", "current_state", "created_at"],
  "properties": {
    "id": { "type": "string", "pattern": "^inst_[a-z0-9]+$" },
    "workflow_name": { "type": "string" },
    "version_id": { "type": "string" },
    "namespace": { "type": "string" },
    "status": { "enum": ["running", "halted", "completed", "failed", "cancelled"] },
    "current_state": { "type": "string" },
    "workflow_data": { "type": "object" },
    "halting_presentation": { "$ref": "workflow-definition.json#/$defs/presentation" },
    "threads": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "status": { "enum": ["running", "halted", "completed"] },
          "current_state": { "type": "string" }
        }
      }
    },
    "history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "state": { "type": "string" },
          "entered_at": { "type": "string", "format": "date-time" },
          "exited_at": { "type": "string", "format": "date-time" },
          "transition": { "type": "string" },
          "duration_ms": { "type": "integer" }
        }
      }
    },
    "error": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" }
  }
}
```

---

## Quick Reference

### Common cURL Commands

```bash
# Create and publish a workflow
curl -X POST https://core.interactor.com/api/v1/workflows \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @workflow.json

curl -X POST https://core.interactor.com/api/v1/workflows/my_workflow/versions/v_abc123/publish \
  -H "Authorization: Bearer $TOKEN"

# Start a workflow instance
curl -X POST https://core.interactor.com/api/v1/workflows/my_workflow/instances \
  -H "Authorization: Bearer $TOKEN" \
  -H "Idempotency-Key: unique-key-123" \
  -H "Content-Type: application/json" \
  -d '{"namespace": "user_123", "input": {"key": "value"}}'

# Check instance status
curl https://core.interactor.com/api/v1/workflows/instances/inst_xyz \
  -H "Authorization: Bearer $TOKEN"

# Resume a halted instance
curl -X POST https://core.interactor.com/api/v1/workflows/instances/inst_xyz/resume \
  -H "Authorization: Bearer $TOKEN" \
  -H "Idempotency-Key: resume-unique-key" \
  -H "Content-Type: application/json" \
  -d '{"input": {"approved": true, "comment": "LGTM"}}'

# List halted instances for a user
curl "https://core.interactor.com/api/v1/workflows/instances?namespace=user_123&status=halted" \
  -H "Authorization: Bearer $TOKEN"

# Cancel an instance
curl -X POST https://core.interactor.com/api/v1/workflows/instances/inst_xyz/cancel \
  -H "Authorization: Bearer $TOKEN"
```

### Elixir Quick Start

```elixir
# Start instance
{:ok, instance} = MyApp.Interactor.Workflows.create_instance("approval", user_id, %{amount: 5000})

# Resume when halted
{:ok, resumed} = MyApp.Interactor.Workflows.resume_instance(instance["id"], %{approved: true})

# Poll for completion
{:ok, final} = MyApp.Interactor.Workflows.wait_for_completion(instance["id"])
```

### TypeScript Quick Start

```typescript
const workflow = new WorkflowManager(client);

// Start instance
const instance = await workflow.createInstance('approval', 'user_123', { amount: 5000 });

// Resume when halted
if (instance.status === 'halted') {
  await workflow.resumeInstance(instance.id, { approved: true });
}

// Wait for completion
const final = await workflow.waitForCompletion(instance.id);
```

---

## FAQ

### Common Issues & Solutions

**Q: My workflow is stuck in "running" status**
- **A**: Check that all action states have transitions. A state without transitions will halt the workflow engine. Add a transition to a terminal state or fix the logic.

**Q: Transitions are not firing as expected**
- **A**: Transitions are evaluated in order. The first matching condition wins. Ensure your conditions are ordered from most specific to least specific. The last transition should typically have no condition (default path).

**Q: Script logic is timing out**
- **A**: Scripts have a 5-second limit. Move complex computations to HTTP endpoints. Use scripts only for simple data transformations and routing decisions.

**Q: Form field validation fails on the client but succeeds on the server**
- **A**: Client-side validation should match server expectations. Use the JSON Schema to generate client validators. Test with the `/validate` endpoint during development.

**Q: Webhook events are not being delivered**
- **A**: Check: (1) Subscription is active, (2) URL is publicly accessible, (3) Endpoint returns 2xx within 30s, (4) Signature verification is correct. Use webhook dashboard to see delivery logs and retry failed events.

**Q: I get "concurrent_modification" errors**
- **A**: Multiple requests tried to resume the same instance. Use idempotency keys to prevent duplicates. Design your UI to disable buttons after submission. Check instance status before resuming.

**Q: How do I handle long-running external operations?**
- **A**: Use a halting state that waits for a webhook callback. Start the operation via HTTP logic, then transition to a halting state. When your external system completes, call the resume endpoint via webhook.

### Best Practices Checklist

- [ ] Use `/validate` endpoint during development
- [ ] Test all transition paths before publishing
- [ ] Implement idempotency keys for create/resume calls
- [ ] Verify webhook signatures in your handler
- [ ] Use namespaces to isolate user data
- [ ] Keep scripts under 100ms execution time
- [ ] Monitor rate limit headers and implement backoff
- [ ] Store `request_id` for debugging and support tickets

### Version Compatibility

| Feature | Introduced | Notes |
|---------|------------|-------|
| Core workflow API | v1.0.0 | Stable |
| Webhook subscriptions | v1.1.0 | Stable |
| `on_enter` for terminal states | v2.0.0 | Optional |
| Idempotency keys | v1.2.0 | Recommended |
| Thread parallelism | v1.3.0 | Stable |
| File field type | v2.1.0 | Beta |

> **Note**: The `on_enter` property for terminal states is available in Interactor v2.0.0+. Check your version before using this feature.

---

## Related Skills

- **interactor-auth**: Setup authentication (prerequisite)
- **interactor-credentials**: Use credentials in workflow HTTP actions
- **interactor-agents**: Combine AI agents with workflows
- **interactor-webhooks**: Real-time workflow status updates
