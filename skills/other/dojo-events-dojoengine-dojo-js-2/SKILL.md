---
name: dojo-events
description: |
  Use when subscribing to game events and tracking tokens in dojo.js.
  Triggers: subscribe events, game events, token balance, event query, achievements,
  event subscription, onTokenBalanceUpdated, activity tracking
---

# Dojo.js Events & Token Tracking

## When to Use

Use this skill when:
- Subscribing to game events
- Tracking token balances
- Monitoring token transfers
- Tracking achievements and activities

## Event Subscriptions

### Subscribe to Event Messages

```tsx
import { ToriiQueryBuilder } from "@dojoengine/sdk";
import { useDojoSDK } from "@dojoengine/sdk/react";

const { sdk } = useDojoSDK();

const [initialEvents, subscription] = await sdk.subscribeEventQuery({
    query: new ToriiQueryBuilder<typeof schema>()
        .addEntityModel("game-GameEvent")
        .withLimit(100),
    callback: ({ data, error }) => {
        if (error) {
            console.error("Event error:", error);
            return;
        }
        console.log("New event:", data);
    }
});

// Process initial events
initialEvents.items.forEach(event => {
    console.log(event.models.game.GameEvent);
});

// Cleanup
subscription.cancel();
```

### Get Event Messages (One-time)

```tsx
const events = await sdk.getEventMessages({
    query: new ToriiQueryBuilder<typeof schema>()
        .addEntityModel("game-PlayerAction")
        .addOrderBy("game-PlayerAction.timestamp", "Desc")
        .withLimit(50)
});
```

## Token Balance Tracking

### Subscribe to Token Balances

```tsx
const [balances, subscription] = await sdk.subscribeTokenBalance({
    // Contract addresses must be full hex strings with 0x prefix
    contractAddresses: ["0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7"],
    accountAddresses: [playerAddress],
    callback: (balance) => {
        console.log("Balance updated:", balance.balance);
    }
});

// Initial balances
balances.items.forEach(b => {
    console.log(`Token: ${b.token_id}, Balance: ${b.balance}`);
});
```

### Get Token Balances

```tsx
const balances = await sdk.getTokenBalances({
    contractAddresses: ["0x..."],
    accountAddresses: [playerAddress],
    pagination: { limit: 100 }
});
```

### Track Balance Updates Only

```tsx
const subscription = await sdk.onTokenBalanceUpdated({
    contractAddresses: ["0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7"],
    accountAddresses: [playerAddress],
    // Empty array for all tokens (ERC20); for ERC721 use specific IDs: ["0x1", "0x2"]
    tokenIds: [],
    callback: (balance) => {
        updateUI(balance);
    }
});
```

## Token Transfer Tracking

```tsx
const [transfers, subscription] = await sdk.subscribeTokenTransfer({
    contractAddresses: ["0x..."],
    accountAddresses: [playerAddress],
    callback: (transfer) => {
        console.log(`Transfer: ${transfer.from} -> ${transfer.to}`);
    }
});
```

## Token Queries

```tsx
// Get tokens
const tokens = await sdk.getTokens({
    contractAddresses: ["0x..."],
    pagination: { limit: 100 }
});

// Get token contracts
const contracts = await sdk.getTokenContracts({
    contractTypes: ["ERC20", "ERC721"]
});
```

## Achievement Tracking

```tsx
// Get achievements
const achievements = await sdk.getAchievements({
    worldAddresses: [worldAddress],
    namespaces: ["game"]
});

// Get player achievements
const playerAchievements = await sdk.getPlayerAchievements({
    playerAddresses: [playerAddress]
});

// Subscribe to achievement progress
const subscription = await sdk.onAchievementProgressionUpdated({
    worldAddresses: [worldAddress],
    playerAddresses: [playerAddress],
    callback: (progression) => {
        console.log("Achievement progress:", progression);
    }
});
```

## Activity Tracking

```tsx
// Get activities
const activities = await sdk.getActivities({
    world_addresses: [worldAddress],
    namespaces: ["game"],
    caller_addresses: [playerAddress]
});

// Subscribe to activities
const subscription = await sdk.onActivityUpdated(
    [worldAddress],
    ["game"],
    [playerAddress],
    (activity) => {
        console.log("New activity:", activity);
    }
);
```

## Aggregations

```tsx
// Get aggregated data
const aggregations = await sdk.getAggregations({
    aggregator_ids: ["total_players", "total_games"],
    pagination: { limit: 10 }
});

// Subscribe to aggregation updates
const subscription = await sdk.onAggregationUpdated(
    ["total_players"],
    null,
    (aggregation) => {
        console.log("Aggregation updated:", aggregation);
    }
);
```

## Update Subscriptions

```tsx
// Update token balance subscription
await sdk.updateTokenBalanceSubscription({
    subscription,
    contractAddresses: newContracts,
    accountAddresses: newAccounts,
    tokenIds: []
});

// Update entity subscription
await sdk.updateEntitySubscription(
    subscription,
    newClause
);
```

## React Effect Atoms

For complex async state:

```tsx
import { createEventQueryAtom, createEventUpdatesAtom } from "@dojoengine/react/effect";

// One-time event query
const eventsAtom = createEventQueryAtom(runtime, query);

// Live event updates
const updatesAtom = createEventUpdatesAtom(runtime, clauses);

// Combined query + updates
const liveEventsAtom = createEventQueryWithUpdatesAtom(runtime, query, clauses);
```

## Common Pitfalls

1. **Subscription cleanup**: Always cancel subscriptions when component unmounts
2. **Contract addresses**: Must be padded hex strings with 0x prefix
3. **Token IDs**: Format depends on token type (ERC20 vs ERC721)
4. **Rate limiting**: Avoid creating too many subscriptions
5. **Callback errors**: Wrap callbacks in try-catch to prevent unhandled errors
