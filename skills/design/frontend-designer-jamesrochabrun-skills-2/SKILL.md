---
name: frontend-designer
description: Build accessible, responsive, and performant frontend components with design system best practices, modern CSS, and framework-agnostic patterns.
---

# Frontend Designer

A comprehensive skill for frontend designers and developers to build beautiful, accessible, and performant user interfaces with modern best practices.

## What This Skill Does

Helps frontend designers/developers with:
- **Component Design & Development** - Build reusable, accessible components
- **Design Systems** - Implement tokens, patterns, and documentation
- **Responsive Design** - Mobile-first, fluid layouts
- **Accessibility (WCAG 2.1)** - Inclusive design patterns
- **Modern CSS** - Flexbox, Grid, custom properties
- **Performance Optimization** - Fast, efficient frontends
- **Framework Patterns** - React, Vue, Svelte best practices
- **Design-to-Code** - Figma to production workflows

## Why This Skill Matters

**Without systematic approach:**
- Inconsistent component implementations
- Accessibility issues
- Poor responsive behavior
- Duplicate code and styles
- Hard to maintain
- Performance problems

**With this skill:**
- Consistent, reusable components
- WCAG AA compliant by default
- Mobile-first responsive design
- Design system aligned
- Maintainable codebase
- Fast, optimized delivery

## Core Principles

### 1. Accessibility First
- WCAG 2.1 AA minimum
- Semantic HTML
- Keyboard navigation
- Screen reader support
- Focus management
- Color contrast

### 2. Mobile-First Responsive
- Start with mobile (320px)
- Progressive enhancement
- Fluid typography
- Flexible layouts
- Touch-friendly targets

### 3. Performance by Default
- Minimal CSS/JS
- Lazy loading
- Optimized images
- Critical CSS
- Tree shaking

### 4. Component-Driven
- Atomic design methodology
- Reusable components
- Props-based customization
- Composition over inheritance

### 5. Design System Aligned
- Design tokens
- Consistent spacing
- Typography scale
- Color palette
- Component library

## Component Patterns

### Button Component

**Accessible, flexible button pattern:**

```tsx
// React example
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  children,
  onClick,
  ...props
}) => {
  return (
    <button
      className={`btn btn--${variant} btn--${size}`}
      disabled={disabled || loading}
      onClick={onClick}
      aria-busy={loading}
      {...props}
    >
      {loading ? <Spinner /> : children}
    </button>
  );
};
```

**CSS (with design tokens):**

```css
.btn {
  /* Base styles */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);

  font-family: var(--font-sans);
  font-weight: 600;
  text-decoration: none;

  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;

  transition: all 0.2s ease;

  /* Accessibility */
  min-height: 44px; /* WCAG touch target */

  &:focus-visible {
    outline: 2px solid var(--color-focus);
    outline-offset: 2px;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

/* Variants */
.btn--primary {
  background: var(--color-primary);
  color: var(--color-on-primary);

  &:hover:not(:disabled) {
    background: var(--color-primary-hover);
  }
}

.btn--secondary {
  background: var(--color-secondary);
  color: var(--color-on-secondary);
}

.btn--ghost {
  background: transparent;
  color: var(--color-primary);
  border: 1px solid currentColor;
}

/* Sizes */
.btn--sm {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
}

.btn--md {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-base);
}

.btn--lg {
  padding: var(--space-4) var(--space-6);
  font-size: var(--text-lg);
}
```

### Card Component

**Flexible, accessible card:**

```tsx
interface CardProps {
  variant?: 'elevated' | 'outlined' | 'filled';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  interactive?: boolean;
  children: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({
  variant = 'elevated',
  padding = 'md',
  interactive = false,
  children,
}) => {
  const Component = interactive ? 'button' : 'div';

  return (
    <Component
      className={`
        card
        card--${variant}
        card--padding-${padding}
        ${interactive ? 'card--interactive' : ''}
      `}
      {...(interactive && { role: 'button', tabIndex: 0 })}
    >
      {children}
    </Component>
  );
};
```

**CSS:**

```css
.card {
  border-radius: var(--radius-lg);
  background: var(--color-surface);
}

.card--elevated {
  box-shadow: var(--shadow-md);
}

.card--outlined {
  border: 1px solid var(--color-border);
}

.card--filled {
  background: var(--color-surface-variant);
}

.card--interactive {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }

  &:focus-visible {
    outline: 2px solid var(--color-focus);
    outline-offset: 2px;
  }
}

.card--padding-sm { padding: var(--space-3); }
.card--padding-md { padding: var(--space-4); }
.card--padding-lg { padding: var(--space-6); }
```

### Form Input Component

**Accessible form input:**

