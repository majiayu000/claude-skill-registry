---
name: trpc-flow-editing
description: ChainGraph flow editing tRPC layer for visual flow editor operations.
  Use when working on apps/chaingraph-backend or packages/chaingraph-trpc/server.
  Covers flow CRUD, node/edge operations, port updat
---

---
name: trpc-flow-editing
description: ChainGraph flow editing tRPC layer for visual flow editor operations. Use when working on apps/chaingraph-backend or packages/chaingraph-trpc/server. Covers flow CRUD, node/edge operations, port updates, real-time subscriptions, locking, version control. Triggers: flow procedure, addNode, removeNode, connectPorts, updatePortValue, subscribeToEvents, flowContextProcedure, chaingraph-backend, chaingraph-trpc, flowStore.
---

# tRPC Flow Editing Layer

This skill covers the tRPC procedures for flow editing operations in ChainGraph - the visual flow editor's backend API.

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                 Frontend (React + XYFlow)                       │
│                        │                                        │
│                   tRPC Client                                   │
│                   (WebSocket)                                   │
└────────────────────────┬───────────────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────────────┐
│              chaingraph-backend (Port 3001)                     │
│                        │                                        │
│   ┌────────────────────▼────────────────────────────────────┐  │
│   │                   appRouter                              │  │
│   │  ├─ flow: flowProcedures (25+ procedures)               │  │
│   │  ├─ edge: edgeProcedures                                │  │
│   │  ├─ nodeRegistry: nodeRegistryProcedures                │  │
│   │  ├─ secrets: secretProcedures                           │  │
│   │  ├─ mcp: mcpProcedures                                  │  │
│   │  └─ users: userProcedures                               │  │
│   └─────────────────────────────────────────────────────────┘  │
│                        │                                        │
│   ┌────────────────────▼────────────────────────────────────┐  │
│   │              FlowStore (PostgreSQL)                      │  │
│   │  - Locking mechanism                                     │  │
│   │  - Version control                                       │  │
│   │  - In-memory cache (optional)                           │  │
│   └─────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
packages/chaingraph-trpc/server/
├── router.ts                 # Main router composition
├── trpc.ts                   # tRPC init & middleware
├── context.ts                # Context creation
├── init.ts                   # Server initialization
│
├── procedures/
│   ├── flow/                 # Flow editing procedures
│   │   ├── index.ts          # Router definition (25+ procedures)
│   │   ├── flow-create.ts
│   │   ├── flow-get.ts
│   │   ├── flow-edit.ts
│   │   ├── flow-delete.ts
│   │   ├── flow-list.ts
│   │   ├── flow-fork.ts
│   │   ├── subscriptions.ts  # Real-time subscription
│   │   ├── add-node.ts
│   │   ├── remove-node.ts
│   │   ├── paste-nodes.ts
│   │   ├── connect-ports.ts
│   │   ├── remove-edge.ts
│   │   ├── update-node-ui.ts
│   │   ├── update-node-position.ts
│   │   ├── update-port-value.ts
│   │   └── __test__/
│   │
│   └── edge/
│       ├── index.ts
│       └── update-anchors.ts
│
└── stores/
    ├── flowStore/
    │   ├── types.ts          # IFlowStore interface
    │   ├── dbFlowStore.ts    # PostgreSQL implementation
    │   └── inMemoryFlowStore.ts
    │
    └── postgres/
        ├── schema.ts         # Drizzle schema
        └── store.ts          # DB operations

apps/chaingraph-backend/
└── src/
    ├── index.ts              # Entry point
    └── ws-server.ts          # WebSocket server
