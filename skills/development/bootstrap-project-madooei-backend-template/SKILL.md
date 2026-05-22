---
name: bootstrap-project
description: Initialize a new backend project with TypeScript, ESLint, Prettier, and Hono. Use when starting a new service from scratch. Triggers on "new project", "bootstrap", "start from scratch", "initialize project".
---

# Bootstrap Project

Initializes a minimal TypeScript backend project with Hono.js, including code quality tooling (ESLint, Prettier) and a "Hello World" app.

## Quick Reference

**Use when**: Creating a new backend service from scratch
**Result**: A minimal project ready for adding layers via other skills

## Prerequisites

- Node.js 20+ installed
- pnpm installed (`npm install -g pnpm`)
- Git installed

## Instructions

### Phase 1: Project Initialization

#### Step 1: Create Project Directory

```bash
mkdir my-backend-service
cd my-backend-service
git init
```

#### Step 2: Initialize Package

```bash
pnpm init
```

#### Step 3: Install Dependencies

```bash
# Core dependencies
pnpm add hono @hono/node-server zod dotenv

# TypeScript and build tools
pnpm add -D typescript tsx tsup @types/node

# Testing
pnpm add -D vitest @vitest/coverage-v8

# Linting and formatting
pnpm add -D eslint typescript-eslint @eslint/js globals jiti
pnpm add -D prettier eslint-config-prettier eslint-plugin-prettier
```

### Phase 2: Configuration Files

#### Step 4: Create TypeScript Config

Create `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "verbatimModuleSyntax": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "jsxImportSource": "hono/jsx",
    "types": ["node"],
    "rootDir": ".",
    "outDir": "./dist",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*", "scripts/**/*", "tests/**/*"],
  "exclude": ["node_modules", "dist", "coverage"]
}
```

Create `tsconfig.build.json`:

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "coverage", "tests", "scripts"]
}
```

#### Step 5: Create Build Config

Create `tsup.config.ts`:

```typescript
import { defineConfig } from "tsup";

export default defineConfig({
  target: "node20",
  entry: ["src/server.ts"],
  outDir: "dist",
  format: ["esm"],
  sourcemap: true,
  clean: true,
  dts: true,
  splitting: true,
  treeshake: true,
  esbuildOptions(options) {
    options.alias = {
      "@": "./src",
    };
  },
});
```

#### Step 6: Create Vitest Config

Create `vitest.config.ts`:

```typescript
import path from "path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["tests/**/*.test.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      all: true,
      include: ["src/**/*.ts"],
      exclude: [
        "**/*.test.ts",
        "**/coverage/**",
        "**/node_modules/**",
        "**/dist/**",
        "**/scripts/**",
        "**/src/server.ts",
      ],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

#### Step 7: Create ESLint Config

Create `eslint.config.ts`:

```typescript
import js from "@eslint/js";
import globals from "globals";
import tseslint from "typescript-eslint";
import eslintConfigPrettier from "eslint-config-prettier";
import eslintPluginPrettier from "eslint-plugin-prettier";

export default tseslint.config(
  { ignores: ["dist", "tests"] },
  {
    extends: [
      js.configs.recommended,
      ...tseslint.configs.recommended,
      eslintConfigPrettier,
    ],
    files: ["**/*.ts"],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
    plugins: {
      prettier: eslintPluginPrettier,
    },
    rules: {},
  },
);
```

#### Step 8: Create Prettier Config

Create `prettier.config.json`:

```json
{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": false,
  "printWidth": 80,
  "tabWidth": 2,
  "endOfLine": "auto"
}
```

Create `.prettierignore`:

```plaintext
**/.git
**/.svn
**/.hg
**/node_modules

pnpm-lock.yaml
dist
```

#### Step 9: Update package.json

Add the following to `package.json`:

```json
{
  "type": "module",
  "scripts": {
    "dev": "tsx watch src/server.ts",
    "build": "tsup",
    "start": "node dist/server.js",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "type-check": "tsc --noEmit --project tsconfig.build.json",
    "lint": "eslint",
    "lint:fix": "eslint --fix",
    "format": "prettier --check .",
    "format:fix": "prettier --write .",
    "validate": "pnpm type-check && pnpm lint:fix && pnpm format:fix && pnpm test",
    "clean": "rm -rf dist coverage"
  }
}
```

### Phase 3: Directory Structure

#### Step 10: Create Directory Structure

```bash
mkdir -p src/{controllers,middlewares,repositories/mockdb,routes,schemas,services}
mkdir -p tests/{controllers,middlewares,repositories,routes,schemas,services}
mkdir -p scripts
```

### Phase 4: Core Files

#### Step 11: Create Environment Config

Create `src/env.ts`:

