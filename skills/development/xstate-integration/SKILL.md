---
name: xstate-integration
description: XState v5 state machine patterns for TMNL. Covers setup().createMachine(), typed context/events/actions/guards, invoke for async, and the novel stx hybrid pattern (XState + Legend-State + effect-atom).
model_invoked: true
triggers:
  - "XState"
  - "xstate"
  - "createMachine"
  - "useMachine"
  - "state machine"
  - "stx"
  - "Legend-State"
---

# XState Integration for TMNL

## Overview

XState v5 is the state machine library for lifecycle management in TMNL. It powers:
- **Minibuffer** (command palette) — `src/lib/minibuffer/v2/machine.ts`
- **Drag orchestration** — `src/lib/drag/machines/drag-machine.ts`
- **Floating panels** — `src/lib/floating/machines/panel-machine.ts`
- **Animation state** — `src/lib/animation/v2/machine.ts`

**Novel Pattern**: TMNL implements a **stx hybrid** pattern that composes XState + Legend-State + effect-atom into a unified state system.

## Canonical Sources

### XState v5 Documentation
- **DeepWiki**: Query `statelyai/xstate` for canonical patterns
- **Official docs**: https://stately.ai/docs

### TMNL Implementations
- **Minibuffer machine** — `src/lib/minibuffer/v2/machine.ts` (canonical example)
- **Minibuffer tests** — `src/lib/minibuffer/v2/__tests__/machine.test.ts`
- **STX architecture** — `src/lib/stx/ARCHITECTURE.md`
- **STX factory** — `src/lib/stx/stx.ts`
- **Test patterns** — `src/lib/stx/__tests__/TEST_PATTERNS.md`

---

## Pattern 1: setup().createMachine() — CANONICAL V5 PATTERN

**When:** Creating any typed state machine in XState v5.

The `setup()` function provides centralized type-safe definitions for context, events, actions, guards, and actors.

```typescript
import { setup, assign, type ActorRefFrom } from 'xstate'

// Event discriminated union
type MyEvent =
  | { type: 'START'; payload: string }
  | { type: 'STOP' }
  | { type: 'RESET' }

// Context interface
interface MyContext {
  count: number
  lastPayload: string | null
}

const myMachine = setup({
  types: {} as {
    context: MyContext
    events: MyEvent
  },
  actions: {
    increment: assign({ count: ({ context }) => context.count + 1 }),
    setPayload: assign({
      lastPayload: ({ event }) =>
        event.type === 'START' ? event.payload : null
    }),
    reset: assign({ count: 0, lastPayload: null }),
  },
  guards: {
    hasPayload: ({ context }) => context.lastPayload !== null,
    isPositive: ({ context }) => context.count > 0,
  },
}).createMachine({
  id: 'myMachine',
  initial: 'idle',
  context: { count: 0, lastPayload: null },
  states: {
    idle: {
      on: {
        START: {
          target: 'active',
          actions: ['increment', 'setPayload'],
        },
      },
    },
    active: {
      on: {
        STOP: 'idle',
        RESET: {
          target: 'idle',
          actions: 'reset',
        },
      },
    },
  },
})

export type MyMachine = typeof myMachine
export type MyActor = ActorRefFrom<MyMachine>
```

**TMNL Example** — Minibuffer machine (`src/lib/minibuffer/v2/machine.ts:1-150`):
```typescript
export type MinibufferEvent =
  | { type: 'OPEN_PROMPT'; prompt: string; defaultValue?: string }
  | { type: 'OPEN_COMMAND'; providerId: ProviderId; prompt?: string }
  | { type: 'INPUT_CHANGE'; value: string }
  | { type: 'SELECT_NEXT' }
  | { type: 'SUBMIT' }
  | { type: 'CANCEL' }

export const minibufferMachine = setup({
  types: {} as {
    context: MinibufferContext
    events: MinibufferEvent
  },
  actions: {
    updateInput: assign(({ event }) => {
      if (event.type !== 'INPUT_CHANGE') return {}
      return { input: event.value, selectedIndex: 0 }
    }),
    selectNext: assign(({ context }) => ({
      selectedIndex: (context.selectedIndex + 1) % context.completions.length,
    })),
  },
  guards: {
    hasCompletions: ({ context }) => context.completions.length > 0,
  },
}).createMachine({
  id: 'minibuffer',
  initial: 'idle',
  context: { /* ... */ },
  states: { /* ... */ },
})
```

