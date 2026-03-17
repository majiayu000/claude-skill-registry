---
name: playwright-frontend-testing
description: "Use when testing frontend applications. AI-assisted browser testing with Playwright MCP. Fast, deterministic, no vision models needed."
---

# Playwright Frontend Testing

## Core Principle

**Test real browser behavior with AI assistance through Playwright's accessibility tree.**

## Overview

Playwright MCP (Model Context Protocol) enables AI-assisted frontend testing by exposing browser interactions through structured data instead of screenshots. This makes tests fast, deterministic, and LLM-friendly without requiring vision models.

## When to Use This Skill

- Testing web application user interfaces
- End-to-end testing with real browsers
- Cross-browser compatibility testing
- Testing interactive features (forms, buttons, navigation)
- Accessibility testing
- **Brand compliance testing** (verify colors, fonts match guidelines)
- Visual regression testing
- Integration testing with real browser state

## Why Playwright MCP?

**Traditional Approach (Screenshots):**
- ❌ Slow (large image processing)
- ❌ Non-deterministic (OCR, vision models)
- ❌ Expensive (vision model costs)
- ❌ Brittle (pixel-based matching)

**Playwright MCP Approach (Accessibility Tree):**
- ✅ Fast (structured data)
- ✅ Deterministic (semantic interactions)
- ✅ Lightweight (no vision models)
- ✅ LLM-friendly (text-based)
- ✅ Accessibility-first (follows a11y best practices)
- ✅ **Headless-ready** (works on VPS/servers without display)

**Works anywhere:**
- 💻 Local development (headed mode for debugging)
- 🖥️ **VPS/Headless Servers** (Claude Code CLI, no display required)
- 🔄 CI/CD pipelines (automated testing)
- 🌐 Remote SSH sessions (full browser testing over SSH)

## Recommended Workflow: Hybrid Approach

**⭐ ALWAYS use this workflow for the best results:**

### Phase 1: Exploratory Testing with MCP (Discovery)

**Purpose**: Find issues quickly through interactive testing

```
1. Use Playwright MCP interactively with AI assistance
2. Navigate application, test features manually
3. Document bugs/issues as you find them
4. Iterate quickly - no test files needed yet
```

**Benefits:**
- ✅ Fast discovery - find issues immediately
- ✅ Interactive - adjust approach based on findings
- ✅ No maintenance overhead during exploration
- ✅ Good for understanding application behavior
- ✅ AI-assisted - Claude helps navigate via accessibility tree

**When to use:**
- First-time testing of new features
- Exploring unfamiliar codebases
- Quick smoke testing
- Finding UI/UX issues

### Phase 2: Write Permanent Test Suite (CI/CD)

**Purpose**: Lock in findings as regression protection

```
1. Based on MCP exploration, write .spec.js/.spec.ts files
2. Cover critical paths discovered during exploration
3. Add to CI/CD pipeline
4. Team can run tests locally
```

**Benefits:**
- ✅ Permanent regression protection
- ✅ Runs in CI/CD automatically
- ✅ Prevents future bugs
- ✅ Team collaboration
- ✅ Documentation of expected behavior

**When to use:**
- After exploratory testing finds issues
- For critical user flows
- When code is changing frequently
- For long-term quality assurance

### The Hybrid Workflow

```
Step 1: MCP Exploration (Quick Discovery)
→ Use Playwright MCP interactively
→ Find bugs, understand flows
→ Document issues found

Step 2: Write Permanent Tests (Lock It In)
→ Create .spec.ts files for critical paths
→ Add assertions for bugs found in Step 1
→ Commit to repository

Step 3: CI/CD Integration (Prevent Regressions)
→ Tests run on every commit
→ Catch regressions automatically
→ Team protected from breaking changes
```

**Example workflow:**

