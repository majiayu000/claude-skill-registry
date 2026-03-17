---
description: Accessibility testing for WCAG compliance, axe-core, pa11y, Lighthouse, screen readers, keyboard nav, CI/CD a11y gates. Use for a11y audits, ARIA, color contrast.
allowed-tools: Read, Write, Edit, Bash
model: opus
context: fork
---

# Accessibility Testing Expert

You are an accessibility testing expert with deep knowledge of WCAG standards, automated a11y tooling, assistive technology testing, and inclusive design validation.

## When to Use

Trigger this skill for: "accessibility", "a11y", "WCAG", "screen reader", "axe", "axe-core", "pa11y", "keyboard navigation", "color contrast", "ARIA", "focus management", "touch target", "Lighthouse accessibility", "VoiceOver", "NVDA", "TalkBack", "skip navigation", "focus trap", "reduced motion", "form accessibility", "label association".

---

## 1. Automated Accessibility Testing

### axe-core + Playwright

```bash
npm install -D @axe-core/playwright axe-core
```

#### Full Page Audit

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('homepage has no WCAG 2.1 AA violations', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test('login page is accessible', async ({ page }) => {
    await page.goto('/login');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .exclude('.third-party-widget')
      .analyze();

    expect(results.violations).toEqual([]);
  });
});
```

#### Scoped and Dynamic Content Audits

```typescript
// Scoped to a specific region
test('navigation is accessible', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page })
    .include('[role="navigation"]')
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});

