---
name: frontend-tech-stack
description: Provides standards for the frontend application technology stack. This skill should be used when setting up new frontend projects or upgrading existing ones with React 19, Vite, and Tailwind v4.
---

# Frontend Tech Stack

This skill defines the standard technology stack for all frontend applications (`erify_creators`, `erify_studios`, etc.) in the project.

## Core Core Technologies

| Category        | Technology          | Version  | Notes                                     |
| :-------------- | :------------------ | :------- | :---------------------------------------- |
| **Framework**   | **React**           | **19.x** | Use functional components and hooks.      |
| **Build Tool**  | **Vite**            | **7.x**  | Fast HMR, uses `@vitejs/plugin-react`.    |
| **Styling**     | **Tailwind CSS**    | **4.x**  | Use the `@tailwindcss/vite` plugin.       |
| **Routing**     | **TanStack Router** | **1.x**  | File-based routing, type-safe navigation. |
| **State/Query** | **TanStack Query**  | **5.x**  | For async server state management.        |
| **I18n**        | **Paraglide JS**    | **2.x**  | Type-safe internationalization.           |

## Project Structure

Frontend apps should follow this structure:

```
src/
├── routes/             # TanStack Router file-based routes
│   ├── __root.tsx      # Root layout
│   ├── index.tsx       # Homepage
│   └── feature.tsx     # Feature route
├── features/           # Feature-based modules (see below)
├── components/         # Shared components used across features
├── hooks/              # Shared hooks used across features
├── lib/                # Utilities and API clients
├── stores/             # Global state stores
├── types/              # Shared types
├── main.tsx            # Entry point
└── index.css           # Global styles (Tailwind imports)
```

### Feature-Based Architecture

For scalability and maintainability, organize most code within the `features/` folder. Each feature should be **self-contained** with its own components, hooks, API calls, and types.

**Feature Structure**:

```
src/features/awesome-feature/
├── api/                # API calls specific to this feature
│   ├── get-items.ts
│   └── create-item.ts
├── components/         # Components used only in this feature
│   ├── ItemList.tsx
│   └── ItemForm.tsx
├── hooks/              # Hooks specific to this feature
│   └── useItemFilters.ts
├── stores/             # State stores for this feature (if needed)
│   └── item-store.ts
├── types/              # TypeScript types for this feature
│   └── item.types.ts
└── utils/              # Utility functions for this feature
    └── format-item.ts
```

**Key Principles**:

1. **Colocation**: Keep related code together. If a component is only used in one feature, it belongs in that feature's `components/` folder, not the global one.

2. **No Cross-Feature Imports**: Features should not import from each other. Instead, compose features at the application level (in routes or app-level components).

3. **Shared Code**: Only code used by multiple features should live in the global folders (`src/components/`, `src/hooks/`, etc.).

**Preventing Cross-Feature Imports**:

Add this ESLint rule to enforce feature isolation:

```javascript
// .eslintrc.cjs
'import/no-restricted-paths': [
  'error',
  {
    zones: [
      // Prevent features from importing from each other
      {
        target: './src/features/auth',
        from: './src/features',
        except: ['./auth'],
      },
      {
        target: './src/features/dashboard',
        from: './src/features',
        except: ['./dashboard'],
      },
      // Add more features as needed
    ],
  },
],
```

## Configuration

### Vite Config ("vite.config.ts")

Ensures Tailwind v4 and TanStack Router integration:

```typescript
import tailwindcss from '@tailwindcss/vite';
import { tanstackRouter } from '@tanstack/router-plugin/vite';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [
    tanstackRouter(),
    react(),
    tailwindcss(),
  ],
});
```

### Tailwind Config (v4)

Tailwind v4 uses CSS-first configuration. Your `index.css` should look like:

```css
@import "tailwindcss";

@theme {
  --font-sans: "Inter", sans-serif;
  /* Define custom tokens here */
}
```

## Checklist

- [ ] Project is initialized with Vite + React + TypeScript.
- [ ] Uses Tailwind CSS v4 plugin.
- [ ] Uses TanStack Router for navigation.
- [ ] Depends on workspace packages (`@eridu/ui`, `@eridu/api-types`) where appropriate.
