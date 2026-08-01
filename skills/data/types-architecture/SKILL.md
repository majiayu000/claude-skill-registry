---
name: types-architecture
description: Types package architecture for ChainGraph core definitions. THE foundation
  package for all development. Use when working on packages/chaingraph-types, port
  system, decorators, node classes, flow defin
---

---
name: types-architecture
description: Types package architecture for ChainGraph core definitions. THE foundation package for all development. Use when working on packages/chaingraph-types, port system, decorators, node classes, flow definitions, execution context, propagation, or any type-related code. Contains 9 port types, decorator system, compositional node architecture, execution engine. Triggers: types, port, decorator, @Node, @Input, @Output, @PortString, @PortArray, @PortObject, BaseNode, INode, IPort, IEdge, IFlow, ExecutionEngine, ExecutionContext, propagation.
---

# ChainGraph Types Architecture

This skill provides comprehensive architectural guidance for the `@badaitech/chaingraph-types` package - **THE foundation package** containing all core type definitions, port system, node architecture, decorators, and execution engine.

## Package Overview

**Location**: `packages/chaingraph-types/`
**Purpose**: Core type definitions, base implementations, and execution engine
**Key Features**: TypeScript decorators, compositional node architecture, 9 port types, propagation engine

## Complete Directory Structure

