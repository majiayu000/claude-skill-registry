---
name: dev-multiplayer-prediction-shooting
description: Shooting prediction with optimistic decals and server rollback. Use when implementing shooting mechanics.
category: multiplayer
---

# Shooting Prediction with Rollback

Shooting mechanics with immediate feedback and server validation.

## When to Use

Use when implementing shooting in multiplayer games:
- FPS weapons
- Paint/projectile systems
- Hit detection
- Ammo management

## Message Structure

```typescript
// Client sends aim direction + fire command
interface PaintFireMessage {
  type: 'paint_fire';
  direction: { x: number; y: number; z: number }; // Normalized aim vector
  sequence: number; // For rollback reconciliation
}

// Server responds with confirmation/rejection
interface PaintResultMessage {
  type: 'paint_result';
  sequence: number; // Matches client's fire sequence
  confirmed: boolean;
  reason?: string; // 'no_ink' | 'cooldown' | 'invalid_aim'
}
```

## Client Implementation

```typescript
import { useRef, useEffect } from 'react';
import { useNetworkManager } from '../../services/NetworkManager';

interface PendingShot {
  id: string;
  direction: Vector3;
  timestamp: number;
  sequence: number;
}

export function PaintGun() {
  const networkManager = useNetworkManager();
  const pendingShotsRef = useRef<PendingShot[]>([]);

  // Optimistic shooting
  function shoot(direction: Vector3) {
    const shotId = `${Date.now()}-${Math.random()}`;
    const sequence = ++shotSequenceRef.current;

    // 1. Spawn paint immediately (optimistic)
    spawnOptimisticDecal(shotId, direction);

    // 2. Store for rollback
    pendingShotsRef.current.push({
      id: shotId,
      direction,
      timestamp: Date.now(),
      sequence,
    });

    // 3. Send to server
    networkManager.send({
      type: 'paint_fire',
      direction,
      sequence,
    });
  }

  // Listen for server confirmation/rollback
  useEffect(() => {
    const unsubscribe = networkManager.onMessage('paint_result', (result) => {
      handlePaintResult(result);
    });
    return unsubscribe;
  }, []);

  function handlePaintResult(result: PaintResultMessage) {
    const pendingIndex = pendingShotsRef.current.findIndex(
      s => s.sequence === result.sequence
    );

    if (pendingIndex === -1) return;

    const pending = pendingShotsRef.current[pendingIndex];

    if (result.confirmed) {
      // Server confirmed - mark optimistic decal as permanent
      confirmDecal(pending.id);
    } else {
      // Server rejected - rollback (remove optimistic decal)
      rollbackDecal(pending.id);
    }

    pendingShotsRef.current.splice(pendingIndex, 1);
  }

  function spawnOptimisticDecal(id: string, direction: Vector3) {
    // Create temporary decal with "optimistic" flag
    decalManager.spawn({
      id,
      position: calculateImpact(direction),
      team: localTeam,
      optimistic: true, // Mark for potential rollback
    });
  }

  function rollbackDecal(id: string) {
    decalManager.remove(id);
  }

  function confirmDecal(id: string) {
    decalManager.markPermanent(id);
  }
}
```

## Optimistic Decal Manager

```typescript
interface PendingDecal {
  id: string;
  sequence: number;
  optimistic: boolean;
  confirmed: boolean;
  createdAt: number;
}

export function PaintDecalManager() {
  const pendingDecalsRef = useRef<Map<string, PendingDecal>>(new Map());

  // Spawn optimistic decal (immediate feedback)
  function spawnOptimisticDecal(sequence: number, position: Vector3) {
    const id = `decal-${sequence}`;
    pendingDecalsRef.current.set(id, {
      id,
      sequence,
      optimistic: true,
      confirmed: false,
      createdAt: Date.now(),
    });

    // Create visual immediately (semi-transparent = optimistic)
    createDecalVisual(id, position, { opacity: 0.7 });
  }

  // Confirm decal (server accepted)
  function confirmDecal(sequence: number) {
    const decal = pendingDecalsRef.current.get(`decal-${sequence}`);
    if (decal) {
      decal.confirmed = true;
      decal.optimistic = false;
      updateDecalVisual(decal.id, { opacity: 1.0 }); // Full opacity = confirmed
    }
  }

  // Rollback decal (server rejected)
  function rollbackDecal(sequence: number) {
    const id = `decal-${sequence}`;
    removeDecalVisual(id);
    pendingDecalsRef.current.delete(id);
  }

  // Cleanup old optimistic decals (in case server never responds)
  useFrame(() => {
    const now = Date.now();
    for (const [id, decal] of pendingDecalsRef.current) {
      if (decal.optimistic && now - decal.createdAt > 2000) {
        rollbackDecal(decal.sequence);
      }
    }
  });
}
```

