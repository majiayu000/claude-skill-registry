---
name: setup-typescript-project
description: Comprehensive configuration templates and guidance for setting up TypeScript
  projects with modern tooling, testing frameworks, and code quality enforcement.
---

# TypeScript Project Setup

Comprehensive configuration templates and guidance for setting up TypeScript projects with modern tooling, testing frameworks, and code quality enforcement.

## Purpose

This skill provides standardized configurations and best practices for TypeScript projects, including:

- TypeScript configuration with ES modules or CommonJS
- Choice of **Biome** (recommended) or **ESLint+Prettier** for linting/formatting
- Vitest for unit and integration testing (optional)
- Playwright for end-to-end testing (optional)
- Husky for pre-commit hooks
- Makefile for common operations
- GitHub Actions for CI/CD
- Package.json scripts for common workflows

## When to Use

Use this skill when:

- Starting a new TypeScript project
- Adding TypeScript to an existing JavaScript project
- Setting up testing infrastructure (unit + e2e)
- Implementing code quality gates and pre-commit hooks
- Standardizing configurations across multiple TypeScript projects
- Need guidance on recommended dependencies and versions

## Initial Setup Questions

When using this skill, Claude will ask:

1. **Module System:**
 - **ES Modules** (recommended for new projects) - Modern, bundler-friendly
 - **CommonJS** - Traditional Node.js, better for legacy compatibility

1. **Linting/Formatting Tool:**
 - **Biome** (recommended) - Modern, fast, all-in-one tool
 - **ESLint + Prettier** - Traditional, wider ecosystem support
 - **None** - Rely on TypeScript strict mode only (minimal approach)

1. **Testing Strategy:**
 - **Vitest only** - Unit and integration testing
 - **Playwright only** - E2E and component testing
 - **Vitest + Playwright** - Comprehensive testing (unit + E2E)
 - **None** - No testing setup

1. **Pre-commit Hooks:**
 - **Yes** - Set up Husky with quality checks
 - **No** - Manual quality checks only

1. **Project Type:**
 - **Vite Frontend** - Browser app with bundler mode
 - **Node.js Backend** - Server-side application
 - **CLI Tool** - Command-line tool
 - **Library** - Reusable package with type definitions
 - **General** - Standard TypeScript project

## Project Structure

Recommended directory structure:

```
project-root/
├── src/ # TypeScript source files
│ ├── **/*.ts
│ └── **/*.tsx
├── tests/ # Test files
│ ├── **/*.test.ts # Vitest unit tests (if using Vitest)
│ └── **/*.spec.ts # Test files (Vitest or Playwright)
├── dist/ # Compiled output (if not using bundler)
├── .husky/ # Git hooks (if enabled)
│ └── pre-commit
├── .github/ # GitHub Actions workflows
│ └── workflows/
│ └── checks.yml
├── tsconfig.json # TypeScript config
├── biome.json # Biome config (if using Biome)
├── eslint.config.js # ESLint config (if using ESLint)
├── .prettierrc.json # Prettier config (if using Prettier)
├── vitest.config.js # Vitest config (if using Vitest)
├── playwright.config.ts # Playwright config (if using Playwright)
├── Makefile # Common operations
└── package.json
```

## Configuration Templates

### 1. TypeScript Configuration (tsconfig.json)

#### For Vite/Bundler Projects (Frontend)

```json
{
 "compilerOptions": {
 "target": "ES2022",
 "lib": ["ES2022", "DOM", "DOM.Iterable"],
 "module": "ESNext",
 "skipLibCheck": true,

 /* Bundler mode */
 "moduleResolution": "bundler",
 "allowImportingTsExtensions": true,
 "resolveJsonModule": true,
 "isolatedModules": true,
 "noEmit": true,

 /* Linting */
 "strict": true,
 "noUnusedLocals": true,
 "noUnusedParameters": true,
 "noFallthroughCasesInSwitch": true,
 "forceConsistentCasingInFileNames": true
 },
 "include": ["src"]
}
```

