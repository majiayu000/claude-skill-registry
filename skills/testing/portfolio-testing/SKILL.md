---
name: portfolio-testing
description: E2E testing skill for Pawel Lipowczan portfolio project (Playwright + React/Vite). Use when user wants to create new E2E tests, debug flaky tests, extend test coverage, verify test completeness for features, or run/interpret test results. Covers navigation, forms, blog, SEO, accessibility (WCAG 2.1 AA), responsiveness. References docs/portfolio/testing/{README.md,TESTING_QUICKSTART.md}. Complements portfolio-code-review skill.
license: Apache-2.0
---

# Portfolio E2E Testing

E2E testing skill for Pawel Lipowczan portfolio project using Playwright.

## Project Testing Context

Before writing tests, familiarize yourself with:
- `docs/portfolio/testing/README.md` - Full test documentation
- `docs/portfolio/testing/TESTING_QUICKSTART.md` - Quick start guide
- `tests/utils/test-helpers.js` - Helper functions
- `playwright.config.js` - Test configuration

**Stack:** React 19 + Vite 7 + Tailwind CSS 3 + Framer Motion 12 + React Router 7

**Test Framework:** Playwright 1.56.1 (Chromium, Firefox, WebKit + Mobile viewports)

## Workflow

### Decision Tree

```
User request → What type?
├── "Create tests for [feature]" → New Test Workflow
├── "Test is failing/flaky" → Debug Workflow
├── "Add more test coverage" → Extend Coverage Workflow
├── "Run tests" → Execute & Interpret Workflow
└── "Verify tests for PR" → Verification Workflow
```

### New Test Workflow

1. Identify test category (navigation, form, blog, SEO, accessibility, responsiveness)
2. Select template from Test Writing Templates below
3. Use existing selectors from `references/test-patterns.md`
4. Use helper functions from `tests/utils/test-helpers.js`
5. Run `npm run test:headed` to verify

### Debug Workflow

1. Run `npm run test:debug` to step through
2. Check `references/debugging-guide.md` for common issues
3. Look for timing issues (add explicit waits)
4. Check viewport settings (mobile tests)
5. Verify selectors are correct

### Extend Coverage Workflow

1. Check existing tests (home.spec.js, blog.spec.js, contact-form.spec.js)
2. Review checklists below for gaps
3. Add tests following existing patterns
4. Run full suite: `npm test`

## Test Commands

```bash
npm test                  # Run all tests (3 browsers)
npm run test:headed       # Visible browser for debugging
npm run test:ui           # Interactive Playwright UI
npm run test:debug        # Step-through debugging
npm run test:chrome       # Chromium only (faster)
npm run test:mobile       # Mobile viewports only
npm run test:report       # View HTML report
```

## Test Writing Templates

### Navigation Tests

```javascript
import { test, expect } from "@playwright/test";

test.describe('Navigation - [Feature]', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('desktop menu navigates to [section]', async ({ page }) => {
    await page.click('nav >> text=[Menu Item]');
    await page.waitForSelector('#[section-id]', { state: 'visible' });
    await expect(page.locator('#[section-id]')).toBeInViewport();
  });

  test('mobile menu works', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.reload(); // Viewport must be set before navigation
    await page.click('[aria-label="Toggle menu"]');
    await expect(page.locator('.mobile-menu')).toBeVisible();
    await page.click('nav >> text=[Menu Item]');
    await expect(page.locator('.mobile-menu')).not.toBeVisible();
  });

  test('smooth scroll works', async ({ page }) => {
    await page.click('nav >> text=Kontakt');
    await page.waitForTimeout(500); // Wait for scroll animation
    await expect(page.locator('#contact')).toBeInViewport();
  });

  test('mobile menu closes on Escape', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.reload();
    await page.click('[aria-label="Toggle menu"]');
    await expect(page.locator('.mobile-menu')).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.locator('.mobile-menu')).not.toBeVisible();
  });
});
```

### Form Validation Tests

