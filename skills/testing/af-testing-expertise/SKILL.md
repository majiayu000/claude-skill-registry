---
name: af-testing-expertise
description: Use when implementing tests, configuring test frameworks, or analyzing test coverage and failures. Covers Jest unit tests, Playwright E2E tests, React Testing Library component tests, email verification via Gmail API, and testing pyramid patterns.

# AgentFlow documentation fields
title: Testing Expertise
created: 2025-10-29
updated: 2026-01-06
last_checked: 2026-01-06
tags: [skill, expertise, testing, jest, playwright, rtl, tdd, email, coverage]
parent: ../README.md
related:
  - ../../docs/guides/testing-guide.md
---

# Testing Expertise

## When to Use This Skill

Load this skill when you need to:
- Implement unit tests from business logic
- Write integration tests for backend/API behaviour
- Create E2E tests for critical user journeys
- Write RTL tests for component behaviour
- Configure test frameworks (Jest, Playwright, RTL)
- Analyze test failures and debug issues
- Review test coverage and quality
- Follow TDD (Red → Green → Refactor) workflow
- Generate tests from Markdown scenario specs
- Verify email delivery in E2E tests (signup, password reset, notifications)

**Common triggers**:
- Delivery phase (implementing tests)
- Dev-test-agent invoked
- Test failures need debugging
- Coverage targets not met
- New feature needs testing
- Feature involves email sending/verification

## Quick Reference

AgentFlow uses a comprehensive testing strategy following the Testing Pyramid principle:

**Testing Pyramid:**
```
       E2E Tests (few, slow)              ← Playwright
            /\
           /  \   15-20%
      Integration Tests (some, medium)    ← Jest + SDK
         /    \   25-30%
        /______\
  Unit + Component Tests (many, fast)     ← Jest + RTL
                  50-60%
```

**Test Type Decision:**
- **E2E (Playwright)** - Complete user journey through real UI + real backend
- **Integration (Jest + SDK)** - Backend/API behaviour without browser
- **Component (RTL)** - React component behaviour in isolation
- **Unit (Jest)** - Pure functions with no external dependencies

**Coverage targets:** 80%+ overall, all scenarios passing

### Test Pyramid Clarification

The test pyramid ratio is a **guideline, not enforcement**. The appropriate ratio depends on feature type:

| Feature Type | Likely Distribution |
|--------------|-------------------|
| Pure business logic | 80% unit, 15% integration, 5% E2E |
| API-heavy workflow | 30% unit, 50% integration, 20% E2E |
| UI-driven user journey | 20% unit, 30% integration, 50% E2E |

The agent should observe the distribution and ask questions if it seems unusual, but **never block progress** based on ratio alone.

### Test Writing Timeline

Tests are written at different phases for specific reasons:

| Test Type | Written In | By Whom | Why This Phase? |
|-----------|------------|---------|-----------------|
| **Storybook (play functions)** | Refinement | ux-design-agent | PRIMARY component test: visual specs + interaction tests in one place |
| **RTL (Component)** | Refinement | ux-design-agent | Non-visual logic only: hooks, utilities, state management, data transforms |
| **E2E (Playwright)** | Delivery (RED) | AI from scenarios | Tests full flow - can't run until implementation exists |
| **Integration** | Delivery (RED) | AI from scenarios | Tests backend/API - generated from Mini-PRD scenarios |
| **Unit** | Delivery (RED) | As needed | Tests pure logic - written alongside implementation |

**The key insight:** Storybook play functions are the PRIMARY test for UI component behavior. They run in a real browser with visual context, making them superior for asserting what users see and interact with. RTL tests complement Storybook for non-visual logic (hooks, utilities, data transforms) that doesn't need a visual context. **Do not duplicate assertions** — if a Storybook play function already tests that a button is enabled/disabled, don't repeat that assertion in RTL.

**Flow:**
```
Refinement phase:
  Mini-PRD Section 4 (scenarios) ──────────────────────┐
  Mini-PRD Section 5 (selector contract) ──┐           │
                                           ▼           │
  ux-design-agent creates:                             │
    - Storybook stories with play functions             │
      (PRIMARY: UI behavior + interaction tests)        │
    - RTL tests (non-visual logic only)                 │
                                                       │
Delivery Phase (RED):                                  │
  AI generates from scenarios: ◄───────────────────────┘
    - E2E tests (tests/e2e/)
    - Integration tests (tests/integration/)
    - Unit tests (as needed)
```

### CI/CD Pipeline

Both test suites gate pull requests:

| Gate | Command | What It Runs | Speed |
|------|---------|-------------|-------|
| Jest | `pnpm test` | RTL tests, unit tests, integration tests | Fast (~seconds) |
| Storybook | `npx storybook test` | All play functions headlessly | Slower (~30s+) |

Both must pass before merge. Configure in CI:
```yaml
- run: pnpm test
- run: npx storybook test --no-open
```

See [Testing Guide](../../docs/guides/testing-guide.md) for comprehensive patterns.

## Rules

### Critical Testing Rules

1. **Always write tests BEFORE implementation** - TDD Red → Green → Refactor
2. **Tests MUST fail before implementation (RED phase)** - Never commit `expect(true).toBe(true)` or any test that trivially passes. Use `test.todo('description')` for tests that cannot run yet (E2E needing backend, integration needing API). **Never use `test.skip()`** — it silently hides unimplemented tests. `test.todo()` is reported in test output so gaps are always visible. If components exist (Refinement phase), RTL and Storybook tests should PASS, not be todo.
3. **Unit tests MUST be isolated** - No external dependencies, use mocks
4. **Storybook play functions are PRIMARY for UI component testing** - RTL tests cover non-visual logic only. Do not duplicate assertions across both.
5. **E2E tests use Playwright directly** - No Cucumber, AI generates from Markdown specs
6. **All tests MUST be deterministic** - No flaky tests, fix timing issues immediately
7. **Tests MUST describe behaviour, not implementation** - Test "what" not "how"
8. **Never commit failing tests** - Fix or use `test.todo()` with clear reason. **Never `test.skip()`** in committed code — it hides gaps silently.
9. **Every test MUST have clear name** - Describe expected behaviour
10. **80%+ coverage required** - Run `npm run test:coverage` before PR
11. **Tests run in isolation** - Each test sets up and tears down its own state

