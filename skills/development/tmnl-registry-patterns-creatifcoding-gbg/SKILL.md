---
name: tmnl-registry-patterns
description: Singleton registries (overlayRegistry), atom registries, command registries. Registry subscription vs useAtomValue patterns.
triggers:
  - "registry"
  - "singleton registry"
  - "atom registry"
  - "registry pattern"
---

# TMNL Registry Patterns

Canonical patterns for creating and using singleton registries in TMNL, with emphasis on effect-atom integration.

## Overview

Registries provide centralized state management and lookup services for:
- Overlay system state (`overlayRegistry`)
- Token-based registries (binding sources, scopes)
- Kernel registries (data-manager drivers)
- Command registries (command execution and keybindings)

**Key Distinction**: Registry subscription (`registry.subscribe()`) vs. atom consumption (`useAtomValue()`).

## Canonical Sources

**Primary Files**:
- `src/lib/overlays/atoms/index.ts` - Global singleton registry pattern
- `src/lib/overlays/services/OverlayRegistry.ts` - Effect.Service registry (deprecated in favor of atoms)
- `src/lib/hotkeys/BindingSourceRegistry.ts` - TokenRegistry-backed registry
- `src/lib/primitives/TokenRegistry/TokenRegistry.ts` - Generic token registry factory
- `src/lib/commands/service.ts` - Command registry with atom bindings

**Reference Implementations**:
- `src/lib/data-manager/v2/KernelRegistry.ts` - Kernel registry pattern
- `src/lib/minibuffer/v2/providers.ts` - Provider registry pattern

## Patterns

### 1. Global Singleton Registry (Atom-Based)

**Pattern**: Single shared `Registry.make()` instance for global state mutations.

**When to Use**:
- State shared across entire application
- React components AND imperative operations need access
- Mutations must be synchronous and atomic

**Implementation** (from `src/lib/overlays/atoms/index.ts`):

```tsx
import { Registry, RegistryContext, Atom } from "@effect-atom/atom-react"
import * as React from "react"

// ─────────────────────────────────────────────────────────────
// Global Registry Singleton
// ─────────────────────────────────────────────────────────────

/**
 * Global registry singleton for overlay state mutations.
 * This is shared across all overlay operations AND React components.
 * Components should use OverlayRegistryProvider to inject this registry.
 */
export const overlayRegistry = Registry.make()

// ─────────────────────────────────────────────────────────────
// State Atoms (Source of Truth)
// ─────────────────────────────────────────────────────────────

export const containersStateAtom = Atom.make<Map<ContainerId, ContainerState>>(
  new Map()
)

// Derived atoms
export const containerIdsAtom = Atom.make((get) => {
  const state = get(containersStateAtom)
  return Array.from(state.keys())
})

// ─────────────────────────────────────────────────────────────
// Mutation Operations (Direct Atom Updates)
// ─────────────────────────────────────────────────────────────

export const containerOps = {
  /**
   * Create a container. Mutates state synchronously via registry.update().
   */
  create: (containerId: ContainerId) => {
    overlayRegistry.update(containersStateAtom, (current) =>
      createContainer(current, containerId)
    )
  },

  destroy: (containerId: ContainerId) => {
    overlayRegistry.update(containersStateAtom, (current) =>
      destroyContainer(current, containerId)
    )
  },
}

// ─────────────────────────────────────────────────────────────
// React Provider (Injects Registry into Context)
// ─────────────────────────────────────────────────────────────

/**
 * Provider that injects the shared overlayRegistry into React context.
 * Wrap your app (or overlay-using subtree) with this provider to ensure
 * React components and imperative operations share the same registry.
 */
export function OverlayRegistryProvider({ children }: { children: React.ReactNode }) {
  return React.createElement(RegistryContext.Provider, { value: overlayRegistry }, children)
}
```

**Usage in React Components**:

```tsx
import { useAtomValue } from "@effect-atom/atom-react"
import { containerIdsAtom, containerOps } from "@/lib/overlays/atoms"

function MyComponent() {
  // Subscribe to atom via registry context (from OverlayRegistryProvider)
  const containerIds = useAtomValue(containerIdsAtom)

  // Mutate via operations
  const createContainer = () => {
    containerOps.create("my-container")
  }

  return <div>Containers: {containerIds.length}</div>
}
```

**Usage Outside React** (imperative):

```tsx
import { overlayRegistry, containerOps, containerIdsAtom } from "@/lib/overlays/atoms"

// Direct mutation (synchronous)
containerOps.create("my-container")

// Read current state
const currentIds = overlayRegistry.get(containerIdsAtom)
console.log("Container IDs:", currentIds)

// Subscribe to changes
const unsub = overlayRegistry.subscribe(containerIdsAtom, (ids) => {
  console.log("Container IDs changed:", ids)
})
```

