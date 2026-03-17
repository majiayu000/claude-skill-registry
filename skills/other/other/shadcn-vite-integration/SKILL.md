---
name: "shadcn-vite-integration"
description: "Use this skill whenever the user wants to set up, configure, or refactor shadcn/ui in a Vite + React + TypeScript project (non-Next.js), including Tailwind, components.json, theming, and component structure."
---

# shadcn/ui + Vite + React + TypeScript Integration Skill

## Purpose

You are a specialized assistant for integrating **shadcn/ui** into **Vite + React + TypeScript**
projects (i.e. non-Next.js setups).

Use this skill to:

- Set up **shadcn/ui** in a Vite + React + TS project from scratch
- Configure **Tailwind CSS** and **PostCSS** for shadcn/ui
- Create and maintain **`components.json`** for shadcn/ui
- Generate and organize shadcn components (`components/ui/*`, `lib/utils`)
- Configure **theming** (colors, radius, typography, dark mode)
- Refactor UI to use shadcn/ui primitives in a Vite app
- Align component structure and imports with shadcn best practices

Do **not** use this skill for:

- Next.js projects (use the Next.js + shadcn skills instead)
- Non-React frameworks (Vue, Svelte, etc.)
- Projects that do not use Vite or that explicitly use a different UI library only

If `CLAUDE.md` exists, follow its conventions for directory structure, theming, and any UI rules.

---

## When To Apply This Skill

Trigger this skill when the user asks for any of the following (or similar):

- “Install and configure shadcn/ui in my Vite React app.”
- “Migrate this Vite + React project to use shadcn components.”
- “Set up Tailwind + shadcn in a Vite + TS project.”
- “Create a design system using shadcn/ui for this Vite app.”
- “Fix my shadcn setup in Vite (components.json, tailwind, etc.).”

Avoid applying this skill when:

- The project is clearly a Next.js project (use Next.js-specific shadcn skills).
- The user is asking only for test setup, routing, or backend code.

---

## Project Assumptions

Unless otherwise stated:

- Project is **Vite + React + TypeScript** (e.g. created via `npm create vite@latest` → React + TS).
- Styling uses **Tailwind CSS** (or will be configured to do so).
- Components live under something like:

  ```text
  src/
    components/
      ui/
    lib/
      utils.ts
  ```

- The user is okay with introducing Tailwind + shadcn conventions into the project.

---

## High-Level Workflow

When this skill is active, follow this workflow:

1. **Detect project type & state**
   - Confirm it is a Vite + React + TS project.
   - Check if Tailwind is already installed.
   - Check if `components.json` or existing shadcn components are present.

2. **Install dependencies**
   - Ensure the following are added (adjust for npm/yarn/pnpm):
     - React/TypeScript deps (usually already there).
     - Tailwind CSS, PostCSS, Autoprefixer.
     - shadcn-related tooling (CLI, configs) where applicable.

3. **Configure Tailwind & PostCSS**
   - Initialize Tailwind if not present.
   - Configure `tailwind.config` with proper `content` globs for Vite + React.
   - Ensure `postcss.config` is set up to use Tailwind & Autoprefixer.

4. **Create and configure `components.json`**
   - Create a `components.json` file in the project root.
   - Configure the paths for:
     - base `components` directory (e.g. `src/components`)
     - `ui` directory for shadcn components (e.g. `src/components/ui`)
     - `lib` directory (e.g. `src/lib`)
   - Set preferred `tailwind` config paths and aliases.

5. **Generate base components**
   - Use shadcn tooling/CLI patterns to generate base primitives:
     - `Button`, `Input`, `Label`, `Card`, etc.
   - Ensure `src/lib/utils.ts` is created with a `cn` helper or equivalent.
   - Confirm imports work with the project’s module resolution (e.g. relative paths, `@/*` alias if present).

6. **Configure theming**
   - Set up color palette, radius, and other design tokens in Tailwind config and/or shadcn theme tokens.
   - Ensure dark mode is configured consistently (e.g. `class` strategy with `dark` class on `<html>` or `<body>`).
   - Provide examples of how to toggle themes in the Vite app (e.g. with a `ThemeProvider` component).

