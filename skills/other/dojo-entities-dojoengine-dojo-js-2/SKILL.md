---
name: dojo-entities
description: |
  Use when querying, fetching, or subscribing to game entities in dojo.js.
  Triggers: entity query, fetch entities, useModel, useEntityQuery, ToriiQueryBuilder,
  subscribe entities, getEntities, entity subscription, model data
---

# Dojo.js Entity Queries & Subscriptions

## When to Use

Use this skill when:
- Fetching game entities from Torii
- Building queries with filters and pagination
- Subscribing to real-time entity updates
- Accessing model data in React components

## ToriiQueryBuilder

Build type-safe queries for entities:

```typescript
import { ToriiQueryBuilder, KeysClause, MemberClause } from "@dojoengine/sdk";

// Basic query with limit
const query = new ToriiQueryBuilder<typeof schema>()
    .withLimit(100)
    .build();

// Query with clause filter
const query = new ToriiQueryBuilder<typeof schema>()
    .withClause(
        KeysClause(["game-Player"], [playerAddress], "VariableLen").build()
    )
    .withLimit(50)
    .build();

// Query with ordering
const query = new ToriiQueryBuilder<typeof schema>()
    .addOrderBy("game-Player.score", "Desc")
    .withLimit(10)
    .build();

// Query specific models
const query = new ToriiQueryBuilder<typeof schema>()
    .addEntityModel("game-Player")
    .addEntityModel("game-Position")
    .withLimit(100)
    .build();
```

## Query Methods

### Pagination

```typescript
const query = new ToriiQueryBuilder<typeof schema>()
    .withLimit(50)                    // Max results
    .withCursor(nextCursor)           // Pagination cursor
    .withDirection("Forward")         // "Forward" | "Backward"
    .build();
```

### Clause Types

```typescript
// Keys clause - filter by entity keys
KeysClause(["namespace-Model"], [key1, key2], "VariableLen")

// Member clause - filter by field value
MemberClause("namespace-Model", "fieldName", "Eq", value)

// Composite clause - combine clauses
CompositeClause("And", [clause1, clause2])
```

## Fetching Entities

```typescript
const { sdk } = useDojoSDK();

// One-time fetch
const result = await sdk.getEntities({
    query: new ToriiQueryBuilder<typeof schema>()
        .withClause(clause)
        .withLimit(100)
});

// Access results
result.items.forEach(entity => {
    console.log(entity.entityId, entity.models);
});

// Pagination
if (result.next_cursor) {
    const nextPage = await sdk.getEntities({
        query: new ToriiQueryBuilder<typeof schema>()
            .withCursor(result.next_cursor)
            .withLimit(100)
    });
}
```

## Subscribing to Entities

```typescript
const { sdk } = useDojoSDK();

const [initialData, subscription] = await sdk.subscribeEntityQuery({
    query: new ToriiQueryBuilder<typeof schema>()
        .withClause(clause)
        .withLimit(100),
    callback: ({ data, error }) => {
        if (error) {
            console.error("Subscription error:", error);
            return;
        }
        // Handle real-time updates
        console.log("Entity updated:", data);
    }
});

// Clean up subscription
subscription.cancel();
```

## React Hooks

### useModel - Single Entity Model

```tsx
import { useModel } from "@dojoengine/sdk/react";

function PlayerStats({ entityId }) {
    // Format: "namespace-ModelName"
    const player = useModel(entityId, "game-Player");

    if (!player) return <div>Loading...</div>;

    return <div>Score: {player.score}</div>;
}
```

### useModels - All Entities with Model

```tsx
import { useModels } from "@dojoengine/sdk/react";

function Leaderboard() {
    const players = useModels("game-Player");

    return (
        <ul>
            {Object.entries(players).map(([entityId, player]) => (
                <li key={entityId}>{player?.name}: {player?.score}</li>
            ))}
        </ul>
    );
}
```

### useHistoricalModel - Time-series Data

```tsx
import { useHistoricalModel } from "@dojoengine/sdk/react";

function PlayerHistory({ entityId }) {
    const history = useHistoricalModel(entityId, "game-Player");

    return (
        <ul>
            {history.map((snapshot, i) => (
                <li key={i}>Score: {snapshot.models.game.Player.score}</li>
            ))}
        </ul>
    );
}
```

## Entity ID Generation

```typescript
import { getEntityIdFromKeys } from "@dojoengine/utils";

// Generate entity ID from keys
const entityId = getEntityIdFromKeys([
    BigInt(playerAddress),
    BigInt(gameId)
]);
```

## Common Pitfalls

1. **Model name format**: Use `"namespace-ModelName"` format (hyphen-separated)
2. **Entity ID type**: Must be string, use `entityId.toString()` if needed
3. **Subscription cleanup**: Always cancel subscriptions on component unmount
4. **Query limits**: Default limit is 100, set explicit limits for large datasets
