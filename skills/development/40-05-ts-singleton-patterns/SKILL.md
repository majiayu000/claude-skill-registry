---
name: 40-05-ts-singleton-patterns
description: "TS: When something has one instance, use a module-level ref. Not a factory. Not a class. Not a closure. Prevents over-engineering and hidden coupling."
---

# 40.05 Singleton Patterns (TypeScript)

When there is exactly one instance of something for the lifetime of the app, represent it as a module-level ref. Period.

## The Decision Tree

```
Is there ever more than one instance?
├── Yes → Factory or class (createEntitySync, createProjectileLifecycle)
└── No → Module-level ref
    ├── Set once at init → ref object (bridge.world, bridge.renderer)
    ├── Mutates over time → ref object (stdb.connection, stdb.connectionState)
    └── Collection → exported Map/Set (shipEntities, positions)
```

## The Patterns

### Module-level ref object (mutable singleton state)

```typescript
// client-state.ts
export const stdb = {
  connection: null as DbConnection | null,
  connectionState: "connecting" as SpacetimeConnectionState,
  playerShipEntityId: null as string | null,
};
```

Set at runtime. Read from anywhere. One owner writes each field (see 40.01).

### Module-level collection (shared data)

```typescript
// client-state.ts
export const shipEntities = new Map<string, number>();
export const positions = new Map<string, PositionRow>();
```

No wrapper. No getter. Just the Map. Everyone who needs it imports it.

### Constructor-time refs (set once, never change)

```typescript
// client-state.ts
export const bridge = {
  world: null as IWorld | null,
  renderer: null as GameRenderer | null,
  prediction: null as PlayerShipPrediction | null,
};

// spacetime-client.ts (at init)
bridge.world = options.world;
bridge.renderer = options.renderer;
```

These are `null` until init, then stable forever. The `!` assertion in consumers is justified — these are only accessed after init.

## Wrong Patterns

### Factory for a singleton

```typescript
// WRONG — factory creates one instance, returns it, done. Why the ceremony?
export function createEcsBridge(deps: { world: IWorld; renderer: GameRenderer }) {
  return {
    upsertShip: (id: string) => { deps.world... },
    removeShip: (id: string) => { deps.renderer... },
  };
}
// Caller: const bridge = createEcsBridge({ world, renderer });
// Nobody ever calls createEcsBridge again.
```

```typescript
// RIGHT — module-level functions reading from a ref
export const bridge = { world: null as IWorld | null, renderer: null as GameRenderer | null };
export const upsertShip = (id: string) => { bridge.world!... };
export const removeShip = (id: string) => { bridge.renderer!... };
```

Same behavior. Less indirection. Testable by setting `bridge.world` directly. No mock factory needed.

### Closure capture for "encapsulation"

```typescript
// WRONG — closure makes testing impossible
function createClient() {
  let playerShipId: string | null = null;
  const getPlayerShipId = () => playerShipId;
  // ... 2000 lines that read/write playerShipId
  return { getPlayerShipId };
}
```

The closure doesn't protect anything — it just makes the state invisible. In a codebase with one client, "encapsulation" of its internals is cargo cult OOP.

### Class for no reason

```typescript
// WRONG — class with one instance, constructed once
class SpacetimeClient {
  private connection: DbConnection | null = null;
  private playerShipId: string | null = null;
  // ... methods
}
const client = new SpacetimeClient(options);
```

This is a factory pattern with `new` instead of `create`. Same problem: state is trapped behind an instance. Use a ref object + standalone functions.

## When Factories ARE Right

Factories are for things with **multiple instances** or **parameterized behavior**:

```typescript
// RIGHT — multiple instances with different configs
const prediction = createPlayerShipPrediction();       // one per player
const projectileLifecycle = createProjectileLifecycle(); // one per entity type

// RIGHT — parameterized behavior
const visualSync = createVisualSync({
  renderer, shipEntities, buildShipData, ...
});
```

Even here, if the factory is called exactly once and the result is stored in a ref — consider whether it's actually a singleton in disguise.

## The Smell Test

> Does this factory get called more than once?

If no — it's a singleton. Kill the factory. Use a ref.