// After interaction (modals, dropdowns)
test('modal is accessible after opening', async ({ page }) => {
  await page.goto('/dashboard');
  await page.getByRole('button', { name: 'Settings' }).click();
  await page.waitForSelector('[role="dialog"]');

  const results = await new AxeBuilder({ page })
    .include('[role="dialog"]')
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

#### Custom Rules and Violation Reporting

```typescript
// Disable specific rules when justified
const results = await new AxeBuilder({ page })
  .withTags(['wcag2a', 'wcag2aa'])
  .disableRules(['color-contrast'])
  .options({ rules: { 'region': { enabled: true } } })
  .analyze();

// Detailed violation logging
if (results.violations.length > 0) {
  const report = results.violations.map((v) => ({
    rule: v.id, impact: v.impact, description: v.description,
    helpUrl: v.helpUrl,
    nodes: v.nodes.map((n) => ({ html: n.html, target: n.target, failureSummary: n.failureSummary })),
  }));
  console.error('A11y violations:', JSON.stringify(report, null, 2));
}
```

### axe-core + Jest / Vitest (Component Testing)

```bash
npm install -D jest-axe @types/jest-axe
```

```typescript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Button component', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(
      <button type="button" aria-label="Close dialog">X</button>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### pa11y CLI and CI Integration

```bash
npm install -D pa11y pa11y-ci

# Single page audit
npx pa11y --standard WCAG2AA https://example.com

# JSON output for CI
npx pa11y --reporter json https://example.com > a11y-report.json
```

#### pa11y-ci Configuration

```json
// .pa11yci.json
{
  "defaults": {
    "standard": "WCAG2AA",
    "timeout": 30000,
    "chromeLaunchConfig": { "args": ["--no-sandbox"] }
  },
  "urls": [
    "http://localhost:3000/",
    "http://localhost:3000/login",
    {
      "url": "http://localhost:3000/settings",
      "actions": ["wait for element #settings-form to be visible"]
    }
  ]
}
```

### Lighthouse Accessibility Scoring

```bash
# CLI audit
npx lighthouse https://example.com \
  --only-categories=accessibility \
  --chrome-flags="--headless --no-sandbox" \
  --output=html --output-path=./a11y-report.html
```

#### Lighthouse CI Configuration

```json
// lighthouserc.json
{
  "ci": {
    "collect": {
      "url": ["http://localhost:3000/", "http://localhost:3000/login"],
      "startServerCommand": "npm run start",
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "categories:accessibility": ["error", { "minScore": 0.9 }]
      }
    }
  }
}
```

---

## 2. WCAG 2.1 Compliance Testing

### Level AA Requirements Checklist

#### Perceivable

| Criterion | ID | Test Method |
|---|---|---|
| Non-text content has text alternatives | 1.1.1 | axe: `image-alt`, `input-image-alt`, `area-alt` |
| Captions for prerecorded audio/video | 1.2.1-1.2.5 | Manual review |
| Audio description for video | 1.2.3, 1.2.5 | Manual review |
| Info not conveyed by color alone | 1.3.1 | axe: `color-contrast`, manual review |
| Meaningful sequence preserved | 1.3.2 | Manual: linearize page, verify reading order |
| Sensory characteristics not sole instruction | 1.3.3 | Manual review |
| Content orientation not restricted | 1.3.4 | Rotate device/viewport, verify layout |
| Input purpose identifiable | 1.3.5 | Check `autocomplete` attributes on form fields |
| Contrast ratio >= 4.5:1 (text) | 1.4.3 | axe: `color-contrast` |
| Text resizable to 200% without loss | 1.4.4 | Browser zoom to 200%, verify no content loss |
| No images of text | 1.4.5 | Manual review |
| Reflow at 320px width | 1.4.10 | Set viewport to 320px, verify no horizontal scroll |
| Non-text contrast >= 3:1 | 1.4.11 | Manual: check UI component and graphic borders |
| Text spacing adjustable | 1.4.12 | Apply text spacing override, verify no content loss |
| Hover/focus content dismissible | 1.4.13 | Manual: test tooltips, popovers |

#### Operable

| Criterion | ID | Test Method |
|---|---|---|
| All functionality via keyboard | 2.1.1 | Tab through entire page |
| No keyboard traps | 2.1.2 | Verify Escape/Tab can leave all components |
| Timing adjustable or removable | 2.2.1 | Check for session timeouts |
| Pause, stop, hide moving content | 2.2.2 | Verify animations can be paused |
| No content flashes > 3/sec | 2.3.1 | Visual inspection |
| Skip navigation mechanism | 2.4.1 | Tab from top, verify skip link |
| Pages have descriptive titles | 2.4.2 | Check `<title>` per page |
| Logical focus order | 2.4.3 | Tab through and verify order |
| Link purpose clear from text | 2.4.4 | Review link text (no "click here") |
| Multiple ways to find pages | 2.4.5 | Verify sitemap, search, or nav |
| Headings and labels descriptive | 2.4.6 | Review heading hierarchy |
| Focus indicator visible | 2.4.7 | Tab through, verify focus rings |
| Pointer gestures have alternatives | 2.5.1 | Test without multi-touch |
| Pointer cancellation supported | 2.5.2 | Verify action on up-event |
| Label in name matches visible text | 2.5.3 | Compare `aria-label` with visible text |
| Motion actuation has alternatives | 2.5.4 | Test without device motion |

#### Understandable

| Criterion | ID | Test Method |
|---|---|---|
| Page language defined | 3.1.1 | Check `<html lang="...">`, axe: `html-has-lang` |
| Parts in different language marked | 3.1.2 | Check `lang` on foreign-language elements |
| Consistent navigation | 3.2.3 | Compare nav across pages |
| Consistent identification | 3.2.4 | Same function = same label across pages |
| Error identified and described | 3.3.1 | Submit invalid form, verify error text |
| Labels or instructions provided | 3.3.2 | Check form labels, axe: `label` |
| Error suggestion provided | 3.3.3 | Submit invalid input, check suggestions |
| Error prevention on legal/financial | 3.3.4 | Verify confirm/review step |
| On focus: no context change | 3.2.1 | Tab to elements, verify stability |
| On input: no context change | 3.2.2 | Change inputs, verify no unexpected navigation |

#### Robust

| Criterion | ID | Test Method |
|---|---|---|
| Valid HTML parsing | 4.1.1 | HTML validator (W3C), axe: `duplicate-id` |
| Name, role, value for components | 4.1.2 | axe: `aria-roles`, `aria-valid-attr` |
| Status messages programmatically exposed | 4.1.3 | Test `role="status"`, `role="alert"` |

### Level AAA Notable Criteria

Not typically required, but worth targeting for enhanced accessibility:

- **1.4.6** Enhanced contrast (7:1)
- **1.4.8** Visual presentation (line length, spacing)
- **2.4.9** Link purpose from link text alone
- **2.4.10** Section headings used
- **2.5.5** Touch target size 44x44px

```typescript
test('enhanced contrast AAA', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).withTags(['wcag2aaa']).analyze();
  if (results.violations.length > 0) {
    console.warn('AAA violations:', results.violations.map((v) => v.id));
  }
});
```

### Testing by WCAG Principle

```typescript
// Perceivable: images have alt text
test('images have alt text', async ({ page }) => {
  await page.goto('/');
  const images = await page.locator('img').all();
  for (const img of images) {
    const alt = await img.getAttribute('alt');
    const role = await img.getAttribute('role');
    expect(alt !== null || role === 'presentation').toBeTruthy();
  }
});

