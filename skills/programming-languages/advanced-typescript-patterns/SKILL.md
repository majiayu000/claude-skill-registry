---
name: advanced-typescript-patterns
description: Advanced TypeScript patterns for TMNL. Covers conditional types, mapped types, branded types, generic constraints, type inference, and utility type composition. Pure TypeScript patterns beyond Effect Schema.
model_invoked: true
triggers:
  - "conditional type"
  - "mapped type"
  - "infer"
  - "keyof"
  - "Extract"
  - "Exclude"
  - "generic constraint"
  - "branded type"
  - "template literal"
  - "utility type"
---

# Advanced TypeScript Patterns for TMNL

## Overview

TMNL uses sophisticated TypeScript patterns that extend beyond Effect Schema. This skill covers:

1. **Conditional Types** — Type-level branching with `infer`
2. **Mapped Types** — Object transformation with `[K in keyof]`
3. **Branded Types** — Nominal typing for type safety
4. **Generic Constraints** — Cascading bounds and defaults
5. **Pattern Matching** — `Extract<>` for discriminated unions
6. **Utility Composition** — Partial, Readonly, Record, Pick, Omit
7. **Template Literals** — String-level type constraints
8. **Type Decomposition** — Extract types from complex generics

**Scope Distinction:** Effect Schema patterns (Schema.TaggedStruct, Schema.brand) are covered in `effect-schema-mastery`. This skill covers **pure TypeScript** patterns.

---

## Pattern 1: Conditional Types — TYPE-LEVEL BRANCHING

**When:** Selecting types based on structural conditions.

### Basic Conditional Type

```typescript
// If T extends Array, extract element type; otherwise, return T
type UnwrapArray<T> = T extends Array<infer U> ? U : T

type A = UnwrapArray<string[]>    // string
type B = UnwrapArray<number>      // number
```

### Extracting from Complex Generics

**TMNL Example** — EffectResult<T> (`src/lib/stx/types.ts:74-78`):

```typescript
// Extract success/error types from Effect.Effect or Effect-returning function
export type EffectResult<T> = T extends Effect.Effect<infer A, infer E, any>
  ? Result<A, E>
  : T extends (...args: any[]) => Effect.Effect<infer A, infer E, any>
  ? Result<A, E>
  : never

// Usage: Wrap an Effect's types in Result for React consumption
type MyResult = EffectResult<typeof myEffect>
```

**Key insight:** Multiple `infer` clauses can extract different type parameters. Chained conditionals handle different input shapes.

### Distributed Conditional Types

```typescript
// T extends U distributes over unions
type ToArray<T> = T extends unknown ? T[] : never

type C = ToArray<string | number>  // string[] | number[] (NOT (string | number)[])
```

**When to use:** When you want conditional to apply to each union member separately.

### Preventing Distribution

```typescript
// Wrap in tuple to prevent distribution
type ToArrayNonDist<T> = [T] extends [unknown] ? T[] : never

type D = ToArrayNonDist<string | number>  // (string | number)[]
```

---

## Pattern 2: Mapped Types — OBJECT TRANSFORMATION

**When:** Transforming object properties systematically.

### Basic Mapped Type

```typescript
// Make all properties optional
type Optional<T> = { [K in keyof T]?: T[K] }

// Make all properties readonly
type Frozen<T> = { readonly [K in keyof T]: T[K] }
```

### Heterogeneous Property Transformation

**TMNL Example** — Effects mapper (`src/lib/stx/types.ts:155-161`):

```typescript
// Each property transforms based on its source type
readonly effects: {
  [K in keyof TEffects]: TEffects[K] extends (...args: infer Args) => Effect.Effect<infer A, infer E, any>
    ? (...args: Args) => Promise<Result<A, E>>
    : TEffects[K] extends Effect.Effect<infer A, infer E, any>
    ? () => Promise<Result<A, E>>
    : never
}
```

**Breakdown:**
1. `[K in keyof TEffects]` — Iterate over all keys
2. First conditional: If property is a function returning Effect, preserve args
3. Second conditional: If property is an Effect value, make it a zero-arg function
4. `never` fallback: Type error if neither shape matches

### Mapped Types with Property Filtering

```typescript
// Only include string-valued properties
type StringProps<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K]
}

interface Mixed {
  name: string
  age: number
  email: string
}

type OnlyStrings = StringProps<Mixed>  // { name: string; email: string }
```

### Handler Map Polymorphism

**TMNL Example** — OverlayHandlerMap (`src/lib/overlays/Overlay.ts:91-93`):

