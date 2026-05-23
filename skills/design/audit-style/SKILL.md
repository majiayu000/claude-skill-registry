---
name: audit-style
description: Audit and refactor CSS to comply with Game Loopers design system and BEM methodology
---

# Game Loopers CSS BEM Audit & Refactor Skill

## Skill Name
**css-bem-auditor**

## Purpose
Audit, normalize, and refactor CSS across the Game Loopers application to comply with the project's **BEM (Block–Element–Modifier)** methodology and design system, ensuring maintainability, consistency, and scalability.

This skill identifies non-compliant selectors, design token violations, naming collisions, overly-specific rules, and architectural inconsistencies, then proposes or applies BEM-aligned fixes specific to Game Loopers.

**Critical**: This project uses **strict BEM with NO utility-first CSS** (no Tailwind, no inline utilities). All styles must use component-scoped CSS with BEM naming.

---

## Scope
This skill operates on:
- Astro component styles (`.astro` files with `<style>` blocks)
- SolidJS component stylesheets (`.tsx` files with co-located `.css` files)
- Global stylesheets (`/src/styles/global.css`)
- Component-specific CSS files (e.g., `product-files-form.css`)

It does **not** redesign UI or change visual intent unless explicitly requested.

---

## Design System Reference

Game Loopers has a comprehensive design system defined in `DESIGN_SYSTEM.md` (co-located in this directory). All CSS must comply with:

### Color System (CSS Custom Properties)

**Semantic Colors**:
```css
--primary                 /* Black in light mode */
--primary-foreground      /* White text on primary */
--secondary               /* Light gray */
--secondary-foreground
--destructive             /* Red for errors/delete */
--destructive-foreground
--accent                  /* Highlights, hover states */
--accent-foreground
--background              /* Page background */
--foreground              /* Primary text */
--card                    /* Card backgrounds */
--card-foreground
--muted                   /* Low emphasis backgrounds */
--muted-foreground        /* Secondary text */
--border                  /* Default borders */
--input                   /* Input borders */
--ring                    /* Focus ring color */
```

**Status Colors**:
```css
--color-success           /* Green - confirmations */
--color-success-foreground
--color-warning           /* Yellow - cautions */
--color-warning-foreground
--color-error             /* Red - failures */
--color-error-foreground
--color-info              /* Blue - notifications */
--color-info-foreground
```

### Typography Scale
```css
--text-xs: 0.75rem;       /* 12px */
--text-sm: 0.875rem;      /* 14px */
--text-base: 1rem;        /* 16px */
--text-lg: 1.125rem;      /* 18px */
--text-xl: 1.25rem;       /* 20px */
--text-2xl: 1.5rem;       /* 24px */
--text-3xl: 1.875rem;     /* 30px */
--text-4xl: 2.25rem;      /* 36px */
--text-5xl: 3rem;         /* 48px */

--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;

--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
```

### Spacing Scale (8px Grid)
```css
--spacing-xs: 0.25rem;    /* 4px */
--spacing-sm: 0.5rem;     /* 8px */
--spacing-md: 1rem;       /* 16px */
--spacing-lg: 1.5rem;     /* 24px */
--spacing-xl: 2rem;       /* 32px */
--spacing-2xl: 3rem;      /* 48px */
--spacing-3xl: 4rem;      /* 64px */
--spacing-4xl: 6rem;      /* 96px */

--gap-xs: 0.25rem;
--gap-sm: 0.5rem;
--gap-md: 1rem;
--gap-lg: 1.5rem;
--gap-xl: 2rem;
--gap-2xl: 3rem;
```

### Border Radius
```css
--radius-sm: 0.125rem;    /* 2px */
--radius-md: 0.375rem;    /* 6px */
--radius-lg: 0.5rem;      /* 8px */
--radius-xl: 0.75rem;     /* 12px */
--radius-2xl: 1rem;       /* 16px */
--radius-full: 9999px;    /* Fully rounded */
```

