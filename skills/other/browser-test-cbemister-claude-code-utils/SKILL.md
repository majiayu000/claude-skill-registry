---
name: browser-test
description: Run comprehensive Playwright browser tests across desktop, tablet, and mobile viewports. Auto-discovers pages and tests navigation, forms, auth, CRUD, responsive behavior, interactive elements, error states, user flows, and performance metrics.
hooks:
  SubagentStart:
    - matcher: ".*"
      hooks:
        - type: command
          command: |
            echo ""
            case "$AGENT_TYPE" in
              "codebase-explorer") echo "   🔍 Discovering application routes and pages..." ;;
              "test-writer") echo "   🧪 Generating Playwright test scripts..." ;;
              "debugger") echo "   🐛 Debugging test failures..." ;;
              *) echo "   🤖 Running: $AGENT_TYPE" ;;
            esac
  SubagentStop:
    - hooks:
        - type: command
          command: "echo '   ✓ Complete'"
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            Verify that /browser-test completed all required phases:

            1. Phase 1 (Setup):
               - Was Playwright installed or verified?
               - Was the playwright.config.ts generated?

            2. Phase 2 (Discovery):
               - Were application routes/pages discovered?
               - Were testable features identified?

            3. Phase 3 (Test Generation):
               - Were test spec files generated?

            4. Phase 4 (Execution):
               - Were tests run across all 3 viewports?
               - Were screenshots captured?

            5. Phase 5 (Report):
               - Was the test report generated?

            Context: $ARGUMENTS

            Return {"ok": true} if all phases completed.
            Return {"ok": false, "reason": "specific issue"} if incomplete.
          timeout: 30
---

# Browser Test Skill

Run comprehensive Playwright browser tests across desktop, tablet, and mobile viewports.

## When to Use

Invoke with `/browser-test` when you need to:
- Test your web application across multiple screen sizes
- Verify responsive behavior and mobile compatibility
- Test user flows and common interactions
- Capture screenshots at different viewports
- Check performance metrics (LCP, CLS, INP)

## Usage

```bash
/browser-test <port> [target]
```

**Arguments:**
- `port` (required) - Port the app is running on (e.g., 3000, 8080)
- `target` (optional) - Specific page (`/dashboard`), flow type (`auth`, `forms`, `crud`), or `all` (default)

**Examples:**
```bash
# Test entire app on port 3000
/browser-test 3000

# Test only the dashboard page
/browser-test 3000 /dashboard

# Test only authentication flows
/browser-test 3000 auth

# Test on different port
/browser-test 8080 all
```

## Instructions

### Phase 1: Setup and Validation

```bash
PORT="$1"
TARGET="${2:-all}"

# Validate port is provided
if [ -z "$PORT" ]; then
  echo "❌ Error: Port number is required"
  echo ""
  echo "Usage: /browser-test <port> [page-or-feature|all]"
  echo ""
  echo "Examples:"
  echo "  /browser-test 3000"
  echo "  /browser-test 3000 all"
  echo "  /browser-test 3000 /dashboard"
  echo "  /browser-test 3000 auth"
  exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎭 Browser Testing with Playwright"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Target: http://localhost:$PORT"
echo "Scope: $TARGET"
echo "Viewports: Desktop (1920x1080), Tablet (768x1024), Mobile (375x812)"
echo ""

# Verify the app is running on the specified port
echo "📡 Checking if app is running on port $PORT..."

# Use curl to check if the port responds (works on Windows/Linux/Mac)
if command -v curl > /dev/null 2>&1; then
  if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT" | grep -q "^[23]"; then
    echo "✓ App is reachable at http://localhost:$PORT"
  else
    echo "⚠️  Warning: Could not reach http://localhost:$PORT"
    echo "   Make sure your app is running before continuing"
    echo ""
  fi
else
  echo "⚠️  curl not found, skipping reachability check"
  echo "   Make sure your app is running at http://localhost:$PORT"
  echo ""
fi

# Check if Playwright is installed
echo ""
echo "🔍 Checking Playwright installation..."

if npx playwright --version > /dev/null 2>&1; then
  PLAYWRIGHT_VERSION=$(npx playwright --version)
  echo "✓ Playwright found: $PLAYWRIGHT_VERSION"
else
  echo "📦 Playwright not found. Installing..."

  # Create package.json if it doesn't exist
  if [ ! -f "package.json" ]; then
    npm init -y > /dev/null 2>&1
  fi

  # Install Playwright
  npm install --save-dev @playwright/test

  # Install Chromium only (faster than all browsers)
  npx playwright install chromium

  echo "✓ Playwright installed successfully"
fi

# Create browser-tests directory structure
echo ""
echo "📁 Setting up test directory structure..."

mkdir -p browser-tests/tests
mkdir -p browser-tests/screenshots/desktop
mkdir -p browser-tests/screenshots/tablet
mkdir -p browser-tests/screenshots/mobile
mkdir -p browser-tests/reports

echo "✓ Directory structure created"
echo ""
```