```tsx
interface InputProps {
  label: string;
  error?: string;
  hint?: string;
  required?: boolean;
  type?: 'text' | 'email' | 'password' | 'number';
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  hint,
  required = false,
  type = 'text',
  ...props
}) => {
  const id = useId();
  const hintId = `${id}-hint`;
  const errorId = `${id}-error`;

  return (
    <div className="input-wrapper">
      <label htmlFor={id} className="input-label">
        {label}
        {required && <span aria-label="required">*</span>}
      </label>

      {hint && (
        <p id={hintId} className="input-hint">
          {hint}
        </p>
      )}

      <input
        id={id}
        type={type}
        className={`input ${error ? 'input--error' : ''}`}
        aria-required={required}
        aria-invalid={!!error}
        aria-describedby={error ? errorId : hint ? hintId : undefined}
        {...props}
      />

      {error && (
        <p id={errorId} className="input-error" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};
```

## Design Tokens

**CSS Custom Properties for design system:**

```css
:root {
  /* Colors - Primary */
  --color-primary: #0066FF;
  --color-primary-hover: #0052CC;
  --color-on-primary: #FFFFFF;

  /* Colors - Surface */
  --color-surface: #FFFFFF;
  --color-surface-variant: #F5F5F5;
  --color-on-surface: #1A1A1A;

  /* Colors - Borders */
  --color-border: #E0E0E0;
  --color-border-hover: #BDBDBD;

  /* Colors - Semantic */
  --color-error: #D32F2F;
  --color-success: #388E3C;
  --color-warning: #F57C00;
  --color-info: #1976D2;

  /* Spacing Scale (8px base) */
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-5: 1.5rem;   /* 24px */
  --space-6: 2rem;     /* 32px */
  --space-8: 3rem;     /* 48px */
  --space-10: 4rem;    /* 64px */

  /* Typography Scale */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */

  /* Font Families */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: "SF Mono", Monaco, "Cascadia Code", monospace;

  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;

  /* Border Radius */
  --radius-sm: 0.25rem;  /* 4px */
  --radius-md: 0.5rem;   /* 8px */
  --radius-lg: 1rem;     /* 16px */
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);

  /* Focus Ring */
  --color-focus: #0066FF;

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: #1A1A1A;
    --color-surface-variant: #2A2A2A;
    --color-on-surface: #FFFFFF;
    --color-border: #3A3A3A;
  }
}
```

## Responsive Design Patterns

### Mobile-First Breakpoints

```css
/* Mobile-first approach */
.container {
  padding: var(--space-4);

  /* Tablet: 768px and up */
  @media (min-width: 48rem) {
    padding: var(--space-6);
  }

  /* Desktop: 1024px and up */
  @media (min-width: 64rem) {
    padding: var(--space-8);
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### Fluid Typography

```css
/* Responsive typography */
h1 {
  font-size: clamp(2rem, 5vw, 3.5rem);
  line-height: var(--leading-tight);
}

h2 {
  font-size: clamp(1.5rem, 4vw, 2.5rem);
}

p {
  font-size: clamp(1rem, 2vw, 1.125rem);
  line-height: var(--leading-normal);
}
```

### Grid Layouts

```css
/* Responsive grid */
.grid {
  display: grid;
  gap: var(--space-4);

  /* Auto-fit columns (min 280px) */
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

/* 12-column grid system */
.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-4);
}

.col-span-4 {
  grid-column: span 4;
}

/* Stack on mobile */
@media (max-width: 48rem) {
  .col-span-4 {
    grid-column: span 12;
  }
}
```

## Accessibility Patterns

### Skip Links

```tsx
export const SkipLink = () => (
  <a href="#main-content" className="skip-link">
    Skip to main content
  </a>
);
```

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-primary);
  color: var(--color-on-primary);
  padding: var(--space-2) var(--space-4);
  text-decoration: none;
  z-index: 100;

  &:focus {
    top: 0;
  }
}
```

### Focus Management

```tsx
// Modal with focus trap
export const Modal = ({ isOpen, onClose, children }) => {
  const modalRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      // Save currently focused element
      const previouslyFocused = document.activeElement;

      // Focus first focusable element in modal
      const firstFocusable = modalRef.current?.querySelector(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      firstFocusable?.focus();

      // Restore focus on close
      return () => previouslyFocused?.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      className="modal-overlay"
    >
      <div className="modal">
        {children}
      </div>
    </div>
  );
};
```

### ARIA Labels

```tsx
// Icon button with accessible label
export const IconButton = ({ icon, label, ...props }) => (
  <button
    aria-label={label}
    className="icon-button"
    {...props}
  >
    <span aria-hidden="true">{icon}</span>
  </button>
);

// Loading state
export const LoadingButton = ({ loading, children, ...props }) => (
  <button
    aria-busy={loading}
    aria-live="polite"
    disabled={loading}
    {...props}
  >
    {loading ? 'Loading...' : children}
  </button>
);
```

