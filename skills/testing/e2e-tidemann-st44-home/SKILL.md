---
name: agent-e2e
description: Playwright expert for end-to-end testing, debugging, test infrastructure, and visual regression testing
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
tags:
  - testing
  - e2e
  - playwright
  - integration
  - automation
version: 1.0.0
---

# E2E Testing Skill

Expert in Playwright end-to-end testing for Angular 21+ applications - test execution, debugging, Page Object Model, and test infrastructure management.

## When to Use This Skill

Use this skill when:

- Running e2e tests (all tests, specific files, or suites)
- Debugging failing or flaky tests
- Creating new e2e tests for features
- Updating page objects or test helpers
- Managing test services (Docker, database)
- Analyzing test coverage
- Troubleshooting test infrastructure
- Setting up e2e testing environment

## Core Principles

### Page Object Model (POM)

- Encapsulate UI interactions in page objects
- Extend `BasePage` for common functionality
- Define locators as private properties
- Create action and query methods
- Improve maintainability and reusability

### AAA (Arrange-Act-Assert) Pattern

- **Arrange**: Set up test data and state
- **Act**: Perform user actions
- **Assert**: Verify expected outcomes
- Structure all tests consistently

### Test Data Isolation

- Reset database before each test
- Seed only required data
- Generate unique test data
- Ensure tests can run independently
- Clean up after tests

### Serial Execution

- Tests run one at a time (workers: 1)
- Prevents database conflicts
- Ensures consistent state
- Easier debugging

## Test Modes

### CI Mode (GitHub Actions)

**Environment**: Ubuntu with PostgreSQL service
**Ports**: Frontend 4200, Backend 3000, Database 55432
**Database**: `st44_test`
**Trigger**: Manual or daily at 2 AM UTC

**How it runs**:

- PostgreSQL service container
- Built frontend and backend
- 4 parallel workers (disabled due to DB conflicts)
- Chromium browser only
- Uploads artifacts on failure

**Workflow**: `.github/workflows/e2e.yml`

### Local Docker Mode

**Environment**: Docker Compose with isolated services
**Ports**: Frontend 4201, Backend 3001, Database 5433
**Database**: `st44_test_local`
**Docker Compose**: `docker-compose.e2e-local.yml`

**How it runs**:

- Full stack in Docker containers
- Isolated from dev environment
- Auto-managed services
- Same environment every time

**Best for**: Complete integration testing, CI-like runs

### Dev Mode

**Environment**: Local dev servers + containerized database
**Ports**: Frontend 4200, Backend 3000, Database 5433
**Database**: `st44_test_local` or dev database

**How it runs**:

- Manual start of frontend/backend
- Database in container
- Uses existing dev servers
- Faster iteration

**Best for**: Rapid test development, debugging

## Running Tests

### Complete Automated Run (Recommended)

```bash
cd apps/frontend
npm run test:e2e:full
```

**What it does**:

1. Starts Docker Compose services
2. Waits for health checks
3. Runs all tests
4. Stops services

**Use when**: Running full test suite, CI-like execution

### Run Tests Only (Services Running)

```bash
npm run test:e2e:local
```

**Prerequisites**: Services already started with `npm run test:e2e:start`

**Use when**: Iterating on tests, services already up

### Interactive UI Mode

```bash
npm run test:e2e:ui
```

**Features**:

- Visual test explorer
- Step through tests
- Pick locators
- View screenshots
- Time travel debugging

**Use when**: Exploring tests, understanding behavior

### Headed Mode (Watch Browser)

```bash
npm run test:e2e:headed
```

**Features**:

- Browser window visible
- See actions in real-time
- Observe page state
- Debug visually

**Use when**: Visual debugging, understanding flow

### Debug Mode (Inspector)

```bash
npm run test:e2e:debug
```

**Features**:

- Playwright Inspector
- Step-by-step execution
- Pick locator tool
- Console logs

**Use when**: Debugging specific issues, selector problems

### Specific Test File

```bash
npx playwright test e2e/auth/login.spec.ts
```

**Use when**: Testing single feature, focused development

### Test Suite by Folder

```bash
npx playwright test e2e/auth/
```

