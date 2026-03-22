---
name: n8n-core-architecture
description: >
  Use when building n8n workflows, creating custom nodes, understanding data
  flow, or debugging execution issues. Prevents incorrect INodeExecutionData
  structure and data flow mistakes. Covers item-based execution model, binary
  data handling, paired items, node types (trigger/regular), process modes
  (main/worker/queue), and workflow settings.
  Keywords: n8n, architecture, INodeExecutionData, execution model, binary data,
  paired items, trigger nodes, queue mode, workflow settings.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n-core-architecture

## Quick Reference

### Architecture Layers (n8n v1.x)

| Layer | Technology | Role |
|-------|-----------|------|
| Execution Engine | Node.js + TypeScript | Processes workflows as item sequences through nodes |
| Item Pipeline | INodeExecutionData | Carries JSON data, binary files, paired items, and errors |
| Node System | INodeType interface | Defines trigger, regular, webhook, polling, and declarative nodes |
| Expression Engine | Data Proxy | Provides `$json`, `$input`, `$binary`, `$execution`, `$workflow`, `$node` |
| Process Model | Main / Worker / Queue | Scales from single-process to distributed queue mode |
| Workflow Settings | IWorkflowSettings | Controls timezone, error handling, execution timeout, execution order |

### Execution Modes (WorkflowExecuteMode)

| Mode | Trigger |
|------|---------|
| `manual` | User clicks "Execute Workflow" in editor |
| `webhook` | HTTP webhook received |
| `trigger` | Trigger node activated (schedule, poll) |
| `retry` | Retrying a failed execution |
| `cli` | Command-line execution |
| `error` | Error workflow triggered |
| `integrated` | Sub-workflow called from another workflow |
| `internal` | Internal system execution |
| `evaluation` | Evaluation/test execution |
| `chat` | Chat-based trigger |

### Node Types

| Type | Method | Inputs | Group |
|------|--------|--------|-------|
| Regular | `execute()` | Has inputs | `['transform']`, `['input']`, `['output']` |
| Event Trigger | `trigger()` | No inputs | `['trigger']` |
| Webhook Trigger | `webhook()` | No inputs | `['trigger']` |
| Polling Trigger | `poll()` | No inputs | `['trigger']` (with `polling: true`) |
| Declarative | None (routing config) | Has inputs | Any |

### Critical Warnings

**NEVER** return a flat `INodeExecutionData[]` from `execute()` -- ALWAYS wrap in an outer array: `return [returnData]`. The outer array represents output indices (for multi-output nodes like IF/Switch).

**NEVER** mutate input items directly -- ALWAYS create new item objects. Mutating input items causes data corruption in downstream nodes that share the same reference.

**NEVER** ignore `pairedItem` in custom nodes that transform items -- ALWAYS set `pairedItem: { item: i }` to maintain item linking. Without paired items, n8n cannot trace data lineage.

**NEVER** assume `item.binary` exists -- ALWAYS check for `undefined` before accessing binary data. Not all items carry binary data.

**NEVER** use `this.getNodeParameter('param', 0)` with a hardcoded index when processing multiple items -- ALWAYS use the loop index `i` to get per-item parameter values.

**NEVER** skip `continueOnFail()` checks in custom nodes -- ALWAYS wrap item processing in try/catch and check `this.continueOnFail()` to respect user error settings.

---

## Item-Based Execution Model

### Data Flow

n8n processes data as **items**. Each node receives an array of items, processes them, and outputs an array of items:

```
Input: INodeExecutionData[]        →  Node  →  Output: INodeExecutionData[][]
[item0, item1, item2]                         [[result0, result1]]  (single output)
                                              [[trueItems], [falseItems]]  (two outputs)
```

### INodeExecutionData Structure

