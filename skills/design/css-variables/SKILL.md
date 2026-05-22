---
name: css-variables
description: Implements CSS custom properties for theming, component styling, and runtime customization. Use when building theme systems, dynamic styling, or configurable components.
---

# CSS Variables (Custom Properties)

Native CSS custom properties for dynamic theming and component customization.

## Quick Start

**Define variables:**
```css
:root {
  --color-primary: #3b82f6;
  --color-secondary: #6b7280;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --radius: 8px;
}
```

**Use variables:**
```css
.button {
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-primary);
  border-radius: var(--radius);
}

.card {
  padding: var(--spacing-lg);
  border-radius: var(--radius);
}
```

## Syntax

### Declaration

```css
/* Global scope */
:root {
  --variable-name: value;
}

/* Component scope */
.component {
  --component-bg: white;
  --component-padding: 16px;
}

/* Media query scope */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #1f2937;
    --color-text: #f9fafb;
  }
}
```

### Usage

```css
.element {
  /* Basic usage */
  color: var(--color-text);

  /* With fallback */
  background: var(--color-bg, white);

  /* Nested fallbacks */
  border-color: var(--border-color, var(--color-primary, blue));
}
```

## Theme System

### Light/Dark Mode

```css
:root {
  /* Light mode (default) */
  --color-bg: #ffffff;
  --color-text: #1f2937;
  --color-text-muted: #6b7280;
  --color-border: #e5e7eb;
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
}

/* Dark mode via class */
.dark {
  --color-bg: #1f2937;
  --color-text: #f9fafb;
  --color-text-muted: #9ca3af;
  --color-border: #374151;
  --color-primary: #60a5fa;
  --color-primary-hover: #93c5fd;
}

/* Dark mode via media query */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #1f2937;
    --color-text: #f9fafb;
  }
}
```

### Complete Token System

```css
:root {
  /* Spacing scale */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;

  /* Font sizes */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;

  /* Font weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-normal: 200ms ease;
  --transition-slow: 300ms ease;
}
```

## Component Variables

### Scoped Variables

```css
.button {
  /* Define component variables */
  --button-padding-x: var(--space-4);
  --button-padding-y: var(--space-2);
  --button-bg: var(--color-primary);
  --button-color: white;
  --button-radius: var(--radius-md);

  /* Use them */
  padding: var(--button-padding-y) var(--button-padding-x);
  background: var(--button-bg);
  color: var(--button-color);
  border-radius: var(--button-radius);
  border: none;
  cursor: pointer;
  transition: background var(--transition-fast);
}

.button:hover {
  --button-bg: var(--color-primary-hover);
}

/* Variant via CSS */
.button.secondary {
  --button-bg: var(--color-secondary);
  --button-color: var(--color-text);
}

/* Size variant */
.button.small {
  --button-padding-x: var(--space-3);
  --button-padding-y: var(--space-1);
}

.button.large {
  --button-padding-x: var(--space-6);
  --button-padding-y: var(--space-3);
}
```

### Customizable Components

```css
.card {
  --card-padding: var(--space-4);
  --card-bg: white;
  --card-border: 1px solid var(--color-border);
  --card-radius: var(--radius-lg);
  --card-shadow: var(--shadow-md);

  padding: var(--card-padding);
  background: var(--card-bg);
  border: var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
}

/* Override anywhere */
.featured-card {
  --card-shadow: var(--shadow-lg);
  --card-padding: var(--space-6);
}
```

## React Integration

### Setting Variables

```tsx
// Inline styles
function ThemedComponent({ accentColor }) {
  return (
    <div style={{ '--accent-color': accentColor } as React.CSSProperties}>
      <button className="themed-button">Click me</button>
    </div>
  );
}

// CSS
.themed-button {
  background: var(--accent-color, #3b82f6);
}
```

### Theme Provider

