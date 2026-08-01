---
name: port-system
description: Deep dive into ChainGraph port system - 9 port types, plugins, factory,
  transfer rules, and frontend rendering. Use when creating custom ports, working
  on port validation, implementing port UI compone
---

---
name: port-system
description: Deep dive into ChainGraph port system - 9 port types, plugins, factory, transfer rules, and frontend rendering. Use when creating custom ports, working on port validation, implementing port UI components, or debugging port compatibility. Triggers: port, PortString, PortNumber, PortArray, PortObject, PortStream, port type, port plugin, port factory, transfer rules, port validation, port compatibility.
---

# ChainGraph Port System

This skill provides a deep dive into the ChainGraph port system - the typed input/output connectors that enable data flow between nodes.

## Port System Overview

Ports are strongly-typed connectors on nodes. The system consists of:

1. **9 Port Types** - string, number, boolean, array, object, stream, enum, secret, any
2. **Port Instances** - Runtime port objects with values
3. **Port Plugins** - Validation and serialization per type
4. **Port Factory** - Creates port instances from configs
5. **Transfer Rules** - Type compatibility for connections
6. **Frontend Stores** - ports-v2 Effector stores for UI

## The 9 Port Types

### Scalar Types

| Type | Decorator | Config | Use Cases |
|------|-----------|--------|-----------|
| `string` | `@PortString()` | `defaultValue`, `minLength`, `maxLength`, `pattern`, `multiline` | Text, prompts, IDs, URLs |
| `number` | `@PortNumber()` | `defaultValue`, `min`, `max`, `step`, `integer` | Counts, scores, coordinates |
| `boolean` | `@PortBoolean()` | `defaultValue` | Flags, toggles, conditions |

### Complex Types

| Type | Decorator | Config | Use Cases |
|------|-----------|--------|-----------|
| `array` | `@PortArray()` | `itemConfig`, `minLength`, `maxLength`, `isMutable` | Lists, batches, collections |
| `object` | `@PortObject()` | `schema`, `isSchemaMutable` | Structured data, records, configs |
| `stream` | `@PortStream()` | `itemConfig` | Real-time data, LLM tokens, multi-channel |

### Special Types

| Type | Decorator | Config | Use Cases |
|------|-----------|--------|-----------|
| `enum` | `@PortEnum()` | `options: EnumOption[]` | Dropdowns, fixed choices |
| `secret` | `@PortSecret()` | `secretType` | API keys, passwords, tokens |
| `any` | `@Any()` | - | Dynamic data (avoid if possible) |

---

## Port Configuration Details

### StringPortConfig

**File**: `packages/chaingraph-types/src/port/base/types.ts`

```typescript
interface StringPortConfig {
  type: 'string'
  defaultValue?: string
  minLength?: number          // Minimum string length
  maxLength?: number          // Maximum string length
  pattern?: string            // Regex pattern for validation
  multiline?: boolean         // UI hint: show textarea
  ui?: PortUIConfig           // Additional UI hints
}

// Example
@Input()
@PortString({
  defaultValue: '',
  maxLength: 10000,
  multiline: true,
})
prompt: string = ''
```

### NumberPortConfig

```typescript
interface NumberPortConfig {
  type: 'number'
  defaultValue?: number
  min?: number                // Minimum value
  max?: number                // Maximum value
  step?: number               // Step increment for UI slider
  integer?: boolean           // Only allow integers
  ui?: PortUIConfig
}

// Example: Temperature slider
@Input()
@PortNumber({
  defaultValue: 0.7,
  min: 0,
  max: 2,
  step: 0.1,
})
temperature: number = 0.7
```

### ArrayPortConfig