```
packages/chaingraph-types/src/
├── index.ts                        # Main entry - exports everything
├── json-transformers.ts            # SuperJSON serialization
│
├── decorator/                      # TypeScript decorators ⭐
│   ├── index.ts                    # All decorator exports
│   ├── node.decorator.ts           # @Node() decorator
│   ├── port.decorator.ts           # @Port() base decorator
│   ├── port.decorator.types.ts     # PortDecoratorOptions, ObjectPortSchemaInput
│   ├── port-config.decorator.ts    # @Input(), @Output(), @Name(), @Description()
│   ├── port-visibility.decorator.ts # @PortVisibility() conditional visibility
│   ├── port-update.decorator.ts    # Port update tracking
│   ├── scalar.decorator.ts         # @PortString(), @PortNumber(), @PortBoolean()
│   ├── object.decorator.ts         # @PortObject()
│   ├── array.decorator.ts          # @PortArray(), @PortArrayNumber()
│   ├── enum.decorator.ts           # @PortEnum()
│   ├── stream.decorator.ts         # @PortStream()
│   ├── secret.decorator.ts         # @PortSecret()
│   ├── object-schema.decorator.ts  # Object schema definition
│   ├── metadata-storage.ts         # reflect-metadata storage
│   ├── registry.ts                 # Node type registry
│   └── recursive-normalization.ts  # Config normalization
│
├── node/                           # Node system ⭐⭐
│   ├── index.ts                    # Node exports
│   ├── interface.ts                # INode interface
│   ├── base-node.ts                # BaseNode class
│   ├── base-node-compositional.ts  # Compositional implementation
│   ├── types.ts                    # NodeMetadata, NodeExecutionResult
│   ├── node-enums.ts               # NodeStatus enum
│   ├── category.ts                 # NodeCategory enum
│   ├── node-ui.ts                  # NodeUIMetadata, Position
│   ├── default-ports.ts            # System ports (flowIn, flowOut, error)
│   ├── traverse-ports.ts           # findPort() utility
│   ├── interfaces/                 # 10+ node interfaces
│   │   ├── inode-composite.ts      # INodeComposite (combines 9 interfaces)
│   │   ├── icore-node.ts           # Core identity/status
│   │   ├── iport-manager.ts        # Port CRUD
│   │   ├── iport-binder.ts         # Port binding
│   │   ├── icomplex-port-handler.ts # Complex type handling
│   │   ├── inode-ui.ts             # UI metadata
│   │   ├── inode-events.ts         # Event emission
│   │   ├── iserializable.ts        # Serialization
│   │   ├── inode-versioning.ts     # Version tracking
│   │   ├── inode-clonable.ts       # Cloning
│   │   └── i-system-port-manager.ts # System ports
│   └── implementations/            # Component implementations
│       ├── port-manager.ts
│       ├── indexed-port-manager.ts
│       ├── port-binder.ts
│       ├── complex-port-handler.ts
│       ├── node-event-manager.ts
│       ├── node-ui-manager.ts
│       ├── node-serializer.ts
│       ├── node-version-manager.ts
│       ├── system-port-manager.ts
│       └── port-update-collector.ts
│
├── port/                           # Port system ⭐⭐⭐
│   ├── index.ts                    # Port exports
│   ├── base/
│   │   ├── IPort.ts                # IPort interface (212 lines)
│   │   ├── BasePort.ts             # BasePort abstract class
│   │   ├── types.ts                # All port config types
│   │   ├── base-config.schema.ts   # Zod validation schemas
│   │   └── secret.ts               # Secret type definitions
│   ├── instances/                  # 9 port implementations
│   │   ├── StringPort.ts
│   │   ├── NumberPort.ts
│   │   ├── BooleanPort.ts
│   │   ├── ArrayPort.ts
│   │   ├── ObjectPort.ts
│   │   ├── StreamPort.ts
│   │   ├── EnumPort.ts
│   │   ├── AnyPort.ts
│   │   └── SecretPort.ts
│   ├── plugins/                    # Validation/serialization plugins
│   │   ├── PortPluginRegistry.ts
│   │   ├── StringPortPlugin.ts
│   │   ├── NumberPortPlugin.ts
│   │   ├── BooleanPortPlugin.ts
│   │   ├── ArrayPortPlugin.ts
│   │   ├── ObjectPortPlugin.ts
│   │   ├── StreamPortPlugin.ts
│   │   ├── EnumPortPlugin.ts
│   │   ├── AnyPortPlugin.ts
│   │   └── SecretPortPlugin.ts
│   ├── factory/
│   │   └── PortFactory.ts          # Port creation factory
│   ├── transfer-rules/             # Port compatibility rules
│   │   ├── engine.ts               # TransferEngine
│   │   ├── types.ts
│   │   ├── predicates.ts
│   │   ├── strategies.ts
│   │   └── rules/default-rules.ts
│   └── utils/
│       ├── json-schema-converter.ts
│       └── json-schema-types.ts
│
├── edge/                           # Edge system
│   ├── interface.ts                # IEdge interface
│   ├── edge.ts                     # Edge class
│   ├── types.ts                    # EdgeStatus, EdgeMetadata, EdgeAnchor
│   └── events.ts                   # Edge events
│
├── flow/                           # Flow system ⭐⭐
│   ├── interface.ts                # IFlow interface
│   ├── flow.ts                     # Flow class
│   ├── types.ts                    # FlowMetadata
│   ├── events.ts                   # FlowEventType (18 types)
│   ├── execution-events.ts         # ExecutionEventEnum (17 types)
│   ├── execution-engine.ts         # ExecutionEngine class
│   ├── execution-handlers.ts       # Event handlers
│   ├── debugger.ts                 # FlowDebugger
│   ├── debugger-types.ts           # DebuggerState, DebuggerCommand
│   ├── edge-transfer-service.ts    # Data transfer between ports
│   ├── cycleDetection.ts           # DAG validation
│   ├── propagation/                # Propagation engine
│   │   ├── PropagationEngine.ts
│   │   ├── types.ts                # ActionContext, PropagationAction
│   │   └── actions/
│   │       └── TransferRulesAction.ts
│   └── serializer/
│       └── flow-serializer.ts
│
├── execution/                      # Execution context
│   ├── execution-context.ts        # ExecutionContext class
│   ├── emitted-event-context.ts    # Event-driven execution
│   ├── integration-context.ts      # Integration settings
│   ├── wallet-context.ts           # Wallet/crypto context
│   └── arch-a-i-context.ts         # AI agent context
│
└── utils/                          # Utilities
    ├── async-queue.ts              # Async queue for execution
    ├── event-queue.ts              # Event queue
    ├── semaphore.ts                # Concurrency control
    ├── deep-copy.ts
    └── deep-equal.ts
```

---

## Node System Architecture

### Compositional Design

Nodes use a **compositional architecture** with 9 specialized interfaces combined into `INodeComposite`:

**File**: `src/node/interfaces/inode-composite.ts`

