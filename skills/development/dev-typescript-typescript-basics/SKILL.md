---
name: typescript-basics
description: Core TypeScript patterns for game development. Use when defining types and interfaces.
---

# TypeScript Basics

> "Strong types catch bugs at compile time – not at runtime."

## When to Use

Use when:
- Defining component props
- Creating game state interfaces
- Writing utility functions
- Handling events and callbacks

## Quick Start

```typescript
// Define interfaces for game entities
interface Player {
  id: string;
  position: Vector3Like;
  health: number;
  inventory: Item[];
}

interface Vector3Like {
  x: number;
  y: number;
  z: number;
}

interface Item {
  id: string;
  type: 'weapon' | 'armor' | 'consumable';
  quantity: number;
}
```

## Decision Framework

| Use Case | Pattern |
|----------|---------|
| Object shape | `interface` |
| Union types | `type` |
| Enum-like values | `const object as const` |
| Nullable values | `T \| null \| undefined` |

## Basic Types

```typescript
// Primitive types
const health: number = 100;
const name: string = 'Player 1';
const isAlive: boolean = true;

// Arrays
const inventory: string[] = ['sword', 'shield'];
const scores: Array<number> = [10, 20, 30];

// Objects
interface Player {
  id: string;
  name: string;
  health: number;
}

const player: Player = {
  id: '1',
  name: 'Hero',
  health: 100,
};
```

## Union Types

```typescript
// String literal unions (better than enum)
type GamePhase = 'loading' | 'menu' | 'playing' | 'paused' | 'gameOver';

// Discriminated unions
type GameEvent =
  | { type: 'PLAYER_SPAWN'; playerId: string; position: Vector3Like }
  | { type: 'PLAYER_DEATH'; playerId: string; cause: string }
  | { type: 'SCORE_UPDATE'; playerId: string; score: number };

// Type narrowing
function handleEvent(event: GameEvent) {
  switch (event.type) {
    case 'PLAYER_SPAWN':
      spawnPlayer(event.playerId, event.position);
      break;
    case 'PLAYER_DEATH':
      logDeath(event.playerId, event.cause);
      break;
  }
}
```

## Nullable Types

```typescript
// Nullable value
interface WeaponSlot {
  weapon: Weapon | null;
}

// Optional property
interface PlayerConfig {
  name: string;
  team?: string;  // Optional
  color?: number;  // Optional
}

// Nullish coalescing
function getTeam(config: PlayerConfig): string {
  return config.team ?? 'unassigned';
}
```

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| Using `any` type | Use specific types |
| `type` for object shape | Use `interface` |
| Using `enum` | Use `const as const` unions |
| Not handling null | Use `??` or `?.` |

## Reference

- [typescript-advanced.md](./typescript-advanced.md) - Generics and utility types