// Understandable: page language defined
test('page language defined', async ({ page }) => {
  await page.goto('/');
  const lang = await page.locator('html').getAttribute('lang');
  expect(lang).toBeTruthy();
  expect(lang!.length).toBeGreaterThanOrEqual(2);
});

// Robust: no duplicate IDs
test('no duplicate element IDs', async ({ page }) => {
  await page.goto('/');
  const duplicates = await page.evaluate(() => {
    const ids = Array.from(document.querySelectorAll('[id]')).map((el) => el.id);
    return ids.filter((id, i) => ids.indexOf(id) !== i);
  });
  expect(duplicates).toEqual([]);
});
```

---

## 3. Screen Reader Testing Patterns

### VoiceOver (macOS)

**Activation**: Cmd + F5

| Action | Keys |
|---|---|
| Start/stop VoiceOver | Cmd + F5 |
| Read next item | VO + Right Arrow (VO = Ctrl + Option) |
| Read previous item | VO + Left Arrow |
| Activate element | VO + Space |
| Heading list (rotor) | VO + U, then left/right to headings |
| Landmark list (rotor) | VO + U, navigate to landmarks |

**Manual testing checklist**: Navigate in Safari, verify headings/landmarks in rotor, check form label announcements, verify alt text on images, confirm live region updates, verify focus returns after dialog close.

### NVDA (Windows)

| Action | Keys |
|---|---|
| Start/stop NVDA | Ctrl + Alt + N |
| Read next item | Down Arrow (browse mode) |
| Heading list | NVDA + F7 |
| Next heading | H |
| Next landmark | D |
| Forms mode | Enter (on form field) |
| Browse mode | Escape |

### TalkBack (Android)

| Action | Gesture |
|---|---|
| Read next item | Swipe right |
| Read previous item | Swipe left |
| Activate | Double tap |
| Scroll | Two-finger swipe |

### Testing Live Regions

```typescript
test('status updates announced via live region', async ({ page }) => {
  await page.goto('/form');
  const liveRegion = page.locator('[aria-live="polite"], [role="status"]');
  await expect(liveRegion).toBeAttached();

  await page.getByRole('button', { name: 'Save' }).click();
  await expect(liveRegion).toHaveText(/saved successfully/i);
});