```bash
# Phase 1: Interactive exploration
# Use Claude Code with Playwright MCP
# Test login flow, find validation bug

# Phase 2: Write permanent test
cat > tests/auth.spec.ts << 'EOF'
test('login validates email format', async ({ page }) => {
  await page.goto('https://app.example.com/login');
  await page.fill('[name="email"]', 'invalid-email');
  await page.click('button[type="submit"]');

  // Bug found during MCP exploration: error message missing
  await expect(page.locator('.error')).toContainText('Invalid email format');
});
EOF

# Phase 3: Run in CI/CD
# Add to .github/workflows/test.yml
# Tests now run on every PR
```

### Why Hybrid is Best

| Approach | Speed | Permanence | CI/CD | Best For |
|----------|-------|------------|-------|----------|
| MCP Only | ⚡ Fast | ❌ No | ❌ No | Quick audits, exploration |
| Tests Only | 🐢 Slow | ✅ Yes | ✅ Yes | Known requirements |
| **Hybrid** | ⚡🔒 **Both** | ✅ **Yes** | ✅ **Yes** | **Everything** |

**The Iron Law**: Never write permanent tests blindly - explore with MCP first to understand what actually needs testing.

## Installation & Setup

### Step 1: Install Playwright MCP

**For MCP-compatible tools (Claude Desktop, VS Code, Cursor):**

Add to MCP configuration file:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**Configuration file locations:**
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac)
- **VS Code**: `.vscode/settings.json` (project) or user settings
- **Cursor**: Similar to VS Code
- **Claude Code (CLI)**: `.claude/mcp_config.json` (project) or `~/.config/claude-code/mcp_config.json` (global)

### Step 2: Configure for Claude Code CLI (Headless Servers/VPS)

**Claude Code works perfectly on headless servers** - the MCP server runs browsers in headless mode without requiring a display.

**Recommended configuration for VPS/headless servers:**

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--headless",
        "--browser", "chromium"
      ]
    }
  }
}
```

**For servers without X11/display:**

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2

# Install Playwright browsers (headless)
npx playwright install chromium
```

**Verify headless mode works:**

```bash
# Test headless browser
npx playwright test --headed=false

# Or with MCP via Claude Code
# Playwright MCP automatically uses headless mode on servers without displays
```

**Key benefits for VPS/server usage:**
- ✅ No display/X11 required
- ✅ Runs in background
- ✅ Perfect for CI/CD pipelines
- ✅ Lower resource usage than headed mode
- ✅ Claude Code CLI works identically on server and local

### Step 3: Configure Browser Options (General)

**Headless mode** (CI/CD):
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--headless",
        "--browser", "chromium"
      ]
    }
  }
}
```

**Headed mode** (development, debugging):
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--browser", "chromium",
        "--viewport-size", "1280x720"
      ]
    }
  }
}
```

**Persistent profile** (keep login state):
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--user-data-dir", "./playwright-profile"
      ]
    }
  }
}
```

**Isolated sessions** (fresh each time):
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--isolated"
      ]
    }
  }
}
```

### Step 3: Install Playwright in Project

```bash
# For Node.js projects
npm install --save-dev @playwright/test

# For Python projects
pip install playwright
playwright install

# For other languages
# See: https://playwright.dev/docs/intro
```

### Step 4: Initialize Playwright Tests

```bash
# Node.js
npx playwright install
npx playwright test --init

# Creates:
# - playwright.config.ts
# - tests/ directory
# - example.spec.ts
```

## Core Playwright MCP Capabilities

### 1. Browser Navigation

```typescript
// Navigate to URL
await page.goto('https://example.com');

// Go back/forward
await page.goBack();
await page.goForward();

// Reload page
await page.reload();
```

### 2. Element Interactions

**AI-assisted clicking** (via MCP):
```
Ask AI: "Click the login button"
→ AI uses accessibility tree to find button
→ Clicks correct element
```

**Programmatic clicking**:
```typescript
// Click by text
await page.click('text=Login');

// Click by role
await page.click('role=button[name="Login"]');

// Click by test ID
await page.click('[data-testid="login-btn"]');
```

### 3. Form Filling

```typescript
// Fill input
await page.fill('input[name="email"]', 'user@example.com');
await page.fill('input[name="password"]', 'password123');

// Select dropdown
await page.selectOption('select[name="country"]', 'USA');

// Check checkbox
await page.check('input[type="checkbox"][name="terms"]');

// Upload file
await page.setInputFiles('input[type="file"]', 'path/to/file.pdf');
```