```

---

## Flow Procedures

**File**: `packages/chaingraph-trpc/server/procedures/flow/index.ts:39-66`

```typescript
export const flowProcedures = router({
  // ═══════════ FLOW CRUD ═══════════
  create,                    // Create new flow
  get,                       // Get full flow (nodes, edges)
  getMeta,                   // Get metadata only (efficient)
  list,                      // List user's flows
  delete: flowDelete,        // Delete flow
  edit,                      // Edit metadata
  fork,                      // Fork flow
  setForkRule,              // Set fork permissions
  setPublic,                // Set public/private

  // ═══════════ REAL-TIME ═══════════
  subscribeToEvents,        // Subscribe to flow events

  // ═══════════ NODE OPERATIONS ═══════════
  addNode,                  // Add node to flow
  removeNode,               // Remove node from flow
  pasteNodes,               // Paste multiple nodes (clipboard)
  updateNodeUI,             // Update UI (position, dimensions, style)
  updateNodeTitle,          // Update node title
  updateNodePosition,       // Move node (with version check)
  updateNodeParent,         // Update parent (for groups)

  // ═══════════ EDGE OPERATIONS ═══════════
  connectPorts,             // Create edge between ports
  removeEdge,               // Remove edge

  // ═══════════ PORT OPERATIONS ═══════════
  updatePortValue,          // Update port value
  updatePortUI,             // Update port UI metadata
  addFieldObjectPort,       // Add field to object port
  removeFieldObjectPort,    // Remove field from object port
  updateItemConfigArrayPort, // Update array item config
  appendElementArrayPort,   // Add array element
  removeElementArrayPort,   // Remove array element
})
```

---

## CRUD Procedures

### Create Flow

**File**: `packages/chaingraph-trpc/server/procedures/flow/flow-create.ts:13-37`

```typescript
export const create = authedProcedure
  .input(z.object({
    name: z.string(),
    description: z.string().optional(),
    tags: z.array(z.string()).optional(),
  }))
  .mutation(async ({ input, ctx }) => {
    const userId = ctx.session?.user?.id
    if (!userId) {
      throw new Error('User not authenticated')
    }

    const flow = await ctx.flowStore.createFlow({
      name: input.name,
      description: input.description,
      createdAt: new Date(),
      updatedAt: new Date(),
      tags: input.tags,
      ownerID: userId,
      forkRule: FORK_DENY_RULE,
      schemaVersion: 'v2',
    })

    return flow.metadata
  })
```

### Get Flow

**File**: `packages/chaingraph-trpc/server/procedures/flow/flow-get.ts:12-23`

```typescript
export const get = flowContextProcedure
  .input(z.object({
    flowId: z.string(),
  }))
  .query(async ({ input, ctx }) => {
    const flow = await ctx.flowStore.getFlow(input.flowId)
    if (!flow) {
      throw new Error(`Flow ${input.flowId} not found`)
    }
    return flow  // Full flow with nodes, edges
  })
```

### List Flows

**File**: `packages/chaingraph-trpc/server/procedures/flow/flow-list.ts:14-67`

Returns metadata only (efficient for list views):

```typescript
export const list = authedProcedure
  .query(async ({ ctx }) => {
    const userId = ctx.session?.user?.id
    if (!userId) {
      throw new Error('User not authenticated')
    }

    const flows = await ctx.flowStore.listFlows(
      userId,
      'updatedAtDesc',  // Sort by last modified
      defaultFlowLimit,
    )

    // Compute canFork for each flow
    return flows.map(flow => ({
      ...flow.metadata,
      canFork: safeApplyJsonLogic(flow.forkRule, {
        userId,
        isOwner: flow.ownerID === userId,
      }),
    }))
  })
```

### Edit Flow Metadata

**File**: `packages/chaingraph-trpc/server/procedures/flow/flow-edit.ts:13-47`

```typescript
export const edit = flowContextProcedure
  .input(z.object({
    flowId: z.string(),
    name: z.string().optional(),
    description: z.string().optional(),
    tags: z.array(z.string()).optional(),
  }))
  .mutation(async ({ input, ctx }) => {
    await ctx.flowStore.lockFlow(input.flowId)

    try {
      const flow = await ctx.flowStore.getFlow(input.flowId)
      if (!flow) {
        throw new Error(`Flow ${input.flowId} not found`)
      }

      // Update metadata fields
      if (input.name !== undefined) flow.metadata.name = input.name
      if (input.description !== undefined) flow.metadata.description = input.description
      if (input.tags !== undefined) flow.metadata.tags = input.tags
      flow.metadata.updatedAt = new Date()

      await ctx.flowStore.updateFlow(flow)
      return flow.metadata
    } finally {
      await ctx.flowStore.unlockFlow(input.flowId)
    }
  })
