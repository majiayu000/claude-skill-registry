---
name: nean-e2e
description: Manage Playwright E2E tests for critical user journeys.
argument-hint: "[--add <journey>] [--run] [--report] [--fix]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Create, run, and maintain E2E tests for critical user flows using Playwright.

## Arguments
- `--add <journey>` — Create new journey test (e.g., `signup-flow`, `checkout`)
- `--run` — Run all E2E tests
- `--run <pattern>` — Run tests matching pattern
- `--report` — Generate and display HTML report
- `--fix` — Fix flaky tests with approval

## Test organization

```
apps/web-e2e/
├── src/
│   ├── journeys/              # User journey tests
│   │   ├── auth.spec.ts       # Sign up, sign in, sign out
│   │   ├── onboarding.spec.ts # First-time user flow
│   │   └── <feature>.spec.ts  # Feature-specific journeys
│   ├── fixtures/              # Test fixtures and helpers
│   │   ├── auth.fixture.ts    # Auth helpers (login as user)
│   │   └── db.fixture.ts      # Database seeding
│   └── pages/                 # Page Object Models
│       ├── home.page.ts
│       └── settings.page.ts
├── playwright.config.ts       # Playwright configuration
└── .env.test                  # Test environment
```

## Journey naming
- `auth` — Authentication flows (signup, signin, signout, password reset)
- `onboarding` — First-time user experience
- `<feature>-crud` — Create, read, update, delete for a feature
- `<feature>-workflow` — Multi-step workflows
- `checkout` — Payment/purchase flows
- `settings` — User settings and preferences

## Commands

```bash
# Run all E2E tests
npm run e2e

# Run specific journey
npm run e2e -- --grep "auth"

# Run in headed mode (watch)
npm run e2e -- --headed

# Run with UI mode
npm run e2e -- --ui

# Generate report
npm run e2e -- --reporter=html && npx playwright show-report
```

## Workflow

### Adding a journey (`--add`)
1. Create test file in `src/journeys/<journey>.spec.ts`
2. Create page objects if needed
3. Add fixtures for test data
4. Run to verify
5. Add to CI if not already included

### Running tests (`--run`)
1. Ensure dev servers are running or use webServer config
2. Execute tests
3. Report results with pass/fail counts
4. Highlight flaky tests (passed on retry)

### Fixing flaky tests (`--fix`)
1. Identify flaky tests from reports
2. Analyze failure patterns
3. Propose fixes (with approval):
   - Add explicit waits
   - Improve selectors
   - Fix race conditions
   - Mock unstable dependencies
4. Re-run to confirm fix

## Best practices enforced
- Use `data-testid` for stable selectors
- Avoid time-based waits (`page.waitForTimeout`)
- Isolate tests (no shared state)
- Reset database state between tests
- Use page object models for reusability
- Test against both light and dark themes

## Angular-specific patterns

```typescript
// Wait for Angular to stabilize
await page.waitForSelector('app-root:not(.loading)');

// Use data-testid attributes
await page.click('[data-testid="submit-button"]');

// Wait for PrimeNG components
await page.waitForSelector('.p-datatable-tbody tr');
```

## Output
- Test results (pass/fail/flaky counts)
- Failure details with screenshots
- Report location

## Reference
For Playwright setup and patterns, see `reference/nean-e2e-reference.md`
