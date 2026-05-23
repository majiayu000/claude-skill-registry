---
name: npm-scripts
description: npm, yarn, and pnpm package management, scripts, workspaces, and publishing. Use when user asks to "run npm script", "setup package.json", "publish package", "manage dependencies", "npm workspaces", "monorepo setup", or package manager operations.
---

# npm/yarn/pnpm

Package management, scripts, and workspaces.

## Package.json Scripts

### Common Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "start": "node dist/index.js",
    "test": "vitest",
    "test:watch": "vitest watch",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "format": "prettier --write .",
    "typecheck": "tsc --noEmit",
    "prepare": "husky"
  }
}
```

### Script Chaining

```json
{
  "scripts": {
    "prebuild": "npm run clean",
    "build": "tsc",
    "postbuild": "npm run copy-assets",
    "clean": "rm -rf dist",
    "copy-assets": "cp -r assets dist/"
  }
}
```

### Run Scripts in Sequence/Parallel

```bash
# Sequence (npm-run-all)
npm-run-all lint test build

# Parallel
npm-run-all --parallel lint typecheck

# Or use &&
npm run lint && npm run test
```

## Dependency Management

### Install

```bash
npm install              # All dependencies
npm install lodash       # Add dependency
npm install -D typescript  # Dev dependency
npm install -g vercel    # Global

# Specific version
npm install lodash@4.17.21
npm install lodash@^4.0.0
```

### Update

```bash
npm update              # Update within ranges
npm update lodash       # Specific package
npx npm-check-updates   # Check for updates
npx npm-check-updates -u  # Update package.json
```

### Remove

```bash
npm uninstall lodash
npm uninstall -g vercel
```

### Audit

```bash
npm audit
npm audit fix
npm audit fix --force  # Breaking changes OK
```

## Workspaces (Monorepo)

### Setup

```json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["packages/*"]
}
```

### Structure

```
my-monorepo/
├── package.json
├── packages/
│   ├── shared/
│   │   └── package.json
│   ├── web/
│   │   └── package.json
│   └── api/
│       └── package.json
```

### Commands

```bash
# Install all workspaces
npm install

# Run script in specific workspace
npm run build -w packages/web

# Run in all workspaces
npm run test --workspaces

# Add dep to workspace
npm install lodash -w packages/shared
```

## pnpm

### Advantages

- Faster installs
- Disk space efficient (hard links)
- Strict node_modules

### Commands

```bash
pnpm install
pnpm add lodash
pnpm add -D typescript
pnpm remove lodash
pnpm run dev
```

### Workspaces

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
```

```bash
pnpm -F web run build     # Filter by name
pnpm -r run build         # All workspaces
```

## yarn

### Commands

```bash
yarn                     # Install
yarn add lodash
yarn add -D typescript
yarn remove lodash
yarn dev
```

### Workspaces

```json
{
  "workspaces": ["packages/*"]
}
```

```bash
yarn workspace web build
yarn workspaces foreach run build
```

## Publishing

### Prepare

```json
{
  "name": "@scope/package",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": ["dist"],
  "repository": "github:user/repo",
  "publishConfig": {
    "access": "public"
  }
}
```

### Publish

```bash
npm login
npm publish
npm publish --access public  # Scoped packages

# Dry run
npm publish --dry-run
```

### Version Bump

```bash
npm version patch  # 1.0.0 -> 1.0.1
npm version minor  # 1.0.0 -> 1.1.0
npm version major  # 1.0.0 -> 2.0.0
```

## Useful Commands

```bash
npm ls                   # List installed
npm ls lodash            # Check specific
npm outdated             # Check outdated
npm why lodash           # Why installed
npm cache clean --force  # Clear cache
npm init -y              # Quick init
npm exec -- eslint .     # Run bin
npx create-react-app     # Run without install
```
