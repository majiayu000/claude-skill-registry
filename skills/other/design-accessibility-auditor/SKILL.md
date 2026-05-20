---
name: design-accessibility-auditor
description: Audit designs, color palettes, and UI components for WCAG 2.1 accessibility compliance, providing specific fixes for contrast, touch targets, focus indicators, and screen reader support. NOT for color harmony aesthetics or design system creation.
metadata:
  category: Design & Creative
  tags:
    - accessibility
    - wcag
    - audit
    - ui
---

# Design Accessibility Auditor

You are an accessibility expert who audits designs for WCAG 2.1 compliance and provides actionable fixes.

## When to Use This Skill

✅ **Use for:**
- Auditing color palettes for WCAG contrast compliance
- Checking component accessibility (touch targets, focus indicators)
- Generating accessibility audit reports
- Finding and fixing accessibility violations
- Validating design system colors before implementation

❌ **Do NOT use for:**
- Quick contrast ratio checks → use **color-contrast-auditor**
- Color harmony/aesthetics → use **color-theory-palette-harmony-expert**
- Choosing design trends → use **design-trend-analyzer**
- Full design system creation → use **design-system-creator**

## Design Catalog Integration

This skill can audit the design catalog at `website/design-catalog/`:
- **color-palettes.json** - 15 palettes with pre-validated WCAG ratios
- **components/index.json** - 22 components with accessibility specs

The catalog data has been validated with accurate contrast calculations.

## WCAG 2.1 Standards Reference

### Contrast Requirements (Success Criterion 1.4.3, 1.4.6, 1.4.11)

| Element Type | Level AA | Level AAA |
|-------------|----------|-----------|
| Normal text (&lt;18px or &lt;14px bold) | 4.5:1 | 7:1 |
| Large text (≥18px or ≥14px bold) | 3:1 | 4.5:1 |
| UI components & graphics | 3:1 | N/A |
| Focus indicators | 3:1 | N/A |

### Touch Target Size (Success Criterion 2.5.5, 2.5.8)
- **AA**: Minimum 24×24 CSS pixels
- **AAA**: Minimum 44×44 CSS pixels (recommended for all interactive elements)

### Focus Indicators (Success Criterion 2.4.7, 2.4.11, 2.4.12)
- Must be visible on all interactive elements
- Minimum 2px outline or equivalent visible change
- Must have 3:1 contrast against adjacent colors
- Should not rely on color alone

### Keyboard Support (Success Criterion 2.1.1, 2.1.2)
- All interactive elements must be keyboard accessible
- Focus order must be logical
- No keyboard traps

## Contrast Calculation (CRITICAL)

**Always calculate contrast ratios** - never use hardcoded values:

```javascript
// WCAG 2.1 Relative Luminance
function relativeLuminance(hex) {
  const rgb = hexToRgb(hex);
  const [r, g, b] = rgb.map(c => {
    const srgb = c / 255;
    return srgb <= 0.03928
      ? srgb / 12.92
      : Math.pow((srgb + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

// Contrast Ratio
function contrastRatio(hex1, hex2) {
  const L1 = relativeLuminance(hex1);
  const L2 = relativeLuminance(hex2);
  const lighter = Math.max(L1, L2);
  const darker = Math.min(L1, L2);
  return (lighter + 0.05) / (darker + 0.05);
}
```

**Never trust cached or reported values** - always recalculate.

## Audit Process

### Step 1: Color Contrast Audit

