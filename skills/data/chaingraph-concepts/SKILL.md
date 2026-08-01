---
name: chaingraph-concepts
description: Core ChainGraph domain concepts - flows, nodes, ports, edges, and execution.
  Use for ANY ChainGraph development to understand the fundamental abstractions. Explains
  what flows are, how nodes process d
---

---
name: chaingraph-concepts
description: Core ChainGraph domain concepts - flows, nodes, ports, edges, and execution. Use for ANY ChainGraph development to understand the fundamental abstractions. Explains what flows are, how nodes process data, port types (9 types), edge data transfer, and execution lifecycle. 19 FlowEventTypes, 21 ExecutionEventEnums. Triggers: chaingraph, flow, node, port, edge, execution, what is, how does, concept, architecture, event types.
---

# ChainGraph Core Concepts

ChainGraph is a flow-based programming framework for building visual computational graphs. This skill covers the fundamental domain concepts that ALL agents need to understand.

## The Four Core Abstractions

```
┌─────────────────────────────────────────────────────────────┐
│                         FLOW                                │
│  (Directed Acyclic Graph - the container)                   │
│                                                             │
│   ┌─────────┐         ┌─────────┐         ┌─────────┐      │
│   │  NODE   │         │  NODE   │         │  NODE   │      │
│   │ ┌─────┐ │  EDGE   │ ┌─────┐ │  EDGE   │ ┌─────┐ │      │
│   │ │PORT │─┼────────▶│ │PORT │─┼────────▶│ │PORT │ │      │
│   │ └─────┘ │         │ └─────┘ │         │ └─────┘ │      │
│   └─────────┘         └─────────┘         └─────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 1. Flow

A **Flow** is a directed acyclic graph (DAG) containing interconnected nodes and edges that define a computational workflow.

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier |
| `metadata` | FlowMetadata | Name, description, timestamps, version, owner |
| `nodes` | Map<string, INode> | All nodes in the flow |
| `edges` | Map<string, IEdge> | All edges connecting nodes |

### Key Methods

```typescript
// Add a node to the flow
flow.addNode(node: INode): Promise<INode>

// Connect two ports via edge
flow.connectPorts(sourceNodeId, sourcePortId, targetNodeId, targetPortId): Edge

// Subscribe to flow events
flow.onEvent(handler: (event: FlowEvent) => void): () => void

// Validate entire flow
flow.validate(): Promise<FlowValidationResult>
```

### Key Files

| File | Purpose |
|------|---------|
| `packages/chaingraph-types/src/flow/flow.ts:42` | Flow class implementation |
| `packages/chaingraph-types/src/flow/interface.ts:19-193` | IFlow interface |
| `packages/chaingraph-types/src/flow/types.ts:12-54` | FlowMetadata type |

---

## 2. Node

A **Node** is a discrete computational unit that performs a specific operation on input data and produces output. Nodes are the building blocks of flows.

### Node Lifecycle

```
Idle → Ready → Executing → Completed
                    ↓
                  Error
```

### NodeStatus Enum

```typescript
enum NodeStatus {
  Idle = 'idle',           // Initial state
  Initialized = 'initialized',
  Ready = 'ready',         // Ready to execute
  Pending = 'pending',     // Waiting for dependencies
  Executing = 'executing', // Currently running
  Completed = 'completed', // Successfully finished
  Skipped = 'skipped',     // Skipped (condition not met)
  Error = 'error',         // Failed with error
  Disposed = 'disposed',   // Cleaned up
}
```

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier |
| `metadata` | NodeMetadata | Type, title, category, description |
| `status` | NodeStatus | Current execution status |
| `ports` | Map<string, IPort> | Input and output ports |

### Key Methods

```typescript
// Execute the node
node.execute(context: ExecutionContext): Promise<NodeExecutionResult>

// Get a port by ID
node.getPort(portId: string): IPort | undefined

// Validate configuration
node.validate(): Promise<NodeValidationResult>

