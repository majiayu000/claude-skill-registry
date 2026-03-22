---
name: n8n-syntax-trigger-nodes
description: >
  Use when creating custom trigger nodes or implementing webhook/polling handlers
  in n8n v1.x. Prevents incorrect trigger lifecycle implementation by missing
  closeFunction or manualTriggerFunction. Covers three trigger patterns
  (event/timer, polling, webhook), ITriggerFunctions, IWebhookFunctions,
  IPollFunctions interfaces, ITriggerResponse, webhook lifecycle methods
  (checkExists/create/delete), and WebhookResponseMode types.
  Keywords: n8n, trigger node, webhook, polling, ITriggerFunctions.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Trigger Node Development

> Build custom trigger nodes for n8n v1.x using event/timer, polling, or webhook patterns.

## Quick Reference

| Pattern | Method | Interface | Description Key | Use When |
|---------|--------|-----------|-----------------|----------|
| Event/Timer | `trigger()` | `ITriggerFunctions` | `group: ['trigger']` | Listening to events, cron schedules, streams |
| Polling | `poll()` | `IPollFunctions` | `polling: true` | Periodically checking an API for new data |
| Webhook | `webhook()` | `IWebhookFunctions` | `webhooks: [...]` | External service sends HTTP requests to n8n |

### Critical Rules

- **ALWAYS** set `inputs: []` on trigger nodes — triggers have NO inputs
- **ALWAYS** include `'trigger'` in the `group` array
- **ALWAYS** double-wrap emitted data: `this.emit([[items]])` — outer array = outputs, inner array = items
- **ALWAYS** provide `manualTriggerFunction` for event triggers so "Test Workflow" works in the editor
- **ALWAYS** implement `closeFunction` when your trigger allocates resources (intervals, connections, listeners)
- **NEVER** emit single-wrapped arrays — `this.emit([items])` causes silent failures
- **NEVER** forget cleanup — leaked intervals/connections persist across workflow deactivation

## Decision Tree: Which Trigger Pattern?

```
Need a trigger node?
├── Does an EXTERNAL SERVICE call YOUR endpoint?
│   └── YES → Use WEBHOOK pattern (webhook() + IWebhookFunctions)
│       ├── Service has webhook registration API? → Add webhookMethods lifecycle
│       └── Service sends to a static URL? → Use webhooks[] description only
├── Do you need to CHECK an API periodically?
│   └── YES → Use POLLING pattern (poll() + IPollFunctions)
│       └── ALWAYS implement deduplication (track last seen ID/timestamp)
└── Do you LISTEN for events, run on schedule, or stream data?
    └── YES → Use EVENT/TIMER pattern (trigger() + ITriggerFunctions)
        └── ALWAYS implement closeFunction for cleanup
```

## Pattern 1: Event/Timer Trigger

Use `trigger()` with `ITriggerFunctions` for schedule-based or event-driven triggers.

### Minimal Structure

```typescript
import type {
    ITriggerFunctions,
    INodeType,
    INodeTypeDescription,
    ITriggerResponse,
    INodeExecutionData,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

export class MyEventTrigger implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'My Event Trigger',
        name: 'myEventTrigger',
        group: ['trigger'],          // REQUIRED for trigger nodes
        version: 1,
        inputs: [],                  // ALWAYS empty for triggers
        outputs: [NodeConnectionTypes.Main],
        defaults: { name: 'My Event Trigger' },
        properties: [/* ... */],
    };

    async trigger(this: ITriggerFunctions): Promise<ITriggerResponse> {
        const executeTrigger = () => {
            // CRITICAL: Double-wrap — [[items]]
            this.emit([[ { json: { timestamp: new Date().toISOString() } } ]]);
        };

        if (this.getMode() === 'manual') {
            // Editor "Test Workflow" mode
            return { manualTriggerFunction: async () => executeTrigger() };
        }

        // Production mode — set up persistent listener
        const intervalId = setInterval(executeTrigger, 60_000);

        // ALWAYS return closeFunction for cleanup
        return { closeFunction: async () => clearInterval(intervalId) };
    }
}
```

