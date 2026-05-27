---
name: brightness-system
description: 8-mode brightness system implementation with CSS custom properties. Use when implementing theme switching, color tokens, or fixing brightness-related issues.
---

# Brightness System Skill

## Overview

The omer-akben portfolio implements an 8-mode brightness system that must be tested and supported for all UI changes. This skill covers implementation patterns, testing requirements, and troubleshooting.

## 8 Brightness Modes

**Modes:** `-3` (darkest) → `0` (baseline) → `+3` (brightest) + `auto`

### Implementation

- `data-brightness` attribute on `<html>` element
- CSS custom properties in `globals.css`
- State management in `lib/brightness-context.tsx`

## CSS Custom Properties (MANDATORY)

### Color Tokens

✅ **ALWAYS USE:**

```css
/* Surfaces */
bg-surf-0    /* Primary background */
bg-surf-1    /* Secondary background */
bg-surf-2    /* Tertiary background */

/* Text */
text-text-1  /* Primary text */
text-text-2  /* Secondary text */
text-text-3  /* Tertiary text */

/* Brand */
bg-brand-primary    /* Brand accent color */
bg-brand-secondary  /* Secondary brand color */

/* Borders */
border-border-line  /* Border color */
```typescript

❌ **NEVER USE:**

- Hardcoded hex colors: `#00FFC6`, `#1a1a1a`
- Inline color values: `bg-[#00FFC6]`
- Direct Tailwind colors without tokens

### Example Implementation

```tsx
// ✅ CORRECT
<div className="bg-surf-1 text-text-1 border-border-line">
  <button className="bg-brand-primary hover:bg-brand-secondary">
    Click me
  </button>
</div>

// ❌ WRONG
<div className="bg-[#1a1a1a] text-white border-gray-800">
  <button className="bg-[#00FFC6] hover:bg-emerald-400">
    Click me
  </button>
</div>
```typescript

## Implementation Patterns

### Setting Brightness Mode

```typescript
import { useBrightness } from "@/lib/brightness-context";

function BrightnessControl() {
  const { brightness, setBrightness } = useBrightness();

  return (
    <select
      value={brightness}
      onChange={(e) => setBrightness(e.target.value as BrightnessMode)}
    >
      <option value="-3">Darkest (-3)</option>
      <option value="-2">Darker (-2)</option>
      <option value="-1">Dark (-1)</option>
      <option value="0">Baseline (0)</option>
      <option value="1">Light (+1)</option>
      <option value="2">Lighter (+2)</option>
      <option value="3">Lightest (+3)</option>
      <option value="auto">Auto</option>
    </select>
  );
}
```typescript

### Brightness Context Provider

Location: `src/lib/brightness-context.tsx`

```typescript
export type BrightnessMode = "-3" | "-2" | "-1" | "0" | "1" | "2" | "3" | "auto";

interface BrightnessContextType {
  brightness: BrightnessMode;
  setBrightness: (mode: BrightnessMode) => void;
}
```typescript

### HTML Attribute

The brightness mode is set on the root HTML element:

```html
<html data-brightness="0">
  <!-- content -->
</html>
```typescript

CSS custom properties respond to this attribute:

```css
[data-brightness="0"] {
  --color-surf-0: #0a0a0a;
  --color-text-1: #ffffff;
}

[data-brightness="3"] {
  --color-surf-0: #f5f5f5;
  --color-text-1: #0a0a0a;
}
```typescript

## Testing Requirements

### ⚠️ CRITICAL: Test All 8 Modes

**Every UI change MUST be tested in all 8 brightness modes.**

### Manual Testing

1. Open DevTools (F12)
2. Find `<html>` element in Elements tab
3. Modify `data-brightness` attribute manually
4. Test each mode: `-3`, `-2`, `-1`, `0`, `1`, `2`, `3`, `auto`
5. Verify:
   - Text is readable
   - Contrast is sufficient
   - Colors follow design tokens
   - No hardcoded colors appear

### Unit Test Pattern

