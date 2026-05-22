---
name: tzurot-code-quality
description: Code quality rules enforced by CI. Use when refactoring, hitting ESLint limits, or extracting complex functions. Covers complexity thresholds, extraction patterns, and rule suppression.
lastUpdated: '2026-01-30'
---

# Code Quality & Linting

**Use this skill when:** Fixing lint warnings, hitting complexity limits, refactoring large functions, or understanding ESLint rule philosophy.

## Quick Reference

```bash
# Run linting
pnpm lint           # Check all
pnpm lint:fix       # Auto-fix

# Check specific service
pnpm --filter @tzurot/api-gateway lint
```

## ESLint Limits (eslint.config.js)

| Rule                     | Limit | Level | Fix Strategy           |
| ------------------------ | ----- | ----- | ---------------------- |
| `max-lines`              | 500   | Error | Split into modules     |
| `max-lines-per-function` | 100   | Warn  | Extract helpers        |
| `complexity`             | 15    | Warn  | Data-driven approach   |
| `max-depth`              | 4     | Warn  | Early returns, extract |
| `max-params`             | 5     | Warn  | Options object pattern |
| `max-statements`         | 30    | Warn  | Extract helpers        |
| `max-nested-callbacks`   | 3     | Warn  | Use async/await        |

## Refactoring Patterns

### Options Object Pattern (max-params fix)

```typescript
// ❌ BAD - 6 parameters
function processMatch(
  ctx: MatchContext,
  fullMatch: string,
  persona: ResolvedPersona | null,
  logContext: Record<string, unknown>,
  refType: string,
  fallbackName?: string
): MatchResult { ... }

// ✅ GOOD - Options object
interface ProcessMatchOptions {
  ctx: MatchContext;
  fullMatch: string;
  persona: ResolvedPersona | null;
  logContext: Record<string, unknown>;
  refType: string;
  fallbackName?: string;
}

function processMatch(opts: ProcessMatchOptions): MatchResult {
  const { ctx, fullMatch, persona, logContext, refType, fallbackName } = opts;
  ...
}
```

### Data-Driven Approach (complexity fix)

```typescript
// ❌ BAD - High cyclomatic complexity from repeated if/else
function formatField(personality: Personality): string {
  let result = '';
  if (personality.characterInfo) {
    result += `<character_info>${personality.characterInfo}</character_info>`;
  }
  if (personality.personalityTraits) {
    result += `<personality_traits>${personality.personalityTraits}</personality_traits>`;
  }
  // ... 7 more similar blocks = complexity 10+
}

// ✅ GOOD - Data-driven, complexity stays at 2
const PERSONALITY_FIELDS = [
  { key: 'characterInfo', tag: 'character_info' },
  { key: 'personalityTraits', tag: 'personality_traits' },
  // ...
] as const;

function formatField(personality: Personality): string {
  return PERSONALITY_FIELDS.map(({ key, tag }) => {
    const value = personality[key];
    return value ? `<${tag}>${value}</${tag}>` : '';
  })
    .filter(Boolean)
    .join('\n');
}
```

### Helper Extraction (max-statements fix)

```typescript
// ❌ BAD - 40+ statements in one function
async function handleRequest(req: Request): Promise<Response> {
  // validation (10 statements)
  // business logic (15 statements)
  // response formatting (10 statements)
  // error handling (5 statements)
}

// ✅ GOOD - Split into focused helpers
async function handleRequest(req: Request): Promise<Response> {
  const validated = validateRequest(req); // 10 statements extracted
  const result = await processRequest(validated); // 15 statements extracted
  return formatResponse(result); // 10 statements extracted
}
```

### Early Return Pattern (max-depth fix)

```typescript
// ❌ BAD - Deep nesting
function process(data: Data | null): Result {
  if (data !== null) {
    if (data.isValid) {
      if (data.items.length > 0) {
        // actual logic at depth 4
      }
    }
  }
}

// ✅ GOOD - Early returns, flat structure
function process(data: Data | null): Result {
  if (data === null) return defaultResult;
  if (!data.isValid) return invalidResult;
  if (data.items.length === 0) return emptyResult;

  // actual logic at depth 1
}
```

## TypeScript Strict Rules