---

## Pattern 2: invoke — ASYNC OPERATIONS

**When:** Machine needs to trigger async operations (API calls, animations, timers).

```typescript
import { setup, fromPromise, assign } from 'xstate'

const fetchData = fromPromise(async ({ input }: { input: { id: string } }) => {
  const response = await fetch(`/api/data/${input.id}`)
  return response.json()
})

const machine = setup({
  actors: {
    fetchData,
  },
  actions: {
    setData: assign({ data: ({ event }) => event.output }),
    setError: assign({ error: ({ event }) => event.error }),
  },
}).createMachine({
  id: 'dataLoader',
  initial: 'idle',
  context: { id: '', data: null, error: null },
  states: {
    idle: {
      on: { FETCH: 'loading' },
    },
    loading: {
      invoke: {
        src: 'fetchData',
        input: ({ context }) => ({ id: context.id }),
        onDone: {
          target: 'success',
          actions: 'setData',
        },
        onError: {
          target: 'failure',
          actions: 'setError',
        },
      },
    },
    success: {},
    failure: {},
  },
})
```

**TMNL Example** — Panel machine (`src/lib/floating/machines/panel-machine.ts`):
```typescript
opening: {
  invoke: {
    src: 'animateOpen',
    input: ({ context }) => ({ panelId: context.targetPanel }),
    onDone: {
      target: 'idle',
      actions: 'clearTargetPanel',
    },
    onError: {
      target: 'idle',
      actions: 'clearTargetPanel',
    },
  },
}
```

---

## Pattern 3: Guards — CONDITIONAL TRANSITIONS

**When:** Transitions should only occur under certain conditions.

```typescript
const dragMachine = setup({
  types: {} as {
    context: { operationId: string | null }
    events: { type: 'START_DRAG' } | { type: 'END_DRAG' }
  },
  guards: {
    hasActiveOperation: ({ context }) => context.operationId !== null,
    noActiveOperation: ({ context }) => context.operationId === null,
  },
}).createMachine({
  id: 'drag',
  initial: 'idle',
  context: { operationId: null },
  states: {
    idle: {
      on: {
        START_DRAG: {
          target: 'dragging',
          guard: 'noActiveOperation',  // Only transition if no drag active
          actions: assign({ operationId: () => crypto.randomUUID() }),
        },
      },
    },
    dragging: {
      on: {
        END_DRAG: {
          target: 'idle',
          guard: 'hasActiveOperation',
          actions: assign({ operationId: null }),
        },
      },
    },
  },
})
```

---

## Pattern 4: stx — TMNL HYBRID PATTERN (XState + Legend-State + effect-atom)

**When:** Need unified state management combining machine shape, reactive data, and Effect operations.

**Architecture** (from `src/lib/stx/ARCHITECTURE.md`):
```
XState (shape/logic)
  ↓
Legend-State (observables/data)
  ↓
effect-atom (Effect bridge)
  ↓
React Components
```

**Factory Pattern** (`src/lib/stx/stx.ts`):
```typescript
import { stx } from '@/lib/stx'
import { dragMachine } from './machines/drag-machine'
import { Effect } from 'effect'

export const dragStx = stx({
  machine: dragMachine,

  // Legend-State observables
  data: {
    currentPosition: { x: 0, y: 0 },
    velocity: { x: 0, y: 0 },
  },

  // Effect-TS programs
  effects: {
    persistState: Effect.gen(function* () {
      // Save to storage
    }),
    trackAnalytics: (event: string) => Effect.gen(function* () {
      // Track event
    }),
  },

  // Derived values (computed from machine + data)
  computed: {
    isDragging: (get) => get.machine.matches('dragging'),
    speed: (get) => Math.sqrt(
      get.data.velocity.x ** 2 + get.data.velocity.y ** 2
    ),
  },

  // Two-way bindings
  bindings: {
    // Sync data changes to machine events
    dataToMachine: {
      'currentPosition': (value) => ({ type: 'POSITION_UPDATE', value }),
    },
    // Sync machine state to data
    machineToData: {
      'idle': () => ({ velocity: { x: 0, y: 0 } }),
    },
  },
})
```

