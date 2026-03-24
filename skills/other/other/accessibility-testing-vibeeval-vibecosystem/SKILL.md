---
name: accessibility-testing
description: axe-core integration, WCAG 2.2 AA checklist, keyboard navigation testing, screen reader testing, and ARIA pattern validation.
---

# Accessibility Testing

## axe-core Setup

### jest-axe (unit / component tests)
```typescript
import { axe, toHaveNoViolations } from 'jest-axe'
import { render } from '@testing-library/react'
expect.extend(toHaveNoViolations)

test('LoginForm has no a11y violations', async () => {
  const { container } = render(<LoginForm />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

### playwright-axe (e2e)
```typescript
import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test('homepage passes axe audit', async ({ page }) => {
  await page.goto('/')
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze()
  expect(results.violations).toEqual([])
})
```

### cypress-axe
```javascript
// cypress/support/e2e.js
import 'cypress-axe'

// in test
cy.visit('/')
cy.injectAxe()
cy.checkA11y(null, {
  runOnly: { type: 'tag', values: ['wcag2aa'] },
})
```

## WCAG 2.2 AA Checklist — Top 20 Violations

| # | Criterion | Check |
|---|-----------|-------|
| 1 | Images have alt text | `<img alt="description">` or `alt=""` for decorative |
| 2 | Form inputs have labels | `<label for>` or `aria-label` or `aria-labelledby` |
| 3 | Color contrast ≥ 4.5:1 | Normal text; 3:1 for large text (18pt or 14pt bold) |
| 4 | Heading hierarchy | h1 → h2 → h3, no skipping levels |
| 5 | Keyboard focusable | All interactive elements reachable via Tab |
| 6 | Focus visible | `:focus` outline never `outline: none` without replacement |
| 7 | No keyboard trap | Tab can always exit modals, dropdowns, widgets |
| 8 | Skip navigation link | First focusable element: "Skip to main content" |
| 9 | Page has `<title>` | Unique, descriptive per page |
| 10 | Language attribute | `<html lang="en">` |
| 11 | Error identification | Form errors are text, not color-only |
| 12 | Error suggestions | Tell users how to fix the error |
| 13 | Link purpose clear | No "click here" or "read more" without context |
| 14 | Button text | No icon-only buttons without `aria-label` |
| 15 | Table headers | `<th scope="col|row">` on data tables |
| 16 | No seizure content | No flashing > 3 times/sec |
| 17 | Status messages | `role="status"` or `aria-live` for dynamic updates |
| 18 | Reflow at 400% zoom | Single column, no horizontal scroll |
| 19 | Text spacing adjustable | No overflow when line-height/letter-spacing increased |
| 20 | Timeout warning | Warn before session expires, allow extension |

## Keyboard Navigation Test Patterns

### Tab order verification
```typescript
test('modal tab order is correct', async ({ page }) => {
  await page.click('[data-testid="open-modal"]')

  // First focus should be the modal's close button or heading
  await expect(page.locator('[aria-label="Close dialog"]')).toBeFocused()

  // Tab through: close → input → submit
  await page.keyboard.press('Tab')
  await expect(page.locator('#email-input')).toBeFocused()

  await page.keyboard.press('Tab')
  await expect(page.locator('[type="submit"]')).toBeFocused()

  // Wrap back to close button (focus trap)
  await page.keyboard.press('Tab')
  await expect(page.locator('[aria-label="Close dialog"]')).toBeFocused()
})
```

### Focus trap in modals
```typescript
// Escape should close
await page.keyboard.press('Escape')
await expect(page.locator('[role="dialog"]')).not.toBeVisible()

// Focus returns to trigger element after close
await expect(page.locator('[data-testid="open-modal"]')).toBeFocused()
```

### Skip navigation link
```typescript
test('skip link goes to main content', async ({ page }) => {
  await page.goto('/')
  await page.keyboard.press('Tab')   // first tab = skip link

  const skipLink = page.locator('a:has-text("Skip to")')
  await expect(skipLink).toBeFocused()

  await page.keyboard.press('Enter')
  await expect(page.locator('main, #main-content')).toBeFocused()
})
```

### Arrow key navigation (listbox/menu)
```typescript
test('dropdown menu responds to arrow keys', async ({ page }) => {
  await page.click('[aria-haspopup="listbox"]')
  await page.keyboard.press('ArrowDown')  // first option focused
  await page.keyboard.press('ArrowDown')  // second option
  await page.keyboard.press('Enter')      // select

  // Verify selection
  await expect(page.locator('[aria-selected="true"]')).toContainText('Option 2')
})
```

## ARIA Patterns

### Live regions (dynamic announcements)
```html
<!-- For important real-time updates (errors, confirmations) -->
<div role="alert">Your payment failed. Please try again.</div>

