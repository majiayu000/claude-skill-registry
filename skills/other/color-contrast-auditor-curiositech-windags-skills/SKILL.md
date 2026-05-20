---
name: color-contrast-auditor
description: Detects and fixes color contrast violations using WCAG 2.1 guidelines and perceptual analysis. Expert in contrast ratio calculation, color blindness simulation, and providing accessible alternatives. Activate on "check contrast", "color accessibility", "WCAG audit", "readability check", "contrast ratio", "hard to read", "can't see text". NOT for general color theory (use color-theory-palette-harmony-expert), brand color selection (use web-design-expert), or non-visual accessibility (use ux-friction-analyzer).
allowed-tools: Read,Write,Edit,WebFetch,Glob,Grep
category: Design & Creative
tags:
  - accessibility
  - wcag
  - contrast
  - color
  - a11y
  - visual-design
pairs-with:
  - skill: web-design-expert
    reason: Implement accessible color fixes
  - skill: ux-friction-analyzer
    reason: Broader accessibility context
  - skill: design-system-creator
    reason: Build accessible design tokens
---

# Color Contrast Auditor

Detects color contrast violations that make text unreadable and provides WCAG-compliant fixes. Uses both mathematical contrast ratio analysis and perceptual evaluation via vision capabilities.

## When to Use

**Activate on:**
- Screenshots of websites/apps with suspected contrast issues
- CSS/Tailwind files for color audit
- "I can't read this" or "this is hard to see"
- Pre-launch accessibility checks
- Design system color validation

**NOT for:**
- Choosing brand colors (use `web-design-expert`)
- Color harmony/aesthetics (use `color-theory-palette-harmony-expert`)
- Non-visual accessibility (screen readers, keyboard nav)

---

## WCAG 2.1 Contrast Requirements

### Minimum Ratios (AA - Required)

| Text Type | Minimum Ratio | Example |
|-----------|---------------|---------|
| **Normal text** (&lt;24px, &lt;18.66px bold) | **4.5:1** | Body copy, labels, buttons |
| **Large text** (≥24px or ≥18.66px bold) | **3:1** | Headlines, hero text |
| **UI components** (borders, icons) | **3:1** | Form inputs, icons, focus rings |
| **Graphical objects** | **3:1** | Charts, infographics |

### Enhanced Ratios (AAA - Recommended)

| Text Type | Minimum Ratio |
|-----------|---------------|
| Normal text | **7:1** |
| Large text | **4.5:1** |

### Non-Text Elements

| Element | Requirement |
|---------|-------------|
| Focus indicators | 3:1 against adjacent colors |
| Form field borders | 3:1 against background |
| Icons conveying meaning | 3:1 against background |
| Disabled elements | No requirement (but consider UX) |

---

## Contrast Ratio Formula

```
Contrast Ratio = (L1 + 0.05) / (L2 + 0.05)

Where L1 = lighter color's relative luminance
      L2 = darker color's relative luminance
```

### Calculating Relative Luminance

```javascript
function relativeLuminance(r, g, b) {
  // Convert 0-255 to 0-1
  let [rs, gs, bs] = [r, g, b].map(c => c / 255);

  // Apply gamma correction
  const gamma = c => c <= 0.03928
    ? c / 12.92
    : Math.pow((c + 0.055) / 1.055, 2.4);

  const [R, G, B] = [rs, gs, bs].map(gamma);

  // Weighted sum (human eye sensitivity)
  return 0.2126 * R + 0.7152 * G + 0.0722 * B;
}

function contrastRatio(color1, color2) {
  const l1 = relativeLuminance(...color1);
  const l2 = relativeLuminance(...color2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}
```

---

## Common Failing Patterns

### 1. Light Text on Light Background

```
❌ FAILING EXAMPLE (from user screenshot):

┌─────────────────────────────────────────────┐
│  Background: #F5F2E8 (beige/cream)          │
│  Text: #C8FF00 (lime green)                 │
│                                             │
│     "Scan. Crawl. Match. Report."           │
│     ← UNREADABLE                            │
│                                             │
│  Calculated Ratio: ~1.5:1                   │
│  Required: 4.5:1 (normal) or 3:1 (large)    │
│  Verdict: FAIL by 3x                        │
└─────────────────────────────────────────────┘

✅ FIXED OPTIONS:
   • Darken text to #5A7300 → Ratio: 4.5:1
   • Darken background to #2A2A2A → Ratio: 12:1
   • Use dark green #1A4D00 → Ratio: 8:1
```

