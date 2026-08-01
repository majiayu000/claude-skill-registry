---
name: react-app-structure
description: Use when auditing, scaffolding, or validating MetaSaver React portal
  app directory structure. Includes file organization patterns, domain grouping, feature
  composition, routing configuration, and Auth
---

---
name: react-app-structure
description: Use when auditing, scaffolding, or validating MetaSaver React portal app directory structure. Includes file organization patterns, domain grouping, feature composition, routing configuration, and Auth0 integration setup. File types: .tsx, .ts, directory layouts.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# React App Structure for MetaSaver Portal Apps

## Purpose

This skill documents the complete file and folder organization for MetaSaver React portal applications (admin-portal, service-catalog, datafeedr). It ensures consistent patterns across:

- Directory hierarchy by domain/feature
- Config file placement and exports
- Library composition (auth, API clients)
- Page-to-feature mapping
- Type-safe routing
- Component composition patterns

**Use when:**

- Scaffolding a new MetaSaver portal app
- Auditing an existing app structure for compliance
- Adding new features/domains to an app
- Validating page-feature alignment
- Setting up Auth0 or API client integration

## Directory Structure Reference

### Root Configuration Files

These are handled by specialized config agents - reference them:

```
├── vite.config.ts              # (vite-agent) Vite build config
├── tsconfig.json               # (typescript-configuration-agent) Base TS config
├── tsconfig.app.json           # (typescript-configuration-agent) App-specific
├── tsconfig.node.json          # (typescript-configuration-agent) Node config
├── tailwind.config.ts          # (tailwind-agent) Tailwind setup
├── postcss.config.js           # (postcss-agent) PostCSS config
├── eslint.config.js            # (eslint-agent) ESLint config
├── package.json                # (root-package-json-agent) Dependencies
├── index.html                  # Entry HTML file
└── .env.example                # Environment variable template
```

### Public Folder

```
public/
└── favicon.svg                 # Browser tab icon ONLY
                                # Always place full logo in src/assets/logo.svg
```

**Rule:** `public/` contains favicon.svg for browser tab. Logo goes in `src/assets/logo.svg`.

### Source Structure (Complete)

```
src/
├── assets/
│   └── logo.svg                # Full logo for in-app use (NOT favicon)
│
├── config/
│   ├── index.tsx               # siteConfig, menuItems exports
│   └── auth-config.ts          # Auth0 configuration (MUST be in config/, NOT lib/)
│
├── hooks/                      # (optional) App-wide hooks only (e.g., impersonation)
│   └── use-impersonation.ts    # Named export pattern
│
├── lib/
│   └── api-client.ts           # Axios client with auth token injection ONLY
│
├── features/
│   └── {domain}/               # Grouped by domain (mirrors pages/)
│       └── {feature}/
│           ├── {feature}.tsx   # Main feature component (named export)
│           ├── components/     # (optional) Reusable sub-components
│           │   └── {component}.tsx  # Each component in own file
│           ├── hooks/          # (optional) Feature-specific hooks
│           │   └── use-{hook}.ts    # Each hook in own file
│           ├── config/         # (optional) Feature-specific config
│           │   └── config.ts   # Named exports
│           └── queries/        # (optional) API query functions
│               └── {entity}-queries.ts  # Query functions
│
├── pages/
│   └── {domain}/               # Grouped by domain (mirrors features/)
│       └── {page}.tsx          # Thin wrapper importing from features/
│   └── theme/
│       └── theme.tsx           # Theme component (named export)
│
├── routes/
│   ├── route-types.ts          # Type-safe ROUTES constant
│   └── routes.tsx              # React Router config with lazy loading
│
├── styles/
│   └── theme-overrides.css     # CSS overrides (global)
│
├── app.tsx                     # Root component with Auth0Provider
├── main.tsx                    # React entry point (ReactDOM.createRoot)
├── index.css                   # Tailwind imports (@tailwind directives)
└── vite-env.d.ts               # Vite type definitions
```

**IMPORTANT - File structure requirements:**

- Always use `@metasaver/{app}-contracts` packages for types - do not create `src/types/`
- Always place auth config in `src/config/` - do not put auth-config.ts in `src/lib/`

## File Organization Rules

### Features Directory Pattern

**Rule 1: Domain Grouping**
Features are organized by domain to match page structure:

