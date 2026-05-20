---
name: 40-04-ts-domain-logic-separation
description: "TS/React: Business logic lives in pure modules. Not in React hooks. Not in closures. Not in callbacks. Prevents untestable, unreasonable code."
---

# 40.04 Domain Logic Separation (TypeScript / React)

Business logic lives in pure modules that can be tested with plain function calls. The view layer visualizes. Stores hold state. Pure functions compute.

## The Problem

Logic in the wrong place:

```typescript
// WRONG — logic in React hook
function useWarpSpeed() {
  const [speed, setSpeed] = useState(0);
  useEffect(() => {
    const interval = setInterval(() => {
      setSpeed(prev => {
        if (prev > maxSpeed) return maxSpeed;  // business rule buried in React
        return prev + acceleration * dt;        // physics in a useEffect
      });
    }, 16);
    return () => clearInterval(interval);
  }, []);
}

// WRONG — logic in closure callback
conn.db.shipComponent.onInsert((_, row) => {
  // 50 lines of entity creation, ECS component setup, visual sync...
  // untestable without mocking the entire subscription system
});
```

## The Rule

| Layer | Responsibility | Tests with |
|-------|---------------|------------|
| Pure functions | Compute, transform, decide | Plain unit tests — `expect(fn(input)).toBe(output)` |
| Stores / shared state | Hold state, expose reads | Store tests — set state, assert reads |
| Domain modules | Orchestrate: read state → compute → write state | Integration tests against shared state |
| React components | Visualize state, dispatch actions | Visual tests (Playwright, Storybook) |
| Callbacks / handlers | Thin glue — call into domain modules | Don't test these directly — test the domain module |

## How to Apply

### 1. Extract the logic

When you find logic inside React, a callback, or a closure:

```typescript
// Before: logic in callback
conn.db.shipComponent.onInsert((_, row) => {
  const eid = addEntity(world);
  addComponent(world, Position, eid);
  Position.x[eid] = row.x;
  // ... 40 more lines
});

// After: thin callback → domain function
conn.db.shipComponent.onInsert((_, row) => upsertShip(row.entityId));

// Domain function — testable, readable, reusable
export const upsertShip = (entityId: string) => {
  const position = positions.get(entityId);
  if (!position) return;
  const eid = addEntity(bridge.world!);
  // ...
};
```

### 2. Keep callbacks thin

Callbacks are glue. They translate events into domain function calls. A callback longer than 5 lines probably contains domain logic that should be extracted.

### 3. React components read and dispatch

```typescript
// Component reads from store, dispatches actions
function WarpButton() {
  const isWarping = useSpacetimeStore(s => s.isWarping);
  return <Button onClick={() => travelActions.engageWarp(targetId)} />;
}
```

The component doesn't know how warp works. It knows the state and the action.

## The Test

> Can I test this logic with a plain function call and an `expect()`?

If no — the logic is in the wrong place. Extract it.

## Relationship to Other Principles

- **40.01 State Ownership** — domain logic reads from owned state, writes to owned state
- **40.02 Module Boundaries** — domain modules are the natural extraction unit
- **40.03 Dependency Direction** — domain logic sits in the middle layer, importing state, imported by UI
- **40.05 Singleton Patterns (TS)** — domain modules read from singleton refs, not injected deps