```typescript
export type OverlayEventTag = 'Open' | 'Close' | 'Toggle' | 'Focus'

export type TypedEventHandler<T extends OverlayEventTag> = (
  event: Extract<OverlayEvent, { _tag: T }>,
  context: OverlayHandlerContext
) => Effect.Effect<HandlerResult>

// Each key maps to a handler for that specific event type
export type OverlayHandlerMap = {
  [K in OverlayEventTag]?: TypedEventHandler<K>
}
```

---

## Pattern 3: Branded Types — NOMINAL TYPING

**When:** Preventing confusion between structurally identical types.

### The Problem

```typescript
type UserId = string
type PostId = string

function getPost(postId: PostId): Post { ... }

const userId: UserId = 'user-123'
getPost(userId)  // Compiles! But semantically wrong
```

### The Solution: Branded Types

```typescript
// Unique symbol for brand discrimination
declare const UserIdBrand: unique symbol
declare const PostIdBrand: unique symbol

type UserId = string & { readonly [UserIdBrand]: typeof UserIdBrand }
type PostId = string & { readonly [PostIdBrand]: typeof PostIdBrand }

// Now this is a compile error:
const userId = 'user-123' as UserId
getPost(userId)  // Error: UserId is not assignable to PostId
```

### Generic Brand Factory

**TMNL Example** — Token<N> (`src/lib/primitives/TokenRegistry/types.ts:26-38`):

```typescript
import { Brand } from 'effect'

// Generic brand factory creates distinct types per namespace
export type Token<N extends string> = string & Brand.Brand<N>

export const TokenSchema = <N extends string>(namespace: N) =>
  Schema.String.pipe(
    Schema.nonEmptyString(),
    Schema.brand(namespace)
  )

// Usage:
type ColorToken = Token<'color'>
type SpacingToken = Token<'spacing'>

const color: ColorToken = 'red-500' as ColorToken
const spacing: SpacingToken = '4' as SpacingToken

// Error: ColorToken not assignable to SpacingToken
const wrong: SpacingToken = color
```

### Registry Enforcement

```typescript
interface TokenRegistry<N extends string> {
  readonly get: (key: string) => Token<N> | undefined
  readonly set: (key: string, value: Token<N>) => void
}

const colorRegistry: TokenRegistry<'color'> = /* ... */
const spacingRegistry: TokenRegistry<'spacing'> = /* ... */

// Type system prevents cross-registry operations
colorRegistry.set('primary', spacingRegistry.get('4')!)  // Error!
```

---

## Pattern 4: Generic Constraints — CASCADING BOUNDS

**When:** Building flexible APIs with type-safe defaults.

### Basic Constraint

```typescript
interface Indexable {
  id: string
}

interface IndexConfig<T extends Indexable> {
  readonly fields: readonly (keyof T)[]
  readonly idField?: keyof T
}

// Usage:
interface User extends Indexable { name: string; email: string }
const config: IndexConfig<User> = {
  fields: ['name', 'email'],  // Autocomplete works!
  idField: 'id'
}
```

### Multi-Parameter Constraints with Cascading

**TMNL Example** — StxConfig (`src/lib/stx/types.ts:34-50`):

```typescript
export interface StxConfig<
  TMachine extends AnyStateMachine | undefined = undefined,
  TData extends object = object,
  TEffects extends EffectsConfig = EffectsConfig,
  TComputed extends ComputedConfig<TData, TMachine> = ComputedConfig<TData, TMachine>,
> {
  readonly machine?: TMachine
  readonly data?: TData
  readonly effects?: TEffects
  readonly computed?: TComputed
  readonly bindings?: BindingsConfig<TData, TMachine>
}
```

**Key patterns:**
1. `= undefined` default allows optional generics
2. Later params can reference earlier ones (`TComputed` uses `TData`, `TMachine`)
3. Constraints flow through composition

### Conditional Property Shape

```typescript
export interface StxGetter<TData extends object, TMachine extends AnyStateMachine | undefined> {
  readonly data: ObservableObject<TData>
  // Property shape depends on generic parameter
  readonly machine: TMachine extends AnyStateMachine
    ? {
        matches: (state: string) => boolean
        snapshot: SnapshotFrom<TMachine>
        context: SnapshotFrom<TMachine>['context']
      }
    : undefined
}
```

---

## Pattern 5: Extract/Exclude — DISCRIMINATED UNION MATCHING

**When:** Type-safe operations on union members.

### Extract Basic Usage

```typescript
type Event =
  | { type: 'click'; x: number; y: number }
  | { type: 'keypress'; key: string }
  | { type: 'scroll'; delta: number }

// Extract members matching a condition
type ClickEvent = Extract<Event, { type: 'click' }>
// { type: 'click'; x: number; y: number }

type InputEvents = Extract<Event, { type: 'click' } | { type: 'keypress' }>
// ClickEvent | KeypressEvent
```