**Key Insight**: `registry.update()` triggers React re-renders via `useAtomValue()` subscriptions.

### 2. TokenRegistry Pattern (Validated Singleton)

**Pattern**: Generic registry for branded token types with validation and metadata.

**When to Use**:
- Fixed set of valid tokens (binding sources, scopes, etc.)
- Need compile-time and runtime validation
- Token metadata (priority, overwritability, etc.)

**Implementation** (from `src/lib/hotkeys/BindingSourceRegistry.ts`):

```tsx
import { TokenRegistry } from "@/lib/primitives/TokenRegistry"
import type { Token } from "@/lib/primitives/TokenRegistry"

// ─────────────────────────────────────────────────────────────
// Metadata
// ─────────────────────────────────────────────────────────────

export interface BindingSourceMetadata {
  readonly priority: number
  readonly overwritable: boolean
}

// ─────────────────────────────────────────────────────────────
// Registry Definition
// ─────────────────────────────────────────────────────────────

export type BindingSourceToken = Token<"binding-source">

export const BindingSourceRegistry = TokenRegistry.create<
  "binding-source",
  BindingSourceMetadata
>({
  identifier: "tmnl/hotkeys/BindingSourceRegistry",
  namespace: "binding-source",
  name: "Binding Sources",
  allowRuntimeRegistration: false, // Fixed set of sources
  allowOverwrite: false,
  defaultMetadata: { priority: 0, overwritable: true },
  builtins: [
    {
      id: "default",
      name: "Default",
      description: "System-provided bindings (lowest priority)",
      metadata: { priority: 0, overwritable: true },
    },
    {
      id: "user",
      name: "User",
      description: "User-configured bindings (highest priority)",
      metadata: { priority: 100, overwritable: false },
    },
  ],
})

// ─────────────────────────────────────────────────────────────
// Convenience Constants
// ─────────────────────────────────────────────────────────────

export const BindingSources = {
  DEFAULT: "default",
  USER: "user",
} as const
```

**Usage**:

```tsx
import { BindingSourceRegistry, BindingSources } from "@/lib/hotkeys/BindingSourceRegistry"

// Type-safe constant access
const binding = {
  keys: ["ctrl+s"],
  commandId: "file.save",
  source: BindingSources.DEFAULT, // ✓ Type-safe
}

// Runtime validation
const token = BindingSourceRegistry.get("user")
if (token) {
  const metadata = BindingSourceRegistry.getMetadata(token)
  console.log("Priority:", metadata?.priority) // 100
}

// Invalid source caught at runtime
const invalid = BindingSourceRegistry.get("builtin") // undefined (not registered)
```

**Key Feature**: Prevents invalid strings like `'builtin'` from slipping through via compile-time types.

### 3. Effect.Service Registry (Deprecated Pattern)

**DEPRECATED**: Use atom-based registries instead.

**Why Deprecated**:
- Layer-per-operation isolation causes state fragmentation
- `Effect.Ref` inside services creates fresh state on each operation
- Atoms provide better React integration and single source of truth

**Old Pattern** (from `src/lib/overlays/services/OverlayRegistry.ts`):

```tsx
import * as Context from "effect/Context"
import * as Effect from "effect/Effect"
import * as Layer from "effect/Layer"
import * as Ref from "effect/Ref"

export class OverlayRegistry extends Context.Tag("tmnl/overlays/OverlayRegistry")<
  OverlayRegistry,
  OverlayRegistryOps
>() {
  static Default = Layer.effect(
    OverlayRegistry,
    Effect.gen(function* () {
      // State: Map of ContainerId -> ContainerState
      const containersRef = yield* Ref.make<Map<ContainerId, ContainerState>>(new Map())

      return OverlayRegistry.of({
        createContainer: (id) =>
          Ref.update(containersRef, (map) => {
            // ... mutation logic
          }),
        // ... other operations
      })
    })
  )
}
```

**Problem**:
```tsx
// Each runtimeAtom.fn() call CAN create a new service instance
const ops = {
  create: runtimeAtom.fn((id) => /* uses OverlayRegistry with fresh Ref */),
  destroy: runtimeAtom.fn((id) => /* different OverlayRegistry instance? */),
}
```

**Fix**: Use atoms as source of truth (Pattern 1).

### 4. Kernel Registry Pattern (Namespaced)

**Pattern**: Registry for managing multiple driver instances (e.g., search kernels).

**When to Use**:
- Multiple instances of same service type
- Need namespace isolation (different containers, features, etc.)
- Per-instance lifecycle management

