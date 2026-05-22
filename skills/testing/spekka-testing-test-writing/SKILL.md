---
name: Vitest Testing Patterns
description: Vitest-based test writing with mocking strategies for Remotion and AWS services. Use this when creating test files (__tests__/*.test.ts), writing unit tests for components or server logic, mocking external dependencies, or validating API endpoints and video rendering behavior.
---

# Vitest Testing Patterns

This Skill provides Claude Code with specific guidance on how it should handle testing test writing.

## When to use this skill:

- Creating new test files in __tests__/ or *.test.ts
- Writing unit tests for API endpoints in server/__tests__/
- Testing Remotion components or animation calculations
- Mocking Remotion bundler, renderer, or AWS S3 client
- Validating request/response behavior
- Testing frame calculations or timing logic

## Instructions

- **Vitest Framework**: Use Vitest for all tests; leverage native ESM and TypeScript support
- **Test File Location**: Place tests in `__tests__/` directories or colocate as `*.test.ts` files
- **Write Minimal Tests During Development**: Focus on completing feature implementation first, then add strategic tests at logical completion points
- **Test Core Workflows**: Test critical paths: video rendering, API endpoints, animation calculations, S3 uploads
- **Mock External Services**: Mock Remotion bundler/renderer and AWS S3 client in tests
- **Test Behavior, Not Implementation**: Focus on what the code does (e.g., "renders correct frame count") not how
- **Clear Test Names**: Use descriptive names: `test('returns 404 when video not found', ...)`
- **Fast Execution**: Unit tests should run in milliseconds; mock heavy operations like video rendering

**Examples:**
```typescript
// Good: Clear mocking, behavior focus, descriptive
import { describe, test, expect, vi } from 'vitest';
import { renderVideo } from '../render';

vi.mock('@remotion/bundler');
vi.mock('@remotion/renderer');

describe('renderVideo', () => {
  test('returns S3 URL after successful render', async () => {
    const result = await renderVideo({ month: 1, year: 2024, books: [] });
    expect(result.s3Url).toMatch(/^https:\/\/.*\.mp4$/);
  });

  test('throws error when month is invalid', async () => {
    await expect(renderVideo({ month: 13, year: 2024 }))
      .rejects.toThrow('Invalid month');
  });
});

// Bad: Implementation details, vague names
test('it works', () => {
  const r = render();
  expect(r.internal.state).toBe('done');
});
```