**Usage in React**:
```typescript
import { dragStx } from './drag-stx'

function DragComponent() {
  const { machine, data, computed, effects } = dragStx.use()

  // Read machine state
  const isDragging = computed.isDragging

  // Read Legend-State observable
  const position = data.currentPosition.get()

  // Send machine event
  machine.send({ type: 'START_DRAG' })

  // Run Effect
  await effects.persistState()
}
```

**TMNL Instances**:
- `src/lib/drag/drag-stx.ts` — Drag singleton
- `src/lib/floating/floating-stx.ts` — Floating panel
- `src/lib/ava/atoms/ava-stx.ts` — AVA client

---

## Pattern 5: Effect-Atom Bridge — MACHINE + ATOMS

**When:** Need to expose machine state/operations through effect-atom for React consumption.

```typescript
// src/lib/minibuffer/v2/atoms.ts
import { Atom } from '@effect-atom/atom-react'
import { createActor } from 'xstate'
import { minibufferMachine, type MinibufferActor } from './machine'

// Singleton actor (created once)
const actorRef = createActor(minibufferMachine)
actorRef.start()

// Expose actor via atom
const minibufferActorAtom = Atom.make<MinibufferActor | null>(actorRef)

// Derived state atoms
export const modeAtom = Atom.make((get) => {
  const actor = get(minibufferActorAtom)
  return actor?.getSnapshot().value ?? 'idle'
})

export const inputAtom = Atom.make((get) => {
  const actor = get(minibufferActorAtom)
  return actor?.getSnapshot().context.input ?? ''
})

// Operation atoms (trigger events)
export const openCommandOp = runtimeAtom.fn<ProviderId>()((providerId, ctx) =>
  Effect.gen(function* () {
    const actor = Atom.get(minibufferActorAtom)
    actor?.send({ type: 'OPEN_COMMAND', providerId })
  })
)

export const submitOp = runtimeAtom.fn()((_, ctx) =>
  Effect.gen(function* () {
    const actor = Atom.get(minibufferActorAtom)
    actor?.send({ type: 'SUBMIT' })
  })
)
```

**React Usage**:
```typescript
function CommandPalette() {
  const mode = useAtomValue(modeAtom)
  const input = useAtomValue(inputAtom)
  const openCommand = useSetAtom(openCommandOp)
  const submit = useSetAtom(submitOp)

  // ...
}
```

---

## Pattern 6: Testing XState Machines

**When:** Writing unit tests for machine transitions.

### Pure Transition Tests

```typescript
// src/lib/minibuffer/v2/__tests__/machine.test.ts
import { describe, it, expect } from 'vitest'
import { createActor } from 'xstate'
import { minibufferMachine } from '../machine'

describe('minibufferMachine', () => {
  it('starts in idle state', () => {
    const actor = createActor(minibufferMachine)
    actor.start()
    expect(actor.getSnapshot().value).toBe('idle')
    actor.stop()
  })

  it('transitions to prompt on OPEN_PROMPT', () => {
    const actor = createActor(minibufferMachine)
    actor.start()
    actor.send({ type: 'OPEN_PROMPT', prompt: 'Enter name: ' })
    expect(actor.getSnapshot().value).toBe('prompt')
    expect(actor.getSnapshot().context.prompt).toBe('Enter name: ')
    actor.stop()
  })

  it('respects guards', () => {
    const actor = createActor(minibufferMachine)
    actor.start()
    // Send event that guard should block
    actor.send({ type: 'SELECT_NEXT' })  // No completions
    expect(actor.getSnapshot().value).toBe('idle')  // Didn't transition
    actor.stop()
  })
})
```