### Shadows
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
```

---

## BEM Rules Enforced

### Naming Convention
```css
.block {}
.block__element {}
.block--modifier {}
.block__element--modifier {}
```

**Block Naming**:
- Lowercase only
- Hyphens for word separation (e.g., `.product-card`, `.browse-cta`)
- Describes component purpose

**Element Naming**:
- Double underscore (`__`) separates block from element
- Lowercase with hyphens (e.g., `.button__text`, `.card__header`)

**Modifier Naming**:
- Double hyphen (`--`) separates block/element from modifier
- Lowercase with hyphens (e.g., `.button--primary`, `.card--elevated`)

### Existing BEM Blocks (Reference)

**Core Components**:
- `.button` (Button.astro)
- `.card` (Card.astro)
- `.page-header` (PageHeader.astro)
- `.navigation` (Navigation.astro)
- `.browse-cta` (BrowseCTA.astro)

**Browse Components** (global.css):
- `.browse-search`
- `.browse-tags`
- `.browse-grid`
- `.browse-card`
- `.browse-empty`
- `.browse-pagination`

**Product Components**:
- `.product-chat`
- `.add-to-cart`
- `.add-to-cart-modal`
- `.product-documents-form`
- `.document-list`
- `.product-contributors`
- `.price-breakdown`
- `.status-editor`
- `.status-badge`
- `.revenue-preview`
- `.royalty-breakdown`
- `.product-files-form`
- `.product-royalty-breakdown`
- `.product-status-editor`
- `.product-embeddable-toggle`
- `.product-embedded-products`

**Document Components**:
- `.document-chat`

**Interactive Components**:
- `.confirm-dialog`
- `.modal-overlay`, `.modal-content`, `.modal-header`, `.modal-body`

### Prohibited Patterns

❌ **Strictly Forbidden**:
```css
/* NO Tailwind-style utilities */
.flex { display: flex; }
.text-center { text-align: center; }
.mt-4 { margin-top: 1rem; }

/* NO chained selectors (breaks BEM) */
.card .title { }
.button .icon { }

/* NO tag-qualified classes */
div.card { }
a.button { }

/* NO ID selectors */
#header { }

/* NO deep nesting beyond 2 levels */
.card__header__title__icon { } /* Too deep */

/* NO generic state classes without block context */
.is-active { }  /* Use .button--active instead */
.has-error { }  /* Use .input--error instead */

/* NO hardcoded colors/sizes (use design tokens) */
.card {
  color: #333;           /* ❌ Use var(--foreground) */
  padding: 24px;         /* ❌ Use var(--spacing-lg) */
  border-radius: 8px;    /* ❌ Use var(--radius-lg) */
}
```

### Allowed Patterns

✅ **Correct Usage**:
```css
/* Flat class selectors with design tokens */
.card {
  background-color: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-3xl);
}

/* Explicit block ownership */
.card__title {
  font-size: var(--text-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--card-foreground);
}

/* Boolean and value modifiers */
.button--primary { }
.button--lg { }
.card--elevated { }

/* Pseudo-states on BEM classes */
.button:hover { }
.button:focus-visible { }
.button:disabled { }

/* Global page utilities (limited exceptions) */
.page { }
.page__container { }

