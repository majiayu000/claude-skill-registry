---
name: coding-patterns
description: TypeScript monorepo patterns including contract-port architecture, dependency injection, hermetic primitive ports, and composition root. Use when creating packages, designing contracts/interfaces, implementing ports, wrapping platform primitives (Date, console, process), or testing with inline mocks.
---

# Coding Patterns





## Package Architecture

| Type | Naming | Purpose |
|------|--------|---------|
| **Contract** | `@{scope}/contract-{name}` | Pure TypeScript interfaces and types. No runtime code. |
| **Port** | `@{scope}/port-{name}` | An implementation that abides by the corresponding contract. All dependencies are injected by the app layer. |

All code within the packages/ directory must be hermetically sealed from direct use of globals. All globals, even simple ones like Date or console, are not allowed. TextEncoder, Buffer, and so on, must be a contract + package. Apps in the /apps directory are specific to a platform and inject platform/os-specific dependencies into our ports. Apps can depend on contracts if they need the types. Apps can also pull in third party libraries, which packages never do.

Direct use of globals creates hidden dependencies and lead to spaghetti code:

1. **Breaks testability**: Can't mock `console.log` or `Date.now()` easily
2. **Couples to platform**: Code assumes Node.js, browser, or specific runtime
3. **Hides dependencies**: Function signatures don't reveal what they need
4. **Prevents composition**: Can't swap implementations at runtime

### Contracts

Contracts contain only types and interfaces. Never use constants, classes, functions or enums in contracts packages. Do not rely on any dependencies except other contracts.

Rule: If it compiles down to executable JavaScript, it doesn't belong in a contract.

```typescript
// GOOD: Contract
export interface Logger {
  info(message: string): void;
}

// BAD: Contract with implementation
export class ConsoleLogger implements Logger {
  info(message: string) { console.log(message); }  // NO! `console.log` reference is incorrect as console is a global.
}
```

### Ports

Ports are an implementation of a contract. They can compose multiple contracts together to perform some useful function. They do not perform dependency injection, but they rely on it. Ports never use globals directly.

```typescript
// BAD: Direct global usage
export function createLogger(): Logger {
  return {
    info(msg) {
      console.log(new Date().toISOString(), msg);  // NO!
    }
  };
}

// GOOD: Dependencies injected
import type { OutChannel } from '@scope/contract-outchannel';
import type { Clock } from '@scope/contract-clock';

export type LoggerDeps = {
  channel: OutChannel;
  clock: Clock;
}

export type LoggerOptions = {
  colors?: boolean;
}

export function createLogger(deps: LoggerDeps, options: LoggerOptions): Logger {
  return {
    info(msg) {
      deps.channel.write(`${deps.clock.timestamp()} ${msg}`);
    }
  };
}
```

With this structure, testing ports is straightforward. You can think of the test code as almost an entry in an `app` directory. Assume test code has access to node.js globals and a JSDOM-provided polyfill of browser globals. Do not exert a lot of effort creating your own custom implementations when injecting dependencies into ports. You can write test code as if you were writing an app.

### 4. Recursive Dependency Extraction

When building a port, if you need to abstract something:

1. Identify the dependency (e.g., "I need current time")
2. Create `@scope/contract-clock` with the interface
3. Create `@scope/port-clock` with system implementation
4. Import the contract in your original port

### 5. Data vs Capability Pattern

A critical distinction in contract design: **Data is not a capability.**

**Data** = Pure values, immutable structures, serializable state
**Capability** = Something that *does* something (I/O, side effects, platform access)

#### The Rule

If you're tempted to put methods on a data structure contract, stop. Those methods are *operations on data*—they belong in the port as pure functions that take the data as input.

#### Benefits of Data-as-Data

| Benefit | Explanation |
|---------|-------------|
| **Serialization** | Pure data can be JSON.stringify'd for persistence, debugging, network transfer |
| **Time-travel debugging** | Store history of states, replay any point |
| **Structural sharing** | Immutable updates enable efficient diffing and caching |
| **Testing without mocks** | Operations are pure functions; just pass data in, check data out |
| **Composition** | Data flows through pipelines; no hidden state |

#### Anti-pattern: Methods on Data

```typescript
// BAD: Contract with methods (treats data as capability)
export interface RingBuffer<T> {
  push(item: T): void;           // NO - mutates state
  pop(): T | undefined;          // NO - mutates state
  peek(): T | undefined;         // NO - operation on data
  readonly size: number;
  readonly capacity: number;
}
```

#### Correct Pattern: Pure Data + Pure Functions