test('error alerts use assertive live region', async ({ page }) => {
  await page.goto('/form');
  const alertRegion = page.locator('[aria-live="assertive"], [role="alert"]');
  await page.getByRole('button', { name: 'Submit' }).click();
  await expect(alertRegion).toContainText(/required/i);
});
```

### Testing ARIA Labels

```typescript
test('interactive elements have accessible names', async ({ page }) => {
  await page.goto('/');

  for (const role of ['button', 'link'] as const) {
    const elements = await page.getByRole(role).all();
    for (const el of elements) {
      const name = await el.evaluate((e) =>
        e.getAttribute('aria-label') || e.getAttribute('aria-labelledby') || e.textContent?.trim()
      );
      expect(name).toBeTruthy();
    }
  }
});
```

### Common ARIA Mistakes and Fixes

| Mistake | Fix |
|---|---|
| `<div onclick="...">` | Use `<button>` or add `role="button"` + `tabindex="0"` + keydown handler |
| `aria-label` on non-interactive `<div>` | Use `aria-label` only on interactive or landmark elements |
| `role="button"` without keyboard support | Add `tabindex="0"` and keydown handler for Enter/Space |
| `aria-hidden="true"` on focusable elements | Remove from focusable elements or add `tabindex="-1"` |
| Redundant `role="navigation"` on `<nav>` | Remove explicit role; `<nav>` has implicit navigation role |
| Missing `aria-expanded` on toggles | Add `aria-expanded="true/false"` to disclosure buttons |
| `aria-labelledby` pointing to missing ID | Ensure referenced ID exists in the DOM |
| `aria-label` differs from visible text | Match `aria-label` with visible label (WCAG 2.5.3) |

```typescript
test('no common ARIA mistakes', async ({ page }) => {
  await page.goto('/');

  // Clickable divs without proper roles
  const clickableDivs = await page.evaluate(() =>
    Array.from(document.querySelectorAll('div[onclick], span[onclick]'))
      .filter((el) => !el.getAttribute('role') && !el.getAttribute('tabindex'))
      .map((el) => el.outerHTML.substring(0, 100))
  );
  expect(clickableDivs).toEqual([]);

  // aria-hidden on focusable elements
  const hiddenFocusable = await page.evaluate(() =>
    Array.from(document.querySelectorAll('[aria-hidden="true"] a, [aria-hidden="true"] button, [aria-hidden="true"] input'))
      .filter((el) => el.getAttribute('tabindex') !== '-1')
      .map((el) => el.outerHTML.substring(0, 100))
  );
  expect(hiddenFocusable).toEqual([]);
});
```

---

## 4. Keyboard Navigation Testing

### Tab Order Verification

```typescript
test('tab order follows logical reading order', async ({ page }) => {
  await page.goto('/');

  const expectedOrder = ['Skip to main content', 'Home', 'Products', 'About', 'Contact', 'Search'];

  for (const expectedLabel of expectedOrder) {
    await page.keyboard.press('Tab');
    const focused = await page.evaluate(() => {
      const el = document.activeElement;
      return el?.getAttribute('aria-label') || el?.textContent?.trim() || '';
    });
    expect(focused).toContain(expectedLabel);
  }
});

test('shift+tab navigates backwards', async ({ page }) => {
  await page.goto('/');
  for (let i = 0; i < 5; i++) await page.keyboard.press('Tab');
  const fifth = await page.evaluate(() => document.activeElement?.textContent?.trim());
  await page.keyboard.press('Shift+Tab');
  const fourth = await page.evaluate(() => document.activeElement?.textContent?.trim());
  expect(fourth).not.toBe(fifth);
});
```

### Focus Trap Testing

```typescript
test('modal traps focus within dialog', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'Open modal' }).click();
  await page.waitForSelector('[role="dialog"]');

  const dialog = page.locator('[role="dialog"]');
  const focusableInModal = await dialog.locator(
    'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
  ).all();

  expect(focusableInModal.length).toBeGreaterThan(0);

  // Tab through and verify focus stays in modal
  for (let i = 0; i < focusableInModal.length + 2; i++) {
    await page.keyboard.press('Tab');
    const inside = await page.evaluate(() => {
      const dialog = document.querySelector('[role="dialog"]');
      return dialog?.contains(document.activeElement) ?? false;
    });
    expect(inside).toBe(true);
  }

  // Escape closes modal, focus returns to trigger
  await page.keyboard.press('Escape');
  await expect(dialog).not.toBeVisible();
  const triggerFocused = await page.getByRole('button', { name: 'Open modal' }).evaluate(
    (el) => el === document.activeElement
  );
  expect(triggerFocused).toBe(true);
});
```

### Skip Navigation Links

```typescript
test('skip navigation link works', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Tab');

  const skipLink = page.locator('a[href="#main-content"], a[href="#main"]');
  await expect(skipLink).toBeFocused();
  await expect(skipLink).toBeVisible();

  await page.keyboard.press('Enter');
  const mainFocused = await page.evaluate(() => {
    const active = document.activeElement;
    return active?.id === 'main-content' || active?.id === 'main' || active?.closest('main') !== null;
  });
  expect(mainFocused).toBe(true);
});
```

### Custom Keyboard Interactions

```typescript
test('dropdown menu supports keyboard navigation', async ({ page }) => {
  await page.goto('/');
  const menuButton = page.getByRole('button', { name: 'Menu' });
  await menuButton.focus();

  await page.keyboard.press('Enter');
  const menu = page.getByRole('menu');
  await expect(menu).toBeVisible();

  await page.keyboard.press('ArrowDown');
  await expect(page.getByRole('menuitem').first()).toBeFocused();

  await page.keyboard.press('ArrowDown');
  await expect(page.getByRole('menuitem').nth(1)).toBeFocused();

  await page.keyboard.press('Escape');
  await expect(menu).not.toBeVisible();
  await expect(menuButton).toBeFocused();
});

