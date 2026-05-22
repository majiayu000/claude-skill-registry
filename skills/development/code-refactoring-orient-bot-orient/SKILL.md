---
name: code-refactoring
description: Guide for refactoring duplicate code in the Orient. Use when extracting shared logic, consolidating services, or improving code organization. Covers tool-calling extraction, database unification, and monorepo migration patterns.
---

# Code Refactoring Patterns

## Overview

This skill provides patterns and checklists for refactoring code in the Orient monorepo. Use this when:

- Extracting shared logic from duplicate implementations
- Migrating services between `src/` and `packages/`
- Unifying database access patterns
- Consolidating tool definitions

## Pattern 1: Service Extraction

**When to use**: Two or more services share identical logic (>50 lines or complex logic).

### Checklist

1. **Identify Shared Code**
   - Find duplicate implementations in the codebase
   - Document the differences (usually import paths and configuration)
   - Verify the logic is semantically identical

2. **Design the Shared Interface**

   ```typescript
   // Define configuration options
   export interface ServiceConfig {
     option1?: string;
     option2?: number;
   }

   // Define the executor/adapter pattern
   export type ServiceExecutor = (input: Input, context?: Context) => Promise<Result>;
   ```

3. **Create the Shared Service**
   - Place in `src/services/` or appropriate package
   - Make all platform-specific parts configurable
   - Add comprehensive JSDoc comments

4. **Update Consumers**
   - Import from the new shared service
   - Pass platform-specific configuration
   - Remove duplicate inline implementations

5. **Write Tests**
   - Unit tests for the shared service
   - Integration tests for each consumer
   - Before/after comparison tests if needed

### Example: Tool-Calling Service

The `toolCallingService.ts` extracts the common tool-calling loop from `AgentService` and `WhatsAppAgentService`:

```typescript
// Shared service with configurable behavior
export async function executeToolLoop(
  anthropic: Anthropic,
  messages: MessageParam[],
  tools: Tool[],
  executor: ToolExecutor, // Platform-specific
  config: ToolCallingConfig,
  context?: unknown // Platform-specific context
): Promise<ToolCallingResult>;
```

Consumers pass their own tool executor while benefiting from shared guardrails.

## Pattern 2: Package Migration

**When to use**: Moving code from `src/` to `packages/` for better modularity.

### Checklist

1. **Create Package Structure**

   ```
   packages/[package-name]/
   ├── package.json
   ├── tsconfig.json
   ├── vitest.config.ts
   ├── README.md
   ├── src/
   │   ├── index.ts
   │   └── [implementation files]
   └── __tests__/
   ```

2. **Define Package Dependencies**
   - Use `"@orient/core": "workspace:*"` for internal deps
   - Keep dependencies minimal
   - Avoid circular dependencies

3. **Update tsconfig.json Path Mappings**

   ```json
   {
     "compilerOptions": {
       "paths": {
         "@orient/[package]": ["./packages/[package]/src/index.ts"]
       }
     }
   }
   ```

4. **Incremental Migration**
   - Start with types-only export if the migration is complex
   - Add deprecation notices to old files
   - Update consumers one at a time
   - Run tests after each consumer update

5. **Verify Package Builds**
   ```bash
   pnpm --filter @orient/[package] build
   pnpm --filter @orient/[package] test
   ```

### Example: @orient/database-services

```typescript
// packages/database-services/src/index.ts
export { MessageDatabase, StoredMessage, StoredGroup } from './messageDatabase.js';
export { SlackDatabase } from './slackDatabase.js';
export { SchedulerDatabase } from './schedulerDatabase.js';
export { WebhookDatabase } from './webhookDatabase.js';
export * from './types/index.js';
```

## Pattern 3: Database Access Unification

**When to use**: Multiple database access patterns coexist (raw SQL, BaseDatabase, Drizzle).

### Checklist

1. **Audit Current Usage**

   ```bash
   grep -r "BaseDatabase" src/
   grep -r "getDatabase" src/
   grep -r "executeRawSql" src/
   ```

2. **Create Comparison Tests**
   - Write tests that verify old and new implementations produce same results
   - Include edge cases and error scenarios

3. **Create Drizzle Helpers**

   ```typescript
   // In @orient/database
   export async function executeRaw<T>(sql: string, params?: unknown[]): Promise<T[]>;
   export async function executeRawOne<T>(sql: string, params?: unknown[]): Promise<T | null>;
   ```

4. **Migrate Services One at a Time**
   - Start with services that already use Drizzle partially
   - Update imports to use @orient/database
   - Run comparison tests after each migration

5. **Deprecate Old Patterns**
   - Add `@deprecated` JSDoc to old implementations
   - Set timeline for removal

## Pattern 4: Tool Definition Consolidation

**When to use**: Same tools defined in multiple places.

### Checklist

1. **Create Tool Definitions Directory**

   ```
   src/tools/definitions/
   ├── index.ts
   ├── jira.ts
   └── whatsapp.ts
   ```

2. **Extract Common Definitions**

   ```typescript
   // src/tools/definitions/jira.ts
   export const JIRA_TOOL_DEFINITIONS: Anthropic.Tool[] = [
     { name: 'get_all_issues', ... },
     // ...
   ];
   ```

