---
name: creating-adts
description: This skill should be used when the user asks to "create an ADT", "scaffold a discriminated union", "add a tagged union", "create Effect Schema union", or needs to create algebraic data types following the ADT library pattern with proper member files and barrel exports.
---

# Creating ADTs

Scaffold ADT (Algebraic Data Type) unions with discriminated member types.

## CRITICAL

### Read the Conventions First

Before creating any ADT, read the convention documents:

* `~/.claude/docs/conventions/namespace-module.md` — Core `_.ts`/`__.ts` pattern
* `~/.claude/docs/conventions/library-adt.md` — ADT-specific patterns

## Operations

### Create ADT Union

__Structure:__

```
src/lib/<adt-name>/
├── _.ts              # export * as AdtName from './__.js'
├── __.ts             # exports member namespaces + union
├── <adt-name>.ts     # Union definition
├── <member-a>.ts     # Member type
└── <member-b>.ts     # Member type
```

__Steps:__

1. Create directory at `src/lib/<adt-name>/` (kebab-case matching ADT name)
2. Create member files with tagged structs
3. Create union file importing members directly (NOT from `__.ts`)
4. Create `__.ts` exporting members as namespaces + union exports
5. Create `_.ts` pointing to `__.ts`
6. Add package.json imports and tsconfig.json paths

### Member File Pattern (Effect Schema)

```typescript
// <member>.ts
import * as S from 'effect/Schema'

export class MemberName extends S.TaggedClass<MemberName>()('AdtNameMemberName', {
  // fields...
}) {
  static is = S.is(MemberName)
}
```

__Naming Rules:__

* Class name = member name (short, local): `Versioned`
* Tag name = fully qualified: `DocumentVersioned`

### Union File Pattern

```typescript
// <adt-name>.ts
import * as S from 'effect/Schema'
import { MemberA } from './member-a.js' // Direct import, NOT from __.ts
import { MemberB } from './member-b.js'

export const AdtName = S.Union(MemberA, MemberB)
export type AdtName = typeof AdtName.Type
```

### Barrel File Pattern (`__.ts`)

```typescript
// __.ts
export * from './<adt-name>.js'
export * as MemberA from './member-a.js'
export * as MemberB from './member-b.js'
```

## Examples

### LifecycleEvent ADT

```typescript
// added.ts
export class Added extends S.TaggedClass<Added>()('LifecycleEventAdded', {
  schema: SchemaRef,
  revision: Revision,
}) {
  static is = S.is(Added)
}

// removed.ts
export class Removed extends S.TaggedClass<Removed>()('LifecycleEventRemoved', {
  schema: SchemaRef,
  revision: Revision,
}) {
  static is = S.is(Removed)
}

// lifecycle-event.ts
import { Added } from './added.js'
import { Removed } from './removed.js'
export const LifecycleEvent = S.Union(Added, Removed)
export type LifecycleEvent = typeof LifecycleEvent.Type

// __.ts
export * as Added from './added.js'
export * from './lifecycle-event.js'
export * as Removed from './removed.js'

// _.ts
export * as LifecycleEvent from './__.js'
```

### Consumer Usage

```typescript
// Import ONLY from namespace (_.js)
import { LifecycleEvent } from '#lifecycle-event'

// Access members via namespace
const added = LifecycleEvent.Added.make({ schema, revision })
const removed = LifecycleEvent.Removed.make({ schema, revision })

// Type check
if (LifecycleEvent.Added.is(event)) {
  // event is Added
}
```

## Notes

* Union file imports members directly to avoid circular dependencies
* Consumer code imports ONLY from `_.js`, never from `__.js`
* Use `.make()` constructor from tagged classes, never manual object construction
* Tag names should be fully qualified (`AdtNameMemberName`) for global uniqueness
* See convention doc for Simple ADT Pattern (alternative when full structure is overkill)
