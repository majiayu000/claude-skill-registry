---
name: n8n-syntax-workflow-json
description: >
  Use when creating workflow JSON, importing/exporting workflows, building
  workflow templates, or debugging connection issues. Prevents malformed
  IConnections nesting and invalid node parameter formats. Covers IWorkflowBase
  format, INode configuration, IConnections 3-level nesting (node name to
  connection type to output index to targets), NodeConnectionTypes (main + 12
  AI types), node parameter formats, and workflow settings.
  Keywords: n8n, workflow JSON, IWorkflowBase, INode, IConnections,
  NodeConnectionTypes, workflow templates, import, export.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n-syntax-workflow-json

## Quick Reference

### Workflow JSON Top-Level Structure (IWorkflowBase)

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | `string` | YES | Unique workflow identifier |
| `name` | `string` | YES | Human-readable workflow name |
| `active` | `boolean` | YES | Whether workflow listens for triggers |
| `isArchived` | `boolean` | YES | Whether workflow is archived |
| `nodes` | `INode[]` | YES | Array of all nodes in the workflow |
| `connections` | `IConnections` | YES | Connection map between nodes |
| `settings` | `IWorkflowSettings` | NO | Workflow-level configuration |
| `staticData` | `IDataObject` | NO | Persistent data (polling state, etc.) |
| `pinData` | `IPinData` | NO | Pinned test data for manual execution |
| `description` | `string \| null` | NO | Workflow description |
| `versionId` | `string` | NO | Version identifier |
| `meta` | `WorkflowFEMeta` | NO | Frontend metadata (template ID, etc.) |

### INode Fields

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | `string` | YES | Unique node ID (UUID format) |
| `name` | `string` | YES | Display name (MUST be unique in workflow) |
| `type` | `string` | YES | Node type (e.g., `n8n-nodes-base.httpRequest`) |
| `typeVersion` | `number` | YES | Node version number |
| `position` | `[number, number]` | YES | Canvas position `[x, y]` |
| `parameters` | `INodeParameters` | YES | Node parameter values |
| `credentials` | `INodeCredentials` | NO | Credential references |
| `disabled` | `boolean` | NO | Whether node is disabled |
| `notes` | `string` | NO | User-visible notes |
| `notesInFlow` | `boolean` | NO | Show notes on canvas |
| `webhookId` | `string` | NO | Webhook ID (webhook nodes only) |
| `retryOnFail` | `boolean` | NO | Retry on error |
| `maxTries` | `number` | NO | Max retry attempts |
| `waitBetweenTries` | `number` | NO | Milliseconds between retries |
| `alwaysOutputData` | `boolean` | NO | Output empty item if no data |
| `executeOnce` | `boolean` | NO | Execute only for first item |
| `onError` | `OnError` | NO | Error behavior strategy |
| `continueOnFail` | `boolean` | NO | Continue workflow on error |

### OnError Values

| Value | Behavior |
|-------|----------|
| `continueErrorOutput` | Route to error output |
| `continueRegularOutput` | Route to regular output with error info |
| `stopWorkflow` | Stop entire workflow execution |

### NodeConnectionType Values

| Constant | String Value | Purpose |
|----------|-------------|---------|
| `NodeConnectionTypes.Main` | `"main"` | Standard data flow |
| `NodeConnectionTypes.AiAgent` | `"ai_agent"` | AI agent connection |
| `NodeConnectionTypes.AiChain` | `"ai_chain"` | AI chain connection |
| `NodeConnectionTypes.AiDocument` | `"ai_document"` | AI document loader |
| `NodeConnectionTypes.AiEmbedding` | `"ai_embedding"` | AI embedding model |
| `NodeConnectionTypes.AiLanguageModel` | `"ai_languageModel"` | AI language model |
| `NodeConnectionTypes.AiMemory` | `"ai_memory"` | AI memory store |
| `NodeConnectionTypes.AiOutputParser` | `"ai_outputParser"` | AI output parser |
| `NodeConnectionTypes.AiRetriever` | `"ai_retriever"` | AI retriever |
| `NodeConnectionTypes.AiReranker` | `"ai_reranker"` | AI reranker |
| `NodeConnectionTypes.AiTextSplitter` | `"ai_textSplitter"` | AI text splitter |
| `NodeConnectionTypes.AiTool` | `"ai_tool"` | AI tool |
| `NodeConnectionTypes.AiVectorStore` | `"ai_vectorStore"` | AI vector store |

### Critical Warnings

**NEVER** use node `id` values as connection keys -- connections are keyed by node **name**, not ID. Using IDs silently produces broken workflows.

**NEVER** omit the `type` field in connection targets -- every `IConnection` object MUST have `node`, `type`, AND `index`. Missing `type` causes runtime errors.

**NEVER** duplicate node names within a workflow -- each `name` field MUST be unique. n8n uses names as connection keys, so duplicates break the connection map.

**ALWAYS** use the 3-level nesting for connections: `sourceName → connectionType → outputIndex → targets[]`. Flat or 2-level structures are invalid.