**Key settings for Vite:**

- `"moduleResolution": "bundler"` - Modern bundler-aware resolution
- `"noEmit": true` - Vite handles compilation, not tsc
- `"allowImportingTsExtensions": true` - Import `.ts` files directly
- `"isolatedModules": true` - Required for bundlers

#### For Node.js/Backend Projects (ES Modules)

```json
{
 "compilerOptions": {
 "target": "ES2022",
 "module": "ES2022",
 "moduleResolution": "node",
 "esModuleInterop": true,
 "strict": true,
 "noImplicitAny": true,
 "strictNullChecks": true,
 "noUnusedLocals": true,
 "noUnusedParameters": true,
 "lib": ["ES2022"],
 "skipLibCheck": true,
 "forceConsistentCasingInFileNames": true,
 "outDir": "dist",
 "rootDir": "src",
 "declaration": true,
 "resolveJsonModule": true
 },
 "include": ["src/**/*.ts"],
 "exclude": ["node_modules", "dist"]
}
```

#### For Node.js/Backend Projects (CommonJS)

```json
{
 "compilerOptions": {
 "target": "ES2020",
 "module": "CommonJS",
 "outDir": "./dist",
 "rootDir": "./src",
 "strict": true,
 "esModuleInterop": true,
 "skipLibCheck": true,
 "forceConsistentCasingInFileNames": true,
 "resolveJsonModule": true
 },
 "include": ["src/**/*"],
 "exclude": ["node_modules"]
}
```

**When to use CommonJS:**

- Legacy Node.js projects
- Enterprise environments with older Node versions
- Projects that depend on CommonJS-only packages
- When ES modules cause compatibility issues

### 2. Linting and Formatting

## Option A: Biome (Recommended)

**Configuration (biome.json):**

```json
{
 "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
 "organizeImports": {
 "enabled": true
 },
 "formatter": {
 "enabled": true,
 "indentStyle": "space",
 "indentWidth": 2,
 "lineWidth": 120,
 "lineEnding": "lf"
 },
 "linter": {
 "enabled": true,
 "rules": {
 "recommended": true,
 "suspicious": {
 "noExplicitAny": "warn"
 },
 "style": {
 "useConst": "error",
 "noNonNullAssertion": "warn"
 }
 }
 },
 "javascript": {
 "formatter": {
 "quoteStyle": "single",
 "semicolons": "asNeeded",
 "trailingCommas": "es5"
 }
 },
 "files": {
 "ignore": [
 "dist",
 "node_modules",
 "test-results",
 "playwright-report",
 "*.config.js",
 "*.config.ts"
 ]
 }
}
```

**Package.json scripts:**

```json
{
 "scripts": {
 "lint": "biome check .",
 "lint:fix": "biome check --write .",
 "format": "biome format --write .",
 "check": "biome check . && tsc --noEmit"
 }
}
```

**Dependencies:**

```bash
npm install --save-dev @biomejs/biome
```

**Biome advantages:**

- 10-100x faster than ESLint (Rust-based)
- Single tool for linting + formatting + import sorting
- Zero config needed (sensible defaults)
- Simple configuration file
- Modern, actively developed

**Code style:**

- Single quotes
- Semicolons only when needed (ASI-friendly)
- Trailing commas in ES5 contexts (arrays, objects)
- 120 character line width
- 2-space indentation

## Option B: ESLint + Prettier (Traditional)

**ESLint Configuration (eslint.config.js):**