**Use when**: Testing related features, specific domain

### Filter by Name

```bash
npx playwright test --grep "registration"
```

**Use when**: Running tests matching pattern

## Service Management

### Start Services

```bash
npm run test:e2e:start
```

**Starts**:

- PostgreSQL test database (port 5433)
- Backend API server (port 3001)
- Frontend dev server (port 4201)

**Wait time**: ~30-60 seconds for all services

### Stop Services

```bash
npm run test:e2e:stop
```

**Stops**: All Docker Compose services

### Restart Services

```bash
npm run test:e2e:restart
```

**Use when**: Services in bad state, need fresh start

### View Service Logs

```bash
npm run test:e2e:logs
```

**Shows**: Real-time logs from all services

**Use when**: Debugging service issues, API errors

### Reset Database

```bash
npm run test:e2e:reset
```

**What it does**: Truncates all tables, resets sequences

**Use when**: Need clean database state

### Check Service Health

```bash
# Backend health
curl http://localhost:3001/health

# Database connection
docker exec -it st44-postgres-test-local psql -U postgres -d st44_test_local -c "SELECT 1"

# Frontend (check browser)
curl http://localhost:4201
```

## Writing Tests

### Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';
import { MyPage } from '../pages/my.page';
import { resetDatabase, seedTestData } from '../helpers/seed-database';

test.describe('My Feature', () => {
  test.beforeEach(async () => {
    // Arrange: Clean state
    await resetDatabase();
  });

  test('should complete user flow', async ({ page }) => {
    // Arrange: Set up test data
    const testData = await seedTestData({
      user: { email: 'test@example.com', password: 'Test123!' },
    });

    const myPage = new MyPage(page);

    // Act: Perform actions
    await myPage.goto();
    await myPage.performAction();

    // Assert: Verify outcomes
    await expect(page).toHaveURL('/success');
    await expect(myPage.successMessage).toBeVisible();
  });
});
```

### Creating a Page Object

```typescript
import { BasePage } from './base.page';
import { Page } from '@playwright/test';

export class MyPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  // Locators (private)
  private emailInput = this.page.locator('[data-testid="email"]');
  private submitButton = this.page.locator('[data-testid="submit"]');
  public successMessage = this.page.locator('[data-testid="success"]');

  // Actions
  async goto(): Promise<void> {
    await this.page.goto('/my-page');
    await this.waitForLoad();
  }

  async fillEmail(email: string): Promise<void> {
    await this.emailInput.fill(email);
  }

  async submit(): Promise<void> {
    await this.submitButton.click();
    await this.waitForNavigation();
  }

  // Queries
  async isEmailValid(): Promise<boolean> {
    const classes = await this.emailInput.getAttribute('class');
    return !classes?.includes('invalid');
  }
}
```

### Database Seeding

```typescript
import { seedTestData, resetDatabase } from '../helpers/seed-database';

// Full scenario (user, household, children, tasks)
const scenario = await seedTestData({
  parent: { email: 'parent@test.com', password: 'Parent123!' },
  children: [{ name: 'Emma', age: 10 }],
  tasks: [{ title: 'Clean room', ruleType: 'daily' }],
});

// Access seeded data
const userId = scenario.user.userId;
const householdId = scenario.household.id;
const childId = scenario.children[0].id;

// Reset database
await resetDatabase();
```

### Authentication in Tests

```typescript
import { loginAsUser } from '../helpers/auth-helpers';