```

---

## Node Operations

### Add Node

**File**: `packages/chaingraph-trpc/server/procedures/flow/add-node.ts:35-120`

```typescript
export const addNode = flowContextProcedure
  .input(z.object({
    flowId: z.string(),
    nodeType: z.string(),
    position: z.object({ x: z.number(), y: z.number() }),
    metadata: z.object({
      title: z.string().optional(),
      description: z.string().optional(),
      category: z.string().optional(),
      tags: z.array(z.string()).optional(),
    }).optional(),
    portsConfig: z.map(z.string(), z.any()).optional(),
  }))
  .mutation(async ({ input, ctx }) => {
    await ctx.flowStore.lockFlow(input.flowId)

    try {
      const flow = await ctx.flowStore.getFlow(input.flowId)
      if (!flow) {
        throw new Error(`Flow ${input.flowId} not found`)
      }

      // 1. Generate node ID
      const nodeId = `NO${generateShortId(16)}`

      // 2. Create node from registry
      const node = ctx.nodeRegistry.createNode(input.nodeType, nodeId)

      // 3. Initialize ports (with optional config)
      if (input.portsConfig) {
        for (const [portId, config] of input.portsConfig) {
          const port = node.getPort(portId)
          if (port) {
            const deserializedConfig = PortPluginRegistry.deserializeConfig(config)
            port.setConfig(deserializedConfig)
          }
        }
      }

      // 4. Set metadata
      node.metadata = {
        ...node.metadata,
        ...input.metadata,
        ui: {
          position: input.position,
        },
      }

      // 5. Add to flow → triggers NodesAdded event
      await flow.addNode(node)

      // 6. Set status → triggers NodeUpdated event
      node.setStatus(NodeStatus.Initialized)

      // 7. Persist
      await ctx.flowStore.updateFlow(flow)

      return {
        nodeId: node.id,
        metadata: node.metadata,
      }
    } finally {
      await ctx.flowStore.unlockFlow(input.flowId)
    }
  })
```

### Update Node Position

**File**: `packages/chaingraph-trpc/server/procedures/flow/update-node-position.ts:15-76`

Uses version control for optimistic locking:

```typescript
export const updateNodePosition = flowContextProcedure
  .input(z.object({
    flowId: z.string(),
    nodeId: z.string(),
    x: z.number(),
    y: z.number(),
    version: z.number(),  // Client's version
  }))
  .mutation(async ({ input, ctx }) => {
    await ctx.flowStore.lockFlow(input.flowId)

    try {
      const flow = await ctx.flowStore.getFlow(input.flowId)
      if (!flow) throw new Error(`Flow ${input.flowId} not found`)

      const node = flow.getNode(input.nodeId)
      if (!node) throw new Error(`Node ${input.nodeId} not found`)

      // VERSION CONTROL: Check for stale update
      if (node.getVersion() >= input.version) {
        // Client's version is stale - return current state
        return {
          position: node.metadata.ui?.position,
          version: node.getVersion(),
        }
      }

      // Apply update
      node.setPosition(input.x, input.y)
      await flow.updateNode(node)
      await ctx.flowStore.updateFlow(flow)

      return {
        position: { x: input.x, y: input.y },
        version: node.getVersion(),  // New version
      }
    } finally {
      await ctx.flowStore.unlockFlow(input.flowId)
    }
  })
