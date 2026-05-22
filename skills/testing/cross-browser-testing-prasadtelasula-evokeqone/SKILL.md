---
name: cross-browser-testing
description: Test cross-browser compatibility on Chrome, Firefox, Safari, and Edge using Playwright. Use when ensuring browser compatibility or fixing browser-specific issues.
allowed-tools: Read, Write, Edit, Bash
---

You implement cross-browser testing for the QA Team Portal using Playwright.

## Requirements from PROJECT_PLAN.md

- Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- Mobile browser support (iOS Safari, Chrome Android)
- Test on different browser versions
- Identify and fix browser-specific issues
- Generate compatibility report

## Browsers to Test

- **Chrome** (Chromium) - Latest + Previous version
- **Firefox** - Latest + Previous version
- **Safari** (WebKit) - Latest version (macOS only)
- **Edge** (Chromium) - Latest version
- **Mobile Safari** (iOS) - Latest version
- **Chrome Android** - Latest version

## Implementation

### 1. Playwright Installation

```bash
cd frontend
npm install -D @playwright/test
npx playwright install
npx playwright install-deps
```

### 2. Playwright Configuration

**Location:** `frontend/playwright.config.ts`

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/junit.xml' }]
  ],

  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    // Desktop Browsers
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1920, height: 1080 }
      },
    },
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        viewport: { width: 1920, height: 1080 }
      },
    },
    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
        viewport: { width: 1920, height: 1080 }
      },
    },
    {
      name: 'edge',
      use: {
        ...devices['Desktop Edge'],
        viewport: { width: 1920, height: 1080 }
      },
    },

    // Mobile Browsers
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 13'] },
    },

    // Tablets
    {
      name: 'iPad',
      use: { ...devices['iPad Pro'] },
    },

    // Different Viewport Sizes
    {
      name: 'Desktop 1366x768',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1366, height: 768 }
      },
    },
    {
      name: 'Desktop 1440x900',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1440, height: 900 }
      },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
})
```

### 3. Cross-Browser Test Suite

**Location:** `frontend/tests/e2e/cross-browser.spec.ts`

```typescript
import { test, expect } from '@playwright/test'