### 2. Gray Text Syndrome

```
❌ COMMON FAILURE:
   Background: #FFFFFF
   Text: #AAAAAA (light gray)
   Ratio: 2.3:1 ← FAIL

✅ FIXES:
   • Text: #767676 → Ratio: 4.5:1 (minimum AA)
   • Text: #595959 → Ratio: 7:1 (AAA)
```

### 3. Saturated Colors That Look Bright

```
❌ DECEPTIVE FAILURE:
   Background: #FFF8E7 (warm white)
   Text: #FF6B6B (coral/salmon)
   Ratio: 2.8:1 ← FAIL (looks "colorful" but fails)

✅ FIXES:
   • Text: #C62828 (darker red) → Ratio: 5.2:1
   • Text: #8B0000 (dark red) → Ratio: 8.1:1
```

### 4. Trendy Low-Contrast Aesthetic

```
❌ "MINIMALIST" FAILURE:
   Background: #FAFAFA
   Text: #E0E0E0
   Ratio: 1.3:1 ← SEVERELY FAILING

This is NOT minimalism. This is inaccessible.

✅ MINIMALIST + ACCESSIBLE:
   Background: #FAFAFA
   Text: #616161 → Ratio: 5.7:1
```

### 5. Placeholder Text Too Light

```
❌ COMMON FORM FAILURE:
   Input background: #FFFFFF
   Placeholder: #CCCCCC
   Ratio: 1.6:1 ← FAIL

✅ FIX:
   Placeholder: #757575 → Ratio: 4.6:1
```

### 6. Gradient Backgrounds

```
❌ VARIABLE CONTRAST:
   Gradient: #FFFFFF → #000080
   Text: #FFFFFF (fixed)

   Top of gradient: 1:1 (invisible!)
   Bottom of gradient: 8.6:1 (good)

✅ SOLUTIONS:
   • Add text shadow/outline
   • Use semi-transparent overlay behind text
   • Ensure ALL gradient stops pass contrast
```

---

## Audit Methodology

### Step 1: Visual Scan (Screenshot Analysis)

When given a screenshot, identify:

1. **Text elements by size:**
   - Headlines (large text → 3:1 required)
   - Body copy (normal text → 4.5:1 required)
   - UI labels (buttons, links → 4.5:1)
   - Captions/fine print (4.5:1 required)

2. **Interactive elements:**
   - Button borders/backgrounds
   - Form field borders
   - Focus states
   - Icons with meaning

3. **Red flags to look for:**
   - Light text on light backgrounds
   - Gray text on white
   - Colored text on colored backgrounds
   - Text over images without overlay

### Step 2: Extract Colors

From CSS/code:
```bash
# Find all color declarations
grep -E "(color:|background:|#[0-9a-fA-F]{3,8}|rgb|hsl)" styles.css
```

From Tailwind:
```bash
# Find text/bg color classes
grep -E "(text-|bg-)" *.tsx *.jsx
```

### Step 3: Calculate Ratios

For each text/background pair:
1. Convert colors to RGB
2. Calculate relative luminance
3. Compute contrast ratio
4. Compare to WCAG requirement

### Step 4: Generate Report

```markdown
# Contrast Audit Report

## Summary
- Total color pairs tested: X
- Passing (AA): Y
- Failing: Z
- Critical failures (&lt;2:1): N

## Failures by Severity

### Critical (Ratio &lt; 2:1)
| Location | Foreground | Background | Ratio | Required | Fix |
|----------|------------|------------|-------|----------|-----|
| Hero tagline | #C8FF00 | #F5F2E8 | 1.5:1 | 3:1 | #5A7300 |

### Moderate (Ratio 2:1 - 3:1)
...

### Minor (Ratio 3:1 - 4.5:1, normal text only)
...

## Recommended Fixes
[Specific color replacements with new ratios]
```

---

## Color Blindness Considerations

Contrast requirements help but don't fully address color blindness. Additional checks:

### Types to Consider

| Type | Affected | Consideration |
|------|----------|---------------|
| **Deuteranopia** | 6% of males | Red/green confusion |
| **Protanopia** | 2% of males | Red appears dark |
| **Tritanopia** | &lt;1% | Blue/yellow confusion |

