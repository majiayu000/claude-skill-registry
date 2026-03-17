---
name: accessibility
description: WCAG 2.2 compliance audit — keyboard navigation, screen reader testing, ARIA, color contrast
triggers: [a11y, accessibility, WCAG, keyboard nav, screen reader, aria, color contrast, tab order]
context_cost: medium
---

# Accessibility Skill

## Goal
Ensure UI features meet WCAG 2.2 Level AA requirements through automated scanning and manual verification. Produce an actionable report with specific violations and fixes.

## Steps

1. **Run automated accessibility scan**
   ```bash
   # axe-core with Playwright (recommended)
   npx playwright test --config=playwright.a11y.config.ts

   # Pa11y for batch URL testing
   npx pa11y http://localhost:3000 --standard WCAG2AA

   # Lighthouse accessibility audit
   npx lighthouse http://localhost:3000 --only-categories=accessibility --output=json
   ```

   **Playwright + axe-core test:**
   ```typescript
   import { test, expect } from '@playwright/test';
   import { checkA11y, injectAxe } from 'axe-playwright';

   test('home page has no accessibility violations', async ({ page }) => {
     await page.goto('/');
     await injectAxe(page);
     await checkA11y(page, null, {
       axeOptions: { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag22aa'] } }
     });
   });
   ```

2. **Keyboard navigation check**
   - Tab through all interactive elements — logical focus order?
   - All interactive elements reachable by keyboard (no mouse-only interactions)?
   - Focus is always visible (not removed with `outline: none` without replacement)?
   - Modal dialogs trap focus correctly (Tab/Shift+Tab stays inside modal)?
   - Escape key dismisses modals and popups?
   - Skip navigation link available to bypass repeated navigation?

   ```typescript
   test('can navigate form fields with keyboard', async ({ page }) => {
     await page.goto('/contact');
     await page.keyboard.press('Tab'); // First field
     await expect(page.locator(':focus')).toHaveAttribute('name', 'name');
     await page.keyboard.press('Tab'); // Second field
     await expect(page.locator(':focus')).toHaveAttribute('name', 'email');
   });
   ```

3. **Screen reader compatibility check**
   - All images have descriptive `alt` text (or `alt=""` for decorative images)
   - Form inputs have associated `<label>` elements (not just placeholder)
   - Error messages linked to inputs via `aria-describedby`
   - ARIA roles are used correctly (no `role="button"` on non-interactive elements)
   - Dynamic content changes announced via `aria-live` regions
   - Headings form a logical hierarchy (H1 → H2 → H3, no skipped levels)

   **Common issues to check:**
   ```html
   <!-- BAD: no label for input -->
   <input type="email" placeholder="Enter email">

   <!-- GOOD: associated label -->
   <label for="email">Email address</label>
   <input id="email" type="email" aria-describedby="email-error">
   <span id="email-error" role="alert">Please enter a valid email</span>
   ```

4. **Color contrast check**
   - Normal text: minimum contrast ratio 4.5:1 (WCAG AA)
   - Large text (18pt+): minimum contrast ratio 3:1
   - UI components and graphical objects: minimum 3:1
   ```bash
   # Check specific color combination
   # Use: https://webaim.org/resources/contrastchecker/ or automated axe-core
   ```

5. **Check WCAG 2.2 specific criteria**
   - **2.5.3 Target Size (Minimum):** Interactive targets at least 24×24 CSS pixels
   - **3.3.7 Redundant Entry:** Don't ask users to re-enter info they've already provided
   - **3.3.8 Accessible Authentication:** No cognitive function test required (CAPTCHAs must have alternative)

6. **Produce accessibility report**
   ```markdown
   ## Accessibility Audit Report
   Standard: WCAG 2.2 Level AA
   Date: [date]
   Pages audited: [list]

   ### Critical Violations (WCAG failures — must fix)
   - [ERROR] img elements missing alt text: src/components/ProductCard.tsx:15
   - [ERROR] Form input has no associated label: src/components/ContactForm.tsx:32

   ### Keyboard Navigation Issues
   - [WARNING] Focus not visible on custom button component
   - [INFO] Tab order could be improved on checkout form

   ### Screen Reader Issues
   - [WARNING] Carousel updates not announced (missing aria-live)

   ### Color Contrast
   - [ERROR] #777 on #fff fails 4.5:1 ratio (actual: 4.48:1) — src/styles/typography.css:23

   ### Passed Checks
   - All form inputs have associated labels (except noted above)
   - Heading hierarchy is logical throughout
   - Skip navigation link present

   ### Overall: LEVEL AA NOT MET
   Blocking: [N] critical violations
   ```

## Constraints
- Critical WCAG violations are blocking for public-facing applications
- Accessibility testing must use real browser (Playwright headless chromium, not jsdom)
- Don't mark complete without keyboard navigation test AND automated scan
- Color contrast must be checked at all relevant breakpoints

## Output Format
Accessibility audit report + list of violations with file:line references + recommended fixes.