### Test Organization Rules

12. **Unit test files** end in `.test.ts` or `.spec.ts`
13. **Unit tests** live next to source files - `auth.ts` → `auth.test.ts`
14. **RTL tests** colocated with components - `SignupForm.tsx` → `SignupForm.test.tsx`
15. **E2E tests** go in `/tests/e2e/` - `tests/e2e/auth/signup.spec.ts`
16. **Integration tests** go in `/tests/integration/`
17. **Selector contracts** go in `/tests/selectors/`
18. **Shared test utilities** go in `/tests/helpers/`

### Directory Structure

```
src/components/
├── auth/
│   ├── SignupForm.tsx
│   ├── SignupForm.test.tsx     ← RTL test (colocated)
│   └── SignupForm.stories.tsx  ← Storybook story

tests/
├── e2e/                        ← Playwright E2E tests
│   └── auth/
│       ├── signup.spec.ts
│       └── signin.spec.ts
├── integration/                ← Jest + SDK tests
│   └── auth/
│       └── cognito.test.ts
├── selectors/                  ← Shared selector contracts
│   └── auth.ts
└── helpers/                    ← Test utilities
    ├── gmail-helper.ts
    └── e2e-auth.ts
```

### Mocking Strategy (CRITICAL)

**This table is the source of truth for what can be mocked in each test type:**

| Test Type | Purpose | Mocks Allowed? | What to Mock |
|-----------|---------|----------------|--------------|
| **E2E** | Complete user journeys through real UI + backend | **NO** | Nothing - real browser, real backend, real emails |
| **Integration** | Backend/API behaviour without browser | **External only** | AWS SDK, third-party APIs (Stripe, SendGrid), NOT your own Cognito/DB |
| **RTL (Component)** | React component behaviour in isolation | **Yes** | API calls, context providers, NOT component internals |
| **Unit** | Pure logic isolation | **YES** | All dependencies - APIs, databases, file system, other modules |

**Key distinction for Integration tests:**
- ✅ Mock: External third-party services (Stripe webhooks, SendGrid API)
- ❌ Don't mock: Your own AWS services (Cognito, DynamoDB) - these ARE the integration

### AAA Pattern Rules (Unit Tests)

17. **Arrange** - Set up test data and preconditions
18. **Act** - Invoke the function/method being tested
19. **Assert** - Verify the outcome
20. **One assertion per test** (preferred) - Makes failures clear
21. **Use descriptive test names** - `test('applies 10% discount to cart total')`

## Workflows

### Workflow: Test Type Decision Framework

**When:** Deciding which type of test to write for a scenario

**Decision Flow:**
```
Is it a COMPLETE USER JOURNEY through REAL UI + REAL BACKEND?
  └─ Yes → E2E (Playwright)
  └─ No  → Does it test BACKEND/API behaviour without UI?
            └─ Yes → Integration (Jest + SDK)
            └─ No  → Does it test COMPONENT behaviour in isolation?
                      └─ Yes → Component (RTL)
                      └─ No  → Unit (Jest)
```

**Examples:**

| Scenario | Test Type | Framework |
|----------|-----------|-----------|
| User signs up, verifies email, lands on dashboard | E2E | Playwright |
| Cognito `adminCreateUser()` creates user with correct attributes | Integration | Jest + SDK |
| Button disables when form invalid | Component | RTL |
| `validatePassword('weak')` returns correct errors | Unit | Jest |

### Workflow: TDD Implementation (Red → Green → Refactor)

**When:** Implementing any new function or feature

**Procedure:**
```
1. Write failing test (RED)
   - Describe expected behaviour
   - Call the function (doesn't exist yet)
   - Assert the outcome
   - Run test: npm test
   - Confirm test FAILS for right reason

2. Write minimal implementation (GREEN)
   - Create the function
   - Write simplest code to pass test
   - Run test: npm test
   - Confirm test PASSES

3. Refactor for quality
   - Improve code structure
   - Add types, error handling
   - Extract functions if needed
   - Run test: npm test
   - Confirm still PASSES

4. Add more tests
   - Error cases
   - Edge cases
   - Boundary conditions
   - Repeat cycle for each test
```

### Workflow: Writing RTL Component Tests

**When:** During Refinement phase, locking component behaviour before engineering handoff

**Procedure:**
```
1. Identify component behaviours from scenarios
   - What can the user see?
   - What actions are possible?
   - What feedback appears?
   - What is enabled/disabled?
   - Accessibility roles and semantics

2. Write RTL tests colocated with component
   Location: src/components/[feature]/Component.test.tsx

3. Use accessibility queries (preferred)
   - getByRole, getByLabelText, getByText
   - Avoid: getByTestId (use only when necessary)

4. Test user interactions
   - userEvent for clicks, typing
   - Assert on visible outcomes

5. Run tests
   npm test -- [component-name]
```

