---
name: dev-typescript-basics
description: Core TypeScript patterns for game development. Use when defining types and interfaces.
category: typescript
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

## Error Boundaries (React 18+)

Error boundaries catch JavaScript errors in component trees, preventing app crashes.

```typescript
// components/ErrorBoundary.tsx
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div style={{ padding: '2rem', textAlign: 'center' }}>
          <h2>Something went wrong</h2>
          <button onClick={() => window.location.reload()}>
            Reload Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Usage in App.tsx
function App() {
  return (
    <ErrorBoundary>
      <Canvas>
        <Scene />
      </Canvas>
    </ErrorBoundary>
  );
}
```

### Error Boundary Best Practices

| Strategy | When to Use |
|----------|-------------|
| Wrap entire app | Always - prevents total crashes |
| Wrap Canvas | For R3F scene errors |
| Wrap data fetching | For API/server errors |
| Wrap third-party integrations | For unpredictable components |

### Async Error Handling

Error boundaries don't catch async errors. Use error callbacks:

```typescript
// For async operations
useEffect(() => {
  const fetchData = async () => {
    try {
      const data = await fetchSomething();
      setState(data);
    } catch (error) {
      console.error('Async error:', error);
      // Handle async errors explicitly
      setErrorState(error);
    }
  };
  fetchData();
}, []);
```

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| Using `any` type | Use specific types |
| `type` for object shape | Use `interface` |
| Using `enum` | Use `const as const` unions |
| Not handling null | Use `??` or `?.` |
| No error boundaries | Wrap app with ErrorBoundary |

## Reference

- **[dev-typescript-advanced](../dev-typescript-advanced/SKILL.md)** — Generics and utility types
