---
name: dojo-react
description: |
  Use for React integration patterns and best practices in dojo.js.
  Triggers: dojo react, react hooks, effect atoms, Result.match, infinite scroll dojo,
  DojoSdkProvider, useDojoSDK, react patterns
---

# Dojo.js React Patterns

## When to Use

Use this skill when:
- Setting up React provider hierarchy
- Using Effect atoms for complex async state
- Implementing infinite scroll
- Handling loading/error states

## Provider Hierarchy

Recommended order:

```tsx
import { StarknetConfig } from "@starknet-react/core";
import { DojoSdkProvider } from "@dojoengine/sdk/react";

function Providers({ children }) {
    return (
        <StarknetConfig connectors={connectors}>
            <DojoSdkProvider
                dojoConfig={dojoConfig}
                sdk={sdk}
                clientFn={createClient}
            >
                {children}
            </DojoSdkProvider>
        </StarknetConfig>
    );
}
```

## useDojoSDK Hook

```tsx
import { useDojoSDK } from "@dojoengine/sdk/react";

function GameComponent() {
    const {
        sdk,          // SDK instance
        config,       // DojoConfig
        client,       // Client from clientFn
        provider,     // DojoProvider
        useDojoStore  // Zustand store hook
    } = useDojoSDK();
}
```

## Effect Atoms (Recommended)

Effect atoms provide robust async state management:

### Entity Query Atom

```tsx
import { createEntityQueryAtom } from "@dojoengine/react/effect";
import { Result } from "@dojoengine/react/effect";

const playersAtom = createEntityQueryAtom(
    runtime,
    new ToriiQueryBuilder().addEntityModel("game-Player").withLimit(100)
);

function PlayerList() {
    const players = useAtomValue(playersAtom);

    return Result.match(players, {
        onSuccess: ({ value }) => (
            <ul>
                {value.items.map(p => <li key={p.entityId}>{p.models.game.Player.name}</li>)}
            </ul>
        ),
        onFailure: (error) => <div>Error: {error.message}</div>,
        onInitial: () => <div>Loading...</div>
    });
}
```

### Entity Updates Atom (Real-time)

```tsx
import { createEntityUpdatesAtom } from "@dojoengine/react/effect";

const updatesAtom = createEntityUpdatesAtom(
    runtime,
    KeysClause(["game-Player"], [], "VariableLen").build()
);
```

### Combined Query + Updates

```tsx
import { createEntityQueryWithUpdatesAtom } from "@dojoengine/react/effect";

const livePlayersAtom = createEntityQueryWithUpdatesAtom(
    runtime,
    query,
    clause
);
```

## Infinite Scroll

```tsx
import { createEntitiesInfiniteScrollAtom } from "@dojoengine/react/effect";

const infinitePlayersAtom = createEntitiesInfiniteScrollAtom(
    runtime,
    new ToriiQueryBuilder().addEntityModel("game-Player"),
    20 // page size
);

function InfinitePlayerList() {
    const [state, loadMore] = useAtom(infinitePlayersAtom);

    return Result.match(state, {
        onSuccess: ({ value }) => (
            <>
                <ul>
                    {value.items.map(p => (
                        <li key={p.entityId}>{p.models.game.Player.name}</li>
                    ))}
                </ul>
                {value.hasMore && (
                    <button onClick={loadMore}>Load More</button>
                )}
            </>
        ),
        onFailure: (error) => <div>Error: {error.message}</div>,
        onInitial: () => <div>Loading...</div>
    });
}
```

## Token Balance Atoms

```tsx
import {
    createTokenBalanceQueryAtom,
    createTokenBalanceUpdatesAtom
} from "@dojoengine/react/effect";

// One-time query
const balanceAtom = createTokenBalanceQueryAtom(runtime, {
    contractAddresses: ["0x..."],
    accountAddresses: [playerAddress]
});

// Polling updates
const liveBalanceAtom = createTokenBalanceUpdatesAtom(
    runtime,
    { contractAddresses: ["0x..."], accountAddresses: [playerAddress] },
    5000 // poll every 5 seconds
);
```

## Data Formatters

Transform data before rendering:

```tsx
const formatters = {
    models: {
        "game-Player": (player) => ({
            ...player,
            displayName: player.name || "Anonymous",
            displayScore: `${player.score.toLocaleString()} pts`
        })
    },
    fields: {
        "game-Player.score": (score) => Math.floor(score / 100)
    }
};

const playersAtom = createEntityQueryAtom(runtime, query, formatters);
```

## Custom Subscription Hooks

```tsx
import { createSubscriptionHook } from "@dojoengine/sdk/react";

const usePlayerSubscription = createSubscriptionHook({
    subscribeMethod: (sdk, params) => sdk.subscribeEntityQuery(params),
    processInitialData: (data) => data.items,
    processUpdateData: (update) => update
});

function PlayerTracker({ entityId }) {
    const { data, error, isLoading } = usePlayerSubscription({
        query: new ToriiQueryBuilder()
            .withClause(KeysClause(["game-Player"], [entityId]).build())
    });
}
```

## Zustand Selectors

Optimize re-renders with selectors:

```tsx
function PlayerScore({ entityId }) {
    const { useDojoStore } = useDojoSDK();

    // Only re-render when score changes
    const score = useDojoStore(
        state => state.entities[entityId]?.models?.game?.Player?.score,
        (a, b) => a === b // equality function
    );

    return <span>{score}</span>;
}
```

## useEntityId Hook

```tsx
import { useEntityId } from "@dojoengine/sdk/react";

function PlayerCard({ address, gameId }) {
    // Memoized entity ID computation
    const entityId = useEntityId(address, gameId);
    const player = useModel(entityId, "game-Player");
}
```

## Error Boundaries

```tsx
import { ErrorBoundary } from "react-error-boundary";

function GameErrorFallback({ error, resetErrorBoundary }) {
    return (
        <div>
            <p>Something went wrong: {error.message}</p>
            <button onClick={resetErrorBoundary}>Retry</button>
        </div>
    );
}

function App() {
    return (
        <ErrorBoundary FallbackComponent={GameErrorFallback}>
            <Game />
        </ErrorBoundary>
    );
}
```

## Common Pitfalls

1. **Missing provider**: Ensure DojoSdkProvider wraps all Dojo-using components
2. **Effect runtime**: Create runtime once at app startup, not in components
3. **Selector stability**: Use stable selector functions to prevent re-renders
4. **Cleanup**: Effect atoms handle cleanup, but manual subscriptions need cleanup
5. **Result.match**: Always handle all three cases (success, failure, initial)