```typescript
import { render } from "@testing-library/react";

describe("Component brightness modes", () => {
  const modes = ["-3", "-2", "-1", "0", "1", "2", "3", "auto"];

  modes.forEach((mode) => {
    it(`should render correctly in brightness mode ${mode}`, () => {
      // Set mode on root
      document.documentElement.setAttribute("data-brightness", mode);

      render(<YourComponent />);

      // Assert appearance
      const element = screen.getByRole("button");
      expect(element).toHaveClass("bg-brand-primary");
      expect(element).not.toHaveClass("bg-[#00FFC6]");
    });
  });
});
```typescript

### E2E Test Pattern

```typescript
import { test, expect } from "@playwright/test";

test.describe("Brightness modes", () => {
  const modes = ["-3", "-2", "-1", "0", "1", "2", "3", "auto"];

  modes.forEach((mode) => {
    test(`should display correctly in mode ${mode}`, async ({ page }) => {
      await page.goto("/");

      // Set brightness mode
      await page.evaluate((m) => {
        document.documentElement.setAttribute("data-brightness", m);
      }, mode);

      // Wait for CSS to apply
      await page.waitForTimeout(100);

      // Take screenshot for visual comparison
      await expect(page).toHaveScreenshot(`brightness-${mode}.png`);
    });
  });
});
```typescript

## Common Issues & Solutions

### Issue: Hardcoded Colors Appear

**Symptoms:** Colors don't change with brightness mode

### Solution

1. Search codebase for hex colors: `#[0-9a-fA-F]{3,6}`
2. Replace with CSS custom properties
3. Verify with `grep -r "#[0-9a-fA-F]" src/`

### Issue: Insufficient Contrast

**Symptoms:** Text hard to read in certain modes

### Solution

1. Review color token values in `globals.css`
2. Adjust contrast ratios (minimum 4.5:1 for normal text)
3. Test with browser DevTools contrast checker

### Issue: Component Not Responding to Mode Changes

**Symptoms:** Component colors stay the same

### Solution

1. Verify component uses CSS custom properties
2. Check if component has inline styles (remove them)
3. Ensure parent elements don't override tokens

## Design Token Reference

Complete list of available tokens in `src/app/globals.css`:

```css
/* Surface Colors */
--color-surf-0: /* Primary surface */
--color-surf-1: /* Secondary surface */
--color-surf-2: /* Tertiary surface */

/* Text Colors */
--color-text-1: /* Primary text */
--color-text-2: /* Secondary text */
--color-text-3: /* Tertiary text */

/* Brand Colors */
--color-brand-primary: /* Primary brand (emerald) */
--color-brand-secondary: /* Secondary brand */

/* Border Colors */
--color-border-line: /* Default border */

/* Functional Colors */
--color-error: /* Error state */
--color-success: /* Success state */
--color-warning: /* Warning state */
```typescript

## Checklist for New Components

When creating a new component:

- [ ] Use only CSS custom properties for colors
- [ ] No hardcoded hex colors or Tailwind color classes
- [ ] Test component in all 8 brightness modes
- [ ] Verify contrast ratios meet WCAG AA (4.5:1)
- [ ] Check hover states in all modes
- [ ] Verify focus indicators are visible in all modes
- [ ] Test with auto mode (respects system preference)

## Auto Mode Behavior

When `brightness="auto"`:

- Respects user's system preference (light/dark)
- Uses `prefers-color-scheme` media query
- Maps to mode `0` (dark) or mode `2` (light) by default

```css
[data-brightness="auto"] {
  @media (prefers-color-scheme: dark) {
    /* Use dark mode tokens */
  }

  @media (prefers-color-scheme: light) {
    /* Use light mode tokens */
  }
}
```typescript

## Performance Considerations

- CSS custom properties are performant (no runtime calculation)
- Mode changes only update root attribute (no re-renders)
- Tailwind processes tokens at build time
- No JavaScript needed for color computation

## Related Files

- `src/lib/brightness-context.tsx` - Context provider and hooks
- `src/app/globals.css` - Color token definitions
- `src/components/brightness-toggle.tsx` - UI control (if exists)

## Quick Reference

```bash
# Find hardcoded colors in codebase
grep -r "#[0-9a-fA-F]" src/

# Test brightness modes in browser DevTools
document.documentElement.setAttribute("data-brightness", "3")

# Check component uses correct tokens
// Should see: bg-surf-1, text-text-1, border-border-line
// Should NOT see: bg-[#xxx], text-white, border-gray-800
```typescript