```javascript
import { test, expect } from "@playwright/test";

test.describe('Contact Form', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/#contact');
    await page.waitForSelector('form#contact-form', { state: 'visible' });
  });

  test('shows error for empty required fields', async ({ page }) => {
    await page.click('button[type="submit"]');
    await expect(page.locator('.error-message')).toBeVisible();
  });

  test('shows error for invalid email', async ({ page }) => {
    await page.fill('input[name="name"]', 'Test User');
    await page.fill('input[name="email"]', 'invalid-email');
    await page.fill('textarea[name="message"]', 'Test message');
    await page.click('button[type="submit"]');
    await expect(page.locator('.error-message')).toContainText('email');
  });

  test('form has accessible labels', async ({ page }) => {
    const nameInput = page.locator('input[name="name"]');
    const label = await nameInput.getAttribute('aria-label') ||
                  await page.locator(`label[for="${await nameInput.getAttribute('id')}"]`).textContent();
    expect(label).toBeTruthy();
  });

  test('tab navigation through fields works', async ({ page }) => {
    await page.click('input[name="name"]');
    await page.keyboard.press('Tab');
    const focusedElement = await page.evaluate(() => document.activeElement?.name);
    expect(focusedElement).toBe('email');
  });
});
```

### Blog Tests

```javascript
import { test, expect } from "@playwright/test";

test.describe('Blog', () => {
  test('blog listing shows posts', async ({ page }) => {
    await page.goto('http://localhost:3000/blog');
    await expect(page.locator('.blog-post-card').first()).toBeVisible();
  });

  test('post card shows required info', async ({ page }) => {
    await page.goto('http://localhost:3000/blog');
    const card = page.locator('.blog-post-card').first();
    await expect(card.locator('img')).toBeVisible(); // Image
    await expect(card.locator('h2, h3')).toBeVisible(); // Title
    await expect(card.locator('.date, time')).toBeVisible(); // Date
  });

  test('post page renders markdown content', async ({ page }) => {
    await page.goto('http://localhost:3000/blog/[slug]');
    await expect(page.locator('article')).toBeVisible();
    await expect(page.locator('article h1')).toBeVisible();
    await expect(page.locator('article .prose, article p')).toBeVisible();
  });

  test('post page shows frontmatter data', async ({ page }) => {
    await page.goto('http://localhost:3000/blog/[slug]');
    await expect(page.locator('.reading-time, [data-reading-time]')).toBeVisible();
    await expect(page.locator('.tags, [data-tags]')).toBeVisible();
  });

  test('back to blog navigation works', async ({ page }) => {
    await page.goto('http://localhost:3000/blog/[slug]');
    await page.click('text=Wróć, text=Blog, a[href="/blog"]');
    await expect(page).toHaveURL(/\/blog\/?$/);
  });
});
```

### SEO Tests

```javascript
import { test, expect } from "@playwright/test";

test.describe('SEO - [Page Name]', () => {
  test('has unique title', async ({ page }) => {
    await page.goto('http://localhost:3000/[path]');
    await page.waitForFunction(() => document.title !== 'Loading...');
    const title = await page.title();
    expect(title).toContain('[Expected keyword]');
    expect(title.length).toBeGreaterThan(10);
    expect(title.length).toBeLessThan(70);
  });

  test('has meta description', async ({ page }) => {
    await page.goto('http://localhost:3000/[path]');
    const description = await page.getAttribute('meta[name="description"]', 'content');
    expect(description).toBeTruthy();
    expect(description.length).toBeGreaterThan(50);
    expect(description.length).toBeLessThan(160);
  });

  test('has OG tags', async ({ page }) => {
    await page.goto('http://localhost:3000/[path]');
    const ogTitle = await page.getAttribute('meta[property="og:title"]', 'content');
    const ogDescription = await page.getAttribute('meta[property="og:description"]', 'content');
    const ogImage = await page.getAttribute('meta[property="og:image"]', 'content');
    const ogUrl = await page.getAttribute('meta[property="og:url"]', 'content');

    expect(ogTitle).toBeTruthy();
    expect(ogDescription).toBeTruthy();
    expect(ogImage).toMatch(/\.(png|jpg|jpeg|webp)$/i);
    expect(ogUrl).toMatch(/^https?:\/\//);
  });

  test('has JSON-LD structured data', async ({ page }) => {
    await page.goto('http://localhost:3000/[path]');
    const jsonLd = await page.$eval(
      'script[type="application/ld+json"]',
      el => JSON.parse(el.textContent)
    );
    expect(jsonLd['@type']).toBeTruthy();
  });

  test('has canonical URL', async ({ page }) => {
    await page.goto('http://localhost:3000/[path]');
    const canonical = await page.getAttribute('link[rel="canonical"]', 'href');
    expect(canonical).toMatch(/^https?:\/\//);
  });
});
```

