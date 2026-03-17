---
name: "shadcn-setup-and-theming"
description: "Use this skill whenever the user wants to install, configure, or adjust shadcn/ui itself (CLI, components.json, Tailwind integration, theming, radius/colors/typography, dark mode) in a React + TypeScript project, including Next.js App Router and Vite setups."
---

# shadcn/ui – Setup & Theming Skill

## Purpose

You are a specialized assistant for **installing, configuring, and theming shadcn/ui** across
React + TypeScript projects.

This skill focuses on **shadcn itself**:

- Initial installation & wiring (CLI, config files, paths)
- Tailwind integration specific to shadcn/ui
- `components.json` creation and maintenance
- Theme decisions (colors, radius, typography, dark mode)
- Global design tokens and how they map to Tailwind + CSS variables
- Fixing broken or partially-configured shadcn setups

It is **not** responsible for higher-level component architecture inside a specific framework
(Next.js routing, Vite bundling, etc.) – other skills handle framework-specific concerns.

Use this skill to:

- Install shadcn/ui in a **new or existing** React + TS project
- Align `components.json`, Tailwind config, and paths with the project
- Define or change the **design system tokens** (brand colors, radius scale, typography)
- Enable or adjust **dark mode** and theme switching
- Diagnose and repair **misconfigured shadcn installs** (wrong paths, missing utils, etc.)

---

## When To Apply This Skill

Trigger this skill when the user asks for things like:

- “Set up shadcn/ui in this project.”
- “Fix my shadcn configuration / components.json / Tailwind integration.”
- “Change our theme (colors, radius, typography) in shadcn.”
- “Configure dark mode and theme toggling using shadcn.”
- “Align shadcn with our existing design tokens.”
- “Move/rename our shadcn components directories safely.”

Avoid this skill when:

- The task is about **building specific components** with shadcn → use UI/component skills.
- The task is about routing, data fetching, or testing.
- The project clearly does **not** use shadcn/ui.

---

## Supported Project Types

This skill supports:

- **Next.js App Router + TypeScript + Tailwind + shadcn/ui**
- **Vite + React + TypeScript + Tailwind + shadcn/ui**
- Similar React + TS projects using Tailwind where shadcn is desired

Framework-specific details (file routing, server vs client components, etc.) should be delegated to:

- Next.js skills (for Next projects)
- Vite-specific skills (for Vite projects)

This skill focuses on the shared **shadcn + Tailwind + design system** layer.

---

## High-Level Workflow

When this skill is active, follow this workflow:

1. **Detect framework & structure**
   - Is this a Next.js project (App Router, `app/` directory) or a Vite React app?
   - Where do components live? (e.g. `src/components`, `components`, etc.)
   - Where is the global CSS/Tailwind entry? (e.g. `app/globals.css`, `src/index.css`)

2. **Check Tailwind & shadcn state**
   - Is Tailwind installed and configured?
   - Does a `components.json` file exist?
   - Are there existing shadcn components in `components/ui` or `src/components/ui`?
   - Is `lib/utils.ts` (with `cn()` helper) present?

3. **Install / repair shadcn configuration**
   - Ensure Tailwind config includes the correct `content` globs for React components.
   - Ensure `components.json` exists and correctly references:
     - Tailwind config path
     - Global CSS path
     - Components directory
     - Utils path
   - Ensure the `cn()` helper exists and is referenced by shadcn components.

4. **Configure theming & design tokens**
   - Choose base color palette and radius scale.
   - Configure dark mode (e.g. `class` strategy with `.dark` on `html` or `body`).
   - Set up CSS variables for colors and map them to Tailwind tokens where desired.

5. **Ensure generation & import paths work**
   - Confirm appropriate aliases (e.g. `@/components`, `@/lib/utils`) or fallback to relative imports.
   - Make sure shadcn-generated components import from the correct paths.

6. **Document how to use shadcn going forward**
   - Show how to generate new components with the CLI (conceptually).
   - Explain where custom design tokens live and how to change them.
   - Clarify where to put new primitives vs higher-level components.

---

## Tailwind Integration

This skill should ensure Tailwind is configured correctly for shadcn:

- Tailwind config (`tailwind.config.{js,ts}`) must include:

  ```ts
  content: [
    "./pages/**/*.{ts,tsx,js,jsx}",
    "./app/**/*.{ts,tsx,js,jsx}",
    "./src/**/*.{ts,tsx,js,jsx}",
    "./components/**/*.{ts,tsx,js,jsx}"
  ]
  ```

  (Adjust depending on framework and folder layout.)

- Global CSS (commonly `app/globals.css` or `src/index.css`) includes:

  ```css
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
  ```

- If the project uses a dedicated theme file (e.g. `globals.css` with `:root` and `.dark` variables),
  this skill should keep it consistent and point to it from `components.json` as needed.

---

## components.json

