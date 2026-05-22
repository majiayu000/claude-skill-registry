---
description: Set up Vue+Vite+TypeScript monorepo workspace with pnpm for NovaTune frontend (project)
---
# Setup Vue Workspace Skill

Create the NovaTune frontend workspace with Vue 3, Vite, TypeScript, and pnpm workspaces.

## Overview

This skill scaffolds `src/NovaTuneClient/` as a pnpm monorepo containing:
- `apps/player` - Listener experience SPA
- `apps/admin` - Admin dashboard SPA
- `packages/api-client` - OpenAPI-generated TypeScript client
- `packages/core` - Shared auth, HTTP, telemetry, errors
- `packages/ui` - Shared Vue components and design system

## Workspace Structure

```
src/NovaTuneClient/
├── package.json
├── pnpm-workspace.yaml
├── tsconfig.base.json
├── .env.example
├── .eslintrc.cjs
├── .prettierrc
├── apps/
│   ├── player/
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   ├── tsconfig.json
│   │   ├── index.html
│   │   └── src/
│   │       ├── main.ts
│   │       ├── App.vue
│   │       ├── router/
│   │       ├── stores/
│   │       ├── features/
│   │       ├── layouts/
│   │       └── composables/
│   └── admin/
│       ├── package.json
│       ├── vite.config.ts
│       ├── tsconfig.json
│       └── src/
├── packages/
│   ├── api-client/
│   │   ├── package.json
│   │   ├── orval.config.ts
│   │   └── src/
│   ├── core/
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── src/
│   │       ├── auth/
│   │       ├── http/
│   │       ├── telemetry/
│   │       ├── device.ts
│   │       └── errors.ts
│   └── ui/
│       ├── package.json
│       └── src/
```

## Root Configuration Files

### pnpm-workspace.yaml

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

### package.json (root)

```json
{
  "name": "@novatune/root",
  "private": true,
  "type": "module",
  "scripts": {
    "dev:player": "pnpm --filter player dev",
    "dev:admin": "pnpm --filter admin dev",
    "build": "pnpm -r build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint",
    "typecheck": "pnpm -r typecheck",
    "generate": "pnpm --filter @novatune/api-client generate"
  },
  "devDependencies": {
    "@types/node": "^20.14.0",
    "typescript": "^5.6.0",
    "eslint": "^9.0.0",
    "prettier": "^3.3.0"
  },
  "engines": {
    "node": ">=20.0.0",
    "pnpm": ">=9.0.0"
  }
}
```

### tsconfig.base.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "noEmit": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "lib": ["ES2022", "DOM", "DOM.Iterable"]
  }
}
```

## App Configuration

### apps/player/package.json

```json
{
  "name": "player",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:e2e": "playwright test",
    "lint": "eslint src",
    "typecheck": "vue-tsc --noEmit"
  },
  "dependencies": {
    "vue": "^3.5.0",
    "vue-router": "^4.4.0",
    "pinia": "^2.2.0",
    "@tanstack/vue-query": "^5.0.0",
    "@novatune/api-client": "workspace:*",
    "@novatune/core": "workspace:*",
    "@novatune/ui": "workspace:*"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^6.0.0",
    "vitest": "^2.0.0",
    "vue-tsc": "^2.0.0",
    "@vue/test-utils": "^2.4.0",
    "@testing-library/vue": "^8.0.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "@playwright/test": "^1.45.0",
    "msw": "^2.0.0"
  }
}
```

### apps/player/vite.config.ts

```typescript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});
```

## Package Configuration

### packages/core/package.json

```json
{
  "name": "@novatune/core",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "main": "./src/index.ts",
  "exports": {
    ".": "./src/index.ts",
    "./auth": "./src/auth/index.ts",
    "./http": "./src/http/index.ts",
    "./telemetry": "./src/telemetry/index.ts",
    "./errors": "./src/errors.ts",
    "./device": "./src/device.ts"
  },
  "dependencies": {
    "axios": "^1.7.0",
    "@noble/hashes": "^1.4.0",
    "pinia": "^2.2.0"
  }
}
```

### packages/api-client/package.json

```json
{
  "name": "@novatune/api-client",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "main": "./src/index.ts",
  "scripts": {
    "generate": "orval"
  },
  "dependencies": {
    "axios": "^1.7.0"
  },
  "devDependencies": {
    "orval": "^7.0.0"
  }
}
```

## Implementation Steps

### 1. Create Directory Structure

```bash
mkdir -p src/NovaTuneClient/{apps/{player,admin}/src,packages/{api-client,core,ui}/src}
```

### 2. Initialize Root Package

```bash
cd src/NovaTuneClient
pnpm init
```

### 3. Create Configuration Files

- `pnpm-workspace.yaml`
- `tsconfig.base.json`
- `.env.example`

### 4. Initialize Apps

```bash
pnpm create vite apps/player --template vue-ts
pnpm create vite apps/admin --template vue-ts
```

### 5. Configure Workspace Dependencies

```bash
pnpm install
pnpm add -D typescript eslint prettier -w
```

### 6. Add Shared Packages

Configure `packages/core`, `packages/api-client`, and `packages/ui` with proper exports.

## Environment Variables

### .env.example

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:5000

# App Configuration
VITE_APP_VERSION=0.0.1-dev

# Feature Flags
VITE_ENABLE_TELEMETRY=true
```

## Development Workflow

```bash
# Install dependencies
pnpm -C src/NovaTuneClient install

# Start player dev server
pnpm -C src/NovaTuneClient dev:player

# Start admin dev server (parallel terminal)
pnpm -C src/NovaTuneClient dev:admin

# Run tests
pnpm -C src/NovaTuneClient test

# Build all apps
pnpm -C src/NovaTuneClient build
```

## Related Documentation

- **Frontend Plan**: `doc/implementation/frontend/main.md`
- **Requirements**: `doc/requirements/stack.md`

## Related Skills

- **generate-api-client** - Generate TypeScript client from OpenAPI
- **implement-player-app** - Build player application
- **implement-admin-app** - Build admin application

## Claude Agents

- **frontend-planner** - Plan frontend implementation
- **vue-app-implementer** - Implement Vue applications