// Reset to initial state
node.reset(): Promise<void>
```

### NodeMetadata

```typescript
interface NodeMetadata {
  type: string           // Node class name (required)
  title?: string         // Display name
  category?: NodeCategory // e.g., 'math', 'flow-control', 'ai'
  description?: string
  version?: number
  icon?: string
  tags?: string[]
  parentNodeId?: string  // If nested in group
  ui?: NodeUIMetadata    // Position, dimensions, etc.
}
```

### Key Files

| File | Purpose |
|------|---------|
| `packages/chaingraph-types/src/node/base-node.ts` | BaseNode abstract class |
| `packages/chaingraph-types/src/node/interface.ts:11-14` | INode interface |
| `packages/chaingraph-types/src/node/node-enums.ts:12-22` | NodeStatus enum |
| `packages/chaingraph-types/src/node/types.ts:17-31` | NodeMetadata type |

---

## 3. Port

A **Port** is a typed input or output connector on a Node through which data flows. Ports are strongly typed and support primitives, arrays, objects, and streams.

### Port Direction

```typescript
type PortDirection = 'input' | 'output' | 'passthrough'
```

- **Input**: Receives data from connected output ports
- **Output**: Sends data to connected input ports
- **Passthrough**: Both input and output

### Port Types (9 Total)

| Type | Description | Example Use |
|------|-------------|-------------|
| `string` | Text values | Names, prompts, API keys |
| `number` | Numeric values | Counts, scores, coordinates |
| `boolean` | True/false | Flags, conditions |
| `array` | List of typed items | Data batches, collections |
| `object` | Structured data with schema | Complex configs, records |
| `stream` | Async multi-channel data | Real-time data, LLM tokens |
| `enum` | Fixed set of options | Dropdown selections |
| `secret` | Encrypted sensitive data | API keys, passwords |
| `any` | Untyped (avoid if possible) | Dynamic data |

### Port Configuration

Each port type has a specific config interface:

```typescript
interface StringPortConfig {
  type: 'string'
  defaultValue?: string
  minLength?: number
  maxLength?: number
  pattern?: RegExp  // Validation regex
}

interface NumberPortConfig {
  type: 'number'
  defaultValue?: number
  min?: number
  max?: number
  step?: number
  integer?: boolean
}

interface ArrayPortConfig<Item> {
  type: 'array'
  itemConfig: IPortConfig  // Type of each item
  minLength?: number
  maxLength?: number
  isMutable?: boolean      // Can items be added/removed?
}

interface ObjectPortConfig<Schema> {
  type: 'object'
  schema: IObjectSchema    // Properties definition
  isSchemaMutable?: boolean
}
```

### Key Methods

```typescript
// Get/set port value
port.getValue(): T | undefined
port.setValue(value: T): void

// Validation
port.validate(): boolean

// Serialization
port.serialize(): JSONValue
port.deserialize(data: JSONValue): IPort

// Connection management
port.addConnection(nodeId: string, portId: string): void
port.removeConnection(nodeId: string, portId: string): void
```

### Key Files

| File | Purpose |
|------|---------|
| `packages/chaingraph-types/src/port/base/IPort.ts:30-187` | IPort interface |
| `packages/chaingraph-types/src/port/base/types.ts:84-213` | Port config types |
| `packages/chaingraph-types/src/port/instances/` | Port implementations |
| `packages/chaingraph-types/src/port/plugins/` | Validation plugins |

---

## 4. Edge

An **Edge** is a directed connection from an output port of one node to an input port of another node, enabling data flow.

### Edge Status

```typescript
enum EdgeStatus {
  Active = 'active',     // Connection working
  Inactive = 'inactive', // Disabled
  Error = 'error',       // Transfer failed
}
```

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier |
| `sourceNode` | INode | Node with output port |
| `sourcePort` | IPort | Output port |
| `targetNode` | INode | Node with input port |
| `targetPort` | IPort | Input port |
| `metadata` | EdgeMetadata | Label, anchors, version |

### EdgeMetadata

```typescript
interface EdgeMetadata {
  label?: string              // Display label
  anchors?: EdgeAnchor[]      // Control points for custom paths
  version?: number            // For optimistic updates
}

interface EdgeAnchor {
  id: string
  x: number                   // Coordinate
  y: number
  index: number               // Order in path
}
```

### Key Files

| File | Purpose |
|------|---------|
| `packages/chaingraph-types/src/edge/edge.ts:18` | Edge implementation |
| `packages/chaingraph-types/src/edge/interface.ts:16-65` | IEdge interface |
| `packages/chaingraph-types/src/edge/types.ts:12-54` | EdgeStatus, EdgeMetadata |

---

## 5. Execution

### ExecutionContext

The runtime context provided to every executing node:

```typescript
class ExecutionContext {
  readonly executionId: string      // Unique run ID
  readonly rootExecutionId?: string // Root workflow ID
  readonly parentExecutionId?: string // Parent ID (for children)
  readonly flowId?: string
  readonly userId?: string
  readonly startTime: Date
  readonly abortController: AbortController
  readonly integrations: IntegrationContext  // AI, wallet, etc.
  readonly executionDepth: number  // Prevents infinite recursion (max 100)

  // Event emission (for event-driven execution)
  emitEvent(eventType: string, data: any, nodeId: string): void

  // Port resolution (for stream ports)
  resolvePort(nodeId: string, portId: string): void
  isPortResolved(nodeId: string, portId: string): boolean

  // Get integration data
  getIntegration<T>(type: string): T | undefined
}
```

### ExecutionEngine

Orchestrates flow execution:

```typescript
class ExecutionEngine {
  constructor(flow: Flow, context: ExecutionContext, options?: ExecutionOptions)

