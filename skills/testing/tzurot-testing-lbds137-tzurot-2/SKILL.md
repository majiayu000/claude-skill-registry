---
name: tzurot-testing
description: Vitest testing patterns for Tzurot v3. Use when writing tests, debugging test failures, or mocking dependencies. Covers mock factories, fake timers, and promise rejection handling.
lastUpdated: '2026-01-30'
---

# Tzurot v3 Testing Patterns

**Use this skill when:** Writing tests, debugging test failures, adding mocks, or working with fake timers.

## Quick Reference

```bash
# Run all tests
pnpm test

# Run specific service
pnpm --filter @tzurot/ai-worker test

# Run specific file
pnpm test -- MyService.test.ts

# Coverage
pnpm test:coverage
```

```typescript
// Basic test structure
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('MyService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should do something', () => {
    expect(result).toBe(expected);
  });
});
```

## Core Principles

1. **Test behavior, not implementation**
2. **Colocated tests** - `MyService.test.ts` next to `MyService.ts`
3. **Mock all external dependencies** - Discord, Redis, Prisma, AI
4. **Use fake timers** - No real delays in tests

## Essential Patterns

### Fake Timers (ALWAYS Use)

```typescript
beforeEach(() => {
  vi.useFakeTimers();
});
afterEach(() => {
  vi.restoreAllMocks();
});

it('should retry with delay', async () => {
  const promise = withRetry(fn);
  await vi.runAllTimersAsync();
  await promise;
});
```

### Promise Rejections with Fake Timers (CRITICAL)

```typescript
// ❌ WRONG - Causes PromiseRejectionHandledWarning
const promise = asyncFunction();
await vi.runAllTimersAsync(); // Rejection happens here!
await expect(promise).rejects.toThrow(); // Too late

// ✅ CORRECT - Attach handler BEFORE advancing timers
const promise = asyncFunction();
const assertion = expect(promise).rejects.toThrow('Error'); // Handler attached
await vi.runAllTimersAsync(); // Now advance
await assertion; // Await result
```

### Mock Factory Pattern

```typescript
// Use async factory for vi.mock hoisting
vi.mock('./MyService.js', async () => {
  const { mockMyService } = await import('../test/mocks/MyService.mock.js');
  return mockMyService;
});

// Import accessors after vi.mock
import { getMyServiceMock } from '../test/mocks/index.js';

it('should call service', () => {
  expect(getMyServiceMock().someMethod).toHaveBeenCalled();
});
```

### Common Mocks

```typescript
// Discord message
function createMockMessage(overrides = {}) {
  return {
    id: '123',
    content: 'test',
    author: { id: 'user-123', bot: false },
    channel: { id: 'channel-123', send: vi.fn() },
    reply: vi.fn().mockResolvedValue({}),
    ...overrides,
  } as unknown as Message;
}

// Prisma
function createMockPrisma() {
  return {
    personality: { findUnique: vi.fn(), findMany: vi.fn() },
    $disconnect: vi.fn(),
  } as unknown as PrismaClient;
}

// Redis
function createMockRedis() {
  return {
    get: vi.fn().mockResolvedValue(null),
    set: vi.fn().mockResolvedValue('OK'),
    ping: vi.fn().mockResolvedValue('PONG'),
  } as unknown as Redis;
}
```

## Test File Naming

| Type        | Pattern            | Location              | Infrastructure |
| ----------- | ------------------ | --------------------- | -------------- |
| Unit        | `*.test.ts`        | Next to source        | Fully mocked   |
| Integration | `*.int.test.ts`    | Next to source        | PGLite         |
| Schema      | `*.schema.test.ts` | `common-types/types/` | Zod only       |
| E2E         | `*.e2e.test.ts`    | `tests/e2e/`          | Real services  |

## Registry Integrity Tests (Commands)

Tests that validate command routing works correctly:

```typescript
// In CommandHandler.int.test.ts
describe('registry integrity', () => {
  it('should have all componentPrefixes registered', () => {
    const prefixToCommand = (handler as any).prefixToCommand as Map<string, unknown>;

    for (const [name, command] of handler.getCommands()) {
      // Command name should always be registered as prefix
      expect(prefixToCommand.has(name)).toBe(true);

      // All componentPrefixes should be registered
      if (command.componentPrefixes) {
        for (const prefix of command.componentPrefixes) {
          expect(
            prefixToCommand.has(prefix),
            `componentPrefix "${prefix}" from "${name}" not registered`
          ).toBe(true);
        }
      }
    }
  });
});
```

**Why**: Catches bugs like the `/me profile edit` "Unknown interaction" error where entityType wasn't in componentPrefixes.

## Command Structure Snapshots

Capture command structure to detect unintended changes:

```typescript
describe('command structure snapshots', () => {
  it('should have stable /persona command structure', () => {
    const personaCommand = handler.getCommand('persona');
    const data = personaCommand!.data.toJSON();
    expect(data.options).toMatchSnapshot('persona-command-options');
  });

  it('should have stable command count', () => {
    const count = handler.getCommands().size;
    expect(count).toMatchSnapshot('total-command-count');
  });
});
```

**When snapshots change**: Intentional command changes require `-u` flag to update.

## Mock Reset Functions

| Function               | What It Does                    | When to Use    |
| ---------------------- | ------------------------------- | -------------- |
| `vi.clearAllMocks()`   | Clears call history, keeps impl | `beforeEach()` |
| `vi.restoreAllMocks()` | Restores original (spies only)  | `afterEach()`  |
| `vi.resetAllMocks()`   | Clears history + resets impl    | Rarely needed  |

## When to Add Tests

| Change              | Unit | Schema       | Integration                    |
| ------------------- | ---- | ------------ | ------------------------------ |
| New API endpoint    | ✅   | ✅ Required  | ✅ If DB/multi-service         |
| New `*.service.ts`  | ✅   | If shared    | ✅ For complex DB operations   |
| New utility/helper  | ✅   | No           | No                             |
| Bug fix             | ✅   | If schema    | If multi-component interaction |
| New dashboard/modal | ✅   | If API types | No (UI logic, mock sessions)   |
| **New tooling**     | ✅   | No           | No                             |

### Tooling Package Tests

**All tooling code requires unit tests.** See `tzurot-tooling` skill for details. Key points:

- Implementation modules in `packages/tooling/src/*/` need `*.test.ts` files
- Command registration files (`commands/*.ts`) are thin wrappers - no tests needed
- Mock `child_process` functions like `execSync` and `spawnSync` for shell commands

### Integration Test Guidance

**When Required**:

- Database operations with complex queries (joins, transactions)
- Cross-service communication (bot-client → api-gateway → ai-worker)
- Business logic spanning multiple services

**When NOT Needed**:

- Pure utility functions
- UI/Discord interaction handlers (mock the session/API instead)
- Simple CRUD operations

**Future Enhancement**: Service-pairing ratchet where every `*.service.ts` requires `*.int.test.ts`

## Schema Tests

Schema tests verify API schemas validate correctly. Located in `common-types/types/`.

```typescript
// *.schema.test.ts - Verify schema validation
import { PersonaResponseSchema } from './schemas.js';

describe('PersonaResponse schema', () => {
  it('should parse valid API response', () => {
    const response = { id: 'uuid', name: 'Test', preferredName: null };
    expect(() => PersonaResponseSchema.parse(response)).not.toThrow();
  });

  it('should reject invalid response', () => {
    const response = { id: 123 }; // Wrong type
    expect(() => PersonaResponseSchema.parse(response)).toThrow();
  });
});
```

**When to write**: New API endpoints, schema changes, cross-service communication.

**Purpose**: Catch breaking changes before they hit production. If bot-client expects `{ name: string }` but api-gateway returns `{ displayName: string }`, schema tests fail.

## Integration Tests

Integration tests verify components with real database (PGLite). Co-located next to source files with `.int.test.ts` suffix.

