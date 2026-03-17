---
name: validating-design-tokens
description: Ensures CSS and components only use approved design tokens. Use when the user asks about design system enforcement, hardcoded colors, spacing values, or wants to validate token usage across files.
---

# Design System Token Validator

## When to use this skill

- User asks to check for hardcoded colors or spacing
- User wants to enforce design token usage
- User mentions design system consistency
- User asks to find `var(--token-*)` violations
- User wants to prevent design debt

## Workflow

- [ ] Identify design token source file
- [ ] Scan target files (CSS, TSX, Vue)
- [ ] Detect hardcoded values
- [ ] Match violations to available tokens
- [ ] Generate fix suggestions
- [ ] Report violations by severity

## Instructions

### Step 1: Identify Token Source

Locate design token definitions:

```bash
ls src/styles/tokens.css src/tokens/*.css styles/variables.css 2>/dev/null
ls src/styles/tokens.ts src/tokens/*.ts 2>/dev/null
ls tokens.json style-dictionary.config.* 2>/dev/null
```

Common token file patterns:

- CSS custom properties: `--color-*`, `--spacing-*`, `--font-*`
- JavaScript/TypeScript objects: `tokens.colors.*`, `theme.spacing.*`
- Style Dictionary output: `tokens.json`

### Step 2: Extract Available Tokens

**From CSS variables:**

```bash
grep -hoE 'var\(--[a-zA-Z0-9-]+' src/styles/tokens.css | sort -u
```

**Parse into categories:**

| Category    | Pattern                          | Examples                                |
| ----------- | -------------------------------- | --------------------------------------- |
| Colors      | `--color-*`                      | `--color-primary`, `--color-text-muted` |
| Spacing     | `--spacing-*`, `--space-*`       | `--spacing-md`, `--space-4`             |
| Typography  | `--font-*`, `--text-*`           | `--font-size-lg`, `--font-weight-bold`  |
| Radii       | `--radius-*`, `--rounded-*`      | `--radius-md`, `--rounded-lg`           |
| Shadows     | `--shadow-*`                     | `--shadow-sm`, `--shadow-elevated`      |
| Transitions | `--transition-*`, `--duration-*` | `--transition-fast`                     |
| Z-index     | `--z-*`                          | `--z-modal`, `--z-tooltip`              |

### Step 3: Scan for Violations

**Hardcoded colors in CSS:**

```bash
grep -rn --include="*.css" --include="*.scss" -E '#[0-9a-fA-F]{3,8}|rgb\(|rgba\(|hsl\(' src/
```

**Hardcoded colors in JSX/TSX:**

```bash
grep -rn --include="*.tsx" --include="*.jsx" -E "color:\s*['\"]#|background:\s*['\"]#|borderColor:\s*['\"]#" src/
```

**Hardcoded spacing (px values):**

```bash
grep -rn --include="*.css" --include="*.scss" -E ':\s*[0-9]+px' src/ | grep -v "0px\|1px"
```

**Inline styles in React:**

```bash
grep -rn --include="*.tsx" --include="*.jsx" "style={{" src/
```

**Tailwind arbitrary values (if using tokens with Tailwind):**

```bash
grep -rn --include="*.tsx" --include="*.jsx" -E '\[#[0-9a-fA-F]+\]|\[[0-9]+px\]' src/
```

### Step 4: Categorize Violations

**Severity levels:**

| Severity | Description                            | Examples                           |
| -------- | -------------------------------------- | ---------------------------------- |
| Error    | Hardcoded colors in component styles   | `color: #333333`                   |
| Error    | Hardcoded spacing in layout            | `padding: 24px`                    |
| Warning  | Inline styles with raw values          | `style={{ margin: 10 }}`           |
| Warning  | Magic numbers                          | `width: 347px`                     |
| Info     | One-off values that may be intentional | Border widths, specific dimensions |

### Step 5: Match to Available Tokens

For each violation, suggest the closest token:

```markdown
## Violation Report

### src/components/Card.module.css:15

**Found**: `background-color: #f5f5f5;`
**Suggestion**: `background-color: var(--color-surface);`

### src/components/Button.tsx:42

**Found**: `padding: '16px 24px'`
**Suggestion**: `padding: 'var(--spacing-md) var(--spacing-lg)'`

