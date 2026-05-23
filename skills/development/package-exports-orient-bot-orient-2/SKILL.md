---
name: package-exports
description: Configure package.json exports and understand import resolution in the Orient monorepo. Use when confused about dist vs source imports, configuring package exports, fixing module resolution errors, or creating barrel files. Covers exports field patterns, development vs production resolution, and re-export strategies.
---

# Package Exports & Import Patterns

## Quick Reference

```bash
# Test package exports work correctly
pnpm --filter @orientbot/core test

# Check what a package exports
cat packages/core/package.json | jq '.exports'

# Verify dist exists before importing
ls packages/core/dist/
```

## The Golden Rule: Source vs Dist

| Context                         | Import From             | Why                |
| ------------------------------- | ----------------------- | ------------------ |
| **Inside same package**         | Source (`./file.js`)    | Direct file access |
| **Cross-package (production)**  | Dist (`@orientbot/pkg`) | Built output       |
| **Cross-package (development)** | Source via path alias   | TypeScript paths   |

**Never** import from another package's `dist/` directory directly:

```typescript
// ❌ WRONG - importing dist directly
import { Service } from '../../../dist/services/service.js';
import { Service } from '@orientbot/core/dist/index.js';

// ✅ CORRECT - use package name (resolves to dist via exports)
import { Service } from '@orientbot/core';

// ✅ CORRECT - use local re-export
import { Service } from './services/index.js';
```

## package.json Exports Field

The `exports` field defines how your package can be imported:

### Basic Export Pattern

```json
{
  "name": "@orientbot/core",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.js",
      "default": "./dist/index.js"
    }
  }
}
```

### Subpath Exports

For packages with multiple entry points:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./config": {
      "types": "./dist/config/index.d.ts",
      "import": "./dist/config/index.js"
    },
    "./logger": {
      "types": "./dist/logger/index.d.ts",
      "import": "./dist/logger/index.js"
    }
  }
}
```

This enables:

```typescript
import { loadConfig } from '@orientbot/core'; // Main export
import { Config } from '@orientbot/core/config'; // Subpath export
import { createLogger } from '@orientbot/core/logger'; // Subpath export
```

### Export Order Matters

Node.js uses the **first matching condition**:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts", // TypeScript reads this first
      "import": "./dist/index.js", // ESM import
      "require": "./dist/index.cjs", // CommonJS require
      "default": "./dist/index.js" // Fallback
    }
  }
}
```

## Development Resolution with Path Aliases

During development, TypeScript uses path aliases from root `tsconfig.json`:

```json
{
  "compilerOptions": {
    "paths": {
      "@orientbot/core": ["./packages/core/src/index"],
      "@orientbot/database": ["./packages/database/src/index"]
    }
  }
}
```

This means:

- **Development**: `@orientbot/core` → `packages/core/src/index.ts`
- **Production**: `@orientbot/core` → `packages/core/dist/index.js`

## Re-Export Patterns (Barrel Files)

### Standard Re-Export

```typescript
// packages/core/src/index.ts

// Named exports
export { loadConfig } from './config/index.js';
export { createLogger, createServiceLogger } from './logger/index.js';

// Type exports (important for consumers)
export type { Config, LogLevel } from './types/index.js';

// Default export
export { default as CoreModule } from './CoreModule.js';
```

### Re-Exporting from Dependencies

When re-exporting from workspace dependencies:

```typescript
// packages/agents/src/index.ts

// Re-export from workspace dependency
export { MessageDatabase } from '@orientbot/database-services';

// Or selective re-export
import { MessageDatabase } from '@orientbot/database-services';
export { MessageDatabase };
```

### Avoiding Re-Export Issues

```typescript
// ❌ Can cause issues with CJS modules
export * from './some-module.js';

// ✅ Explicit named exports are safer
export { SpecificClass, specificFunction } from './some-module.js';
```

## Common Errors & Solutions

### "Cannot find module '@orientbot/package'"

1. **Build the package first**:

   ```bash
   pnpm --filter @orientbot/package build
   ```

2. **Check exports match dist structure**:

   ```bash
   ls packages/package/dist/
   cat packages/package/package.json | jq '.exports'
   ```

3. **Verify workspace dependency**:
   ```json
   {
     "dependencies": {
       "@orientbot/package": "workspace:*"
     }
   }
   ```

### "Module has no exported member"

The export exists in source but not in the barrel file:

```typescript
// Check src/index.ts includes the export
export { MissingClass } from './MissingClass.js';
```

### Import Works in IDE but Fails at Runtime

TypeScript uses path aliases (source), but runtime uses package exports (dist):

1. Ensure package is built
2. Check exports field matches what you're importing
3. Subpath imports need explicit exports