```typescript
interface INodeComposite extends
  ICoreNode,           // Core identity and status
  IPortManager,        // Port CRUD operations
  IPortBinder,         // Port binding to node
  IComplexPortHandler, // Complex type handling (Array, Object)
  INodeUI,             // UI metadata (position, dimensions)
  INodeEvents,         // Event subscription/emission
  ISerializable,       // Serialization
  INodeVersioning,     // Version tracking
  ISystemPortManager,  // System ports (flowIn, flowOut, error)
  INodeClonable        // Deep cloning
{
  // Additional methods
  initialize(portsConfig?: Map<string, IPortConfig>): void
  executeWithSystemPorts(context: ExecutionContext): Promise<NodeExecutionResult>
  startBatchUpdate(): void
  commitBatchUpdate(eventContext?: EventContext): Promise<void>
}
```

### BaseNode Implementation

**File**: `src/node/base-node-compositional.ts`

```typescript
class BaseNodeCompositional implements INodeComposite {
  // Core properties
  protected _id: string
  protected _metadata: NodeMetadata
  protected _status: NodeStatus

  // Specialized components (composition over inheritance)
  protected portManager: PortManager
  protected portBinder: PortBinder
  protected complexPortHandler: ComplexPortHandler
  protected eventManager: NodeEventManager
  protected uiManager: NodeUIManager
  protected versionManager: NodeVersionManager
  protected serializer: NodeSerializer
  protected systemPortManager: SystemPortManager
  protected portUpdateCollector: PortUpdateCollector

  // Execute method - override in subclasses
  async execute(context: ExecutionContext): Promise<NodeExecutionResult> {
    throw new Error('execute() must be implemented')
  }
}
```

### NodeStatus Lifecycle

**File**: `src/node/node-enums.ts`

```
Idle → Initialized → Ready → Executing → Completed
                              ↓            ↓
                           Skipped       Error
                                          ↓
                                       Disposed
```

### NodeMetadata

**File**: `src/node/types.ts`

```typescript
interface NodeMetadata {
  type: string              // Required: Node class identifier
  id?: string               // Unique node ID
  title?: string            // Display name
  category?: NodeCategory   // e.g., 'math', 'flow-control', 'ai'
  description?: string
  version?: number
  icon?: string
  tags?: string[]
  author?: string
  parentNodeId?: string     // For grouped nodes
  ui?: NodeUIMetadata       // Position, dimensions
  flowPorts?: FlowPorts     // System port configuration
}

interface FlowPorts {
  flowIn: boolean           // Has flow input port
  flowOut: boolean          // Has flow output port
  error: boolean            // Has error port
  errorMessage: boolean     // Has error message port
}
```

---

## Port System (9 Types)

### IPort Interface

**File**: `src/port/base/IPort.ts` (212 lines)

```typescript
interface IPort<C extends IPortConfig = IPortConfig> {
  // Identity
  id: string
  key: string

  // Configuration
  getConfig(): C
  setConfig(newConfig: C): void

  // Value management
  getValue(): ExtractValue<C> | undefined
  setValue(newValue: ExtractValue<C>): void
  reset(): void
  getDefaultValue(): ExtractValue<C> | undefined

  // Validation
  validate(): boolean
  validateValue(value: ExtractValue<C>): boolean
  validateConfig(config: C): boolean

  // Serialization
  serialize(): JSONValue
  deserialize(data: JSONValue): IPort<C>
  serializeConfig(config: C): JSONValue
  serializeValue(value: ExtractValue<C>): JSONValue
  deserializeConfig(data: JSONValue): C
  deserializeValue(data: JSONValue): ExtractValue<C>

  // Cloning
  clone(): IPort<C>
  cloneWithNewId(): IPort<C>

  // System/Connection
  isSystem(): boolean
  isSystemError(): boolean
  addConnection(nodeId: string, portId: string): void
  removeConnection(nodeId: string, portId: string): void
}
```

### Port Types and Configurations

**File**: `src/port/base/types.ts`

| Type | Config Interface | Key Properties |
|------|------------------|----------------|
| `string` | `StringPortConfig` | `defaultValue`, `minLength`, `maxLength`, `pattern`, `multiline` |
| `number` | `NumberPortConfig` | `defaultValue`, `min`, `max`, `step`, `integer` |
| `boolean` | `BooleanPortConfig` | `defaultValue` |
| `array` | `ArrayPortConfig<Item>` | `itemConfig`, `minLength`, `maxLength`, `isMutable` |
| `object` | `ObjectPortConfig<Schema>` | `schema`, `isSchemaMutable` |
| `stream` | `StreamPortConfig<Value>` | `itemConfig` (for channel items) |
| `enum` | `EnumPortConfig` | `options: EnumOption[]` |
| `secret` | `SecretPortConfig<SecretType>` | `secretType` |
| `any` | `AnyPortConfig` | No constraints |