```tsx
// ThemeProvider.tsx
interface Theme {
  colors: {
    primary: string;
    secondary: string;
    background: string;
    text: string;
  };
  spacing: {
    sm: string;
    md: string;
    lg: string;
  };
}

const lightTheme: Theme = {
  colors: {
    primary: '#3b82f6',
    secondary: '#6b7280',
    background: '#ffffff',
    text: '#1f2937',
  },
  spacing: {
    sm: '8px',
    md: '16px',
    lg: '24px',
  },
};

const darkTheme: Theme = {
  colors: {
    primary: '#60a5fa',
    secondary: '#9ca3af',
    background: '#1f2937',
    text: '#f9fafb',
  },
  spacing: lightTheme.spacing,
};

function ThemeProvider({
  theme,
  children,
}: {
  theme: Theme;
  children: React.ReactNode;
}) {
  const style = {
    '--color-primary': theme.colors.primary,
    '--color-secondary': theme.colors.secondary,
    '--color-bg': theme.colors.background,
    '--color-text': theme.colors.text,
    '--space-sm': theme.spacing.sm,
    '--space-md': theme.spacing.md,
    '--space-lg': theme.spacing.lg,
  } as React.CSSProperties;

  return <div style={style}>{children}</div>;
}

// Usage
function App() {
  const [isDark, setIsDark] = useState(false);

  return (
    <ThemeProvider theme={isDark ? darkTheme : lightTheme}>
      <main className="app">
        <button onClick={() => setIsDark(!isDark)}>
          Toggle Theme
        </button>
      </main>
    </ThemeProvider>
  );
}
```

### Reading Variables in JS

```typescript
// Get computed value
const element = document.documentElement;
const primaryColor = getComputedStyle(element)
  .getPropertyValue('--color-primary')
  .trim();

// Set variable
element.style.setProperty('--color-primary', '#ff0000');

// React hook
function useCSSVariable(name: string) {
  const [value, setValue] = useState('');

  useEffect(() => {
    const computed = getComputedStyle(document.documentElement)
      .getPropertyValue(name)
      .trim();
    setValue(computed);
  }, [name]);

  const setVariable = useCallback((newValue: string) => {
    document.documentElement.style.setProperty(name, newValue);
    setValue(newValue);
  }, [name]);

  return [value, setVariable] as const;
}
```

## Calculations

```css
.element {
  /* Basic calc */
  padding: calc(var(--space-4) / 2);

  /* Combining variables */
  margin: calc(var(--space-2) + var(--space-4));

  /* With fixed values */
  width: calc(100% - var(--space-8));

  /* Multiplication */
  font-size: calc(var(--text-base) * 1.5);

  /* Complex expressions */
  height: calc(100vh - var(--header-height) - var(--footer-height));
}
```

## Responsive Variables

```css
:root {
  --container-padding: var(--space-4);
  --heading-size: var(--text-2xl);
}

@media (min-width: 768px) {
  :root {
    --container-padding: var(--space-6);
    --heading-size: var(--text-3xl);
  }
}

@media (min-width: 1024px) {
  :root {
    --container-padding: var(--space-8);
    --heading-size: var(--text-4xl);
  }
}

.container {
  padding: var(--container-padding);
}

h1 {
  font-size: var(--heading-size);
}
```

## Animation with Variables

```css
.animated-element {
  --animation-distance: 20px;
  --animation-duration: 0.3s;

  transition: transform var(--animation-duration) ease;
}

.animated-element:hover {
  transform: translateY(calc(var(--animation-distance) * -1));
}

/* Keyframes with variables */
@keyframes slide-in {
  from {
    transform: translateX(var(--slide-distance, 100%));
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.slide-in {
  --slide-distance: 50px;
  animation: slide-in 0.3s ease-out;
}
```

## Best Practices

1. **Use semantic names** - `--color-primary` not `--blue-500`
2. **Define at :root** - Global tokens at document level
3. **Component scope** - Component-specific vars in component
4. **Provide fallbacks** - `var(--color, fallback)`
5. **Document variables** - Comment what each does

## Common Patterns

### Color Opacity

```css
:root {
  --color-primary-rgb: 59, 130, 246;
}

.overlay {
  background: rgb(var(--color-primary-rgb) / 0.5);
}

.backdrop {
  background: rgb(var(--color-primary-rgb) / 0.1);
}
```

### Conditional Styling

```css
.component {
  --is-active: 0;
  opacity: calc(0.5 + (var(--is-active) * 0.5));
  transform: scale(calc(0.95 + (var(--is-active) * 0.05)));
}

.component.active {
  --is-active: 1;
}
```

## Reference Files

- [references/theming.md](references/theming.md) - Theme patterns
- [references/tokens.md](references/tokens.md) - Token organization