```typescript
interface ArrayPortConfig<Item extends IPortConfig> {
  type: 'array'
  itemConfig: Item            // Config for each item
  defaultValue?: Array<ExtractValue<Item>>
  minLength?: number
  maxLength?: number
  isMutable?: boolean         // Can add/remove items in UI?
  isSchemaMutable?: boolean   // Can change item schema?
  ui?: PortUIConfig
}

// Example: List of strings
@Input()
@PortArray({
  itemConfig: { type: 'string', defaultValue: '' },
  isMutable: true,
  minLength: 1,
})
items: string[] = ['']

// Example: Nested array of objects
@Input()
@PortArray({
  itemConfig: {
    type: 'object',
    schema: {
      properties: {
        name: { type: 'string' },
        value: { type: 'number' },
      }
    }
  }
})
records: Array<{ name: string, value: number }> = []
```

### ObjectPortConfig

```typescript
interface ObjectPortConfig<Schema extends IObjectSchema> {
  type: 'object'
  schema: Schema              // Object property definitions
  defaultValue?: ExtractObjectValue<Schema>
  isSchemaMutable?: boolean   // Can add/remove properties?
  ui?: PortUIConfig
}

interface IObjectSchema {
  properties: Record<string, IPortConfig>
  required?: string[]
}

// Example: Structured config
@Input()
@PortObject({
  schema: {
    properties: {
      model: { type: 'string', defaultValue: 'gpt-4' },
      maxTokens: { type: 'number', defaultValue: 1000, min: 1 },
      stream: { type: 'boolean', defaultValue: false },
    },
    required: ['model'],
  },
})
config: { model: string, maxTokens: number, stream: boolean }
```

### StreamPortConfig

**File**: `packages/chaingraph-types/src/port/base/types.ts:178-184`

```typescript
interface StreamPortConfig<Item extends IPortConfig> {
  type: 'stream'
  itemConfig: Item            // Required: Type of values in stream
  isSchemaMutable?: boolean   // Can change item type?
  defaultValue?: StreamPortValue<Item>  // Initial channel state
  ui?: PortUIConfig
}

// StreamPortValue is aliased to MultiChannel<T>
type StreamPortValue<T extends IPortConfig> = MultiChannel<ExtractValue<T>>
```

**IMPORTANT**: Stream values are `MultiChannel<T>`, NOT `AsyncIterable<T>`.

**MultiChannel**: `packages/chaingraph-types/src/utils/multi-channel.ts`

```typescript
class MultiChannel<T> {
  // Send value to stream
  send(value: T): void
  sendBatch(values: T[]): void

  // Close stream (signals completion)
  close(): void

  // Error handling
  setError(error: Error): void
  getError(): Error | null

  // Async iteration (implements AsyncIterable)
  [Symbol.asyncIterator](): AsyncIterableIterator<T>

  // Utilities
  isChannelClosed(): boolean
  getBuffer(): T[]
  getSubscriberCount(): number
}
```

**Example: Token stream from LLM**

```typescript
@Output()
@PortStream({
  title: 'Response Stream',
  description: 'Streamed response from Claude',
  itemConfig: { type: 'string' },
})
responseStream: MultiChannel<string> = new MultiChannel<string>()

async execute(context: ExecutionContext) {
  // Resolve port - downstream can start reading NOW
  context.resolvePort(this.id, 'responseStream')

  // Stream tokens as they arrive
  for await (const event of llmStream) {
    this.responseStream.send(event.delta.text || '')
  }

  // Close stream when done
  this.responseStream.close()
}

// Consuming node
async execute(context: ExecutionContext) {
  for await (const token of this.responseStream) {
    console.log('Token:', token)
  }
  // Loop exits when stream is closed
}
```

**Example: Multi-channel with structured data**

```typescript
@Output()
@PortStream({
  itemConfig: {
    type: 'object',
    schema: {
      properties: {
        type: { type: 'string' },
        data: { type: 'any' },
      }
    }
  }
})
events: MultiChannel<{ type: string, data: any }> = new MultiChannel()

async execute(context: ExecutionContext) {
  // Send different event types through same stream
  this.events.send({ type: 'start', data: null })
  this.events.send({ type: 'progress', data: { percent: 50 } })
  this.events.send({ type: 'complete', data: { result: 'done' } })
  this.events.close()
}
```

