---
name: starwards-colyseus
description: Colyseus multiplayer patterns for Starwards - @gameField decorators, state sync, JSON Pointer commands, room architecture, and avoiding common Colyseus pitfalls; state is source of truth, server authoritative
version: 2025-11-04
related_skills:
  - starwards-tdd (test state sync with harnesses)
  - starwards-debugging (debug sync issues)
  - starwards-verification (verify multiplayer scenarios)
  - using-superpowers (announce skill usage)
---

# Colyseus Multiplayer Patterns for Starwards

## Overview

Starwards uses Colyseus v0.15 for real-time multiplayer state synchronization. Understanding decorators, rooms, and state sync prevents bugs.

**Core principle:** State is the source of truth. Commands modify state. Clients receive automatic updates.

## Architecture

```
Client (Browser)
  ↓ WebSocket connection
Room (Server)
  ↓ owns
State (Schema)
  ↓ syncs to
Client State (Mirror)
```

**Flow:**
1. Client sends command → Room
2. Room modifies State
3. Colyseus patches → Client
4. Client state updates automatically
5. UI reacts to state changes

## The @gameField Decorator

**Purpose:** Marks properties for automatic Colyseus synchronization

**Location:** `modules/core/src/game-field.ts`

**Usage:**

```typescript
import { gameField } from '../game-field';

class Shield extends SystemState {
  // Primitive types
  @gameField('float32') strength = 1000;
  @gameField('float32') power = 1.0;
  @gameField('boolean') broken = false;

  // Nested Schema
  @gameField(ShieldDesign) design = new ShieldDesign();

  // Arrays
  @gameField([Emitter]) emitters = new ArraySchema<Emitter>();

  // Maps
  @gameField({ map: Target }) targets = new MapSchema<Target>();
}
```

**Types:**
- `'float32'` - 32-bit float (precision loss vs 64-bit number!)
- `'float64'` - 64-bit float
- `'int8'`, `'int16'`, `'int32'` - Signed integers
- `'uint8'`, `'uint16'`, `'uint32'` - Unsigned integers
- `'boolean'` - Boolean
- `'string'` - String
- `SchemaClass` - Nested Schema
- `[SchemaClass]` - Array of Schema
- `{map: SchemaClass}` - Map of Schema

## Critical @gameField Rules

### Rule 1: @gameField Must Be Last Decorator

```typescript
// CORRECT order
@range([0, 1])           // 1st
@tweakable('number')     // 2nd
@gameField('float32')    // 3rd - LAST
power = 1.0;

// WRONG order
@gameField('float32')    // Can't be first
@range([0, 1])
power = 1.0;
```

**Why:** Decorators execute bottom-to-top. @gameField must wrap the final property.

### Rule 2: Initialize Collections

```typescript
// CORRECT
@gameField([Thruster])
thrusters = new ArraySchema<Thruster>();

@gameField({map: Spaceship})
ships = new MapSchema<Spaceship>();

// WRONG
@gameField([Thruster])
thrusters: ArraySchema<Thruster>;  // Not initialized!
```

**Why:** Colyseus needs instances, not undefined.

### Rule 3: Use Correct Types

```typescript
// CORRECT
@gameField('float32') speed = 0;      // 32-bit float
@gameField('int16') count = 0;        // 16-bit int

// WRONG
@gameField('number') speed = 0;       // No 'number' type
@gameField('float') speed = 0;        // No 'float' type (use float32/float64)
```

**Why:** Colyseus schema types are explicit.

### Rule 4: Don't Sync Everything

```typescript
// Only sync state that clients need
@gameField('float32') health = 100;   // ✅ Clients need this
@gameField('float32') damage = 10;    // ❌ Internal calculation, don't sync

// Derive internally
get damage() {
  return this.weapon.baseDamage * this.effectiveness;
}
```

**Why:** Less sync = better performance.

## Float32 Precision Gotcha

**Problem:** JavaScript numbers are 64-bit, Colyseus `float32` is 32-bit

```typescript
@gameField('float32') speed = 123.456789;
console.log(speed);  // 123.46 (precision lost!)
```

**Solution:** Use `toBeCloseTo()` in tests

```typescript
// WRONG
expect(ship.speed).toBe(123.456789);

// CORRECT
expect(ship.speed).toBeCloseTo(123.46, 1);
```

## State vs Non-State

**State (synced):**
```typescript
class ShipState extends Schema {
  @gameField('float32') health = 100;   // Synced
  @gameField(Reactor) reactor!: Reactor;  // Synced
}
```

**Non-State (server only):**
```typescript
class ShipManager {
  updateRate = 60;                      // Not synced
  lastUpdate = Date.now();              // Not synced

  update(dt: number) {
    this.state.health -= 10 * dt;       // Modify state → syncs
  }
}
```

**Rule:** Only Schema classes with @gameField sync. Plain properties don't sync.