**Example RTL Test:**
```typescript
// src/components/auth/SignupForm.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SignupForm } from './SignupForm';

describe('SignupForm', () => {
  it('disables submit button when password is too weak', async () => {
    render(<SignupForm onSubmit={jest.fn()} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'weak');

    expect(screen.getByRole('button', { name: /sign up/i })).toBeDisabled();
    expect(screen.getByText(/password is too short/i)).toBeInTheDocument();
  });

  it('enables submit button when form is valid', async () => {
    render(<SignupForm onSubmit={jest.fn()} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'SecurePass123!');

    expect(screen.getByRole('button', { name: /sign up/i })).toBeEnabled();
  });

  it('calls onSubmit with form data when submitted', async () => {
    const handleSubmit = jest.fn();
    render(<SignupForm onSubmit={handleSubmit} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'SecurePass123!');
    await userEvent.click(screen.getByRole('button', { name: /sign up/i }));

    expect(handleSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'SecurePass123!',
    });
  });
});
```

### Workflow: Writing E2E Tests from Markdown Specs

**When:** Delivery phase, implementing E2E tests from approved scenario specs

**Procedure:**
```
1. Read Markdown scenario spec from Mini-PRD
   Example:
   ### E2E: User signs up with valid email
   **Preconditions:**
   - User is not logged in
   - Email address not already registered

   **Steps:**
   1. User navigates to /signup
   2. User enters valid email and strong password
   3. User submits form

   **Expected:**
   - Verification email sent
   - User sees "Check your email" message

   **Selectors:** AUTH.signup.*

2. Create Playwright test file
   Location: tests/e2e/[capability]/[feature].spec.ts

3. Import selector contract
   import { AUTH } from '../../selectors/auth';

4. Implement test using Playwright API
   - Use selector contract for element references
   - Follow Preconditions/Steps/Expected structure
   - Use Playwright assertions

5. Run E2E tests
   npm run test:e2e
```

**Example E2E Test:**
```typescript
// tests/e2e/auth/signup.spec.ts
import { test, expect } from '@playwright/test';
import { AUTH } from '../../selectors/auth';

const sel = (id: string) => `[data-testid="${id}"]`;

test.describe('User Signup', () => {
  test('signs up with valid email and password', async ({ page }) => {
    // Preconditions: User not logged in (fresh browser context)

    // Step 1: Navigate to signup
    await page.goto('/signup');

    // Step 2: Enter valid email and strong password
    await page.fill(sel(AUTH.signup.email), 'test@example.com');
    await page.fill(sel(AUTH.signup.password), 'SecurePass123!');

    // Step 3: Submit form
    await page.click(sel(AUTH.signup.submit));

    // Expected: User sees "Check your email" message
    await expect(page.locator(sel(AUTH.signup.successMessage)))
      .toContainText('Check your email');
  });

  test('rejects weak password', async ({ page }) => {
    await page.goto('/signup');
    await page.fill(sel(AUTH.signup.email), 'test@example.com');
    await page.fill(sel(AUTH.signup.password), 'weak');

    await expect(page.locator(sel(AUTH.signup.passwordError)))
      .toContainText('Too short');
  });
});
```

### Workflow: Creating Selector Contracts

**When:** Refinement phase, creating shared selectors for Storybook and tests

**Procedure:**
```
1. Identify UI elements from scenario specs
   - Form fields, buttons, messages
   - Interactive elements
   - Status indicators

2. Create selector contract file
   Location: tests/selectors/[capability].ts

3. Define hierarchical selector structure
   - Group by feature area
   - Use descriptive names
   - Follow consistent naming pattern

4. Use in components
   <Input data-testid={AUTH.signup.email} />

5. Use in tests
   await page.fill(sel(AUTH.signup.email), value);
```

**Example Selector Contract:**
```typescript
// tests/selectors/auth.ts
export const AUTH = {
  signup: {
    form: 'signup-form',
    email: 'signup-email',
    password: 'signup-password',
    passwordError: 'signup-password-error',
    submit: 'signup-submit',
    successMessage: 'signup-success',
  },
  signin: {
    form: 'signin-form',
    email: 'signin-email',
    password: 'signin-password',
    submit: 'signin-submit',
    errorMessage: 'signin-error',
  },
  verification: {
    codeInput: 'verification-code',
    submit: 'verification-submit',
    resendButton: 'verification-resend',
  },
};
```

### Workflow: Analyzing Test Failures - Bug or Test Issue?

**When:** Tests fail - need to determine if tests found a real bug or have a test issue

**Critical Question:** "Are our failing tests finding defective code?"

**Procedure:**
```
1. BEFORE modifying any test, investigate the failure
   - Read error message and screenshots carefully
   - Check if the test ever passed (regression vs new test)
   - Look at what the screenshot shows vs what was expected

2. Classify the failure
   REAL BUG indicators:
   - Test logic is sound, but app behaviour is wrong
   - Error screenshots show unexpected UI state (wrong page, missing data)
   - Lambda/API returns wrong data or wrong URL format
   - Multiple tests fail in same area with consistent pattern

   TEST ISSUE indicators:
   - Test works with seeded users but fails with new users (timing)
   - Test fails on retry with different error (flaky)
   - Test passes locally but fails in CI (environment)
   - Assertion timeout but feature appears to work manually

3. For real bugs: Fix the production code first
   - Don't "fix" the test to match broken behaviour
   - Document the bug and fix in commit message

4. For test issues: Then fix the test
   - Add waits, use correct navigation patterns
   - Improve test resilience
```

**Example Real Bug Found:**
```
Test: "invitee can complete signup via invitation"
Error: "Invalid Invitation" error shown
Screenshot: Shows error page instead of signup form

Investigation: Lambda was generating `/accept-invitation?token=xxx`
             but app route is `/invite/[token]`
Fix: Changed Lambda URL format (production bug!)
```

### Workflow: Analyzing Test Failures

**When:** Tests fail in CI/CD or locally

