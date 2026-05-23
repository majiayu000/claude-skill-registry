---
name: tooling-setup
description: Configure Vite, TypeScript, Biome, and Vitest for React 19 projects. Covers build configuration, strict TypeScript setup, linting/formatting, and testing infrastructure. Use when setting up new projects or updating tool configurations.
---

# Tooling Setup for React 19 Projects

Production-ready configuration for modern frontend tooling with Vite, TypeScript, Biome, and Vitest.

## 1. Vite + React 19 + React Compiler

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    react({
      babel: {
        // React Compiler must run first:
        plugins: ['babel-plugin-react-compiler'],
      },
    }),
  ],
})
```

**Verify:** Check DevTools for "Memo ✨" badge on optimized components.

## 2. TypeScript (strict + bundler mode)

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noFallthroughCasesInSwitch": true,
    "types": ["vite/client", "vitest"]
  },
  "include": ["src", "vitest-setup.ts"]
}
```

**Key Settings:**
- `moduleResolution: "bundler"` - Optimized for Vite
- `strict: true` - Enable all strict type checks
- `noUncheckedIndexedAccess: true` - Safer array/object access
- `verbatimModuleSyntax: true` - Explicit import/export

## 3. Biome (formatter + linter)

```bash
npx @biomejs/biome init
npx @biomejs/biome check --write .
```

```json
// biome.json
{
  "formatter": { "enabled": true, "lineWidth": 100 },
  "linter": {
    "enabled": true,
    "rules": {
      "style": { "noUnusedVariables": "error" }
    }
  }
}
```

**Usage:**
- `npx biome check .` - Check for issues
- `npx biome check --write .` - Auto-fix issues
- Replaces ESLint + Prettier with one fast tool

## 4. Environment Variables

- Read via `import.meta.env`
- Prefix all app-exposed vars with `VITE_`
- Never place secrets in the client bundle

```typescript
// Access environment variables
const apiUrl = import.meta.env.VITE_API_URL
const isDev = import.meta.env.DEV
const isProd = import.meta.env.PROD

// .env.local (not committed)
VITE_API_URL=https://api.example.com
VITE_ANALYTICS_ID=UA-12345-1
```

## 5. Testing Setup (Vitest)

```typescript
// vitest-setup.ts
import '@testing-library/jest-dom/vitest'

// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./vitest-setup.ts'],
    coverage: { reporter: ['text', 'html'] }
  }
})
```

**Setup Notes:**
- Use React Testing Library for DOM assertions
- Use MSW for API mocks (see **tanstack-query** skill for MSW patterns)
- Add `types: ["vitest", "vitest/jsdom"]` for jsdom globals in tsconfig.json

**Run Tests:**
```bash
npx vitest                    # Run in watch mode
npx vitest run               # Run once
npx vitest --coverage        # Generate coverage report
```

## Package Installation

```bash
# Core
pnpm add react@rc react-dom@rc
pnpm add -D vite @vitejs/plugin-react typescript

# Biome (replaces ESLint + Prettier)
pnpm add -D @biomejs/biome

# React Compiler
pnpm add -D babel-plugin-react-compiler

# Testing
pnpm add -D vitest @testing-library/react @testing-library/jest-dom
pnpm add -D @testing-library/user-event jsdom
pnpm add -D msw

# TanStack
pnpm add @tanstack/react-query @tanstack/react-router
pnpm add -D @tanstack/router-plugin @tanstack/react-query-devtools

# Utilities
pnpm add axios zod
```

## Project Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest --coverage",
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "format": "biome format --write ."
  }
}
```

## IDE Setup

**VSCode Extensions:**
- Biome (biomejs.biome)
- TypeScript (built-in)
- Vite (antfu.vite)

**VSCode Settings:**
```json
{
  "editor.defaultFormatter": "biomejs.biome",
  "editor.formatOnSave": true,
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "biomejs.biome"
  }
}
```

## Related Skills

- **core-principles** - Project structure and best practices
- **react-patterns** - React 19 specific features
- **testing-strategy** - Advanced testing patterns with MSW
