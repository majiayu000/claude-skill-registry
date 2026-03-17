---
name: dev-web
description: Create and manage modern React web applications using Bun, Vite, React 19, Tailwind CSS 4, and shadcn/ui. Use this skill when the user asks to build a frontend, a web app, or modify UI components.
metadata:
  author: Yuga Sun
  version: "2026.01.29"
---

# Web Development Skill

## Instructions

Use this skill to scaffold and maintain web frontend projects in the `web/` directory. Follow the stack preferences and configuration details below.

### Quick Start

1.  **Initialize**: Use `bun create vite web --template react-ts`.
2.  **Install**: `bun install`.
3.  **Styling**: Configure Tailwind CSS 4.
4.  **Components**: Initialize `shadcn/ui`.

## Core Stack preferences

### Package Manager & Runtime (Bun)

Use **Bun** as the primary package manager and runtime.

| Command | Description |
|---------|-------------|
| `bun install` | Install dependencies |
| `bun add <pkg>` | Add dependency |
| `bun add -d <pkg>` | Add dev dependency |
| `bun run dev` | Start development server |

### Project Location

The web frontend project should be initialized in the `web/` directory.

### Framework & Build (Vite + React 19)

Use **Vite** with **React 19** and **TypeScript 5**.

To create a new project:
```bash
bun create vite web --template react-ts
```

### Styling (Tailwind CSS 4)

Use **Tailwind CSS v4**.

-   Install using the Vite plugin: `@tailwindcss/vite` and `tailwindcss`.
-   Use the CSS-first configuration approach where possible (`@import "tailwindcss";`).

Installation:
```bash
bun add tailwindcss@next @tailwindcss/vite
```

### UI Library (shadcn/ui 3)

Use **shadcn/ui v3** for the component system.

-   Initialize with `bunx --bun shadcn@latest init`.
-   Configure `components.json` to resolve paths correctly (e.g., `@/components`, `@/lib/utils`).
-   Use `bunx --bun shadcn@latest add <component>` to add components.

### Data & Routing (TanStack)

Use the **TanStack** suite for complex app needs:

-   **@tanstack/react-query**: For async state management.
-   **@tanstack/react-router**: For type-safe routing.

Installation:
```bash
bun add @tanstack/react-query @tanstack/react-router
```

---

## Configuration Details

### TypeScript

Ensure `tsconfig.json` is set to strict mode.

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "jsx": "react-jsx",
    "noEmit": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Vite Configuration

Update `vite.config.ts` to include the Tailwind CSS 4 plugin and path aliases.

```ts
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import path from "node:path"
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
```

### Global CSS

In `src/index.css`:

```css
@import "tailwindcss";

/* Configuration for shadcn/ui CSS variables should be added here if not automatically handled by the CLI init */
```

---

## References

### Styling & Theming

| Topic | Description | Reference |
|-------|-------------|-----------|
| Theming System | CSS variables, Dark mode, and Tailwind v4 configuration | [theme](references/theme.md) |