## Commands: Client → Server

Two patterns:

### 1. JSON Pointer (Dynamic)

**Client:**
```typescript
room.send({
  type: '/Spaceship/ship-1/reactor/power',
  value: 0.8
});
```

**Server (auto-handled in ShipRoom):**
```typescript
// No code needed - JSON Pointer auto-applies to state
```

**Use when:** Simple property updates, GM interface, debugging

### 2. Typed Commands (Optimized)

**Define (in core):**
```typescript
export const setShieldPower: StateCommand<number, ShipState, void> = {
  cmdName: 'setShieldPower',
  setValue: (state, value) => {
    state.shield.power = value;
  }
};
```

**Server (register in room):**
```typescript
this.onMessage(setShieldPower.cmdName, cmdReceiver(this.manager, setShieldPower));
```

**Client (send):**
```typescript
const send = cmdSender(room, setShieldPower, undefined);
send(0.5);  // Type-safe!
```

**Use when:** High-frequency commands, complex validation, type safety

## Room Architecture

### AdminRoom

**Purpose:** Game management, map selection, start/stop

**State:** `AdminState` (has SpaceState)

**Clients:** GM interface, admin panel

**Commands:** `startGame`, `stopGame`, `loadMap`

### SpaceRoom

**Purpose:** Space-level gameplay, physics simulation

**State:** `SpaceState` (all space objects)

**Clients:** Tactical displays, overview screens

**Managed by:** `GameManager`, `SpaceManager`

### ShipRoom (per ship)

**Purpose:** Individual ship control

**State:** `ShipState` (ship systems)

**Clients:** Ship stations (weapons, engineering, etc.)

**roomId:** Equals `shipId` (`ship-0`, `ship-1`, etc.)

**Commands:** JSON Pointer only (for flexibility)

## State Sync Patterns

### Pattern 1: Server Modifies, Clients React

**Server:**
```typescript
class ShieldManager {
  update(dt: number) {
    // Modify state → auto-syncs
    this.state.shield.strength += rechargeRate * dt;
  }
}
```

**Client:**
```typescript
// Listen for changes
ship.state.shield.onChange(() => {
  updateUI(ship.state.shield.strength);
});
```

### Pattern 2: Client Commands, Server Validates

**Client:**
```typescript
// User adjusts power slider
powerSlider.on('change', (value) => {
  room.send({type: '/Spaceship/ship-0/reactor/power', value});
});
```

**Server:**
```typescript
// Receives command, validates, applies
this.onMessage((client, message) => {
  const value = clamp(0, 1, message.value);  // Validate
  applyJsonPointer(this.state, message.type, value);  // Apply
  // Auto-syncs to all clients
});
```

**Client:**
```typescript
// UI updates automatically from synced state
ship.state.reactor.listen('power', (value) => {
  powerSlider.value = value;
});
```

### Pattern 3: Multiplayer Testing

**Use `ShipTestHarness`:**
```typescript
import { ShipTestHarness } from './ship-test-harness';

test('client receives server state updates', async () => {
  const harness = new ShipTestHarness();
  await harness.connect();

  // Server modifies
  harness.shipManager.state.shield.strength = 750;

  // Wait for sync
  await harness.waitForSync();

  // Client receives
  expect(harness.shipDriver.state.shield.strength).toBe(750);

  await harness.cleanup();
});
```

**Use `MultiClientDriver`:**
```typescript
import { MultiClientDriver } from '@starwards/server/test/multi-client-driver';

test('multiple clients see same state', async () => {
  const driver = new MultiClientDriver();
  await driver.start();

  const [c1, c2] = await Promise.all([
    driver.joinShip('ship-1'),
    driver.joinShip('ship-1')
  ]);

  // Modify server state
  driver.getShipManager('ship-1').state.shield.strength = 800;
  await driver.waitForSync();

  // Both clients updated
  expect(c1.state.shield.strength).toBe(800);
  expect(c2.state.shield.strength).toBe(800);

  await driver.cleanup();
});
```

See `docs/testing/UTILITIES.md` for full API.

## Common Colyseus Pitfalls

### Pitfall 1: Modifying State Without @gameField

```typescript
// WRONG - doesn't sync
class Shield {
  strength = 1000;  // No decorator
}

// CORRECT - syncs
class Shield extends Schema {
  @gameField('float32') strength = 1000;
}
```

### Pitfall 2: Setting Objects Instead of Properties

```typescript
// WRONG - breaks references
state.velocity = {x: 10, y: 0};

// CORRECT - update properties
state.velocity.setValue({x: 10, y: 0});
// Or:
state.velocity.x = 10;
state.velocity.y = 0;
```

**Why:** Colyseus tracks property changes, not object replacement.

### Pitfall 3: Forgetting await harness.waitForSync()

