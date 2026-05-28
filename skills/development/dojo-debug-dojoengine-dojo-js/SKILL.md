---
name: dojo-debug
description: |
  Use when debugging and troubleshooting dojo.js applications.
  Triggers: dojo error, torii connection, entity not found, type mismatch, debug dojo,
  troubleshoot, subscription error, sync issues
---

# Dojo.js Debugging & Troubleshooting

## When to Use

Use this skill when:
- Debugging connection issues
- Troubleshooting entity sync problems
- Fixing type mismatches
- Diagnosing subscription errors

## Connection Issues

### Torii Not Responding

```bash
# Check if Torii is running
curl http://localhost:8080/health

# Check Torii logs
katana & torii --world 0x... --rpc http://localhost:5050
```

**Common causes:**
- Torii not started
- Wrong `toriiUrl` in config
- CORS blocking requests
- World address mismatch

### CORS Errors

```
Access to fetch blocked by CORS policy
```

**Solution:** Start Torii with CORS enabled:
```bash
torii --world 0x... --allowed-origins "*"
```

### WebSocket Connection Failed

```typescript
// Check if WebSocket is supported
if (typeof WebSocket === 'undefined') {
    console.error("WebSocket not available");
}

// Try gRPC instead
import { initGrpc } from "@dojoengine/sdk";
const grpcClient = await initGrpc({ toriiUrl, worldAddress });
```

## Entity Issues

### Entity Not Found

```typescript
// Debug: Check if entity exists
const { useDojoStore } = useDojoSDK();
const allEntities = useDojoStore.getState().entities;
console.log("All entities:", Object.keys(allEntities));

// Verify entity ID format
import { getEntityIdFromKeys } from "@dojoengine/utils";
const entityId = getEntityIdFromKeys([BigInt(key1), BigInt(key2)]);
console.log("Expected entityId:", entityId);
```

**Common causes:**
- Wrong entity key(s)
- Entity not yet indexed by Torii
- Query filter too restrictive

### Entity Not Updating

```typescript
// Check subscription is active
const [data, subscription] = await sdk.subscribeEntityQuery({...});
console.log("Subscription active:", subscription);

// Verify callback is being called
callback: ({ data, error }) => {
    console.log("Callback triggered:", { data, error });
}
```

**Common causes:**
- Subscription filter doesn't match entity
- Callback throwing error
- Store not being updated

## Type Issues

### Schema Type Mismatch

```
Type 'X' is not assignable to type 'Y'
```

**Solution:** Regenerate types from ABI:
```bash
npx @dojoengine/core compile-abi path/to/manifest.json
```

### Model Name Format

```typescript
// Wrong
useModel(entityId, "Player");       // Missing namespace
useModel(entityId, "game_Player");  // Wrong separator

// Correct
useModel(entityId, "game-Player");  // namespace-ModelName
```

## Subscription Errors

### Subscription Callback Error

```typescript
// Wrap callback in try-catch
callback: ({ data, error }) => {
    try {
        if (error) {
            console.error("Subscription error:", error);
            return;
        }
        processData(data);
    } catch (e) {
        console.error("Callback error:", e);
    }
}
```

### Memory Leaks

```typescript
// Always cleanup subscriptions
useEffect(() => {
    let subscription;

    async function setup() {
        [, subscription] = await sdk.subscribeEntityQuery({...});
    }
    setup();

    return () => {
        if (subscription) {
            subscription.cancel();
        }
    };
}, []);
```

## Transaction Errors

### Insufficient Funds

```
Transaction reverted: insufficient balance
```

**Solution:** Fund the account:
```typescript
// Check balance
const balance = await provider.provider.getBalance(account.address);
console.log("Balance:", balance);
```

### Nonce Mismatch

```
Invalid transaction nonce
```

**Solution:** Wait for pending transactions:
```typescript
await account.waitForTransaction(tx.transaction_hash);
```

### Contract Not Found

```
Contract not found in manifest
```

**Solution:** Verify contract name and namespace:
```typescript
console.log("Manifest contracts:", manifest.contracts.map(c => c.tag));
```

## Performance Issues

### Slow Queries

```typescript
// Use pagination
const query = new ToriiQueryBuilder()
    .withLimit(50)  // Smaller batches
    .addEntityModel("game-Player")  // Specific models only
    .build();

// Consider gRPC for better performance
import { initGrpc } from "@dojoengine/sdk";
```

### Too Many Re-renders

```typescript
// Use selectors to minimize updates
const score = useDojoStore(
    state => state.entities[entityId]?.models?.game?.Player?.score,
    (a, b) => a === b  // Custom equality
);

// Use memo for expensive computations
const sortedPlayers = useMemo(() =>
    Object.values(entities).sort((a, b) => b.score - a.score),
    [entities]
);
```

## Debugging Tools

### Log All Store Changes

```typescript
useDojoStore.subscribe((state, prevState) => {
    console.log("Store changed:", {
        added: Object.keys(state.entities).filter(k => !prevState.entities[k]),
        removed: Object.keys(prevState.entities).filter(k => !state.entities[k])
    });
});
```

### Query Torii Directly

```bash
# Check indexed entities
curl "http://localhost:8080/entities?model=game-Player&limit=10"

# Check events
curl "http://localhost:8080/events?limit=10"
```

### Enable SDK Logging

```typescript
const provider = new DojoProvider(manifest, rpcUrl, "debug");
```

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `DojoProvider can only be used once` | Duplicate provider | Remove duplicate |
| `Either client or grpcClient must be provided` | SDK init failed | Check init options |
| `Contract did not return expected uuid` | Wrong world address | Verify world address |
| `Failed to fetch uuid` | RPC connection failed | Check RPC URL |

## Quick Diagnostics

```typescript
// Add to your app for debugging
function DebugPanel() {
    const { sdk, config, useDojoStore } = useDojoSDK();
    const entityCount = useDojoStore(s => Object.keys(s.entities).length);

    return (
        <div style={{ position: 'fixed', bottom: 0, right: 0, background: '#000', color: '#0f0', padding: 10 }}>
            <div>Torii: {config.toriiUrl}</div>
            <div>World: {config.manifest?.world?.address?.slice(0, 10)}...</div>
            <div>Entities: {entityCount}</div>
        </div>
    );
}
```
