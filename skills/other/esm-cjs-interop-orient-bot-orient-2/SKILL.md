---
name: esm-cjs-interop
description: Handle ESM/CJS module interoperability in the Orient monorepo. Use when encountering import errors, circular dependencies, module resolution issues, or "does not provide an export named" errors. Covers import patterns, re-export strategies, and avoiding circular dependency chains.
---

# ESM/CJS Interoperability

## Quick Reference

```bash
# Check if package is ESM or CJS
grep '"type"' packages/*/package.json

# Find circular dependency issues
npx madge --circular packages/*/src/index.ts
```

## Module System in This Monorepo

This monorepo uses **ESM** (`"type": "module"`) for all packages:

```json
// packages/*/package.json
{
  "type": "module",
  "module": "NodeNext",
  "moduleResolution": "NodeNext"
}
```

However, some legacy code in `src/` may still use CJS patterns, creating interop issues.

## Required: .js Extensions for ESM

ESM requires explicit `.js` extensions in import paths, even for TypeScript files:

```typescript
// ✅ Correct - explicit .js extension
import { loadConfig } from './config/index.js';
import { createLogger } from '@orientbot/core';

// ❌ Wrong - missing extension (works in CJS, fails in ESM)
import { loadConfig } from './config/index';
```

## Common Error: "Does not provide an export named"

This error occurs when CJS modules are re-exported incorrectly in ESM:

```
Error: The requested module '@orientbot/package' does not provide
an export named 'SomeClass'
```

### Solution: Use Default Import + Re-export

```typescript
// ❌ Wrong - doesn't work with CJS modules
export * from './some-cjs-module.js';
export { SomeClass } from './some-cjs-module.js';

// ✅ Correct - use default import first
import SomeCjsModule from './some-cjs-module.js';
export const { SomeClass, someFunction } = SomeCjsModule;

// Or re-export the whole module
export default SomeCjsModule;
```

## Circular Dependency Prevention

Circular dependencies cause runtime failures, especially when ESM and CJS mix.

### Pattern: Circular Dependency Chain

```
@orientbot/mcp-tools
    └── imports @orientbot/agents (to get PromptService)
            └── imports @orientbot/mcp-tools (for tool definitions)
                └── CIRCULAR!
```

### Solution: Import Lower-Level Package

Instead of importing a high-level package that re-exports, import the specific lower-level package:

```typescript
// ❌ Creates circular dependency
import { PromptService } from '@orientbot/agents';

// ✅ Import the actual implementation package
import { MessageDatabase } from '@orientbot/database-services';
// Use MessageDatabase.setSystemPrompt directly
```

### Identifying Circular Dependencies

1. **Build fails with cryptic ESM error** - often circular deps
2. **Import works in tests but fails at runtime** - module loading order differs
3. **"Cannot access before initialization"** - circular import timing issue

### Debug Command

```bash
# Check for circular dependencies
npx madge --circular --extensions ts packages/*/src/index.ts

# Visualize dependency graph
npx madge --image deps.svg packages/mcp-tools/src/index.ts
```

## Package Dependency Direction

Follow this dependency direction to avoid cycles:

```
┌─────────────────────────────────────────────────┐
│              Allowed Import Direction           │
│                                                 │
│  @orientbot/core                                   │
│      ↓                                         │
│  @orientbot/database                              │
│      ↓                                         │
│  @orientbot/database-services                     │
│      ↓                                         │
│  @orientbot/integrations                          │
│      ↓                                         │
│  @orientbot/agents                                │
│      ↓                                         │
│  @orientbot/mcp-tools                             │
│      ↓                                         │
│  @orientbot/bot-whatsapp | @orientbot/bot-slack      │
└─────────────────────────────────────────────────┘
```

Packages can only import from packages **above** them in this hierarchy.

## Re-Export Patterns

### Barrel File (index.ts) Pattern

```typescript
// packages/*/src/index.ts

// Re-export types (always safe)
export type { ConfigOptions, LogLevel } from './types/index.js';

// Re-export ESM modules
export { loadConfig } from './config/index.js';
export { createLogger } from './logger/index.js';

// Re-export default exports
export { default as SomeClass } from './SomeClass.js';
```

### Conditional ESM/CJS Exports

Use `package.json` exports field for dual support:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.cjs",
      "default": "./dist/index.js"
    }
  }
}
```

## Troubleshooting

### Import Works in Tests, Fails in Runtime

Tests may use different module resolution (esbuild/vite transforms). Check:

1. Is the import target an ESM or CJS module?
2. Are you using `export *` with a CJS module?
3. Is there a circular dependency in the runtime load order?

### "Module not found" After Build

```bash
# Ensure dist/ exists
ls packages/*/dist/

# Rebuild the package
pnpm --filter @orientbot/package-name build

# Check exports in package.json match dist/ structure
```

### Dynamic Import for CJS Modules

When importing CJS modules dynamically:

```typescript
// ESM dynamic import of CJS module
const cjsModule = await import('./cjs-module.cjs');
const { someExport } = cjsModule.default || cjsModule;
```

## Best Practices

1. **Use explicit `.js` extensions** in all import paths
2. **Avoid `export *`** with modules that might be CJS
3. **Import from specific packages** rather than re-export barrels
4. **Follow dependency hierarchy** to prevent circular deps
5. **Test imports at runtime** not just in vitest (different resolution)
