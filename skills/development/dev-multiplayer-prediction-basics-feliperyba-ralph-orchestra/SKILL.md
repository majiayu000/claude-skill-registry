---
name: dev-multiplayer-prediction-basics
description: Client-side prediction and server reconciliation core concepts. Use when implementing responsive multiplayer controls.
category: multiplayer
---

# Client-Side Prediction Basics

Client prediction makes multiplayer feel responsive. Server reconciliation keeps it honest.

## When to Use

Use for EVERY server-authoritative gameplay feature that needs responsive feel:
- Movement (WASD, jump, sprint)
- Shooting (aim, fire, ammo)
- Interactions (vault, mantle, crouch)

## Architecture Flow

```
INPUT
  │
  ├───► LOCAL PREDICTION (immediate visual feedback)
  │      │
  │      └───► Display updates instantly (feels responsive)
  │
  └───► SEND TO SERVER (validation)
         │
         │    NETWORK LATENCY (~100ms)
         │
         ▼
      SERVER PROCESSES
         │
         └───► SERVER STATE (authoritative)
                │
                │    NETWORK LATENCY
                │
                ▼
           CLIENT RECONCILES
                │
                ├───► Discard confirmed inputs
                ├───► Re-apply pending inputs
                └───► Smooth correction

Result: Responsive feel + cheat prevention
```

## Key Concepts

### Local Prediction
- Apply input immediately on client
- Show result to player instantly
- No perceived lag

### Server Validation
- Send input to server
- Server processes authoritatively
- Validates rules, prevents cheating

### Reconciliation
- Server sends authoritative state back
- Client removes processed inputs from pending
- Re-applies remaining pending inputs
- Smoothly interpolates to reconciled position

## Input Message Pattern

```typescript
interface InputMessage {
  type: 'player_input';
  input: {
    forward: boolean;
    backward: boolean;
    left: boolean;
    right: boolean;
    jump: boolean;
  };
  sequence: number;  // Incrementing counter for matching
}
```

### Sequence Numbers

Critical for reconciliation:
- Client increments counter for each input
- Server echoes sequence in state updates
- Client uses sequence to match server responses

## Reconciliation Flow

```typescript
// Server sends authoritative state
interface ServerState {
  position: { x: number; y: number; z: number };
  lastProcessedSequence: number;  // Key for reconciliation
}

// Client reconciles
function reconcile(serverState: ServerState) {
  // 1. Remove inputs server has processed
  pendingInputs = pendingInputs.filter(
    p => p.sequence > serverState.lastProcessedSequence
  );

  // 2. Start from server position (authoritative)
  let position = { ...serverState.position };

  // 3. Re-apply all pending inputs
  for (const input of pendingInputs) {
    position = applyInput(position, input.input, 0.016);
  }

  // 4. Smoothly interpolate display
  displayPosition = lerp(displayPosition, position, 0.2);
}
```

## Config Synchronization

**CRITICAL**: Config values MUST match exactly between client and server.

### Wrong Way

```typescript
// ❌ Config defined separately
// Client: const MOVEMENT_SPEED = 10;
// Server: const MOVEMENT_SPEED = 10;  // Can drift!
```

### Right Way - Shared Module

```typescript
// ✅ shared/config/MovementConfig.ts
export const MOVEMENT_CONFIG = {
  walkSpeed: 10,
  sprintSpeed: 16,
  jumpForce: 8,
  gravity: 20,
} as const;

// Both client and server import from same file
```

### Right Way - Server-Driven

```typescript
// ✅ Server sends config on connect
onJoin(client: Client) {
  client.send({
    type: 'config_sync',
    movement: MOVEMENT_CONFIG,
  });
}
```

## Testing Checklist

- [ ] Input feels immediate (no perceived lag)
- [ ] Server rejection causes rollback
- [ ] Rollback is smooth (not jarring)
- [ ] Reconciliation completes within 200ms
- [ ] No rubber-banding under normal latency
- [ ] High latency (200ms+) still playable

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| No prediction, send input only | Predict locally, then send |
| No reconciliation, just snap | Smooth interpolation |
| Apply server state directly | Re-apply pending inputs first |
| Separate client/server config | Shared config module |
| Hardcoded values everywhere | Single source of truth |

## Performance Notes

- Limit pending inputs to ~100 entries
- Clean up old inputs (> 1 second)
- Use object pooling for input objects
- Batch reconciliation updates (not every frame)

## Reference

- [Valve Latency Compensation](https://developer.valvesoftware.com/wiki/Latency_Compensating_Methods)
- [Gaffer On Games - Networking](https://gafferongames.com/post/what_every_programmer_needs_to_know_about_game_networking/)