```typescript
// WRONG - client not updated yet
harness.shipManager.state.health = 50;
expect(harness.shipDriver.state.health).toBe(50);  // FAILS

// CORRECT - wait for replication
harness.shipManager.state.health = 50;
await harness.waitForSync();
expect(harness.shipDriver.state.health).toBe(50);  // PASSES
```

### Pitfall 4: Using State in Client-Side Logic

```typescript
// WRONG - client shouldn't have business logic
if (ship.state.health < 50) {
  ship.state.broken = true;  // Don't modify from client
}

// CORRECT - send command, server decides
if (ship.state.health < 50) {
  room.send({type: 'checkBroken'});  // Server validates & applies
}
```

**Why:** Server is authoritative. Client is display only.

### Pitfall 5: Float32 Precision in Tests

```typescript
// WRONG - exact match fails
expect(ship.speed).toBe(123.456789);

// CORRECT - close enough
expect(ship.speed).toBeCloseTo(123.46, 1);
```

### Pitfall 6: Not Cleaning Up Test Harness

```typescript
// WRONG - leaves connections open
test('something', async () => {
  const harness = new ShipTestHarness();
  await harness.connect();
  // Test code
});  // MISSING cleanup()!

// CORRECT
test('something', async () => {
  const harness = new ShipTestHarness();
  await harness.connect();
  // Test code
  await harness.cleanup();  // Clean up
});
```

## Debugging Colyseus Issues

### 1. Colyseus Monitor

```
http://localhost:2567/colyseus-monitor
Login: admin / admin
```

**See:**
- Active rooms
- Connected clients
- State tree (live values)

### 2. Chrome DevTools Network Tab

**WebSocket messages:**
1. Open DevTools (F12)
2. Network tab → WS filter
3. Click connection
4. See Messages: commands sent, patches received

### 3. State Logging

**Server:**
```typescript
console.log('[SERVER] Shield strength:', this.state.shield.strength);
```

**Client:**
```typescript
console.log('[CLIENT] Shield strength:', ship.state.shield.strength);
```

Compare values to find sync issues.

### 4. JSON Pointer Path Validation

**Test paths:**
```typescript
const path = '/Spaceship/ship-1/shield/power';
const obj = resolveJsonPointer(state, path);
console.log('Resolved:', obj);  // Should not be undefined
```

## Performance Considerations

### Minimize Sync Frequency

```typescript
// WRONG - syncs 60 times/sec
update(dt: number) {
  this.state.position.x += velocity.x * dt;
  this.state.position.y += velocity.y * dt;
}

// BETTER - sync only when significant change
update(dt: number) {
  const newX = this.state.position.x + velocity.x * dt;
  const newY = this.state.position.y + velocity.y * dt;

  if (Math.abs(newX - this.state.position.x) > 0.1) {
    this.state.position.x = newX;
  }
  if (Math.abs(newY - this.state.position.y) > 0.1) {
    this.state.position.y = newY;
  }
}
```

**But:** Starwards updates are already optimized. Don't prematurely optimize.

### Use Appropriate Types

```typescript
// WRONG - wastes bandwidth
@gameField('float64') health = 100;  // 8 bytes

// CORRECT - sufficient precision
@gameField('float32') health = 100;  // 4 bytes
```

### Batch Commands

```typescript
// WRONG - multiple round trips
room.send({type: '/Spaceship/ship-0/reactor/power', value: 0.8});
room.send({type: '/Spaceship/ship-0/thrusters/0/enabled', value: true});
room.send({type: '/Spaceship/ship-0/thrusters/1/enabled', value: true});

// BETTER - single batch command
room.send('batchUpdate', {
  '/reactor/power': 0.8,
  '/thrusters/0/enabled': true,
  '/thrusters/1/enabled': true
});
```

**But:** Only if actually a bottleneck. JSON Pointer is fine for normal use.

## Integration with Other Skills

- **starwards-tdd** - Test state sync with harnesses
- **starwards-debugging** - Debug sync issues with tools
- **starwards-verification** - Verify multiplayer scenarios

## Quick Reference

| Task | Pattern |
|------|---------|
| Add synced property | `@gameField('type') prop = value` |
| Nested Schema | `@gameField(Class) obj = new Class()` |
| Array | `@gameField([Class]) arr = new ArraySchema()` |
| Map | `@gameField({map: Class}) map = new MapSchema()` |
| Send command (client) | `room.send({type: '/path', value})` |
| Listen to changes (client) | `state.onChange(() => {})` |
| Test sync | `await harness.waitForSync()` |
| Debug state | Colyseus Monitor (port 2567) |

## The Bottom Line

**Remember:**
1. @gameField must be last decorator
2. State is source of truth (server authoritative)
3. Commands go client → server, patches go server → client
4. Use harnesses for multiplayer tests
5. Float32 has precision loss (use toBeCloseTo)
6. Clean up test connections (await cleanup())
7. When in doubt, check Colyseus Monitor