| Rule                         | Level | Alternative                                |
| ---------------------------- | ----- | ------------------------------------------ |
| `no-explicit-any`            | Error | Use `unknown` + type guards                |
| `no-unsafe-assignment`       | Error | Validate with Zod                          |
| `no-non-null-assertion`      | Warn  | Use optional chaining + nullish coalescing |
| `strict-boolean-expressions` | Error | Be explicit: `!== null`, `!== undefined`   |

```typescript
// ❌ BAD
const data = response.json() as MyType;
if (data) { ... }

// ✅ GOOD
const data: unknown = await response.json();
const validated = MyTypeSchema.parse(data);
if (validated !== null) { ... }
```

## When to Suppress Rules

### OK to Suppress

```typescript
// Generated code or external types
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type PrismaPayload = any;

// Test utilities with intentional complexity
// eslint-disable-next-line max-lines-per-function
function createComplexTestFixture() { ... }

// One-off scripts (not production code)
/* eslint-disable complexity */
```

### Never Suppress

- Production business logic
- API route handlers
- Core services
- Security-related code

**If you need to suppress, ask: "Should I refactor instead?"**

## Pino Logger Format (ESLint Enforced)

Custom ESLint rule enforces correct pino format:

```typescript
// ✅ CORRECT - Error object in first argument
logger.error({ err: error }, 'Failed to process request');
logger.warn({ err: error, userId }, 'User quota exceeded');
logger.info({ requestId, duration }, 'Request completed');

// ❌ WRONG - Will fail lint
logger.error(error, 'Failed to process');
logger.error('Failed:', error);
```

## Error Handling Best Practices

### Current Pattern (callGatewayApi)

```typescript
const result = await callGatewayApi<PersonaResponse>('/user/persona', { userId });
if (!result.ok) {
  logger.warn({ error: result.error, status: result.status }, 'API call failed');
  await interaction.editReply(`❌ ${result.error}`);
  return;
}
// result.data is typed correctly here
```

### Aspirational: Result Pattern for New Services

For complex domain logic, consider typed error returns:

```typescript
type Result<T, E = string> = { ok: true; data: T } | { ok: false; error: E };

// Explicit error types at compile time
type GetUserError = 'NOT_FOUND' | 'FORBIDDEN' | 'INVALID_ID';

async function getUser(id: string): Promise<Result<User, GetUserError>> {
  if (!isValidId(id)) return { ok: false, error: 'INVALID_ID' };

  const user = await prisma.user.findUnique({ where: { id } });
  if (!user) return { ok: false, error: 'NOT_FOUND' };

  return { ok: true, data: user };
}
```

## Module Organization

### Avoid Re-exports

**Import from source modules, not index files.**

Re-exports create spaghetti code and obscure dependencies. They make refactoring harder and cause circular import issues (see: Turbo 2.x cyclic dependency that required splitting test-utils).

```typescript
// ❌ BAD - Re-exporting for convenience
// utils/index.ts
export { formatDate } from './dateUtils.js';
export { parseUrl } from './urlUtils.js';

// ✅ GOOD - Import from source
import { formatDate } from './utils/dateUtils.js';
import { parseUrl } from './utils/urlUtils.js';
```

**Exceptions**: Package entry points (e.g., `@tzurot/common-types`) are acceptable.

**📚 See**: `CLAUDE.md#avoid-re-exports` for full guidance

## Common Lint Fixes

### Promise Handling

```typescript
// ❌ Floating promise
someAsyncFunction();

// ✅ Explicit handling
await someAsyncFunction();
void someAsyncFunction(); // Fire-and-forget (intentional)
```

### Boolean Expressions

```typescript
// ❌ Implicit boolean coercion
if (user) { ... }
if (items.length) { ... }

// ✅ Explicit checks
if (user !== null && user !== undefined) { ... }
if (items.length > 0) { ... }
```

### Unused Variables

```typescript
// ❌ Unused
const result = await fetch();

// ✅ Prefix with underscore if intentionally unused
const _result = await fetch();
```

## Related Skills

- **tzurot-testing** - Coverage requirements, test patterns
- **tzurot-architecture** - Service boundaries, SRP
- **tzurot-git-workflow** - Pre-push checks run lint
- **tzurot-types** - Zod validation, type safety

## References

- ESLint config: `eslint.config.js`
- TypeScript config: `tsconfig.json`
- Prettier config: `.prettierrc`