## Performance Optimization

### Critical CSS

```html
<!-- Inline critical CSS -->
<style>
  /* Above-the-fold styles */
  body { margin: 0; font-family: var(--font-sans); }
  .header { /* critical header styles */ }
  .hero { /* critical hero styles */ }
</style>

<!-- Load full stylesheet async -->
<link rel="stylesheet" href="styles.css" media="print" onload="this.media='all'">
```

### Lazy Loading Images

```tsx
export const LazyImage = ({ src, alt, ...props }) => (
  <img
    src={src}
    alt={alt}
    loading="lazy"
    decoding="async"
    {...props}
  />
);
```

### Code Splitting

```tsx
// React lazy loading
const Dashboard = lazy(() => import('./Dashboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Dashboard />
    </Suspense>
  );
}
```

## Modern CSS Techniques

### Container Queries

```css
.card {
  container-type: inline-size;
}

.card-content {
  display: flex;
  flex-direction: column;

  /* Switch to row layout when container > 400px */
  @container (min-width: 400px) {
    flex-direction: row;
  }
}
```

### CSS Grid Auto-Fit

```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-4);
}
```

### Custom Properties for Theming

```css
/* Light theme (default) */
:root {
  --bg: #ffffff;
  --text: #000000;
}

/* Dark theme */
[data-theme="dark"] {
  --bg: #000000;
  --text: #ffffff;
}

body {
  background: var(--bg);
  color: var(--text);
}
```

## Component Library Structure

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.css
│   │   ├── Button.test.tsx
│   │   └── Button.stories.tsx
│   ├── Card/
│   ├── Input/
│   └── index.ts
├── tokens/
│   ├── colors.css
│   ├── spacing.css
│   ├── typography.css
│   └── index.css
├── utils/
│   ├── a11y.ts
│   └── responsive.ts
└── index.ts
```

## Using This Skill

### Generate Component

```bash
./scripts/generate_component.sh Button
```

Creates component with:
- TypeScript/JSX file
- CSS module
- Test file
- Storybook story
- Accessibility checks

### Design System Setup

```bash
./scripts/setup_design_system.sh
```

Creates:
- Design tokens (CSS custom properties)
- Base styles
- Component templates
- Documentation structure

### Accessibility Audit

```bash
./scripts/audit_accessibility.sh
```

Checks:
- Color contrast ratios
- Keyboard navigation
- ARIA attributes
- Semantic HTML
- Focus management

## Best Practices

### Component Design

✅ **DO:**
- Use semantic HTML
- Make components keyboard accessible
- Provide ARIA labels
- Support both light and dark modes
- Make touch targets 44x44px minimum
- Use proper heading hierarchy
- Handle loading and error states

❌ **DON'T:**
- Use divs for buttons
- Forget focus styles
- Hard-code colors
- Ignore mobile viewports
- Skip alt text on images
- Create inaccessible modals

### CSS Best Practices

✅ **DO:**
- Use design tokens
- Mobile-first responsive
- BEM or CSS modules for naming
- Logical properties (inline-start vs left)
- Modern layout (flexbox, grid)

❌ **DON'T:**
- Use !important
- Deep nesting (> 3 levels)
- Fixed pixel values everywhere
- Browser-specific hacks
- Inline styles

### Performance

✅ **DO:**
- Lazy load images
- Code split routes
- Minimize CSS
- Use system fonts
- Optimize images (WebP)
- Critical CSS inline

❌ **DON'T:**
- Load unused CSS
- Large JavaScript bundles
- Unoptimized images
- Blocking resources
- Too many web fonts

## Framework-Specific Patterns

### React

```tsx
// Composition pattern
export const Card = ({ children }) => (
  <div className="card">{children}</div>
);

export const CardHeader = ({ children }) => (
  <div className="card-header">{children}</div>
);

// Usage
<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content</CardBody>
</Card>
```

### Vue

```vue
<!-- Composable component -->
<template>
  <div :class="cardClasses">
    <slot />
  </div>
</template>

<script setup>
const props = defineProps({
  variant: String,
  padding: String
});

const cardClasses = computed(() => [
  'card',
  `card--${props.variant}`,
  `card--padding-${props.padding}`
]);
</script>
```

## Resources

All reference materials included:
- Design token systems
- Accessibility checklist (WCAG 2.1)
- Responsive design patterns
- Component library templates
- Performance optimization guide

## Summary

This skill provides:
- **Accessible components** - WCAG AA by default
- **Responsive design** - Mobile-first approach
- **Design systems** - Token-based consistency
- **Modern CSS** - Flexbox, Grid, custom properties
- **Performance** - Optimized delivery
- **Best practices** - Production-ready patterns

**Use this skill to build beautiful, accessible, performant frontends.**

---

**"Good design is accessible design."**