## Server Validation

```typescript
// server/systems/ProjectileSystem.ts
export class ProjectileSystem {
  private projectiles: PaintProjectile[] = [];

  processFireMessage(client: Client, data: FireMessage) {
    const player = this.room.state.players.get(client.sessionId);
    if (!player) return;

    // 1. Validate ammo (server-enforced)
    if (player.ink <= 0) {
      this.sendReject(client, data.sequence, 'no_ink');
      return;
    }

    // 2. Validate fire rate (server-enforced, 600 RPM = 100ms cooldown)
    const now = Date.now();
    if (now - player.lastShotTime < 100) {
      this.sendReject(client, data.sequence, 'cooldown');
      return;
    }

    // 3. Validate aim direction (prevent packet spam exploits)
    const aimLength = Math.sqrt(
      data.direction.x ** 2 +
      data.direction.y ** 2 +
      data.direction.z ** 2
    );
    if (aimLength > 1.1 || aimLength < 0.9) {
      this.sendReject(client, data.sequence, 'invalid_aim');
      return;
    }

    // Create projectile SERVER-SIDE
    const projectile: PaintProjectile = {
      id: `proj-${client.sessionId}-${data.sequence}`,
      x: player.x,
      y: player.y + 1.5,
      z: player.z,
      dx: data.direction.x * 25, // 25 m/s
      dy: data.direction.y * 25,
      dz: data.direction.z * 25,
      owner: client.sessionId,
      team: player.team,
      sequence: data.sequence,
    };

    this.projectiles.push(projectile);
    player.ink -= 1;
    player.lastShotTime = now;

    // Notify client that shot was accepted
    this.sendConfirm(client, data.sequence);
  }

  update(dt: number) {
    const deltaTime = dt / 1000;

    for (let i = this.projectiles.length - 1; i >= 0; i--) {
      const proj = this.projectiles[i];

      // Move projectile
      proj.x += proj.dx * deltaTime;
      proj.y += proj.dy * deltaTime;
      proj.z += proj.dz * deltaTime;

      // Apply gravity
      proj.dy -= 9.8 * deltaTime;

      // Check collision
      if (this.checkCollision(proj)) {
        this.spawnPaintDecal(proj);
        this.broadcastPaintEvent(proj);
        this.projectiles.splice(i, 1);
      } else if (proj.y < 0) {
        // Below ground
        this.projectiles.splice(i, 1);
      }
    }
  }

  sendConfirm(client: Client, sequence: number) {
    client.send({
      type: 'paint_result',
      sequence,
      confirmed: true,
    });
  }

  sendReject(client: Client, sequence: number, reason: string) {
    client.send({
      type: 'paint_result',
      sequence,
      confirmed: false,
      reason,
    });
  }
}
```

## Grid-Based Paint Coverage

```typescript
// 5x5 unit grid cells for performance
interface PaintGrid {
  [cellKey: string]: {
    orange: number; // Orange paint count
    blue: number;   // Blue paint count
  };
}

function getCellKey(x: number, z: number): string {
  const cellX = Math.floor(x / 5);
  const cellZ = Math.floor(z / 5);
  return `${cellX},${cellZ}`;
}

function addPaintToGrid(grid: PaintGrid, x: number, z: number, team: 'orange' | 'blue') {
  const key = getCellKey(x, z);
  if (!grid[key]) {
    grid[key] = { orange: 0, blue: 0 };
  }
  grid[key][team]++;
}

function getPaintCoverage(grid: PaintGrid, team: 'orange' | 'blue'): number {
  return Object.values(grid).reduce(
    (sum, cell) => sum + cell[team],
    0
  );
}
```

## Validation Checklist

```typescript
function validateFireMessage(player: PlayerState, data: PaintFireMessage): string | null {
  // Validate ammo
  if (player.ink <= 0) return 'no_ink';

  // Validate fire rate
  const now = Date.now();
  if (now - player.lastShotTime < 100) return 'cooldown';

  // Validate aim direction
  const aimLength = Math.sqrt(
    data.direction.x ** 2 +
    data.direction.y ** 2 +
    data.direction.z ** 2
  );
  if (aimLength > 1.1 || aimLength < 0.9) return 'invalid_aim';

  return null; // Valid
}
```

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| No optimistic feedback | Spawn decal immediately |
| Server accepts all shots | Validate ammo, cooldown, aim |
| No rollback mechanism | Remove rejected effects |
| Cleanup never happens | Timeout old optimistic decals |
| Trust client hit detection | Server-authoritative hit validation |

## Reference

- [prediction-basics.md](./prediction-basics.md) - Core prediction concepts
- [prediction-movement.md](./prediction-movement.md) - Movement prediction
