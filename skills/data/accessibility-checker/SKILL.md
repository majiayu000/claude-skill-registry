---
name: accessibility-checker
description: Validate WCAG 2.1 Level AA compliance and accessibility best practices.
  Use when performing accessibility audits and WCAG certification.
allowed-tools: Read, Grep, Glob, Bash, mcp__playwright-mcp__playwright_navigate, mcp__playwright-mcp__playwright_screenshot,
  mcp__playwright-mcp__playwright_evaluate
---

# Accessibility Checker Skill

## Purpose

This skill provides comprehensive accessibility validation against WCAG 2.1 Level AA standards, combining automated testing with manual verification procedures.

## When to Use

- Accessibility audits for new features
- WCAG 2.1 Level AA compliance checks
- Pre-release accessibility validation
- Accessibility regression testing
- Legal compliance verification (ADA, Section 508)

## WCAG 2.1 Level AA Validation Workflow

### 1. Automated Accessibility Scanning

**Using Axe-core with Playwright:**

```typescript
// Install axe-core
npm install -D @axe-core/playwright

// Accessibility test
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('page should not have accessibility violations', async ({ page }) => {
  await page.goto('/');

  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

**Scan All Pages:**

```bash
# Create script to scan all pages
cat > scripts/accessibility-scan.js << 'EOF'
const { chromium } = require('playwright');
const AxeBuilder = require('@axe-core/playwright').default;

async function scanPage(url) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(url);

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();

  await browser.close();
  return results;
}

// Scan multiple pages
const pages = [
  'http://localhost:3000/',
  'http://localhost:3000/about',
  'http://localhost:3000/products',
];

(async () => {
  for (const url of pages) {
    console.log(`Scanning ${url}`);
    const results = await scanPage(url);
    console.log(`Violations: ${results.violations.length}`);
  }
})();
EOF

node scripts/accessibility-scan.js
```

**Deliverable:** Automated scan results with violation list

---

### 2. WCAG 2.1 Principle: Perceivable

**1.1 Text Alternatives:**

**Check Images:**
```bash
# Find images without alt text
grep -r "<img" src/ | grep -v "alt="

# Using Playwright
await page.locator('img:not([alt])').count(); // Should be 0
```

**Checklist:**
- [ ] All images have alt attributes
- [ ] Decorative images use alt=""
- [ ] Complex images have detailed descriptions
- [ ] Icons have aria-label or title
- [ ] Image buttons have descriptive text

**1.3 Adaptable:**

```typescript
// Test: Content order makes sense
test('content order is logical', async ({ page }) => {
  await page.goto('/');

  // Disable CSS to check content order
  await page.addStyleTag({ content: '* { all: unset !important; }' });

  const textContent = await page.textContent('body');
  // Verify content reads logically
});

// Test: Responsive tables
test('tables are responsive', async ({ page }) => {
  await page.goto('/data');

  const tables = page.locator('table');
  const count = await tables.count();

  for (let i = 0; i < count; i++) {
    const table = tables.nth(i);

    // Check for headers
    await expect(table.locator('th')).toHaveCount(greaterThan(0));

    // Check for scope attributes
    const headers = await table.locator('th').all();
    for (const header of headers) {
      const scope = await header.getAttribute('scope');
      expect(['col', 'row', 'colgroup', 'rowgroup']).toContain(scope);
    }
  }
});
```

**Checklist:**
- [ ] Semantic HTML elements used (header, nav, main, footer)
- [ ] Heading hierarchy logical (h1 > h2 > h3)
- [ ] Lists use ul/ol/dl elements
- [ ] Tables have proper headers and scope
- [ ] Forms have fieldset and legend where appropriate

**1.4 Distinguishable:**

**Color Contrast:**
```bash
# Manual check with browser DevTools or:
# Use axe-core for automated checking

# Check specific contrast ratios
# Text: 4.5:1 minimum
# Large text (18pt+): 3:1 minimum
# UI components: 3:1 minimum
```

```typescript
// Test: Color contrast
test('text has sufficient color contrast', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['color-contrast'])
    .analyze();

  expect(results.violations).toEqual([]);
});