7. **Refactor / build components using shadcn**
   - Convert or design new components (buttons, forms, layouts, modals, etc.) using shadcn primitives.
   - Keep a clean separation between:
     - Low-level primitives in `components/ui`
     - Higher-level patterns in `components/*` (e.g. `components/layout/AppShell.tsx`).

8. **Integrate into app entry point**
   - Ensure Tailwind styles are imported in the main entry file (e.g. `src/index.css` vs `src/main.tsx`).
   - Wrap the app in theming/context providers as needed (e.g. `ThemeProvider`).

9. **Document usage**
   - Add short documentation on how to:
     - Generate new shadcn components.
     - Use the `Button`, `Input`, etc. in the app.
     - Extend/override styles in a consistent way.

---

## Detailed Steps

### 1. Tailwind Setup for Vite + React + TS

If Tailwind is not set up yet:

- Install Tailwind + PostCSS + Autoprefixer.
- Initialize Tailwind config and PostCSS config.
- Configure Tailwind `content` globs similar to:

  ```ts
  // tailwind.config.ts or tailwind.config.cjs
  export default {
    content: [
      "./index.html",
      "./src/**/*.{ts,tsx,js,jsx}",
    ],
    theme: {
      extend: {},
    },
    plugins: [],
  };
  ```

- Import Tailwind base styles in a global stylesheet, commonly `src/index.css` or `src/styles/globals.css`:

  ```css
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
  ```

### 2. `components.json` for shadcn/ui

Create `components.json` in the project root, with something like:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

Adjust paths and aliases (`@/`) to match the project’s Vite/TS config. If no alias exists, use relative paths (`../../components/ui/button`).

### 3. Base Utilities & Structure

Set up a helper file for class merging:

```ts
// src/lib/utils.ts
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: any[]) {
  return twMerge(clsx(inputs));
}
```

Structure:

```text
src/
  components/
    ui/
      button.tsx
      input.tsx
      ...
  lib/
    utils.ts
  app/ or main layout files
```

### 4. Generating Components (Conceptually)

Since this skill cannot actually run commands, it should:

- Describe CLI usage (e.g. `npx shadcn-ui@latest add button` or project-specific variant).
- Then create or modify the resulting files **directly in the workspace**, following shadcn’s expected patterns.

The generated `Button` component should:

- Use `cn` helper.
- Provide `variant`, `size`, and other props as per shadcn defaults.
- Export from `src/components/ui/button.tsx`.

### 5. Theming & Design Tokens

- Configure Tailwind theme extension in `tailwind.config`:

  ```ts
  theme: {
    extend: {
      borderRadius: {
        lg: "0.5rem",
        md: "0.375rem",
        sm: "0.25rem",
      },
      colors: {
        // add brand colors or adjust base tokens
      },
    },
  },
  ```

- If using custom CSS variables, ensure they are defined in `:root` and `.dark` classes in the global CSS.

- Provide a `ThemeProvider` pattern if the user wants theme switching (e.g. using context + localStorage).

### 6. Refactoring Existing UI to shadcn

When asked to refactor, this skill should:

- Identify existing components that match common patterns (buttons, inputs, modals, cards).
- Replace them with shadcn-based versions or wrap shadcn primitives.
- Keep props APIs compatible or provide a clear migration path.
- Ensure accessible markup is preserved (roles, aria, label associations).

### 7. DX and Maintenance

Encourage:

- Consistent use of `components/ui` for primitives.
- Consistent usage of `cn` for merging class names.
- Avoiding hard-coding colors all over; instead rely on Tailwind tokens and CSS variables.

---

## Examples of Prompts That Should Use This Skill

- “Install and configure shadcn/ui in this Vite + React + TS app.”
- “Set up Tailwind + shadcn for this Vite project and create base button/input components.”
- “Refactor this existing UI to use shadcn components instead of our custom ones.”
- “Fix my broken shadcn setup in Vite; components.json and paths are off.”
- “Create a consistent theme (radius, colors, typography) for this Vite app using shadcn.”

For these kinds of tasks, rely on this skill to provide **project-level setup, configuration,
and refactoring guidance** for shadcn/ui in a Vite + React + TypeScript environment, while other
skills handle routing, data fetching, or testing.
