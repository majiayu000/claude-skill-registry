---
name: ta-validation-typescript
description: TypeScript best practices for game development. Use when writing TypeScript for game code, defining types, avoiding anti-patterns.
category: architectural
---

# TypeScript Patterns Skill

> "Strong types catch bugs at compile time – not at runtime."

## When to Use This Skill

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

| Use Case           | Pattern                 |
| ------------------ | ----------------------- | --------- | ---------- |
| Object shape       | `interface`             |
| Union types        | `type`                  |
| Enum-like values   | `const object as const` |
| Generic containers | `Generic<T>`            |
| Nullable values    | `T                      | null`or`T | undefined` |
| Exhaustive checks  | `never` type            |

## Progressive Guide

### Level 1: Basic Types

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

### Level 2: Union Types

```typescript
// String literal unions (better than enum)
type GamePhase = 'loading' | 'menu' | 'playing' | 'paused' | 'gameOver';

// Discriminated unions
type GameEvent =
  | { type: 'PLAYER_SPAWN'; playerId: string; position: Vector3 }
  | { type: 'PLAYER_DEATH'; playerId: string; cause: string }
  | { type: 'SCORE_UPDATE'; playerId: string; score: number };

// Type narrowing
function handleEvent(event: GameEvent) {
  switch (event.type) {
    case 'PLAYER_SPAWN':
      // TypeScript knows event has position here
      spawnPlayer(event.playerId, event.position);
      break;
    case 'PLAYER_DEATH':
      // TypeScript knows event has cause here
      logDeath(event.playerId, event.cause);
      break;
  }
}
```

### Level 3: Generics

```typescript
// Generic pool
class ObjectPool<T> {
  private pool: T[] = [];
  private factory: () => T;

  constructor(factory: () => T, initialSize: number) {
    this.factory = factory;
    for (let i = 0; i < initialSize; i++) {
      this.pool.push(factory());
    }
  }

  acquire(): T {
    return this.pool.pop() ?? this.factory();
  }

  release(item: T): void {
    this.pool.push(item);
  }
}

// Usage
const bulletPool = new ObjectPool(() => new Bullet(), 100);
```

### Level 4: Utility Types

```typescript
// Partial - make all properties optional
type PartialPlayer = Partial<Player>;

// Required - make all properties required
type RequiredConfig = Required<GameConfig>;

// Pick - select specific properties
type PlayerPosition = Pick<Player, 'x' | 'y' | 'z'>;

// Omit - exclude properties
type PlayerWithoutId = Omit<Player, 'id'>;

// Record - create object type from keys
type ScoreBoard = Record<string, number>;

// ReturnType - get return type of function
type SpawnResult = ReturnType<typeof spawnPlayer>;
```

### Level 5: React + TypeScript Patterns

```typescript
// Component props
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
}

// Props with children
interface ContainerProps {
  children: React.ReactNode;
  className?: string;
}

// Event handlers
interface GameCanvasProps {
  onPlayerMove: (position: Vector3) => void;
  onPlayerShoot: (direction: Vector3) => void;
}

// Ref types
const meshRef = useRef<THREE.Mesh>(null);
const rigidBodyRef = useRef<RapierRigidBody>(null);

// State with complex types
const [gameState, setGameState] = useState<GameState>({
  phase: 'loading',
  players: [],
  score: 0,
});
```

## Anti-Patterns

❌ **DON'T:**

```typescript
// Using 'any'
const data: any = fetchData();

// Ignoring errors
// @ts-ignore
brokenCode();

// Using 'as' without reason
const value = data as ComplexType;

// Non-null assertion abuse
const name = player!.name!.first!;
```

✅ **DO:**

```typescript
// Use 'unknown' and narrow
const data: unknown = fetchData();
if (isPlayer(data)) {
  // Now TypeScript knows it's Player
}

// Fix the actual error
fixedCode();

// Use type guards
function isPlayer(obj: unknown): obj is Player {
  return typeof obj === 'object' && obj !== null && 'id' in obj;
}

// Safe access
const name = player?.name?.first ?? 'Unknown';
```

## Type Guards

```typescript
// Custom type guard
function isVector3(obj: unknown): obj is Vector3 {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'x' in obj &&
    'y' in obj &&
    'z' in obj &&
    typeof (obj as Vector3).x === 'number'
  );
}

// Assert function
function assertDefined<T>(value: T | undefined): asserts value is T {
  if (value === undefined) {
    throw new Error('Value is undefined');
  }
}
```

## Zustand Store Types