### ITriggerResponse Fields

| Field | Type | Purpose |
|-------|------|---------|
| `closeFunction` | `() => Promise<void>` | Cleanup when workflow deactivated. ALWAYS implement when allocating resources. |
| `manualTriggerFunction` | `() => Promise<void>` | Simulates trigger for "Test Workflow" in editor. ALWAYS implement for event triggers. |
| `manualTriggerResponse` | `Promise<INodeExecutionData[][]>` | Alternative: promise that resolves when data is emitted. |

### Emitting Data

```typescript
// CORRECT — double array wrapping
this.emit([[ { json: { key: 'value' } } ]]);

// CORRECT — multiple items in one emission
this.emit([[ { json: { id: 1 } }, { json: { id: 2 } } ]]);

// CORRECT — using helper for array conversion
this.emit([this.helpers.returnJsonArray([{ id: 1 }, { id: 2 }])]);

// WRONG — single array wrapping (SILENT FAILURE)
this.emit([{ json: { key: 'value' } }]);  // DO NOT DO THIS
```

### Error Reporting

```typescript
// Non-fatal: log error, workflow stays active
this.saveFailedExecution(error);

// Fatal: deactivates workflow, queues for reactivation with backoff
this.emitError(error);
```

## Pattern 2: Polling Trigger

Use `poll()` with `IPollFunctions` for periodic API checks.

### Minimal Structure

```typescript
export class MyPollingTrigger implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'My Polling Trigger',
        name: 'myPollingTrigger',
        group: ['trigger'],
        version: 1,
        polling: true,               // REQUIRED — marks as polling trigger
        inputs: [],
        outputs: [NodeConnectionTypes.Main],
        defaults: { name: 'My Polling Trigger' },
        properties: [
            {
                displayName: 'Poll Interval',
                name: 'pollInterval',
                type: 'options',
                default: 'every5Minutes',
                options: [
                    { name: 'Every Minute', value: 'everyMinute' },
                    { name: 'Every 5 Minutes', value: 'every5Minutes' },
                ],
            },
        ],
    };

    async poll(this: IPollFunctions): Promise<INodeExecutionData[][] | null> {
        // Return null when no new data — NEVER return empty arrays
        // Return [[items]] when new data found
    }
}
```

### Deduplication Pattern

**ALWAYS** implement deduplication for polling triggers to prevent duplicate processing.

```typescript
async poll(this: IPollFunctions): Promise<INodeExecutionData[][] | null> {
    const webhookData = this.getWorkflowStaticData('node');
    const lastTimestamp = webhookData.lastTimestamp as string | undefined;

    const items = await fetchNewItems(lastTimestamp);

    if (items.length === 0) {
        return null;  // ALWAYS return null for "no new data"
    }

    // Update stored state for next poll cycle
    webhookData.lastTimestamp = items[items.length - 1].updatedAt;

    return [items.map(item => ({ json: item }))];
}
```

> **Key**: Use `this.getWorkflowStaticData('node')` to persist state between poll cycles. This data survives workflow restarts. ALWAYS update the stored marker after processing.

## Pattern 3: Webhook Trigger

Use `webhook()` with `IWebhookFunctions` for HTTP-triggered workflows.

### Minimal Structure

```typescript
export class MyWebhookTrigger implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'My Webhook Trigger',
        name: 'myWebhookTrigger',
        group: ['trigger'],
        version: 1,
        inputs: [],
        outputs: [NodeConnectionTypes.Main],
        defaults: { name: 'My Webhook Trigger' },
        webhooks: [
            {
                name: 'default',
                httpMethod: '={{$parameter["httpMethod"] || "POST"}}',
                path: '={{$parameter["path"]}}',
                responseMode: '={{$parameter["responseMode"]}}',
            },
        ],
        properties: [/* httpMethod, path, responseMode */],
    };

    async webhook(this: IWebhookFunctions): Promise<IWebhookResponseData> {
        const body = this.getBodyData();
        return { workflowData: [[ { json: body } ]] };
    }
}
```

