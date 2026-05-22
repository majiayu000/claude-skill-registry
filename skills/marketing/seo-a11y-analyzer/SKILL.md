---
name: seo-a11y-analyzer
description: Analyzes HTML/JSX/TSX files for SEO and accessibility issues including WCAG 2.1 AA compliance, color contrast (4.5:1), heading hierarchy, meta tags, image alt text, and ARIA attributes. Use when checking web pages for SEO, accessibility, WCAG compliance, or when user mentions "a11y", "contrast", "alt text", "meta tags", "heading structure", or "accessibility audit".
---

# SEO & Accessibility Analyzer

Analyzes HTML/JSX/TSX files for SEO issues and WCAG 2.1 AA compliance.

## Quick Start

Copy this workflow checklist and track progress:

```
Analysis Progress:
- [ ] Step 1: Read target file
- [ ] Step 2: Run quick checks (P0 critical issues)
- [ ] Step 3: Run detailed checks (all issues)
- [ ] Step 4: Validate with axe-core CLI
- [ ] Step 5: Generate report with fixes
```

## Step 1: Read Target File

Read the HTML/JSX/TSX file using the Read tool.

Identify file type:
- `.html` - Standard HTML
- `.jsx` / `.tsx` - React components (check className instead of class)

## Step 2: Quick Checks (P0 Critical Issues)

Check these **immediately** - they block compliance:

### 1. Title Tag (WCAG 2.4.2)
```html
<!-- Required -->
<title>Descriptive Page Title - Site Name</title>
```
- Must exist and be non-empty
- Recommended length: 50-60 characters
- Should be unique per page

### 2. Meta Description (SEO)
```html
<!-- Required -->
<meta name="description" content="Concise page description...">
```
- Must exist
- Recommended length: 150-160 characters

### 3. H1 Uniqueness (WCAG 2.4.6)
- Exactly **one** `<h1>` per page
- Must be descriptive and unique

### 4. Heading Hierarchy
- No skipped levels (h1 → h3 without h2)
- Logical nesting structure

### 5. Image Alt Text (WCAG 1.1.1)
```html
<!-- Informative image -->
<img src="photo.jpg" alt="Team members at annual retreat">

<!-- Decorative image -->
<img src="decoration.png" alt="">
```
- All `<img>` must have `alt` attribute
- Decorative images: `alt=""`
- Informative images: descriptive text (not filename)

### 6. Color Contrast (WCAG 1.4.3)
- Normal text: **4.5:1** minimum
- Large text (18pt / 14pt bold+): **3:1** minimum
- See [reference/color-contrast.md](reference/color-contrast.md) for common color combinations

**If any P0 issue found, report immediately with location and fix.**

## Step 3: Detailed Checks

### SEO Checks
See [reference/seo-checks.md](reference/seo-checks.md) for complete list (30 items).

Key items:
- Canonical URL: `<link rel="canonical" href="...">`
- Open Graph tags: `<meta property="og:title">`, `og:description`, `og:image`
- Twitter Cards: `<meta name="twitter:card">`, `twitter:title`
- Structured data: `<script type="application/ld+json">`
- Mobile viewport: `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Language attribute: `<html lang="en">`

### WCAG Checks
See [reference/wcag-quick-ref.md](reference/wcag-quick-ref.md) for criteria reference.

Key items:
- Form labels: All inputs must have associated `<label>` or `aria-label`
- Link text: Avoid "click here", use descriptive text
- Focus indicators: Ensure `:focus` styles are visible
- Keyboard navigation: All interactive elements must be keyboard accessible

### ARIA Checks
- Valid roles only (no custom roles like `role="hamburger"`)
- Required attributes present (slider needs `aria-valuenow`, `aria-valuemin`, `aria-valuemax`)
- No `aria-hidden="true"` on focusable elements
- No redundant roles on native elements (`<button role="button">`)

## Step 4: Validate with axe-core CLI

**Required**: Run axe-core for automated WCAG validation.

```bash
npx @axe-core/cli file.html --tags wcag21aa
```

Or use the provided script:
```bash
bash scripts/validate-with-axe.sh path/to/file.html
```

### Interpret Results

| Severity | Action |
|----------|--------|
| critical | Must fix - blocks compliance |
| serious | Should fix - affects many users |
| moderate | Nice to fix - best practice |
| minor | Consider fixing |

**Goal**: Zero critical and serious issues.

## Step 5: Generate Report

Use this exact format:

```markdown
# Accessibility & SEO Report: [filename]

## Summary
- Critical: [count]
- Serious: [count]
- Warnings: [count]
- Info: [count]

## Critical Issues (P0)

### 1. [Issue Title] - [WCAG X.X.X or SEO]

**Problem**: [specific description]

**Location**: Line [number] or `[CSS selector]`

**Current code**:
```html
[problematic code]
```

**Fixed code**:
```html
[corrected code]
```

**Why this matters**: [brief explanation]

## Serious Issues

[Same format as above]

## Warnings

[Same format as above]

## Passed Checks

- [list of successful checks]
```

## Validation Loop

For complex fixes, follow this pattern:

1. Apply fix
2. Re-run axe-core validation
3. If issues remain → refine fix, return to step 1
4. **Only proceed when validation passes**

```
Validation Loop:
- [ ] Applied fix for [issue]
- [ ] Re-ran axe-core
- [ ] Confirmed resolution
```

## Common Fix Patterns

### Missing Title
```html
<!-- Before -->
<head>
  <meta charset="UTF-8">
</head>

<!-- After -->
<head>
  <meta charset="UTF-8">
  <title>Page Title - Site Name</title>
</head>
```

### Missing Alt Text
```html
<!-- Before -->
<img src="product.jpg">

<!-- After -->
<img src="product.jpg" alt="Blue wireless headphones with noise cancellation">
```

### Low Contrast Text
```css
/* Before: #999 on #fff = 2.85:1 */
.text { color: #999999; }

/* After: #767676 on #fff = 4.54:1 */
.text { color: #767676; }
```

### Missing Form Label
```html
<!-- Before -->
<input type="email" placeholder="Email">

<!-- After -->
<label for="email">Email address</label>
<input type="email" id="email" placeholder="Email">
```

## JSX/TSX Specifics

When analyzing React files:
- Check `className` instead of `class`
- Verify `htmlFor` instead of `for` on labels
- Check for `key` props in lists (not accessibility, but important)
- Look for accessible component patterns in design system usage

## Examples

See [reference/examples.md](reference/examples.md) for:
- Complete page audit example
- React component audit example
- Before/after fix comparisons

## When NOT to Use This Skill

- URL-based testing (use axe-core CLI directly on served pages)
- Dynamic content analysis (requires browser rendering)
- Complex SPA testing (use Lighthouse or Playwright)
- PDF accessibility (different tooling required)

## References

- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [axe-core Rules](https://dequeuniversity.com/rules/axe/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