/* Third-party libraries (unmodifiable) */
.tiptap { }
.astro-* { }
```

---

## Audit Process

### 1. Inventory Phase
- Extract all class selectors from `.astro` and `.css` files
- Map class usage across templates (Astro pages, SolidJS islands)
- Identify design token violations (hardcoded colors, spacing, typography)
- Detect duplicates and collisions
- Find orphaned selectors (defined but not used)

### 2. Classification Phase
Each selector is categorized as:
- **Block** (component root)
- **Element** (component part)
- **Modifier** (component variation)
- **Global Utility** (allowed: `.page`, `.page__container`)
- **Third-party** (allowed: `.tiptap`, `.astro-*`)
- **Invalid** (Tailwind-style utilities, non-BEM patterns)

### 3. Violation Detection

**Naming Violations**:
- Incorrect separator usage (`_` instead of `__`, `-` instead of `--`)
- CamelCase or snake_case naming
- Too-deep element nesting (`.block__element__subelement`)

**Design Token Violations**:
- Hardcoded colors instead of `var(--primary)`, `var(--muted-foreground)`, etc.
- Hardcoded spacing instead of `var(--spacing-*)` or `var(--gap-*)`
- Hardcoded font sizes instead of `var(--text-*)`
- Hardcoded border radius instead of `var(--radius-*)`
- Hardcoded shadows instead of `var(--shadow-*)`

**Structural Violations**:
- Cross-block element access (`.card .button__text`)
- Tag-qualified classes (`div.button`)
- ID selectors
- Utility-first patterns (Tailwind-style)

### 4. Refactor Strategy

For each violation:
1. **Propose canonical BEM block name** (check existing blocks first)
2. **Replace hardcoded values with design tokens**
3. **Flatten selector structure** (convert nested to explicit elements)
4. **Normalize modifiers** (ensure `--` separator)
5. **Update markup** (Astro/TSX files) to match new class names

### 5. Design Token Compliance

Ensure all CSS uses design tokens:
```css
/* BEFORE (violations) */
.card {
  color: #333;
  background: #fff;
  padding: 24px;
  margin-bottom: 32px;
  border-radius: 8px;
  font-size: 18px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* AFTER (compliant) */
.card {
  color: var(--foreground);
  background: var(--card);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  border-radius: var(--radius-lg);
  font-size: var(--text-lg);
  box-shadow: var(--shadow-md);
}
```

### 6. Validation Phase
- Ensure no orphaned selectors remain
- Confirm visual intent preservation (run dev server, check pages)
- Verify class usage consistency across Astro/SolidJS components
- Check accessibility (focus states, ARIA compatibility)

---

## Example Transformations

### Example 1: Tailwind-style Utilities → BEM

**BEFORE (Violation)**:
```html
<!-- Astro component using Tailwind-style classes -->
<div class="flex gap-4 p-6 rounded-lg bg-white">
  <h2 class="text-xl font-bold">Title</h2>
  <p class="text-gray-600">Description</p>
</div>

<style>
.flex { display: flex; }
.gap-4 { gap: 1rem; }
.p-6 { padding: 1.5rem; }
.rounded-lg { border-radius: 0.5rem; }
.bg-white { background: white; }
.text-xl { font-size: 1.25rem; }
.font-bold { font-weight: bold; }
.text-gray-600 { color: #666; }
</style>
```

**AFTER (BEM Compliant)**:
```html
<div class="product-card">
  <h2 class="product-card__title">Title</h2>
  <p class="product-card__description">Description</p>
</div>

<style>
.product-card {
  display: flex;
  gap: var(--gap-md);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  background: var(--card);
}

.product-card__title {
  font-size: var(--text-xl);
  font-weight: var(--font-weight-bold);
  color: var(--card-foreground);
}

.product-card__description {
  color: var(--muted-foreground);
}
</style>
```

### Example 2: Nested Selectors → Flat BEM

**BEFORE (Violation)**:
```css
.card .header .title {
  font-size: 20px;
}

.card.active {
  border-color: blue;
}

.card .footer button {
  padding: 12px 24px;
}
```

**AFTER (BEM Compliant)**:
```css
.card__title {
  font-size: var(--text-xl);
}

.card--active {
  border-color: var(--primary);
}

.card__footer-button {
  padding: var(--spacing-sm) var(--spacing-lg);
}
```

```html
<div class="card card--active">
  <div class="card__header">
    <h2 class="card__title">Title</h2>
  </div>
  <div class="card__footer">
    <button class="card__footer-button">Action</button>
  </div>
</div>
```

### Example 3: Hardcoded Values → Design Tokens

**BEFORE (Violations)**:
```css
.product-card {
  background: #ffffff;
  color: #333333;
  border: 1px solid #e0e0e0;
  padding: 16px 24px;
  margin-bottom: 32px;
  border-radius: 8px;
  font-size: 16px;
  line-height: 1.5;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.product-card__title {
  color: #000000;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.product-card__description {
  color: #666666;
  font-size: 14px;
  line-height: 1.6;
}

.product-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
```

**AFTER (Design Token Compliant)**:
```css
.product-card {
  background: var(--card);
  color: var(--card-foreground);
  border: 1px solid var(--border);
  padding: var(--spacing-md) var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  border-radius: var(--radius-lg);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  box-shadow: var(--shadow-sm);
}

.product-card__title {
  color: var(--foreground);
  font-size: var(--text-2xl);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--spacing-sm);
}

.product-card__description {
  color: var(--muted-foreground);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
}

.product-card:hover {
  box-shadow: var(--shadow-md);
}
```

---

## Component-Specific Patterns

### Button Component Pattern
```css
/* Base button block */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  font-weight: var(--font-weight-medium);
  transition: background-color 150ms;
}

/* Variant modifiers */
.button--primary {
  background-color: var(--primary);
  color: var(--primary-foreground);
}

.button--secondary {
  background-color: var(--secondary);
  color: var(--secondary-foreground);
}

.button--destructive {
  background-color: var(--destructive);
  color: var(--destructive-foreground);
}

/* Size modifiers */
.button--sm {
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: var(--text-sm);
}

.button--lg {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: var(--text-lg);
}

/* Elements */
.button__icon {
  margin-right: var(--spacing-xs);
}

.button__text { }

/* States */
.button:hover {
  opacity: 0.9;
}

.button:focus-visible {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}

.button:disabled {
  opacity: 0.5;
  pointer-events: none;
}
```

### Modal Component Pattern
```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgb(0 0 0 / 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
  z-index: 50;
}

.modal-content {
  background: var(--card);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  max-width: 32rem;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border);
}