```typescript
// UserService.int.test.ts - Test with real database
describe('UserService', () => {
  let pglite: PGlite;
  let prisma: PrismaClient;

  beforeAll(async () => {
    pglite = new PGlite({ extensions: { vector } });
    await pglite.exec(loadPGliteSchema());
    prisma = new PrismaClient({ adapter: new PrismaPGlite(pglite) });
  });

  it('should create user with default persona', async () => {
    const service = new UserService(prisma);
    const userId = await service.getOrCreateUser('123', 'testuser');
    expect(userId).toBeDefined();
  });
});
```

**When to write**: Database operations, complex queries, service-level behavior.

**Key difference**:

- **Unit tests** (`*.test.ts`): Mock all dependencies, test one function
- **Integration tests** (`*.int.test.ts`): Use PGLite, test database interactions

### PGLite for Local Integration Tests

```bash
# Run integration tests (no DATABASE_URL needed)
pnpm test:int

# Regenerate schema after Prisma migrations
./scripts/testing/regenerate-pglite-schema.sh
```

**⚠️ ALWAYS use `loadPGliteSchema()` - NEVER create tables manually!**

Manual table creation (via `$executeRawUnsafe('CREATE TABLE...')`) breaks when migrations add new columns. The shared schema file stays in sync with Prisma migrations.

**📚 See**: `docs/reference/testing/PGLITE_SETUP.md` for full setup, environment detection, and test patterns.

## Definition of Done

Before marking a feature complete:

- [ ] New service files have `.int.test.ts`
- [ ] New API schemas have `.schema.test.ts` (if crossing service boundary)
- [ ] Complex DB operations have integration test coverage
- [ ] Coverage doesn't drop (Codecov enforces 80% threshold)
- [ ] Run `pnpm ops test:audit` to verify no new test gaps

## Test Coverage Audits (Ratchet System)

The project uses a unified ratchet audit to prevent new untested code:

```bash
# Run unified audit (CI does this automatically)
pnpm ops test:audit

# Filter by category
pnpm ops test:audit --category=services   # Service tests only
pnpm ops test:audit --category=contracts  # Contract tests only

# Update baseline (after closing gaps)
pnpm ops test:audit --update
pnpm ops test:audit --category=services --update  # Update only services

# Strict mode (fails on ANY gap, not just new ones)
pnpm ops test:audit --strict

# Verbose output (show all covered items)
pnpm ops test:audit --verbose
```

**Unified Baseline**: `test-coverage-baseline.json` (project root)

**📚 See**: `docs/reference/testing/COVERAGE_AUDIT_SYSTEM.md` for detailed audit workflows, chip-away process, and priority order.

## Anti-Patterns

```typescript
// ❌ BAD - Testing private methods
expect(service['privateMethod']()).toBe(value);

// ❌ BAD - Real delays
await new Promise(r => setTimeout(r, 1000));

// ❌ BAD - console.log in tests
console.log('Debug:', value);

// ❌ BAD - Skipping instead of fixing
it.skip('broken test', () => {});
```

## Coverage Requirements

**Threshold**: 80% project-wide and per-patch. Codecov blocks if coverage drops >2%.

```bash
pnpm test:coverage                                  # Check coverage locally
pnpm --filter @tzurot/api-gateway test:coverage     # Specific service
```

**📚 See**: `docs/reference/testing/COVERAGE_AUDIT_SYSTEM.md` for detailed thresholds and reading coverage data.

## Related Skills

- **tzurot-code-quality** - Lint rules, refactoring patterns
- **tzurot-types** - Type-safe test fixtures
- **tzurot-git-workflow** - Run tests before pushing
- **tzurot-observability** - Mock logger in tests

## References

- Full testing guide: `docs/reference/guides/TESTING.md`
- Mock factories: `services/*/src/test/mocks/`
- Global philosophy: `~/.claude/CLAUDE.md#universal-testing-philosophy`
- PGLite setup: `packages/test-utils/` (`loadPGliteSchema` from `@tzurot/test-utils`)
- Test audit command: `pnpm ops test:audit`
- Schema regeneration: `./scripts/testing/regenerate-pglite-schema.sh`
- Unified baseline: `test-coverage-baseline.json`