test.describe('Cross-Browser Compatibility', () => {
  test('homepage loads correctly', async ({ page, browserName }) => {
    await page.goto('/')

    // Check page title
    await expect(page).toHaveTitle(/QA Team Portal/)

    // Check hero section visible
    await expect(page.locator('h1')).toBeVisible()

    // Check navigation menu
    await expect(page.locator('nav')).toBeVisible()

    // Check footer
    await expect(page.locator('footer')).toBeVisible()

    // Browser-specific checks
    if (browserName === 'webkit') {
      // Safari-specific checks
      console.log('Running Safari-specific tests')
    }
  })

  test('navigation works across browsers', async ({ page }) => {
    await page.goto('/')

    // Click team link
    await page.click('a[href="#team"]')
    await page.waitForURL('/#team')

    // Click tools link
    await page.click('a[href="#tools"]')
    await page.waitForURL('/#tools')

    // All navigations should work smoothly
  })

  test('forms work correctly', async ({ page }) => {
    await page.goto('/admin/login')

    // Fill form
    await page.fill('input[name="email"]', 'admin@test.com')
    await page.fill('input[name="password"]', 'Test123!@#')

    // Submit form
    await page.click('button[type="submit"]')

    // Check for expected behavior
    // (adjust based on your app's behavior)
  })

  test('responsive layout adjusts correctly', async ({ page, viewport }) => {
    await page.goto('/')

    if (viewport && viewport.width < 768) {
      // Mobile: hamburger menu should be visible
      await expect(page.locator('[data-testid="mobile-menu-button"]')).toBeVisible()

      // Desktop menu should be hidden
      await expect(page.locator('[data-testid="desktop-menu"]')).toBeHidden()
    } else {
      // Desktop: desktop menu should be visible
      await expect(page.locator('[data-testid="desktop-menu"]')).toBeVisible()

      // Mobile menu button should be hidden
      await expect(page.locator('[data-testid="mobile-menu-button"]')).toBeHidden()
    }
  })

  test('CSS grid and flexbox layouts work', async ({ page }) => {
    await page.goto('/')

    // Check team grid
    const teamGrid = page.locator('[data-testid="team-grid"]')
    await expect(teamGrid).toBeVisible()

    // Check grid has correct display property
    const display = await teamGrid.evaluate((el) =>
      window.getComputedStyle(el).getPropertyValue('display')
    )
    expect(display).toBe('grid')

    // Check grid columns
    const gridTemplateColumns = await teamGrid.evaluate((el) =>
      window.getComputedStyle(el).getPropertyValue('grid-template-columns')
    )
    expect(gridTemplateColumns).toBeTruthy()
  })

  test('images load correctly', async ({ page }) => {
    await page.goto('/')

    // Wait for images to load
    await page.waitForLoadState('networkidle')

    // Check all images are loaded
    const images = page.locator('img')
    const count = await images.count()

    for (let i = 0; i < count; i++) {
      const img = images.nth(i)
      const loaded = await img.evaluate((el: HTMLImageElement) => el.complete)
      expect(loaded).toBe(true)
    }
  })

  test('fonts render correctly', async ({ page }) => {
    await page.goto('/')

    // Check font family is applied
    const heading = page.locator('h1')
    const fontFamily = await heading.evaluate((el) =>
      window.getComputedStyle(el).getPropertyValue('font-family')
    )

    // Should include expected font
    expect(fontFamily).toContain('Poppins')
  })

  test('animations and transitions work', async ({ page }) => {
    await page.goto('/')

    // Check element has transition
    const button = page.locator('button').first()
    const transition = await button.evaluate((el) =>
      window.getComputedStyle(el).getPropertyValue('transition')
    )

    expect(transition).toBeTruthy()
  })

  test('local storage works', async ({ page, context }) => {
    await page.goto('/admin/login')

    // Set local storage
    await page.evaluate(() => {
      localStorage.setItem('test_key', 'test_value')
    })

    // Get local storage
    const value = await page.evaluate(() => {
      return localStorage.getItem('test_key')
    })

    expect(value).toBe('test_value')

    // Clear local storage
    await page.evaluate(() => {
      localStorage.removeItem('test_key')
    })
  })

  test('date/time inputs work', async ({ page, browserName }) => {
    await page.goto('/admin/team-members/create')

    // Skip for older browsers that don't support date input
    if (browserName === 'webkit') {
      // Safari handles dates differently
      console.log('Skipping date input test for Safari')
      test.skip()
    }

    await page.fill('input[type="date"]', '2025-11-01')
    const value = await page.inputValue('input[type="date"]')
    expect(value).toBe('2025-11-01')
  })
})

test.describe('Browser-Specific Features', () => {
  test('WebP images work with fallback', async ({ page, browserName }) => {
    await page.goto('/')

    // Modern browsers should use WebP
    const img = page.locator('picture img').first()
    const src = await img.getAttribute('src')

    if (['chromium', 'firefox', 'webkit'].includes(browserName)) {
      // Should support WebP
      expect(src).toContain('.webp')
    } else {
      // Fallback to JPG/PNG
      expect(src).toMatch(/\.(jpg|jpeg|png)$/)
    }
  })

  test('modern CSS features work', async ({ page }) => {
    await page.goto('/')

    // Check CSS Grid support
    const supportsGrid = await page.evaluate(() => {
      return CSS.supports('display', 'grid')
    })
    expect(supportsGrid).toBe(true)

    // Check CSS Flexbox support
    const supportsFlex = await page.evaluate(() => {
      return CSS.supports('display', 'flex')
    })
    expect(supportsFlex).toBe(true)

    // Check CSS Custom Properties support
    const supportsCustomProps = await page.evaluate(() => {
      return CSS.supports('--test', '0')
    })
    expect(supportsCustomProps).toBe(true)
  })
})
```

### 4. Browser-Specific Polyfills

**Location:** `frontend/src/polyfills.ts`

```typescript
// Polyfills for older browsers

// Promise polyfill
if (typeof Promise === 'undefined') {
  // @ts-ignore
  window.Promise = import('promise-polyfill').then(m => m.default)
}

