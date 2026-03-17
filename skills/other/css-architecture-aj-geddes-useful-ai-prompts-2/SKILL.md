---
name: css-architecture
description: Organize CSS using BEM, SMACSS, and CSS-in-JS patterns. Use when building scalable, maintainable styling systems with proper naming conventions.
---

# CSS Architecture

## Overview

Build maintainable CSS systems using methodologies like BEM (Block Element Modifier), SMACSS, and CSS-in-JS patterns with proper organization and conventions.

## When to Use

- Large-scale stylesheets
- Component-based styling
- Design system development
- Multiple team collaboration
- CSS scalability and reusability

## Implementation Examples

### 1. **BEM (Block Element Modifier) Pattern**

```css
/* Block - standalone component */
.button {
  display: inline-block;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

/* Element - component part */
.button__icon {
  margin-right: 8px;
  vertical-align: middle;
}

/* Modifier - variant */
.button--primary {
  background-color: #007bff;
  color: white;
}

.button--primary:hover {
  background-color: #0056b3;
}

.button--secondary {
  background-color: #6c757d;
  color: white;
}

.button--disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.button--large {
  padding: 15px 30px;
  font-size: 18px;
}

.button--small {
  padding: 5px 10px;
  font-size: 12px;
}

/* Card Block with Elements */
.card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card__header {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  background-color: #f8f9fa;
}

.card__body {
  padding: 16px;
}

.card__footer {
  padding: 16px;
  border-top: 1px solid #e0e0e0;
  background-color: #f8f9fa;
}

.card--elevated {
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
```

### 2. **SMACSS (Scalable and Modular Architecture for CSS)**

```css
/* 1. Base Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 16px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #333;
  line-height: 1.6;
}

body {
  background-color: #fff;
}

a {
  color: #007bff;
  text-decoration: none;
}

/* 2. Layout Styles */
.layout-main {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20px;
  padding: 20px;
}

.layout-header {
  padding: 16px;
  background-color: #333;
  color: white;
}

.layout-sidebar {
  width: 250px;
  background-color: #f5f5f5;
  padding: 16px;
}

/* 3. Module Styles */
.module-card {
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.module-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.module-form__input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* 4. State Styles */
.is-hidden {
  display: none;
}

.is-active {
  background-color: #007bff;
  color: white;
}

.is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.is-error {
  border-color: #dc3545;
  color: #dc3545;
}

/* 5. Theme Styles */
.theme-dark {
  background-color: #222;
  color: #fff;
}

.theme-dark .module-card {
  border-color: #444;
}
```

### 3. **CSS-in-JS with Styled Components**

```typescript
// styled-components example
import styled from 'styled-components';

interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

const StyledButton = styled.button<ButtonProps>`
  display: inline-block;
  border: none;
  border-radius: 4px;
  cursor: ${props => props.disabled ? 'not-allowed' : 'pointer'};
  font-size: ${props => {
    switch (props.size) {
      case 'sm': return '12px';
      case 'lg': return '18px';
      default: return '16px';
    }
  }};
  padding: ${props => {
    switch (props.size) {
      case 'sm': return '5px 10px';
      case 'lg': return '15px 30px';
      default: return '10px 20px';
    }
  }};
  background-color: ${props => {
    if (props.disabled) return '#ccc';
    return props.variant === 'secondary' ? '#6c757d' : '#007bff';
  }};
  color: white;
  opacity: ${props => props.disabled ? 0.6 : 1};
  transition: all 0.3s ease;

  &:hover:not(:disabled) {
    background-color: ${props =>
      props.variant === 'secondary' ? '#5a6268' : '#0056b3'
    };
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }
`;

export const Button = (props: ButtonProps) => <StyledButton {...props} />;
```

### 4. **CSS Variables (Custom Properties)**

```css
/* Root variables */
:root {
  /* Colors */
  --color-primary: #007bff;
  --color-secondary: #6c757d;
  --color-danger: #dc3545;
  --color-success: #28a745;
  --color-warning: #ffc107;
  --color-text: #333;
  --color-background: #fff;
  --color-border: #e0e0e0;

  /* Typography */
  --font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-size-base: 16px;
  --font-size-lg: 18px;
  --font-size-sm: 14px;
  --line-height-base: 1.6;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 2px 4px rgba(0,0,0,0.1);
  --shadow-lg: 0 4px 8px rgba(0,0,0,0.15);

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
}

/* Dark theme override */
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #e0e0e0;
    --color-background: #1e1e1e;
    --color-border: #333;
  }
}

/* Usage */
.button {
  background-color: var(--color-primary);
  color: white;
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  font-family: var(--font-family-base);
  font-size: var(--font-size-base);
  line-height: var(--line-height-base);
}

.card {
  background-color: var(--color-background);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
}
```

### 5. **Utility-First CSS (Tailwind Pattern)**

```html
<!-- Utility classes provide granular control -->
<div class="flex flex-col gap-4 p-6 bg-white rounded-lg shadow-md">
  <h2 class="text-2xl font-bold text-gray-900">Title</h2>
  <p class="text-gray-600 leading-relaxed">Description</p>

  <div class="flex gap-2">
    <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition">
      Primary
    </button>
    <button class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition">
      Secondary
    </button>
  </div>
</div>

<style>
  /* Utility classes */
  .flex { display: flex; }
  .flex-col { flex-direction: column; }
  .gap-4 { gap: 1rem; }
  .gap-2 { gap: 0.5rem; }
  .p-6 { padding: 1.5rem; }
  .px-4 { padding-left: 1rem; padding-right: 1rem; }
  .py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
  .bg-white { background-color: white; }
  .bg-blue-500 { background-color: #3b82f6; }
  .text-white { color: white; }
  .text-gray-900 { color: #111827; }
  .text-2xl { font-size: 1.5rem; }
  .font-bold { font-weight: bold; }
  .rounded { border-radius: 0.375rem; }
  .rounded-lg { border-radius: 0.5rem; }
  .shadow-md { box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
</style>
```

## Best Practices

- Choose one methodology and stick to it
- Use CSS variables for theming
- Keep specificity low
- Organize files by feature
- Use preprocessors (Sass/Less) for DRY code
- Document naming conventions
- Implement proper file structure
- Use linting tools (stylelint)

## Resources

- [BEM Methodology](http://getbem.com/)
- [SMACSS](http://smacss.com/)
- [CSS Variables MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [Styled Components](https://styled-components.com/)
- [Tailwind CSS](https://tailwindcss.com/)