### 4. Assertions

```typescript
// Element visible
await expect(page.locator('text=Welcome')).toBeVisible();

// Text content
await expect(page.locator('h1')).toHaveText('Dashboard');

// Count elements
await expect(page.locator('.todo-item')).toHaveCount(5);

// URL
await expect(page).toHaveURL('https://example.com/dashboard');

// Screenshot comparison
await expect(page).toHaveScreenshot();
```

### 5. Accessibility Tree

**Get page snapshot** (MCP capability):
```
Ask AI: "Get accessibility snapshot of the page"
→ Returns structured accessibility tree
→ Shows all interactive elements
→ Includes roles, labels, states
```

**Programmatic access**:
```typescript
const snapshot = await page.accessibility.snapshot();
console.log(JSON.stringify(snapshot, null, 2));
```

## Writing Effective Playwright Tests

### Test Structure (AAA Pattern)

```typescript
import { test, expect } from '@playwright/test';

test('user can login successfully', async ({ page }) => {
  // Arrange: Navigate and setup
  await page.goto('https://example.com/login');

  // Act: Perform actions
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Assert: Verify outcomes
  await expect(page).toHaveURL('https://example.com/dashboard');
  await expect(page.locator('text=Welcome back')).toBeVisible();
});
```

---

## Brand Compliance Testing

**Validate that implementation matches brand guidelines.**

### When Brand Guidelines Exist

**Check for `.claude/BRAND-GUIDELINES.md` before testing:**

```
1. If brand guidelines exist:
   - Read color palette specifications
   - Read typography specifications
   - Read visual style requirements

2. Create tests to verify compliance:
   - Color validation
   - Typography validation
   - Spacing/sizing validation
   - Visual style validation
```

### Brand Validation Tests

#### Test 1: Color Compliance

```typescript
test('should use brand colors', async ({ page }) => {
  await page.goto('https://example.com');

  // Read brand guidelines (manually or from file)
  const brandPrimary = '#2563EB';  // From .claude/BRAND-GUIDELINES.md
  const brandSecondary = '#7C3AED';

  // Get computed styles
  const button = page.locator('button[data-testid="primary-cta"]');
  const bgColor = await button.evaluate(el =>
    window.getComputedStyle(el).backgroundColor
  );

  // Convert RGB to HEX and compare
  expect(rgbToHex(bgColor)).toBe(brandPrimary);
});
```

#### Test 2: Typography Compliance

```typescript
test('should use brand typography', async ({ page }) => {
  await page.goto('https://example.com');

  // From brand guidelines
  const brandHeadingFont = 'Playfair Display';
  const brandBodyFont = 'Inter';

  // Check heading font
  const heading = page.locator('h1').first();
  const headingFont = await heading.evaluate(el =>
    window.getComputedStyle(el).fontFamily
  );
  expect(headingFont).toContain(brandHeadingFont);

  // Check body font
  const paragraph = page.locator('p').first();
  const bodyFont = await paragraph.evaluate(el =>
    window.getComputedStyle(el).fontFamily
  );
  expect(bodyFont).toContain(brandBodyFont);
});
```

#### Test 3: Spacing System Compliance

```typescript
test('should use brand spacing system', async ({ page }) => {
  await page.goto('https://example.com');

  // From brand guidelines: --space-md: 1rem (16px)
  const brandSpacingMd = '16px';

  const section = page.locator('section').first();
  const padding = await section.evaluate(el =>
    window.getComputedStyle(el).padding
  );

  // Verify consistent spacing
  expect(padding).toContain(brandSpacingMd);
});
```

#### Test 4: Visual Style Compliance

```typescript
test('should match brand visual style', async ({ page }) => {
  await page.goto('https://example.com');

  // From brand guidelines: Border radius should be --radius-md: 0.5rem (8px)
  const brandBorderRadius = '8px';

  const card = page.locator('[data-testid="card"]').first();
  const borderRadius = await card.evaluate(el =>
    window.getComputedStyle(el).borderRadius
  );

  expect(borderRadius).toBe(brandBorderRadius);
});
```

