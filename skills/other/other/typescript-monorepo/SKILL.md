---
name: typescript-monorepo
description: >-
  Configure TypeScript in a Bun/npm workspaces monorepo with shared base config,
  package-specific overrides, path aliases, and cross-package type sharing.
  Use when setting up tsconfig files, configuring path aliases, resolving
  module errors, or sharing types between packages.
license: MIT
compatibility: [Claude Code]
metadata:
  author: ftcmetrics
  version: "1.0.0"
  category: tools
---

# TypeScript Monorepo Configuration

This guide covers TypeScript configuration patterns for monorepos using Bun/npm workspaces, with examples from the FTC Metrics project structure.

## Project Structure

```
ftcmetrics-v2/
  tsconfig.base.json          # Shared compiler options
  package.json                 # Workspaces: ["packages/*"]
  packages/
    web/                       # Next.js frontend
      tsconfig.json            # Extends base, adds JSX/DOM
    api/                       # Hono API server
      tsconfig.json            # Extends base, adds Node types
    db/                        # Prisma database package
      tsconfig.json            # Extends base
    shared/                    # Shared types and utilities
      tsconfig.json            # Extends base
      src/
        index.ts               # Re-exports all types
        types.ts               # Shared type definitions
```

## Base Configuration

The `tsconfig.base.json` at the workspace root defines shared compiler options:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

### Key Settings Explained

| Option | Value | Purpose |
|--------|-------|---------|
| `target` | ES2022 | Modern JS output with top-level await, class fields |
| `module` | ESNext | Native ESM with dynamic imports |
| `moduleResolution` | bundler | For bundlers (Bun, Vite, Next.js) |
| `strict` | true | Enables all strict type checks |
| `isolatedModules` | true | Required for bundlers/transpilers |
| `skipLibCheck` | true | Faster builds, skip .d.ts checking |
| `declaration` | true | Generate .d.ts for package consumers |
| `declarationMap` | true | Source maps for .d.ts files |

## Package-Specific Configurations

### Web Package (Next.js)

`packages/web/tsconfig.json`:

```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "ES2022"],
    "jsx": "preserve",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    },
    "incremental": true
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**Additions:**
- `lib: ["dom", "dom.iterable"]` - Browser APIs
- `jsx: "preserve"` - Let Next.js handle JSX transformation
- `paths` - Local import aliases (`@/components/...`)
- `plugins` - Next.js TypeScript plugin for route typing

### API Package (Node/Hono)

`packages/api/tsconfig.json`:

```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "types": ["node"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Additions:**
- `types: ["node"]` - Node.js type definitions
- `outDir/rootDir` - Build output configuration

### Shared Package (Types Only)

`packages/shared/tsconfig.json`:

```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Path Aliases

### Local Aliases (Within Package)

For imports within the same package, use `paths` in tsconfig:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/components/*": ["./src/components/*"]
    }
  }
}
```

**Usage:**
```typescript
import { Button } from "@/components/Button";
import { fetchApi } from "@/lib/api";
```

### Cross-Package Imports (Workspace)

For importing from other packages, use workspace dependencies in `package.json`:

```json
{
  "dependencies": {
    "@ftcmetrics/shared": "workspace:*",
    "@ftcmetrics/db": "workspace:*"
  }
}
```

**Usage:**
```typescript
import { Team, ApiResponse } from "@ftcmetrics/shared";
import { prisma } from "@ftcmetrics/db";
```

## Shared Types Pattern

### Structure the Shared Package

`packages/shared/package.json`:
```json
{
  "name": "@ftcmetrics/shared",
  "main": "./src/index.ts",
  "types": "./src/index.ts"
}
```

`packages/shared/src/index.ts`:
```typescript
// Re-export all types
export * from './types';
export * from './constants';
export * from './utils';
```

`packages/shared/src/types.ts`:
```typescript
// Domain types
export type TeamRole = 'mentor' | 'member';
export type SharingLevel = 'private' | 'event' | 'public';

export interface Team {
  id: string;
  teamNumber: number;
  name: string;
  sharingLevel: SharingLevel;
  createdAt: Date;
}

// API response wrapper
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}
```

### Consume Shared Types

```typescript
// In packages/api/src/routes/teams.ts
import type { Team, ApiResponse } from "@ftcmetrics/shared";

function getTeam(id: string): Promise<ApiResponse<Team>> {
  // ...
}
```

## Module Augmentation

Extend third-party types using declaration files:

`packages/web/src/types/next-auth.d.ts`:
```typescript
import { DefaultSession } from "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
    } & DefaultSession["user"];
  }
}
```

## Strict Mode Benefits

The `strict: true` flag enables these checks:

| Flag | What It Catches |
|------|-----------------|
| `strictNullChecks` | Null/undefined access errors |
| `strictFunctionTypes` | Incorrect callback parameter types |
| `strictBindCallApply` | Wrong arguments to bind/call/apply |
| `strictPropertyInitialization` | Uninitialized class properties |
| `noImplicitAny` | Missing type annotations |
| `noImplicitThis` | Ambiguous `this` context |
| `useUnknownInCatchVariables` | Catch variables typed as `unknown` |
| `alwaysStrict` | Emits `"use strict"` in JS output |

## Common Type Errors and Fixes

### 1. Module Not Found

**Error:** `Cannot find module '@ftcmetrics/shared'`

**Fix:** Ensure workspace dependency is added:
```bash
bun add @ftcmetrics/shared@workspace:*
```

### 2. Path Alias Not Resolving

**Error:** `Cannot find module '@/lib/api'`

**Fix:** Ensure `baseUrl` is set when using `paths`:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

### 3. Type Mismatch Across Packages

**Error:** `Type 'import("pkg-a").Team' is not assignable to type 'import("pkg-b").Team'`

**Fix:** Import from the shared package, not duplicate definitions:
```typescript
// Wrong: duplicate type
interface Team { ... }

// Right: import from shared
import type { Team } from "@ftcmetrics/shared";
```

### 4. Declaration File Not Emitting

**Error:** Types not available to consumers

**Fix:** Enable declarations in tsconfig:
```json
{
  "compilerOptions": {
    "declaration": true,
    "declarationMap": true
  }
}
```

### 5. Implicit Any in Catch Blocks

**Error:** `Catch clause variable is of type 'unknown'`

**Fix:** Type-narrow the error:
```typescript
try {
  // ...
} catch (error) {
  if (error instanceof Error) {
    console.error(error.message);
  }
}
```

### 6. Missing DOM Types in Node Package

**Error:** `Cannot find name 'fetch'`

**Fix:** Add to lib or use node-fetch:
```json
{
  "compilerOptions": {
    "lib": ["ES2022", "DOM"]
  }
}
```

Or with Node 18+:
```json
{
  "compilerOptions": {
    "types": ["node"]
  }
}
```

### 7. JSON Import Error

**Error:** `Cannot find module './config.json'`

**Fix:** Enable JSON imports:
```json
{
  "compilerOptions": {
    "resolveJsonModule": true
  }
}
```

## Type Checking Commands

```bash
# Type check all packages
bun run typecheck

# Type check specific package
bun run --filter @ftcmetrics/web typecheck

# Type check with verbose output
tsc --noEmit --pretty
```

## Best Practices

1. **Single Source of Truth**: Define types once in `@ftcmetrics/shared`
2. **Use `type` Imports**: Prefer `import type { }` for type-only imports
3. **Avoid Relative Imports Across Packages**: Use workspace dependencies
4. **Keep Base Config Minimal**: Package-specific settings in package tsconfig
5. **Enable Incremental Builds**: Add `"incremental": true` for faster rebuilds
6. **Exclude Build Outputs**: Always exclude `node_modules`, `dist`, `.next`

## Adding a New Package

1. Create package directory with `src/` folder
2. Create `package.json` with workspace name
3. Create `tsconfig.json` extending base:

```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

4. Add typecheck script:
```json
{
  "scripts": {
    "typecheck": "tsc --noEmit"
  }
}
```

5. If consuming shared types, add dependency:
```json
{
  "dependencies": {
    "@ftcmetrics/shared": "workspace:*"
  }
}
```

## References

- [TypeScript Project References](https://www.typescriptlang.org/docs/handbook/project-references.html)
- [TypeScript Module Resolution](https://www.typescriptlang.org/docs/handbook/modules/theory.html)
- [Bun Workspaces](https://bun.sh/docs/install/workspaces)