### src/pages/Home.module.css:8

**Found**: `color: #1a1a1a;`
**Suggestion**: `color: var(--color-text-primary);`
```

### Step 6: Generate Fixes

**CSS fix pattern:**

```css
/* Before */
.card {
  background-color: #ffffff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* After */
.card {
  background-color: var(--color-surface);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}
```

**React inline style fix:**

```tsx
// Before
<div style={{ color: '#333', marginBottom: 16 }}>

// After
<div style={{ color: 'var(--color-text)', marginBottom: 'var(--spacing-md)' }}>

// Best: Use CSS modules instead
<div className={styles.container}>
```

**Tailwind with CSS variables:**

```tsx
// Before (arbitrary value)
<div className="bg-[#3b82f6] p-[24px]">

// After (use theme or CSS var)
<div className="bg-primary p-6">
// Or with CSS variable in tailwind.config.js
```

## Token Mapping Reference

Create a mapping file for consistent suggestions:

```typescript
// scripts/token-map.ts
export const colorMap: Record<string, string> = {
  "#ffffff": "var(--color-surface)",
  "#000000": "var(--color-text)",
  "#3b82f6": "var(--color-primary)",
  "#ef4444": "var(--color-error)",
  "#22c55e": "var(--color-success)",
};

export const spacingMap: Record<string, string> = {
  "4px": "var(--spacing-xs)",
  "8px": "var(--spacing-sm)",
  "16px": "var(--spacing-md)",
  "24px": "var(--spacing-lg)",
  "32px": "var(--spacing-xl)",
};

export const findClosestToken = (
  value: string,
  map: Record<string, string>,
): string | null => {
  return map[value.toLowerCase()] ?? null;
};
```

## ESLint Integration

**Custom ESLint rule (conceptual):**

```javascript
// .eslintrc.js
module.exports = {
  rules: {
    "no-hardcoded-colors": "error",
    "no-hardcoded-spacing": "warn",
  },
};
```

**Stylelint for CSS:**

```bash
npm install -D stylelint stylelint-declaration-strict-value
```

```javascript
// .stylelintrc.js
module.exports = {
  plugins: ["stylelint-declaration-strict-value"],
  rules: {
    "scale-unlimited/declaration-strict-value": [
      ["/color/", "fill", "stroke", "background", "border-color"],
      {
        ignoreValues: ["transparent", "inherit", "currentColor"],
      },
    ],
  },
};
```

## Report Template

```markdown
## Design Token Validation Report

**Scanned**: 47 files
**Violations**: 12
**Auto-fixable**: 9

### Summary by Category

| Category   | Violations | Fixable |
| ---------- | ---------- | ------- |
| Colors     | 7          | 6       |
| Spacing    | 4          | 3       |
| Typography | 1          | 0       |

### Violations

#### Colors (7)

| File            | Line | Found             | Suggested Token   |
| --------------- | ---- | ----------------- | ----------------- |
| Card.module.css | 15   | `#f5f5f5`         | `--color-surface` |
| Button.tsx      | 42   | `#3b82f6`         | `--color-primary` |
| Header.css      | 8    | `rgba(0,0,0,0.5)` | `--color-overlay` |

#### Spacing (4)

| File       | Line | Found  | Suggested Token |
| ---------- | ---- | ------ | --------------- |
| Layout.css | 23   | `24px` | `--spacing-lg`  |
| Modal.tsx  | 67   | `16px` | `--spacing-md`  |
```

## Validation

Before completing:

- [ ] All hardcoded colors replaced with tokens
- [ ] Spacing uses token scale
- [ ] No inline styles with raw values
- [ ] Stylelint configured for enforcement
- [ ] New violations blocked in CI

## Error Handling

- **No token file found**: Ask user to specify token source location.
- **Unknown color value**: Flag for manual review; may need new token.
- **False positives**: Exclude reset styles, third-party CSS, and intentional overrides.
- **Complex values**: Gradients, calc() expressions may need manual review.

## Resources

- [Style Dictionary](https://amzn.github.io/style-dictionary/)
- [Stylelint Declaration Strict Value](https://github.com/AndyOGo/stylelint-declaration-strict-value)
- [Design Tokens W3C Spec](https://design-tokens.github.io/community-group/format/)
