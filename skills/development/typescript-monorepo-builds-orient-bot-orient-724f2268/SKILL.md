---
name: typescript-monorepo-builds
description: Configure TypeScript for the Orient monorepo packages. Use when creating new packages, fixing build errors, configuring tsconfig.json, setting up project references, or debugging "cannot find module" errors. Covers package tsconfig templates, turbo build order, path aliases, and common build errors.
---

# TypeScript Monorepo Builds

## Quick Reference

```bash
# Build all packages (respects dependency order)
pnpm turbo build

# Build specific package and its dependencies
pnpm --filter @orient/package-name... build

# Type check without building
pnpm turbo typecheck

# Clean all build artifacts
pnpm turbo clean
```

## Package tsconfig.json Template

Every package in `packages/` should have this configuration:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist", "__tests__"]
}
```

### Key Options Explained

| Option             | Value      | Purpose                                |
| ------------------ | ---------- | -------------------------------------- |
| `module`           | `NodeNext` | ESM-compatible module system           |
| `moduleResolution` | `NodeNext` | Matches Node.js module resolution      |
| `declaration`      | `true`     | Generate `.d.ts` type files            |
| `declarationMap`   | `true`     | Enable Go-to-Definition for consumers  |
| `isolatedModules`  | `true`     | Required for esbuild/swc compatibility |

## Project References (For Cross-Package Imports)

When a package imports from another package at compile time, add project references:

```json
{
  "compilerOptions": {
    "composite": true
  },
  "references": [{ "path": "../core" }, { "path": "../database" }]
}
```

**Note**: Project references require `composite: true` in the **referenced** package's tsconfig.

### When to Use References

- ✅ Package directly imports types from another package
- ✅ Package uses workspace dependency (`"@orient/core": "workspace:*"`)
- ❌ Package only uses runtime exports (no compile-time dependency)

## Build Order with Turbo

Turbo automatically builds dependencies first via `dependsOn: ["^build"]`:

```json
// turbo.json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    }
  }
}
```

### Build Order

```
1. @orient/core (no dependencies)
2. @orient/database (depends on core)
3. @orient/database-services (depends on database)
4. @orient/integrations (depends on core, database)
5. @orient/agents (depends on database-services)
6. @orient/mcp-tools (depends on agents, integrations)
7. @orient/bot-* (depends on mcp-tools, agents)
```

## Root tsconfig.json Path Aliases

The root `tsconfig.json` defines path aliases for development:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@orient/core": ["./packages/core/src/index"],
      "@orient/database": ["./packages/database/src/index"],
      "@orient/agents": ["./packages/agents/src/index"]
    }
  }
}
```

**Important**: Path aliases point to **source** files for development, but production builds use **dist** via package.json exports.

## Incremental Compilation Troubleshooting

### Stale .tsbuildinfo Files

**Symptom**: Build completes with no errors but dist/ is empty. Turbo shows "cache hit" or warns "no output files found."

**Cause**: `.tsbuildinfo` stores incremental state. When stale, tsc skips compilation entirely.

**Fix**:

```bash
find packages -name "*.tsbuildinfo" -delete
rm -f .tsbuildinfo
pnpm run build:packages
```

### Verifying Build Completion

**Always verify dist/ before running dependent builds or tests:**

```bash
# After build, verify all packages have dist/index.js
ls packages/*/dist/index.js

# If any are missing, that package didn't compile
# Check for stale tsbuildinfo or stray .js files in src/
```

### Empty dist/ Despite "Cache Hit"

Turbo's cache can be misleading when tsbuildinfo is stale:

1. Turbo checks its cache → finds cached task
2. Replays cached tsc (which produced no output due to stale tsbuildinfo)
3. Result: "cache hit" but empty dist/

**Fix**: Clean both turbo cache AND tsbuildinfo:

```bash
rm -rf .turbo packages/*/.turbo
find packages -name "*.tsbuildinfo" -delete
pnpm run build:packages
```

## Common Build Errors

### "Cannot find module '@orient/package'" (TS2307)

**Most common cause**: Prerequisite package didn't build (empty dist/).

1. Verify prerequisite dist exists: `ls packages/package/dist/index.js`
2. If empty, clean tsbuildinfo and rebuild: `find packages -name "*.tsbuildinfo" -delete && pnpm run build:packages`
3. If still failing, check package.json exports match dist structure

### "Type 'X' is not assignable to type 'Y'"

Cross-package type mismatches usually mean:

1. **Stale build**: Run `pnpm turbo build --force`
2. **Different TypeScript versions**: Check `peerDependencies`
3. **Missing type export**: Add to package's `index.ts`

### "Cannot find name 'X'" in tests

Tests don't use project references. Add vitest path aliases:

```typescript
// vitest.config.ts
export default defineConfig({
  resolve: {
    alias: {
      '@orient/core': resolve(__dirname, '../core/src'),
    },
  },
});
```

### "Declaration emit skipped"

```
error TS5069: Option 'declarationDir' cannot be specified
```

Ensure `outDir` is set and remove `declarationDir`:

```json
{
  "compilerOptions": {
    "outDir": "./dist",
    "declaration": true
  }
}
```

### Circular Reference Error

```
error TS6202: Project references may not form a circular graph
```

Check `references` in tsconfig files. Package A cannot reference B if B references A.

## Creating a New Package

1. Create package structure:

   ```bash
   mkdir -p packages/new-package/src
   ```

2. Create `package.json`:

   ```json
   {
     "name": "@orient/new-package",
     "version": "1.0.0",
     "type": "module",
     "main": "./dist/index.js",
     "types": "./dist/index.d.ts",
     "exports": {
       ".": {
         "types": "./dist/index.d.ts",
         "import": "./dist/index.js"
       }
     },
     "scripts": {
       "build": "tsc",
       "typecheck": "tsc --noEmit"
     }
   }
   ```

3. Create `tsconfig.json` using the template above

4. Add workspace dependency to consumers:

   ```json
   {
     "dependencies": {
       "@orient/new-package": "workspace:*"
     }
   }
   ```

5. Add path alias to root `tsconfig.json`

6. Build: `pnpm --filter @orient/new-package build`

## Debugging Build Issues

```bash
# Verbose TypeScript output
pnpm --filter @orient/package tsc --listFiles

# Check what files are included
pnpm --filter @orient/package tsc --listFilesOnly

# Trace module resolution
pnpm --filter @orient/package tsc --traceResolution

# Show build dependency graph
pnpm turbo build --graph

# Force rebuild ignoring cache
pnpm turbo build --force
```

## Best Practices

1. **Keep packages focused** - smaller packages = faster builds
2. **Use `composite: true`** only when needed for references
3. **Build before testing** - `dependsOn: ["^build"]` in turbo.json
4. **Export types explicitly** - `export type { X }` in barrel files
5. **Match exports to dist** - package.json exports must match dist structure