### EnumPortConfig

**File**: `packages/chaingraph-types/src/port/base/types.ts:198-203`

```typescript
interface EnumPortConfig {
  type: 'enum'
  options: IPortConfig[]      // Each option is a full port config
  defaultValue?: EnumPortValue
  ui?: PortUIConfig
}
```

**IMPORTANT**: Options are `IPortConfig[]`, not simple value/label pairs. Each option is a complete port configuration.

**Decorators**: `packages/chaingraph-types/src/decorator/enum.decorator.ts`

```typescript
// Manual enum - full control
@Input()
@PortEnum({
  options: [
    { id: 'gpt-4', type: 'string', defaultValue: 'gpt-4', title: 'GPT-4' },
    { id: 'gpt-3.5', type: 'string', defaultValue: 'gpt-3.5-turbo', title: 'GPT-3.5 Turbo' },
    { id: 'claude', type: 'string', defaultValue: 'claude-3', title: 'Claude 3' },
  ],
  defaultValue: 'gpt-4',
})
model: string = 'gpt-4'

// StringEnum - convenience decorator
@Input()
@StringEnum(['Red', 'Green', 'Blue'], { defaultValue: 'Red' })
color: string = 'Red'
// Automatically creates: options: [{ id: 'Red', type: 'string', defaultValue: 'Red', title: 'Red' }, ...]

// NumberEnum - convenience decorator
@Input()
@NumberEnum([1, 2, 3, 4, 5], { defaultValue: 1 })
rating: number = 1
// Automatically creates: options: [{ id: '1', type: 'number', defaultValue: 1, title: '1' }, ...]
```

### SecretPortConfig

```typescript
interface SecretPortConfig<SecretType extends string> {
  type: 'secret'
  secretType: SecretType      // Type identifier for secret storage
  defaultValue: undefined     // Secrets have no default
  ui?: PortUIConfig
}

// Example: API key
@Input()
@PortSecret({ secretType: 'openai-api-key' })
apiKey: Secret<'openai-api-key'>
```

### Stream Port Best Practices

**Always initialize MultiChannel**:
```typescript
// ✅ GOOD: Initialize in class definition
@Output()
@PortStream({ itemConfig: { type: 'string' } })
tokens: MultiChannel<string> = new MultiChannel<string>()

// ❌ BAD: Uninitialized will be undefined
@Output()
@PortStream({ itemConfig: { type: 'string' } })
tokens: MultiChannel<string>  // undefined!
```

**Always close streams when done**:
```typescript
async execute(context: ExecutionContext) {
  try {
    for (const item of items) {
      this.outputStream.send(item)
    }
  } finally {
    this.outputStream.close()  // ✅ Always close
  }
}
```

**Handle stream errors**:
```typescript
async execute(context: ExecutionContext) {
  try {
    // ... stream processing
  } catch (error) {
    this.outputStream.setError(error)  // Signal error to consumers
    throw error
  }
}

// Consumer checks for errors
async execute(context: ExecutionContext) {
  for await (const item of this.inputStream) {
    // Process items
  }

  const error = this.inputStream.getError()
  if (error) {
    throw new Error(`Stream error: ${error.message}`)
  }
}
```

**Resolve ports for parallel consumption**:
```typescript
async execute(context: ExecutionContext) {
  // Tell execution engine this port is ready
  context.resolvePort(this.id, 'responseStream')

  // Now downstream nodes can start consuming in parallel
  for await (const event of llmApi) {
    this.responseStream.send(event.text)
  }

  this.responseStream.close()
}
```

---

## Port Plugins

Each port type has a dedicated plugin for validation and serialization.

**Location**: `packages/chaingraph-types/src/port/plugins/`

### Plugin Interface

