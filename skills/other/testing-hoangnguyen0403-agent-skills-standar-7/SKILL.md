---
name: Next.js Testing
description: Unit, Integration, and E2E testing standards for App Router.
metadata:
  labels: [nextjs, testing, vitest, playwright, msw]
  triggers:
    files: ['**/*.test.{ts,tsx}', 'cypress/**', 'tests/**']
    keywords: [vitest, playwright, msw, testing-library]
---

# Next.js Testing

## **Priority: P1 (HIGH)**

## Structure

```text
tests/
├── unit/               # Vitest + RTL
├── e2e/                # Playwright
└── mocks/              # MSW Handlers
```

## Implementation Guidelines

- **Unit Testing**: Use **Vitest** for speed and React Testing Library for components.
- **E2E Testing**: Use **Playwright** for full-stack App Router validation.
- **MSW**: Mock API boundaries using **Mock Service Worker** (server + client).
- **RSC Testing**: Test Server Components via unit tests or full E2E flow.
- **Data Isolation**: Use isolation strategies for test databases/cache.
- **CI reporting**: Ensure JSON/JUnit output for automated analysis.

## Anti-Patterns

- **Real Fetches**: **No real network usage**: Always use MSW or mocks.
- **Shallow Testing**: **No implementation testing**: Test user behavior only.
- **Slow suites**: **No heavy E2E for unit logic**: Use Vitest for logic.
- **Global mocks**: **No global state leakage**: Reset mocks after each test.

## References

- [Next.js Test Patterns](references/implementation.md)