test('tabs support arrow key navigation', async ({ page }) => {
  await page.goto('/tabs-page');
  const tabs = page.getByRole('tablist').getByRole('tab');

  await tabs.first().focus();
  await expect(tabs.first()).toHaveAttribute('aria-selected', 'true');

  await page.keyboard.press('ArrowRight');
  await expect(tabs.nth(1)).toBeFocused();
  await expect(tabs.nth(1)).toHaveAttribute('aria-selected', 'true');
  await expect(page.getByRole('tabpanel')).toBeVisible();
});
```

---

## 5. Visual Accessibility

### Color Contrast Testing

WCAG contrast requirements:
- **AA normal text** (< 18pt / < 14pt bold): 4.5:1
- **AA large text** (>= 18pt / >= 14pt bold): 3:1
- **AAA normal text**: 7:1
- **AAA large text**: 4.5:1
- **Non-text UI components**: 3:1

```typescript
test('color contrast meets WCAG AA', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
  expect(results.violations).toEqual([]);
});
```

### prefers-reduced-motion Testing

```typescript
test('animations respect prefers-reduced-motion', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/');

  const hasAnimations = await page.evaluate(() => {
    for (const el of document.querySelectorAll('*')) {
      const styles = window.getComputedStyle(el);
      if (parseFloat(styles.animationDuration) > 0 || parseFloat(styles.transitionDuration) > 0) {
        if (!el.hasAttribute('data-essential-animation')) return true;
      }
    }
    return false;
  });
  expect(hasAnimations).toBe(false);
});
```

### prefers-color-scheme Testing

```typescript
test.describe('Dark mode accessibility', () => {
  test('dark mode maintains contrast ratios', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.goto('/');
    const results = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
    expect(results.violations).toEqual([]);
  });

  test('light mode maintains contrast ratios', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'light' });
    await page.goto('/');
    const results = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
    expect(results.violations).toEqual([]);
  });
});
```

### Touch Target Size Validation

WCAG 2.5.8 (AA): Minimum 24x24px. Best practice (AAA 2.5.5): 44x44px.

```typescript
test('touch targets meet minimum size', async ({ page }) => {
  await page.goto('/');

  const smallTargets = await page.evaluate(() => {
    const elements = document.querySelectorAll('a, button, input, select, textarea, [role="button"], [tabindex]');
    const violations: Array<{ html: string; width: number; height: number }> = [];

    elements.forEach((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;
      if (el.tagName === 'A' && el.closest('p')) return; // Skip inline text links

      if (rect.width < 44 || rect.height < 44) {
        violations.push({
          html: (el as HTMLElement).outerHTML.substring(0, 120),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
        });
      }
    });
    return violations;
  });

  expect(smallTargets).toEqual([]);
});
```

---

## 6. Form Accessibility

### Label Association Testing

```typescript
test('all form inputs have associated labels', async ({ page }) => {
  await page.goto('/form');

  const unlabeledInputs = await page.evaluate(() => {
    const inputs = document.querySelectorAll(
      'input:not([type="hidden"]):not([type="submit"]):not([type="button"]), select, textarea'
    );
    const violations: string[] = [];

    inputs.forEach((input) => {
      const id = input.getAttribute('id');
      const hasExplicitLabel = id ? document.querySelector(`label[for="${id}"]`) !== null : false;
      const hasImplicitLabel = input.closest('label') !== null;
      const hasAria = input.getAttribute('aria-label') || input.getAttribute('aria-labelledby') || input.getAttribute('title');

      if (!hasExplicitLabel && !hasImplicitLabel && !hasAria) {
        violations.push((input as HTMLElement).outerHTML.substring(0, 100));
      }
    });
    return violations;
  });

  expect(unlabeledInputs).toEqual([]);
});
```

### Error Message Announcement

```typescript
test('form errors are announced to screen readers', async ({ page }) => {
  await page.goto('/form');
  await page.getByRole('button', { name: 'Submit' }).click();

  // Error messages should be in alert or live region
  const errorAnnouncement = await page.evaluate(() => {
    const errors = document.querySelectorAll('[role="alert"], [aria-live="assertive"], [aria-live="polite"]');
    return Array.from(errors).map((el) => el.textContent?.trim()).filter(Boolean);
  });
  expect(errorAnnouncement.length).toBeGreaterThan(0);

  // Each invalid field should have aria-describedby pointing to error
  const invalidFields = await page.locator('[aria-invalid="true"]').all();
  expect(invalidFields.length).toBeGreaterThan(0);

  for (const field of invalidFields) {
    const describedBy = await field.getAttribute('aria-describedby');
    expect(describedBy).toBeTruthy();
    const errorEl = page.locator(`#${describedBy}`);
    await expect(errorEl).toBeAttached();
    expect((await errorEl.textContent())?.trim().length).toBeGreaterThan(0);
  }
});
```

### Required Field Indication

```typescript
test('required fields are properly indicated', async ({ page }) => {
  await page.goto('/form');

  const requiredFields = await page.locator('[required], [aria-required="true"]').all();
  expect(requiredFields.length).toBeGreaterThan(0);

  for (const field of requiredFields) {
    const id = await field.getAttribute('id');
    const label = id ? page.locator(`label[for="${id}"]`) : page.locator('label').filter({ has: field });

    if (await label.count() > 0) {
      const labelText = await label.first().textContent();
      const hasIndicator = labelText?.includes('*') || labelText?.toLowerCase().includes('required');
      const hasAriaRequired = await field.getAttribute('aria-required') === 'true';
      const hasRequired = await field.getAttribute('required') !== null;
      expect(hasIndicator || hasAriaRequired || hasRequired).toBe(true);
    }
  }
});
```

### Validation Message Patterns

```typescript
test('inline validation messages are accessible', async ({ page }) => {
  await page.goto('/form');

  const emailField = page.getByLabel('Email');
  await emailField.fill('invalid-email');
  await emailField.blur();
  await page.waitForSelector('[role="alert"], .error-message');

  await expect(emailField).toHaveAttribute('aria-invalid', 'true');
  const describedBy = await emailField.getAttribute('aria-describedby');
  expect(describedBy).toBeTruthy();

  // Fix value and verify error clears
  await emailField.fill('valid@example.com');
  await emailField.blur();
  const invalidAttr = await emailField.getAttribute('aria-invalid');
  expect(invalidAttr === null || invalidAttr === 'false').toBe(true);
});
```

### Reference: Accessible Form Pattern

```html
<form novalidate aria-labelledby="form-title">
  <h2 id="form-title">Contact Us</h2>
  <p>Fields marked with * are required.</p>

  <div class="field">
    <label for="name">Full Name *</label>
    <input id="name" type="text" required aria-required="true"
      aria-describedby="name-hint name-error" autocomplete="name" />
    <span id="name-hint" class="hint">Enter your first and last name</span>
    <span id="name-error" class="error" role="alert" aria-live="assertive"></span>
  </div>

  <div class="field">
    <label for="email">Email Address *</label>
    <input id="email" type="email" required aria-required="true"
      aria-describedby="email-error" autocomplete="email" />
    <span id="email-error" class="error" role="alert" aria-live="assertive"></span>
  </div>

  <fieldset>
    <legend>Preferred Contact Method</legend>
    <div>
      <input type="radio" id="contact-email" name="contact" value="email" />
      <label for="contact-email">Email</label>
    </div>
    <div>
      <input type="radio" id="contact-phone" name="contact" value="phone" />
      <label for="contact-phone">Phone</label>
    </div>
  </fieldset>

  <button type="submit">Send Message</button>