```javascript
import eslint from '@eslint/js'
import tseslint from '@typescript-eslint/eslint-plugin'
import tsParser from '@typescript-eslint/parser'

export default [
 eslint.configs.recommended,
 {
 files: ['**/*.ts', '**/*.js'],
 languageOptions: {
 parser: tsParser,
 ecmaVersion: 2020,
 sourceType: 'module',
 globals: {
 // Browser globals
 window: 'readonly',
 document: 'readonly',
 console: 'readonly',
 // Node globals
 process: 'readonly',
 module: 'readonly',
 require: 'readonly',
 __dirname: 'readonly'
 }
 },
 plugins: {
 '@typescript-eslint': tseslint
 },
 rules: {
 ...tseslint.configs.recommended.rules,
 '@typescript-eslint/no-unused-vars': ['error', {
 argsIgnorePattern: '^_',
 varsIgnorePattern: '^_'
 }],
 '@typescript-eslint/no-explicit-any': 'warn',
 'no-console': 'warn',
 'semi': ['error', 'never'],
 'quotes': ['error', 'single', { avoidEscape: true }],
 'comma-dangle': ['error', 'never']
 }
 },
 {
 files: ['**/*.test.js', '**/*.test.ts'],
 rules: {
 'no-console': 'off'
 }
 }
]
```

**Prettier Configuration (.prettierrc.json):**

```json
{
 "semi": false,
 "singleQuote": true,
 "trailingComma": "none",
 "printWidth": 100,
 "tabWidth": 2,
 "arrowParens": "avoid"
}
```

**Package.json scripts:**

```json
{
 "scripts": {
 "lint": "eslint src/**/*.{js,ts}",
 "lint:fix": "eslint src/**/*.{js,ts} --fix",
 "lint:errors-only": "eslint src/**/*.{js,ts} --quiet",
 "format": "prettier --write src/**/*.{js,ts}",
 "format:check": "prettier --check src/**/*.{js,ts}",
 "check": "npm run typecheck && npm run lint && npm run format:check"
 }
}
```

**Dependencies:**

```bash
npm install --save-dev \
 eslint @eslint/js \
 @typescript-eslint/eslint-plugin \
 @typescript-eslint/parser \
 prettier
```

**Code style:**

- Single quotes
- No semicolons
- No trailing commas
- 100 character line width
- 2-space indentation

## Option C: No Linting (Minimal)

**When to use:**

- Small, simple projects
- Relying on TypeScript strict mode for type safety
- Team has strong IDE setup and conventions
- CI handles quality checks

**Package.json scripts:**

```json
{
 "scripts": {
 "check": "tsc --noEmit"
 }
}
```

**Note:** TypeScript's strict mode catches many issues that linters would, but you lose style consistency enforcement.

### 3. Testing Configurations

## Option A: Vitest Only

**When to use:** Unit testing, integration testing, API testing (no browser needed).

**Configuration (vitest.config.js):**

```javascript
import {defineConfig} from 'vitest/config'

export default defineConfig({
 test: {
 environment: 'jsdom',
 globals: true,
 setupFiles: ['./tests/setup.js'],
 include: ['./tests/**/*.test.js', './tests/**/*.test.ts', './tests/**/*.spec.ts'],
 coverage: {
 provider: 'v8',
 reporter: ['text', 'json', 'html']
 }
 }
})
```

**Note:** Vitest works without a config file - it will auto-discover tests. Config is optional for customization.

**Package.json scripts:**

```json
{
 "scripts": {
 "test": "vitest run",
 "test:watch": "vitest",
 "test:coverage": "vitest run --coverage",
 "test:ui": "vitest --ui"
 }
}
```

**Dependencies:**

```bash
npm install --save-dev vitest @vitest/coverage-v8
```

## Option B: Playwright Only

**When to use:** E2E testing, browser testing, visual testing.

**Configuration (playwright.config.ts):**

```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
 testDir: './tests',
 fullyParallel: true,
 forbidOnly: !!process.env.CI,
 retries: process.env.CI ? 2 : 0,
 workers: process.env.CI ? 1 : undefined,
 reporter: 'html',

 use: {
 baseURL: process.env.BASE_URL || 'http://localhost:3000',
 trace: 'on-first-retry',
 screenshot: 'only-on-failure',
 },

 projects: [
 {
 name: 'chromium',
 use: { ...devices['Desktop Chrome'] },
 },
 ],

 webServer: process.env.BASE_URL ? undefined : {
 command: 'npm run preview',
 url: 'http://localhost:3000',
 reuseExistingServer: !process.env.CI,
 },
})
```