### Port Instances

**Location**: `src/port/instances/`

Each port type has a dedicated class extending `BasePort<Config>`:

```typescript
// StringPort.ts
class StringPort extends BasePort<StringPortConfig> {
  validateValue(value: string): boolean {
    const { minLength, maxLength, pattern } = this.config
    // Validation logic
  }
}

// ArrayPort.ts
class ArrayPort<T> extends BasePort<ArrayPortConfig<T>> {
  // Handles nested item configs
  // Supports mutable/immutable arrays
}

// ObjectPort.ts
class ObjectPort<S> extends BasePort<ObjectPortConfig<S>> {
  // Handles object schema with nested ports
  // Supports schema mutations
}
```

### Port Plugins

**Location**: `src/port/plugins/`

Plugins provide validation and serialization for each port type:

```typescript
interface PortPlugin<C extends IPortConfig, V> {
  validateConfig(config: C): ValidationError[]
  validateValue(value: V, config: C): ValidationError[]
  serializeConfig(config: C): JSONValue
  serializeValue(value: V): JSONValue
  deserializeConfig(data: JSONValue): C
  deserializeValue(data: JSONValue): V
  getDefaultValue(config: C): V | undefined
}
```

### Port Factory

**File**: `src/port/factory/PortFactory.ts`

```typescript
class PortFactory {
  static create<T extends IPortConfig>(config: T): PortInstance {
    switch (config.type) {
      case 'string': return new StringPort(config)
      case 'number': return new NumberPort(config)
      case 'boolean': return new BooleanPort(config)
      case 'array': return new ArrayPort(config)
      case 'object': return new ObjectPort(config)
      case 'stream': return new StreamPort(config)
      case 'enum': return new EnumPort(config)
      case 'secret': return new SecretPort(config)
      case 'any': return new AnyPort(config)
    }
  }
}
```

### Transfer Rules

**Location**: `src/port/transfer-rules/`

Rules for port type compatibility during edge connections:

```typescript
// Check if two ports can connect
const engine = getDefaultTransferEngine()
const canConnect = engine.canTransfer(sourcePort, targetPort)

// Rules include:
// - Same type → direct transfer
// - Number → String → auto-convert
// - Array<T> → Array<T> → item-wise transfer
// - Object schema compatibility
```

---

## Decorator System

### Node Decorator

**File**: `src/decorator/node.decorator.ts`

```typescript
@Node({
  type: 'my-node',           // Required: unique identifier
  title: 'My Node',          // Display name
  category: 'math',          // NodeCategory enum
  description: 'Does X',
  version: 1,
  icon: 'calculator',
  tags: ['arithmetic'],
  flowPorts: {               // System port configuration
    flowIn: true,
    flowOut: true,
    error: true,
    errorMessage: true,
  },
})
class MyNode extends BaseNode { }
```

### Port Direction Decorators

**File**: `src/decorator/port-config.decorator.ts`

```typescript
@Input()      // direction: 'input'
@Output()     // direction: 'output'
@Passthrough() // direction: 'passthrough' (bidirectional)
```

### Port Type Decorators

**Files**: `scalar.decorator.ts`, `array.decorator.ts`, `object.decorator.ts`, etc.

```typescript
// Scalar types
@PortString({ defaultValue: '', minLength: 0, maxLength: 1000 })
@PortNumber({ defaultValue: 0, min: -Infinity, max: Infinity, step: 1 })
@PortBoolean({ defaultValue: false })

// Complex types
@PortArray({ itemConfig: { type: 'string' }, minLength: 0 })
@PortObject({ schema: mySchema })
@PortStream({ itemConfig: { type: 'string' } })

// Enum types
@PortEnum({ options: [{ value: 'a', label: 'Option A' }] })

// Special types
@PortSecret({ secretType: 'api-key' })
```

### Port Metadata Decorators

```typescript
@Name('customName')           // Override port name
@Description('Port purpose')  // Add description
@Title('Display Title')       // Add title
@Id('custom-id')              // Custom port ID
@DefaultValue(42)             // Set default value
@Metadata('key', value)       // Arbitrary metadata
```

### Port Visibility Decorator