```

### Paste Nodes

**File**: `packages/chaingraph-trpc/server/procedures/flow/paste-nodes.ts:70-end`

Complex operation for clipboard paste:

```typescript
export const pasteNodes = flowContextProcedure
  .input(z.object({
    flowId: z.string(),
    clipboard: z.object({
      nodes: z.array(SerializedNodeSchema),
      edges: z.array(SerializedEdgeSchema),
    }),
    position: z.object({ x: z.number(), y: z.number() }),
  }))
  .mutation(async ({ input, ctx }) => {
    await ctx.flowStore.lockFlow(input.flowId)

    try {
      // 1. Create node ID mapping (old → new)
      const nodeIdMap = new Map<string, string>()
      for (const serializedNode of input.clipboard.nodes) {
        nodeIdMap.set(serializedNode.id, `NO${generateShortId(16)}`)
      }

      // 2. Clone nodes with new IDs
      const newNodes: INode[] = []
      for (const serializedNode of input.clipboard.nodes) {
        const node = deserializeNode(serializedNode)
        node.id = nodeIdMap.get(serializedNode.id)!

        // Adjust position relative to paste point
        node.metadata.ui.position = {
          x: serializedNode.metadata.ui.position.x + input.position.x,
          y: serializedNode.metadata.ui.position.y + input.position.y,
        }

        newNodes.push(node)
      }

      // 3. Rebuild edges with new node IDs
      const newEdges: IEdge[] = []
      for (const serializedEdge of input.clipboard.edges) {
        const newSourceId = nodeIdMap.get(serializedEdge.sourceNodeId)
        const newTargetId = nodeIdMap.get(serializedEdge.targetNodeId)
        if (newSourceId && newTargetId) {
          newEdges.push(createEdge({
            sourceNodeId: newSourceId,
            sourcePortId: serializedEdge.sourcePortId,
            targetNodeId: newTargetId,
            targetPortId: serializedEdge.targetPortId,
          }))
        }
      }

      // 4. Add all to flow (batch)
      await flow.addNodes(newNodes)
      await flow.addEdges(newEdges)
      await ctx.flowStore.updateFlow(flow)

      return { nodeIds: newNodes.map(n => n.id) }
    } finally {
      await ctx.flowStore.unlockFlow(input.flowId)
    }
  })
```

---

## Edge Operations

### Connect Ports

**File**: `packages/chaingraph-trpc/server/procedures/flow/connect-ports.ts:13-73`

```typescript
export const connectPorts = flowContextProcedure
  .input(z.object({
    flowId: z.string(),
    sourceNodeId: z.string(),
    sourcePortId: z.string(),
    targetNodeId: z.string(),
    targetPortId: z.string(),
    metadata: z.object({
      label: z.string().optional(),
      description: z.string().optional(),
    }).optional(),
  }))
  .mutation(async ({ input, ctx }) => {
    await ctx.flowStore.lockFlow(input.flowId)

    try {
      const flow = await ctx.flowStore.getFlow(input.flowId)
      if (!flow) throw new Error(`Flow ${input.flowId} not found`)

      // Validates port compatibility internally
      const edge = await flow.connectPorts(
        input.sourceNodeId,
        input.sourcePortId,
        input.targetNodeId,
        input.targetPortId,
        input.metadata,
      )

      await ctx.flowStore.updateFlow(flow)

      return {
        edgeId: edge.id,
        sourceNodeId: input.sourceNodeId,
        sourcePortId: input.sourcePortId,
        targetNodeId: input.targetNodeId,
        targetPortId: input.targetPortId,
      }
    } finally {
      await ctx.flowStore.unlockFlow(input.flowId)
    }
  })
```

### Update Edge Anchors

**File**: `packages/chaingraph-trpc/server/procedures/edge/update-anchors.ts:18-81`

Batch update with version control:

```typescript
export const updateAnchors = flowContextProcedure
  .input(z.object({
    flowId: z.string(),
    edgeId: z.string(),
    anchors: z.array(EdgeAnchorSchema),
    version: z.number(),
  }))
  .mutation(async ({ input, ctx }) => {
    await ctx.flowStore.lockFlow(input.flowId)

    try {
      const flow = await ctx.flowStore.getFlow(input.flowId)
      const edge = flow?.getEdge(input.edgeId)
      if (!edge) throw new Error(`Edge ${input.edgeId} not found`)

      // VERSION CONTROL
      const currentVersion = edge.metadata.version ?? 0
      if (currentVersion > input.version) {
        return {
          anchors: edge.metadata.anchors,
          version: currentVersion,
          stale: true,  // Signal client to refresh
        }
      }

      // Validate anchors (parent nodes exist, are groups)
      for (const anchor of input.anchors) {
        if (anchor.parentNodeId) {
          const parentNode = flow.getNode(anchor.parentNodeId)
          if (!parentNode || parentNode.metadata.type !== 'groupNode') {
            throw new Error(`Invalid parent node for anchor`)
          }
        }
      }

      // Apply update
      edge.metadata.anchors = input.anchors
      edge.metadata.version = currentVersion + 1
      await flow.updateEdgeMetadata(edge)
      await ctx.flowStore.updateFlow(flow)

      return {
        anchors: edge.metadata.anchors,
        version: edge.metadata.version,
        stale: false,
      }
    } finally {
      await ctx.flowStore.unlockFlow(input.flowId)
    }
  })
