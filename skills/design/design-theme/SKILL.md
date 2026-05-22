---
name: design-theme
description: |
  DESIGN-THEME
---

---
description: Create or update theme with design tokens
argument-hint: "[selected-direction]"
---

# DESIGN-THEME

Implement a theme system with proper design tokens.

## MANDATORY: Kimi Delegation

**Theme implementation MUST be delegated to Kimi K2.5 via MCP.**

Kimi excels at CSS/Tailwind work:

```javascript
mcp__kimi__spawn_agent({
  prompt: `Implement design theme with tokens:
Direction: ${selectedDNA}
Typography: ${fontStack}
Colors: ${palette}
Use Tailwind 4 @theme directive (CSS-first).
OKLCH for colors. Modular type scale.
Output: Update app/globals.css with token architecture.
Then update components to use tokens.`,
  thinking: true
})
```

**Workflow:**
1. Define direction → Claude (from catalog selection)
2. Implement tokens → Kimi (CSS/Tailwind work)
3. Validate → Claude (quality checks)

## When to Use

- After `/design-catalog` — user selected a direction
- After `/design-audit` — fixing design debt
- Starting fresh — establishing design system

## Process

### 1. Understand Direction

If `$1` provided (from catalog selection):
- Load the selected design DNA
- Extract: typography, colors, spacing, motion

If from audit:
- Address issues found
- Maintain existing patterns where working

### 2. Define Token Architecture

Using Tailwind 4 `@theme` directive (CSS-first):

```css
@theme {
  /* Colors - OKLCH for perceptual uniformity */
  --color-primary: oklch(0.7 0.15 250);
  --color-primary-hover: oklch(0.65 0.15 250);

  /* Typography - modular scale */
  --font-sans: "Custom Font", system-ui, sans-serif;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;

  /* Spacing - consistent scale */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-8: 2rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px oklch(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px oklch(0 0 0 / 0.1);

  /* Radii */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
}
```

### 3. Implement Tokens

Update `app/globals.css` (or equivalent):
- Define all tokens in `@theme`
- Remove `tailwind.config.ts` (CSS-first approach)
- Migrate hardcoded values to tokens

### 4. Update Components

For each component:
- Replace hardcoded colors → `var(--color-*)`
- Replace magic numbers → `var(--spacing-*)`
- Ensure dark mode support

### 5. Validate

Run quality checks:
```
/check-quality  # Typecheck, lint, tests
/rams           # Accessibility score
```

### 6. Document Theme

Create or update design system docs:

```markdown
## Theme: [Name]

### Colors
[Visual color palette with names and values]

### Typography
[Font stack, scale, usage guidelines]

### Spacing
[Scale and when to use each]

### Components
[Key component patterns]
```

## Token Naming Convention

```
--category-variant-state

Examples:
--color-primary
--color-primary-hover
--color-text-muted
--text-heading-1
--spacing-component-gap
```

## Output

Theme implemented with tokens. Commit:
```bash
git add -A && git commit -m "feat: implement design system tokens"
```