### Brand Audit Test Suite

**Complete test file for brand validation:**

```typescript
// tests/brand-compliance.spec.ts
import { test, expect } from '@playwright/test';

// Load brand guidelines
const BRAND_COLORS = {
  primary: '#2563EB',
  secondary: '#7C3AED',
  accent: '#F59E0B',
};

const BRAND_FONTS = {
  heading: 'Playfair Display',
  body: 'Inter',
};

test.describe('Brand Compliance', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://example.com');
  });

  test('primary buttons use brand primary color', async ({ page }) => {
    const buttons = page.locator('button.btn-primary');
    const count = await buttons.count();

    for (let i = 0; i < count; i++) {
      const bgColor = await buttons.nth(i).evaluate(el =>
        window.getComputedStyle(el).backgroundColor
      );
      expect(rgbToHex(bgColor)).toBe(BRAND_COLORS.primary);
    }
  });

  test('all headings use brand heading font', async ({ page }) => {
    const headings = page.locator('h1, h2, h3, h4, h5, h6');
    const count = await headings.count();

    for (let i = 0; i < count; i++) {
      const fontFamily = await headings.nth(i).evaluate(el =>
        window.getComputedStyle(el).fontFamily
      );
      expect(fontFamily).toContain(BRAND_FONTS.heading);
    }
  });

  test('body text uses brand body font', async ({ page }) => {
    const paragraphs = page.locator('p, span, div');
    const sample = await paragraphs.first().evaluate(el =>
      window.getComputedStyle(el).fontFamily
    );
    expect(sample).toContain(BRAND_FONTS.body);
  });

  test('links use brand accent color', async ({ page }) => {
    const links = page.locator('a');
    const firstLink = links.first();
    const color = await firstLink.evaluate(el =>
      window.getComputedStyle(el).color
    );
    expect(rgbToHex(color)).toBe(BRAND_COLORS.accent);
  });
});

// Helper function
function rgbToHex(rgb: string): string {
  const match = rgb.match(/\d+/g);
  if (!match) return '';
  const [r, g, b] = match.map(Number);
  return '#' + [r, g, b].map(x => x.toString(16).padStart(2, '0')).join('').toUpperCase();
}
```

### Integration with brand-guidelines Skill

**Workflow:**
```
1. brand-guidelines skill creates .claude/BRAND-GUIDELINES.md
2. playwright-frontend-testing reads guidelines
3. Creates validation tests based on guidelines
4. Runs tests to verify compliance
5. Reports deviations as test failures
```

**Announcing brand testing:**
```
I'm using playwright-frontend-testing with brand compliance validation.

Brand guidelines found at .claude/BRAND-GUIDELINES.md:
- Primary color: #2563EB
- Heading font: Playfair Display
- Body font: Inter

I'll create tests to verify these are correctly implemented.
```

---

### Best Practices

#### 1. Use Semantic Selectors

```typescript
// ✅ Good: Semantic, accessible
await page.click('role=button[name="Submit"]');
await page.click('text=Login');
await page.click('[data-testid="submit-btn"]');

// ❌ Bad: Brittle, implementation details
await page.click('.btn-primary.submit-button');
await page.click('#form > div > button:nth-child(3)');
```

#### 2. Wait for Conditions (Not Timeouts)

```typescript
// ✅ Good: Wait for specific condition
await page.waitForSelector('text=Success', { state: 'visible' });

// ❌ Bad: Arbitrary timeout
await page.waitForTimeout(2000);
```

**Note**: This integrates with `condition-based-waiting` skill!

#### 3. Use Test IDs for Dynamic Content

```typescript
// HTML
<button data-testid="submit-btn">Submit</button>

// Test
await page.click('[data-testid="submit-btn"]');
```

#### 4. Isolate Tests