```

---

## Port Operations

### Update Port Value

**File**: `packages/chaingraph-trpc/server/procedures/flow/update-port-value.ts:25-81`

Uses batch update to prevent multiple events:

```typescript
export const updatePortValue = flowContextProcedure
  .input(z.object({
    flowId: z.string(),
    nodeId: z.string(),
    portId: z.string(),
    value: z.any(),
  }))
  .mutation(async ({ input, ctx }) => {
    await ctx.flowStore.lockFlow(input.flowId)

    try {
      const flow = await ctx.flowStore.getFlow(input.flowId)
      const node = flow?.getNode(input.nodeId)
      const port = node?.getPort(input.portId)
      if (!port) throw new Error(`Port not found`)

      // START BATCH MODE - collect updates without emitting
      node.startBatchUpdate()

      // Update port value
      port.setValue(input.value)

      // Propagate to parent ports (for nested ports)
      const portsToUpdate = [port]
      let currentPort = port
      while (currentPort.getConfig().parentId) {
        const parentPort = node.getPort(currentPort.getConfig().parentId!)
        if (parentPort) {
          portsToUpdate.push(parentPort)
          currentPort = parentPort
        } else {
          break
        }
      }

      // Collect updates
      node.updatePorts(portsToUpdate)

      // COMMIT - emits all updates at once
      await flow.updateNode(node)
      await ctx.flowStore.updateFlow(flow)

      return { success: true }
    } finally {
      await ctx.flowStore.unlockFlow(input.flowId)
    }
  })
```

### Object Port Field Operations

**File**: `packages/chaingraph-trpc/server/procedures/flow/update-port-value.ts:83-240`

```typescript
// Add field to object port
export const addFieldObjectPort = flowContextProcedure
  .input(z.object({
    flowId: z.string(),
    nodeId: z.string(),
    portId: z.string(),
    key: z.string(),
    fieldConfig: PortConfigSchema,
  }))
  .mutation(async ({ input, ctx }) => {
    // Validates port is object type
    // Checks key doesn't already exist
    // Creates child port via node.addObjectProperty()
    // Triggers PortCreate event
  })

// Remove field from object port
export const removeFieldObjectPort = flowContextProcedure
  .input(z.object({
    flowId: z.string(),
    nodeId: z.string(),
    portId: z.string(),
    key: z.string(),
  }))
  .mutation(async ({ input, ctx }) => {
    // Finds child port by key
    // Removes port, descendants, and connections via flow.removePort()
    // Triggers PortDelete event
    // Propagates PortUpdate to parent ports
  })