### Phase 2: Route and Feature Discovery

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Phase 2: Discovering Routes and Features"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Detect framework
FRAMEWORK="unknown"

echo "🔍 Detecting framework..."

if [ -d "app" ] && ([ -f "next.config.js" ] || [ -f "next.config.ts" ] || [ -f "next.config.mjs" ]); then
  FRAMEWORK="nextjs-app-router"
  echo "✓ Detected: Next.js (App Router)"
elif [ -d "pages" ] && ([ -f "next.config.js" ] || [ -f "next.config.ts" ]); then
  FRAMEWORK="nextjs-pages-router"
  echo "✓ Detected: Next.js (Pages Router)"
elif [ -f "nuxt.config.ts" ] || [ -f "nuxt.config.js" ]; then
  FRAMEWORK="nuxt"
  echo "✓ Detected: Nuxt"
elif [ -f "vite.config.ts" ] || [ -f "vite.config.js" ]; then
  FRAMEWORK="vite-spa"
  echo "✓ Detected: Vite SPA"
elif [ -f "angular.json" ]; then
  FRAMEWORK="angular"
  echo "✓ Detected: Angular"
elif [ -d "src" ] && grep -q "react-router" package.json 2>/dev/null; then
  FRAMEWORK="react-router"
  echo "✓ Detected: React Router"
elif [ -d "src" ] && grep -q "vue-router" package.json 2>/dev/null; then
  FRAMEWORK="vue-router"
  echo "✓ Detected: Vue Router"
else
  echo "⚠️  Framework not auto-detected, will use runtime crawling"
fi

echo ""
echo "🗺️  Discovering routes and features..."
echo ""