```typescript
interface GameStore {
  // State
  players: Map<string, Player>;
  phase: GamePhase;
  score: number;

  // Actions
  addPlayer: (player: Player) => void;
  removePlayer: (id: string) => void;
  setPhase: (phase: GamePhase) => void;
  incrementScore: (amount: number) => void;
}

const useGameStore = create<GameStore>((set) => ({
  players: new Map(),
  phase: 'loading',
  score: 0,

  addPlayer: (player) =>
    set((state) => ({
      players: new Map(state.players).set(player.id, player),
    })),

  removePlayer: (id) =>
    set((state) => {
      const players = new Map(state.players);
      players.delete(id);
      return { players };
    }),

  setPhase: (phase) => set({ phase }),
  incrementScore: (amount) => set((state) => ({ score: state.score + amount })),
}));
```

## React UI Component Patterns

### ❌ AVOID: Inline Styles Anti-Pattern

**Problem**: Inline styles in JSX are a major maintainability anti-pattern:

```tsx
// BAD: 90+ lines of inline styles - impossible to maintain
<div style={{
  position: 'absolute',
  top: 0,
  left: 0,
  width: '100%',
  height: '100%',
  backgroundColor: 'rgba(0, 0, 0, 0.7)',
  display: 'flex',
  flexDirection: 'column',
  // ... 80 more lines
}}>
```

**Why it's bad**:
- Impossible to theme or update consistently
- No CSS optimizations (browser can't cache)
- Can't use CSS pseudo-classes (`:hover`, `:focus`)
- Hard to test in isolation
- Violates separation of concerns

### ✅ DO: Extract UI Components with CSS Modules

```tsx
// GOOD: Separate component with CSS module
import styles from './PausedOverlay.module.css';

interface PausedOverlayProps {
  onResume: () => void;
  onQuit: () => void;
}

export function PausedOverlay({ onResume, onQuit }: PausedOverlayProps) {
  return (
    <div className={styles.overlay}>
      <h1 className={styles.title}>PAUSED</h1>
      <div className={styles.buttons}>
        <button onClick={onResume} className={styles.button}>Resume</button>
        <button onClick={onQuit} className={styles.buttonQuit}>Quit</button>
      </div>
    </div>
  );
}
```

**CSS Module (`PausedOverlay.module.css`)**:

```css
.overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.title {
  font-size: clamp(2rem, 5vw, 4rem);
  color: #ff6464;
  text-shadow: 0 0 20px rgba(255, 100, 100, 0.8);
}

.button {
  padding: 0.75rem 2rem;
  margin: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.button:hover {
  transform: scale(1.05);
}
```

### State Management Pattern: Single Source of Truth

**Problem**: Duplicate state between parent and child components

```tsx
// BAD: Duplicate state - GameScene and GameSceneContent both track pointer lock
const [isPointerLocked, setIsPointerLocked] = useState(false); // In GameScene
const [isPointerLocked, setIsPointerLocked] = useState(false); // In GameSceneContent
```

**Solution**: Either lift state up OR keep it in the child, not both:

```tsx
// GOOD: Single source of truth - keep in child, use callback for parent
interface GameSceneProps {
  onPointerLockChange?: (locked: boolean) => void;
}

// Child manages the actual state
function GameSceneContent({ onPointerLockChange }: GameSceneProps) {
  const [isPointerLocked, setIsPointerLocked] = useState(false);

  const handleLockChange = useCallback(() => {
    const locked = document.pointerLockElement !== null;
    setIsPointerLocked(locked);
    onPointerLockChange?.(locked); // Notify parent if needed
  }, [onPointerLockChange]);

  // ...
}
```

### Theme Constants for Magic Numbers

```tsx
// GOOD: Extract magic values to named constants
// src/styles/theme.ts
export const OVERLAY = {
  BACKGROUND: 'rgba(0, 0, 0, 0.7)',
  PAUSED_GLOW: '0 0 20px rgba(255, 100, 100, 0.8)',
} as const;

export const FONT = {
  SANS: 'Arial, sans-serif',
  MONO: 'monospace',
} as const;

export const SENSITIVITY = {
  DPI_800_HIPFIRE: 0.002,
  DPI_800_ADS: 0.0014, // 70% of hipfire
  ADS_MULTIPLIER: 0.7,
} as const;

// Usage
import { OVERLAY, FONT, SENSITIVITY } from '@/styles/theme';
```

## Checklist

Before committing TypeScript code:

- [ ] No `any` types without justification comment
- [ ] No `@ts-ignore` or `@ts-expect-error`
- [ ] Interfaces defined for all data structures
- [ ] Function parameters and returns typed
- [ ] Optional properties marked with ? (the ? operator)
- [ ] Nullable values handled with optional chaining (?.) or nullish coalescing (??)
- [ ] Type guards for unknown data
- [ ] **NEW**: No inline styles longer than 3 properties
- [ ] **NEW**: Extract UI overlays to separate components with CSS modules
- [ ] **NEW**: No duplicate state between parent and child components
- [ ] **NEW**: Magic numbers extracted to named constants

## Related Skills

For UI component patterns: `Skill("ta-ui-polish")`

## External References

- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