### Accessibility Tests

```javascript
import { test, expect } from "@playwright/test";

test.describe('Accessibility - [Component]', () => {
  test('keyboard navigation works', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.keyboard.press('Tab');
    const focused = await page.evaluate(() => document.activeElement?.tagName);
    expect(['A', 'BUTTON', 'INPUT']).toContain(focused);
  });

  test('focus indicators are visible', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await page.keyboard.press('Tab');
    const focusedElement = page.locator(':focus');
    const outline = await focusedElement.evaluate(el =>
      getComputedStyle(el).outline || getComputedStyle(el).boxShadow
    );
    expect(outline).not.toBe('none');
  });

  test('images have alt text', async ({ page }) => {
    await page.goto('http://localhost:3000');
    const images = page.locator('img');
    const count = await images.count();
    for (let i = 0; i < count; i++) {
      const alt = await images.nth(i).getAttribute('alt');
      expect(alt).toBeTruthy();
    }
  });

  test('only one H1 per page', async ({ page }) => {
    await page.goto('http://localhost:3000/[path]');
    const h1Count = await page.locator('h1').count();
    expect(h1Count).toBe(1);
  });

  test('heading hierarchy is correct', async ({ page }) => {
    await page.goto('http://localhost:3000');
    const headings = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'))
        .map(h => parseInt(h.tagName[1]));
    });
    // Check no level is skipped (e.g., h1 -> h3 without h2)
    for (let i = 1; i < headings.length; i++) {
      expect(headings[i] - headings[i-1]).toBeLessThanOrEqual(1);
    }
  });

  test('form labels are properly linked', async ({ page }) => {
    await page.goto('http://localhost:3000/#contact');
    const inputs = page.locator('input:not([type="hidden"]), textarea, select');
    const count = await inputs.count();
    for (let i = 0; i < count; i++) {
      const input = inputs.nth(i);
      const id = await input.getAttribute('id');
      const ariaLabel = await input.getAttribute('aria-label');
      const ariaLabelledby = await input.getAttribute('aria-labelledby');
      const hasLabel = id ? await page.locator(`label[for="${id}"]`).count() > 0 : false;
      expect(hasLabel || ariaLabel || ariaLabelledby).toBeTruthy();
    }
  });
});
```

### Responsiveness Tests

```javascript
import { test, expect } from "@playwright/test";

const viewports = {
  mobile: { width: 375, height: 667 },
  tablet: { width: 768, height: 1024 },
  desktop: { width: 1920, height: 1080 }
};

test.describe('Responsiveness', () => {
  for (const [name, size] of Object.entries(viewports)) {
    test(`content is readable on ${name}`, async ({ page }) => {
      await page.setViewportSize(size);
      await page.goto('http://localhost:3000');

      // Check no horizontal overflow
      const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
      expect(bodyWidth).toBeLessThanOrEqual(size.width);

      // Check main content is visible
      await expect(page.locator('main, #hero, .hero')).toBeVisible();
    });

    test(`images scale correctly on ${name}`, async ({ page }) => {
      await page.setViewportSize(size);
      await page.goto('http://localhost:3000');

      const images = page.locator('img');
      const count = await images.count();
      for (let i = 0; i < Math.min(count, 5); i++) {
        const box = await images.nth(i).boundingBox();
        if (box) {
          expect(box.width).toBeLessThanOrEqual(size.width);
        }
      }
    });
  }
});
```

## Verification Checklists

### Navigation Tests Checklist

- [ ] Desktop menu - all links work
- [ ] Smooth scroll to sections
- [ ] Mobile hamburger menu opens/closes
- [ ] Mobile menu closes after navigation
- [ ] Mobile menu closes on Escape key
- [ ] Mobile menu closes on click outside
- [ ] Logo links to home
- [ ] Active section highlighting (if implemented)