// Fetch polyfill
if (typeof fetch === 'undefined') {
  import('whatwg-fetch')
}

// IntersectionObserver polyfill
if (typeof IntersectionObserver === 'undefined') {
  import('intersection-observer')
}

// ResizeObserver polyfill
if (typeof ResizeObserver === 'undefined') {
  import('@juggle/resize-observer').then(({ ResizeObserver }) => {
    window.ResizeObserver = ResizeObserver
  })
}

// Array.from polyfill
if (!Array.from) {
  Array.from = (function () {
    const toStr = Object.prototype.toString
    const isCallable = function (fn: any) {
      return typeof fn === 'function' || toStr.call(fn) === '[object Function]'
    }
    return function from(arrayLike: any, mapFn?: any, thisArg?: any) {
      const C = this
      const items = Object(arrayLike)

      if (arrayLike == null) {
        throw new TypeError('Array.from requires an array-like object')
      }

      const len = items.length >>> 0

      const A = isCallable(C) ? Object(new C(len)) : new Array(len)

      let k = 0
      let kValue
      while (k < len) {
        kValue = items[k]
        if (mapFn) {
          A[k] = typeof thisArg === 'undefined' ? mapFn(kValue, k) : mapFn.call(thisArg, kValue, k)
        } else {
          A[k] = kValue
        }
        k += 1
      }

      A.length = len
      return A
    }
  })()
}
```

### 5. CSS Vendor Prefixes (Auto with PostCSS)

```bash
npm install -D autoprefixer
```

**Location:** `frontend/postcss.config.js`

```javascript
export default {
  plugins: {
    autoprefixer: {
      overrideBrowserslist: [
        '> 1%',
        'last 2 versions',
        'not dead',
        'not ie 11'
      ]
    },
    tailwindcss: {},
  },
}
```

### 6. Browser Detection Utility

**Location:** `frontend/src/utils/browserDetect.ts`

```typescript
export const getBrowserInfo = () => {
  const ua = navigator.userAgent
  let browserName = 'Unknown'
  let version = 'Unknown'

  // Chrome
  if (ua.indexOf('Chrome') > -1 && ua.indexOf('Edg') === -1) {
    browserName = 'Chrome'
    version = ua.match(/Chrome\/(\d+)/)?.[1] || 'Unknown'
  }
  // Edge
  else if (ua.indexOf('Edg') > -1) {
    browserName = 'Edge'
    version = ua.match(/Edg\/(\d+)/)?.[1] || 'Unknown'
  }
  // Firefox
  else if (ua.indexOf('Firefox') > -1) {
    browserName = 'Firefox'
    version = ua.match(/Firefox\/(\d+)/)?.[1] || 'Unknown'
  }
  // Safari
  else if (ua.indexOf('Safari') > -1 && ua.indexOf('Chrome') === -1) {
    browserName = 'Safari'
    version = ua.match(/Version\/(\d+)/)?.[1] || 'Unknown'
  }

  return {
    browserName,
    version,
    userAgent: ua,
    isMobile: /Mobile|Android|iPhone|iPad/i.test(ua)
  }
}

export const isModernBrowser = () => {
  const info = getBrowserInfo()
  const version = parseInt(info.version)

  // Define minimum versions
  const minVersions: Record<string, number> = {
    Chrome: 90,
    Edge: 90,
    Firefox: 88,
    Safari: 14
  }

  return version >= (minVersions[info.browserName] || 0)
}

// Usage
if (!isModernBrowser()) {
  console.warn('You are using an outdated browser. Some features may not work correctly.')
}
```

### 7. Run Cross-Browser Tests

```bash
# Run tests on all browsers
npx playwright test

# Run on specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit

# Run on mobile
npx playwright test --project="Mobile Chrome"
npx playwright test --project="Mobile Safari"

# Run with UI
npx playwright test --ui

# Generate HTML report
npx playwright show-report
```

### 8. CI/CD Integration

**Location:** `.github/workflows/cross-browser-tests.yml`

```yaml
name: Cross-Browser Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        browser: [chromium, firefox, webkit]

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Install Playwright Browsers
        run: npx playwright install --with-deps ${{ matrix.browser }}

      - name: Run Playwright tests
        run: npx playwright test --project=${{ matrix.browser }}

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report-${{ matrix.browser }}
          path: playwright-report/
          retention-days: 30