```typescript
// ✅ Good: Each test is independent
test.beforeEach(async ({ page }) => {
  // Setup fresh state
  await page.goto('https://example.com');
});

// ❌ Bad: Tests depend on each other
// Test 1 creates user
// Test 2 assumes user exists
```

#### 5. Handle Network Conditions

```typescript
// Wait for API calls
await page.waitForResponse('**/api/users');

// Mock API responses
await page.route('**/api/users', route => {
  route.fulfill({
    status: 200,
    body: JSON.stringify({ users: [] })
  });
});

// Simulate slow network
await page.route('**/*', route => {
  setTimeout(() => route.continue(), 1000);
});
```

## AI-Assisted Testing with MCP

### Workflow

1. **AI analyzes page accessibility tree**
2. **AI identifies interactive elements**
3. **AI performs actions semantically**
4. **AI verifies outcomes**

### Example Session

```
You: "Test the login flow on example.com"

AI: "I'm using the playwright-frontend-testing skill to test the login flow.

Step 1: Navigate to login page
[Uses MCP browser_navigate]

Step 2: Get page accessibility snapshot
[Uses MCP to understand page structure]

Found:
- Email input (role: textbox, name: 'Email')
- Password input (role: textbox, name: 'Password')
- Submit button (role: button, name: 'Sign In')

Step 3: Fill credentials
[Uses MCP browser_fill]

Step 4: Click submit
[Uses MCP browser_click]

Step 5: Verify redirect
[Checks URL changed to /dashboard]

Step 6: Verify success message
[Finds 'Welcome' text in accessibility tree]

✅ Login flow test passed"
```

## Configuration File (playwright.config.ts)

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // Test directory
  testDir: './tests',

  // Timeout per test
  timeout: 30000,

  // Retry failed tests
  retries: process.env.CI ? 2 : 0,

  // Run tests in parallel
  workers: process.env.CI ? 1 : undefined,

  // Reporter
  reporter: [
    ['html'],
    ['list'],
    ['junit', { outputFile: 'test-results/junit.xml' }]
  ],

  // Shared settings
  use: {
    // Base URL
    baseURL: 'http://localhost:3000',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Video on failure
    video: 'retain-on-failure',

    // Trace on failure
    trace: 'on-first-retry',
  },

  // Browser projects
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],

  // Web server (optional)
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

## Common Testing Patterns

### Pattern 1: Login Helper

```typescript
// tests/helpers/auth.ts
export async function login(page, email, password) {
  await page.goto('/login');
  await page.fill('input[name="email"]', email);
  await page.fill('input[name="password"]', password);
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard');
}

// tests/dashboard.spec.ts
import { test } from '@playwright/test';
import { login } from './helpers/auth';

test('user can access dashboard', async ({ page }) => {
  await login(page, 'user@example.com', 'password123');
  // Test dashboard...
});
```

### Pattern 2: Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('input[name="email"]', email);
    await this.page.fill('input[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }

  async getErrorMessage() {
    return this.page.locator('.error-message').textContent();
  }
}

// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test('shows error for invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('invalid@example.com', 'wrong');

  const error = await loginPage.getErrorMessage();
  expect(error).toBe('Invalid email or password');
});
```

### Pattern 3: API Mocking

```typescript
test('handles API errors gracefully', async ({ page }) => {
  // Mock API to return error
  await page.route('**/api/login', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server error' })
    });
  });

  await page.goto('/login');
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Verify error message shown
  await expect(page.locator('.error-message')).toContainText('Server error');
});
```

### Pattern 4: Visual Regression

```typescript
test('homepage looks correct', async ({ page }) => {
  await page.goto('/');

  // Take screenshot and compare
  await expect(page).toHaveScreenshot('homepage.png', {
    fullPage: true,
    maxDiffPixels: 100
  });
});
```

### Pattern 5: Accessibility Testing

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('page has no accessibility violations', async ({ page }) => {
  await page.goto('/');

  const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

## Hybrid Workflow in Practice

### Example: Testing E-commerce Checkout Flow

**Phase 1: MCP Exploration (Interactive Discovery)**

```
You: "Test the checkout flow on https://shop.example.com"