```
features/
├── microservices-feature/      # Maps to pages/service-catalog/micro-services.tsx
├── endpoints-feature/          # Maps to pages/service-catalog/endpoints.tsx
├── merchants-feature/          # Maps to pages/datafeedr/merchants.tsx
└── status-feature/             # Maps to pages/datafeedr/status.tsx
```

**Rule 2: Use Direct Imports**
Always import directly from specific files using `#/` alias for internal imports:

```typescript
// CORRECT - Import from specific files with full paths
import { MicroservicesFeature } from "#/features/microservices-feature/microservices.tsx";
import { useGetServices } from "#/features/microservices-feature/hooks/use-get-services.ts";
import { ServiceCard } from "#/features/microservices-feature/components/service-card.tsx";
```

**Rule 3: Component Naming**

- Main component filename matches feature: `microservices.tsx`
- Main component export: `export function MicroservicesFeature() { ... }`
- Sub-components in `components/` subfolder with descriptive names
- Use named exports only (no default exports)

**Rule 4: Optional Subfolders**
Only create `components/`, `hooks/`, `config/`, `queries/` if needed:

- No empty folders
- Each file has specific purpose and named exports
- `queries/` contains API query functions (e.g., `{entity}-queries.ts`)
- Deep nesting (3+ levels) suggests refactoring needed

### Pages Directory Pattern

**Rule 1: Mirrors Features**
Page structure mirrors feature structure by domain:

```
pages/
├── service-catalog/
│   ├── micro-services.tsx
│   ├── endpoints.tsx
│   └── schedule.tsx
├── datafeedr/
│   ├── merchants.tsx
│   ├── networks.tsx
│   ├── products.tsx
│   └── status.tsx
└── home/
    └── home.tsx
```

**Rule 2: Thin Wrappers**
Page files are thin wrappers (5-15 lines) with direct imports:

```typescript
// src/pages/service-catalog/micro-services.tsx
import { MicroservicesFeature } from "#/features/microservices-feature/microservices.tsx";

export function MicroServicesPage() {
  return <MicroservicesFeature />;
}
```

**Rule 3: Keep Pages Thin**

- Always import from features using `#/` alias
- Ensure pages contain NO business logic
- Ensure pages have NO their own hooks/components
- Exception: Page-level wrappers (auth guards, layouts)

**Rule 4: Import Order**
Follow standard import order in all files:

```typescript
// 1. Node.js built-ins (rare in React apps)
import { resolve } from "path";

// 2. External packages
import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";

// 3. Workspace packages (external imports)
import type { User } from "@metasaver/contracts/users/types";

// 4. Internal imports (same package)
import { MicroservicesFeature } from "#/features/microservices-feature/microservices.tsx";
import { useAuth } from "#/hooks/use-auth.ts";
```

### Config Directory Pattern

**index.tsx** exports:

```typescript
export const siteConfig = {
  name: "Admin Portal",
  description: "...",
  // ...
};

export const menuItems = [
  // Navigation structure
];
```

**auth-config.ts** exports:

```typescript
export const auth0Config = {
  domain: process.env.VITE_AUTH0_DOMAIN,
  clientId: process.env.VITE_AUTH0_CLIENT_ID,
  // ...
};
```

### Routes Pattern

**route-types.ts** defines type-safe routes:

```typescript
export const ROUTES = {
  HOME: "/",
  DASHBOARD: "/dashboard",
  MICROSERVICES: "/service-catalog/microservices",
  // ...
} as const;
```

**routes.tsx** uses lazy loading with named exports:

```typescript
import { lazy } from "react";
import { createBrowserRouter } from "react-router-dom";

const HomePage = lazy(() =>
  import("#/pages/home/home.tsx").then((m) => ({
    default: m.HomePage,
  }))
);

const MicroServicesPage = lazy(() =>
  import("#/pages/service-catalog/micro-services.tsx").then((m) => ({
    default: m.MicroServicesPage,
  }))
);

export const router = createBrowserRouter([
  {
    path: ROUTES.HOME,
    element: <HomePage />,
  },
  {
    path: ROUTES.MICROSERVICES,
    element: <MicroServicesPage />,
  },
  // ...
]);
```

### Styles Organization

**theme-overrides.css** contains:

- CSS custom properties overrides
- Global component styles
- Utility classes not in Tailwind