# Claude: Based on detected framework, discover routes using static analysis:
#
# Next.js App Router:
# - Scan app/**/page.tsx and app/**/page.jsx
# - Map directory structure to routes
# - Identify route groups (app/(auth)/login -> /login)
# - Identify dynamic routes (app/posts/[id] -> /posts/:id)
#
# Next.js Pages Router:
# - Scan pages/**/*.tsx and pages/**/*.jsx
# - Exclude _app, _document, _error
# - Map file names to routes
#
# Nuxt:
# - Scan pages/**/*.vue
# - Follow Nuxt routing conventions
#
# React Router / Vue Router:
# - Find router configuration files (usually src/router, src/routes)
# - Parse route definitions
#
# Vite SPA / Unknown:
# - Fall back to runtime crawling (Phase 2B below)
#
# For each route, detect features by analyzing source code:
#
# FORMS - Look for:
# - <form>, <input>, <textarea>, <select> elements
# - Form libraries: react-hook-form, Formik, useForm
# - Validation schemas: Zod, Yup
# - API handlers with POST/PUT methods
#
# AUTHENTICATION - Look for:
# - Auth providers: NextAuth, Clerk, Auth0, Supabase
# - /login, /signin, /signup, /register routes
# - useSession, getServerSession, useAuth hooks
# - Middleware with authentication checks
# - Protected route patterns
#
# CRUD OPERATIONS - Look for:
# - Table/list components with edit/delete buttons
# - Routes with /new, /create, /edit, /:id patterns
# - API routes with GET/POST/PUT/DELETE methods
# - Database queries in server components/API routes
#
# INTERACTIVE ELEMENTS - Look for:
# - Dialog/Modal components
# - Dropdown/Select components
# - Accordion/Collapse components
# - Tooltip/Popover components
# - Tab/TabPanel components
#
# ERROR PAGES - Look for:
# - 404.tsx, not-found.tsx, [not-found].tsx
# - 500.tsx, error.tsx
# - ErrorBoundary components
#
# Present discovery results in structured format:
#
# Example output format:
# ┌────────────────────────────────────────┐
# │ Routes Discovered: 12                  │
# ├────────────────────────────────────────┤
# │ / (homepage)                           │
# │ /about                                 │
# │ /dashboard (requires auth)             │
# │ /dashboard/settings                    │
# │ /products (CRUD list)                  │
# │ /products/[id] (CRUD detail)           │
# │ /products/new (CRUD create)            │
# │ /login (auth)                          │
# │ /signup (auth)                         │
# │ /contact (form)                        │
# │ /404 (error page)                      │
# │ /api/health (API - skip browser test) │
# └────────────────────────────────────────┘
#
# ┌────────────────────────────────────────┐
# │ Features Detected                      │
# ├────────────────────────────────────────┤
# │ ✓ Forms: 3 pages                       │
# │   - /contact (contact form)            │
# │   - /login (credentials)               │
# │   - /signup (registration)             │
# │                                        │
# │ ✓ Authentication: NextAuth             │
# │   - /login, /signup pages              │
# │   - Protected: /dashboard/*            │
# │                                        │
# │ ✓ CRUD: Products                       │
# │   - List: /products                    │
# │   - Detail: /products/[id]             │
# │   - Create: /products/new              │
# │                                        │
# │ ✓ Interactive Elements                 │
# │   - Modal: Delete confirmation         │
# │   - Dropdown: Navigation menu          │
# │                                        │
# │ ✓ Error Pages                          │
# │   - Custom 404: /404                   │
# └────────────────────────────────────────┘
#
# If TARGET is not "all", filter to matching scope:
# - If TARGET is a path like "/dashboard", only test that route
# - If TARGET is "auth", only test authentication flows
# - If TARGET is "forms", only test form pages
# - If TARGET is "crud", only test CRUD operations

echo ""
```

### Phase 3: Test Generation

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Phase 3: Generating Test Scripts"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Generate playwright.config.ts with 3 viewport projects
echo "📝 Generating playwright.config.ts..."

cat > browser-tests/playwright.config.ts << 'PLAYWRIGHT_CONFIG_EOF'
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  outputDir: './test-results',
  fullyParallel: false, // Sequential for predictable screenshots
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 1,
  workers: 1, // Run one test at a time
  timeout: 30000,
  use: {
    baseURL: `http://localhost:${PORT}`,
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  projects: [
    {
      name: 'desktop',
      use: {
        viewport: { width: 1920, height: 1080 },
        ...devices['Desktop Chrome'],
      },
    },
    {
      name: 'tablet',
      use: {
        viewport: { width: 768, height: 1024 },
        ...devices['iPad Mini'],
      },
    },
    {
      name: 'mobile',
      use: {
        viewport: { width: 375, height: 812 },
        ...devices['iPhone 13'],
      },
    },
  ],
  reporter: [
    ['json', { outputFile: './reports/test-results.json' }],
    ['html', { outputFolder: './reports/html', open: 'never' }],
    ['list'],
  ],
});
PLAYWRIGHT_CONFIG_EOF