**Package.json scripts:**

```json
{
 "scripts": {
 "test": "playwright test",
 "test:headed": "playwright test --headed",
 "test:ui": "playwright test --ui"
 }
}
```

**Dependencies:**

```bash
npm install --save-dev @playwright/test
```

## Option C: Vitest + Playwright

**When to use:** Comprehensive testing strategy (fast unit tests + thorough E2E tests).

**Testing strategy:**

- `.test.ts` files → Vitest (unit tests)
- `.spec.ts` files → Playwright (E2E tests)

**Package.json scripts:**

```json
{
 "scripts": {
 "test": "vitest run",
 "test:watch": "vitest",
 "test:coverage": "vitest run --coverage",
 "test:ui": "vitest --ui",
 "test:e2e": "playwright test",
 "test:e2e:ui": "playwright test --ui",
 "test:e2e:report": "playwright show-report"
 }
}
```

### 4. Pre-commit Hooks with Husky

**Setup Husky:**

```bash
npm install --save-dev husky
npx husky init
```

**Pre-commit hook (.husky/pre-commit):**

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npm run quality:commit
```

**Package.json scripts:**

For Biome:

```json
{
 "scripts": {
 "quality": "npm run check && npm run test",
 "quality:commit": "biome check . && tsc --noEmit && npm run test",
 "prepare": "husky"
 }
}
```

For ESLint+Prettier:

```json
{
 "scripts": {
 "quality": "npm run typecheck && npm run lint && npm run format:check && npm run test",
 "quality:commit": "npm run typecheck && npm run lint:errors-only && npm run test",
 "prepare": "husky"
 }
}
```

For minimal (no linting):

```json
{
 "scripts": {
 "quality": "npm run typecheck && npm run test",
 "quality:commit": "tsc --noEmit && npm run test",
 "prepare": "husky"
 }
}
```

**What runs in pre-commit:**

1. Type checking (fast)
1. Linting errors only (warnings ignored)
1. Tests (unit tests only, not E2E)

**What NOT to run in pre-commit:**

- Formatting (too slow, should be editor responsibility)
- Full linting with warnings (too noisy)
- E2E tests (too slow)

### 5. Makefile

**Common Makefile targets:**

```makefile
.PHONY: help install build test clean lint format check

help:
 @echo "Available targets:"
 @echo " install - Install dependencies"
 @echo " build - Build the project"
 @echo " test - Run tests"
 @echo " clean - Clean build artifacts"
 @echo " lint - Run linting"
 @echo " format - Format code"
 @echo " check - Run all quality checks"

install:
 npm ci

build:
 npm run build

test:
 npm run test

clean:
 rm -rf dist node_modules

lint:
 npm run lint

format:
 npm run format

check:
 npm run quality
```

### 6. GitHub Actions

**Basic CI workflow (.github/workflows/checks.yml):**

```yaml
name: Checks

on:
 push:
 branches-ignore:
 - main
 pull_request:
 branches:
 - main

permissions: read-all

jobs:
 quality:
 runs-on: ubuntu-latest
 steps:
 - uses: actions/checkout@v4

 - name: Setup Node.js
 uses: actions/setup-node@v4
 with:
 node-version: '20'
 cache: 'npm'

 - name: Install dependencies
 run: npm ci

 - name: Type check
 run: npm run typecheck

 - name: Lint
 run: npm run lint
 if: hashFiles('biome.json', 'eslint.config.js') != ''

 - name: Test
 run: npm run test
 if: hashFiles('vitest.config.js', 'playwright.config.ts') != ''