test.beforeEach(async ({ page }) => {
  await resetDatabase();
  const user = await seedTestUser({
    email: 'test@example.com',
    password: 'Test123!',
  });

  // Login via helper
  await loginAsUser(page, user.email, 'Test123!');

  // Now on dashboard, authenticated
});
```

## Debugging

### Playwright UI Mode (Best Option)

```bash
npm run test:e2e:ui
```

**Features**:

- Visual test explorer
- Click to run tests
- Step through execution
- Pick locators visually
- View DOM and network
- Time travel debugging

**Workflow**:

1. Start UI mode
2. Select test to run
3. Click play to execute
4. Pause and inspect at any point
5. Use "Pick Locator" to find selectors
6. View screenshots and videos

### Playwright Inspector

```bash
npm run test:e2e:debug
```

**Features**:

- Step-by-step execution
- Pause at any point
- Inspect page state
- Generate selectors
- View console logs

### VS Code Debugging

**Launch Configurations** (already set up):

- "Debug E2E Tests" - All tests with auto-start
- "Debug Current E2E Test" - Current file only
- "Debug E2E with Inspector" - Playwright UI
- "Debug E2E (Services Running)" - Skip service start

**Usage**:

1. Open test file
2. Set breakpoint
3. Press F5 or use Run & Debug
4. Step through with F10/F11
5. Inspect variables

### Screenshots and Videos

**Location**: `apps/frontend/test-results/<test-name>/`

**Files**:

- `screenshot.png` - Screenshot on failure
- `video.webm` - Video recording (if enabled)
- `trace.zip` - Complete trace file

**View trace**:

```bash
npx playwright show-trace test-results/<test-name>/trace.zip
```

### Console Logging

```typescript
test('debug example', async ({ page }) => {
  console.log('Test starting');

  // Log page title
  console.log('Title:', await page.title());

  // Log element text
  const text = await page.locator('h1').textContent();
  console.log('Heading:', text);

  // Monitor network
  page.on('response', (resp) => {
    console.log(`${resp.status()} ${resp.url()}`);
  });
});
```

## Test Structure

### Directory Organization

```
apps/frontend/e2e/
├── auth/                    # Authentication tests
│   ├── login.spec.ts       # Login flow (13 tests)
│   └── registration.spec.ts # Registration flow (17 tests)
├── features/                # Feature-specific tests
│   ├── task-templates.spec.ts
│   ├── task-viewing-completion.spec.ts
│   ├── task-form-button.spec.ts
│   └── manual-assignment.spec.ts
├── infrastructure/          # System tests
│   └── database.spec.ts
├── ux-redesign/            # UX-specific tests
│   ├── dashboard.spec.ts
│   ├── family.spec.ts
│   ├── navigation.spec.ts
│   ├── progress.spec.ts
│   └── tasks.spec.ts
├── pages/                   # Page objects (POM)
│   ├── base.page.ts        # Base class
│   ├── login.page.ts
│   ├── register.page.ts
│   ├── home.page.ts
│   ├── family.page.ts
│   ├── tasks.page.ts
│   └── progress.page.ts
├── helpers/                 # Test utilities
│   ├── auth-helpers.ts     # Login, logout
│   ├── api-helpers.ts      # API requests
│   ├── seed-database.ts    # Database seeding
│   └── test-helpers.ts     # Common utilities
└── example.spec.ts         # Basic example
```

### Test Coverage

- **Total Test Files**: 11 spec files
- **Total Page Objects**: 7 (including base)
- **Total Helpers**: 4

## Common Patterns

### Wait for Navigation

```typescript
await page.click('[data-testid="submit"]');
await page.waitForURL('/dashboard');
```

### Wait for Element

```typescript
await page.waitForSelector('[data-testid="welcome"]');
await expect(page.locator('[data-testid="welcome"]')).toBeVisible();
```

### Wait for Network

```typescript
await page.click('[data-testid="load-data"]');
await page.waitForResponse((resp) => resp.url().includes('/api/tasks') && resp.status() === 200);
```

### Wait for Load State

```typescript
await page.goto('/dashboard');
await page.waitForLoadState('networkidle');
```

### Error Handling

```typescript
test('should show error message', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('invalid@example.com', 'wrong');

  const error = await loginPage.getErrorMessage();
  expect(error).toContain('Invalid credentials');
});
```

### Multiple Assertions

```typescript
test('should display user data', async ({ page }) => {
  await page.goto('/profile');

  await expect(page.locator('[data-testid="name"]')).toHaveText('John Doe');
  await expect(page.locator('[data-testid="email"]')).toHaveText('john@example.com');
  await expect(page.locator('[data-testid="avatar"]')).toBeVisible();
});
```

## Troubleshooting

### Port Already in Use

**Symptom**: `Error: bind: address already in use`

**Solution**:

```bash
# Find process (Windows)
netstat -ano | findstr :5433
netstat -ano | findstr :3001
netstat -ano | findstr :4201