**Procedure:**
```
1. Identify failure type
   - Syntax error → Fix code
   - Assertion failure → Logic bug or wrong expectation
   - Timeout → Async issue or performance problem
   - Flaky → Non-deterministic behaviour

2. Read failure message carefully
   Expected: 90
   Received: 100
   → Discount not applied

3. Check test assumptions
   - Is test data set up correctly?
   - Are mocks configured right?
   - Is async/await handled properly?

4. Run test in isolation
   npm test -- [specific-test-name]
   Eliminates cross-test contamination

5. Add debug output if needed
   console.log('Price:', price);
   console.log('Discount:', discount);
   console.log('Result:', result);

6. Fix root cause
   - Not just the symptom
   - Update test if expectations wrong
   - Fix implementation if logic broken

7. Verify fix
   - Run specific test: passes
   - Run full suite: passes
   - Run multiple times: consistent
```

### Workflow: Email Verification in E2E Tests

**When:** Testing flows that send emails (signup, password reset, notifications, invitations)

**Infrastructure:** Gmail Testing via `testing@gaininsight.global`
- Service account with domain-wide delegation
- Credentials stored in Doppler (`gi` project, `prd` config)
- Plus addressing: `testing+appname@gaininsight.global` for test isolation

**Critical:** E2E email tests need BOTH AWS credentials AND Gmail credentials in the same Doppler config.

**Procedure:**
```
1. Configure app to send test emails
   - Use: testing+[appname]@gaininsight.global as recipient
   - The +appname suffix identifies which app/test sent the email
   - All emails arrive in same inbox

2. Get Gmail credentials
   - Local: doppler secrets get GMAIL_TESTING_SERVICE_ACCOUNT --project gi --config prd --plain
   - CI/CD: Inject via Doppler GitHub Action

3. Implement email verification helper
   - Connect to Gmail API with service account
   - Impersonate testing@gaininsight.global
   - Poll for expected email with timeout
   - Verify email content (subject, body, links)

4. Clean up after tests
   - Delete test emails to avoid inbox clutter
   - Use plus addressing to scope cleanup
```

**Key patterns:**
- **Polling with timeout** - Emails aren't instant; poll every 5s for up to 60s
- **Plus addressing** - `testing+myapp@` isolates your tests from others
- **Search queries** - Use Gmail's query syntax: `to:testing+myapp@ subject:"Welcome"`
- **Cleanup** - Always delete test emails after verification

**Email URL Pattern:**
Email links must work across all environments (localhost, feature branches, production). Derive base URL from request headers, not environment variables:

```typescript
// In email-sending API routes
const protocol = request.headers.get("x-forwarded-proto") || "https";
const host = request.headers.get("host") || "localhost:3000";
const baseUrl = `${protocol}://${host}`;

await sendEmail({
  // ...
  verifyUrl: `${baseUrl}/verify?token=${token}`,
});
```

**Gmail Helper Example:**
```typescript
// tests/helpers/gmail-helper.ts
import { google } from 'googleapis';

interface EmailSearchOptions {
  query: string;
  timeout?: number;
  pollInterval?: number;
}

export class GmailTestHelper {
  private gmail;

  constructor(serviceAccountJson: string) {
    const credentials = JSON.parse(serviceAccountJson);
    const auth = new google.auth.GoogleAuth({
      credentials,
      scopes: ['https://www.googleapis.com/auth/gmail.readonly',
               'https://www.googleapis.com/auth/gmail.modify'],
      clientOptions: { subject: 'testing@gaininsight.global' }
    });
    this.gmail = google.gmail({ version: 'v1', auth });
  }

  async waitForEmail(options: EmailSearchOptions): Promise<any> {
    const { query, timeout = 60000, pollInterval = 5000 } = options;
    const startTime = Date.now();

    while (Date.now() - startTime < timeout) {
      const res = await this.gmail.users.messages.list({
        userId: 'me',
        q: `${query} newer_than:1m`
      });

      if (res.data.messages?.length) {
        const msg = await this.gmail.users.messages.get({
          userId: 'me',
          id: res.data.messages[0].id!
        });
        return msg.data;
      }

      await new Promise(r => setTimeout(r, pollInterval));
    }

    throw new Error(`Email matching "${query}" not found within ${timeout}ms`);
  }

  async deleteEmail(messageId: string): Promise<void> {
    await this.gmail.users.messages.trash({ userId: 'me', id: messageId });
  }

  async cleanupTestEmails(appName: string): Promise<void> {
    const res = await this.gmail.users.messages.list({
      userId: 'me',
      q: `to:testing+${appName}@gaininsight.global`
    });

    for (const msg of res.data.messages || []) {
      await this.deleteEmail(msg.id!);
    }
  }
}
```

### Workflow: Integration Tests for AWS SDK Code

**When:** Testing production code that calls AWS services (Cognito, DynamoDB, SES)

**Key Insight:** Integration tests must import PRODUCTION code to contribute to coverage. Using separate fixture helpers that duplicate functionality creates 0% coverage.

**Pattern:**
```typescript
// tests/integration/lib/cognito-admin.integration.test.ts

// ✅ Import PRODUCTION code (contributes to coverage)
import { listUsers, getUser, disableUser } from '@/lib/cognito-admin';

// ✅ Use fixture helpers for setup/teardown only
import { createTestUser, deleteTestUser } from '../helpers/cognito-helper';

describe('cognito-admin.ts', () => {
  const testUsers: string[] = [];

  afterAll(async () => {
    // Cleanup test users created during tests
    for (const username of testUsers) {
      await deleteTestUser(username);
    }
  });

  it('getUser returns user by username', async () => {
    // Arrange: Create test user via helper
    const username = await createTestUser({ email: 'test@example.com' });
    testUsers.push(username);

    // Act: Call PRODUCTION function
    const user = await getUser(username);

    // Assert
    expect(user?.email).toBe('test@example.com');
  });
});
```

**Run with credentials:**
```bash
# If project has :local scripts configured (recommended)
npm run test:integration:local