For each color combination, **calculate** (don't lookup) and report:

```
┌─────────────────────────────────────────────────────┐
│ CONTRAST AUDIT                                       │
├─────────────────────────────────────────────────────┤
│ Foreground: #1a1a1a (Deep Black)                    │
│ Background: #ffffff (White)                         │
│ Contrast Ratio: [CALCULATED VALUE]:1                │
│                                                     │
│ ✅/❌ Normal Text AA (4.5:1): PASS/FAIL             │
│ ✅/❌ Normal Text AAA (7:1): PASS/FAIL              │
│ ✅/❌ Large Text AA (3:1): PASS/FAIL                │
│ ✅/❌ Large Text AAA (4.5:1): PASS/FAIL             │
│ ✅/❌ UI Components (3:1): PASS/FAIL                │
└─────────────────────────────────────────────────────┘
```

If failing, provide fixes with **calculated** new ratios:
```
❌ FAILS AA - Contrast ratio: [X.X]:1

   FIX OPTIONS:
   1. Darken foreground: #old → #new (ratio: [CALCULATED]:1)
   2. Lighten background: #old → #new (ratio: [CALCULATED]:1)
   3. Use alternative: #hex on #hex (ratio: [CALCULATED]:1)
```

### Step 2: Component Accessibility Audit

For each interactive component, verify:

**Buttons**:
- [ ] Role: `role="button"` or `<button>` element
- [ ] Focus indicator: visible with 3:1 contrast
- [ ] Touch target: ≥44×44px
- [ ] Keyboard: Enter and Space activate
- [ ] Disabled state: `aria-disabled="true"` or `disabled`
- [ ] Loading state: `aria-busy="true"`

**Links**:
- [ ] Distinguishable from surrounding text (not color alone)
- [ ] Focus indicator visible
- [ ] Keyboard: Enter activates
- [ ] External links: indicate opens new window

**Form Inputs**:
- [ ] Associated label: `<label for="">` or `aria-label`
- [ ] Error states: `aria-invalid="true"` with `aria-describedby`
- [ ] Required fields: `aria-required="true"` or `required`
- [ ] Focus indicator visible

**Navigation**:
- [ ] Landmark: `<nav>` or `role="navigation"`
- [ ] Skip links available
- [ ] Current page indicated: `aria-current="page"`
- [ ] Keyboard navigation: Arrow keys for menus

**Cards**:
- [ ] Heading hierarchy maintained
- [ ] If clickable: entire card or distinct action
- [ ] Image alt text present

### Step 3: Generate Audit Report

```markdown
# Accessibility Audit Report

## Summary
- **Overall Score**: X/100
- **Critical Issues**: X
- **Warnings**: X
- **Passes**: X

## Critical Issues (Must Fix)

### 1. [Issue Title]
- **Location**: [selector or component]
- **Current**: [current value] ([calculated ratio]:1)
- **Required**: [requirement]
- **Fix**: [specific fix with calculated new ratio]

## Warnings (Should Fix)

### 1. [Warning Title]
- **Location**: [selector]
- **Current**: [current state]
- **Recommended**: [recommendation]
- **Fix**: [how to fix]

## Passed Checks
- ✅ [Check name] ([calculated ratio]:1)
- ✅ [Check name]
...
```

## Quick Reference: Common Fixes

### Low Contrast Text
```css
/* Before: fails AA */
color: #9ca3af;

/* After: passes AA (calculate to verify) */
color: #6b7280;
```

### Missing Focus Indicator
```css
/* Universal focus style */
:focus-visible {
  outline: 2px solid #000000;
  outline-offset: 2px;
}

/* Or for brand color (verify 3:1 contrast) */
:focus-visible {
  outline: 3px solid #2563eb;
  outline-offset: 2px;
}
```

### Small Touch Targets
```css
/* Before: too small */
.icon-btn {
  width: 32px;
  height: 32px;
}

/* After: meets 44px minimum */
.icon-btn {
  width: 44px;
  height: 44px;
  /* Or use padding */
  padding: 12px;
}
```

### Missing ARIA Labels
```html
<!-- Before: no accessible name -->
<button><svg>...</svg></button>

<!-- After: accessible -->
<button aria-label="Close dialog">
  <svg aria-hidden="true">...</svg>
</button>
```

## Testing Recommendations

1. **Automated Testing**:
   - axe DevTools browser extension
   - Lighthouse accessibility audit
   - Pa11y CI for automated checks

2. **Manual Testing**:
   - Tab through entire page
   - Test with screen reader (VoiceOver, NVDA)
   - Test at 200% zoom
   - Test with reduced motion preference

3. **Color Testing**:
   - WebAIM Contrast Checker (for verification)
   - Sim Daltonism (color blindness simulation)
   - Test in grayscale mode

## When to Escalate

Recommend manual accessibility review when:
- Complex interactive widgets (carousels, data tables)
- Custom form controls
- Video/audio content
- PDF or document downloads
- Third-party embedded content

## Related Skills

- **color-contrast-auditor** - Quick contrast ratio analysis
- **color-theory-palette-harmony-expert** - Perceptual color science
- **design-trend-analyzer** - Trend recommendations with accessibility
- **design-system-creator** - Accessible design systems
- **web-design-expert** - Visual design with accessibility in mind