# Kill process
taskkill /PID <process_id> /F

# Or change ports in .env.e2e-local
```

### Services Won't Start

**Symptom**: Timeout waiting for services

**Solution**:

```bash
# Check Docker running
docker ps

# View logs
npm run test:e2e:logs

# Check backend health
curl http://localhost:3001/health

# Restart services
npm run test:e2e:restart
```

### Database Connection Errors

**Symptom**: `connect ECONNREFUSED` or `password authentication failed`

**Solution**:

```bash
# Verify container running
docker ps | findstr postgres-test

# Test connection
docker exec -it st44-postgres-test-local psql -U postgres -d st44_test_local

# Reset database
npm run test:e2e:reset
```

### Tests Timeout

**Symptom**: `Timeout 30000ms exceeded`

**Solution**:

```typescript
// Increase test timeout
test('slow operation', async ({ page }) => {
  test.setTimeout(60000); // 60 seconds
  // ...
});

// Use proper waits
await page.waitForLoadState('networkidle');
await page.waitForSelector('[data-testid="result"]');
```

### Flaky Tests

**Symptom**: Tests pass/fail inconsistently

**Solution**:

```typescript
// Replace fixed timeouts
// ❌ Bad
await page.waitForTimeout(2000);

// ✅ Good
await page.waitForSelector('[data-testid="loaded"]');

// Add explicit waits
await page.waitForLoadState('networkidle');

// Ensure test independence
test.beforeEach(async () => {
  await resetDatabase();
});
```

### Selector Not Found

**Symptom**: `Error: locator.click: Timeout waiting for selector`

**Solution**:

```typescript
// Use Playwright UI to pick locator
npm run test:e2e:ui

// Or use data-testid
<button data-testid="submit">Submit</button>
await page.click('[data-testid="submit"]');

// Check element exists
const exists = await page.locator('[data-testid="submit"]').count();
console.log('Button count:', exists);
```

### CI Tests Fail, Local Pass

**Common causes**:

- Port differences (use environment variables)
- Timing differences (add proper waits)
- Database state (ensure test independence)
- Environment variables (match CI config)

**Solution**:

```bash
# Run in CI mode locally
CI=true npm run test:e2e
```

## Best Practices

### Selector Priority

1. **data-testid** (best):

   ```typescript
   await page.click('[data-testid="submit-button"]');
   ```

2. **Role + name** (semantic):

   ```typescript
   await page.click('role=button[name="Submit"]');
   ```

3. **Label** (forms):

   ```typescript
   await page.fill('input[placeholder="Email"]', 'test@example.com');
   ```

4. **Text** (user-visible):

   ```typescript
   await page.click('text=Submit');
   ```

5. **CSS classes** (avoid):
   ```typescript
   // ❌ Fragile
   await page.click('.btn.btn-primary');
   ```

### Test Independence

```typescript
// ✅ Good - Each test is self-contained
test.beforeEach(async () => {
  await resetDatabase();
});

test('test 1', async ({ page }) => {
  const user = await seedTestUser({ ... });
  // Test uses own data
});

test('test 2', async ({ page }) => {
  const user = await seedTestUser({ ... });
  // Also uses own data, can run alone
});
```

### Wait Strategies

```typescript
// ✅ Good
await page.click('[data-testid="submit"]');
await page.waitForURL('/success');

// ✅ Good
await page.click('[data-testid="load"]');
await page.waitForResponse((r) => r.url().includes('/api/data'));

// ❌ Bad
await page.click('[data-testid="submit"]');
await page.waitForTimeout(2000); // Arbitrary wait
```

### Error Messages

```typescript
// ✅ Good - Descriptive
await expect(page.locator('[data-testid="household"]')).toBeVisible({
  message: 'Household should appear after creation',
});

// ❌ Bad - No context
await expect(page.locator('[data-testid="household"]')).toBeVisible();
```

### Cleanup

```typescript
test.beforeEach(async () => {
  await resetDatabase(); // Fresh state for every test
});