```typescript
import dotenv from "dotenv";
import { z } from "zod";

dotenv.config();

/**
 * Environment variable prefix for this service.
 * This prevents conflicts when running multiple services in the same environment.
 * Change this prefix when creating a new service from this template.
 */
const PREFIX = "BT";

/**
 * Helper function to get prefixed environment variable.
 * Falls back to unprefixed variable for backwards compatibility during migration.
 */
const getEnv = (name: string): string | undefined => {
  return process.env[`${PREFIX}_${name}`] ?? process.env[name];
};

const envSchema = z.object({
  NODE_ENV: z.string().default("development"),
  PORT: z.coerce.number().default(3000),
});

// Map prefixed environment variables to internal names
const mappedEnv = {
  NODE_ENV: getEnv("NODE_ENV"),
  PORT: getEnv("PORT"),
};

const _env = envSchema.safeParse(mappedEnv);

if (!_env.success) {
  console.error("Invalid environment variables:", _env.error.format());
  process.exit(1);
}

export const env = _env.data;
```

Create `.env.example`:

```bash
# Environment variable prefix: BT (Backend Template)
# Change this prefix in src/env.ts when creating a new service

BT_NODE_ENV=development
BT_PORT=3000
```

Create `.env`:

```bash
BT_NODE_ENV=development
BT_PORT=3000
```

#### Step 12: Create App Context Schema

Create `src/schemas/app-env.schema.ts`:

```typescript
export interface AppEnv {
  Variables: {
    validatedBody: unknown;
    validatedQuery: unknown;
    validatedParams: unknown;
  };
}
```

#### Step 13: Create App

Create `src/app.ts`:

```typescript
import { Hono } from "hono";
import type { AppEnv } from "@/schemas/app-env.schema";

export const app = new Hono<AppEnv>();

app.get("/", (c) => c.text("Hello Hono!"));
```

#### Step 14: Create Server

Create `src/server.ts`:

```typescript
import { serve } from "@hono/node-server";
import { app } from "@/app";
import { env } from "@/env";

serve(
  {
    fetch: app.fetch,
    port: env.PORT,
  },
  (info) => {
    console.log(`Server is running on http://localhost:${info.port}`);
  },
);
```

### Phase 5: Git Configuration

#### Step 15: Create .gitignore

Create `.gitignore`:

```plaintext
# dev
.yarn/
!.yarn/releases
.vscode/*
!.vscode/launch.json
!.vscode/*.code-snippets
!.vscode/extensions.json
!.vscode/settings.json
.idea/

# deps
node_modules/
.pnpm-store/

# env
.env
.env.production

# logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# misc
.DS_Store

# Build artifacts
dist

# Test Coverage
coverage
```

### Phase 6: Verification

#### Step 16: Verify Setup

```bash
# Install dependencies (if not already done)
pnpm install

# Type check
pnpm type-check

# Lint
pnpm lint

# Format
pnpm format:fix

# Start dev server
pnpm dev

# In another terminal, test the endpoint
curl http://localhost:3000
# Should return: Hello Hono!
```

## Files Created Summary

```plaintext
my-backend-service/
├── src/
│   ├── app.ts                    # Hono app with Hello World route
│   ├── server.ts                 # Server startup
│   ├── env.ts                    # Environment configuration
│   ├── controllers/              # (empty)
│   ├── middlewares/              # (empty)
│   ├── repositories/
│   │   └── mockdb/               # (empty)
│   ├── routes/                   # (empty)
│   ├── schemas/
│   │   └── app-env.schema.ts     # AppEnv interface
│   └── services/                 # (empty)
├── tests/
│   ├── controllers/              # (empty)
│   ├── middlewares/              # (empty)
│   ├── repositories/             # (empty)
│   ├── routes/                   # (empty)
│   ├── schemas/                  # (empty)
│   └── services/                 # (empty)
├── scripts/                      # (empty)
├── .env
├── .env.example
├── .gitignore
├── .prettierignore
├── eslint.config.ts
├── package.json
├── prettier.config.json
├── tsconfig.json
├── tsconfig.build.json
├── tsup.config.ts
└── vitest.config.ts
```

## Next Steps

After bootstrapping, use these skills to build out your application:

1. **`setup-errors`** - Add error handling infrastructure (BaseError, HTTP errors, global handler)
2. **`setup-events`** - Add event system for real-time updates (EventEmitter, BaseService)
3. **`setup-testing`** - Enhanced test infrastructure (fixtures, helpers)
4. **`setup-docker`** - Add Docker support for development and production
5. **`setup-mongodb`** - Add MongoDB database support
6. **`create-resource`** - Create your first CRUD resource (schema, repository, service, controller, routes)

## What NOT to Do

- Do NOT skip the TypeScript configuration
- Do NOT use relative imports (always use `@/` path alias)
- Do NOT commit `.env` file (only `.env.example`)
- Do NOT add complex infrastructure here (use dedicated setup skills)

## See Also

- `setup-errors` - Error handling infrastructure
- `setup-events` - Event-driven architecture
- `setup-testing` - Test infrastructure
- `setup-docker` - Docker configuration
- `setup-mongodb` - MongoDB setup
- `create-resource` - Create a complete CRUD resource