**Implementation** (from `src/lib/data-manager/v2/KernelRegistry.ts`):

```tsx
import { Effect, Ref, HashMap } from "effect"

export class KernelRegistry {
  static make = <K extends KernelType>(): Effect.Effect<KernelRegistryOps<K>> =>
    Effect.gen(function* () {
      const kernelsRef = yield* Ref.make<HashMap.HashMap<string, KernelInstance<K>>>(
        HashMap.empty()
      )

      return {
        register: (id: string, kernel: KernelInstance<K>) =>
          Ref.update(kernelsRef, (map) => HashMap.set(map, id, kernel)),

        get: (id: string) =>
          Effect.map(Ref.get(kernelsRef), (map) => HashMap.get(map, id)),

        unregister: (id: string) =>
          Ref.update(kernelsRef, (map) => HashMap.remove(map, id)),

        list: () =>
          Effect.map(Ref.get(kernelsRef), (map) => Array.from(HashMap.keys(map))),
      }
    })
}
```

**Usage**:

```tsx
import { KernelRegistry } from "@/lib/data-manager/v2/KernelRegistry"

const program = Effect.gen(function* () {
  const registry = yield* KernelRegistry.make()

  // Register kernel
  yield* registry.register("search-1", myKernelInstance)

  // Retrieve kernel
  const kernel = yield* registry.get("search-1")

  // Cleanup
  yield* registry.unregister("search-1")
})
```

**Key Feature**: Each registry instance is scoped to a specific context (e.g., container, feature).

### 5. Registry Subscription vs useAtomValue

**Critical Distinction**:
- **Registry subscription**: Imperative, outside React
- **useAtomValue**: Reactive, inside React components

**Registry Subscription** (imperative):

```tsx
import { overlayRegistry, containerIdsAtom } from "@/lib/overlays/atoms"

// Subscribe outside React
const unsub = overlayRegistry.subscribe(containerIdsAtom, (ids) => {
  console.log("Container IDs changed:", ids)
})

// Cleanup
unsub()
```

**useAtomValue** (React):

```tsx
import { useAtomValue } from "@effect-atom/atom-react"
import { containerIdsAtom } from "@/lib/overlays/atoms"

function MyComponent() {
  // Automatically subscribes and unsubscribes
  const containerIds = useAtomValue(containerIdsAtom)

  return <div>Containers: {containerIds.length}</div>
}
```

**When to Use Each**:
- **Registry subscription**: Background services, logging, analytics
- **useAtomValue**: React component rendering, derived UI state

### 6. Provider Injection Pattern

**Pattern**: Inject global registry into React context to ensure components and imperative code share state.

**Implementation**:

```tsx
import { RegistryContext } from "@effect-atom/atom-react"

export function OverlayRegistryProvider({ children }: { children: React.ReactNode }) {
  return React.createElement(RegistryContext.Provider, { value: overlayRegistry }, children)
}
```

**Usage**:

```tsx
function App() {
  return (
    <OverlayRegistryProvider>
      <MyOverlayComponents />
    </OverlayRegistryProvider>
  )
}
```

**Why Needed**: Without provider, `useAtomValue()` won't find the registry context and will fail.

## Examples

### Example 1: Global Registry with Mutations

```tsx
// atoms/index.ts
import { Atom, Registry } from "@effect-atom/atom-react"

export const myRegistry = Registry.make()

export const counterAtom = Atom.make(0)

export const counterOps = {
  increment: () => {
    myRegistry.update(counterAtom, (n) => n + 1)
  },
  decrement: () => {
    myRegistry.update(counterAtom, (n) => n - 1)
  },
  reset: () => {
    myRegistry.set(counterAtom, 0)
  },
}

export function MyRegistryProvider({ children }: { children: React.ReactNode }) {
  return React.createElement(RegistryContext.Provider, { value: myRegistry }, children)
}
```

**Component**:

```tsx
import { useAtomValue } from "@effect-atom/atom-react"
import { counterAtom, counterOps } from "./atoms"

function Counter() {
  const count = useAtomValue(counterAtom)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={counterOps.increment}>+</button>
      <button onClick={counterOps.decrement}>-</button>
      <button onClick={counterOps.reset}>Reset</button>
    </div>
  )
}
```

### Example 2: TokenRegistry for Validated IDs