# Or manually with Doppler
doppler run --project <project> --config dev -- npm run test:integration
```

**Note:** GainInsight Standard projects should have paired test scripts configured. See `af-setup-process` skill for the full pattern (`test:integration` for CI/CD, `test:integration:local` for local dev).

**Eventual Consistency:** AWS services like Cognito use eventual consistency. Newly created records may not be immediately queryable. Use retry with backoff for tests that create then query data.

### Workflow: API Route Unit Testing

**When:** Implementing new API routes or adding tests to existing routes with low coverage

**Key Pattern:** Mock `next/server` BEFORE importing the route handler:

```typescript
// src/app/api/[resource]/route.test.ts

/**
 * @unit API Route Tests
 */

// Mock next/server BEFORE importing anything else
jest.mock('next/server', () => {
  class MockNextRequest {
    url: string;
    nextUrl: { searchParams: URLSearchParams };
    private _body: string | null;

    constructor(url: string, init?: { method?: string; body?: string }) {
      this.url = url;
      this.nextUrl = { searchParams: new URL(url).searchParams };
      this._body = init?.body || null;
    }

    async json() {
      return this._body ? JSON.parse(this._body) : {};
    }
  }

  class MockNextResponse {
    static json(body: unknown, init?: { status?: number }) {
      return {
        status: init?.status || 200,
        json: async () => body,
        headers: new Map(),
      };
    }
  }

  return { NextRequest: MockNextRequest, NextResponse: MockNextResponse };
});

// Mock dependencies BEFORE importing route
jest.mock('@/lib/amplify-server-utils', () => ({
  runWithAmplifyServerContext: jest.fn(),
}));

// NOW import the route handler
import { GET, POST } from './route';
import { runWithAmplifyServerContext } from '@/lib/amplify-server-utils';
```

**Test Structure:**
```typescript
describe('/api/[resource]', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('GET', () => {
    it('returns 401 when not authenticated', async () => {
      mockRunWithAmplifyServerContext.mockResolvedValue({
        session: { tokens: null },
      });

      const request = new NextRequest('http://localhost/api/resource');
      const response = await GET(request);

      expect(response.status).toBe(401);
    });

    it('returns data when authenticated', async () => {
      mockRunWithAmplifyServerContext.mockResolvedValue({
        user: { userId: 'user-1' },
        session: { tokens: { idToken: { payload: { /* claims */ } } } },
      });

      const request = new NextRequest('http://localhost/api/resource');
      const response = await GET(request);

      expect(response.status).toBe(200);
      const data = await response.json();
      expect(data).toHaveProperty('items');
    });
  });
});
```

**What to Test:**
- Authentication checks (401 responses)
- Authorization/permission checks (403 responses)
- Input validation (400 responses)
- Resource not found (404 responses)
- Successful operations (200/201 responses)
- Error handling paths

**Running Route Tests:**
```bash
npm run test:unit -- --testPathPattern="route.test"
```

### Workflow: Improving Test Coverage

**When:** Coverage below 80%, new code not tested, preparing for PR

**Procedure:**
```
1. Run coverage report
   npm run test:coverage
   Open coverage/lcov-report/index.html

2. Identify uncovered lines
   - Red highlights in coverage report
   - Branches not taken
   - Functions never called

3. Prioritize coverage
   High priority:
   - Business logic (discount calculations, validations)
   - Error handling paths
   - Security-critical code

   Low priority:
   - UI rendering (covered by E2E)
   - Configuration loading
   - Logging statements

4. Write missing tests
   Focus on untested paths:
   - Error branches
   - Edge cases
   - Different input combinations

5. Run coverage again
   npm run test:coverage
   Verify coverage increased

6. Commit when targets met
   Target: 80%+ overall coverage
   Critical paths: 100% coverage
```

### Coverage Configuration Strategy

**Per-file thresholds** are preferred over global thresholds for mixed codebases:

```javascript
// jest.config.js
coverageThreshold: {
  // Per-file thresholds for critical code
  './src/lib/auth-utils.ts': {
    statements: 80, branches: 70, functions: 85, lines: 80,
  },
  './src/components/auth/SignInForm.tsx': {
    statements: 90, branches: 80, functions: 90, lines: 90,
  },
  // No global threshold - avoids failures from demo/base components
},
collectCoverageFrom: [
  'src/**/*.{ts,tsx}',
  // Generic exclusions (framework-level)
  '!src/**/*.stories.tsx',     // Storybook files - visual testing only
  '!src/**/*.d.ts',            // Type definitions
  // Project-specific exclusions go here
  // Review coverage report to identify paths that should be excluded
],
```

**Why per-file?**
- Demo/example components drag down global averages
- Third-party base components (e.g., shadcn) don't need RTL tests - Storybook covers them
- Critical code gets enforced thresholds
- E2E tests cover excluded paths

**What to exclude (project decision):**

| Category | Exclude? | Reason |
|----------|----------|--------|
| Component library base (`ui/`) | Often yes | Tested via Storybook, E2E covers usage |
| Demo/example code | Yes | Not production code |
| Generated types | Yes | Not hand-written code |
| Stories files | Yes | Visual testing only |
| Config files | Often yes | Simple configuration |

**Process:** Review coverage report → Identify low-coverage paths → Decide if they need tests or exclusion → Document rationale

## Examples

### Good: AAA Pattern Unit Test

**✅ Correct - Clear arrangement, action, assertion:**
```typescript
describe('calculateDiscount', () => {
  test('applies 10% percentage discount correctly', () => {
    // Arrange
    const price = 100;
    const discount = { type: 'percentage', value: 10 };

    // Act
    const result = calculateDiscount(price, discount);

    // Assert
    expect(result).toBe(90);
  });
});
```

**❌ Wrong - Mixed setup and assertion:**
```typescript
test('discount', () => {
  const result = calculateDiscount(100, { type: 'percentage', value: 10 });
  expect(result).toBe(90);
  const result2 = calculateDiscount(200, { type: 'fixed', value: 20 });
  expect(result2).toBe(180);
});
```

**Why wrong:** Tests multiple things, unclear which assertion failed.

### Good: Mocking External Dependencies

**✅ Correct - Mock at boundaries:**
```typescript
import { fetchPromoCode } from './api'; // External API
jest.mock('./api');