```

---

## Real-Time Subscription

**File**: `packages/chaingraph-trpc/server/procedures/flow/subscriptions.ts:25-132`

### Event Sequence on Subscribe

```
1. FlowInitStart (metadata)           ← Signals start
2. NodesAdded (non-parented nodes)    ← Root nodes first
3. NodesAdded (parented nodes)        ← Child nodes second
4. EdgesAdded (all edges)             ← Then edges
5. FlowInitEnd                        ← Commit signal
6. [future events streamed...]        ← Real-time updates
```

### Implementation

```typescript
export const subscribeToEvents = flowContextProcedure
  .input(z.object({
    flowId: z.string(),
    eventTypes: z.array(z.nativeEnum(FlowEventType)).optional(),
    lastEventId: z.string().nullish(),
  }))
  .output(zAsyncIterable({
    yield: z.custom<FlowEvent>(),
    tracked: true,
  }))
  .subscription(async function* ({ input, ctx }) {
    const { flowId, eventTypes, lastEventId } = input
    const flow = await ctx.flowStore.getFlow(flowId)

    if (!flow) {
      throw new Error(`Flow with ID ${flowId} not found`)
    }

    let eventIndex = Number(lastEventId) || 0
    const eventQueue = new EventQueue<FlowEvent>(1000)

    try {
      // Subscribe to future events
      const unsubscribe = flow.onEvent(async (event) => {
        if (!isAcceptedEventType(eventTypes, event.type)) return
        await eventQueue.publish(event)
      })

      // 1. FlowInitStart
      yield tracked(String(eventIndex++), newEvent(
        eventIndex, flowId, FlowEventType.FlowInitStart,
        { flowId, metadata: flow.metadata }
      ))

      // 2. NodesAdded (root nodes)
      const rootNodes = flow.getNodes().filter(n => !n.metadata.parentNodeId)
      if (rootNodes.length > 0) {
        yield tracked(String(eventIndex++), newEvent(
          eventIndex, flowId, FlowEventType.NodesAdded,
          { nodes: rootNodes.map(serializeNode) }
        ))
      }

      // 3. NodesAdded (child nodes)
      const childNodes = flow.getNodes().filter(n => n.metadata.parentNodeId)
      if (childNodes.length > 0) {
        yield tracked(String(eventIndex++), newEvent(
          eventIndex, flowId, FlowEventType.NodesAdded,
          { nodes: childNodes.map(serializeNode) }
        ))
      }

      // 4. EdgesAdded
      const edges = flow.getEdges()
      if (edges.length > 0) {
        yield tracked(String(eventIndex++), newEvent(
          eventIndex, flowId, FlowEventType.EdgesAdded,
          { edges: edges.map(serializeEdge) }
        ))
      }

      // 5. FlowInitEnd
      yield tracked(String(eventIndex++), newEvent(
        eventIndex, flowId, FlowEventType.FlowInitEnd, {}
      ))

      // 6. Stream future events
      const iterator = createQueueIterator(eventQueue)
      for await (const event of iterator) {
        yield tracked(String(eventIndex++), event)
      }
    } finally {
      await eventQueue.close()
    }
  })
```

---

## Flow Locking

**File**: `packages/chaingraph-trpc/server/stores/flowStore/dbFlowStore.ts:245-300`

### Lock Queue Implementation

```typescript
private lockQueues: Map<string, {
  locked: boolean
  waitQueue: Array<{ resolve: () => void, reject: (error: Error) => void }>
}>

async lockFlow(flowId: string, timeout = 5000): Promise<void> {
  // Check flow exists
  const flow = await this.getFlow(flowId)
  if (!flow) {
    throw new Error(`Flow ${flowId} not found`)
  }

  // Initialize queue if needed
  if (!this.lockQueues.has(flowId)) {
    this.lockQueues.set(flowId, { locked: false, waitQueue: [] })
  }

  const queue = this.lockQueues.get(flowId)!

  // If already locked, wait in queue
  if (queue.locked) {
    return new Promise((resolve, reject) => {
      // Add to wait queue
      queue.waitQueue.push({ resolve, reject })

      // Setup timeout
      setTimeout(() => {
        const index = queue.waitQueue.findIndex(w => w.resolve === resolve)
        if (index !== -1) {
          queue.waitQueue.splice(index, 1)
          reject(new Error(`Lock timeout for flow ${flowId}`))
        }
      }, timeout)
    })
  }

  // Acquire lock immediately
  queue.locked = true
}