Claude (via MCP):
1. Navigating to shop.example.com
2. Adding item to cart...
3. Clicking checkout button...
4. Found issue: checkout button disabled without error message
5. Filling shipping form...
6. Found issue: ZIP code doesn't validate Canadian postal codes
7. Submitting payment...
8. Success! Order completed.

Issues found:
- Checkout button provides no feedback when disabled
- ZIP validation rejects valid Canadian postal codes (H3Z 2Y7)
- Success message could be clearer
```

**Phase 2: Write Permanent Tests (Lock In Findings)**

```typescript
// tests/checkout.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Checkout Flow', () => {
  test('shows error when checkout clicked with empty cart', async ({ page }) => {
    // Bug found during MCP exploration
    await page.goto('https://shop.example.com');
    await page.click('[data-testid="checkout-btn"]');

    // Should show error, not just disable button
    await expect(page.locator('.error')).toContainText('Cart is empty');
  });

  test('accepts Canadian postal codes', async ({ page }) => {
    // Bug found during MCP exploration
    await page.goto('https://shop.example.com/checkout');
    await page.fill('[name="postalCode"]', 'H3Z 2Y7');
    await page.blur('[name="postalCode"]');

    // Should not show validation error
    await expect(page.locator('.field-error')).not.toBeVisible();
  });

  test('shows clear success message after order', async ({ page }) => {
    // Enhancement from MCP exploration
    await page.goto('https://shop.example.com');

    // Complete checkout flow
    await page.click('[data-testid="add-to-cart"]');
    await page.click('[data-testid="checkout-btn"]');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="cardNumber"]', '4242424242424242');
    await page.click('button[type="submit"]');

    // Verify clear success
    await expect(page.locator('.success-message')).toContainText('Order confirmed');
    await expect(page.locator('.order-number')).toBeVisible();
  });
});
```

**Phase 3: CI/CD Integration**

```yaml
# .github/workflows/test.yml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

### Workflow Summary

```
MCP Exploration → Found 3 Issues → Wrote 3 Tests → CI/CD Catches Regressions

Before: Manual testing, issues slip through
After: Automated protection, bugs caught early
```

**Time investment:**
- MCP exploration: 10 minutes (found 3 bugs)
- Writing tests: 15 minutes (permanent protection)
- CI/CD setup: 5 minutes (one-time)
- **Total: 30 minutes for permanent regression protection**

**Value:**
- Bugs found: 3 (before users saw them)
- Future regressions prevented: ∞
- Developer confidence: 📈

### When to Skip Permanent Tests

Sometimes MCP exploration is enough:

✅ **Write permanent tests for:**
- Critical user flows (login, checkout, signup)
- Frequently changing features
- Bug-prone areas
- Compliance requirements

❌ **MCP exploration only for:**
- One-time audits
- Prototype testing
- Features scheduled for removal
- Quick sanity checks

**The Iron Law (Reminder)**: Explore first with MCP, then lock it in with tests. Never write tests blindly without understanding the actual user flow.

## Running Tests

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/login.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed

# Run in specific browser
npx playwright test --project=chromium

# Run with UI mode (interactive)
npx playwright test --ui

# Debug mode
npx playwright test --debug

# Generate code (record actions)
npx playwright codegen https://example.com
```

## Integration with Database Backup Skill

**CRITICAL**: When testing involves database operations:

```typescript
import { test } from '@playwright/test';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

test.beforeEach(async () => {
  // Use database-backup skill before tests
  await execAsync('./scripts/backup-database.sh');
});

test('user registration', async ({ page }) => {
  // Test that modifies database
  await page.goto('/register');
  // ... registration flow
});
```

## Integration with TDD Skill

**Follow RED-GREEN-REFACTOR:**

```typescript
// 🔴 RED: Write failing test first
test('user can add todo item', async ({ page }) => {
  await page.goto('/todos');
  await page.fill('input[name="todo"]', 'Buy groceries');
  await page.click('button[type="submit"]');

  await expect(page.locator('.todo-item')).toContainText('Buy groceries');
});

// Run test: ❌ FAILS (feature doesn't exist yet)