### Form Tests Checklist

- [ ] Required field validation (name, email, message)
- [ ] Email format validation
- [ ] Error message display
- [ ] Form labels present (accessibility)
- [ ] Tab navigation through fields
- [ ] Submit button state (disabled when invalid)
- [ ] Success message after submission (if backend connected)

### Blog Tests Checklist

- [ ] Blog listing loads posts
- [ ] Post cards show: image, title, excerpt, date
- [ ] Individual post page renders
- [ ] Markdown content renders correctly
- [ ] Frontmatter displays: date, reading time, tags
- [ ] Back to blog navigation works
- [ ] 404 for non-existent slugs

### SEO Tests Checklist

- [ ] Title tag unique per page
- [ ] Meta description present (50-160 chars)
- [ ] OG tags: og:title, og:description, og:image, og:url
- [ ] Twitter card tags
- [ ] Canonical URL
- [ ] JSON-LD structured data (Person on home, BlogPosting on posts)
- [ ] Sitemap accessible at /sitemap.xml

### Accessibility Tests Checklist (WCAG 2.1 AA)

- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] Focus indicators visible
- [ ] ARIA labels on icon-only buttons
- [ ] Alt text on all images
- [ ] One H1 per page
- [ ] Heading hierarchy (H1 -> H2 -> H3, no skips)
- [ ] Form labels linked to inputs
- [ ] Color contrast >= 4.5:1 for text

### Responsiveness Tests Checklist

- [ ] Mobile (375px) - content readable, no overflow
- [ ] Tablet (768px) - grid layouts adjust
- [ ] Desktop (1920px) - full layout
- [ ] Images scale correctly
- [ ] Text doesn't overflow containers
- [ ] Touch targets >= 44x44px on mobile

## Helper Functions Reference

Available in `tests/utils/test-helpers.js`:

- `waitForSection(page, sectionId)` - Wait for section visibility
- `checkFormAccessibility(page)` - Verify form accessibility
- `testResponsiveLayout(page, viewports)` - Test across viewports
- `verifyMetaTags(page, expected)` - Check SEO meta tags
- `navigateToSection(page, sectionName)` - Navigate via menu
- `checkMobileMenu(page)` - Test mobile menu behavior
- `scrollToElement(page, selector)` - Smooth scroll helper

## Examples

### Example 1: Create tests for new Projects filtering

User: "Dodaj testy dla nowego filtrowania projektów"

Steps:
1. Read existing tests structure in `tests/home.spec.js`
2. Create new describe block for Projects filtering
3. Write tests:
   - Filter buttons are visible
   - Clicking filter shows only matching projects
   - "All" filter shows all projects
   - Filter state persists (if URL-based)
4. Run: `npm run test:headed`

```javascript
test.describe('Projects Filtering', () => {
  test('filter buttons are visible', async ({ page }) => {
    await page.goto('http://localhost:3000/#projects');
    await expect(page.locator('.filter-buttons')).toBeVisible();
  });

  test('clicking filter shows matching projects', async ({ page }) => {
    await page.goto('http://localhost:3000/#projects');
    await page.click('button:has-text("React")');
    const projects = page.locator('.project-card');
    const count = await projects.count();
    for (let i = 0; i < count; i++) {
      await expect(projects.nth(i)).toContainText('React');
    }
  });
});
```

### Example 2: Debug flaky mobile menu test

User: "Test mobile menu failuje losowo"

Steps:
1. Run `npm run test:debug` to step through
2. Check common issues in `references/debugging-guide.md`:
   - Viewport must be set BEFORE page.goto()
   - Animation timing - add waitForTimeout after clicks
   - Selector specificity - use more specific selectors
3. Fix the test:

```javascript
// Before (flaky)
test('mobile menu', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.setViewportSize({ width: 375, height: 667 });
  await page.click('[aria-label="Toggle menu"]');
});

// After (stable)
test('mobile menu', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('http://localhost:3000');
  await page.waitForSelector('[aria-label="Toggle menu"]', { state: 'visible' });
  await page.click('[aria-label="Toggle menu"]');
  await page.waitForSelector('.mobile-menu', { state: 'visible' });
});
```

