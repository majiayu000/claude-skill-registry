---
name: css-modules
description: Implements scoped CSS using CSS Modules with automatic class name generation, composition, and TypeScript support. Use when needing component-scoped styles, avoiding naming collisions, or migrating from global CSS.
---

# CSS Modules

Locally scoped CSS by generating unique class names at build time.

## Quick Start

CSS Modules work out of the box in Vite, Next.js, and Create React App.

**Create module file:**
```css
/* Button.module.css */
.button {
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.primary {
  background: #3b82f6;
  color: white;
}

.secondary {
  background: #e5e7eb;
  color: #1f2937;
}
```

**Import and use:**
```tsx
// Button.tsx
import styles from './Button.module.css';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
}

export function Button({ variant = 'primary', children }: ButtonProps) {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
}
```

## File Naming Convention

```
ComponentName.module.css    # Component styles
page.module.css             # Page styles
layout.module.css           # Layout styles
```

Files without `.module.css` are treated as global CSS.

## Accessing Classes

```tsx
import styles from './Component.module.css';

// Single class
<div className={styles.container} />

// Multiple classes
<div className={`${styles.card} ${styles.elevated}`} />

// Conditional classes
<div className={`${styles.button} ${isActive ? styles.active : ''}`} />

// Dynamic class from variable
const variant = 'primary';
<div className={styles[variant]} />

// With clsx/classnames library
import clsx from 'clsx';
<div className={clsx(styles.button, {
  [styles.active]: isActive,
  [styles.disabled]: isDisabled,
})} />
```

## Class Name Conventions

CSS class names become JavaScript property names:

```css
/* Valid patterns */
.button { }           /* styles.button */
.primaryButton { }    /* styles.primaryButton */
.primary-button { }   /* styles['primary-button'] or styles.primaryButton (with camelCase) */
.Button { }           /* styles.Button */

/* Avoid - invalid JS identifiers */
.123start { }         /* Won't work */
.my class { }         /* Won't work */
```

## Composition

### Same File Composition

```css
/* base.module.css */
.base {
  padding: 16px;
  border-radius: 8px;
  font-family: system-ui;
}

.card {
  composes: base;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.panel {
  composes: base;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
}
```

### Cross-File Composition

```css
/* typography.module.css */
.heading {
  font-weight: 700;
  line-height: 1.2;
}

.body {
  font-weight: 400;
  line-height: 1.6;
}
```

```css
/* Card.module.css */
.title {
  composes: heading from './typography.module.css';
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.description {
  composes: body from './typography.module.css';
  color: #6b7280;
}
```

### Composing Multiple Classes

```css
.special {
  composes: base highlight from './shared.module.css';
  composes: bordered from './borders.module.css';
}
```

### Global Class Composition

```css
.button {
  /* Compose from global CSS (like a reset or utility) */
  composes: reset-button from global;
  padding: 12px 24px;
}
```

## Global Styles

### :global Selector

```css
/* Within a module file */
:global(.body-locked) {
  overflow: hidden;
}

/* Mixed local and global */
.modal :global(.overlay) {
  background: rgba(0,0,0,0.5);
}

/* Global block */
:global {
  .utility-class {
    display: flex;
  }
  .another-utility {
    gap: 16px;
  }
}
```

### :local Selector (explicit)

```css
:local(.className) {
  /* Explicitly local (default behavior) */
}
```

## Nesting with PostCSS

With PostCSS nesting or native CSS nesting:

```css
.card {
  padding: 16px;

  .header {
    display: flex;
    justify-content: space-between;
  }

  .body {
    margin-top: 12px;
  }

  &:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }

  &.highlighted {
    border: 2px solid #3b82f6;
  }
}
```

## TypeScript Support

### Declaration File

```typescript
// css-modules.d.ts (in src/ or types/)
declare module '*.module.css' {
  const classes: { readonly [key: string]: string };
  export default classes;
}

declare module '*.module.scss' {
  const classes: { readonly [key: string]: string };
  export default classes;
}
```

### typed-css-modules

Generate type definitions from CSS files:

```bash
npm install -D typed-css-modules
npx tcm src
```

Generates `.css.d.ts` files:

```typescript
// Button.module.css.d.ts
declare const styles: {
  readonly button: string;
  readonly primary: string;
  readonly secondary: string;
};
export default styles;
```

**Watch mode:**
```bash
npx tcm src --watch
```

**Options:**
```bash
# CamelCase class names
npx tcm src --camelCase

# Named exports (for tree shaking)
npx tcm src --namedExports

# TypeScript 5 arbitrary extensions
npx tcm src --allowArbitraryExtensions
```

### typescript-plugin-css-modules

IDE support without generating files:

```json
// tsconfig.json
{
  "compilerOptions": {
    "plugins": [
      { "name": "typescript-plugin-css-modules" }
    ]
  }
}
```

## Framework Configuration

### Vite

Works out of the box. Custom configuration:

```typescript
// vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  css: {
    modules: {
      // Generate scoped class names
      generateScopedName: '[name]__[local]___[hash:base64:5]',
      // Export class names as camelCase
      localsConvention: 'camelCase',
    },
  },
});
```

### Next.js

Works out of the box. No configuration needed.

### Webpack (manual)

```javascript
// webpack.config.js
module.exports = {
  module: {
    rules: [
      {
        test: /\.module\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              modules: {
                localIdentName: '[name]__[local]--[hash:base64:5]',
              },
            },
          },
        ],
      },
    ],
  },
};
```

## Patterns

### Component with Variants

```css
/* Alert.module.css */
.alert {
  padding: 12px 16px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.info {
  composes: alert;
  background: #dbeafe;
  color: #1e40af;
}

.success {
  composes: alert;
  background: #dcfce7;
  color: #166534;
}

.warning {
  composes: alert;
  background: #fef3c7;
  color: #92400e;
}

.error {
  composes: alert;
  background: #fee2e2;
  color: #991b1b;
}
```

```tsx
import styles from './Alert.module.css';

type AlertVariant = 'info' | 'success' | 'warning' | 'error';

interface AlertProps {
  variant: AlertVariant;
  children: React.ReactNode;
}

export function Alert({ variant, children }: AlertProps) {
  return <div className={styles[variant]}>{children}</div>;
}
```

### Responsive Styles

```css
.container {
  padding: 16px;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 768px) {
  .container {
    padding: 24px;
  }

  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Theming with CSS Variables

```css
.card {
  background: var(--card-bg, white);
  color: var(--card-text, #1f2937);
  border: 1px solid var(--card-border, #e5e7eb);
  border-radius: var(--radius-md, 8px);
  padding: var(--spacing-4, 16px);
}

/* Dark theme override via parent */
:global(.dark) .card {
  --card-bg: #1f2937;
  --card-text: #f9fafb;
  --card-border: #374151;
}
```

## Best Practices

1. **One module per component** - Keep styles co-located
2. **Use composition** - Share styles via `composes`
3. **Avoid deep nesting** - Max 2-3 levels
4. **Meaningful class names** - `.submitButton` not `.btn1`
5. **TypeScript types** - Use typed-css-modules or plugin

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `.module.css` extension | Rename to `*.module.css` |
| Accessing undefined class | Check spelling, add TypeScript |
| composes after other rules | Move `composes` to top of rule |
| Circular composition | Restructure dependencies |
| Styling by element | Use class selectors instead |

## Reference Files

- [references/composition.md](references/composition.md) - Advanced composition
- [references/typescript.md](references/typescript.md) - TypeScript integration