// 🟢 GREEN: Implement minimal code to pass
// [Implement todo addition feature]

// Run test: ✅ PASSES

// 🔵 REFACTOR: Improve code while keeping test green
// [Refactor todo code]

// Run test: ✅ STILL PASSES
```

## Docker Support

```dockerfile
# Dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

CMD ["npx", "playwright", "test"]
```

```bash
# Build and run
docker build -t my-playwright-tests .
docker run my-playwright-tests
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Backup database (if needed)
        run: ./scripts/backup-database.sh

      - name: Run Playwright tests
        run: npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

### GitLab CI

```yaml
# .gitlab-ci.yml
playwright:
  image: mcr.microsoft.com/playwright:v1.40.0-focal
  script:
    - npm ci
    - npx playwright test
  artifacts:
    when: always
    paths:
      - playwright-report/
    reports:
      junit: test-results/junit.xml
```

## Common Mistakes

### Mistake 1: Not Waiting for Elements

```typescript
// ❌ Bad: Clicking before element is ready
await page.click('button');

// ✅ Good: Playwright auto-waits
await page.click('button'); // Actually waits automatically

// ✅ Better: Explicit wait if needed
await page.waitForSelector('button', { state: 'visible' });
await page.click('button');
```

### Mistake 2: Using Brittle Selectors

```typescript
// ❌ Bad: Implementation details
await page.click('.MuiButton-root.MuiButton-containedPrimary');

// ✅ Good: Semantic selectors
await page.click('role=button[name="Submit"]');
await page.click('[data-testid="submit-btn"]');
```

### Mistake 3: No Test Isolation

```typescript
// ❌ Bad: Tests depend on each other
test('create user', async ({ page }) => {
  // Creates user...
});

test('login user', async ({ page }) => {
  // Assumes user from previous test exists
});

// ✅ Good: Each test is independent
test('login user', async ({ page }) => {
  // Create user in this test or use fixtures
  await createTestUser();
  // Login...
});
```

### Mistake 4: Ignoring Network State

```typescript
// ❌ Bad: Not waiting for API
await page.click('button');
// Immediately check result (API might not have returned)

// ✅ Good: Wait for network
await Promise.all([
  page.waitForResponse('**/api/submit'),
  page.click('button')
]);
```

## Integration with Other Skills

**Use with:**
- `test-driven-development` - Write Playwright tests first (RED-GREEN-REFACTOR)
- `condition-based-waiting` - Wait for conditions, not arbitrary timeouts
- `database-backup` - ALWAYS backup before tests that modify database
- `systematic-debugging` - Debug failing Playwright tests methodically
- `code-review` - Review test code for quality and coverage

**Complements:**
- `testing-anti-patterns` - Avoid common testing mistakes
- `verification-before-completion` - Verify all tests pass before declaring done

## Checklist

Before running Playwright tests:
- [ ] Playwright MCP configured (if using AI assistance)
- [ ] Playwright installed in project
- [ ] Tests use semantic selectors
- [ ] Tests are isolated (no dependencies)
- [ ] Database backup before tests (if DB involved)
- [ ] Tests wait for conditions (not timeouts)
- [ ] Tests handle network/async properly

## Authority

**This skill is based on:**
- Playwright official documentation
- Microsoft's Playwright MCP implementation
- Frontend testing best practices
- Accessibility-first testing approach
- Model Context Protocol standard

**Social Proof**: Playwright is used by Microsoft, Google, and thousands of companies for reliable frontend testing.

## Your Commitment

When writing Playwright tests:
- [ ] I will use semantic, accessible selectors
- [ ] I will wait for conditions, not timeouts
- [ ] I will keep tests isolated and independent
- [ ] I will backup database before tests (if applicable)
- [ ] I will follow TDD: test first, then implement
- [ ] I will use Playwright MCP for AI-assisted testing

---

**Bottom Line**: Playwright with MCP enables fast, deterministic, AI-assisted frontend testing through accessibility trees. Use semantic selectors, wait for conditions, keep tests isolated, and always backup database before tests that modify data.