  async execute(): Promise<void>

  // Control flow
  pause(): void
  resume(): void
  stop(reason?: string): void

  // Event handling
  onEvent(eventType: ExecutionEventEnum, callback): void
  onError(callback): void
}
```

### ExecutionOptions

```typescript
interface ExecutionOptions {
  execution?: {
    maxConcurrency?: number    // Default: 50
    nodeTimeoutMs?: number     // Default: 3600000 (1 hour)
    flowTimeoutMs?: number     // Default: 10800000 (3 hours)
  }
  debug?: boolean              // Enable debugger
  breakpoints?: string[]       // Node IDs to break on
}
```

### Key Files

| File | Purpose |
|------|---------|
| `packages/chaingraph-types/src/execution/execution-context.ts:37-320` | ExecutionContext |
| `packages/chaingraph-types/src/flow/execution-engine.ts:49` | ExecutionEngine |

---

## 6. Events

### Flow Events (FlowEventType)

Events emitted during flow editing (19 total):

| Event | Description |
|-------|-------------|
| `FlowInitStart` | Subscription started |
| `FlowInitEnd` | Initial state sent |
| `MetadataUpdated` | Flow metadata changed |
| `NodesAdded` | Batch nodes added |
| `NodeAdded` | Single node added |
| `NodeRemoved` | Node deleted |
| `NodesUpdated` | Batch nodes updated |
| `NodeUpdated` | Node data changed |
| `NodeParentUpdated` | Node parent changed |
| `PortCreated` | Port added |
| `PortUpdated` | Port value/config changed |
| `PortRemoved` | Port deleted |
| `EdgesAdded` | Batch edges added |
| `EdgeAdded` | Connection created |
| `EdgeRemoved` | Connection deleted |
| `EdgeMetadataUpdated` | Edge metadata changed |
| `NodeUIPositionChanged` | Node moved |
| `NodeUIDimensionsChanged` | Node resized |
| `NodeUIChanged` | General UI changed |

### Execution Events (ExecutionEventEnum)

Events emitted during execution (21 total):

| Event | Description |
|-------|-------------|
| `EXECUTION_CREATED` | Execution initialized (index -1) |
| `FLOW_SUBSCRIBED` | Flow subscription confirmed |
| `FLOW_STARTED` | Execution began |
| `FLOW_COMPLETED` | Execution finished |
| `FLOW_FAILED` | Execution errored |
| `FLOW_CANCELLED` | Execution cancelled |
| `FLOW_PAUSED` | Execution paused |
| `FLOW_RESUMED` | Execution resumed |
| `NODE_STARTED` | Node began executing |
| `NODE_COMPLETED` | Node finished |
| `NODE_FAILED` | Node errored |
| `NODE_SKIPPED` | Node skipped |
| `NODE_STATUS_CHANGED` | Node status changed |
| `NODE_DEBUG_LOG_STRING` | Debug log from node |
| `EDGE_TRANSFER_STARTED` | Data transfer started |
| `EDGE_TRANSFER_COMPLETED` | Data transferred |
| `EDGE_TRANSFER_FAILED` | Data transfer failed |
| `CHILD_EXECUTION_SPAWNED` | Child workflow spawned |
| `CHILD_EXECUTION_COMPLETED` | Child workflow completed |
| `CHILD_EXECUTION_FAILED` | Child workflow failed |
| `DEBUG_BREAKPOINT_HIT` | Debugger breakpoint hit |

### Key Files

| File | Purpose |
|------|---------|
| `packages/chaingraph-types/src/flow/events.ts:17-47` | FlowEventType enum |
| `packages/chaingraph-types/src/flow/execution-events.ts:15-48` | ExecutionEventEnum |

---

## Quick Reference

### Creating a Node (with decorators)

```typescript
import { Node, Input, Output, PortString, PortNumber } from '@badaitech/chaingraph-types'

@Node({
  title: 'Add Numbers',
  category: 'math',
  description: 'Adds two numbers',
})
class AddNode extends BaseNode {
  @Input()
  @PortNumber({ defaultValue: 0 })
  a: number = 0

  @Input()
  @PortNumber({ defaultValue: 0 })
  b: number = 0

  @Output()
  @PortNumber()
  result: number = 0

  async execute(context: ExecutionContext): Promise<NodeExecutionResult> {
    this.result = this.a + this.b
    return {}
  }
}
```

### Data Flow Summary

```
1. Flow loads nodes and edges
2. ExecutionEngine resolves dependencies (topological sort)
3. Nodes execute in parallel where possible
4. Output port values transfer to connected input ports
5. Events stream in real-time
6. Flow completes or fails
```

---

## Related Skills

- `types-architecture` - Deep dive into the types package
- `port-system` - Detailed port types and decorators
- `effector-patterns` - Frontend state management
- `dbos-patterns` - Backend durable execution