Does NOT contain:

- Component-scoped styles (use Tailwind classes in JSX)
- Animations (inline or separate component files)

## Workflow: Scaffolding New Feature

1. **Create Feature Directory**

   ```bash
   mkdir -p src/features/{domain}/{feature}
   mkdir -p src/features/{domain}/{feature}/components
   mkdir -p src/features/{domain}/{feature}/hooks
   mkdir -p src/features/{domain}/{feature}/config
   ```

2. **Create Feature Files** (use templates)
   - `src/features/{domain}/{feature}/{feature}.tsx` - Main feature component with named export
   - `src/features/{domain}/{feature}/components/{component}.tsx` - Component files as needed
   - `src/features/{domain}/{feature}/hooks/use-{hook}.ts` - Hook files as needed
   - `src/features/{domain}/{feature}/config/config.ts` - Config file as needed

3. **Create Page File** (use template)
   - `src/pages/{domain}/{page}.tsx` - Import feature using `#/` alias

4. **Update Routes**
   - Add ROUTES constant in `src/routes/route-types.ts`
   - Add route config in `src/routes/routes.tsx` with lazy loading
   - Add to `menuItems` in `src/config/index.tsx`

5. **Ensure Import Order**
   - Node.js built-ins → External packages → Workspace packages → Internal imports (`#/`)

## Audit Checklist

### Directory Structure

- [ ] `src/` folder exists
- [ ] All required subdirectories present: `assets`, `config`, `lib`, `features`, `pages`, `routes`, `styles`
- [ ] Optional subdirectory: `hooks/` (only for app-wide hooks like impersonation)
- [ ] Always use contracts packages for types - ensure no `src/types/` folder
- [ ] Keep root `src/` clean - only have `app.tsx`, `main.tsx`, `index.css`, `vite-env.d.ts`
- [ ] `public/` contains only `favicon.svg` (place full logo in `src/assets/logo.svg`)

### Features Directory

- [ ] Features grouped by domain: `features/{domain}/{feature}/`
- [ ] Main component: `{feature}.tsx` in feature root with named export
- [ ] Sub-components in `components/` with descriptive names (if exists)
- [ ] Hooks in `hooks/` folder with `use-` prefix
- [ ] Always use direct exports - ensure no `index.ts` barrel files
- [ ] No empty folders
- [ ] Feature names use kebab-case: `microservices-feature`
- [ ] Always use `#/` alias for internal paths

### Pages Directory

- [ ] Pages mirror feature structure: `pages/{domain}/{page}.tsx`
- [ ] Page files are thin wrappers (< 20 lines)
- [ ] Always import from features using `#/` alias
- [ ] Ensure pages contain no business logic
- [ ] Ensure no sub-components in pages folder
- [ ] Page export: `export function {Page}Page()` (named export only)
- [ ] Always follow correct import order: external packages → workspace packages → internal (`#/`)

### Config Files

- [ ] `src/config/index.tsx` exports `siteConfig` and `menuItems`
- [ ] `src/config/auth-config.ts` exports `auth0Config` object
- [ ] Always use environment variables for config
- [ ] Always keep API URLs and secrets out of code

### Library Files

- [ ] `src/lib/api-client.ts` exports configured Axios instance
- [ ] API client injects auth token automatically
- [ ] Client handles errors consistently

### Routes

- [ ] `src/routes/route-types.ts` defines `ROUTES` constant
- [ ] All routes in `ROUTES` are type-safe
- [ ] `src/routes/routes.tsx` uses lazy loading for pages
- [ ] Routes match navigation items in config
- [ ] No hardcoded URL strings in components

### Styles

- [ ] `src/styles/theme-overrides.css` contains only overrides
- [ ] Global styles imported in `src/index.css`
- [ ] Tailwind `@tailwind` directives present in `src/index.css`
- [ ] PostCSS configured in `postcss.config.js`

### Root Source Files

- [ ] `src/app.tsx` wraps with Auth0Provider
- [ ] `src/main.tsx` uses `ReactDOM.createRoot()`
- [ ] `src/index.css` imports Tailwind
- [ ] `src/vite-env.d.ts` declares Vite types
- [ ] `index.html` references `src/main.tsx`

### Asset Organization

