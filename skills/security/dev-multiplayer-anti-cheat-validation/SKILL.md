---
name: dev-multiplayer-anti-cheat-validation
description: Input validation and anti-cheat patterns for multiplayer servers. Use when implementing server-side validation.
category: multiplayer
---

# Anti-Cheat Validation

Server-side validation to prevent cheating in multiplayer games.

## When to Use

Use when:
- Implementing input validation on the server
- Adding shooting mechanics
- Preventing speed hacks or teleportation

## Input Validation Pattern

```typescript
function validateInput(input: PlayerInput, player: PlayerState): boolean {
  // Sanity checks - reject impossible inputs
  if (input.movementSpeed > 20) return false; // Speed hack
  if (input.jumpHeight > 10) return false;   // Super jump hack

  // Movement constraints
  const dx = input.targetX - player.x;
  const dz = input.targetZ - player.z;
  const distance = Math.sqrt(dx * dx + dz * dz);

  // Can't move more than X meters per tick
  if (distance > 2) return false;

  return true;
}

onMessage(client: Client, data: any) {
  const player = this.state.players.get(client.sessionId);
  if (!player) return;

  if (data.type === 'player_input') {
    // VALIDATE before processing
    if (validateInput(data.input, player)) {
      player.pendingInput = data.input;
    } else {
      // Log potential cheater
      console.warn(`Suspicious input from ${client.sessionId}`);
    }
  }
}
```

## Shooting Validation

```typescript
onMessage(client: Client, data: any) {
  if (data.type !== 'shoot') return;

  const shooter = this.state.players.get(client.sessionId);
  if (!shooter) return;

  // Validate shooter can shoot
  if (shooter.ink <= 0) return;
  if (Date.now() - shooter.lastShotTime < 100) return; // 100ms cooldown

  // Validate aim direction is reasonable
  const aim = data.aimDirection;
  const aimLength = Math.sqrt(aim.x ** 2 + aim.y ** 2 + aim.z ** 2);
  if (aimLength > 1.1 || aimLength < 0.9) return; // Must be normalized

  // Server creates paint projectile
  const projectile = {
    x: shooter.x,
    y: shooter.y + 1.5,
    z: shooter.z,
    dx: aim.x * 25,
    dy: aim.y * 25,
    dz: aim.z * 25,
    owner: client.sessionId,
    team: shooter.team,
  };

  this.projectiles.push(projectile);
  shooter.ink -= 1;
  shooter.lastShotTime = Date.now();
}
```

## Hit Detection with Lag Compensation

```typescript
// Server validates hits by rewinding time
function checkHit(shooter: PlayerState, targetId: string, aim: Vector3): boolean {
  const target = this.state.players.get(targetId);
  if (!target) return false;

  // Get target position at the time of shooting (lag compensation)
  const shotTime = Date.now();
  const latency = this.getClientLatency(shooter.sessionId);
  const rewindTime = shotTime - latency;

  // Find where target was at rewindTime
  const historicalPosition = this.getPositionHistory(targetId, rewindTime);
  if (!historicalPosition) return false;

  // Raycast from shooter to historical position
  return this.raycastHits(shooter, historicalPosition, aim);
}

// Store position history for lag compensation
private positionHistory: Map<string, Array<{time: number, x: number, y: number, z: number}>> = new Map();

update(dt: number) {
  const now = Date.now();

  for (const [sessionId, player] of this.state.players) {
    if (!this.positionHistory.has(sessionId)) {
      this.positionHistory.set(sessionId, []);
    }
    const history = this.positionHistory.get(sessionId)!;

    // Store position for lag compensation (keep last 500ms)
    history.push({ time: now, x: player.x, y: player.y, z: player.z });

    // Remove old entries
    while (history.length > 0 && history[0].time < now - 500) {
      history.shift();
    }
  }
}
```

## Anti-Cheat Best Practices

1. **Validate all inputs** - Reject impossible values
2. **Rate limit actions** - Prevent spam exploits
3. **Track position history** - Detect teleportation
4. **Checksum game state** - Detect tampering
5. **Log suspicious activity** - For analysis/banning

## Testing Checklist

- [ ] Server running successfully
- [ ] Feature works through network (not just locally)
- [ ] Server logs show player actions
- [ ] State updates propagate to all clients
- [ ] Inputs are validated server-side
- [ ] Impossible inputs are rejected
- [ ] No client-authoritative position updates

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| Trust client position | Validate all inputs |
| No rate limiting | Add cooldowns |
| No logging | Log suspicious activity |
| Client determines hit | Server validates hit |

## Reference

- [server-authoritative.md](./server-authoritative.md) - Architecture principles
- [prediction-shooting.md](./prediction-shooting.md) - Shooting prediction