// Test: Focus indicators
test('focus indicators are visible', async ({ page }) => {
  await page.goto('/');

  const links = page.locator('a, button, input');
  const count = await links.count();

  for (let i = 0; i < count; i++) {
    await page.keyboard.press('Tab');

    // Check focus is visible
    const focused = await page.evaluateHandle(() => document.activeElement);
    const outline = await focused.evaluate(el =>
      window.getComputedStyle(el).outline
    );

    expect(outline).not.toBe('none');
  }
});
```

**Checklist:**
- [ ] Text contrast ≥ 4.5:1 (normal text)
- [ ] Large text contrast ≥ 3:1 (18pt+ or 14pt+ bold)
- [ ] UI component contrast ≥ 3:1
- [ ] Focus indicators visible (3:1 contrast with adjacent colors)
- [ ] Color not sole means of conveying information
- [ ] Text resizable to 200% without loss of content
- [ ] No horizontal scrolling at 200% zoom
- [ ] Images of text avoided (use real text)

**Deliverable:** Perceivable compliance report

---

### 3. WCAG 2.1 Principle: Operable

**2.1 Keyboard Accessible:**

```typescript
// Test: Full keyboard navigation
test('all functionality available via keyboard', async ({ page }) => {
  await page.goto('/');

  // Tab through all interactive elements
  const interactiveElements = await page.locator(
    'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
  ).all();

  for (let i = 0; i < interactiveElements.length; i++) {
    await page.keyboard.press('Tab');

    const focused = await page.evaluateHandle(() => document.activeElement);
    const tagName = await focused.evaluate(el => el.tagName);

    // Verify element is focusable
    expect(['A', 'BUTTON', 'INPUT', 'SELECT', 'TEXTAREA']).toContain(tagName);
  }

  // Verify no keyboard trap
  // Tab through all elements without getting stuck
});

// Test: Skip links
test('skip link allows bypassing navigation', async ({ page }) => {
  await page.goto('/');

  // Press Tab to focus skip link
  await page.keyboard.press('Tab');

  const skipLink = page.locator('a[href="#main-content"]');
  await expect(skipLink).toBeFocused();

  // Activate skip link
  await page.keyboard.press('Enter');

  // Verify focus moved to main content
  const mainContent = page.locator('#main-content');
  await expect(mainContent).toBeFocused();
});
```

**Checklist:**
- [ ] All functionality available via keyboard
- [ ] Keyboard shortcuts don't conflict
- [ ] Tab order is logical
- [ ] No keyboard traps
- [ ] Skip links present and functional
- [ ] Custom widgets keyboard accessible

**2.4 Navigable:**

```typescript
// Test: Page title
test('pages have descriptive titles', async ({ page }) => {
  await page.goto('/products');
  const title = await page.title();
  expect(title).toContain('Products');
  expect(title.length).toBeGreaterThan(5);
});

// Test: Heading structure
test('heading hierarchy is logical', async ({ page }) => {
  await page.goto('/');

  const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
  const levels = await Promise.all(
    headings.map(h => h.evaluate(el => parseInt(el.tagName[1])))
  );

  // Check h1 exists and is unique
  const h1Count = levels.filter(l => l === 1).length;
  expect(h1Count).toBe(1);

  // Check no skipped levels
  for (let i = 1; i < levels.length; i++) {
    const diff = levels[i] - levels[i-1];
    expect(diff).toBeLessThanOrEqual(1);
  }
});

// Test: Link purpose
test('links have descriptive text', async ({ page }) => {
  await page.goto('/');

  const links = await page.locator('a').all();

  for (const link of links) {
    const text = await link.textContent();
    const ariaLabel = await link.getAttribute('aria-label');
    const title = await link.getAttribute('title');

    const hasText = text && text.trim().length > 0;
    const hasLabel = ariaLabel && ariaLabel.length > 0;
    const hasTitle = title && title.length > 0;

    expect(hasText || hasLabel || hasTitle).toBe(true);

    // Avoid generic text
    if (text) {
      expect(['click here', 'read more', 'link']).not.toContain(text.toLowerCase().trim());
    }
  }
});
```

**Checklist:**
- [ ] Page titles descriptive and unique
- [ ] Focus order follows visual order
- [ ] Link purpose clear from text or context
- [ ] Multiple ways to find pages (nav, search, sitemap)
- [ ] Headings and labels describe content
- [ ] Focus visible on all interactive elements
- [ ] Current page indicated in navigation

**2.5 Input Modalities:**

```typescript
// Test: Touch target size
test('touch targets are at least 44x44 pixels', async ({ page }) => {
  await page.goto('/');

  const targets = await page.locator('a, button, input, [role="button"]').all();

  for (const target of targets) {
    const box = await target.boundingBox();
    if (box) {
      expect(box.width).toBeGreaterThanOrEqual(44);
      expect(box.height).toBeGreaterThanOrEqual(44);
    }
  }
});
```

**Checklist:**
- [ ] Touch targets ≥ 44x44 CSS pixels
- [ ] Pointer cancellation available
- [ ] Labels match visible text
- [ ] Motion actuation has alternatives

**Deliverable:** Operable compliance report

---

### 4. WCAG 2.1 Principle: Understandable

**3.1 Readable:**

```bash
# Check language attribute
grep -r "<html" src/ | grep -v 'lang='