<!-- For polite updates (search results count) -->
<div aria-live="polite" aria-atomic="true">
  Showing 42 results for "laptop"
</div>

<!-- Screen reader only text (visually hidden) -->
<style>
  .sr-only {
    position: absolute; width: 1px; height: 1px;
    padding: 0; margin: -1px; overflow: hidden;
    clip: rect(0,0,0,0); white-space: nowrap; border: 0;
  }
</style>
```

### Dialog / Modal
```html
<div role="dialog"
     aria-modal="true"
     aria-labelledby="dialog-title"
     aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Delete</h2>
  <p id="dialog-desc">This action cannot be undone.</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

### Tabs
```html
<div role="tablist" aria-label="Account settings">
  <button role="tab" aria-selected="true"  aria-controls="panel-profile" id="tab-profile">Profile</button>
  <button role="tab" aria-selected="false" aria-controls="panel-billing" id="tab-billing" tabindex="-1">Billing</button>
</div>
<div role="tabpanel" id="panel-profile" aria-labelledby="tab-profile">...</div>
<div role="tabpanel" id="panel-billing" aria-labelledby="tab-billing" hidden>...</div>
```

### Combobox / Autocomplete
```html
<label for="search">Search users</label>
<input type="text"
       id="search"
       role="combobox"
       aria-autocomplete="list"
       aria-expanded="true"
       aria-controls="search-listbox"
       aria-activedescendant="opt-2" />
<ul id="search-listbox" role="listbox">
  <li role="option" id="opt-1">Alice</li>
  <li role="option" id="opt-2" aria-selected="true">Bob</li>
</ul>
```

## Color Contrast Requirements

| Text Size | Minimum Ratio | Enhanced (AAA) |
|-----------|--------------|----------------|
| Normal text (< 18pt / < 14pt bold) | 4.5:1 | 7:1 |
| Large text (≥ 18pt or ≥ 14pt bold) | 3:1 | 4.5:1 |
| UI components / icons | 3:1 | — |
| Decorative / disabled | No requirement | — |

Test tools: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/), Figma A11y Plugin, Chrome DevTools CSS Overview.

## VoiceOver Quick Reference (macOS)

| Action | Shortcut |
|--------|----------|
| Start / Stop VoiceOver | Cmd + F5 |
| Read next item | VO + Right Arrow |
| Read page from top | VO + A |
| Navigate headings | VO + Cmd + H |
| Navigate links | VO + Cmd + L |
| Navigate form controls | VO + Cmd + J |
| Open Web Rotor | VO + U |

VO = Control + Option

## Common Violations and Fixes

```html
<!-- VIOLATION: Missing alt -->
<img src="logo.png" />
<!-- FIX -->
<img src="logo.png" alt="Acme Corp logo" />
<!-- Decorative: -->
<img src="divider.png" alt="" role="presentation" />

<!-- VIOLATION: Icon button with no label -->
<button><svg>...</svg></button>
<!-- FIX -->
<button aria-label="Close dialog"><svg aria-hidden="true">...</svg></button>

<!-- VIOLATION: Placeholder as label -->
<input placeholder="Email address" />
<!-- FIX -->
<label for="email">Email address</label>
<input id="email" type="email" placeholder="you@example.com" />

<!-- VIOLATION: Color-only error -->
<input style="border: 2px solid red" />
<!-- FIX -->
<input aria-invalid="true" aria-describedby="email-error" />
<span id="email-error" role="alert">Email is required</span>
```

## CI Integration (axe-core in GitHub Actions)

```yaml
# .github/workflows/a11y.yml
name: Accessibility Tests
on: [pull_request]

jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npm run test:a11y
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: a11y-report
          path: playwright-report/
```
