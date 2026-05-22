---
description: Testing requirements for Brief codebase
---

# Testing Strategy

> **Methodology**: This skill defines WHAT to test and coverage requirements. For HOW to write tests (RED-GREEN-REFACTOR workflow), see the `tdd` skill.

## TDD Integration

All new code should follow test-driven development:

1. **Write test first** (RED) - See `tdd` skill
2. **Implement minimal code** (GREEN)
3. **Refactor while green** (REFACTOR)

This skill provides the patterns and requirements; `tdd` provides the methodology.

## Coverage Requirements

- **New features**: Minimum 80% coverage
- **Bug fixes**: MUST include regression test
- **Refactors**: Maintain or improve existing coverage

## What MUST Have Tests

1. All API routes (app/api/v1/**/route.ts)
2. All custom hooks (hooks/use-*.ts)
3. Complex business logic
4. MCP tool implementations
5. Utility functions with branching logic

## Test Patterns

### API Route Tests

```typescript
import { POST } from './route';
import { mockAuth } from '@/test/helpers';

describe('POST /api/v1/documents', () => {
  it('creates document with valid data', async () => {
    mockAuth({ userId: 'test-user' });
    const req = new Request('http://localhost', {
      method: 'POST',
      body: JSON.stringify({ title: 'Test', folder_id: 'abc' })
    });
    const res = await POST(req);
    expect(res.status).toBe(201);
  });

  it('returns 400 for missing folder_id', async () => {
    // Test error path
  });

  it('returns 401 for unauthenticated request', async () => {
    // Test auth error
  });
});
```

### Hook Tests

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useDocuments } from './use-documents';

describe('useDocuments', () => {
  it('fetches documents successfully', async () => {
    const { result } = renderHook(() => useDocuments('folder-id'));
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toHaveLength(3);
  });

  it('handles loading state', () => {
    const { result } = renderHook(() => useDocuments('folder-id'));
    expect(result.current.isLoading).toBe(true);
    expect(result.current.data).toBeUndefined();
  });

  it('handles error state', async () => {
    mockApiError('Failed to fetch');
    const { result } = renderHook(() => useDocuments('folder-id'));

    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.error).toBeDefined();
    expect(result.current.error?.message).toContain('Failed to fetch');
  });

  it('handles empty folder', async () => {
    mockApiResponse([]);
    const { result } = renderHook(() => useDocuments('empty-folder'));

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toHaveLength(0);
  });

  it('cleans up on unmount', () => {
    const { unmount } = renderHook(() => useDocuments('folder-id'));
    unmount();
    // Verify cleanup (e.g., aborted requests, cleared timers)
  });
});
```

## Running Tests

- `pnpm test` - Run all tests
- `pnpm run test:watch` - Watch mode for development
- `pnpm run test:coverage` - Coverage report

## Before Requesting Commit

- ✅ All tests pass
- ✅ New code has tests (written BEFORE implementation per `tdd` skill)
- ✅ Coverage meets thresholds
- ✅ No test.only or test.skip left in code
- ✅ Tests verify behavior, not implementation details

## Related Skills

| Skill | Purpose |
|-------|---------|
| `tdd` | RED-GREEN-REFACTOR methodology |
| `debugging` | Systematic bug investigation (write regression test first) |
| `brief-patterns` | API route and database patterns to test |
| `security-patterns` | Auth and RLS testing requirements |
