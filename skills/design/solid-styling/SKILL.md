---
name: solid-styling
description: "SolidJS styling: CSS Modules, Tailwind, Sass, Less, CSS-in-JS, global styles, component-scoped styles, class and style bindings."
metadata:
  globs:
    - "**/*.css"
    - "**/*.scss"
    - "**/*.less"
    - "**/*module.css"
    - "tailwind.config.*"
---

# SolidJS Styling

Complete guide to styling SolidJS components. Choose from CSS preprocessors, CSS Modules, utility frameworks, or CSS-in-JS solutions.

## Basic Styling

### Class Binding

```tsx
import { createSignal } from "solid-js";

function Component() {
  const [active, setActive] = createSignal(false);

  return (
    <button
      class="btn"
      classList={{ active: active() }}
      onClick={() => setActive(!active())}
    >
      Click me
    </button>
  );
}
```

### Style Binding

```tsx
function Component() {
  const [color, setColor] = createSignal("red");

  return (
    <div style={{ color: color(), "font-size": "16px" }}>
      Styled content
    </div>
  );
}
```

## CSS Modules

Scoped CSS with automatic class name hashing.

### Setup

```tsx
// Component.module.css
.button {
  padding: 10px;
  background: blue;
}

.active {
  background: red;
}
```

### Usage

```tsx
import styles from "./Component.module.css";

function Component() {
  return (
    <button class={styles.button}>
      Click me
    </button>
  );
}
```

**Benefits:**
- Scoped styles
- No naming conflicts
- Type-safe (with TypeScript)
- Automatic class hashing

## Tailwind CSS

Utility-first CSS framework.

### Setup

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**tailwind.config.js:**
```js
export default {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

### Usage

```tsx
function Component() {
  return (
    <div class="flex items-center justify-center p-4 bg-blue-500">
      <button class="px-4 py-2 bg-white rounded hover:bg-gray-100">
        Click me
      </button>
    </div>
  );
}
```

**Features:**
- Utility classes
- Responsive design
- Dark mode
- Custom configuration

## Sass/Less

CSS preprocessors for advanced styling.

### Sass Setup

```bash
npm install -D sass
```

**Component.scss:**
```scss
$primary-color: blue;

.button {
  padding: 10px;
  background: $primary-color;

  &:hover {
    background: darken($primary-color, 10%);
  }
}
```

**Usage:**
```tsx
import "./Component.scss";

function Component() {
  return <button class="button">Click me</button>;
}
```

### Less Setup

```bash
npm install -D less
```

**Component.less:**
```less
@primary-color: blue;

.button {
  padding: 10px;
  background: @primary-color;
}
```

## CSS-in-JS

### Macaron

Type-safe CSS-in-JS for Solid.

```tsx
import { styled } from "@macaron-css/solid";

const Button = styled("button", {
  base: {
    padding: "10px",
    background: "blue",
  },
  variants: {
    size: {
      small: { padding: "5px" },
      large: { padding: "20px" },
    },
  },
});

function Component() {
  return <Button size="large">Click me</Button>;
}
```

### Other CSS-in-JS Libraries

- Solid Styled Components
- Solid Styled JSX
- Vanilla Extract (with adapter)

## UnoCSS

Atomic CSS engine.

### Setup

```bash
npm install -D unocss
```

**uno.config.ts:**
```ts
import { defineConfig } from "unocss";

export default defineConfig({
  // ...
});
```

### Usage

```tsx
function Component() {
  return (
    <div class="flex items-center p-4">
      <button class="btn-primary">Click me</button>
    </div>
  );
}
```

## Global Styles

### Import Global CSS

```tsx
// app.tsx or entry-client.tsx
import "./styles.css";

export default function App() {
  return <div>App</div>;
}
```

### CSS Variables

```css
/* styles.css */
:root {
  --primary-color: blue;
  --spacing: 16px;
}

.button {
  background: var(--primary-color);
  padding: var(--spacing);
}
```

## Component-Scoped Styles

### CSS Modules (Recommended)

```tsx
import styles from "./Component.module.css";
```

### Scoped Styles with Build Tools

Vite automatically handles scoped styles when using `<style scoped>`:

```tsx
function Component() {
  return (
    <>
      <div class="container">Content</div>
      <style>{`
        .container {
          padding: 20px;
        }
      `}</style>
    </>
  );
}
```

## Dynamic Styling

### Conditional Classes

```tsx
function Component() {
  const [active, setActive] = createSignal(false);

  return (
    <button
      class="btn"
      classList={{
        active: active(),
        disabled: !active(),
      }}
    >
      Click me
    </button>
  );
}
```

### Dynamic Styles

```tsx
function Component() {
  const [width, setWidth] = createSignal(100);

  return (
    <div
      style={{
        width: `${width()}px`,
        transition: "width 0.3s",
      }}
    >
      Content
    </div>
  );
}
```

## Best Practices

1. **Choose the right solution:**
   - CSS Modules: Scoped styles, type safety
   - Tailwind: Rapid development, utility-first
   - Sass/Less: Advanced features, variables
   - CSS-in-JS: Dynamic styles, theming

2. **Use CSS Modules for components:**
   - Prevents naming conflicts
   - Better performance
   - Type safety

3. **Use Tailwind for utilities:**
   - Rapid prototyping
   - Consistent design
   - Small bundle size (with purging)

4. **Organize styles:**
   - Component-level: CSS Modules
   - Global: Separate CSS file
   - Utilities: Tailwind/UnoCSS

5. **Optimize for production:**
   - Purge unused CSS
   - Minify CSS
   - Use CSS variables for theming

## Common Patterns

### Theming

```css
/* styles.css */
[data-theme="dark"] {
  --bg-color: #000;
  --text-color: #fff;
}

[data-theme="light"] {
  --bg-color: #fff;
  --text-color: #000;
}
```

```tsx
function Component() {
  const [theme, setTheme] = createSignal("light");

  return (
    <div data-theme={theme()}>
      <button onClick={() => setTheme(theme() === "light" ? "dark" : "light")}>
        Toggle theme
      </button>
    </div>
  );
}
```

### Responsive Design

**Tailwind:**
```tsx
<div class="text-sm md:text-base lg:text-lg">
  Responsive text
</div>
```

**CSS:**
```css
.container {
  padding: 10px;
}

@media (min-width: 768px) {
  .container {
    padding: 20px;
  }
}
```

## Summary

- **CSS Modules**: Scoped, type-safe styles
- **Tailwind**: Utility-first framework
- **Sass/Less**: Preprocessors with advanced features
- **CSS-in-JS**: Dynamic, component-based styles
- **Global styles**: Import CSS files
- **Dynamic styling**: Use classList and style bindings

