---
name: e2e-writer
description: Write E2E tests with Playwright using selector best practices. Use when you need to write end-to-end integration tests, user scenarios, or complete workflows.
---

# E2E Test Writer (Playwright)

You write **robust** E2E tests with Playwright, prioritizing semantic selectors.

## Reference

Complete selector hierarchy (getByRole, getByLabel, getByText, getByTestId, locator) and best practices are documented in `.claude/rules/testing-e2e.md`.

**You MUST read this file** to understand exact selection rules and pitfalls to avoid.

## Execution Commands

```bash
npm run test:e2e        # Headless (CI)
npm run test:e2e:ui     # UI mode
npm run test:e2e:debug  # Step by step
```

## Complete Test Pattern

See [examples.md](./examples.md) for a complete E2E test example.

## Best Practices

See [examples.md](./examples.md) for detailed best practices (dynamic waiting, timeouts, cleanup) and naming conventions.

## Checklist

- [ ] Only semantic selectors (`getByRole`, `getByLabel`)
- [ ] No CSS classes (`.btn-primary`) or IDs (`#title-input`)
- [ ] No `waitForTimeout()` → wait for specific elements
- [ ] Structure : Navigate → Interact → Verify
- [ ] Tests cover nominal + error cases

## See Also

- **[test-writer](../test-writer/SKILL.md)** — Complementary approach for unit and integration tests of business logic. Use test-writer for isolating logic; use e2e-writer for complete user workflows.
