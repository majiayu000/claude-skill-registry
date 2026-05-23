---
name: dev-multiplayer-colyseus-state
description: Colyseus state schema definition, types, decorators, and serialization patterns. Use when defining room state.
category: multiplayer
---

# Colyseus State Schema

Define efficient binary-serializable state for Colyseus rooms using @colyseus/schema.

## When to Use

Use when:
- Defining room state schemas
- Creating player/entity state
- Setting up state collections
- Optimizing network bandwidth

## Schema Types

```typescript
import { Schema, type, MapSchema, ArraySchema } from '@colyseus/schema';

// Primitive types
@type('string')   // String
@type('number')   // Number (float)
@type('uint8')    // Unsigned 8-bit (0-255)
@type('uint16')   // Unsigned 16-bit (0-65535)
@type('uint32')   // Unsigned 32-bit
@type('int8')     // Signed 8-bit
@type('int16')    // Signed 16-bit
@type('int32')    // Signed 32-bit
@type('boolean')  // Boolean
@type('float32')  // 32-bit float

// Collection types
@type({ map: PlayerState })  // Map<string, PlayerState>
@type([PlayerState])         // Array<PlayerState>
```

## Basic Player State

```typescript
import { Schema, type } from '@colyseus/schema';

class PlayerState extends Schema {
  @type('string') clientId: string = '';
  @type('uint8') team: number = 0;  // 0 = orange, 1 = blue
  @type('float32') x: number = 0;
  @type('float32') y: number = 0;
  @type('float32') z: number = 0;
  @type('float32') rotation: number = 0;
  @type('uint16') score: number = 0;
  @type('boolean') isAlive: boolean = true;
}
```

## Room State Schema

```typescript
import { Schema, type, MapSchema } from '@colyseus/schema';

class GameRoomState extends Schema {
  @type({ map: PlayerState }) players = new MapSchema<PlayerState>();
  @type('uint8') phase: number = 0; // 0=waiting, 1=playing, 2=ended
  @type('uint16') orangeScore: number = 0;
  @type('uint16') blueScore: number = 0;
}
```

## Complex Nested Schema

```typescript
class Vector3Schema extends Schema {
  @type('float32') x: number = 0;
  @type('float32') y: number = 0;
  @type('float32') z: number = 0;
}

class PlayerState extends Schema {
  @type('string') clientId: string = '';
  @type(Vector3Schema) position: Vector3Schema = new Vector3Schema();
  @type(Vector3Schema) velocity: Vector3Schema = new Vector3Schema();
  @type('uint16') score: number = 0;
  @type('uint8') health: number = 100;
  @type('uint8') inkTank: number = 100;
  @type('boolean') isAlive: boolean = true;
}

class TeamScore extends Schema {
  @type('uint16') paintCoverage: number = 0;
  @type('uint16') kills: number = 0;
  @type('uint16') deaths: number = 0;
  @type('boolean') hasWon: boolean = false;
}

class MatchState extends Schema {
  @type('string') phase: string = 'waiting';
  @type('uint16') timeRemaining: number = 180;
  @type({ map: TeamScore }) teamScores = new MapSchema<TeamScore>();
  @type({ map: PlayerState }) players = new MapSchema<PlayerState>();
  @type([PaintSplat]) paintSplats = new ArraySchema<PaintSplat>();
}
```

## Using State in Room Handler

```typescript
export class GameRoom extends Room<GameRoomState> {
  onCreate(options: any) {
    this.setState(new GameRoomState());
  }

  onJoin(client: Client, options: any) {
    const player = new PlayerState();
    player.clientId = client.sessionId;
    player.x = 0; player.y = 0; player.z = 0;

    // Assign team
    const orangeCount = this.getOrangeCount();
    const blueCount = this.getBlueCount();
    player.team = orangeCount <= blueCount ? 0 : 1;

    this.state.players.set(client.sessionId, player);
  }

  onLeave(client: Client, consented: boolean) {
    this.state.players.delete(client.sessionId);
  }

  onMessage(client: Client, data: any) {
    const player = this.state.players.get(client.sessionId);
    if (!player) return;

    // Update player state
    if (data.type === 'move') {
      player.x = data.x;
      player.y = data.y;
      player.z = data.z;
    }
  }

  private getOrangeCount(): number {
    return Array.from(this.state.players.values())
      .filter(p => p.team === 0).length;
  }

  private getBlueCount(): number {
    return Array.from(this.state.players.values())
      .filter(p => p.team === 1).length;
  }
}
```

## Array Schema Operations

```typescript
class MyState extends Schema {
  @type([PlayerState]) players = new ArraySchema<PlayerState>();
}

// Add to array
this.state.players.push(new PlayerState());

// Remove from array
this.state.players.splice(index, 1);

// Iterate
this.state.players.forEach((player, index) => {
  console.log(player.clientId);
});
```