### Exclude Usage

```typescript
// Remove members matching a condition
type NonClickEvents = Exclude<Event, { type: 'click' }>
// { type: 'keypress'; ... } | { type: 'scroll'; ... }
```

### Type-Safe Event Dispatch

**TMNL Example** — TypedEventHandler (`src/lib/overlays/Overlay.ts:85-88`):

```typescript
type OverlayEventTag = 'Open' | 'Close' | 'Toggle' | 'Focus'

type OverlayEvent =
  | { _tag: 'Open'; overlayId: string }
  | { _tag: 'Close'; overlayId: string }
  | { _tag: 'Toggle'; overlayId: string }
  | { _tag: 'Focus'; overlayId: string; element: HTMLElement }

// Handler knows exact event shape based on T
type TypedEventHandler<T extends OverlayEventTag> = (
  event: Extract<OverlayEvent, { _tag: T }>,  // Narrow to specific event
  context: OverlayHandlerContext
) => Effect.Effect<HandlerResult>

// Usage:
const openHandler: TypedEventHandler<'Open'> = (event, ctx) => {
  // event is narrowed to { _tag: 'Open'; overlayId: string }
  console.log(event.overlayId)  // Works!
  // event.element  // Error: 'element' doesn't exist on Open event
}
```

---

## Pattern 6: Utility Type Composition

**When:** Building immutable, constrained object types.

### Composition Patterns

```typescript
// Read-only record with string keys
type ImmutableConfig = Readonly<Record<string, number>>

// Partial version of a record
type OptionalConfig = Partial<Record<'a' | 'b' | 'c', number>>

// Pick specific properties
type Subset = Pick<FullConfig, 'name' | 'version'>

// Omit specific properties
type WithoutSecret = Omit<User, 'password' | 'ssn'>
```

### Component Registry Pattern

**TMNL Example** — CapabilityMap (`src/lib/capabilities/types.ts:140-145`):

```typescript
export interface CapabilityMap {
  position: PositionCapability
  velocity: VelocityCapability
  collision: CollisionCapability
  render: RenderCapability
}

// Indexed access type
export type Component<K extends CapabilityName> = CapabilityMap[K]

// Partial for optional components
export type EntityComponents = Partial<CapabilityMap>

// Usage:
const entity: EntityComponents = {
  position: { x: 0, y: 0 },
  // velocity optional
  render: { visible: true }
}
```

### Deep Readonly

```typescript
type DeepReadonly<T> = T extends (infer U)[]
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T

interface Config {
  db: { host: string; port: number }
  cache: { ttl: number }
}

type FrozenConfig = DeepReadonly<Config>
// All nested properties are readonly
```

---

## Pattern 7: Template Literal Types

**When:** Constraining string values at the type level.

### Basic Template Literal

```typescript
type ColorHex = `#${string}`

const valid: ColorHex = '#ff0000'  // OK
const invalid: ColorHex = 'red'     // Error: Type '"red"' is not assignable
```

**TMNL Example** — ColorValue (`src/lib/animation/v2/types.ts:22`):

```typescript
export type ColorValue = `#${string}`

interface AnimationConfig {
  color?: ColorValue
}
```

### Constrained Template Literals

```typescript
// Hex digits only
type HexDigit = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
  | 'a' | 'b' | 'c' | 'd' | 'e' | 'f'
  | 'A' | 'B' | 'C' | 'D' | 'E' | 'F'

// Two-char hex
type Hex2 = `${HexDigit}${HexDigit}`

// Full hex color
type HexColor = `#${Hex2}${Hex2}${Hex2}`
```

### Event Name Patterns

```typescript
type DomEventName = `on${Capitalize<keyof HTMLElementEventMap>}`
// 'onClick' | 'onMousedown' | 'onKeypress' | ...

type Handler<T extends DomEventName> = T extends `on${infer E}`
  ? (event: HTMLElementEventMap[Uncapitalize<E>]) => void
  : never
```

---

## Pattern 8: Type Decomposition — EXTRACTING FROM GENERICS

**When:** Pulling apart complex composed types.

### Basic Decomposition

```typescript
interface Stx<TMachine, TData, TEffects, TComputed> {
  readonly machine: TMachine
  readonly data: TData
  readonly effects: TEffects
  readonly computed: TComputed
}