### Async Actor Tests with waitFor

```typescript
import { createActor, waitFor } from 'xstate'

it('handles async invoke', async () => {
  const actor = createActor(dataLoaderMachine)
  actor.start()

  actor.send({ type: 'FETCH' })

  // Wait for state transition
  await waitFor(actor, (snapshot) =>
    snapshot.matches('success') || snapshot.matches('failure')
  )

  expect(actor.getSnapshot().value).toBe('success')
  expect(actor.getSnapshot().context.data).toBeDefined()
  actor.stop()
})
```

---

## Anti-Patterns

### 1. Actors in Context

```typescript
// WRONG — Actors aren't serializable
context: {
  childActor: spawn(childMachine),  // Bad!
}

// CORRECT — Store actor ID, use actorRef map
context: {
  childActorId: 'child-1',
}
// Access via actor.system.get('child-1')
```

### 2. Blocking Effect Operations in Actions

```typescript
// WRONG — Actions should be synchronous
actions: {
  saveToDb: () => {
    Effect.runSync(saveEffect)  // Blocks!
  }
}

// CORRECT — Use invoke for async
states: {
  saving: {
    invoke: {
      src: fromPromise(() => Effect.runPromise(saveEffect)),
      onDone: 'saved',
    }
  }
}
```

### 3. Observable Values in Context

```typescript
// WRONG — Context is pure data, not observables
context: {
  position$: observable.box({ x: 0, y: 0 }),  // Bad!
}

// CORRECT — Use stx bindings for Legend-State integration
const myStx = stx({
  machine: myMachine,
  data: { position: { x: 0, y: 0 } },  // Legend-State
  bindings: { /* sync */ },
})
```

### 4. Guards That Don't Constrain

```typescript
// WRONG — Guard always returns true
guards: {
  alwaysTrue: () => true,  // Why have it?
}

// CORRECT — Guards enforce constraints
guards: {
  noActiveOperation: ({ context }) => context.operationId === null,
}
```

---

## Decision Tree: When to Use XState

```
Need lifecycle state management?
│
├─ Simple toggle/flag?
│  └─ Use: useState or Atom.make (simpler)
│
├─ Multiple states with defined transitions?
│  ├─ Async operations (invoke)?
│  │  └─ Use: XState with fromPromise actors
│  ├─ Need Legend-State integration?
│  │  └─ Use: stx hybrid pattern
│  └─ Pure state machine?
│     └─ Use: setup().createMachine()
│
└─ Complex UI mode (command palette, drawer)?
   └─ Use: XState + effect-atom bridge
```

---

## File Locations Summary

| Component | File | Purpose |
|-----------|------|---------|
| **Minibuffer machine** | `src/lib/minibuffer/v2/machine.ts` | Command palette lifecycle |
| **Minibuffer atoms** | `src/lib/minibuffer/v2/atoms.ts` | Effect-atom bridge |
| **Minibuffer tests** | `src/lib/minibuffer/v2/__tests__/machine.test.ts` | Test patterns |
| **Drag machine** | `src/lib/drag/machines/drag-machine.ts` | Drag orchestration |
| **Panel machine** | `src/lib/floating/machines/panel-machine.ts` | Panel lifecycle |
| **Animation machine** | `src/lib/animation/v2/machine.ts` | Animation state flow |
| **STX factory** | `src/lib/stx/stx.ts` | Hybrid pattern factory |
| **STX architecture** | `src/lib/stx/ARCHITECTURE.md` | Design documentation |
| **STX test patterns** | `src/lib/stx/__tests__/TEST_PATTERNS.md` | Test guidance |

---

## Integration Points

- **effect-atom-integration** — Atom bridge patterns
- **effect-patterns** — Service patterns (when stx uses Effect operations)
- **tmnl-testbed-patterns** — Testbed validation with machine state
- **ux-interaction-patterns** — UI state management