```typescript
interface INodeExecutionData {
    json: IDataObject;                    // REQUIRED - main data payload
    binary?: IBinaryKeyData;              // Optional file/binary data
    error?: NodeApiError | NodeOperationError;  // Error info if item errored
    pairedItem?: IPairedItemData | IPairedItemData[] | number;  // Item linking
    metadata?: {
        subExecution: RelatedExecution;   // Sub-workflow execution reference
    };
}
```

- `json` is the ONLY required field -- it contains the item's data as key-value pairs
- `binary` holds file data keyed by property name (e.g., `"data"`, `"attachment"`)
- `pairedItem` links output items back to their source input items
- `error` carries error details when an item fails processing

### execute() Return Type

The return type `INodeExecutionData[][]` is a 2D array:
- **First dimension**: output index (output 0, output 1, etc.)
- **Second dimension**: items for that output

```typescript
// Single output node (most common):
return [returnData];  // returnData is INodeExecutionData[]

// Two-output node (e.g., IF node):
return [trueItems, falseItems];

// Three-output node (e.g., Switch):
return [output0Items, output1Items, output2Items];
```

---

## Binary Data

### IBinaryData Structure

```typescript
interface IBinaryData {
    data: string;          // Base64 encoded binary data (or reference ID)
    mimeType: string;      // MIME type (e.g., "image/png", "application/pdf")
    fileType?: BinaryFileType;  // 'text' | 'json' | 'image' | 'audio' | 'video' | 'pdf' | 'html'
    fileName?: string;
    fileExtension?: string;
    fileSize?: string;
    id?: string;           // Reference ID for filesystem-stored binary
}
```

### IBinaryKeyData

Binary data on an item is stored as a keyed dictionary:

```typescript
interface IBinaryKeyData {
    [key: string]: IBinaryData;  // e.g., { "data": {...}, "attachment": {...} }
}
```

ALWAYS access binary data through the key name: `item.binary?.data` or `item.binary?.attachment`.

### Binary Helper Methods (in execute())

| Method | Purpose |
|--------|---------|
| `this.helpers.assertBinaryData(itemIndex, propertyName)` | Get binary data or throw |
| `this.helpers.getBinaryDataBuffer(itemIndex, propertyName)` | Get binary as Buffer |
| `this.helpers.detectBinaryEncoding(buffer)` | Detect text encoding |
| `this.helpers.prepareBinaryData(buffer, fileName?, mimeType?)` | Create IBinaryData from Buffer |

---

## Paired Items

### IPairedItemData Structure

```typescript
interface IPairedItemData {
    item: number;          // Index of the source item in the input
    input?: number;        // Input index (default 0)
    sourceOverwrite?: ISourceData;  // Override source node
}
```

### Setting Paired Items

ALWAYS set `pairedItem` when creating output items to maintain data lineage:

```typescript
for (let i = 0; i < items.length; i++) {
    returnData.push({
        json: { /* processed data */ },
        pairedItem: { item: i },  // Links to input item at index i
    });
}
```

For items that map to multiple source items, use an array:

```typescript
returnData.push({
    json: { /* aggregated data */ },
    pairedItem: [{ item: 0 }, { item: 1 }, { item: 2 }],
});
```

---

## Process Modes

### Single Process (Default)

- One Node.js process handles everything: webhooks, triggers, UI, and execution
- Suitable for low-volume workloads or development

### Queue Mode (Production Scaling)

- **Main process**: Handles webhooks, triggers, and UI; enqueues execution jobs
- **Worker processes**: Dequeue and execute workflows independently
- Uses **BullMQ** (Redis-backed) for job queue management

| Environment Variable | Purpose |
|---------------------|---------|
| `EXECUTIONS_MODE=queue` | Enable queue mode |
| `QUEUE_BULL_REDIS_HOST` | Redis host for job queue |
| `QUEUE_BULL_REDIS_PORT` | Redis port for job queue |
| `QUEUE_WORKER_CONCURRENCY` | Concurrent executions per worker |

---

## Workflow Settings (IWorkflowSettings)