```typescript
interface PortPlugin<C extends IPortConfig, V> {
  // Validate configuration
  validateConfig(config: C): ValidationError[]

  // Validate value against config
  validateValue(value: V, config: C): ValidationError[]

  // Serialize config to JSON
  serializeConfig(config: C): JSONValue

  // Serialize value to JSON
  serializeValue(value: V): JSONValue

  // Deserialize config from JSON
  deserializeConfig(data: JSONValue): C

  // Deserialize value from JSON
  deserializeValue(data: JSONValue): V

  // Get default value from config
  getDefaultValue(config: C): V | undefined
}
```

### Plugin Registry

```typescript
// Get plugin for a port type
import { PortPluginRegistry } from '@badaitech/chaingraph-types'

const stringPlugin = PortPluginRegistry.getPlugin('string')
const errors = stringPlugin.validateValue('test', config)
```

---

## Port Factory

Creates port instances from configuration.

**File**: `packages/chaingraph-types/src/port/factory/PortFactory.ts`

```typescript
import { PortFactory } from '@badaitech/chaingraph-types'

// Create single port
const stringPort = PortFactory.create({
  type: 'string',
  defaultValue: 'hello',
  maxLength: 100,
})

// Create multiple ports
const ports = PortFactory.createFromConfigs([
  { type: 'string', id: 'input' },
  { type: 'number', id: 'count', defaultValue: 0 },
])

// Type inference
const arrayPort = PortFactory.create<ArrayPortC
onfig<StringPortConfig>>({
  type: 'array',
  itemConfig: { type: 'string' },
})
```

---

## Transfer Rules (Port Compatibility)

Determines which port types can connect to each other.

**Location**: `packages/chaingraph-types/src/port/transfer-rules/`

### Default Transfer Rules

| Source | Target | Rule |
|--------|--------|------|
| `string` | `string` | Direct transfer |
| `number` | `number` | Direct transfer |
| `number` | `string` | Auto-convert to string |
| `boolean` | `boolean` | Direct transfer |
| `array<T>` | `array<T>` | Item-wise transfer |
| `object` | `object` | Schema compatibility check |
| `any` | `*` | Always compatible |
| `*` | `any` | Always compatible |

### Using Transfer Engine

```typescript
import { getDefaultTransferEngine, canConnect } from '@badaitech/chaingraph-types'

// Check compatibility
const compatible = canConnect(sourcePort, targetPort)

// Get transfer engine for custom rules
const engine = getDefaultTransferEngine()
const result = engine.canTransfer(sourceConfig, targetConfig)
```

### Custom Transfer Rules

```typescript
import { RuleBuilder, Predicates, Strategies } from '@badaitech/chaingraph-types'

const customRule = RuleBuilder.create()
  .when(Predicates.sourceIs('number'))
  .when(Predicates.targetIs('string'))
  .then(Strategies.convert((value) => String(value)))
  .build()
```

---

## Frontend Port Stores (ports-v2)

The frontend uses Effector stores for port state management.

**Location**: `apps/chaingraph-frontend/src/store/ports-v2/`

### Store Organization

```
store/ports-v2/
├── domain.ts           # portsV2Domain
├── stores.ts           # Main stores
├── events.ts           # Events for updates
├── effects.ts          # Server sync effects
├── selectors.ts        # Derived stores
├── buffer.ts           # Event batching
├── echo-detection.ts   # Echo prevention
├── pending-mutations.ts # Optimistic tracking
├── collapsed-handles.ts # UI collapse state
└── descendants.ts      # Array/Object child tracking
```

### Key Stores

```typescript
// Port values by key (nodeId:portId)
export const $portValues = portsV2Domain.createStore<Map<string, unknown>>(new Map())

// Port configs by key
export const $portConfigs = portsV2Domain.createStore<Map<string, IPortConfig>>(new Map())

// Port UI state (expanded/collapsed)
export const $portUI = portsV2Domain.createStore<Map<string, PortUIState>>(new Map())

// Collapsed handles for array/object ports
export const $collapsedHandles = portsV2Domain.createStore<Set<string>>(new Set())
```