test('validates promo code from API', async () => {
  // Arrange
  const mockFetch = fetchPromoCode as jest.MockedFunction<typeof fetchPromoCode>;
  mockFetch.mockResolvedValue({ code: 'SAVE10', valid: true });

  // Act
  const result = await validatePromoCode('SAVE10');

  // Assert
  expect(result).toBe(true);
  expect(mockFetch).toHaveBeenCalledWith('SAVE10');
});
```

**❌ Wrong - Mocking internal functions:**
```typescript
import { calculateDiscount, validatePromoCode } from './promo';
jest.mock('./promo'); // Mocking your own code!

test('applies promo code', () => {
  validatePromoCode.mockReturnValue(true);
  calculateDiscount.mockReturnValue(90);
  // Not testing real integration
});
```

**Why wrong:** Not testing real code, just testing mocks.

### Good: RTL Component Test

**✅ Correct - Uses accessibility queries, tests behaviour:**
```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('shows error message for invalid credentials', async () => {
    const onSubmit = jest.fn().mockRejectedValue(new Error('Invalid credentials'));
    render(<LoginForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'wrongpassword');
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid credentials');
  });
});
```

**❌ Wrong - Testing implementation details:**
```typescript
it('sets error state', async () => {
  const { result } = renderHook(() => useLoginForm());
  act(() => {
    result.current.setError('Some error');
  });
  expect(result.current.error).toBe('Some error');
});
```

**Why wrong:** Tests internal state, not user-visible behaviour.

### Good: Descriptive Test Names

**✅ Correct - Describes behaviour:**
```typescript
describe('Promo code validation', () => {
  test('rejects expired promo code', () => { ... });
  test('accepts active promo code within date range', () => { ... });
  test('throws error when promo code not found', () => { ... });
});
```

**❌ Wrong - Vague names:**
```typescript
describe('Promo codes', () => {
  test('test 1', () => { ... });
  test('works', () => { ... });
  test('error case', () => { ... });
});
```

**Why wrong:** When tests fail, names don't help diagnose issue.

### Good: RTL Tests for Complex Components with Dialogs

**Pattern for components with dialogs, dropdowns, and role-based actions:**

```typescript
// src/components/org/UserList.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserList } from './UserList';

const mockUsers = [
  { id: '1', email: 'owner@org.com', role: 'owner' },
  { id: '2', email: 'admin@org.com', role: 'admin' },
];

describe('UserList', () => {
  // Test permission-based visibility
  it('shows invite button for admin users', () => {
    render(<UserList users={mockUsers} currentUserRole="admin" />);
    expect(screen.getByTestId('invite-user-button')).toBeInTheDocument();
  });

  it('hides invite button for member users', () => {
    render(<UserList users={mockUsers} currentUserRole="member" />);
    expect(screen.queryByTestId('invite-user-button')).not.toBeInTheDocument();
  });

  // Test dialog interactions
  it('opens invite dialog and submits', async () => {
    const user = userEvent.setup();
    const onInvite = jest.fn();
    render(<UserList users={mockUsers} currentUserRole="admin" onInvite={onInvite} />);

    await user.click(screen.getByTestId('invite-user-button'));
    await user.type(screen.getByTestId('invite-email-input'), 'new@org.com');
    await user.click(screen.getByTestId('send-invitation-button'));

    expect(onInvite).toHaveBeenCalledWith('new@org.com', expect.any(String));
  });

  // Test dropdown menu actions
  it('opens action menu and triggers role change', async () => {
    const user = userEvent.setup();
    const onChangeRole = jest.fn();
    render(
      <UserList
        users={mockUsers}
        currentUserRole="owner"
        currentUserEmail="owner@org.com"
        onChangeRole={onChangeRole}
      />
    );

    // Use email-based test IDs for row-specific actions
    await user.click(screen.getByTestId('user-actions-admin-at-org.com'));
    await user.click(screen.getByTestId('change-role-admin-at-org.com'));

    expect(onChangeRole).toHaveBeenCalledWith(
      expect.objectContaining({ email: 'admin@org.com' }),
      expect.any(String)
    );
  });

  // Test confirmation dialogs
  it('requires confirmation before removing user', async () => {
    const user = userEvent.setup();
    const onRemove = jest.fn();
    render(<UserList users={mockUsers} currentUserRole="owner" onRemove={onRemove} />);

    await user.click(screen.getByTestId('user-actions-admin-at-org.com'));
    await user.click(screen.getByTestId('remove-user-admin-at-org.com'));

    // Dialog should appear
    expect(screen.getByText('Remove Team Member')).toBeInTheDocument();

    // Confirm removal
    await user.click(screen.getByTestId('confirm-remove-user'));
    expect(onRemove).toHaveBeenCalled();
  });
});
```

**Key patterns:**
- Use `data-testid` with email-based IDs for row actions: `user-actions-${email.replace('@', '-at-')}`
- Test permission-based visibility (admin vs member vs owner)
- Split callback tests to avoid dialog overlay issues
- Use `waitFor` for async dialog closures

## Common Pitfalls

### 1. Silent Skips and Placeholder Tests
**Problem:** `test.skip()` and `expect(true).toBe(true)` both hide gaps — one silently, the other with false confidence. Neither shows up as "not implemented" in test output.

**Example of what NOT to do:**
```typescript
❌ test('Super Admin can access tenant management API', async () => {
  // TODO: Implement when admin API is deployed
  expect(true).toBe(true); // ALWAYS passes - never catches bugs!
});