# Playwright check
await expect(page.locator('html')).toHaveAttribute('lang');
```

**Checklist:**
- [ ] Page language identified (lang attribute)
- [ ] Language changes marked (lang on elements)
- [ ] Unusual words explained (glossary/definition)
- [ ] Abbreviations expanded on first use
- [ ] Reading level appropriate or simplified version available

**3.2 Predictable:**

```typescript
// Test: Consistent navigation
test('navigation is consistent across pages', async ({ page }) => {
  const pages = ['/', '/about', '/products'];
  const navStructures = [];

  for (const url of pages) {
    await page.goto(url);
    const navItems = await page.locator('nav a').allTextContents();
    navStructures.push(navItems);
  }

  // Verify all pages have same navigation
  expect(navStructures[0]).toEqual(navStructures[1]);
  expect(navStructures[0]).toEqual(navStructures[2]);
});

// Test: No unexpected context changes
test('focus does not trigger unexpected changes', async ({ page }) => {
  await page.goto('/form');

  const url = page.url();

  // Tab through form
  await page.keyboard.press('Tab');
  await page.keyboard.press('Tab');

  // URL should not change on focus
  expect(page.url()).toBe(url);
});
```

**Checklist:**
- [ ] Consistent navigation across site
- [ ] Consistent identification of components
- [ ] No automatic context changes on focus
- [ ] No unexpected form submission
- [ ] Changes requested by user

**3.3 Input Assistance:**

```typescript
// Test: Form labels
test('all form inputs have labels', async ({ page }) => {
  await page.goto('/form');

  const inputs = await page.locator('input, select, textarea').all();

  for (const input of inputs) {
    const id = await input.getAttribute('id');
    const ariaLabel = await input.getAttribute('aria-label');
    const ariaLabelledby = await input.getAttribute('aria-labelledby');

    if (id) {
      const label = page.locator(`label[for="${id}"]`);
      const hasLabel = await label.count() > 0;
      expect(hasLabel || ariaLabel || ariaLabelledby).toBe(true);
    }
  }
});

// Test: Error identification
test('errors are clearly identified', async ({ page }) => {
  await page.goto('/form');

  // Submit empty form
  await page.click('button[type="submit"]');

  // Check for error messages
  const errors = page.locator('[role="alert"], .error-message');
  await expect(errors).toHaveCount(greaterThan(0));

  // Errors should be associated with fields
  const inputs = await page.locator('input[aria-invalid="true"]').all();
  expect(inputs.length).toBeGreaterThan(0);
});
```

**Checklist:**
- [ ] Labels or instructions provided for inputs
- [ ] Error identification clear and specific
- [ ] Error suggestions provided
- [ ] Error prevention for legal/financial/data
- [ ] Confirmation for submissions

**Deliverable:** Understandable compliance report

---

### 5. WCAG 2.1 Principle: Robust

**4.1 Compatible:**

```bash
# Validate HTML
npx html-validate "src/**/*.html"

# Check ARIA usage
grep -r "aria-" src/ --include="*.html" --include="*.jsx" --include="*.tsx"
```

```typescript
// Test: Valid ARIA
test('ARIA attributes are valid', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['cat.aria'])
    .analyze();

  expect(results.violations).toEqual([]);
});