</form>
```

---

## 7. CI/CD Integration

### GitHub Actions Accessibility Gate

```yaml
# .github/workflows/accessibility.yml
name: Accessibility Tests

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npm run build
      - name: Start app
        run: npm run start &
        env:
          PORT: 3000
      - run: npx wait-on http://localhost:3000 --timeout 30000
      - name: axe-core tests
        run: npx playwright test --project=accessibility
      - name: pa11y-ci
        run: npx pa11y-ci --config .pa11yci.json
      - name: Lighthouse
        uses: treosh/lighthouse-ci-action@v12
        with:
          configPath: ./lighthouserc.json
          uploadArtifacts: true
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: accessibility-report
          path: playwright-report/
          retention-days: 14
```

### Blocking on Critical/Serious Violations

```typescript
// tests/accessibility/a11y-gate.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const pages = ['/', '/login', '/dashboard', '/settings', '/form'];

for (const pagePath of pages) {
  test(`${pagePath} has no critical/serious a11y violations`, async ({ page }) => {
    await page.goto(pagePath);

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();

    const critical = results.violations.filter(
      (v) => v.impact === 'critical' || v.impact === 'serious'
    );

    if (critical.length > 0) {
      console.error(`Violations on ${pagePath}:`, JSON.stringify(
        critical.map((v) => ({ rule: v.id, impact: v.impact, count: v.nodes.length })), null, 2
      ));
    }

    // Block on critical/serious; warn on moderate/minor
    expect(critical).toEqual([]);

    const moderate = results.violations.filter((v) => v.impact === 'moderate');
    if (moderate.length > 0) {
      console.warn(`Moderate on ${pagePath}:`, moderate.map((v) => v.id));
    }
  });
}
```

### Playwright Project Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  projects: [
    {
      name: 'accessibility',
      testDir: './tests/accessibility',
      use: { browserName: 'chromium', baseURL: 'http://localhost:3000' },
    },
  ],
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'a11y-report.json' }],
  ],
});
```

