---
name: typescript-type-safety
description: Use when encountering TypeScript any types, type errors, or lax type checking - eliminates type holes and enforces strict type safety through proper interfaces, type guards, and module augmentation
---

# TypeScript Type Safety

## Overview

**Zero tolerance for `any` types.** Every `any` is a runtime bug waiting to happen.

Replace `any` with proper types using interfaces, `unknown` with type guards, or generic constraints. Use `@ts-expect-error` with explanation only when absolutely necessary.

## When to Use

**Use when you see:**
- `: any` in function parameters or return types
- `as any` type assertions
- TypeScript errors you're tempted to ignore
- External libraries without proper types
- Catch blocks with implicit `any`

**Don't use for:**
- Already properly typed code
- Third-party `.d.ts` files (contribute upstream instead)

## Type Safety Hierarchy

**Prefer in this order:**
1. Explicit interface/type definition
2. Generic type parameters with constraints
3. Union types
4. `unknown` (with type guards)
5. `never` (for impossible states)

**Never use:** `any`

## Quick Reference

| Pattern | Bad | Good |
|---------|-----|------|
| **Error handling** | `catch (error: any)` | `catch (error) { if (error instanceof Error) ... }` |
| **Unknown data** | `JSON.parse(str) as any` | `const data = JSON.parse(str); if (isValid(data)) ...` |
| **Type assertions** | `(request as any).user` | `(request as AuthRequest).user` |
| **Double casting** | `return data as unknown as Type` | Align interfaces instead: make types compatible |
| **External libs** | `const server = fastify() as any` | `declare module 'fastify' { ... }` |
| **Generics** | `function process(data: any)` | `function process<T extends Record<string, unknown>>(data: T)` |

## Implementation

### Error Handling

```typescript
// ❌ BAD
try {
  await operation();
} catch (error: any) {
  console.error(error.message);
}

// ✅ GOOD - Use unknown and type guard
try {
  await operation();
} catch (error) {
  if (error instanceof Error) {
    console.error(error.message);
  } else {
    console.error('Unknown error:', String(error));
  }
}

// ✅ BETTER - Helper function
function toError(error: unknown): Error {
  if (error instanceof Error) return error;
  return new Error(String(error));
}

try {
  await operation();
} catch (error) {
  const err = toError(error);
  console.error(err.message);
}
```

### Unknown Data Validation

```typescript
// ❌ BAD
const data = await response.json() as any;
console.log(data.user.name);

// ✅ GOOD - Type guard
interface UserResponse {
  user: {
    name: string;
    email: string;
  };
}

function isUserResponse(data: unknown): data is UserResponse {
  return (
    typeof data === 'object' &&
    data !== null &&
    'user' in data &&
    typeof data.user === 'object' &&
    data.user !== null &&
    'name' in data.user &&
    typeof data.user.name === 'string'
  );
}

const data = await response.json();
if (isUserResponse(data)) {
  console.log(data.user.name); // Type-safe
}
```

### Module Augmentation

```typescript
// ❌ BAD
const user = (request as any).user;
const db = (server as any).pg;

// ✅ GOOD - Augment third-party types
import { FastifyRequest, FastifyInstance } from 'fastify';

interface AuthUser {
  user_id: string;
  username: string;
  email: string;
}

declare module 'fastify' {
  interface FastifyRequest {
    user?: AuthUser;
  }

  interface FastifyInstance {
    pg: PostgresPlugin;
  }
}

// Now type-safe everywhere
const user = request.user; // AuthUser | undefined
const db = server.pg;      // PostgresPlugin
```

### Generic Constraints

```typescript
// ❌ BAD
function merge(a: any, b: any): any {
  return { ...a, ...b };
}

// ✅ GOOD - Constrained generic
function merge<
  T extends Record<string, unknown>,
  U extends Record<string, unknown>
>(a: T, b: U): T & U {
  return { ...a, ...b };
}
```

