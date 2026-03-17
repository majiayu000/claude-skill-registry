---
name: creating-libraries
description: This skill should be used when the user asks to "create a library", "scaffold a new lib", "add a local library", "create a namespace module", "set up _.ts and __.ts", or needs to create a new TypeScript library following the _.ts/__.ts namespace pattern. Handles both simple (single file) and complex (barrel) library structures.
---

# Creating Libraries

Scaffold new TypeScript libraries following the namespace module conventions.

## CRITICAL

### Read the Conventions First

Before creating any library, read the appropriate convention documents:

* __Core pattern__: `~/.claude/docs/conventions/namespace-module.md` — The abstract `_.ts`/`__.ts` pattern
* __Local libraries__ (`/src/lib/*`): `~/.claude/docs/conventions/library-local.md`
* __Package libraries__ (package IS the library): `~/.claude/docs/conventions/library-package.md`

### File Naming

* `_.ts` — Namespace module (REQUIRED)
* `__.ts` — Barrel module (only if multiple implementation files)
* `_.test.ts` — Public API tests
* `_.test.fixture.ts` — Shared test fixtures (exports `namespace Fx`)

## Operations

### Create Simple Library (Single Implementation)

Use when library has one implementation file.

__Structure:__

```
src/lib/<name>/
├── _.ts           # export * as Name from './<name>.js'
├── <name>.ts      # Implementation
└── _.test.ts      # Tests
```

__Steps:__

1. Create directory at `src/lib/<name>/` (kebab-case)
2. Create `<name>.ts` with implementation
3. Create `_.ts` with: `export * as <PascalName> from './<name>.js'`
4. Create `_.test.ts` importing from `./_.js`
5. Add to `package.json` imports: `"#<name>": "./build/lib/<name>/_.js"`
6. Add to `tsconfig.json` paths: `"#<name>": ["src/lib/<name>/_.ts"]`

### Create Complex Library (Multiple Files)

Use when library has multiple implementation files.

__Structure:__

```
src/lib/<name>/
├── _.ts           # export * as Name from './__.js'
├── __.ts          # Barrel: exports from all implementation files
├── foo.ts         # Implementation
├── bar.ts         # Implementation
└── _.test.ts      # Tests
```

__Steps:__

1. Create directory at `src/lib/<name>/` (kebab-case)
2. Create implementation files
3. Create `__.ts` with re-exports from all implementation files
4. Create `_.ts` with: `export * as <PascalName> from './__.js'`
5. Create `_.test.ts` importing from `./_.js`
6. Add package.json imports and tsconfig.json paths

## Examples

### Simple Library Example

```typescript
// src/lib/mask/mask.ts
export const create = (pattern: string): Mask => ({ pattern })
export const apply = (mask: Mask, value: string): string => value
export interface Mask {
  pattern: string
}

// src/lib/mask/_.ts
export * as Mask from './mask.js'

// src/lib/mask/_.test.ts
import { Mask } from './_.js'
test('.create', () => {/* ... */})
```

### Complex Library Example

```typescript
// src/lib/parser/tokenizer.ts
export const tokenize = (input: string): Token[] => []

// src/lib/parser/lexer.ts
export const lex = (tokens: Token[]): Lexeme[] => []

// src/lib/parser/__.ts
export { lex, type Lexeme } from './lexer.js'
export { type Token, tokenize } from './tokenizer.js'

// src/lib/parser/_.ts
export * as Parser from './__.js'
```

## Reference

### Naming Conventions

| Element   | Case       | Example     |
| --------- | ---------- | ----------- |
| Directory | kebab-case | `my-lib/`   |
| Files     | kebab-case | `my-lib.ts` |
| Namespace | PascalCase | `MyLib`     |

### Package.json Imports Entry

```json
{
  "imports": {
    "#<name>": "./build/lib/<name>/_.js"
  }
}
```

### TSConfig Paths Entry

```json
{
  "compilerOptions": {
    "paths": {
      "#<name>": ["src/lib/<name>/_.ts"]
    }
  }
}
```

## Notes

* Always use `.js` extension in imports (ESM requirement)
* Namespace name = PascalCase of directory name
* Tests import ONLY from `_.ts`, never from implementation files
* Code modules can import siblings via relative paths
* Cross-library imports use `#<name>` subpath imports
