---
name: dojo-state
description: |
  Use when managing game state with Zustand in dojo.js.
  Triggers: dojo state, zustand dojo, game state, createDojoStore, optimistic update,
  getEntity, mergeEntities, state management, revert transaction
---

# Dojo.js State Management

## When to Use

Use this skill when:
- Setting up the Zustand store for game state
- Accessing entities from the store
- Implementing optimistic updates
- Working with historical entity data

## Store Setup

```typescript
import { createDojoStore } from "@dojoengine/sdk/react";
import type { GameState } from "@dojoengine/state/zustand";

// Create typed store
const useDojoStore = createDojoStore<typeof schema>();
```

## GameState Interface

```typescript
interface GameState<T> {
    entities: Record<string, ParsedEntity<T>>;
    historical_entities: Record<string, ParsedEntity<T>[]>;
    pendingTransactions: Record<string, PendingTransaction>;

    // Entity operations
    setEntities: (entities: ParsedEntity<T>[]) => void;
    mergeEntities: (entities: ParsedEntity<T>[]) => void;
    updateEntity: (entity: Partial<ParsedEntity<T>>) => void;

    // Historical operations
    setHistoricalEntities: (entities: ParsedEntity<T>[]) => void;
    mergeHistoricalEntities: (entities: ParsedEntity<T>[]) => void;

    // Optimistic updates
    applyOptimisticUpdate: (transactionId: string, updateFn: (draft) => void) => void;
    revertOptimisticUpdate: (transactionId: string) => void;
    confirmTransaction: (transactionId: string) => void;

    // Queries
    getEntity: (entityId: string) => ParsedEntity<T> | undefined;
    getEntities: (filter?: (entity) => boolean) => ParsedEntity<T>[];
    getEntitiesByModel: (namespace: keyof T, model: keyof T[keyof T]) => ParsedEntity<T>[];
    getHistoricalEntities: (entityId: string) => ParsedEntity<T>[];

    // Subscriptions
    subscribeToEntity: (entityId: string, listener: (entity) => void) => () => void;
    waitForEntityChange: (entityId: string, predicate: (entity) => boolean, timeout?: number) => Promise<ParsedEntity<T> | undefined>;

    // Cleanup
    resetStore: () => void;
}
```

## Accessing Store Data

```tsx
import { useDojoSDK } from "@dojoengine/sdk/react";

function GameComponent() {
    const { useDojoStore } = useDojoSDK();

    // Get single entity
    const player = useDojoStore(state => state.getEntity(entityId));

    // Get all entities with filter
    const activePlayers = useDojoStore(state =>
        state.getEntities(e => e.models?.game?.Player?.isActive)
    );

    // Get entities by model
    const allPlayers = useDojoStore(state =>
        state.getEntitiesByModel("game", "Player")
    );
}
```

## Optimistic Updates

Optimistic updates show changes immediately while the transaction confirms:

```tsx
function movePlayer(direction: string) {
    const { useDojoStore, provider } = useDojoSDK();
    const store = useDojoStore.getState();

    const transactionId = `move-${Date.now()}`;

    // 1. Apply optimistic update immediately
    store.applyOptimisticUpdate(transactionId, (draft) => {
        const entity = draft.entities[entityId];
        if (entity?.models?.game?.Position) {
            entity.models.game.Position.x += direction === "right" ? 1 : -1;
        }
    });

    try {
        // 2. Execute the actual transaction
        await provider.execute(account, {
            contractName: "actions",
            entrypoint: "move",
            calldata: [direction]
        }, "game");

        // 3. Confirm on success (removes pending state)
        store.confirmTransaction(transactionId);
    } catch (error) {
        // 4. Revert on failure
        store.revertOptimisticUpdate(transactionId);
    }
}
```

## Entity Subscriptions

```tsx
function useEntitySubscription(entityId: string) {
    const { useDojoStore } = useDojoSDK();
    const store = useDojoStore.getState();

    useEffect(() => {
        const unsubscribe = store.subscribeToEntity(entityId, (entity) => {
            console.log("Entity changed:", entity);
        });

        return () => unsubscribe();
    }, [entityId]);
}
```

## Waiting for Entity Changes

```tsx
async function waitForMove(entityId: string) {
    const { useDojoStore } = useDojoSDK();
    const store = useDojoStore.getState();

    const entity = await store.waitForEntityChange(
        entityId,
        (entity) => entity?.models?.game?.Position?.x > 10,
        30000 // 30 second timeout
    );

    if (entity) {
        console.log("Player reached position:", entity.models.game.Position);
    }
}
```

## Historical Entities

```tsx
function PlayerTimeline({ entityId }) {
    const { useDojoStore } = useDojoSDK();

    const history = useDojoStore(state =>
        state.getHistoricalEntities(entityId)
    );

    return (
        <ul>
            {history.map((snapshot, i) => (
                <li key={i}>
                    Position: ({snapshot.models.game.Position.x}, {snapshot.models.game.Position.y})
                </li>
            ))}
        </ul>
    );
}
```

## Merging Entities from Subscriptions

```tsx
const { sdk, useDojoStore } = useDojoSDK();

await sdk.subscribeEntityQuery({
    query: query,
    callback: ({ data }) => {
        if (data) {
            // Merge updates into store
            useDojoStore.getState().mergeEntities([data]);
        }
    }
});
```

## Common Pitfalls

1. **Forgetting to confirm/revert**: Always handle both success and error cases for optimistic updates
2. **Stale closures**: Use `useDojoStore.getState()` for callbacks to avoid stale state
3. **Over-subscribing**: Use selectors to minimize re-renders
4. **Missing cleanup**: Always unsubscribe from entity subscriptions on unmount