### Example 3: SEO tests for new blog post

User: "Zweryfikuj SEO dla nowego posta o automatyzacji"

Steps:
1. Get the post slug (e.g., `automatyzacja-email`)
2. Add test in `tests/blog.spec.js`:

```javascript
test.describe('SEO - Blog Post: Automatyzacja Email', () => {
  const postUrl = 'http://localhost:3000/blog/automatyzacja-email';

  test('has correct title', async ({ page }) => {
    await page.goto(postUrl);
    const title = await page.title();
    expect(title).toContain('Automatyzacja');
  });

  test('has OG image', async ({ page }) => {
    await page.goto(postUrl);
    const ogImage = await page.getAttribute('meta[property="og:image"]', 'content');
    expect(ogImage).toMatch(/og-automatyzacja-email\.webp/);
  });

  test('has BlogPosting schema', async ({ page }) => {
    await page.goto(postUrl);
    const jsonLd = await page.$eval(
      'script[type="application/ld+json"]',
      el => JSON.parse(el.textContent)
    );
    expect(jsonLd['@type']).toBe('BlogPosting');
  });
});
```

3. Verify sitemap includes post:
```javascript
test('sitemap includes new post', async ({ page }) => {
  const response = await page.goto('http://localhost:3000/sitemap.xml');
  const content = await response.text();
  expect(content).toContain('/blog/automatyzacja-email');
});
```

## Integration with portfolio-code-review

| portfolio-code-review | portfolio-testing |
|----------------------|-------------------|
| Reviews code changes | Verifies runtime behavior |
| Static analysis | E2E tests |
| Checks conventions | Checks functionality |
| Pre-merge review | Post-implementation verification |

**Workflow:**
1. Developer makes changes
2. `portfolio-code-review` reviews code quality, edge cases, conventions
3. `portfolio-testing` creates/runs tests to verify behavior
4. Both pass → Ready to merge

**When to use which:**
- Code review finds: "Missing rel='noopener' on external link"
- Testing verifies: "External links open in new tab"

## Test Report Template

After running tests, generate report:

```markdown
# E2E Test Report - [Feature/Date]

## Summary
- **Tests run:** [number]
- **Passed:** [number]
- **Failed:** [number]
- **Skipped:** [number]

## Test Coverage

### Navigation
- [x] Desktop menu: PASS
- [x] Mobile menu: PASS
- [ ] Smooth scroll: FAIL - timeout on #contact

### Forms
- [x] Validation: PASS
- [x] Accessibility: PASS

### Blog
- [x] Listing: PASS
- [x] Single post: PASS

### SEO
- [x] Meta tags: PASS
- [ ] OG image: FAIL - 404 for og-[slug].webp

## Failed Tests

### smooth scroll to contact section
**Error:** Timeout 30000ms exceeded
**Screenshot:** [link to report]
**Likely cause:** Animation timing or element not found
**Suggested fix:** Add explicit wait or check selector

### OG image for new post
**Error:** 404 for /images/og-new-post.webp
**Likely cause:** OG image not created
**Suggested fix:** Run `npm run img:convert` or create WebP image

## Next Steps
1. Fix smooth scroll timing
2. Create missing OG image
3. Re-run tests: `npm test`
```

## Guidelines

### Philosophy

- **Test user flows** - Focus on real user scenarios, not implementation details
- **Mobile first** - Always test mobile viewports (majority of users)
- **Edge cases** - Test what can go wrong (empty states, errors, timeouts)
- **Accessibility** - Every test should consider keyboard/screen reader users

### Process

1. Read existing tests first (understand patterns)
2. Use helper functions (avoid duplication)
3. Run `test:headed` during development (see what's happening)
4. Run full suite before PR (catch cross-browser issues)

### Common pitfalls

- Viewport not set before goto (causes flaky mobile tests)
- Missing waits for animations (Framer Motion needs ~300ms)
- Hardcoded timeouts (prefer waitForSelector)
- Testing implementation, not behavior (brittle tests)
- Forgetting mobile menu close behavior (nav, Escape, outside click)