```tsx
// FeatureRegistry.ts
import { TokenRegistry } from "@/lib/primitives/TokenRegistry"

export interface FeatureMetadata {
  readonly enabled: boolean
  readonly version: string
}

export const FeatureRegistry = TokenRegistry.create<"feature", FeatureMetadata>({
  identifier: "tmnl/features/FeatureRegistry",
  namespace: "feature",
  name: "Features",
  allowRuntimeRegistration: true, // Allow dynamic features
  allowOverwrite: false,
  defaultMetadata: { enabled: true, version: "1.0.0" },
  builtins: [
    {
      id: "search",
      name: "Search",
      description: "Search functionality",
      metadata: { enabled: true, version: "2.0.0" },
    },
  ],
})

export const Features = {
  SEARCH: "search",
} as const
```

**Usage**:

```tsx
import { FeatureRegistry, Features } from "./FeatureRegistry"

// Register new feature at runtime
FeatureRegistry.register({
  id: "ai-assistant",
  name: "AI Assistant",
  description: "AI-powered help",
  metadata: { enabled: false, version: "0.1.0" },
})

// Check if feature enabled
const searchToken = FeatureRegistry.get(Features.SEARCH)
const metadata = FeatureRegistry.getMetadata(searchToken!)
console.log("Search enabled:", metadata?.enabled) // true
```

### Example 3: Effect Runtime Atom with Registry

```tsx
import { Atom } from "@effect-atom/atom-react"
import { Layer, Effect } from "effect"
import { MyService } from "./MyService"

// Runtime atom for services that need Effect context
export const myRuntimeAtom = Atom.runtime(MyService.Default)

// Operations that run Effects
export const myOps = {
  doSomething: myRuntimeAtom.fn<{ input: string }>()(({ input }) =>
    Effect.gen(function* () {
      const service = yield* MyService
      return yield* service.process(input)
    })
  ),
}
```

**Usage**:

```tsx
import { myOps } from "./atoms"

// Call from React component or imperative code
const result = await myOps.doSomething({ input: "test" })
```

## Anti-Patterns

### Don't: Create Multiple Registry Instances

```tsx
// ✗ BAD - Each component gets its own registry
function MyComponent() {
  const registry = Registry.make() // New instance every render!
  return <RegistryContext.Provider value={registry}>...</RegistryContext.Provider>
}

// ✓ GOOD - Single global registry
export const globalRegistry = Registry.make()
export function MyProvider({ children }) {
  return <RegistryContext.Provider value={globalRegistry}>{children}</RegistryContext.Provider>
}
```

### Don't: Use Effect.Ref in Services for React State

```tsx
// ✗ BAD - Fresh Ref on each operation
export class MyService extends Context.Tag("MyService")<MyService, MyServiceOps>() {
  static Default = Layer.effect(
    MyService,
    Effect.gen(function* () {
      const stateRef = yield* Ref.make(initialState) // Fresh on each Layer provision
      return { /* operations using stateRef */ }
    })
  )
}

// ✓ GOOD - Use atoms for state
export const myStateAtom = Atom.make(initialState)
export const myOps = {
  update: (value) => myRegistry.set(myStateAtom, value),
}
```

### Don't: Forget Provider Wrapper

```tsx
// ✗ BAD - useAtomValue won't find registry
function App() {
  return <MyComponent /> // No RegistryContext.Provider!
}

// ✓ GOOD - Wrap with provider
function App() {
  return (
    <MyRegistryProvider>
      <MyComponent />
    </MyRegistryProvider>
  )
}
```

### Don't: Mix Registry Instances

```tsx
// ✗ BAD - Mutation uses different registry than subscription
const registryA = Registry.make()
const registryB = Registry.make()

registryA.set(myAtom, "foo") // Set on registryA
const value = registryB.get(myAtom) // Read from registryB (won't see change!)

// ✓ GOOD - Single registry for all operations
const registry = Registry.make()
registry.set(myAtom, "foo")
const value = registry.get(myAtom) // Correct
```

## Quick Reference

**Registry Types**:
- **Global Singleton**: `Registry.make()` exported as module constant
- **TokenRegistry**: `TokenRegistry.create<Namespace, Metadata>(config)`
- **Kernel Registry**: `KernelRegistry.make<K>()` per namespace
- **Effect.Service**: Deprecated, use atoms instead

**Mutation Patterns**:
- `registry.set(atom, value)` - Direct set
- `registry.update(atom, fn)` - Update via function
- `registry.subscribe(atom, callback)` - Imperative subscription

**React Integration**:
- `useAtomValue(atom)` - Subscribe in component
- `RegistryContext.Provider` - Inject registry
- `MyRegistryProvider` - Custom provider wrapper

**When to Use What**:
- **Global state across app**: Global singleton registry with atoms
- **Validated tokens**: TokenRegistry with branded types
- **Multiple instances**: Kernel registry pattern
- **React state only**: Just atoms with provider (no custom registry needed)