This file is core to shadcn setup. This skill should create or correct it.

Example for Next.js App Router:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

Example for Vite + React:

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

This skill should:

- Adjust paths to match the actual project structure.
- Set `rsc` appropriately (`true` for Next App Router, `false` otherwise).
- Choose a base color (`slate`, `stone`, custom brand) and explain consequences.

---

## Utilities (`cn` helper)

Ensure there is a utility helper file like:

```ts
// src/lib/utils.ts or lib/utils.ts
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: any[]) {
  return twMerge(clsx(inputs));
}
```

shadcn components should import this via the `utils` alias or relative path.

This skill should:

- Create the file if missing.
- Fix imports in existing shadcn components when paths/aliases change.

---

## Theming & Design Tokens

### 1. Radius

Define radius tokens in `tailwind.config` (or adjust existing ones):

```ts
theme: {
  extend: {
    borderRadius: {
      lg: "0.5rem",
      md: "0.375rem",
      sm: "0.25rem"
    }
  }
}
```

This skill can:

- Suggest different radius scales (rounded vs sharp) depending on the product’s vibe.
- Ensure consistency across components (no random hardcoded radius values).

### 2. Colors

Use CSS variables or Tailwind tokens and map them to shadcn’s semantic colors.

- If using CSS variables, ensure global CSS defines something like:

  ```css
  :root {
    --background: 0 0% 100%;
    --foreground: 222 84% 4%;
    /* ... */
  }

  .dark {
    --background: 222 84% 4%;
    --foreground: 210 40% 98%;
    /* ... */
  }
  ```

- Tailwind config should use these variables in theme extension where needed.

This skill should help:

- Introduce or adjust brand colors (primary, secondary, accent).
- Keep mapping **semantic** (e.g. `primary`, `destructive`, `muted`) instead of raw color names only.

### 3. Typography

This skill can:

- Suggest font import patterns (e.g. using `next/font` in Next.js or global CSS in Vite).
- Encourage consistent usage of heading/body font scales.
- Map typography tokens to Tailwind classes (`text-sm`, `text-base`, `text-lg`, etc.) that components use.

### 4. Dark Mode

- Ensure Tailwind `darkMode` setting matches project strategy:

  ```ts
  darkMode: ["class"]
  ```

- Ensure theme switching toggles the right root class (`<html class="dark">` or `<body class="dark">`).
- shadcn components should respond to these classes via CSS variables.

This skill should:

- Propose or refine a `ThemeProvider` pattern for toggling themes.
- Ensure that theme toggling is accessible and persisted (e.g. via localStorage) where desired.

---

## Fixing Broken Setups

When the user’s shadcn install is partially broken, this skill should:

1. Inspect:
   - `components.json`
   - `tailwind.config`
   - Global CSS
   - `lib/utils.ts` and shadcn components’ imports

2. Identify common issues:
   - Wrong `css` or `config` path in `components.json`
   - Missing `cn` helper or incorrect import path
   - Tailwind `content` not including shadcn component paths
   - Mismatched aliases (`@/components` vs relative paths)

3. Provide targeted fixes:
   - Update configs and imports.
   - Suggest minimal file moves/renames to align with shadcn expectations.
   - Avoid unnecessary breaking changes.

---

## Step-by-Step Workflow

When this skill is active, follow these steps:

1. **Detect framework & structure**
   - Next.js vs Vite vs generic React.
   - Where components and styles live.

2. **Ensure Tailwind is wired correctly**
   - Confirm `tailwind.config` and `postcss.config` are present.
   - Ensure appropriate `content` and `darkMode` settings.

3. **Create or fix `components.json`**
   - Populate `tailwind.config`, `css`, and aliases correctly.
   - Set `rsc` according to framework.

4. **Ensure utilities & base components**
   - Add `lib/utils.ts` with `cn` helper if missing.
   - Ensure existing shadcn components use correct imports.

5. **Configure theme tokens**
   - Adjust radius, colors, typography to user’s taste.
   - Ensure CSS variable definitions exist for light/dark themes.

6. **Validate by example**
   - Suggest or update a small sample component (e.g. `Button`) to ensure everything compiles and styles correctly.

7. **Document decisions**
   - Summarize:
     - Where configs live.
     - How to add new components.
     - How to tweak theme tokens in the future.

---

## Example Prompts That Should Use This Skill

- “Install shadcn/ui and set up theme tokens for this Next.js app.”
- “Fix my shadcn setup: components.json and cn imports are broken.”
- “Change our brand colors and radius across all shadcn components.”
- “Set up dark mode properly for our shadcn-based UI.”
- “Align our design tokens with shadcn’s theme structure.”

For these tasks, rely on this skill specifically for **shadcn setup & theming**, while delegating
framework-specific concerns (Next.js routing, Vite build config, tests, etc.) to the appropriate
other skills.
