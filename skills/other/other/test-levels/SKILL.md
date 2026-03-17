---
name: test-levels
description: This skill explains the 3 test levels (Unit, Integration, E2E) using the "Building a Car" analogy and provides guidance on when to use each type. Includes project-specific Playwright examples.
---

# Test Levels Guide

Explains test types & guides test selection using car analogy.

## When to Use

Invoke when:

- Explaining test concepts to team members
- Deciding which test type to write
- Reviewing test coverage strategy
- Onboarding new developers to testing

## The 3 Test Levels

### 1. Unit Test (Test Case)

**The specific instruction.**

Single fn/component tested in isolation. No external deps (DB, API, browser).

| Aspect | Description |
|--------|-------------|
| Analogy | "Check if left turn signal blinks when I push lever down" |
| Scope | Tiny detail - one fn, one input/output |
| Speed | Fast (ms) |
| Location | `tests/unit/` |

**When to write:**

- Pure functions (formatters, validators, utils)
- Data transformations
- Business logic w/o side effects

**Project example:**

```typescript
// tests/unit/utils/formatters.spec.ts
import {expect, test} from 'next/experimental/testmode/playwright';
import {leadingZero, formatCurrency} from '@/app/_utils/formatters';

test.describe('formatters', () => {
    test('leadingZero adds zero to single-digit numbers', () => {
        expect(leadingZero(7)).toBe('07');
        expect(leadingZero(10)).toBe('10');
    });

    test('formatCurrency formats correctly', () => {
        const result = formatCurrency({value: 1234.56, locale: 'en', currency: 'USD'});
        expect(result).toBe('1,234.56 $');
    });
});
```

---

### 2. Integration Test

**The handshake.**

Tests if 2+ parts communicate correctly. Focuses on connections, not full system.

| Aspect | Description |
|--------|-------------|
| Analogy | "Does engine make wheels turn?" (Engine → Transmission) |
| Scope | Connections between components |
| Speed | Medium (100ms-few seconds) |
| Location | `tests/integration/` |

**When to write:**

- Validators w/ schemas (Zod)
- API route handlers
- Service-to-service communication
- DB queries w/ mocked data

**Project example:**

```typescript
// tests/integration/validators/offer.spec.ts
import {expect, test} from 'next/experimental/testmode/playwright';
import {mockLoggedUser} from '../../common';
import {validateCustomerStatus} from '@/app/_lib/validator';

test.beforeEach(async ({context}) => {
    await mockLoggedUser(context);
});

test.describe('validate customer status', () => {
    const validData = {
        offerId: '670e80f0a65da593d265088a',
        status: 'viewing',
    };

    test('returns success for valid data', async () => {
        const result = validateCustomerStatus(validData);
        expect(result.success).toBe(true);
        expect(result.data).toEqual(validData);
    });

    test('returns error for invalid offerId', async () => {
        const result = validateCustomerStatus({...validData, offerId: ''});
        expect(result.success).toBe(false);
        expect(result.error?.issues[0]?.path).toContain('offerId');
    });
});
```

---

### 3. E2E Test (End-to-End)

**The real user journey.**

Full system test: browser, DB, network, 3rd-party services. Exactly as user experiences.

| Aspect | Description |
|--------|-------------|
| Analogy | "Start car, drive to store, park, turn off" |
| Scope | Full user flow |
| Speed | Slow (seconds-minutes) |
| Location | `tests/pages/` |

**When to write:**

- Critical user flows (login, checkout, payment)
- Multi-page journeys
- Features requiring browser interaction
- Smoke tests for deployment

**Project example:**

```typescript
// tests/pages/start.spec.ts
import {expect, test} from 'next/experimental/testmode/playwright';
import {mockLoggedUser, resetAPIEndpointsMock} from '../common';

test.beforeEach(async ({context}) => {
    await mockLoggedUser(context);
});

test.afterEach(async ({next, context}) => {
    await resetAPIEndpointsMock(next);
    await context.clearCookies();
});

test('start page renders correctly', async ({page}) => {
    test.setTimeout(120000);

    await page.goto('http://localhost:3000/start', {
        timeout: 90000,
        waitUntil: 'domcontentloaded'
    });

    await expect(page).toHaveURL('http://localhost:3000/start');
    await expect(page.getByTestId('pageHeader')).toHaveClass('drop-shadow-font');
    await expect(page.getByTestId('subTotal')).toContainText('Sub total');
    await expect(page.getByTestId('startCounter')).toContainText('Your vacation starts in');
});
```

---

## Quick Decision Guide

| Question | Test Type |
|----------|-----------|
| "Does this fn return correct value?" | Unit |
| "Do these 2 parts work together?" | Integration |
| "Does full flow work for user?" | E2E |

### Test Pyramid

```
        /\
       /E2E\         Few (slow, expensive)
      /------\
     /Integr- \      Some (medium)
    /  ation   \
   /------------\
  /    Unit      \   Many (fast, cheap)
 /________________\
```

**Rule:** More unit tests, fewer E2E tests. Unit tests catch bugs early & run fast.

---

## Project Structure

```
tests/
├── unit/              # Pure fn tests (no browser)
│   └── utils/         # Utility fn tests
├── integration/       # Component interaction tests
│   ├── validators/    # Schema validation tests
│   └── lib/           # Library fn tests
├── pages/             # E2E browser tests
│   ├── start.spec.ts
│   ├── payment.spec.ts
│   └── confirm.spec.ts
├── common.ts          # Shared test utilities
├── mock/              # Mock data & helpers
└── seed.spec.ts       # DB seed for tests
```

---

## Commands

```bash
# Run all tests (headed mode)
npm run test

# Run specific test file
npm run test tests/unit/utils/formatters.spec.ts

# Run tests in UI mode
npm run test:ui

# Show test report
npm run test:report
```

---

## Best Practices

1. **Name tests clearly:** `should [action] when [condition]`
2. **One assertion focus:** Test one behavior per test
3. **Use test.describe:** Group related tests
4. **Clean up:** Use `afterEach` for state reset
5. **Mock external deps:** Use `mockLoggedUser`, `resetAPIEndpointsMock`
6. **Set timeouts:** E2E tests need longer timeouts (120s)
7. **Use data-testid:** For reliable element selection

---

## Summary Table

| Level | Question | Scope | Speed | Location |
|-------|----------|-------|-------|----------|
| **Unit** | "Does this fn work?" | Single fn | Fast | `tests/unit/` |
| **Integration** | "Do parts connect?" | Connections | Medium | `tests/integration/` |
| **E2E** | "Does flow work?" | Full system | Slow | `tests/pages/` |