**Contract** (pure types only):
```typescript
// Data is just data - indices and storage reference
export interface RingBuffer<T> {
  readonly head: number;
  readonly tail: number;
  readonly size: number;
  readonly capacity: number;
  readonly storage: RingBufferStorage<T>;
}
```

**Port** (pure functions that transform data):
```typescript
// Operations return new state, never mutate
export function push<T>(buffer: RingBuffer<T>, item: T): RingBuffer<T>;
export function pop<T>(buffer: RingBuffer<T>): PopResult<T>;
export function peek<T>(buffer: RingBuffer<T>): T | undefined;
export function toArray<T>(buffer: RingBuffer<T>): T[];
```

**Usage** (immutable style):
```typescript
let buffer = createRingBuffer(factory, 5);
buffer = push(buffer, 1);
buffer = push(buffer, 2);
const { item, buffer: next } = pop(buffer);
// `buffer` still has 2 elements - unchanged!
// `next` has 1 element
```

#### When Capabilities Are Appropriate

Capabilities (interfaces with methods) are correct for:

1. **Platform abstractions** - `Logger`, `Clock`, `OutChannel` do I/O
2. **Observer callbacks** - `DagExecutionObserver.onNodeStart()` fires events
3. **Storage interfaces** - `RingBufferStorage.get()/set()` abstracts platform storage

The distinction: these represent *external capabilities* injected by the platform, not operations on your domain data.

#### Reference Implementations

| Package | Contract | Port |
|---------|----------|------|
| DAG | `Dag<T>` = pure array of nodes | `validateDag()`, `executeDag()`, `getTopologicalOrder()` |
| Ring Buffer | `RingBuffer<T>` = indices + storage | `push()`, `pop()`, `peek()`, `toArray()` |
| Control Flow | `Result<T,E>`, `ExitCode` = pure types | `ok()`, `err()`, `mapResult()` |

### 6. Factory Function Argument Order

Port factories follow a consistent two-argument pattern:

| Argument | Contains | Required |
|----------|----------|----------|
| 1st: `deps` | Other contracts/ports | Yes (if port has external deps) |
| 2nd: `options` | Configuration settings | No (always optional) |

**Pattern A: Port with external dependencies**

```typescript
// Dependencies: other contracts this port needs (required)
export interface LoggerDependencies {
  readonly channel: OutChannel;
  readonly clock: WallClock;
}

// Options: configuration settings (all optional)
export interface LoggerOptions {
  readonly minLevel?: LogLevel;
}

// Factory: deps first, options second
export function createLogger(
  deps: LoggerDependencies,
  options: LoggerOptions = {}
): Logger { ... }
```

**Pattern B: Simple port (no external deps)**

```typescript
export interface WallClockOptions {
  readonly nowMs?: () => number;  // Override for testing
}

export function createWallClock(
  options: WallClockOptions = {}
): WallClock { ... }
```
### 7. No Fake Defaults for Required Dependencies

**The Problem**: Code that provides "defaults" that don't actually work.

```typescript
// BAD: Looks sensible, but createDefaultGenerateId is a no-op
const generateId = deps.generateId ?? createDefaultGenerateId(DateCtor);

// BAD: "Default" logger that silently drops messages
const logger = deps.logger ?? { info: () => {}, error: () => {} };

// BAD: Fallback that returns garbage
const clock = deps.clock ?? { now: () => 0 };
```
**The Fix**: Required dependencies must be required.

```typescript
// GOOD: Required dependency - fails fast at wiring time
export interface ServiceDependencies {
  readonly generateId: () => string;  // No optional, no default
  readonly logger: Logger;
  readonly clock: Clock;
}

export function createService(deps: ServiceDependencies): Service {
  // deps.generateId is guaranteed to exist and work
  return {
    process: () => {
      const id = deps.generateId();
      deps.logger.info(`Processing ${id}`);
      // ...
    }
  };
}
```
**Anti-patterns to catch in review:**

| Pattern | Problem |
|---------|---------|
| `deps.x ?? () => {}` | No-op function default |
| `deps.x ?? () => null` | Null-returning default |
| `deps.x ?? () => 0` | Magic number default |
| `deps.x ?? createDefault...()` | Suspiciously named "default" factory |
| `deps.x ?? { method: () => {} }` | Stub object with empty methods |

**The Rule**: If you can't provide a default that fulfills the contract, don't provide a default. Let it fail loud at wiring time, not silent at runtime.

### Using `declare const` for Contract Symbols

When a contract needs to reference a symbol (like EXIT_CODE), use TypeScript's ambient declaration syntax with a type alias to avoid `typeof import()`:

```typescript
// In contract (no runtime value)
export declare const EXIT_CODE: unique symbol;

// Export a type alias so ports can use proper import type
export type ExitCodeSymbol = typeof EXIT_CODE;

// In port (actual runtime value)
import type { ExitCodeSymbol } from '@scope/contract-control-flow';

export const EXIT_CODE: ExitCodeSymbol = Symbol.for('scope.exitCode') as ExitCodeSymbol;
```
**Never use `typeof import()` syntax** - it looks like a runtime import and violates the type-only contract principle. The verification pipeline will flag violations.

## App Dependency Injection

Apps are composition roots. They inject dependencies into ports. This is the only place where real platform globals are referenced.

```typescript
// src/main.ts (composition root)
import { createLogger } from '@scope/port-logger';
import { createSystemClock } from '@scope/port-clock';
import { createStderrChannel } from '@scope/port-outchannel';
import { createApp } from './app';

const clock = createSystemClock(Date);
const channel = createStderrChannel(console);
const logger = createLogger({ channel, clock });
const app = createApp({ logger, clock });
app.start();
```

**Key principle**: All packages except the composition root are hermetically sealed.

```typescript
// src/app.ts (business logic - no globals)
import type { Logger } from '@scope/contract-logger';

interface AppDeps {
  logger: Logger;
}

export function createApp(deps: AppDeps) {
  return {
    start: () => deps.logger.info('Starting app'),
  };
}
```

### Contract Package

```
packages/contract-{name}/
├── src/index.ts
├── package.json
└── tsconfig.json
```

```json
{
  "name": "@scope/contract-{name}",
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "development": "./src/index.ts",
      "source": "./src/index.ts",
      "import": "./dist/index.js"
    }
  },
  "scripts": { "build": "tsc" }
}
```

### Port Package

```
packages/port-{name}/
├── src/
│   ├── index.ts
│   └── index.test.ts
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

```json
{
  "name": "@scope/port-{name}",
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "development": "./src/index.ts",
      "source": "./src/index.ts",
      "import": "./dist/index.js"
    }
  },
  "scripts": {
    "build": "tsc",
    "test": "vitest run",
    "test:coverage": "vitest run --coverage"
  },
  "dependencies": {
    "@scope/contract-{dep}": "0.0.1"
  },
  "devDependencies": {
    "vitest": "^4.0.15"
  }
}
```

**Vitest Configuration** (`vitest.config.ts`):

```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    include: ['src/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts'],
      exclude: ['src/**/*.test.ts'],
      thresholds: {
        lines: 100,
        functions: 100,
        branches: 100,
        statements: 100,
      },
    },
  },
})
```
### Testing Time-Based Code

Use Vitest's built-in fake timers instead of complex inline implementations:

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { createScheduler } from './scheduler';

describe('Scheduler', () => {
  beforeEach(() => { vi.useFakeTimers(); });
  afterEach(() => { vi.useRealTimers(); });

  function createTestScheduler() {
    return createScheduler({
      setTimeout: globalThis.setTimeout,
      clearTimeout: globalThis.clearTimeout,
      setInterval: globalThis.setInterval,
      clearInterval: globalThis.clearInterval,
    });
  }

  it('executes callback after delay', () => {
    const scheduler = createTestScheduler();
    const callback = vi.fn();

    scheduler.delay(callback, 1000);
    expect(callback).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1000);
    expect(callback).toHaveBeenCalledOnce();
  });
});
```

**Why Vitest fake timers over inline fakes:**
- Simpler tests with less boilerplate
- Vitest handles edge cases (nested timers, microtasks)
- Consistent with other tests in the codebase
- Works perfectly with real globalThis functions when timers are faked

### Creating a Contract

- [ ] Name follows `@scope/contract-{name}` pattern
- [ ] Contains only interfaces and types
- [ ] No runtime code (no JS emitted)
- [ ] No runtime dependencies
- [ ] Exports documented with JSDoc

### Creating a Port

- [ ] Name follows `@scope/port-{name}` pattern
- [ ] All dependencies are contracts
- [ ] No direct globals (console, Date, process, Math.random)
- [ ] Dependencies (contracts) separate from options (config)
- [ ] `vitest.config.ts` present with 80% coverage thresholds
- [ ] Internal package dependencies use version `0.0.1`

## Exceptions

These patterns are **not required** in:

1. **Test files**: Direct globals are acceptable in test code
3. **Entry points**: The composition root can inject platform-specific implementations as dependencies to ports