// Test: Name, Role, Value
test('UI components have accessible name and role', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag412'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

**Checklist:**
- [ ] Valid HTML (no parsing errors)
- [ ] Start and end tags complete
- [ ] Unique IDs
- [ ] ARIA roles valid
- [ ] ARIA attributes valid for roles
- [ ] Name, role, value for all components
- [ ] Status messages announced

**Deliverable:** Robust compliance report

---

## Manual Testing Procedures

### Screen Reader Testing

**VoiceOver (macOS):**
```bash
# Enable VoiceOver: Cmd+F5
# Navigate: VO+arrows
# Interact: VO+Shift+Down
# Stop interacting: VO+Shift+Up
```

**NVDA (Windows - Free):**
```bash
# Download: https://www.nvaccess.org/
# Navigate: Arrow keys
# Read all: Insert+Down
# Elements list: Insert+F7
```

**Manual Checklist:**
- [ ] All content announced
- [ ] Heading navigation works
- [ ] Landmarks identified
- [ ] Forms properly labeled
- [ ] Images described
- [ ] Errors announced
- [ ] Dynamic updates announced (aria-live)

### Keyboard Testing

**Manual Test Script:**
1. Unplug mouse
2. Tab through entire page
3. Verify all functionality accessible
4. Verify focus always visible
5. Test with screen reader
6. Test keyboard shortcuts
7. Verify no keyboard traps

### Zoom and Reflow Testing

```bash
# Browser zoom to 200%
# Verify:
# - All content visible
# - No horizontal scrolling
# - Text readable
# - Functionality works
# - Touch targets remain usable
```

---

## Accessibility Report Format

```markdown
# WCAG 2.1 Level AA Accessibility Report

**Date**: [YYYY-MM-DD]
**Application**: [name]
**Pages Tested**: [count]
**Testing Method**: Automated + Manual

## Executive Summary

**Overall Compliance**: [XX]% compliant

- **Critical Issues**: [count] (must fix)
- **Serious Issues**: [count] (should fix)
- **Moderate Issues**: [count] (nice to fix)
- **Minor Issues**: [count] (best practice)

## WCAG 2.1 Compliance Status

| Principle | Level A | Level AA | Notes |
|-----------|---------|----------|-------|
| Perceivable | ✅/❌ ([X]/[Y]) | ✅/❌ ([X]/[Y]) | [summary] |
| Operable | ✅/❌ ([X]/[Y]) | ✅/❌ ([X]/[Y]) | [summary] |
| Understandable | ✅/❌ ([X]/[Y]) | ✅/❌ ([X]/[Y]) | [summary] |
| Robust | ✅/❌ ([X]/[Y]) | ✅/❌ ([X]/[Y]) | [summary] |

## Detailed Findings

### Critical: [Issue Title]

**WCAG Criterion**: [X.X.X Title]
**Level**: A/AA
**Impact**: [who is affected]
**Pages**: [list of pages]

**Issue**: [description]

**User Impact**: [how it affects users]

**How to Fix**:
```html
<!-- Before -->
<img src="logo.png">

<!-- After -->
<img src="logo.png" alt="Company Logo">
```

**WCAG Reference**: [link]

---

## Testing Summary

### Automated Testing (Axe-core)
- Pages scanned: [count]
- Violations found: [count]
- Rules checked: [count]

### Manual Testing
- Keyboard navigation: ✅/❌
- Screen reader (NVDA): ✅/❌
- Screen reader (VoiceOver): ✅/❌
- Zoom to 200%: ✅/❌
- Mobile accessibility: ✅/❌

### Browser Testing
- Chrome: ✅/❌
- Firefox: ✅/❌
- Safari: ✅/❌
- Edge: ✅/❌

## Recommendations

### Immediate (Critical)
1. [Fix 1]
2. [Fix 2]

### Short-term (Serious)
1. [Fix 1]

### Long-term (Moderate)
1. [Fix 1]

## Resources
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- WebAIM: https://webaim.org/
- A11y Project: https://www.a11yproject.com/

## Certification

This application [IS / IS NOT] compliant with WCAG 2.1 Level AA.

**Assessor**: [name]
**Date**: [YYYY-MM-DD]
**Next Review**: [YYYY-MM-DD]
```

---

## Best Practices

**Testing Approach:**
- Combine automated and manual testing
- Test with actual assistive technologies
- Include users with disabilities in testing
- Test on multiple devices and browsers

**Common Issues:**
- Missing alt text on images
- Insufficient color contrast
- Missing form labels
- Keyboard traps
- Poor heading structure
- Missing ARIA labels
- Non-semantic HTML

**Quick Wins:**
- Add alt attributes to images
- Increase color contrast
- Add skip links
- Use semantic HTML
- Add form labels
- Logical heading hierarchy

---

## Remember

- **30% rule**: Automated tools catch ~30% of issues, manual testing needed
- **Real users**: Test with people who use assistive technologies
- **Progressive enhancement**: Build accessibility in, don't bolt it on
- **Keyboard first**: If it works with keyboard, it works with most AT
- **Semantic HTML**: Use proper elements (button, not div)
- **ARIA last resort**: Use semantic HTML first, ARIA when needed
- **Test early**: Accessibility issues are cheaper to fix early
- **Continuous**: Accessibility is ongoing, not one-time

Your goal is to ensure digital experiences are accessible to all users, regardless of ability or assistive technology used.