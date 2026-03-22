---
name: testing
description: Vitest and Playwright testing patterns, conventions, and gotchas for this project.
user-invocable: true
---

# Testing Patterns

## Vitest (Unit + Integration)
- Config lives in `apps/web/vite.config.ts` (no separate vitest.config)
- Run: `npm run test` from `apps/web/`
- Run single file: `npx vitest run path/to/file.test.ts`

### vi.mock Gotcha (IMPORTANT)
`vi.mock()` is hoisted to the top of the file. You CANNOT reference variables declared above it:

```typescript
// BAD — will be undefined
const mockFn = vi.fn()
vi.mock('./module', () => ({ doThing: mockFn }))

// GOOD — define inline
vi.mock('./module', () => ({ doThing: vi.fn() }))
import { doThing } from './module'
// Now doThing is the mock — use it for assertions
```

### Rules
- Test behavior, not implementation
- Prefer integration tests over unit tests
- Mock external services, not internal functions
- "close timed out" warning after Vitest is a known nitro issue — ignore

## Playwright (E2E)
- Config: `apps/web/playwright.config.ts`
- Tests: `apps/web/e2e/`
- Run: `npm run test:e2e` from `apps/web/`
- Use `page.getByRole()`, `page.getByText()` over CSS selectors