**ALWAYS** set `typeVersion` to a valid version for the node type. Omitting or using an unsupported version causes the node to fail silently or use unexpected defaults.

---

## IConnections Format (3-Level Nesting)

This is the **#1 source of errors** when generating workflow JSON. The connection format uses three nesting levels:

```
Level 1: Source node NAME (string key)
  Level 2: Connection TYPE (string key, usually "main")
    Level 3: Output INDEX (array position)
      → Array of target connections [{node, type, index}]
```

### TypeScript Interface

```typescript
// Level 1: Keyed by SOURCE node name
interface IConnections {
    [sourceNodeName: string]: INodeConnections;
}

// Level 2: Keyed by connection type
interface INodeConnections {
    [connectionType: string]: NodeInputConnections;
}

// Level 3: Array indexed by output index
type NodeInputConnections = Array<IConnection[] | null>;

// Individual connection target
interface IConnection {
    node: string;           // Destination node NAME
    type: NodeConnectionType; // Connection type at destination
    index: number;          // Destination INPUT index
}
```

### Visual Breakdown

```json
{
    "connections": {
        "HTTP Request": {          // Level 1: source node name
            "main": [              // Level 2: connection type
                [                  // Level 3: output index 0
                    {
                        "node": "Set",       // target node name
                        "type": "main",      // target connection type
                        "index": 0           // target input index
                    }
                ]
            ]
        }
    }
}
```

### Multi-Output Node (IF Node)

```json
{
    "IF": {
        "main": [
            [{"node": "True Handler", "type": "main", "index": 0}],
            [{"node": "False Handler", "type": "main", "index": 0}]
        ]
    }
}
```

- Output index `0` = true branch → routes to "True Handler"
- Output index `1` = false branch → routes to "False Handler"

### Fan-Out (One Output to Multiple Nodes)

```json
{
    "Trigger": {
        "main": [
            [
                {"node": "Branch A", "type": "main", "index": 0},
                {"node": "Branch B", "type": "main", "index": 0}
            ]
        ]
    }
}
```

Multiple targets in the SAME output index array means parallel fan-out.

### AI Node Connections

AI nodes use typed connections instead of `"main"`:

```json
{
    "OpenAI Chat Model": {
        "ai_languageModel": [
            [{"node": "AI Agent", "type": "ai_languageModel", "index": 0}]
        ]
    },
    "Calculator Tool": {
        "ai_tool": [
            [{"node": "AI Agent", "type": "ai_tool", "index": 0}]
        ]
    },
    "Window Buffer Memory": {
        "ai_memory": [
            [{"node": "AI Agent", "type": "ai_memory", "index": 0}]
        ]
    }
}
```

---

## Workflow Settings

```typescript
interface IWorkflowSettings {
    timezone?: 'DEFAULT' | string;              // e.g., "Europe/Amsterdam"
    errorWorkflow?: 'DEFAULT' | string;         // Workflow ID to run on error
    callerIds?: string;                         // Allowed caller workflow IDs
    callerPolicy?: CallerPolicy;                // Sub-workflow access
    saveDataErrorExecution?: SaveDataExecution;  // "all" | "none" | "DEFAULT"
    saveDataSuccessExecution?: SaveDataExecution;
    saveManualExecutions?: 'DEFAULT' | boolean;
    saveExecutionProgress?: 'DEFAULT' | boolean;
    executionTimeout?: number;                  // Timeout in seconds
    executionOrder?: 'v0' | 'v1';              // ALWAYS use 'v1' for new workflows
}
```

**ALWAYS** set `executionOrder` to `"v1"` for new workflows. The `"v0"` algorithm has known edge cases with complex branching.

---

## Decision Tree: Building Workflow JSON

```
START: Creating workflow JSON
├── Define all nodes first
│   ├── Each node MUST have: id, name, type, typeVersion, position, parameters
│   ├── Each name MUST be unique across the workflow
│   └── Use UUID format for id fields
├── Build connections after nodes
│   ├── Is this a standard data flow?
│   │   └── YES → Use "main" as connection type
│   ├── Is this an AI sub-node connection?
│   │   └── YES → Use the specific ai_* connection type
│   ├── Does the source node have multiple outputs?
│   │   └── YES → Add entries at each output index position
│   └── Does one output go to multiple nodes?
│       └── YES → Add multiple targets in the same output index array
└── Add settings
    └── ALWAYS include executionOrder: "v1"
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- IWorkflowBase, INode, IConnections, NodeConnectionType interface details
- [references/examples.md](references/examples.md) -- Complete workflow JSON examples (minimal, multi-output, AI workflow)
- [references/anti-patterns.md](references/anti-patterns.md) -- Common JSON structure mistakes and connection format errors

### Official Sources

- https://docs.n8n.io/workflows/
- https://docs.n8n.io/api/
- https://github.com/n8n-io/n8n (packages/workflow/src/interfaces.ts)