- [ ] `src/assets/logo.svg` contains full logo
- [ ] `public/favicon.svg` contains browser tab icon ONLY
- [ ] Ensure no duplicate icon files
- [ ] Always import logo in config/layout files

## Common Violations & Fixes

**Violation:** Pages contain business logic

```typescript
// INCORRECT
export function MicroServicesPage() {
  const [services, setServices] = useState([]);
  useEffect(() => { /* fetch logic */ }, []);
  return <ServiceTable services={services} />;
}
```

**Fix:** Move logic to feature component

```typescript
// CORRECT - Page wrapper
export function MicroServicesPage() {
  return <MicroservicesFeature />;
}

// Feature component has logic
export function MicroservicesFeature() {
  const [services, setServices] = useState([]);
  useEffect(() => { /* fetch logic */ }, []);
  return <ServiceTable services={services} />;
}
```

**Violation:** Using barrel exports (index.ts files)

```typescript
// INCORRECT - Barrel export pattern
src/features/microservices-feature/
├── index.ts                    // export * from "./microservices"
├── microservices.tsx
├── hooks/
│   ├── index.ts               // export * from "./use-get-services"
│   └── use-get-services.ts

// INCORRECT - Import from barrel
import { MicroservicesFeature } from "#/features/microservices-feature";
```

**Fix:** Use direct imports with `#/` alias

```typescript
// CORRECT - No index.ts files, use direct imports
src/features/microservices-feature/
├── microservices.tsx
└── hooks/
    └── use-get-services.ts

// CORRECT - Direct import with full path
import { MicroservicesFeature } from "#/features/microservices-feature/microservices.tsx";
import { useGetServices } from "#/features/microservices-feature/hooks/use-get-services.ts";
```

**Violation:** Page structure doesn't mirror feature structure

```
features/microservices-feature/        pages/dashboard/
pages/admin/microservices.tsx   ✗      (mismatch in domain/path)
```

**Fix:** Align domain structure

```
features/service-catalog/microservices-feature/
pages/service-catalog/micro-services.tsx   ✓
```

**Violation:** Config file hardcoding values

```typescript
// INCORRECT
export const auth0Config = {
  domain: "dev-abc123.auth0.com",
  clientId: "xyz789",
};
```

**Fix:** Use environment variables

```typescript
// CORRECT
export const auth0Config = {
  domain: import.meta.env.VITE_AUTH0_DOMAIN,
  clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
};
```

## Examples

### Example 1: Audit Admin Portal Structure

```bash
# Commands to validate structure
find src -type f -name "*.tsx" -o -name "*.ts" | head -20
ls -la src/features/
ls -la src/pages/
```

Audit checklist:

1. All features have `index.ts`
2. All pages are thin wrappers
3. Routes match config menu items
4. No business logic in pages

### Example 2: Add New Feature (DataFeedr Products)

**Files to create:**

1. `src/features/datafeedr/products-feature/index.ts`
2. `src/features/datafeedr/products-feature/products.tsx`
3. `src/features/datafeedr/products-feature/hooks/index.ts`
4. `src/features/datafeedr/products-feature/hooks/use-get-products.ts`
5. `src/pages/datafeedr/products.tsx`
6. Update `src/routes/route-types.ts`
7. Update `src/routes/routes.tsx`
8. Update `src/config/index.tsx` menuItems

**Use templates for each file.**

### Example 3: Validate Page-Feature Alignment

```typescript
// Check that pages import from matching features using #/ alias
// src/pages/service-catalog/micro-services.tsx
import { MicroservicesFeature } from "#/features/service-catalog/microservices-feature/microservices.tsx";

// Domain must match: service-catalog / service-catalog ✓
// Feature path must match: microservices-feature / microservices-feature ✓
// Import uses #/ alias ✓
// Import includes full file path with extension ✓
```

## Related Skills

- **vite-agent** - Vite configuration (vite.config.ts)
- **typescript-configuration-agent** - TypeScript config (tsconfig.json, tsconfig.app.json)
- **tailwind-agent** - Tailwind setup (tailwind.config.ts)
- **postcss-agent** - PostCSS config (postcss.config.js)
- **eslint-agent** - ESLint config (eslint.config.js)
- **root-package-json-agent** - Dependencies (package.json)
- **auth0-integration** - Auth0 setup patterns
- **react-routing** - React Router patterns