### Best Practices

1. **Never rely on color alone** for meaning
   - Add icons, patterns, or text labels
   - Red/green for error/success needs icons too

2. **Test problematic pairs:**
   - Red + Green (stop/go)
   - Blue + Purple
   - Green + Brown
   - Light green + Yellow

3. **Use sufficient lightness difference**
   - Even with same hue, different lightness helps

---

## Quick Reference: Safe Color Pairs

### On White (#FFFFFF)

| Use Case | Color | Hex | Ratio |
|----------|-------|-----|-------|
| Body text | Dark gray | #333333 | 12.6:1 |
| Secondary text | Medium gray | #767676 | 4.5:1 |
| Links | Blue | #0066CC | 5.3:1 |
| Success | Green | #2E7D32 | 5.1:1 |
| Error | Red | #C62828 | 6.0:1 |
| Warning | Orange-brown | #E65100 | 4.5:1 |

### On Black (#000000)

| Use Case | Color | Hex | Ratio |
|----------|-------|-----|-------|
| Body text | Light gray | #E0E0E0 | 13.4:1 |
| Secondary | Medium gray | #9E9E9E | 6.3:1 |
| Accent | Light blue | #90CAF9 | 7.3:1 |

### On Dark Gray (#1A1A1A)

| Use Case | Color | Hex | Ratio |
|----------|-------|-----|-------|
| Body text | Off-white | #F5F5F5 | 14.1:1 |
| Secondary | Light gray | #BDBDBD | 8.3:1 |

---

## Tools & Validation

### Online Checkers
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Coolors Contrast Checker](https://coolors.co/contrast-checker)
- [Adobe Color Accessibility](https://color.adobe.com/create/color-accessibility)

### Browser DevTools
```javascript
// Chrome DevTools: Elements → Styles → hover color swatch
// Shows contrast ratio automatically

// Firefox: Accessibility Inspector
// Shows color contrast issues
```

### Automated Testing
```javascript
// axe-core (popular a11y testing library)
const axe = require('axe-core');
axe.run(document, { rules: ['color-contrast'] });

// Lighthouse (built into Chrome)
// Performance → Accessibility → Color contrast
```

### CLI Tools
```bash
# Lighthouse CLI
npx lighthouse https://example.com --only-categories=accessibility

# Pa11y
npx pa11y https://example.com
```

---

## Integration with This Skill

When analyzing a screenshot or codebase:

1. **I will identify** all text/background color pairs
2. **I will calculate** contrast ratios for each
3. **I will flag** anything below WCAG AA thresholds
4. **I will suggest** specific hex values that pass
5. **I will provide** before/after comparisons

For the example screenshot (lime on beige):
```
AUDIT RESULT: CRITICAL FAILURE

Element: Hero tagline "Scan. Crawl. Match. Report."
Foreground: ~#C8FF00 (lime green)
Background: ~#F5F2E8 (beige)
Calculated Ratio: ~1.5:1
Required (large text): 3:1
Required (normal text): 4.5:1
Status: ❌ FAILS BY 2-3x

RECOMMENDED FIXES:
1. Darken text to #5A7300 (olive) → 4.8:1 ✓
2. Darken text to #3D5C00 (dark olive) → 7.1:1 ✓✓
3. Keep lime, darken BG to #3D3D3D → 8.2:1 ✓✓
4. Use #1B5E20 (dark green) → 8.4:1 ✓✓
```

---

## Checklist for New Designs

Before shipping:

- [ ] All body text has ≥4.5:1 contrast
- [ ] All large text has ≥3:1 contrast
- [ ] All form borders have ≥3:1 contrast
- [ ] All icons conveying meaning have ≥3:1 contrast
- [ ] Placeholder text is readable (≥4.5:1)
- [ ] Focus states are clearly visible (≥3:1)
- [ ] Links are distinguishable without color alone
- [ ] Error/success states use icons, not just color
- [ ] Tested with color blindness simulators
- [ ] Automated accessibility scan passes

---

**Philosophy:** Beautiful design and accessibility are not mutually exclusive. High contrast can be striking, dramatic, and intentional. Low contrast isn't "minimalist"—it's exclusionary. Every unreadable word is a user lost.