❌ test.skip('Super Admin can access tenant management API', async () => {
  // Silently hidden — test runner ignores this entirely
});
```

**Why both are wrong:** `expect(true).toBe(true)` inflates pass counts. `test.skip()` is invisible in output — the test runner pretends it doesn't exist. Both create false confidence: the summary says "400 passed" when 40 scenarios were never verified.

**Solution — use `test.todo()`:**
```typescript
// ✅ Visible in output: reported as "todo" alongside pass/fail counts
test.todo('Super Admin can access tenant management API');

// Test output: Tests: 350 passed, 10 failed, 40 todo
// Clear that 40 scenarios are not yet implemented
```

**When to use each:**
| Approach | When | Visible in output? |
|----------|------|-------------------|
| `test.todo('description')` | Test not yet implemented | YES — reported as "todo" count |
| `test('description', () => { ... })` | Test implemented, should pass | YES — reported as pass/fail |
| `test.skip()` | **NEVER in committed code** | NO — silently hidden |
| `expect(true).toBe(true)` | **NEVER** | Misleading — counts as "passed" |

**The ideal test output shows the full picture:**
```
Tests:  350 passed, 10 failed, 40 todo
Total:  400
```

### 2. Testing Implementation Instead of Behaviour
**Problem:** Tests break when refactoring, even though behaviour unchanged

**Example:**
```typescript
❌ test('calls calculateDiscount with right params', () => {
  const spy = jest.spyOn(module, 'calculateDiscount');
  applyPromoCode(cart, code);
  expect(spy).toHaveBeenCalled(); // Implementation detail
});

✅ test('reduces cart total by 10% when promo code applied', () => {
  const result = applyPromoCode({ total: 100 }, 'SAVE10');
  expect(result.total).toBe(90); // Behaviour
});
```

### 2. Flaky Tests from Timing Issues
**Problem:** Tests pass/fail randomly due to async timing

**Solution:** Use proper async patterns
```typescript
❌ test('loads data', () => {
  loadData();
  expect(data).toBeDefined(); // Might not be loaded yet!
});

✅ test('loads data', async () => {
  await loadData();
  expect(data).toBeDefined(); // Guaranteed loaded
});
```

### 3. Shared State Between Tests
**Problem:** Tests fail when run together, pass in isolation

**Solution:** Reset state in beforeEach
```typescript
✅ beforeEach(() => {
  jest.clearAllMocks();
  // Reset test database
  // Clear test data
});
```

### 4. Over-Mocking
**Problem:** Mocking everything = testing mocks, not code

**Guideline:**
- ✅ Mock: External APIs, databases, file system
- ❌ Don't mock: Your own business logic

### 5. Poor Coverage of Error Cases
**Problem:** Only testing happy paths

**Solution:** Test error scenarios
```typescript
✅ describe('calculateDiscount', () => {
  test('handles negative price', () => {
    expect(() => calculateDiscount(-100, discount))
      .toThrow('Price cannot be negative');
  });

  test('handles discount over 100%', () => {
    expect(() => calculateDiscount(100, { type: 'percentage', value: 150 }))
      .toThrow('Discount cannot exceed 100%');
  });
});
```

### 6. Integration Tests Not Contributing to Coverage
**Problem:** Integration tests exist but production code shows 0% coverage

**Root Cause:** Test helpers duplicate production functionality instead of calling it
```typescript
// ❌ Bad: cognito-helper.ts reimplements listUsers for testing
export async function listTestUsers() {
  return cognitoClient.send(new ListUsersCommand({ ... }));
}

// Tests use helper, production code never called
import { listTestUsers } from '../helpers/cognito-helper';
test('lists users', async () => {
  const users = await listTestUsers(); // 0% coverage on production code!
});
```

**Solution:** Import production code, use helpers only for fixtures
```typescript
// ✅ Good: Import production code
import { listUsers } from '@/lib/cognito-admin';

// Use helpers for test setup only
import { createTestUser } from '../helpers/cognito-helper';

test('listUsers returns B2CUser format', async () => {
  await createTestUser({ email: 'test@example.com' });  // Fixture setup
  const result = await listUsers();                      // Production code!
  expect(result.users[0]).toHaveProperty('email');
});
```

### 7. Gmail Search Query Mismatch
**Problem:** Tests time out waiting for emails that exist but aren't found

**Solution:** Match actual email subjects
```typescript
// Check actual subject line in Gmail first
❌ query: `subject:"verification code"` // Too specific
✅ query: `subject:verify` // Matches "Verify your account"

❌ query: `subject:"invitation"` // Wrong word
✅ query: `subject:invited` // Matches "You've been invited..."
```

### 8. Environment-Specific URL Assertions
**Problem:** Tests pass locally but fail on deployed feature branches

**Solution:** Use environment-agnostic patterns
```typescript
// Only matches localhost
❌ await expect(page).toHaveURL(/^http:\/\/localhost:\d+\/$/);

// Matches any URL ending with /
✅ await expect(page).toHaveURL(/\/$/);
```

### 9. Playwright webServer Fails in CI
**Problem:** `Exit code: 127` when running E2E tests in GitHub Actions

**Root cause:** `webServer` configured to start local dev server with `doppler run`, but CI tests against deployed URLs.

**Solution:** Make `webServer` conditional:
```typescript
// playwright.config.ts
webServer: process.env.CI
  ? undefined  // CI: test against deployed URL
  : {
      command: `doppler run --project ${project} --config dev -- npm run dev`,
      url: `http://localhost:${port}`,
      reuseExistingServer: true,
      timeout: 120000,
    },