.modal-title {
  font-size: var(--text-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--foreground);
}

.modal-close {
  padding: var(--spacing-xs);
  color: var(--muted-foreground);
}

.modal-close:hover {
  color: var(--foreground);
}

.modal-body {
  padding: var(--spacing-lg);
}
```

---

## Accessibility Compliance

All CSS must support accessibility standards:

### Focus States
```css
/* All interactive elements MUST have visible focus indicators */
.button:focus-visible,
.browse-tags__tag:focus-visible,
.navigation__link:focus-visible {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}
```

### Color Contrast
- Body text: 4.5:1 minimum contrast ratio
- Large text: 3:1 minimum contrast ratio
- UI components: 3:1 against adjacent colors

**All semantic color tokens meet WCAG 2.1 Level AA standards.**

### Screen Reader Compatibility
```css
/* Hidden but accessible to screen readers */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Decorative elements should be hidden from screen readers via aria-hidden="true" */
/* No CSS-only hiding for interactive elements */
```

---

## File Organization

CSS files must follow this structure:

```
src/
├── styles/
│   └── global.css              # Global styles, shared .browse-* classes
├── components/
│   ├── Button.astro            # <style> block in component
│   ├── Card.astro              # <style> block in component
│   ├── products/
│   │   ├── ProductFilesForm.tsx          # SolidJS component
│   │   ├── product-files-form.css        # Co-located CSS
│   │   ├── ProductRoyaltyBreakdown.tsx
│   │   └── product-royalty-breakdown.css
```

**Rules**:
- Astro components: Use `<style>` blocks in `.astro` files
- SolidJS islands: Use co-located `.css` files with matching names
- Shared browse styles: Use `.browse-*` classes in `global.css`
- Page-specific styles: Use `<style>` blocks in page `.astro` files

---

## Output Modes

### Report Mode
Generates:
- BEM compliance score (0-100%)
- Design token compliance score (0-100%)
- List of violations by severity (critical, high, medium, low)
- Suggested renames and restructures
- Hardcoded value inventory (colors, spacing, typography)
- Unused selector report
- Missing design token opportunities

### Patch Mode
Generates:
- Diff-style rename suggestions
- Design token replacement mapping
- Refactored selector examples
- Migration mapping table (old → new)
- Markup update requirements (`.astro` and `.tsx` files)

### Auto-fix Mode
Generates:
- Updated CSS files with BEM-compliant selectors
- Design token replacements applied
- Updated markup class names in Astro/TSX files
- Migration notes for breaking changes
- Before/after screenshots (if possible)

---

## Safety & Constraints

- **Never rename without updating all references** (search across `.astro`, `.tsx`, `.css`)
- **Avoid visual regressions** - test in dev server before committing
- **Preserve comments and documentation**
- **Flag breaking changes clearly**
- **Verify accessibility** - ensure focus states, contrast ratios, ARIA compatibility
- **Test responsive behavior** - check mobile, tablet, desktop breakpoints

---

## Success Criteria

✅ **Pass Conditions**:
- All selectors follow valid BEM syntax (`.block__element--modifier`)
- No cross-block coupling remains
- No hardcoded colors, spacing, typography (all use design tokens)
- No utility-first CSS patterns (Tailwind-style)
- Reduced specificity and nesting
- Clear, predictable class semantics
- Accessibility standards maintained (focus states, contrast, ARIA)
- Responsive design patterns preserved

---

## Summary

This skill enforces Game Loopers' strict BEM architecture and design system compliance. It ensures:

1. **Consistent BEM naming** across all components
2. **Design token usage** for theming and maintainability
3. **No utility-first CSS** (Tailwind prohibition)
4. **Accessibility compliance** (WCAG 2.1 Level AA)
5. **Scalable architecture** for long-term maintenance

This is critical for a product-market fit focused MVP where consistency and maintainability enable rapid iteration.