**File**: `src/decorator/port-visibility.decorator.ts`

```typescript
@PortVisibility({
  showIf: (instance: INode) => instance.getPort('mode')?.getValue() === 'advanced'
})
@Input()
@PortString()
advancedOption: string = ''
```

### Complete Node Example

```typescript
import {
  Node, Input, Output,
  PortString, PortNumber, PortBoolean, PortArray, PortObject,
  Name, Description, PortVisibility
} from '@badaitech/chaingraph-types'

@Node({
  type: 'text-processor',
  title: 'Text Processor',
  category: 'text',
  description: 'Processes text with configurable options',
})
class TextProcessorNode extends BaseNode {
  // String input with validation
  @Input()
  @PortString({ defaultValue: '', maxLength: 10000 })
  @Description('Text to process')
  text: string = ''

  // Number input with range
  @Input()
  @PortNumber({ defaultValue: 100, min: 1, max: 1000 })
  maxLength: number = 100

  // Boolean flag
  @Input()
  @PortBoolean({ defaultValue: false })
  uppercase: boolean = false

  // Conditional visibility
  @PortVisibility({ showIf: (node) => node.getPort('uppercase')?.getValue() === true })
  @Input()
  @PortString({ defaultValue: '' })
  prefix: string = ''

  // Array output
  @Output()
  @PortArray({ itemConfig: { type: 'string' } })
  words: string[] = []

  // Object output with schema
  @Output()
  @PortObject({
    schema: {
      properties: {
        processed: { type: 'string' },
        wordCount: { type: 'number' },
      }
    }
  })
  result: { processed: string, wordCount: number } = { processed: '', wordCount: 0 }

  async execute(context: ExecutionContext): Promise<NodeExecutionResult> {
    let processed = this.text.slice(0, this.maxLength)
    if (this.uppercase) {
      processed = (this.prefix + processed).toUpperCase()
    }
    this.words = processed.split(' ').filter(w => w.length > 0)
    this.result = { processed, wordCount: this.words.length }
    return {}
  }
}
```

---

## Flow & Execution Engine

### Flow Class

**File**: `src/flow/flow.ts`

```typescript
class Flow implements IFlow {
  id: string
  metadata: FlowMetadata
  nodes: Map<string, INode>
  edges: Map<string, IEdge>

  // Internal components
  eventQueue: EventQueue<FlowEvent>
  propagationEngine: PropagationEngine

  // Node operations
  async addNode(node: INode): Promise<INode>
  async addNodes(nodes: INode[]): Promise<INode[]>
  async removeNode(nodeId: string): Promise<void>

  // Edge operations
  async addEdge(edge: IEdge): Promise<void>
  async connectPorts(sourceNodeId, sourcePortId, targetNodeId, targetPortId): Promise<IEdge>

  // Events
  onEvent(handler: (event: FlowEvent) => void): () => void

  // Validation
  async validate(): Promise<FlowValidationResult>
}
```

### ExecutionEngine

**File**: `src/flow/execution-engine.ts`

```typescript
class ExecutionEngine {
  // Execution queues
  readyQueue: AsyncQueue<() => Promise<void>>
  completedQueue: AsyncQueue<INode>

  // Tracking
  executingNodes: Set<string>
  completedNodes: Set<string>
  nodeDependencies: Map<string, number>
  dependentsMap: Map<string, INode[]>

  // Port-level resolution
  resolvedPorts: Set<string>
  sourcePortToWaitingNodes: Map<string, Set<string>>

  // Event-driven nodes
  eventListenerNodeIds: Set<string>
  eventBoundNodes: Set<string>

  // Concurrency control
  semaphore: Semaphore
  debugger: FlowDebugger | null

  constructor(
    flow: Flow,
    context: ExecutionContext,
    options?: ExecutionOptions,
    onBreakpointHit?: (node: INode) => void
  )

  async execute(): Promise<void>
}
```

### ExecutionOptions

```typescript
interface ExecutionOptions {
  execution?: {
    maxConcurrency?: number     // Default: 50
    nodeTimeoutMs?: number      // Default: 3600000 (1 hour)
    flowTimeoutMs?: number      // Default: 10800000 (3 hours)
  }
  debug?: boolean               // Enable debugger
  breakpoints?: string[]        // Node IDs to break on
}
```

### FlowDebugger

**File**: `src/flow/debugger.ts`