# Replace PORT placeholder
sed -i "s/\${PORT}/$PORT/g" browser-tests/playwright.config.ts

echo "✓ Config generated"
echo ""

# Claude: Generate test spec files based on discovered features
#
# For each test category, generate a spec file:
#
# 1. navigation.spec.ts - For every discovered route:
#    - Test page loads without console errors
#    - Test title/heading is present
#    - Test all internal links are clickable
#    - Test back/forward browser navigation
#    - Capture screenshot after page load
#
# 2. forms.spec.ts - For each detected form:
#    - Test form renders with expected fields
#    - Test empty submit shows validation errors
#    - Test valid submit succeeds (or shows success state)
#    - Test tab order for accessibility
#    - Capture screenshots of: form, validation errors, success
#
# 3. auth.spec.ts - Only if auth detected:
#    - Test login page renders
#    - Test invalid credentials show error
#    - Test valid login redirects (if test credentials available)
#    - Test logout works
#    - Test protected routes redirect to login
#    - Note: Ask user for test credentials or check .env.test
#
# 4. crud.spec.ts - Only if CRUD detected:
#    - Test list view loads and displays items
#    - Test create form submits
#    - Test edit form pre-fills data
#    - Test delete shows confirmation and removes item
#    - Test empty state renders
#
# 5. responsive.spec.ts - Cross-viewport comparison:
#    - Test mobile menu vs desktop nav visibility
#    - Test no horizontal scroll
#    - Test touch targets >= 44x44px on mobile
#    - Test text readability (no overflow)
#
# 6. interactive.spec.ts - For detected interactive elements:
#    - Test modals open/close (click, Escape, overlay)
#    - Test dropdowns expand and allow selection
#    - Test accordions expand/collapse
#    - Test tooltips appear on hover
#
# 7. error-states.spec.ts - Error handling:
#    - Test 404 page for non-existent routes
#    - Test form validation errors display
#    - Test error page has navigation back to home
#
# 8. performance.spec.ts - Web vitals for all pages:
#    - Measure LCP (target: <2.5s)
#    - Measure CLS (target: <0.1)
#    - Measure INP (target: <200ms)
#    - Report per viewport
#
# 9. user-flows.spec.ts - End-to-end journeys:
#    Based on detected features, generate flows like:
#    - Signup-to-first-action: Register → onboard → complete task
#    - Browse-to-purchase: Browse → select → cart → checkout
#    - Search-and-filter: Search → filter → view result
#    - Settings-update: Navigate → change → save → verify
#    - Content-creation: Navigate → create → submit → verify in list
#
# Each test file should:
# - Import from '@playwright/test'
# - Use test.describe() to group related tests
# - Use test() for individual test cases
# - Access viewport via testInfo.project.name
# - Reference actual selectors/routes from Phase 2 discovery
# - Capture screenshots at key steps
# - Use meaningful test names and assertions
#
# Example test structure:
# ```typescript
# import { test, expect } from '@playwright/test';
#
# test.describe('Homepage', () => {
#   test('loads successfully', async ({ page }, testInfo) => {
#     await page.goto('/');
#
#     // Common assertions
#     await expect(page).toHaveTitle(/.+/);
#     await expect(page.locator('body')).toBeVisible();
#
#     // Viewport-specific assertions
#     const viewport = testInfo.project.name;
#     if (viewport === 'mobile') {
#       await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();
#     } else {
#       await expect(page.locator('[data-testid="desktop-nav"]')).toBeVisible();
#     }
#
#     // Screenshot
#     await page.screenshot({
#       path: `screenshots/${viewport}/homepage.png`,
#       fullPage: true
#     });
#   });
# });
# ```
#
# For each spec file generated, output:
echo "✓ Generated: tests/navigation.spec.ts"
echo "✓ Generated: tests/forms.spec.ts"
# ... etc for each test file created
#
# Skip spec files for features not detected