### Using Port Stores in Components

```typescript
import { useUnit } from 'effector-react'
import { $portValues, updatePortValue } from '@/store/ports-v2'

function PortInput({ portKey }: { portKey: string }) {
  const [portValues, update] = useUnit([$portValues, updatePortValue])
  const value = portValues.get(portKey)

  return (
    <input
      value={value ?? ''}
      onChange={(e) => update({ portKey, value: e.target.value })}
    />
  )
}
```

---

## Port UI Components

**Location**: `apps/chaingraph-frontend/src/components/flow/nodes/ChaingraphNode/ports/`

### Port Component Hierarchy

```
ports/
├── PortRenderer.tsx        # Routes to correct port component
├── ScalarPort/
│   ├── StringPortInput.tsx # Text input/textarea
│   ├── NumberPortInput.tsx # Number input/slider
│   └── BooleanPortInput.tsx # Checkbox/toggle
├── ArrayPort/
│   └── ArrayPort.tsx       # List with add/remove
├── ObjectPort/
│   └── ObjectPort.tsx      # Nested property editors
├── EnumPort/
│   └── EnumPortSelect.tsx  # Dropdown select
└── StreamPort/
    └── StreamPortDisplay.tsx # Real-time display
```

### Port Rendering Pattern

```typescript
function PortRenderer({ nodeId, portKey, config }: PortRendererProps) {
  switch (config.type) {
    case 'string':
      return <StringPortInput nodeId={nodeId} portKey={portKey} config={config} />
    case 'number':
      return <NumberPortInput nodeId={nodeId} portKey={portKey} config={config} />
    case 'array':
      return <ArrayPort nodeId={nodeId} portKey={portKey} config={config} />
    case 'object':
      return <ObjectPort nodeId={nodeId} portKey={portKey} config={config} />
    // ... etc
  }
}
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `types/src/port/base/IPort.ts` | Port interface (212 lines) |
| `types/src/port/base/types.ts` | All config types |
| `types/src/port/instances/` | 9 port implementations |
| `types/src/port/plugins/` | Validation plugins |
| `types/src/port/factory/PortFactory.ts` | Port creation |
| `types/src/port/transfer-rules/` | Compatibility rules |
| `frontend/src/store/ports-v2/` | Frontend Effector stores |
| `frontend/src/components/flow/nodes/ChaingraphNode/ports/` | UI components |

---

## Common Patterns

### Creating a Port with Validation

```typescript
@Input()
@PortString({
  defaultValue: '',
  minLength: 1,
  maxLength: 100,
  pattern: '^[a-zA-Z0-9_]+$',  // Alphanumeric + underscore only
})
@Description('Unique identifier (alphanumeric)')
identifier: string = ''
```

### Conditional Port Visibility

```typescript
@Input()
@PortEnum({
  options: [
    { value: 'simple', label: 'Simple' },
    { value: 'advanced', label: 'Advanced' },
  ],
  defaultValue: 'simple',
})
mode: 'simple' | 'advanced' = 'simple'

@PortVisibility({ showIf: (node) => node.getPort('mode')?.getValue() === 'advanced' })
@Input()
@PortObject({ schema: advancedSchema })
advancedConfig: AdvancedConfig
```

### Mutable Array Port

```typescript
@Input()
@PortArray({
  itemConfig: { type: 'string', defaultValue: '' },
  isMutable: true,       // Allow add/remove in UI
  minLength: 1,          // At least one item
  maxLength: 10,         // Maximum 10 items
})
tags: string[] = ['default']
```

---

## Related Skills

- `types-architecture` - Complete types package overview
- `frontend-architecture` - Frontend store organization
- `effector-patterns` - Store patterns for ports-v2
- `chaingraph-concepts` - What ports ARE conceptually
