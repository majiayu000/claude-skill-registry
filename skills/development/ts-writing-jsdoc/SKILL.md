---
name: writing-jsdoc
description: This skill should be used when the user asks to "add JSDoc", "document this function", "write JSDoc comments", "link to a type", "use @link tag", "hyperlink in JSDoc", "reference external service in docs", or needs guidance on JSDoc syntax, clickable type references, or TypeScript-optimized documentation.
---

# Writing JSDoc

TypeScript-optimized JSDoc documentation guidance. TypeScript provides types; JSDoc provides meaning.

## CRITICAL: No Type Repetition

TypeScript already has complete type information. Never duplicate it in JSDoc.

```typescript
// ❌ BAD - Redundant type information
/**
 * @param {string} name - The user's name
 * @param {number} age - The user's age
 * @returns {boolean} Whether the user is valid
 */
function isValidUser(name: string, age: number): boolean { ... }

// ✅ GOOD - Description only, types come from TS
/**
 * Validates user meets minimum requirements.
 * @param name - Display name (must be non-empty)
 * @param age - Must be 13 or older
 */
function isValidUser(name: string, age: number): boolean { ... }
```

__Forbidden in TS projects:__

| Tag               | Why Forbidden                |
| ----------------- | ---------------------------- |
| `@type`           | TS has the type              |
| `@param {Type}`   | TS has param types           |
| `@returns {Type}` | TS has return type           |
| `@typedef`        | Use TS `type` or `interface` |
| `@callback`       | Use TS function types        |

## What to Document

Document what TypeScript cannot express:

| Document           | Example                                     |
| ------------------ | ------------------------------------------- |
| __Purpose/intent__ | "Validates user meets minimum requirements" |
| __Constraints__    | "Must be non-empty", "Range: 0-100"         |
| __Side effects__   | "Writes to localStorage", "Mutates input"   |
| __Exceptions__     | `@throws` - TS doesn't track thrown errors  |
| __Defaults__       | `@default` - Runtime default values         |
| __Examples__       | `@example` - Usage patterns                 |
| __Deprecation__    | `@deprecated` - Migration guidance          |
| __External refs__  | `@see` - Links to docs, specs               |

## What NOT to Document

Skip JSDoc entirely for:

* __Self-evident code__ - `getName()` returning a name needs no docs
* __Internal helpers__ - Private functions used in one place
* __Type-only exports__ - Types are self-documenting
* __Trivial getters/setters__ - `get id() { return this._id; }`

## JSDoc Placement Rules

### DON'T Add JSDoc To

* Namespace exports (`export * as Name`)
* Barrel exports (`export * from './foo'`)
* Re-exports
* Implementations that inherit documentation from their interface/type
* Multiple JSDoc blocks for the same declaration (only closest one is effective)

### Avoid Duplicate JSDoc

If a const implements an interface with JSDoc, don't repeat it on the const:

```typescript
/** Creates a user validator. */
interface UserValidator {
  validate(user: User): boolean;
}

// ❌ BAD - Duplicates interface JSDoc
/** Creates a user validator. */
const validator: UserValidator = { ... };

// ✅ GOOD - Interface JSDoc is inherited
const validator: UserValidator = { ... };
```

### Namespace Export Hack

For `export * as Name`, use `@ts-expect-error` with duplicate namespace to add docs:

```typescript
// @ts-expect-error Duplicate identifier
export * as Utils from './utils'
/** Utility functions for string manipulation. */
export namespace Utils {}
```

## Useful Tags for TypeScript

### `@throws`

TypeScript doesn't track exceptions. Document them:

```typescript
/**
 * Parses JSON configuration file.
 * @throws {SyntaxError} If JSON is malformed
 * @throws {Error} If file doesn't exist
 */
function parseConfig(path: string): Config { ... }
```

### `@example`

Show usage patterns, especially for complex APIs:

```typescript
/**
 * Creates a debounced version of a function.
 * @example
 * const debouncedSave = debounce(save, 300);
 * input.addEventListener('change', debouncedSave);
 */
function debounce<T extends (...args: any[]) => any>(fn: T, ms: number): T { ... }
```

### `@default`

Document runtime defaults (complements TS default params):

```typescript
interface Options {
  /** @default 3000 */
  timeout?: number
  /** @default 'warn' */
  logLevel?: 'debug' | 'info' | 'warn' | 'error'
}
```

### `@deprecated`

Always include migration path:

```typescript
/**
 * @deprecated Use {@link createUser} instead. Will be removed in v3.0.
 */
function addUser(name: string): User { ... }
```

### `@typeParam` - Use Sparingly

Only document type parameters users explicitly provide:

```typescript
// ✅ Document - user explicitly provides type
/**
 * Creates a type-safe event emitter.
 * @typeParam Events - Map of event names to payload types
 * @example
 * const emitter = createEmitter<{ click: MouseEvent; key: KeyboardEvent }>();
 */
function createEmitter<
  Events extends Record<string, unknown>,
>(): Emitter<Events>

// ❌ Don't document - type is inferred from arguments
/**
 * Returns first element of array.
 */
function first<T>(arr: T[]): T | undefined
```

## The `{@link}` Tag

Create clickable references to types, functions, and identifiers.

### Syntax

```typescript
/** Composes {@link RhythmMediaPlayPauseButton} and {@link RhythmMediaTimeDisplay}. */

/** Returns result from {@link audiosByPriority | the priority list}. */
```

### Import Requirement

For `{@link Identifier}` to be clickable, the identifier must be in scope:

| Scenario         | Clickable?      |
| ---------------- | --------------- |
| Same file export | Yes             |
| Imported type    | Yes             |
| Not imported     | No (plain text) |

### JSDoc-Only Imports

When a type is needed only for `{@link}`, use underscore prefix to avoid lint errors:

```typescript
// For JSDoc {@link} only
import type { MuxAsset as _MuxAsset } from '@heartbeat/types';

/**
 * Uploads audio to {@link _MuxAsset | Mux} for transcoding.
 */
export const uploadVoiceNote = async (blob: Blob) => { ... };
```

## External Links

### `@see` for Reference Docs

```typescript
/**
 * Type-safe predicates for DOMException error types.
 * @see https://developer.mozilla.org/en-US/docs/Web/API/DOMException
 */
```

### Markdown for Inline Links

```typescript
/**
 * Uploads audio to [Mux](https://www.mux.com/) for transcoding.
 */
```

## Quick Reference

| Use Case           | Syntax                               |
| ------------------ | ------------------------------------ |
| Link to identifier | `{@link Identifier}`                 |
| Link with text     | `{@link Identifier \| display text}` |
| External docs      | `@see https://...`                   |
| Inline link        | `[Text](https://...)`                |
| Exception          | `@throws {ErrorType} Description`    |
| Example            | `@example` + code block              |
| Default value      | `@default value`                     |
| Deprecation        | `@deprecated Use X instead`          |
| JSDoc-only import  | `import type { X as _X }`            |

## Notes

* TypeScript provides types; JSDoc provides meaning and context
* `{@link}` requires identifier in scope (imported or same file)
* Underscore-prefixed imports avoid unused-vars lint errors
* Links render as clickable in VSCode, Zed, and modern IDEs
* Focus on what TS cannot express: intent, constraints, exceptions
* See `limitations.md` for known TypeScript/IDE limitations