### Type Alignment (Avoid Double Casts)

```typescript
// ❌ BAD - Double cast indicates misaligned types
interface SearchPackage {
  id: string;
  type: string;  // Too loose
}

interface RegistryPackage {
  id: string;
  type: PackageType;  // Specific enum
}

return data.packages as unknown as RegistryPackage[];  // Hiding incompatibility

// ✅ GOOD - Align types from the source
interface SearchPackage {
  id: string;
  type: PackageType;  // Use same specific type
}

interface RegistryPackage {
  id: string;
  type: PackageType;  // Now compatible
}

return data.packages;  // No cast needed - types match
```

**Rule:** If you need `as unknown as Type`, your interfaces are misaligned. Fix the root cause, don't hide it with double casts.

## ESM Import Extensions

**Always use `.js` extension for relative imports in ESM projects.**

Node.js ESM requires explicit file extensions. TypeScript compiles `.ts` → `.js`, so imports must reference the output extension.

```typescript
// ❌ BAD - Will fail at runtime in ESM
import { helper } from './utils';
import { CLIError } from '../utils/cli-error';
import type { Package } from './types/package';

// ✅ GOOD - Explicit .js extensions
import { helper } from './utils.js';
import { CLIError } from '../utils/cli-error.js';
import type { Package } from './types/package.js';
```

**Why this is a TypeScript/type safety issue:**
- TypeScript doesn't catch missing extensions at compile time
- Errors only appear at runtime: `ERR_MODULE_NOT_FOUND`
- CI builds fail but local development works (cached modules)
- This is one of the most common "works locally, fails in CI" issues

**TSConfig for ESM:**
```json
{
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    // OR
    "module": "ESNext",
    "moduleResolution": "bundler"
  }
}
```

**Common Import Mistakes:**

| Pattern | Issue | Fix |
|---------|-------|-----|
| `import { x } from './file'` | Missing extension | `import { x } from './file.js'` |
| `import { x } from './dir'` | Missing index | `import { x } from './dir/index.js'` |
| `import pkg from 'pkg/subpath'` | Package export | Check package.json `exports` field |

**Linting for Import Extensions:**
```bash
# Find imports missing .js extension
grep -rn "from '\.\.\?/[^']*[^j][^s]'" --include="*.ts" src/

# ESLint rule (if using eslint)
# "import/extensions": ["error", "always", { "ignorePackages": true }]
```

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Using `any` for third-party libs | Loses all type safety | Use module augmentation or `@types/*` package |
| `as any` for complex types | Hides real type errors | Create proper interface or use `unknown` |
| `as unknown as Type` double casts | Misaligned interfaces | Align types at source - same enums/unions |
| Skipping catch block types | Unsafe error access | Use `unknown` with type guards or toError helper |
| Generic functions without constraints | Allows invalid operations | Add `extends` constraint |
| Ignoring `ts-ignore` accumulation | Tech debt compounds | Fix root cause, use `@ts-expect-error` with comment |
| Missing `.js` import extensions | ESM runtime failures | Always use `.js` for relative imports |

## TSConfig Strict Settings

Enable all strict options for maximum type safety:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## Type Audit Workflow

1. **Find**: `grep -r ": any\|as any" --include="*.ts" src/`
2. **Categorize**: Group by pattern (errors, requests, external libs)
3. **Define**: Create interfaces/types for each category
4. **Replace**: Systematic replacement with proper types
5. **Validate**: `npm run build` must succeed
6. **Test**: All tests must pass

## Real-World Impact

**Before type safety:**
- Runtime errors from undefined properties
- Silent failures from type mismatches
- Hours debugging production issues
- Difficult refactoring

**After type safety:**
- Errors caught at compile time
- IntelliSense shows all available properties
- Confident refactoring with compiler help
- Self-documenting code

---

**Remember:** Type safety isn't about making TypeScript happy - it's about preventing runtime bugs. Every `any` you eliminate is a production bug you prevent.
