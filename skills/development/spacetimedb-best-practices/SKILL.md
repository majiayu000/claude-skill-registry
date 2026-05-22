---
name: spacetimedb-best-practices
description: SpacetimeDB development best practices for TypeScript server modules and client SDK. This skill should be used when writing, reviewing, or refactoring SpacetimeDB code to ensure optimal patterns for real-time, multiplayer applications. Triggers on tasks involving SpacetimeDB modules, tables, reducers, subscriptions, or React integration.
license: MIT
metadata:
  author: spacetimedb
  version: "2.0.0"
---

# SpacetimeDB Best Practices

Comprehensive development guide for SpacetimeDB applications, covering both TypeScript server modules and client SDK integration with React. Contains rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

**Package:** `spacetimedb` (v1.4.0+)

## When to Apply

Reference these guidelines when:
- Writing SpacetimeDB server modules in TypeScript
- Designing table schemas and indexes
- Implementing reducers for state mutations
- Setting up client subscriptions and queries
- Integrating SpacetimeDB with React applications
- Optimizing real-time sync performance

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Module Design | CRITICAL | `module-` |
| 2 | Table Schema & Indexing | CRITICAL | `table-` |
| 3 | Reducer Patterns | HIGH | `reducer-` |
| 4 | Subscription Optimization | HIGH | `subscription-` |
| 5 | Client State Management | MEDIUM-HIGH | `client-` |
| 6 | React Integration | MEDIUM | `react-` |
| 7 | TypeScript Patterns | MEDIUM | `ts-` |
| 8 | Real-time Sync | LOW-MEDIUM | `sync-` |

## Quick Reference

### Server Module API (TypeScript)

```typescript
import { spacetimedb, table, t, ReducerContext } from 'spacetimedb';

// Define tables with the table builder
const Player = table(
  { name: 'player', public: true },
  {
    identity: t.identity().primaryKey(),
    name: t.string(),
    score: t.u64().index(),
    isOnline: t.bool().index(),
  }
);

// Define reducers
spacetimedb.reducer('create_player', { name: t.string() }, (ctx: ReducerContext, { name }) => {
  ctx.db.player.insert({
    identity: ctx.sender,
    name,
    score: 0n,
    isOnline: true,
  });
});

// Lifecycle hooks
spacetimedb.init((ctx: ReducerContext) => { /* module init */ });
spacetimedb.clientConnected((ctx: ReducerContext) => { /* client connected */ });
spacetimedb.clientDisconnected((ctx: ReducerContext) => { /* client disconnected */ });
```

### Client SDK API (TypeScript)

```typescript
import { DbConnection } from './generated';

// Build connection
const conn = DbConnection.builder()
  .withUri('ws://localhost:3000')
  .withModuleName('my-module')
  .onConnect((ctx, identity, token) => {
    // Setup subscriptions
    conn.subscription(['SELECT * FROM player WHERE isOnline = true']);
  })
  .onDisconnect((ctx, error) => { /* handle disconnect */ })
  .build();

// Call reducers
await conn.reducers.createPlayer('Alice');

// Access tables
const player = conn.db.player.identity.find(identity);
```

### React Integration

```typescript
import { useTable, where, eq } from 'spacetimedb/react';
import { DbConnection, Player } from './generated';

function OnlinePlayers() {
  const { rows: players } = useTable<DbConnection, Player>(
    'player',
    where(eq('isOnline', true))
  );

  return players.map(p => <div key={p.identity.toHexString()}>{p.name}</div>);
}
```

## Rule Categories

### 1. Module Design (CRITICAL)

- `module-single-responsibility` - One module per domain concept
- `module-lifecycle` - Use lifecycle hooks appropriately (init, clientConnected, clientDisconnected)
- `module-error-handling` - Handle errors gracefully in module code
- `module-type-exports` - Export types for client consumption

### 2. Table Schema & Indexing (CRITICAL)

- `table-primary-keys` - Choose appropriate primary key strategies
- `table-indexing` - Add `.index()` for frequently queried columns
- `table-relationships` - Model relationships between tables correctly
- `table-column-types` - Use appropriate SpacetimeDB types

### 3. Reducer Patterns (HIGH)

- `reducer-atomicity` - Keep reducers atomic and focused
- `reducer-validation` - Validate inputs at reducer entry
- `reducer-authorization` - Check caller identity for sensitive operations
- `reducer-batch-operations` - Batch related mutations in single reducer

### 4. Subscription Optimization (HIGH)

- `subscription-selective` - Subscribe only to needed data
- `subscription-filters` - Use subscription filters to reduce data transfer
- `subscription-cleanup` - Clean up subscriptions when no longer needed
- `subscription-batching` - Batch subscription setup on client connect

### 5. Client State Management (MEDIUM-HIGH)

- `client-connection-lifecycle` - Handle connection/reconnection properly
- `client-optimistic-updates` - Use optimistic updates for responsive UI
- `client-error-recovery` - Handle reducer errors gracefully
- `client-identity` - Manage identity tokens securely

### 6. React Integration (MEDIUM)

- `react-use-subscription` - Use subscription hooks correctly
- `react-table-hooks` - Use `useTable<DbConnection, Type>()` for reactive data
- `react-reducer-hooks` - Call `conn.reducers.*` with proper error handling
- `react-connection-status` - Display connection status to users

### 7. TypeScript Patterns (MEDIUM)

- `ts-generated-types` - Use generated types from SpacetimeDB CLI
- `ts-strict-mode` - Enable strict TypeScript for better type safety
- `ts-discriminated-unions` - Use discriminated unions for state
- `ts-type-guards` - Implement type guards for runtime validation

### 8. Real-time Sync (LOW-MEDIUM)

- `sync-conflict-resolution` - Handle concurrent modifications
- `sync-offline-support` - Design for offline-first when needed
- `sync-debounce-updates` - Debounce rapid UI updates
- `sync-presence` - Implement user presence efficiently

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/module-single-responsibility.md
rules/table-primary-keys.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