```typescript
class FlowDebugger implements DebuggerController {
  state: DebuggerState  // 'running' | 'paused' | 'stepping' | 'stopped'

  pause(): void
  continue(): void
  step(): void
  stop(): void
  addBreakpoint(nodeId: string): void
  removeBreakpoint(nodeId: string): void
  getState(): DebuggerState
}
```

### PropagationEngine

**File**: `src/flow/propagation/PropagationEngine.ts`

Handles automatic data propagation when ports change:

```typescript
class PropagationEngine {
  actions: PropagationAction[]

  async handleEvent(event: FlowEvent, flow: IFlow): Promise<ActionResult[]>
}

interface PropagationAction {
  name: string
  canExecute(context: ActionContext): boolean
  execute(context: ActionContext): void | Promise<void>
}

interface ActionContext {
  event: FlowEvent
  flow: IFlow
  sourcePort?: IPort
  targetPort?: IPort
  edge?: IEdge
  sourceNode?: INode
  targetNode?: INode
}
```

---

## ExecutionContext

**File**: `src/execution/execution-context.ts`

```typescript
class ExecutionContext {
  // Identity
  executionId: string
  rootExecutionId?: string
  parentExecutionId?: string
  flowId?: string
  userId?: string

  // Timing
  startTime: Date
  executionDepth: number  // Max 100

  // Control
  abortController: AbortController

  // Integrations
  integrations: IntegrationContext

  // Event-driven execution
  emittedEvents?: EmittedEvent[]
  eventData?: EmittedEventContext
  isChildExecution?: boolean

  // Node resolution
  getNodeById: (nodeId: string) => INode | undefined
  findNodes: (predicate: (node: INode) => boolean) => INode[]

  // Methods
  emitEvent(event: EmittedEvent): void
  getEmittedEvents(eventType?: string): EmittedEvent[]
  resolvePort(nodeId: string, portId: string): void
  isPortResolved(nodeId: string, portId: string): boolean
}
```

---

## Key Files Reference

| File | Purpose | Lines |
|------|---------|-------|
| `src/port/base/IPort.ts` | Port interface | 1-212 |
| `src/port/base/types.ts` | Port config types | 1-150+ |
| `src/node/interfaces/inode-composite.ts` | Composite interface | 1-86 |
| `src/node/base-node-compositional.ts` | Node implementation | 1-100+ |
| `src/decorator/port-config.decorator.ts` | Direction decorators | 1-118 |
| `src/decorator/port-visibility.decorator.ts` | Visibility decorator | 1-138 |
| `src/decorator/metadata-storage.ts` | Reflect metadata | 1-86 |
| `src/flow/execution-engine.ts` | Execution engine | 1-100+ |
| `src/flow/debugger.ts` | Flow debugger | 1-100+ |
| `src/flow/propagation/PropagationEngine.ts` | Data propagation | 1-80+ |
| `src/execution/execution-context.ts` | Runtime context | 1-100+ |

---

## Quick Reference

| Need | Where | Export |
|------|-------|--------|
| Create a node | `decorator/node.decorator.ts` | `@Node()` |
| Input port | `decorator/port-config.decorator.ts` | `@Input()` |
| Output port | `decorator/port-config.decorator.ts` | `@Output()` |
| String port | `decorator/scalar.decorator.ts` | `@PortString()` |
| Number port | `decorator/scalar.decorator.ts` | `@PortNumber()` |
| Boolean port | `decorator/scalar.decorator.ts` | `@PortBoolean()` |
| Array port | `decorator/array.decorator.ts` | `@PortArray()` |
| Object port | `decorator/object.decorator.ts` | `@PortObject()` |
| Stream port | `decorator/stream.decorator.ts` | `@PortStream()` |
| Enum port | `decorator/enum.decorator.ts` | `@PortEnum()` |
| Conditional port | `decorator/port-visibility.decorator.ts` | `@PortVisibility()` |
| Create port instance | `port/factory/PortFactory.ts` | `PortFactory.create()` |
| Check compatibility | `port/transfer-rules/engine.ts` | `TransferEngine` |

---

## Related Skills

- `chaingraph-concepts` - Core domain concepts
- `port-system` - Port types deep dive (planned)
- `executor-architecture` - How types are used in execution
- `frontend-architecture` - How types render in UI
- `dbos-patterns` - Execution context in DBOS
