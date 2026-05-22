---
name: Axe-core Accessibility Testing
description: Accessibility testing skill using axe-core and Playwright for automated WCAG 2.1 compliance auditing, custom rules, and accessibility reporting.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [accessibility, axe-core, wcag, a11y, playwright, automated-audit]
testingTypes: [accessibility]
frameworks: [axe-core, playwright]
languages: [typescript]
domains: [web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Axe-core Accessibility Testing Skill

You are an expert accessibility engineer specializing in automated accessibility testing with axe-core and Playwright. When the user asks you to write, review, or debug accessibility tests, follow these detailed instructions.

## Core Principles

1. **WCAG 2.1 AA as baseline** -- All pages must meet at minimum WCAG 2.1 Level AA.
2. **Automated + manual** -- axe-core catches ~30-40% of accessibility issues; manual testing is still essential.
3. **Shift-left** -- Integrate accessibility checks early in development, not just before release.
4. **Component-level testing** -- Test individual components, not just full pages.
5. **Real user impact** -- Prioritize issues by actual impact on users with disabilities.

## Project Structure

```
tests/
  accessibility/
    pages/
      homepage.a11y.spec.ts
      login.a11y.spec.ts
      dashboard.a11y.spec.ts
    components/
      navigation.a11y.spec.ts
      forms.a11y.spec.ts
      modals.a11y.spec.ts
    utils/
      axe-helper.ts
      a11y-reporter.ts
    config/
      axe-config.ts
playwright.config.ts
```

## Setup

### Installation

```bash
npm install --save-dev @axe-core/playwright axe-core playwright @playwright/test
```

### Axe Configuration

```typescript
// config/axe-config.ts
import { AxeBuilder } from '@axe-core/playwright';
import { Page } from '@playwright/test';

export const DEFAULT_AXE_OPTIONS = {
  runOnly: {
    type: 'tag' as const,
    values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'],
  },
};

export const STRICT_AXE_OPTIONS = {
  runOnly: {
    type: 'tag' as const,
    values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'],
  },
};

export async function runAxeScan(page: Page, options = DEFAULT_AXE_OPTIONS) {
  const results = await new AxeBuilder({ page })
    .options(options)
    .analyze();
  return results;
}

export async function runAxeOnComponent(page: Page, selector: string) {
  const results = await new AxeBuilder({ page })
    .include(selector)
    .options(DEFAULT_AXE_OPTIONS)
    .analyze();
  return results;
}
```

## Writing Accessibility Tests

### Full Page Scan

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Homepage Accessibility', () => {
  test('should have no accessibility violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('should have no critical or serious violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

    const criticalViolations = accessibilityScanResults.violations.filter(
      (v) => v.impact === 'critical' || v.impact === 'serious'
    );

    expect(criticalViolations).toEqual([]);
  });

  test('should pass accessibility after dynamic content loads', async ({ page }) => {
    await page.goto('/');

    // Wait for dynamic content
    await page.getByRole('heading', { name: 'Featured Products' }).waitFor();
    await page.waitForLoadState('networkidle');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();

    expect(results.violations).toEqual([]);
  });
});
```

### Component-Level Scanning

```typescript
test.describe('Navigation Component Accessibility', () => {
  test('navigation menu should be accessible', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .include('nav[aria-label="Main navigation"]')
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test('navigation should have proper ARIA landmarks', async ({ page }) => {
    await page.goto('/');

    // Check for main navigation landmark
    const nav = page.getByRole('navigation', { name: 'Main navigation' });
    await expect(nav).toBeVisible();

    // Check for skip navigation link
    const skipLink = page.getByRole('link', { name: /skip to/i });
    await expect(skipLink).toBeAttached();
  });

  test('mobile menu should be accessible when opened', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    // Open mobile menu
    const menuButton = page.getByRole('button', { name: /menu/i });
    await menuButton.click();

    // Scan the opened menu
    const results = await new AxeBuilder({ page })
      .include('[role="dialog"], [aria-expanded="true"]')
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();

    expect(results.violations).toEqual([]);

    // Verify focus management
    const firstMenuItem = page.getByRole('menuitem').first();
    await expect(firstMenuItem).toBeFocused();
  });
});
```

### Form Accessibility

```typescript
test.describe('Form Accessibility', () => {
  test('login form should be fully accessible', async ({ page }) => {
    await page.goto('/login');

    const results = await new AxeBuilder({ page })
      .include('form')
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test('form inputs should have associated labels', async ({ page }) => {
    await page.goto('/login');

    // Every input should be findable by its label
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
  });

  test('form errors should be announced to screen readers', async ({ page }) => {
    await page.goto('/login');

    // Submit empty form
    await page.getByRole('button', { name: 'Sign in' }).click();

    // Error messages should have appropriate ARIA attributes
    const errorMessages = page.locator('[role="alert"]');
    await expect(errorMessages.first()).toBeVisible();

    // Check aria-describedby links errors to inputs
    const emailInput = page.getByLabel('Email');
    const describedBy = await emailInput.getAttribute('aria-describedby');
    expect(describedBy).toBeTruthy();

    const errorElement = page.locator(`#${describedBy}`);
    await expect(errorElement).toBeVisible();
  });

  test('required fields should be marked with aria-required', async ({ page }) => {
    await page.goto('/login');

    const emailInput = page.getByLabel('Email');
    const passwordInput = page.getByLabel('Password');

    await expect(emailInput).toHaveAttribute('aria-required', 'true');
    await expect(passwordInput).toHaveAttribute('aria-required', 'true');
  });
});
```

### Keyboard Navigation Testing

```typescript
test.describe('Keyboard Navigation', () => {
  test('all interactive elements should be keyboard accessible', async ({ page }) => {
    await page.goto('/');

    // Tab through the page and collect focused elements
    const focusedElements: string[] = [];
    for (let i = 0; i < 20; i++) {
      await page.keyboard.press('Tab');
      const focused = await page.evaluate(() => {
        const el = document.activeElement;
        return el ? `${el.tagName}:${el.textContent?.trim().substring(0, 30)}` : 'none';
      });
      focusedElements.push(focused);
    }

    // Verify that interactive elements are in the tab order
    expect(focusedElements.some((el) => el.includes('Skip'))).toBe(true);
    expect(focusedElements.some((el) => el.includes('A:'))).toBe(true); // Links
  });

  test('modal dialog should trap focus', async ({ page }) => {
    await page.goto('/');

    // Open a modal
    await page.getByRole('button', { name: 'Open dialog' }).click();

    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible();

    // Tab through modal elements
    await page.keyboard.press('Tab');
    const firstFocused = await page.evaluate(() => document.activeElement?.closest('[role="dialog"]') !== null);
    expect(firstFocused).toBe(true);

    // Tab many times -- focus should stay within dialog
    for (let i = 0; i < 20; i++) {
      await page.keyboard.press('Tab');
    }
    const stillInDialog = await page.evaluate(() => document.activeElement?.closest('[role="dialog"]') !== null);
    expect(stillInDialog).toBe(true);

    // Escape should close dialog
    await page.keyboard.press('Escape');
    await expect(dialog).toBeHidden();

    // Focus should return to trigger element
    const triggerFocused = await page.evaluate(() =>
      document.activeElement?.textContent?.includes('Open dialog')
    );
    expect(triggerFocused).toBe(true);
  });

  test('dropdown menu should support arrow key navigation', async ({ page }) => {
    await page.goto('/');

    const menuButton = page.getByRole('button', { name: 'Account menu' });
    await menuButton.focus();
    await page.keyboard.press('Enter');

    // Arrow down should move to first item
    await page.keyboard.press('ArrowDown');
    const firstItem = page.getByRole('menuitem').first();
    await expect(firstItem).toBeFocused();

    // Arrow down again
    await page.keyboard.press('ArrowDown');
    const secondItem = page.getByRole('menuitem').nth(1);
    await expect(secondItem).toBeFocused();
  });
});
```

### Color Contrast and Visual

```typescript
test.describe('Color Contrast', () => {
  test('text elements should meet contrast requirements', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .withRules(['color-contrast'])
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test('focus indicators should be visible', async ({ page }) => {
    await page.goto('/');

    // Tab to first link
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');

    // Check that the focused element has a visible focus indicator
    const focusOutline = await page.evaluate(() => {
      const el = document.activeElement;
      if (!el) return null;
      const styles = window.getComputedStyle(el);
      return {
        outline: styles.outline,
        outlineWidth: styles.outlineWidth,
        boxShadow: styles.boxShadow,
      };
    });

    // Should have either outline or box-shadow for focus
    const hasFocusIndicator =
      (focusOutline?.outlineWidth && focusOutline.outlineWidth !== '0px') ||
      (focusOutline?.boxShadow && focusOutline.boxShadow !== 'none');

    expect(hasFocusIndicator).toBe(true);
  });
});
```

### Excluding Known Issues

```typescript
test('should pass with known exceptions excluded', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .exclude('#third-party-widget')    // Exclude third-party content
    .exclude('.legacy-component')       // Exclude legacy code being refactored
    .disableRules(['color-contrast'])   // Disable specific rules if justified
    .analyze();

  expect(results.violations).toEqual([]);
});
```

## Custom Axe Reporter

```typescript
// utils/a11y-reporter.ts
import { AxeResults, Result } from 'axe-core';

export function formatViolations(violations: Result[]): string {
  if (violations.length === 0) return 'No accessibility violations found.';

  return violations
    .map((violation) => {
      const nodes = violation.nodes.map((node) => {
        return `  - Element: ${node.html}\n    Target: ${node.target.join(', ')}\n    Fix: ${node.failureSummary}`;
      }).join('\n');

      return `
Rule: ${violation.id}
Impact: ${violation.impact}
Description: ${violation.description}
Help: ${violation.helpUrl}
Affected elements:
${nodes}`;
    })
    .join('\n---\n');
}

export function assertNoViolations(results: AxeResults, allowedImpacts: string[] = []) {
  const filteredViolations = results.violations.filter(
    (v) => !allowedImpacts.includes(v.impact || '')
  );

  if (filteredViolations.length > 0) {
    throw new Error(
      `Found ${filteredViolations.length} accessibility violations:\n${formatViolations(filteredViolations)}`
    );
  }
}
```

## WCAG 2.1 Quick Reference

| Level | Guideline | Test Approach |
|-------|-----------|---------------|
| A | 1.1.1 Non-text Content | Check all images have alt text |
| A | 1.3.1 Info and Relationships | Verify headings, lists, tables are semantic |
| A | 2.1.1 Keyboard | Tab through all functionality |
| A | 2.4.1 Bypass Blocks | Verify skip navigation link exists |
| A | 4.1.2 Name, Role, Value | Check ARIA attributes on custom widgets |
| AA | 1.4.3 Contrast (Minimum) | 4.5:1 for normal text, 3:1 for large text |
| AA | 1.4.4 Resize Text | Page usable at 200% zoom |
| AA | 2.4.6 Headings and Labels | Descriptive heading hierarchy |
| AA | 2.4.7 Focus Visible | Visible focus indicator on all elements |
| AA | 1.4.11 Non-text Contrast | 3:1 contrast for UI components |

## Best Practices

1. **Run axe on every page** -- Add accessibility scans to your E2E test suite for all routes.
2. **Test with keyboard only** -- Navigate the entire app without a mouse.
3. **Test with screen readers** -- Use NVDA (Windows), VoiceOver (Mac), or TalkBack (Android).
4. **Test at 200% zoom** -- Content must remain functional when zoomed.
5. **Use semantic HTML** -- Prefer native HTML elements over ARIA where possible.
6. **Test dynamic content** -- Run scans after modals, dropdowns, and AJAX loads.
7. **Include in CI/CD** -- Fail the build on critical accessibility violations.
8. **Document exclusions** -- If you exclude rules or elements, document why.
9. **Test with reduced motion** -- Verify `prefers-reduced-motion` is respected.
10. **Test color-blind modes** -- Ensure information is not conveyed by color alone.

## Anti-Patterns to Avoid

1. **Relying solely on automated tools** -- Automated scans miss many issues.
2. **Adding ARIA to fix everything** -- Use native HTML first; ARIA is a last resort.
3. **Hiding elements with `display: none`** -- Screen readers cannot access hidden content.
4. **Using `tabindex` greater than 0** -- It disrupts natural tab order.
5. **Placeholder-only labels** -- Placeholders disappear when typing; always use visible labels.
6. **Auto-playing media** -- Auto-play with sound violates WCAG 1.4.2.
7. **Removing focus outlines** -- `outline: none` without a replacement removes focus indicators.
8. **Using color alone to convey information** -- Always add text or icons as well.
9. **Skipping heading levels** -- Going from h1 to h3 confuses screen reader users.
10. **Ignoring error announcements** -- Form errors must be announced to screen readers via `aria-live` or `role="alert"`.
