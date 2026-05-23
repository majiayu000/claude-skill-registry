---
name: typescript-expert-2025
description: Expert TypeScript development patterns and tooling for December 2025. Use when (1) Setting up modern TypeScript projects with Bun, Node 22+, or Deno, (2) Configuring tsconfig, ESM/CJS dual publishing, or build tooling, (3) Implementing advanced type patterns like satisfies, as const, template literals, mapped types, (4) Choosing between Biome, Oxlint, or ESLint for linting, (5) Optimizing TypeScript performance, or any expert-level TypeScript architecture questions.
---

# TypeScript Expert Guide - December 2025

## Current Landscape

### TypeScript Versions
| Version | Status | Key Feature |
|---------|--------|-------------|
| **5.7** | Stable | Uninitialized variable detection |
| **5.8** | Stable | `--erasableSyntaxOnly`, `require(esm)` support |
| **5.9** | Current | `import defer`, improved `tsc --init` |
| **7.0** | Preview | Go port (Strada), 10x faster type-checking |

### Runtime Options
| Runtime | TS Support | Speed | Use Case |
|---------|-----------|-------|----------|
| **Node 22+** | Native (strip types) | Baseline | Production, ecosystem compatibility |
| **Bun** | Native | 3x faster | Development, all-in-one toolkit |
| **Deno** | Native | ~Node | Security-first, standard APIs |
| **tsx** | esbuild | Fast | Node + TS quick execution |

### Linting Landscape
| Tool | Speed vs ESLint | Type-Aware | Notes |
|------|-----------------|------------|-------|
| **Biome 2.0** | 20x faster | 85% coverage | All-in-one (lint + format) |
| **Oxlint 1.0** | 50-100x faster | Experimental | Linting only, 520+ rules |
| **ESLint** | Baseline | Full | Most customizable |

## Quick Patterns

### Modern tsconfig.json (TS 5.9+)
```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noEmit": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

### Run TypeScript Directly
```bash
# Node 22+ (native)
node --experimental-strip-types app.ts

# Bun (zero config)
bun app.ts

# tsx (Node + esbuild)
npx tsx app.ts
```

### Type-Safe Object Definition
```typescript
// satisfies: validate type while preserving literal inference
const config = {
  port: 3000,
  env: 'production',
} satisfies { port: number; env: string };
// config.env is 'production', not string

// as const: immutable literals
const routes = ['/', '/api', '/admin'] as const;
// routes[0] is '/', not string
```

### Template Literal Types
```typescript
type EventName = 'click' | 'hover' | 'scroll';
type Handler = `on${Capitalize<EventName>}`;
// 'onClick' | 'onHover' | 'onScroll'

type Route = `/api/${string}/${'get' | 'post'}`;
// '/api/users/get' | '/api/users/post' | ...
```

## Reference Files

Load based on task:

- **TS 5.5-5.9 features & TS 7 preview**: See [typescript-5x-features.md](references/typescript-5x-features.md)
- **Bun, tsx, tsup, Node 22**: See [modern-tooling.md](references/modern-tooling.md)
- **Advanced type patterns**: See [advanced-types.md](references/advanced-types.md)
- **Biome, Oxlint, ESLint**: See [linting-formatting.md](references/linting-formatting.md)
- **tsconfig, package.json, ESM/CJS**: See [project-setup.md](references/project-setup.md)
- **Zod, error handling, async**: See [runtime-patterns.md](references/runtime-patterns.md)

## Build Tool Quick Reference

### tsup (Library Bundling)
```bash
tsup src/index.ts --format esm,cjs --dts
```

### Bun Build
```bash
bun build ./src/index.ts --outdir ./dist --target node
```

### Package Scripts
```json
{
  "scripts": {
    "dev": "bun --watch src/index.ts",
    "build": "tsup src/index.ts --format esm,cjs --dts",
    "lint": "biome check .",
    "typecheck": "tsc --noEmit"
  }
}
```

## Key Compiler Flags (TS 5.8+)

| Flag | Purpose |
|------|---------|
| `--erasableSyntaxOnly` | Enforce type-strippable syntax (no enums, decorators) |
| `--rewriteRelativeImportExtensions` | Rewrite .ts → .js in imports |
| `--isolatedDeclarations` | Parallel .d.ts generation |
| `--noCheck` | Skip type-checking (build only) |
| `--verbatimModuleSyntax` | Enforce explicit type imports |

## Utility Types Quick Reference

```typescript
// Built-in
Partial<T>           // All optional
Required<T>          // All required
Readonly<T>          // All readonly
Pick<T, K>           // Select keys
Omit<T, K>           // Exclude keys
Record<K, V>         // Key-value map
Extract<T, U>        // Filter union
Exclude<T, U>        // Remove from union
NonNullable<T>       // Remove null/undefined
ReturnType<T>        // Function return type
Parameters<T>        // Function parameters
Awaited<T>           // Unwrap Promise

// String manipulation
Uppercase<S>
Lowercase<S>
Capitalize<S>
Uncapitalize<S>
```

## Decision Framework

### Runtime Choice
- **Bun**: New projects, maximum speed, all-in-one
- **Node 22+**: Production, ecosystem compatibility
- **tsx**: Existing Node projects, quick migration

### Linter Choice
- **Biome**: New projects, speed + simplicity
- **Oxlint**: Speed-critical CI, existing ESLint config
- **ESLint**: Complex rules, full type-aware linting

### Build Tool Choice
- **tsup**: Library publishing, ESM/CJS dual
- **Bun build**: Bun-native projects
- **tsc**: Type-checking only (use with bundler)