// Extract each type parameter
type DataOf<S> = S extends Stx<any, infer D, any, any> ? D : never
type MachineOf<S> = S extends Stx<infer M, any, any, any> ? M : never
type EffectsOf<S> = S extends Stx<any, any, infer E, any> ? E : never
type ComputedOf<S> = S extends Stx<any, any, any, infer C> ? C : never
```

**TMNL Example** (`src/lib/stx/types.ts:262-278`):

```typescript
// Usage in components
const stx = createStx({ data: { count: 0 }, effects: { save: Effect.void } })

type MyData = DataOf<typeof stx>        // { count: number }
type MyEffects = EffectsOf<typeof stx>  // { save: Effect.Effect<void> }
```

### Promise Unwrapping

```typescript
type Awaited<T> = T extends PromiseLike<infer U> ? Awaited<U> : T

type A = Awaited<Promise<string>>              // string
type B = Awaited<Promise<Promise<number>>>     // number (recursive)
```

### Array Element Extraction

```typescript
type ElementOf<T> = T extends ReadonlyArray<infer U> ? U : never

type Items = ElementOf<typeof ['a', 'b', 'c']>  // 'a' | 'b' | 'c'
```

---

## Anti-Patterns

### 1. Overusing `any` in Conditionals

```typescript
// WRONG — any leaks type safety
type Bad<T> = T extends any ? T[] : never

// CORRECT — Use unknown for truly unconstrained
type Good<T> = T extends unknown ? T[] : never
```

### 2. Forgetting Distribution Behavior

```typescript
// WRONG — Expects single output, gets union
type Confused<T> = T extends string ? 'string' : 'other'
type X = Confused<string | number>  // 'string' | 'other', NOT 'other'

// CORRECT — Prevent distribution if needed
type Fixed<T> = [T] extends [string] ? 'string' : 'other'
type Y = Fixed<string | number>  // 'other'
```

### 3. Circular Type References

```typescript
// WRONG — Infinite recursion
type Broken<T> = { value: Broken<T> }  // Error: Type alias circularly references itself

// CORRECT — Use interface for self-reference
interface Node<T> {
  value: T
  children: Node<T>[]  // Allowed with interface
}
```

### 4. Overly Complex Conditional Chains

```typescript
// WRONG — Unreadable, unmaintainable
type Monster<T> = T extends A ? (T extends B ? (T extends C ? D : E) : F) : G

// CORRECT — Break into named helper types
type IsA<T> = T extends A ? true : false
type IsB<T> = T extends B ? true : false
type Resolve<T, A extends boolean, B extends boolean> = ...
```

---

## Decision Tree: Which Pattern to Use

```
Need to transform object properties?
│
├─ Same transformation for all props?
│  └─ Use: Mapped type { [K in keyof T]: Transform<T[K]> }
│
├─ Different transformation per prop?
│  └─ Use: Mapped type with conditional { [K in keyof T]: T[K] extends X ? A : B }
│
├─ Filter/remove some props?
│  └─ Use: as clause { [K in keyof T as Filter<K>]: T[K] }
│
Need to extract types from generics?
│
├─ From Effect/Promise/Array?
│  └─ Use: Conditional with infer (T extends X<infer U> ? U : never)
│
├─ From discriminated union?
│  └─ Use: Extract<Union, { _tag: 'Specific' }>
│
├─ Remove from discriminated union?
│  └─ Use: Exclude<Union, { _tag: 'Remove' }>
│
Need type safety between same structures?
│
└─ Use: Branded types (Brand.Brand<'Name'>)
```

---

## File Locations Summary

| Pattern | File | Lines | Description |
|---------|------|-------|-------------|
| **EffectResult conditional** | `src/lib/stx/types.ts` | 74-78 | Extract from Effect types |
| **Effects heterogeneous map** | `src/lib/stx/types.ts` | 155-161 | Mapped type with conditional |
| **StxConfig cascading** | `src/lib/stx/types.ts` | 34-50 | Multi-param constraints |
| **TypedEventHandler** | `src/lib/overlays/Overlay.ts` | 85-88 | Extract for type-safe dispatch |
| **Token<N> brand factory** | `src/lib/primitives/TokenRegistry/types.ts` | 26-38 | Generic branded types |
| **ColorValue template** | `src/lib/animation/v2/types.ts` | 22 | Template literal |
| **CapabilityMap** | `src/lib/capabilities/types.ts` | 140-145 | Utility composition |
| **IndexConfig<T>** | `src/lib/search/types.ts` | 100-107 | Constrained generic |

---

## Integration Points

- **effect-schema-mastery** — When patterns involve Schema.TaggedStruct, Schema.brand
- **effect-patterns** — When patterns define Effect.Service generic shapes
- **common-conventions** — Naming and file organization for type definitions
- **tmnl-registry-patterns** — Generic registry types with branded keys