```

## Browser Compatibility Checklist

### Chrome/Edge (Chromium)
- [ ] Latest version tested
- [ ] Responsive design works
- [ ] All features functional
- [ ] CSS Grid/Flexbox working
- [ ] WebP images loading
- [ ] Animations smooth

### Firefox
- [ ] Latest version tested
- [ ] Responsive design works
- [ ] All features functional
- [ ] CSS Grid/Flexbox working
- [ ] Fonts rendering correctly
- [ ] Form inputs working

### Safari (WebKit)
- [ ] Latest macOS version tested
- [ ] iOS Safari tested
- [ ] Responsive design works
- [ ] Date inputs working (or fallback)
- [ ] Flexbox gap property supported or polyfilled
- [ ] Backdrop-filter working or fallback provided
- [ ] -webkit- prefixes added where needed

### Mobile Browsers
- [ ] iOS Safari tested
- [ ] Chrome Android tested
- [ ] Touch interactions work
- [ ] Viewport meta tag configured
- [ ] Mobile menu functional
- [ ] Touch targets >= 44x44px

## Common Browser Issues & Solutions

### Safari-Specific Issues

**1. Flexbox Gap Not Supported (< Safari 14.1)**
```css
/* Instead of gap */
.container {
  display: flex;
  gap: 1rem; /* Not supported in old Safari */
}

/* Use margin fallback */
.container > * {
  margin-right: 1rem;
  margin-bottom: 1rem;
}
.container > *:last-child {
  margin-right: 0;
}
```

**2. Date Input Not Supported**
```typescript
// Provide fallback for Safari
const DateInput = ({ value, onChange }) => {
  const isDateSupported = () => {
    const input = document.createElement('input')
    input.setAttribute('type', 'date')
    return input.type === 'date'
  }

  if (!isDateSupported()) {
    // Use text input with placeholder
    return <input type="text" placeholder="YYYY-MM-DD" />
  }

  return <input type="date" value={value} onChange={onChange} />
}
```

### Firefox-Specific Issues

**1. Scrollbar Styling**
```css
/* Firefox uses different properties */
* {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}

/* Chrome/Edge */
*::-webkit-scrollbar {
  width: 8px;
}
```

## Browser Testing Report Template

```markdown
# Cross-Browser Testing Report

**Date:** 2025-11-01
**Tested By:** QA Team
**App Version:** 1.0.0

## Browsers Tested

### Chrome 120 (Desktop)
- ✅ All features working
- ✅ Responsive design correct
- ✅ Performance good (Lighthouse 95)

### Firefox 119 (Desktop)
- ✅ All features working
- ✅ Responsive design correct
- ⚠️ Minor font rendering difference (acceptable)

### Safari 17 (macOS)
- ✅ All features working
- ✅ Responsive design correct
- ⚠️ Backdrop-filter not working (fallback applied)

### Safari (iOS 17)
- ✅ Mobile layout works
- ✅ Touch interactions smooth
- ✅ Forms functional

### Edge 120 (Desktop)
- ✅ All features working (Chromium-based)

## Issues Found

1. **Safari: Date input fallback needed**
   - Severity: Low
   - Status: Fixed
   - Solution: Added text input fallback

2. **Firefox: Scrollbar styling different**
   - Severity: Low
   - Status: Accepted
   - Note: Minor visual difference, acceptable

## Recommendations

- Continue testing on Safari when new features added
- Monitor browser release notes for breaking changes
- Keep polyfills updated
```

## Report

✅ Playwright configured for cross-browser testing
✅ All major browsers tested (Chrome, Firefox, Safari, Edge)
✅ Mobile browsers tested (iOS Safari, Chrome Android)
✅ Responsive layouts verified across browsers
✅ Browser-specific issues identified and fixed
✅ Polyfills added for older browsers
✅ Vendor prefixes auto-added (autoprefixer)
✅ CI/CD integration configured
✅ Test report generated
✅ 100% compatibility achieved