```

### 7. Complete Package.json Examples

**For ES Modules + Biome + Vitest:**

```json
{
 "name": "my-typescript-project",
 "version": "1.0.0",
 "type": "module",
 "scripts": {
 "dev": "your-dev-command",
 "build": "tsc",
 "typecheck": "tsc --noEmit",
 "test": "vitest run",
 "test:watch": "vitest",
 "test:coverage": "vitest run --coverage",
 "lint": "biome check .",
 "lint:fix": "biome check --write .",
 "format": "biome format --write .",
 "check": "biome check . && tsc --noEmit",
 "quality": "npm run check && npm run test",
 "quality:commit": "biome check . && tsc --noEmit && npm run test",
 "prepare": "husky"
 },
 "devDependencies": {
 "@biomejs/biome": "^1.9.0",
 "@types/node": "^22.0.0",
 "@vitest/coverage-v8": "^2.1.0",
 "husky": "^9.0.0",
 "typescript": "^5.6.0",
 "vitest": "^2.1.0"
 }
}
```

**For CommonJS + No Linting + Vitest:**

```json
{
 "name": "my-typescript-project",
 "version": "1.0.0",
 "scripts": {
 "build": "tsc",
 "test": "vitest",
 "coverage": "vitest run --coverage",
 "typecheck": "tsc --noEmit",
 "quality": "npm run typecheck && npm run test",
 "quality:commit": "tsc --noEmit && npm run test",
 "prepare": "husky"
 },
 "devDependencies": {
 "@types/node": "^22.0.0",
 "@vitest/coverage-v8": "^2.1.0",
 "husky": "^9.0.0",
 "typescript": "^5.6.0",
 "vitest": "^2.1.0"
 }
}
```

## Quick Setup Guide

### 1. Initialize Project

```bash
npm init -y
npm install --save-dev typescript
```

### 2. Choose Module System

**For ES Modules (recommended):**

```bash
npm pkg set type=module
```

**For CommonJS:**

No action needed (default)

### 3. Initialize TypeScript

```bash
npx tsc --init
```

Then replace with the appropriate config from this skill.

### 4. Choose Linting/Formatting

**Option A: Biome (recommended)**

```bash
npm install --save-dev @biomejs/biome
npx @biomejs/biome init
```

**Option B: ESLint + Prettier**

```bash
npm install --save-dev \
 eslint @eslint/js \
 @typescript-eslint/eslint-plugin \
 @typescript-eslint/parser \
 prettier
