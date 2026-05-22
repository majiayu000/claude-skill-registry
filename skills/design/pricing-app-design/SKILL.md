---
name: pricing-app-design
description: Tesla Design System - CSS Modules, design tokens, dark mode, component patterns
license: MIT
metadata:
  author: pricing-app
  version: "1.0.0"
  scope: [frontend, root]
  auto_invoke:
    - "Styling with Tesla Design System"
    - "Creating design tokens"
    - "Implementing dark mode theming"
    - "Using CSS composition"
allowed-tools: Read, Edit, Write, Glob, Grep
---

# Pricing App - Tesla Design System

## CRITICAL RULES - NON-NEGOTIABLE

### Design Tokens
- ALWAYS: Use CSS variables from `design-tokens.css`
- ALWAYS: Theme-aware colors: `var(--bg-primary)`, `var(--text-primary)`
- NEVER: Hardcoded colors (#fff, rgb())
- NEVER: Inline styles for theming

### CSS Modules
- ALWAYS: Use composition: `composes: btn-base from '../../styles/buttons-tesla.css'`
- ALWAYS: CamelCase class names: `.modalHeader`, `.btnPrimary`
- NEVER: Nested selectors (keep flat)
- NEVER: !important (except in rare utility classes)

### Dark Mode
- ALWAYS: Test in both themes
- ALWAYS: Use semantic tokens (bg-primary) not raw colors (bg-white)
- ALWAYS: Respect user preference via ThemeContext

---

## DESIGN TOKENS

### Colors

**Backgrounds:**
```css
--bg-primary: #ffffff (light) / #1a1a1a (dark)
--bg-secondary: #f5f5f5 (light) / #2a2a2a (dark)
--bg-tertiary: #e0e0e0 (light) / #3a3a3a (dark)
--bg-hover: rgba(0,0,0,0.05) (light) / rgba(255,255,255,0.05) (dark)
--bg-overlay: rgba(0,0,0,0.3) (light) / rgba(0,0,0,0.5) (dark)
```

**Text:**
```css
--text-primary: #000000 (light) / #ffffff (dark)
--text-secondary: #666666 (light) / #a0a0a0 (dark)
--text-tertiary: #999999 (light) / #707070 (dark)
```

**Brand:**
```css
--brand-primary: #0066cc
--brand-secondary: #0052a3
--brand-hover: #004a94
```

**Semantic:**
```css
--success: #00c851
--success-bg: rgba(0,200,81,0.1)
--error: #ff3547
--error-bg: rgba(255,53,71,0.1)
--warning: #ffaa00
--warning-bg: rgba(255,170,0,0.1)
```

**Borders:**
```css
--border-color: #e0e0e0 (light) / #404040 (dark)
--border-hover: #cccccc (light) / #505050 (dark)
```

### Spacing

```css
--spacing-xs: 4px
--spacing-sm: 8px
--spacing-md: 16px
--spacing-lg: 24px
--spacing-xl: 32px
--spacing-xxl: 48px
```

### Border Radius

```css
--radius-sm: 4px
--radius-md: 8px
--radius-lg: 12px
--radius-full: 9999px
```

### Shadows

```css
--shadow-sm: 0 1px 3px rgba(0,0,0,0.1)
--shadow-md: 0 4px 6px rgba(0,0,0,0.1)
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1)
--shadow-tesla: 0 2px 8px rgba(0,0,0,0.08)
```

---

## TESLA COMPONENTS

### Buttons

**Available classes:**
- `.btn-base` - Base button styles
- `.btn-primary` - Primary action (brand color)
- `.btn-secondary` - Secondary action (outline)
- `.btn-danger` - Destructive action (red)
- `.btn-ghost` - Minimal button (transparent)
- `.btn-sm`, `.btn-md`, `.btn-lg` - Sizes

**Usage:**
```jsx
import styles from './MyComponent.module.css';

// In CSS Module:
.myButton {
  composes: btn-primary from '../../styles/buttons-tesla.css';
}

// In JSX:
<button className={styles.myButton}>Click Me</button>
```

### Modals

**Available classes:**
- `.modal-overlay` - Backdrop
- `.modal-container` - Modal wrapper
- `.modal-header` - Header with title
- `.modal-body` - Content area
- `.modal-footer` - Footer with actions

**Pattern:**
```jsx
<div className="modal-overlay">
  <div className="modal-container">
    <div className="modal-header">
      <h2>Title</h2>
      <button className="modal-close">×</button>
    </div>
    <div className="modal-body">
      {/* Content */}
    </div>
    <div className="modal-footer">
      <button className="btn-secondary">Cancel</button>
      <button className="btn-primary">Confirm</button>
    </div>
  </div>
</div>
```

### Tables

**Available classes:**
- `.table-tesla` - Base table
- `.table-row-hover` - Hover effect on rows
- `.table-striped` - Zebra striping
- `.table-compact` - Reduced padding

**Usage:**
```jsx
<table className="table-tesla table-row-hover">
  <thead>
    <tr>
      <th>Column 1</th>
      <th>Column 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Data 1</td>
      <td>Data 2</td>
    </tr>
  </tbody>
</table>
```

---

## DARK MODE

### ThemeContext

```jsx
import { useTheme } from '@/contexts/ThemeContext';

function MyComponent() {
  const { theme, toggleTheme } = useTheme();
  
  return (
    <button onClick={toggleTheme}>
      {theme === 'dark' ? '🌙' : '☀️'}
    </button>
  );
}
```

### Theme Toggle Persistence

```javascript
// Saved in localStorage
localStorage.setItem('theme', 'dark');

// Applied to document
document.documentElement.setAttribute('data-theme', 'dark');
```

### CSS for Dark Mode

```css
/* Light mode (default) */
:root {
  --bg-primary: #ffffff;
  --text-primary: #000000;
}

/* Dark mode */
[data-theme="dark"] {
  --bg-primary: #1a1a1a;
  --text-primary: #ffffff;
}

/* Component always uses token */
.container {
  background: var(--bg-primary);
  color: var(--text-primary);
}
```

---

## CSS COMPOSITION PATTERN

```css
/* Base component */
.btnBase {
  composes: btn-base from '../../styles/buttons-tesla.css';
  /* Custom additions */
  min-width: 120px;
}

.btnPrimary {
  composes: btnBase;
  composes: btn-primary from '../../styles/buttons-tesla.css';
}

.btnDanger {
  composes: btnBase;
  composes: btn-danger from '../../styles/buttons-tesla.css';
}
```

---

## RESPONSIVE DESIGN

```css
/* Mobile first */
.container {
  padding: var(--spacing-sm);
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: var(--spacing-md);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: var(--spacing-lg);
  }
}
```

---

## COMMON PITFALLS

- ❌ Don't hardcode colors → Use design tokens
- ❌ Don't use `!important` → Refactor specificity
- ❌ Don't nest selectors deeply → Keep flat
- ❌ Don't forget dark mode → Test both themes
- ❌ Don't mix inline styles → Use CSS Modules
- ❌ Don't create global classes → Use composition

---

## REFERENCES

### Internal
- [Design Tokens](../../frontend/src/styles/design-tokens.css)
- [Tesla Buttons](../../frontend/src/styles/buttons-tesla.css)
- [Tesla Modals](../../frontend/src/styles/modals-tesla.css)
- [Tesla Tables](../../frontend/src/styles/table-tesla.css)
- [ThemeContext](../../frontend/src/contexts/ThemeContext.jsx)
- [Theme Toggle Component](../../frontend/src/components/ThemeToggle.jsx)

### Assets
See `assets/` for examples:
- `button-example.module.css` - Button variants with composition
- `modal-example.module.css` - Modal styling
- `table-example.module.css` - Table styling