## Type Selection Guidelines

| Use Case | Type | Bytes | Range |
|----------|------|-------|-------|
| Player health 0-100 | uint8 | 1 | 0-255 |
| Score 0-65535 | uint16 | 2 | 0-65535 |
| Coordinates (-100 to 100) | float32 | 4 | ±3.4E38 |
| Team enum | uint8 | 1 | 0-255 |
| Player ID | string | variable | text |
| Boolean flag | boolean | 1 | true/false |

## Best Practices

1. **Use smallest type that fits** - Saves bandwidth
2. **Always add @type decorators** - Required for serialization
3. **Use collections efficiently** - MapSchema for dynamic keys, ArraySchema for ordered lists
4. **Initialize default values** - Prevents undefined issues
5. **Keep state flat** - Deep nesting increases complexity

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| Missing @type decorator | Always add `@type('string')` |
| Using `number` for small ranges | Use `uint8`, `uint16` for savings |
| Deep nesting (4+ levels) | Keep state shallow |
| Not initializing defaults | Set default: `x: number = 0` |

## Reference

- [Schema Documentation](https://docs.colyseus.io/state-synchronization/)
- [Schema API](https://docs.colyseus.io/state-synchronization/schema-api/)

---

## Schema Definition Best Practices (Updated 2026-01-28)

From arch-003 retrospective - proven patterns for @colyseus/schema.

### Complete Player Schema Pattern

```typescript
import { Schema, type } from '@colyseus/schema';

/**
 * Player state schema for server-authoritative multiplayer
 *
 * Type Selection Guidelines:
 * - uint8: 0-255 (health, armor, small counters)
 * - uint16: 0-65535 (scores, larger counters)
 * - float32: Coordinates, rotation (precision needed)
 * - string: Variable text (sessionId, weapon names)
 * - boolean: Flags (isAlive, connected)
 */
export class PlayerState extends Schema {
  // Position (float32 for precision)
  @type('float32') x: number = 0;
  @type('float32') y: number = 0;
  @type('float32') z: number = 0;

  // Rotation (degrees or radians)
  @type('float32') rotation: number = 0;

  // Combat stats (uint8 sufficient for 0-100 ranges)
  @type('uint8') health: number = 100;
  @type('uint8') armor: number = 0;

  // Weapon (string for flexibility - consider enum for type safety)
  @type('string') weapon: string = 'blaster';

  // Score tracking
  @type('uint8') kills: number = 0;
  @type('boolean') isAlive: boolean = true;
}
```

### Complete Room State Pattern

```typescript
import { Schema, type, MapSchema } from '@colyseus/schema';
import { PlayerState } from './PlayerState';

export class ArenaState extends Schema {
  // Players map - keyed by sessionId
  @type({ map: PlayerState }) players = new MapSchema<PlayerState>();

  // Room settings
  @type('string') mapSeed: string = '';

  // Match state
  @type('uint16') playersAlive: number = 0;
  @type('string') phase: string = 'lobby';  // lobby, playing, ended
}
```

### Schema Type Selection Guide

| Data | Type | Bytes | Range | Example |
|------|------|-------|-------|---------|
| Health 0-100 | uint8 | 1 | 0-255 | `@type('uint8') health: number = 100` |
| Armor 0-100 | uint8 | 1 | 0-255 | `@type('uint8') armor: number = 0` |
| Kills 0-63 | uint8 | 1 | 0-255 | `@type('uint8') kills: number = 0` |
| Score 0-65535 | uint16 | 2 | 0-65535 | `@type('uint16') score: number = 0` |
| Position X/Y/Z | float32 | 4 | ±3.4E38 | `@type('float32') x: number = 0` |
| Rotation | float32 | 4 | ±3.4E38 | `@type('float32') rotation: number = 0` |
| Session ID | string | variable | text | `@type('string') sessionId: string = ''` |
| Weapon name | string | variable | text | `@type('string') weapon: string = ''` |
| Alive status | boolean | 1 | true/false | `@type('boolean') isAlive: boolean = true` |
| Player map | MapSchema | 4+ bytes | dynamic | `@type({ map: PlayerState })` |

### Common Schema Mistakes

| ❌ Wrong | ✅ Right | Why |
|----------|----------|-----|
| `@type()` missing | `@type('uint8')` | Required for serialization |
| `@type('number')` for health | `@type('uint8')` | Saves 3 bytes per player |
| `health` without default | `health: number = 100` | Prevents undefined |
| Using `Array` for players | `MapSchema<Player>` | Efficient lookup by ID |

**Sources:**
- https://docs.colyseus.io/colyseus/server/schema/
- **Learned from arch-003 retrospective (2026-01-28)**