### WebhookResponseMode

| Mode | Behavior | Use When |
|------|----------|----------|
| `onReceived` | Respond immediately after webhook node executes | Fire-and-forget; caller does not need workflow result |
| `lastNode` | Respond after the LAST node in workflow finishes | Caller needs the final processed result |
| `responseNode` | Respond from a dedicated "Respond to Webhook" node | Need custom response body/status at a specific point |

### IWebhookFunctions Methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `getBodyData()` | `IDataObject` | Parsed request body |
| `getHeaderData()` | `IncomingHttpHeaders` | Request headers |
| `getQueryData()` | `object` | URL query parameters |
| `getParamsData()` | `object` | URL path parameters |
| `getRequestObject()` | `express.Request` | Full Express request (advanced) |
| `getResponseObject()` | `express.Response` | Full Express response (advanced, for manual response) |
| `getNodeWebhookUrl('default')` | `string` | The registered webhook URL |

### Webhook Lifecycle (webhookMethods)

For triggers that register webhooks on EXTERNAL services (e.g., GitHub, Stripe):

```typescript
webhookMethods: {
    default: {
        async checkExists(this: IHookFunctions): Promise<boolean> {
            // Return true if webhook already registered on external service
        },
        async create(this: IHookFunctions): Promise<boolean> {
            // Register webhook URL on external service
            // Store webhook ID in static data for later deletion
            const webhookUrl = this.getNodeWebhookUrl('default');
            // ... API call to register ...
            return true;
        },
        async delete(this: IHookFunctions): Promise<boolean> {
            // Remove webhook from external service on deactivation
            return true;
        },
    },
},
```

**Lifecycle**: `checkExists` runs first. If `false`, `create` runs. On workflow deactivation, `delete` runs.

### IWebhookResponseData Fields

| Field | Type | Purpose |
|-------|------|---------|
| `workflowData` | `INodeExecutionData[][]` | Data passed into the workflow |
| `webhookResponse` | `any` | Custom response sent back to the caller |
| `noWebhookResponse` | `boolean` | Set `true` if you already sent a response via `getResponseObject()` |

## Trigger Node Description Requirements

Every trigger node description MUST include:

```typescript
description: INodeTypeDescription = {
    group: ['trigger'],              // REQUIRED — identifies as trigger
    inputs: [],                      // REQUIRED — triggers have no inputs
    outputs: [NodeConnectionTypes.Main],
    // For polling triggers, add:
    polling: true,
    // For webhook triggers, add:
    webhooks: [{ name: 'default', httpMethod: '...', path: '...', responseMode: '...' }],
    // Optional but recommended:
    eventTriggerDescription: 'Waiting for events from MyService',
    activationMessage: 'Your trigger is now active and listening.',
};
```

## Reference Files

| File | Contents |
|------|----------|
| [references/methods.md](references/methods.md) | Complete ITriggerFunctions, IWebhookFunctions, IPollFunctions, ITriggerResponse, webhookMethods, WebhookResponseMode |
| [references/examples.md](references/examples.md) | Full implementations: schedule trigger, webhook trigger, polling trigger |
| [references/anti-patterns.md](references/anti-patterns.md) | Common trigger implementation mistakes and fixes |

## Sources

- n8n-io/n8n GitHub: `packages/workflow/src/interfaces.ts` — ITriggerFunctions, IWebhookFunctions, IPollFunctions, ITriggerResponse
- n8n-io/n8n GitHub: `packages/nodes-base/nodes/Schedule/ScheduleTrigger.node.ts`
- n8n-io/n8n GitHub: `packages/nodes-base/nodes/Webhook/Webhook.node.ts`
- n8n official docs: https://docs.n8n.io/integrations/creating-nodes/build/programmatic-style/