```

### 10. Amplify Auth Session Lost on Navigation
**Problem:** User signs in successfully, but `page.goto('/settings')` loses auth session.

**Root cause:**
- `page.goto()` and `window.location.href` trigger full page reloads
- Full reloads can lose React state and auth context before tokens are persisted
- This is especially problematic for **newly created users** whose tokens may still be writing to storage
- `router.push()` does client-side navigation that preserves React state

**Solution:** Use Next.js client-side navigation instead of full page reloads:
```typescript
// BAD - full page reload, may lose auth session
await page.goto('/settings/team');
// Also BAD - same problem
await page.evaluate(() => { window.location.href = '/settings/team'; });

// GOOD - clicking links uses Next.js Link component
await page.click('text=Manage Team');
await expect(page).toHaveURL(/\/settings\/team/);

// GOOD - use Next.js router.push when Link not available
await page.evaluate(() => {
  const nextRouter = (window as unknown as { next?: { router?: { push: (url: string) => void } } }).next?.router;
  if (nextRouter) {
    nextRouter.push('/settings/team');
  } else {
    window.location.href = '/settings/team'; // fallback
  }
});

// ALSO IMPORTANT - wait for auth to stabilize after user creation
await expect(page).toHaveURL(/\/dashboard/, { timeout: 15000 });
await page.waitForLoadState('networkidle'); // tokens are persisted
// NOW safe to navigate
```

**Key insight:** Tests with seeded users often work with `page.goto()` because auth tokens are already persisted. Tests that create users dynamically are more vulnerable because tokens may still be writing to storage.

### 11. CI Tests Fail But Can't Reproduce Locally
**Problem:** Safari tests fail in CI with viewport/timing issues that never occur locally.

**Root cause:** Different test matrix in CI vs local: `process.env.CI ? [Chrome, Safari] : [Chrome]`

**Solution:** **CI/Local parity rule** - Never test in CI what you can't debug locally. Same browser config everywhere:
```typescript
// playwright.config.ts
projects: [
  { name: 'Desktop Chrome', use: { ...devices['Desktop Chrome'] } },
  // Add Safari only after verifying it works locally
],
```

Add Safari later with explicit opt-in (`--project="Mobile Safari"`) only after verifying it works locally.

### 12. Email Links Contain Production URLs But Tests Run Locally
**Problem:** E2E tests extract invitation/verification URLs from emails, but the Lambda sends production/staging URLs while the test database (sandbox) only has the data locally.

**Root cause:**
- Lambda `APP_URL` is set to production/staging environment (e.g., `https://dev.myapp.com`)
- Email contains full URL: `https://dev.myapp.com/invite/abc-123`
- Test navigates to production URL, but invitation record only exists in sandbox database
- Test sees "Invalid Invitation" error

**Solution:** Extract just the path from email links, navigate to local path:
```typescript
// BAD - extracts full URL from email
function extractInvitationLink(emailBody: string): string | null {
  const match = emailBody.match(/https?:\/\/[^\s]+\/invite\/[a-zA-Z0-9-]+/);
  return match ? match[0] : null;  // Returns https://dev.myapp.com/invite/abc-123
}

// GOOD - extract path only, test navigates to local server
function extractInvitationLink(emailBody: string): string | null {
  const patterns = [
    /\/invite\/([a-zA-Z0-9-]+)/,  // Extract token from path
    /href="[^"]*\/invite\/([a-zA-Z0-9-]+)"/,  // Extract from href
  ];
  for (const pattern of patterns) {
    const match = emailBody.match(pattern);
    if (match && match[1]) {
      return `/invite/${match[1]}`;  // Returns /invite/abc-123
    }
  }
  return null;
}

// Test navigates to local path
await page.goto(invitationLink!);  // Goes to localhost:3000/invite/abc-123
```

**Also check:** If tests fail with "Invalid Invitation", verify the Lambda URL pattern matches the app route. Common mismatch: `/accept-invitation?token=xxx` vs `/invite/[token]`.

### 13. E2E Timeout Waiting for Amplify Deployment
**Problem:** E2E workflow times out (15 min) waiting for Amplify deployment.

**Root cause:** Fresh deployments (new User Pool creation) take 18+ minutes. Jobs can also queue behind previous deployments.

**Solution:** Increase timeout and account for queued jobs:
```yaml
# Poll for up to 20 minutes (120 attempts * 10s)
for i in {1..120}; do
  # ... poll logic
  sleep 10
done
```

**Timing reference:**
| Stage | Duration |
|-------|----------|
| Amplify deployment | ~13-14 min |
| CloudFront propagation | 30s |
| E2E test suite | ~1-2 min |
| **Total staging pipeline** | **~17 min** |

## Essential Reading

**For comprehensive testing patterns:**
- [Testing Guide](../../docs/guides/testing-guide.md) - Complete strategy, seed data, Amplify integration

**For email verification in E2E tests:**
- [Gmail Testing Infrastructure](/srv/docs/GMAIL_TESTING.md) - Service account setup, API patterns

**Official documentation:**
- [Jest](https://jestjs.io/) - Unit testing
- [Playwright](https://playwright.dev/) - E2E testing
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) - Component testing

---

**Remember:**
1. Write tests BEFORE implementation (TDD)
2. Test behaviour, not implementation details
3. RTL tests lock component behaviour during Refinement
4. E2E tests use Playwright directly (no Cucumber)
5. Mock external dependencies only
6. 80%+ coverage is required, not optional