echo ""
```

### Phase 4: Test Execution

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Phase 4: Running Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd browser-tests

echo "🧪 Running Playwright tests across 3 viewports..."
echo "   This may take a few minutes..."
echo ""

# Run tests
npx playwright test

# Capture exit code
TEST_EXIT_CODE=$?

echo ""

if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo "✅ All tests passed!"
else
  echo "⚠️  Some tests failed. See report for details."
  echo ""

  # Claude: Analyze failures
  # - Read test-results.json
  # - For each failure, determine if it's:
  #   1. Test authoring issue (wrong selector, timing) → Fix the test
  #   2. Application bug (wrong behavior) → Report it
  #   3. Untestable scenario (needs real auth) → Add test.fixme() annotation
  #
  # If fixes are made, re-run:
  # npx playwright test --last-failed
fi

cd ..

echo ""
```

### Phase 5: Report Generation

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Phase 5: Generating Report"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📊 Generating test report..."

# Claude: Read browser-tests/reports/test-results.json
# Generate browser-tests/reports/test-report.md with:
#
# Format:
# ```markdown
# # Browser Test Report
#
# **Generated**: 2026-02-05T12:00:00Z
# **Application**: http://localhost:3000
# **Framework**: Next.js (App Router)
#
# ---
#
# ## Summary
#
# | Viewport | Tests | Passed | Failed | Skipped |
# |----------|-------|--------|--------|---------|
# | Desktop (1920x1080) | 42 | 40 | 1 | 1 |
# | Tablet (768x1024) | 42 | 41 | 0 | 1 |
# | Mobile (375x812) | 42 | 39 | 2 | 1 |
# | **Total** | **126** | **120** | **3** | **3** |
#
# **Pass Rate**: 95.2%
#
# ---
#
# ## Routes Tested
#
# | Route | Desktop | Tablet | Mobile | Notes |
# |-------|---------|--------|--------|-------|
# | / | PASS | PASS | PASS | Homepage loads in <1s |
# | /dashboard | PASS | PASS | FAIL | Mobile nav overlaps content |
# | /products | PASS | PASS | PASS | |
# | /login | PASS | PASS | PASS | |
# | /contact | FAIL | PASS | FAIL | Form submit 500 error |
# | /404 | PASS | PASS | PASS | Custom error page works |
#
# ---
#
# ## Test Results by Category
#
# ### Navigation (8 tests per viewport)
# - ✅ All pages load without console errors
# - ✅ Internal links resolve correctly
# - ✅ Back/forward navigation works
# - ❌ Dashboard nav overlaps main content at 375px (mobile)
#
# ### Forms (6 tests per viewport)
# - ✅ Contact form renders all fields
# - ✅ Validation errors appear for empty required fields
# - ❌ Contact form submit returns 500 (server error)
# - ✅ Login form accepts credentials
#
# ### Authentication (4 tests per viewport)
# - ✅ Login page renders
# - ✅ Invalid credentials show error message
# - ⏭️  Valid login (skipped - no test credentials)
# - ✅ Protected routes redirect to /login
#
# ### User Flows (3 flows)
# - ✅ Browse-to-detail: Click product → view detail → back to list
# - ❌ Signup-to-dashboard: Form submit fails at registration step
# - ✅ Settings-update: Change setting → save → persists on reload
#
# ### Responsive Behavior (6 tests per viewport)
# - ✅ Mobile menu visible on mobile/tablet
# - ✅ Desktop nav hidden on mobile
# - ❌ Dashboard sidebar does not collapse on mobile
# - ✅ No horizontal scroll on any viewport
#
# ### Interactive Elements (5 tests per viewport)
# - ✅ Delete confirmation modal opens/closes
# - ✅ Dropdown navigation works
# - ✅ Modal closes on Escape key
#
# ### Error States (4 tests per viewport)
# - ✅ /nonexistent shows 404 page
# - ✅ 404 page has link back to home
# - ✅ Form validation errors are accessible
#
# ### Performance Metrics
#
# | Page | Metric | Desktop | Tablet | Mobile | Target | Status |
# |------|--------|---------|--------|--------|--------|--------|
# | / | LCP | 1.2s | 1.4s | 1.8s | <2.5s | ✅ |
# | / | CLS | 0.02 | 0.03 | 0.05 | <0.1 | ✅ |
# | /dashboard | LCP | 1.8s | 2.1s | 2.8s | <2.5s | ⚠️ |
# | /products | LCP | 0.9s | 1.1s | 1.3s | <2.5s | ✅ |
#
# ---
#
# ## Failures Detail
#
# ### 1. Contact Form Server Error
# **Viewports**: Desktop, Mobile
# **File**: tests/forms.spec.ts:45
# **Description**: Submitting the contact form with valid data returns HTTP 500
# **Expected**: Success message or redirect
# **Actual**: Server error response
# **Screenshot**: screenshots/desktop/contact-form-error.png
# **Recommendation**: Check the /api/contact endpoint server-side handler
#
# ### 2. Dashboard Mobile Layout
# **Viewports**: Mobile
# **File**: tests/responsive.spec.ts:23
# **Description**: Dashboard sidebar does not collapse at mobile width
# **Expected**: Sidebar hidden behind hamburger menu
# **Actual**: Sidebar overlaps main content
# **Screenshot**: screenshots/mobile/dashboard-layout-issue.png
# **Recommendation**: Add responsive breakpoint for sidebar at 768px
#
# ---
#
# ## Screenshots
#
# All screenshots saved to `browser-tests/screenshots/`:
# - `desktop/` - 12 screenshots (1920x1080)
# - `tablet/` - 12 screenshots (768x1024)
# - `mobile/` - 12 screenshots (375x812)
#
# ---
#
# ## Re-running Tests
#
# ```bash
# # Run all tests
# cd browser-tests && npx playwright test
#
# # Run specific test file
# npx playwright test tests/forms.spec.ts
#
# # Run for specific viewport only
# npx playwright test --project=mobile
#
# # Run with UI mode for debugging
# npx playwright test --ui
#
# # View HTML report
# npx playwright show-report reports/html
# ```
#
# ---
#
# ## Files Generated
#
# - `browser-tests/playwright.config.ts` - Playwright configuration
# - `browser-tests/tests/*.spec.ts` - Test spec files
# - `browser-tests/screenshots/` - Screenshots by viewport
# - `browser-tests/reports/test-report.md` - This report
# - `browser-tests/reports/test-results.json` - Machine-readable results
# - `browser-tests/reports/html/` - Interactive HTML report
# ```

echo "✓ Report generated: browser-tests/reports/test-report.md"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Browser Testing Complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📄 View report:"
echo "   browser-tests/reports/test-report.md"
echo ""
echo "🖼️  Screenshots:"
echo "   browser-tests/screenshots/{desktop,tablet,mobile}/"
echo ""
echo "🔄 Re-run tests:"
echo "   cd browser-tests && npx playwright test"
echo ""
echo "🎭 Debug with UI:"
echo "   cd browser-tests && npx playwright test --ui"
echo ""
```

## Quick Reference

| Phase | Action | Key Output |
|-------|--------|------------|
| 1 | Setup | Playwright installed, directories created |
| 2 | Discovery | Routes and features identified |
| 3 | Generation | Test spec files created |
| 4 | Execution | Tests run across 3 viewports |
| 5 | Report | Markdown report with results and recommendations |

## Notes

- Tests run **sequentially** (not parallel) for predictable screenshots
- Only **Chromium** is installed (not Firefox/WebKit) for speed
- Tests are saved to the **project** (not the skill) so users can re-run them
- Screenshots captured at **key steps** in each test flow
- Performance metrics measured using **Web Vitals API**
- **User flows** test end-to-end journeys based on detected features
- Report includes **specific recommendations** for fixing failures
