---
name: dev-typescript-advanced
description: Advanced TypeScript patterns - generics, utility types, React patterns. Use for complex type scenarios.
category: typescript
---

# Advanced TypeScript Patterns

Generics, utility types, and React integration patterns.

## When to Use

Use when:
- Creating reusable generic types
- Working with complex type transformations
- Typing React components and hooks

## Generics

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

## Utility Types

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

## React Patterns

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
  onPlayerMove: (position: Vector3Like) => void;
  onPlayerShoot: (direction: Vector3Like) => void;
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

## Generic Constraints

```typescript
// Constrain generic type
interface Entity<T extends { id: string }> {
  entities: Map<string, T>;
}

function addEntity<T extends { id: string }>(state: EntityState<T>, entity: T): void {
  state.entities.set(entity.id, entity);
}
```

## Type Guards

```typescript
// Type guard for discriminated unions
function isPlayerSpawn(event: GameEvent): event is Extract<GameEvent, { type: 'PLAYER_SPAWN' }> {
  return event.type === 'PLAYER_SPAWN';
}

// Usage
function handleEvent(event: GameEvent) {
  if (isPlayerSpawn(event)) {
    // TypeScript knows event has position here
    console.log(event.position);
  }
}
```

## Reference

- **[dev-typescript-basics](../dev-typescript-basics/SKILL.md)** — Core patterns