```

**Option C: None**

Skip this step

### 5. Choose Testing

**Option A: Vitest**

```bash
npm install --save-dev vitest @vitest/coverage-v8
```

**Option B: Playwright**

```bash
npm init playwright@latest
```

**Option C: Both**

```bash
npm install --save-dev vitest @vitest/coverage-v8 @playwright/test
npm init playwright@latest
```

### 6. Set up Pre-commit Hooks

```bash
npm install --save-dev husky
npx husky init
echo "npm run quality:commit" > .husky/pre-commit
chmod +x .husky/pre-commit
```

### 7. Create Makefile

Create a `Makefile` with the targets shown above.

### 8. Set up GitHub Actions

Create `.github/workflows/checks.yml` with the workflow shown above.

## Best Practices

### 1. Module System Choice

**ES Modules (recommended for new projects):**

- Modern, future-proof
- Better tree-shaking in bundlers
- Native browser support
- Required for Vite and modern tools

**CommonJS (for legacy compatibility):**

- Better compatibility with older Node.js
- Some npm packages only support CommonJS
- Traditional Node.js pattern

### 2. Type Safety

- Enable all strict flags in tsconfig.json
- Use `noUnusedLocals` and `noUnusedParameters`
- Avoid `any` types (linters warn about them)
- Prefix unused variables with `_` if needed

### 3. Code Style

- **Biome default:** Single quotes, semicolons as needed, trailing commas in ES5 contexts
- **ESLint+Prettier default:** Single quotes, no semicolons, no trailing commas
- Consistent 2-space indentation
- 120 char line width (modern)

### 4. Testing Strategy

- **Vitest only:** Fast, good for libraries and backend
- **Playwright only:** Essential for frontend apps
- **Both:** Comprehensive coverage for full-stack apps
- Keep E2E tests out of pre-commit hooks (too slow)

### 5. Pre-commit Hooks

- Run fast checks only (typecheck, lint errors, unit tests)
- Skip slow checks (formatting, warnings, E2E tests)
- Let CI handle comprehensive quality checks
- Developers should format code via editor

### 6. CI/CD

- Run comprehensive checks in CI (what you skip in pre-commit)
- Use caching for faster builds
- Separate workflows for PRs vs main branch
- Consider coverage thresholds

### 7. Makefile Usage

- Provides consistent interface across projects
- Easier for new contributors (single command reference)
- Works regardless of language/tooling
- Good for complex multi-step operations

## Decision Matrix

| Criteria | Biome | ESLint+Prettier | None |
|----------|-------|-----------------|------|
| Speed | Much faster | Slower | Fastest |
| Simplicity | Single tool | Two tools | No tools |
| Ecosystem | Growing | Mature, extensive | N/A |
| Style enforcement | Excellent | Excellent | Manual |
| Type safety | Via rules | Via rules | TypeScript only |

| Criteria | ES Modules | CommonJS |
|----------|------------|----------|
| Modern | Yes | No |
| Bundler support | Excellent | Good |
| Node.js compat | Node 12+ | All versions |
| Future-proof | Yes | Legacy |

| Criteria | Vitest | Playwright | Both |
|----------|--------|------------|------|
| Unit testing | Excellent | N/A | Excellent |
| E2E testing | N/A | Excellent | Excellent |
| Speed | Fast | Slower | Mixed |
| Setup | Simple | Moderate | Complex |

## Common Issues and Solutions

### Issue: "Cannot find module" errors with ES modules

**Solution:** Ensure `"type": "module"` is in package.json and use `.js` extension for config files.

### Issue: Biome not recognizing TypeScript

**Solution:** Biome works out of the box with TypeScript. Ensure `biome.json` exists and `@biomejs/biome` is installed.

### Issue: ESLint not recognizing TypeScript

**Solution:** Verify `@typescript-eslint/parser` is specified in `languageOptions.parser`.

### Issue: Pre-commit hook is too slow

**Solution:** Use `quality:commit` (fast) instead of `quality` (comprehensive). Remove E2E tests from pre-commit.

### Issue: Vitest not finding tests

**Solution:** Vitest auto-discovers tests. Ensure test files match patterns: `**/*.{test,spec}.{js,ts}`.

### Issue: Husky hooks not running

**Solution:** Ensure `.husky/pre-commit` is executable: `chmod +x .husky/pre-commit`.

### Issue: Make commands not working

**Solution:** Ensure Makefile uses tabs (not spaces) for indentation.

## Project Type Recommendations

### Vite Frontend Projects

- ES Modules
- Biome (faster, modern)
- TypeScript with bundler mode
- Playwright for E2E testing
- Pre-commit hooks
- GitHub Actions CI

### Node.js Backend Projects

- ES Modules (or CommonJS for legacy)
- Biome or ESLint+Prettier
- TypeScript with node resolution
- Vitest for unit tests
- Pre-commit hooks
- GitHub Actions CI

### CLI Tools

- CommonJS (better compatibility)
- Minimal linting (or none)
- TypeScript with CommonJS module
- Vitest for unit tests
- Pre-commit hooks
- GitHub Actions CI

### Library Projects

- ES Modules with CommonJS output (dual package)
- ESLint+Prettier (wider compatibility)
- TypeScript with `declaration: true`
- Vitest for comprehensive unit testing
- Pre-commit hooks with strict checks
- GitHub Actions CI with publishing

### Monorepo Projects

- ES Modules
- Biome (single config, fast)
- TypeScript project references
- Both Vitest + Playwright
- Workspace-level pre-commit hooks
- GitHub Actions CI with matrix builds
