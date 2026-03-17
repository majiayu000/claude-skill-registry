---
name: walkeros-testing-strategy
description:
  Use when writing tests, reviewing test code, or discussing testing approach
  for walkerOS packages. Covers env pattern, dev examples, and package-specific
  strategies.
---

# walkerOS Testing Strategy

## Overview

walkerOS uses a layered testing approach with built-in patterns for mocking and
documentation sync. This skill ensures tests are reliable, efficient, and
maintainable.

**Core principle:** Test real behavior using the `env` pattern, link to `dev`
examples, verify before claiming complete.

## The Rules

### Rule 1: Use `env` for Mocking, Not Jest

walkerOS has a built-in dependency injection pattern via `env` in context. This
is lighter than Jest mocks, enables documentation generation, and keeps tests in
sync with examples.

**Wrong:**

```typescript
jest.mock('../ga4', () => ({ initGA4: jest.fn() }));
expect(initGA4).toHaveBeenCalledWith(...);
```

**Right:**

```typescript
import { examples } from '../dev';
import { mockEnv } from '@walkeros/core';

const calls: Array<{ path: string[]; args: unknown[] }> = [];
const testEnv = mockEnv(examples.env.push, (path, args) => {
  calls.push({ path, args });
});

await destination.push(event, { ...context, env: testEnv });
expect(calls).toContainEqual({
  path: ['window', 'gtag'],
  args: ['event', 'page_view', { page_title: 'Home' }],
});
```

### Rule 2: Link Tests to `dev` Examples

The `dev.ts` export provides `examples.env`, `examples.events`, and
`examples.mapping`. Using these in tests ensures documentation stays in sync.

```typescript
import { examples } from '../dev';

// Use examples.env for mock environment
const testEnv = mockEnv(examples.env.push, interceptor);

// Assert against examples.events (documented expected output)
expect(calls[0].args).toEqual(examples.events.ga4PageView());

// Test with examples.mapping configurations
const config = { mapping: examples.mapping.ecommerce };
```

### Rule 3: Test Real Behavior, Not Mock Behavior

If you're asserting that a mock was called, you're testing the mock works, not
the code.

**Red flags:**

- `expect(mockFn).toHaveBeenCalled()` without verifying the mock produces real
  effects
- Assertions on `*-mock` test IDs
- Tests that pass when mock is present, fail when removed

**Fix:** Test what the code actually does. If external APIs must be mocked,
verify the real API would receive correct data.

### Rule 4: Test First, Watch It Fail

If you didn't see the test fail, you don't know it tests the right thing.

**Process:**

1. Write failing test
2. Verify it fails for expected reason (missing feature, not typo)
3. Write minimal code to pass
4. Verify it passes
5. Refactor if needed

**Red flags:**

- Test passes immediately when written
- Can't explain why test failed
- "I'll add tests later"

### Rule 5: No Test-Only Methods in Production Code

Production classes shouldn't have methods only tests use.

**Wrong:**

```typescript
class Session {
  destroy() {
    /* only used in tests */
  }
}
```

**Right:**

```typescript
// In test-utils/
export function cleanupSession(session: Session) { ... }
```

### Rule 6: Verify Before Claiming Complete

"Should pass now" is not verification.

**Process:**

1. Run the actual test command
2. Read the output
3. Confirm pass/fail count
4. Only then claim status

## When to Use Each Test Type

| Type            | When to Add                                                         | Example                                                        |
| --------------- | ------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Integration** | New usage pattern, new external API interaction, new data flow path | Collector → Destination → gtag()                               |
| **Unit**        | Combinatorics, edge cases, pure function logic                      | Mapping variations, core utilities                             |
| **Contract**    | Boundary validation                                                 | Destination output matches vendor API, source input validation |

**Guideline:** Integration tests prove things work when stuck together. Unit
tests efficiently cover variations. Contract tests catch API drift.

## Package-Specific Approaches

| Package                 | Approach                                                                        |
| ----------------------- | ------------------------------------------------------------------------------- |
| **core**                | Unit tests only - pure functions, no env needed                                 |
| **collector**           | Integration tests critical - input/output consistency is paramount              |
| **browser source**      | Maintain walker algorithm coverage                                              |
| **web destinations**    | Integration tests per unique pattern + unit tests for mappings, use env pattern |
| **server destinations** | Same as web destinations                                                        |
| **cli/docker**          | Integration tests for spawn behavior, explore dev pattern to reduce duplication |
| **sources**             | Contract tests for input validation, integration tests for event capture        |

## The env Pattern Deep Dive

### How env Works

Each destination/source defines an `env` type that specifies external
dependencies:

```typescript
// Destination-specific env type
export interface Env extends DestinationWeb.Env {
  window: {
    gtag: Gtag.Gtag;
    dataLayer: unknown[];
  };
  document: {
    createElement: (tagName: string) => HTMLElement;
    head: { appendChild: (node: unknown) => void };
  };
}
```

### mockEnv() Function

The `mockEnv()` function from `@walkeros/core` creates a Proxy that intercepts
all function calls:

```typescript
import { mockEnv } from '@walkeros/core';

const calls: Array<{ path: string[]; args: unknown[] }> = [];
const testEnv = mockEnv(examples.env.push, (path, args) => {
  calls.push({ path, args });
  // Optionally return a value
});

// Now use testEnv in your destination context
await destination.push(event, { ...context, env: testEnv });

// Assert on captured calls
expect(calls).toContainEqual({
  path: ['window', 'gtag'],
  args: ['event', 'purchase', expect.objectContaining({ value: 99.99 })],
});
```

### dev.ts Structure

Each package with external dependencies should have:

```typescript
// src/dev.ts
export * as schemas from './schemas';
export * as examples from './examples';

// src/examples/index.ts
export * as env from './env';
export * as events from './events';
export * as mapping from './mapping';
```

## Red Flags - Stop and Fix

- Using `jest.mock()` for internal modules when `env` pattern is available
- Tests that don't import from `../dev`
- Assertions only checking mock call counts
- Tests with extensive mock setup (>50% of test is setup)
- Test-only methods added to production classes
- Claiming tests pass without running them

## Commands

```bash
# Run all tests
npm run test

# Run tests for specific package
cd packages/[name] && npm run test

# Run single test file
npm run test -- path/to/file.test.ts

# Watch mode
npm run test -- --watch
```

## Related Skills

- [walkeros-understanding-development](../walkeros-understanding-development/SKILL.md) -
  Development conventions and workflow

**Reference:**

- [AGENT.md](../../AGENT.md) - Development guide
