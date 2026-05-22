---
name: mantine-dev
description: "Mantine UI library for React: 100+ components, hooks, forms, theming, dark mode, CSS modules, and Vite/TypeScript setup."
version: "8.3.14"
release_date: "2026-02-01"
---

# Mantine UI Library

Mantine is a fully-featured React components library with TypeScript support. It provides 100+ hooks and components with native dark mode, CSS-in-JS via CSS modules, and excellent accessibility.

## When to use

- Building React applications with a comprehensive UI library
- Need TypeScript-first component library with full type safety
- Want native dark/light theme support with CSS variables
- Building forms with validation (useForm hook)
- Need utility hooks for common React patterns
- Working with Vite as build tool

## Focus

This skill focuses on:

- **Vite** + **TypeScript** setup (not Next.js or CRA)
- CSS modules with PostCSS preset
- Vitest for testing
- ESLint with eslint-config-mantine

## Quick Start (Vite Template)

```bash
# Use official template (recommended)
git clone https://github.com/mantinedev/vite-template my-app
cd my-app
yarn install
yarn dev
```

Or manual setup:

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @mantine/core @mantine/hooks
npm install -D postcss postcss-preset-mantine postcss-simple-vars
```

## Required Packages

```bash
# Core packages
npm install @mantine/core @mantine/hooks

# Optional packages (as needed)
npm install @mantine/form          # Form management
npm install @mantine/dates dayjs   # Date components
npm install @mantine/charts recharts # Charts
npm install @mantine/notifications  # Toast notifications
npm install @mantine/modals        # Modal manager
npm install @mantine/dropzone      # File upload
npm install @mantine/spotlight     # Command palette
npm install @mantine/tiptap @tiptap/react @tiptap/pm @tiptap/starter-kit  # Rich text editor
```

## PostCSS Configuration

Create `postcss.config.cjs`:

```js
module.exports = {
  plugins: {
    "postcss-preset-mantine": {},
    "postcss-simple-vars": {
      variables: {
        "mantine-breakpoint-xs": "36em",
        "mantine-breakpoint-sm": "48em",
        "mantine-breakpoint-md": "62em",
        "mantine-breakpoint-lg": "75em",
        "mantine-breakpoint-xl": "88em",
      },
    },
  },
};
```

## App Setup

```tsx
// src/App.tsx
import "@mantine/core/styles.css";
// Other style imports as needed:
// import '@mantine/dates/styles.css';
// import '@mantine/notifications/styles.css';

import { MantineProvider, createTheme } from "@mantine/core";

const theme = createTheme({
  // Theme customization here
});

function App() {
  return <MantineProvider theme={theme}>{/* Your app */}</MantineProvider>;
}
```

## Critical Prohibitions

- Do NOT skip MantineProvider wrapper — all components require it
- Do NOT forget to import `@mantine/core/styles.css` — components won't style without it
- Do NOT mix Mantine with other UI libraries (e.g., Chakra, MUI) in same project
- Do NOT use inline styles for theme values — use CSS variables or theme object
- Do NOT skip PostCSS setup — responsive mixins won't work
- Do NOT forget `key={form.key('path')}` when using uncontrolled forms

## Core Concepts

### 1. MantineProvider

Wraps your app, provides theme context and color scheme management.

### 2. Theme Object

Customize colors, typography, spacing, component default props.

### 3. Style Props

All components accept style props like `mt`, `p`, `c`, `bg`, etc.

### 4. CSS Variables

All theme values exposed as CSS variables (e.g., `--mantine-color-blue-6`).

### 5. Polymorphic Components

Many components support `component` prop to render as different elements.

## Definition of Done

- [ ] MantineProvider wraps the app
- [ ] Styles imported (`@mantine/core/styles.css`)
- [ ] PostCSS configured with mantine-preset
- [ ] Theme customization in createTheme
- [ ] Color scheme (light/dark) handled
- [ ] TypeScript types working
- [ ] Tests pass with Vitest + custom render

## References (Detailed Guides)

### Setup & Configuration

- [getting-started.md](references/getting-started.md) — Installation, Vite setup, project structure
- [styling.md](references/styling.md) — MantineProvider, theme, CSS modules, style props, dark mode

### Core Features

- [components.md](references/components.md) — Core UI components patterns
- [hooks.md](references/hooks.md) — @mantine/hooks utility hooks
- [forms.md](references/forms.md) — @mantine/form, useForm, validation

### Development

- [testing.md](references/testing.md) — Vitest setup, custom render, mocking
- [eslint.md](references/eslint.md) — eslint-config-mantine setup

## Links

- Official docs: https://mantine.dev
- GitHub: https://github.com/mantinedev/mantine
- Vite template: https://github.com/mantinedev/vite-template
- ESLint config: https://github.com/mantinedev/eslint-config-mantine
- LLM docs: https://mantine.dev/llms.txt