| Setting | Type | Purpose |
|---------|------|---------|
| `timezone` | `string` | Workflow timezone (e.g., `"Europe/Amsterdam"`) |
| `errorWorkflow` | `string` | Workflow ID to execute on error |
| `executionTimeout` | `number` | Timeout in seconds |
| `executionOrder` | `'v0' \| 'v1'` | Node execution order algorithm |
| `saveDataErrorExecution` | `string` | Save policy for failed executions |
| `saveDataSuccessExecution` | `string` | Save policy for successful executions |
| `saveManualExecutions` | `boolean` | Whether to save manual test executions |
| `saveExecutionProgress` | `boolean` | Save progress during execution |
| `callerPolicy` | `CallerPolicy` | Sub-workflow access control |
| `callerIds` | `string` | Allowed caller workflow IDs |

ALWAYS set `executionOrder: 'v1'` for new workflows -- v0 is legacy and produces non-deterministic execution order.

---

## Expression Data Proxy

During execution, expressions have access to these variables:

| Variable | Type | Purpose |
|----------|------|---------|
| `$json` | `IDataObject` | Current item's JSON data |
| `$binary` | `IBinaryKeyData` | Current item's binary data |
| `$input` | `ProxyInput` | Current node's input accessor |
| `$input.all()` | `INodeExecutionData[]` | All input items |
| `$input.first()` | `INodeExecutionData` | First input item |
| `$input.last()` | `INodeExecutionData` | Last input item |
| `$input.item` | `INodeExecutionData` | Current input item |
| `$node["Name"]` | -- | Access another node's output |
| `$workflow` | -- | Workflow metadata |
| `$execution.id` | `string` | Current execution ID |
| `$execution.mode` | `'test' \| 'production'` | Execution mode |
| `$execution.resumeUrl` | `string` | URL to resume waiting executions |
| `$now` | `DateTime` | Current DateTime (Luxon) |
| `$today` | `DateTime` | Today's date (Luxon) |
| `$parameter` | `INodeParameters` | Current node's parameters |
| `$position` | `number` | Current item index |
| `$env` | -- | Environment variables |

### $execution.customData

Store and retrieve custom metadata during execution:

```typescript
$execution.customData.set("orderId", "12345");
$execution.customData.get("orderId");  // "12345"
$execution.customData.setAll({ key1: "val1", key2: "val2" });
$execution.customData.getAll();  // { key1: "val1", key2: "val2" }
```

---

## Decision Trees

### Choosing a Node Type

```
Need to START a workflow?
├── YES → Is it time-based?
│   ├── YES → Use trigger() with ITriggerFunctions (schedule trigger)
│   └── NO → Does it receive HTTP requests?
│       ├── YES → Use webhook() with IWebhookFunctions
│       └── NO → Does it poll an external service?
│           ├── YES → Use poll() with IPollFunctions (set polling: true)
│           └── NO → Use trigger() with custom event listener
└── NO → Is it a simple REST API wrapper?
    ├── YES → Use declarative node (routing config, no execute())
    └── NO → Use programmatic node with execute()
```

### Choosing Process Mode

```
How many executions per day?
├── < 1000 → Single process (default)
├── 1000-10000 → Queue mode with 1-2 workers
└── > 10000 → Queue mode with multiple workers + Redis cluster
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- INodeExecutionData, IBinaryData, IPairedItemData, IWorkflowSettings, WorkflowExecuteMode type signatures
- [references/examples.md](references/examples.md) -- Item processing, binary data handling, paired items, workflow settings examples
- [references/anti-patterns.md](references/anti-patterns.md) -- Data flow mistakes, item handling errors, common pitfalls

### Official Sources

- https://docs.n8n.io/integrations/creating-nodes/
- https://docs.n8n.io/data/data-structure/
- https://docs.n8n.io/code/builtin/data-transformation-functions/
- https://github.com/n8n-io/n8n (packages/workflow/src/interfaces.ts)