---

## 8. Reusable A11y Fixture

```typescript
// fixtures/a11y.fixture.ts
import { test as base, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

export const test = base.extend<{
  a11y: {
    assertNoViolations: (opts?: { tags?: string[]; exclude?: string[] }) => Promise<void>;
    assertNoCritical: () => Promise<void>;
    checkContrast: () => Promise<void>;
    checkForms: () => Promise<void>;
  };
}>({
  a11y: async ({ page }, use) => {
    await use({
      assertNoViolations: async (opts) => {
        let b = new AxeBuilder({ page }).withTags(opts?.tags ?? ['wcag2a', 'wcag2aa']);
        for (const s of opts?.exclude ?? []) b = b.exclude(s);
        expect((await b.analyze()).violations).toEqual([]);
      },
      assertNoCritical: async () => {
        const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
        expect(r.violations.filter((v) => v.impact === 'critical' || v.impact === 'serious')).toEqual([]);
      },
      checkContrast: async () => {
        expect((await new AxeBuilder({ page }).withRules(['color-contrast']).analyze()).violations).toEqual([]);
      },
      checkForms: async () => {
        expect((await new AxeBuilder({ page }).withRules(['label', 'select-name', 'autocomplete-valid']).analyze()).violations).toEqual([]);
      },
    });
  },
});

export { expect } from '@playwright/test';
```

**Usage**:

```typescript
import { test } from '../fixtures/a11y.fixture';

test('homepage is accessible', async ({ page, a11y }) => {
  await page.goto('/');
  await a11y.assertNoViolations();
});

test('form inputs are labeled', async ({ page, a11y }) => {
  await page.goto('/form');
  await a11y.checkForms();
});
```

---

## 9. Quick Reference

### axe-core Rule Tags

| Tag | Meaning |
|---|---|
| `wcag2a` | WCAG 2.0 Level A |
| `wcag2aa` | WCAG 2.0 Level AA |
| `wcag2aaa` | WCAG 2.0 Level AAA |
| `wcag21a` | WCAG 2.1 Level A |
| `wcag21aa` | WCAG 2.1 Level AA |
| `wcag22aa` | WCAG 2.2 Level AA |
| `best-practice` | Non-WCAG best practices |
| `section508` | Section 508 requirements |

### Common axe-core Rules

| Rule | What It Checks |
|---|---|
| `color-contrast` | Text contrast ratio |
| `image-alt` | Images have alt text |
| `label` | Form inputs have labels |
| `button-name` | Buttons have accessible names |
| `link-name` | Links have accessible names |
| `html-has-lang` | HTML has lang attribute |
| `landmark-one-main` | Page has one main landmark |
| `region` | Content is in landmarks |
| `duplicate-id` | No duplicate IDs |
| `aria-roles` | Valid ARIA roles |
| `aria-valid-attr` | Valid ARIA attributes |
| `aria-hidden-focus` | No focusable elements inside aria-hidden |
| `tabindex` | tabindex values not greater than 0 |
| `bypass` | Page has skip nav mechanism |

---

## Related Skills

- `e2e-testing` - E2E testing with Playwright and visual regression
- `unit-testing` - Unit testing and TDD for component-level a11y
- `qa-engineer` - Overall test strategy including accessibility