async unlockFlow(flowId: string): Promise<void> {
  const queue = this.lockQueues.get(flowId)
  if (!queue) return

  // Grant lock to next waiter
  if (queue.waitQueue.length > 0) {
    const next = queue.waitQueue.shift()!
    next.resolve()  // They get the lock
  } else {
    queue.locked = false
  }
}
```

### Usage Pattern

**Every mutation follows this pattern:**

```typescript
await ctx.flowStore.lockFlow(flowId)
try {
  const flow = await ctx.flowStore.getFlow(flowId)
  // ... mutation logic ...
  await ctx.flowStore.updateFlow(flow)
} finally {
  await ctx.flowStore.unlockFlow(flowId)  // Always release
}
```

---

## Database Schema

**File**: `packages/chaingraph-trpc/server/stores/postgres/schema.ts`

```typescript
export const chaingraph_flows = pgTable('chaingraph_flows', {
  id: text('id').primaryKey(),
  data: jsonb('data').notNull(),       // Full flow serialization
  createdAt: timestamp('created_at'),
  updatedAt: timestamp('updated_at'),
  ownerId: text('owner_id'),
  parentId: text('parent_id'),         // For forked flows
  version: integer('version').default(1),  // Optimistic locking
}, (table) => ({
  ownerCreatedAtIndex: index('flows_owner_created_at_idx').on(table.ownerId, table.createdAt),
  ownerUpdatedAtIndex: index('flows_owner_updated_at_idx').on(table.ownerId, table.updatedAt),
  parentIdIndex: index('flows_parent_id_idx').on(table.parentId),
}))

export const chaingraph_users = pgTable('chaingraph_users', {
  id: text('id').primaryKey(),         // USR... format
  email: text('email'),
  displayName: text('display_name'),
  avatarUrl: text('avatar_url'),
  role: text('role').default('user'),  // 'user' | 'admin' | 'agent'
  createdAt: timestamp('created_at'),
  updatedAt: timestamp('updated_at'),
  lastLoginAt: timestamp('last_login_at'),
  metadata: jsonb('metadata'),
})

export const chaingraph_external_accounts = pgTable('chaingraph_external_accounts', {
  id: text('id').primaryKey(),
  userId: text('user_id').references(() => chaingraph_users.id),
  provider: text('provider'),          // 'google', 'github', etc.
  externalId: text('external_id'),
  externalEmail: text('external_email'),
  displayName: text('display_name'),
  avatarUrl: text('avatar_url'),
  metadata: jsonb('metadata'),
}, (table) => ({
  uniqueProviderExternal: uniqueIndex('unique_provider_external').on(table.provider, table.externalId),
}))
```

---

## Key Files

| File | Purpose |
|------|---------|
| `packages/chaingraph-trpc/server/procedures/flow/index.ts` | Flow router (25+ procedures) |
| `packages/chaingraph-trpc/server/procedures/flow/subscriptions.ts` | Real-time subscription |
| `packages/chaingraph-trpc/server/procedures/flow/add-node.ts` | Node creation |
| `packages/chaingraph-trpc/server/procedures/flow/connect-ports.ts` | Edge creation |
| `packages/chaingraph-trpc/server/procedures/flow/update-port-value.ts` | Port updates |
| `packages/chaingraph-trpc/server/procedures/edge/update-anchors.ts` | Anchor updates |
| `packages/chaingraph-trpc/server/stores/flowStore/dbFlowStore.ts` | Flow storage + locking |
| `packages/chaingraph-trpc/server/stores/postgres/schema.ts` | Database schema |
| `apps/chaingraph-backend/src/index.ts` | Server entry point |

---

## Quick Reference

| Operation | Procedure | Key Pattern |
|-----------|-----------|-------------|
| Create flow | `flow.create` | `authedProcedure` |
| Get flow | `flow.get` | `flowContextProcedure` |
| Add node | `flow.addNode` | Lock → create → unlock |
| Move node | `flow.updateNodePosition` | Version check → update |
| Connect | `flow.connectPorts` | Lock → validate → create edge |
| Update port | `flow.updatePortValue` | Batch mode → propagate to parents |
| Subscribe | `flow.subscribeToEvents` | Init sequence → stream future |

---

## Related Skills

- `trpc-patterns` - General tRPC framework patterns
- `trpc-execution` - Execution tRPC layer
- `subscription-sync` - Frontend subscription handling
- `optimistic-updates` - Optimistic UI patterns