test.afterAll(async () => {
  // Optional: Additional cleanup
  await cleanupResources();
});
```

## Configuration

### playwright.config.ts

Key settings:

```typescript
export default defineConfig({
  testDir: './e2e',
  fullyParallel: false, // Disabled for DB consistency
  workers: 1, // Serial execution
  timeout: 30000, // 30 second timeout
  retries: 2, // Retry twice in CI
  use: {
    baseURL: `http://${frontendHost}:${frontendPort}`,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [{ name: 'chromium' }],
});
```

### Environment Variables

**Local Docker**:

- `FRONTEND_PORT=4201`
- `BACKEND_PORT=3001`
- `DB_PORT=5433`
- `DB_NAME=st44_test_local`
- `USE_DOCKER_COMPOSE=true`

**CI**:

- `FRONTEND_PORT=4200`
- `BACKEND_PORT=3000`
- `DB_PORT=55432`
- `DB_NAME=st44_test`
- `USE_DOCKER_COMPOSE=false`
- `CI=true`

## Success Criteria

Before marking E2E work complete:

- [ ] All tests pass locally (headless)
- [ ] All tests pass in headed mode
- [ ] Tests follow AAA pattern
- [ ] Page objects used for UI interactions
- [ ] Tests are independent
- [ ] Database reset before each test
- [ ] No fixed timeouts used
- [ ] Proper wait strategies implemented
- [ ] Selectors use data-testid when possible
- [ ] Error cases covered
- [ ] Tests documented
- [ ] No flaky tests

## Comparing with Live Behavior

Use Chrome browser tools to compare e2e test expectations with actual production behavior at **home.st44.no**.

### When to Use

- E2e test assertions don't match live behavior
- Investigating discrepancies between local and production
- Verifying fixes deployed correctly
- Understanding production state for test updates

### Comparison Workflow

```bash
# 1. Run e2e test locally to see expected behavior
npm run test:e2e:ui

# 2. Check live site
tabs_context_mcp(createIfEmpty: true)
navigate(url: "https://home.st44.no", tabId: <id>)
computer(action: "screenshot", tabId: <id>)

# 3. Read page structure
read_page(tabId: <id>)

# 4. Compare with test assertions
# - Check element presence
# - Verify text content
# - Confirm state matches expectations

# 5. Update tests or file bug as needed
```

### Example: Comparing Login Flow

```bash
# Local e2e test expects:
# - "Welcome Back!" heading
# - Email and Password fields
# - "Log In" button

# Check live site:
tabs_context_mcp(createIfEmpty: true)
navigate(url: "https://home.st44.no/login", tabId: <id>)
computer(action: "screenshot", tabId: <id>)
read_page(tabId: <id>, filter: "interactive")

# Compare elements with test assertions
find(query: "login button", tabId: <id>)
find(query: "email input", tabId: <id>)
```

### Test vs Production Differences

Common causes of discrepancies:

- **Different data**: Test database vs production data
- **Feature flags**: Features enabled differently
- **Caching**: Browser/CDN cache differences
- **Timing**: Animation/load timing differences
- **Environment**: API URL, config differences

When differences found:

1. Determine if test or production is "correct"
2. Update test expectations if production is correct
3. File bug if production behavior is wrong

## Related Resources

### Documentation

- **E2E Agent**: `.claude/agents/agent-e2e.md` - Comprehensive agent for e2e tasks
- **E2E Guide**: `docs/E2E.md` - Complete testing documentation
- **Playwright Docs**: https://playwright.dev/docs/intro

### Key Files

- **Playwright Config**: `apps/frontend/playwright.config.ts`
- **Docker Compose**: `docker-compose.e2e-local.yml`
- **CI Workflow**: `.github/workflows/e2e.yml`
- **Test Helpers**: `apps/frontend/e2e/helpers/`
- **Page Objects**: `apps/frontend/e2e/pages/`

### Quick Commands

```bash
# Complete run
npm run test:e2e:full

# Interactive debugging
npm run test:e2e:ui

# Specific test
npx playwright test e2e/auth/login.spec.ts

# View report
npx playwright show-report

# Service management
npm run test:e2e:start
npm run test:e2e:logs
npm run test:e2e:stop
```