### Circular Import Error

Usually caused by re-export chains:

```typescript
// Package A re-exports from B
export { Something } from '@orientbot/B';

// Package B re-exports from A
export { Other } from '@orientbot/A'; // Circular!
```

Solution: Import from the source package directly.

## Testing Package Exports

Add a contract test to verify exports work:

```typescript
// tests/contracts/core.contract.test.ts
import { describe, it, expect } from 'vitest';

describe('@orientbot/core exports', () => {
  it('should export loadConfig', async () => {
    const { loadConfig } = await import('@orientbot/core');
    expect(typeof loadConfig).toBe('function');
  });

  it('should export from subpath', async () => {
    const { Config } = await import('@orientbot/core/config');
    expect(Config).toBeDefined();
  });
});
```

## Files Field for Publishing

Control what gets published to npm:

```json
{
  "files": ["dist", "README.md"]
}
```

This excludes `src/`, tests, and config files from the package.

## Exporting Database Schema Tables (Drizzle ORM)

The `@orientbot/database` package uses Drizzle ORM and requires explicit exports for schema tables.

### Step 1: Verify Table Definition Exists

Tables are defined in `packages/database/src/schema/index.ts`:

```typescript
// packages/database/src/schema/index.ts
import { pgTable, text, boolean, timestamp, integer, index } from 'drizzle-orm/pg-core';

export const featureFlags = pgTable(
  'feature_flags',
  {
    id: text('id').primaryKey(),
    name: text('name').notNull(),
    enabled: boolean('enabled').default(true),
    createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
  },
  (table) => [index('idx_feature_flags_name').on(table.name)]
);
```

### Step 2: Add Export to Main Package Index

Add the table to the exports in `packages/database/src/index.ts`:

```typescript
// packages/database/src/index.ts

// Export schema tables directly for convenience
export {
  messages,
  groups,
  dashboardUsers,
  // ... existing exports ...

  // Feature Flags tables (NEW)
  featureFlags,
  userFeatureFlagOverrides,

  // Enums
  messageDirectionEnum,
} from './schema/index.js';
```

### Step 3: Rebuild Dependent Packages

After adding exports, rebuild the database package and all dependent packages:

```bash
# Rebuild database package
pnpm turbo run build --filter=@orientbot/database

# Rebuild all dependent packages (dashboard depends on database)
pnpm turbo run build --filter=@orientbot/dashboard
```

### Step 4: Use the Export

Now you can import the table in other packages:

```typescript
// packages/dashboard/src/server/routes/featureFlags.routes.ts
import { getDatabase, featureFlags, eq } from '@orientbot/database';

const db = getDatabase();

// Query the table
const flags = await db.select().from(featureFlags).where(eq(featureFlags.enabled, true));

// Update the table
await db
  .update(featureFlags)
  .set({ enabled: false, updatedAt: new Date() })
  .where(eq(featureFlags.id, 'mini_apps'));
```

### Step 5: Add Test for Export

Verify the export works with a contract test:

```typescript
// packages/database/__tests__/schema.test.ts
import { describe, it, expect } from 'vitest';
import { featureFlags } from '../src/index.js';

describe('@orientbot/database schema exports', () => {
  it('should export featureFlags table', () => {
    expect(featureFlags).toBeDefined();
    expect(featureFlags.id).toBeDefined();
    expect(featureFlags.enabled).toBeDefined();
  });
});
```

## Verifying Exports at Runtime

### The IDE vs Runtime Gap

A common pitfall: **imports work in your IDE but fail at runtime**. This happens because:

- IDE uses TypeScript path aliases → resolves to source files
- Runtime uses package exports → resolves to built dist files

### Ensuring Rebuilt Packages Are Picked Up

After modifying exports, follow this sequence:

```bash
# 1. Rebuild the modified package AND its dependents in order
pnpm turbo run build --filter=@orientbot/database
pnpm turbo run build --filter=@orientbot/dashboard

# Or rebuild everything that depends on database
pnpm turbo run build --filter=...@orientbot/database
```

**Why turbo?** It handles dependency order automatically. If dashboard depends on database, turbo builds database first.

### Restarting Servers After Rebuilds

Running servers cache module imports. After rebuilding packages:

```bash
# Find and kill the server process
lsof -i :4098  # Find dashboard server PID
kill <PID>

# Or if using ./run.sh dev, it may auto-restart
# If not, restart the dev environment
./run.sh stop && ./run.sh dev
```

### Verifying Runtime Imports

Test that exports work at runtime, not just in IDE:

```bash
# Quick runtime verification
node -e "import('@orientbot/database').then(m => console.log(Object.keys(m)))"

# Or check specific export
node -e "import('@orientbot/database').then(m => console.log('featureFlags:', !!m.featureFlags))"
```

### Debugging Stale Builds

If runtime still fails after rebuilding:

1. **Check dist files exist**:

   ```bash
   ls packages/database/dist/schema/
   grep -l "featureFlags" packages/database/dist/*.js
   ```

2. **Clear turbo cache** (nuclear option):

   ```bash
   rm -rf .turbo node_modules/.cache
   pnpm turbo run build --filter=@orientbot/database --force
   ```

3. **Check tsbuildinfo isn't stale**:
   ```bash
   rm packages/database/tsconfig.tsbuildinfo
   pnpm turbo run build --filter=@orientbot/database
   ```

## Transforming Database Rows to API Responses

When creating API routes that query database tables, you need to transform Drizzle row objects into the format expected by the frontend.

### Type Mapping: Database -> API

```typescript
// Database row from Drizzle (nullable fields, Date objects)
const dbRow = {
  id: 'mini_apps',
  name: 'Mini Apps',
  enabled: true, // boolean | null in DB
  createdAt: Date, // Date object
  updatedAt: Date, // Date object
};

// API response format (non-null, ISO strings)
const apiResponse = {
  id: dbRow.id,
  name: dbRow.name,
  enabled: dbRow.enabled ?? true, // Handle nulls with defaults
  createdAt: dbRow.createdAt?.toISOString() ?? new Date().toISOString(),
  updatedAt: dbRow.updatedAt?.toISOString() ?? new Date().toISOString(),
};
```

### Date Serialization

Drizzle returns `Date` objects, but JSON APIs need ISO strings:

```typescript
// ❌ WRONG - Date objects don't serialize correctly
res.json({ flags: dbFlags });

// ✅ CORRECT - Convert dates to ISO strings
const flags = dbFlags.map((flag) => ({
  ...flag,
  createdAt: flag.createdAt?.toISOString() ?? new Date().toISOString(),
  updatedAt: flag.updatedAt?.toISOString() ?? new Date().toISOString(),
}));
res.json({ flags });
```

### Adding Computed/Derived Fields

APIs often need fields not in the database:

```typescript
// Frontend expects FeatureFlagWithOverride
interface FeatureFlagWithOverride {
  id: string;
  name: string;
  enabled: boolean;
  userOverride: boolean | null; // Not in DB yet
  effectiveValue: boolean; // Computed field
}

// Transform DB row to API format
const flags = dbFlags.map((flag) => ({
  id: flag.id,
  name: flag.name,
  enabled: flag.enabled ?? true,
  userOverride: null, // Placeholder until implemented
  effectiveValue: flag.enabled ?? true, // Computed from enabled
  createdAt: flag.createdAt?.toISOString(),
  updatedAt: flag.updatedAt?.toISOString(),
}));
```

### Common Error: "flags is not iterable"

```
Uncaught TypeError: flags is not iterable
```

**Cause**: API returns object map `{ flags: { id: {...} } }` but frontend expects array `{ flags: [...] }`.

**Fix**: Ensure API returns an array:

```typescript
// ❌ Returns object map
const flagsMap: Record<string, any> = {};
for (const flag of dbFlags) {
  flagsMap[flag.id] = { enabled: flag.enabled };
}
res.json({ flags: flagsMap });

// ✅ Returns array
const flags = dbFlags.map((flag) => ({
  id: flag.id,
  enabled: flag.enabled ?? true,
}));
res.json({ flags });
```

### Common Error: "does not provide an export named"

```
SyntaxError: The requested module '@orientbot/database' does not provide an export named 'featureFlags'
```

**Cause**: Table is defined in `schema/index.ts` but not re-exported from main `index.ts`.

**Fix**:

1. Add the table name to exports in `packages/database/src/index.ts`
2. Rebuild: `pnpm turbo run build --filter=@orientbot/database`
3. Restart any running servers

### Checklist for New Database Tables

- [ ] Define table in `packages/database/src/schema/index.ts`
- [ ] Add migration in `data/migrations/XXX_add_table.sql`
- [ ] Export table from `packages/database/src/index.ts`
- [ ] Export any related types from `packages/database/src/types.ts`
- [ ] Rebuild: `pnpm turbo run build --filter=@orientbot/database`
- [ ] Add schema test in `packages/database/__tests__/schema.test.ts`
- [ ] Rebuild dependent packages

## Checklist for New Exports

When adding a new export to a package:

- [ ] Add export to `src/index.ts`
- [ ] If subpath export, add to `package.json` exports
- [ ] Rebuild the package
- [ ] Add contract test for the export
- [ ] Update consumers to use the new export