3. **Create Platform-Specific Getters**

   ```typescript
   export function getSlackJiraTools(): Anthropic.Tool[] {
     return [...JIRA_TOOL_DEFINITIONS];
   }

   export function getWhatsAppJiraTools(): Anthropic.Tool[] {
     return [...JIRA_TOOL_DEFINITIONS, ...EXTENDED_TOOLS];
   }
   ```

4. **Update Consumers**
   - Import from definitions instead of defining inline
   - Test that all tools are still available

## Common Pitfalls

### 1. Breaking Import Paths

- Always update tsconfig.json path mappings
- Use `.js` extensions for ESM compatibility
- Build dependent packages before consumers

### 2. Missing Type Exports

- Export types explicitly: `export type { TypeName }`
- Re-export from index.ts for convenience

### 3. Circular Dependencies

- Keep packages loosely coupled
- Use dependency injection patterns
- Types can often break circular deps

### 4. Test Coverage Gaps

- Write tests BEFORE refactoring
- Use comparison tests for migrations
- Run tests after each incremental change

## Pattern 5: Import Path Migration

**When to use**: Migrating imports from old paths to new package exports, or consolidating scattered imports.

### Pre-Migration Audit

Before changing any imports, audit the current state:

```bash
# Find all imports of a specific module
grep -r "from '.*oldModule'" packages/ src/ --include="*.ts"

# Count imports by pattern
grep -r "from '@orient/old" packages/ --include="*.ts" | wc -l

# Find files importing from dist (should be zero)
grep -r "from '.*dist/" packages/ src/ --include="*.ts"
```

### Migration Checklist

1. **Build the target package first**

   ```bash
   pnpm --filter @orient/new-package build
   ls packages/new-package/dist/  # Verify dist exists
   ```

2. **Add workspace dependency to consumer's package.json**

   ```json
   {
     "dependencies": {
       "@orient/new-package": "workspace:*"
     }
   }
   ```

3. **Update imports one file at a time**

   ```typescript
   // Before
   import { Service } from '../../old/path/service.js';

   // After
   import { Service } from '@orient/new-package';
   ```

4. **Verify after each file**

   ```bash
   pnpm --filter @orient/consumer-package build
   pnpm --filter @orient/consumer-package test
   ```

5. **Check for runtime issues**
   - Build passes but runtime fails = missing export or ESM/CJS issue
   - See `esm-cjs-interop` and `package-exports` skills for solutions

### Import Path Decision Tree

| Scenario                          | Import From                   |
| --------------------------------- | ----------------------------- |
| Same package, same directory      | `./file.js`                   |
| Same package, different directory | `../other/file.js`            |
| Different package (production)    | `@orient/package`             |
| Different package (dev, no build) | Path alias resolves to source |
| Legacy src/ code                  | `../../services/file.js`      |

### Avoiding Dist Imports

**Never** import directly from another package's dist:

```typescript
// ❌ Wrong - brittle, breaks on rebuild
import { X } from '../../../packages/core/dist/index.js';
import { X } from '@orient/core/dist/something.js';

// ✅ Correct - uses package exports
import { X } from '@orient/core';
```

Add this test to prevent regressions:

```typescript
// tests/no-dist-imports.test.ts
import { describe, it, expect } from 'vitest';
import { execSync } from 'child_process';

describe('Import hygiene', () => {
  it('should not import from dist directories', () => {
    const result = execSync("grep -r \"from '.*dist/\" packages/ src/ --include='*.ts' || true", {
      encoding: 'utf-8',
    });
    expect(result.trim()).toBe('');
  });
});
```

### Bulk Migration Script

For large migrations, use a script:

```bash
#!/bin/bash
# migrate-imports.sh

OLD_IMPORT="from '../../old/service"
NEW_IMPORT="from '@orient/new-package"

find packages/ src/ -name "*.ts" -exec \
  sed -i '' "s|${OLD_IMPORT}|${NEW_IMPORT}|g" {} \;

echo "Updated files:"
git diff --name-only
```

### Post-Migration Verification

```bash
# Full rebuild
pnpm turbo build --force

# Run all tests
pnpm test

# Type check
pnpm turbo typecheck

# Check for leftover old imports
grep -r "old/import/path" packages/ src/ --include="*.ts"
```

## Package Dependency Graph

```
@orient/core (foundation)
    ├── @orient/database (Drizzle ORM)
    ├── @orient/database-services (MessageDB, SlackDB, etc.)
    ├── @orient/integrations (JIRA, Google)
    ├── @orient/mcp-tools (tool implementations)
    ├── @orient/bot-whatsapp
    ├── @orient/bot-slack
    ├── @orient/api-gateway
    └── @orient/dashboard
```

## Migration Status Tracking

Use this template to track migration progress:

```markdown
| Component          | Status   | Package                   | Notes                           |
| ------------------ | -------- | ------------------------- | ------------------------------- |
| jiraService        | partial  | @orient/integrations      | Types exported, service pending |
| messageDatabase    | complete | @orient/database-services |                                 |
| toolCallingService | complete | src/services/             | Shared between agents           |
```
