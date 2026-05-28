---
name: workspace-management
description: Manage pnpm workspaces, add packages, configure dependencies, and organize monorepo structure. Use when adding new packages, restructuring workspace, or managing cross-package dependencies.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Workspace Management Skill

This skill helps you manage the pnpm monorepo workspace structure and dependencies.

## When to Use This Skill

- Adding new packages to monorepo
- Configuring workspace dependencies
- Managing cross-package dependencies
- Restructuring workspace
- Sharing code between packages
- Setting up new apps or packages
- Managing workspace scripts

## Workspace Structure

```
sgcarstrends/
├── pnpm-workspace.yaml          # Workspace configuration
├── package.json                  # Root package.json
├── turbo.json                    # Turbo configuration
├── apps/
│   ├── api/                     # API service
│   ├── web/                     # Web application (includes admin at /admin)
│   └── docs/                    # Documentation
├── packages/
│   ├── database/                # Database schemas
│   ├── types/                   # Shared types
│   ├── ui/                      # UI components
│   ├── utils/                   # Utilities
│   └── logos/                   # Logo management
└── infra/                       # Infrastructure
```

## Workspace Configuration

### pnpm-workspace.yaml

```yaml
packages:
  - "apps/*"
  - "packages/*"
  - "infra"

catalog:
  # React ecosystem
  next: ^16.0.0
  react: ^19.0.0
  react-dom: ^19.0.0

  # Database
  drizzle-orm: ^0.30.0
  drizzle-kit: ^0.20.0
  postgres: ^3.4.3

  # TypeScript
  typescript: ^5.3.3
  "@types/node": ^20.11.5
  "@types/react": ^19.0.0

  # Build tools
  "@biomejs/biome": ^1.9.4
  turbo: ^2.3.3

  # Testing
  vitest: ^2.1.8
  "@playwright/test": ^1.49.1
```

## Adding New Package

### Create Package Structure

```bash
# Create package directory
mkdir -p packages/new-package/src

# Create package.json
cat > packages/new-package/package.json <<EOF
{
  "name": "@sgcarstrends/new-package",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    ".": {
      "types": "./src/index.ts",
      "default": "./src/index.ts"
    }
  },
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {},
  "devDependencies": {
    "typescript": "catalog:",
    "vitest": "catalog:"
  }
}
EOF
```

### Create TypeScript Config

```json
// packages/new-package/tsconfig.json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "__tests__"]
}
```

### Create Entry Point

```typescript
// packages/new-package/src/index.ts
export { myFunction } from "./my-function";
```

### Install Dependencies

```bash
# Install workspace dependencies
pnpm install

# Install package-specific dependency
pnpm -F @sgcarstrends/new-package add some-package
```

## Managing Dependencies

### Add Dependency to Package

```bash
# Add to specific package
pnpm -F @sgcarstrends/api add hono

# Add dev dependency
pnpm -F @sgcarstrends/web add -D tailwindcss

# Add from catalog
pnpm -F @sgcarstrends/web add typescript  # Automatically uses catalog:
```

### Add Workspace Dependency

```bash
# Add internal dependency
pnpm -F @sgcarstrends/web add @sgcarstrends/database

# package.json will have:
{
  "dependencies": {
    "@sgcarstrends/database": "workspace:*"
  }
}
```

### Add Dependency to All Packages

```bash
# Add to root (CLI tools)
pnpm add -w -D biome turbo

# Add to all workspaces
pnpm -r add some-package
```

### Remove Dependency

```bash
# Remove from specific package
pnpm -F @sgcarstrends/api remove lodash

# Remove from all packages
pnpm -r remove lodash

# Remove from root
pnpm remove -w lodash
```

## Cross-Package Dependencies

### Import from Workspace Package

```typescript
// apps/web/src/app/page.tsx
import { db } from "@sgcarstrends/database";
import { redis } from "@sgcarstrends/utils";
import { Button } from "@sgcarstrends/ui/components/button";

export default async function Page() {
  const cars = await db.query.cars.findMany();
  return <div>...</div>;
}
```

### TypeScript Path Mapping

```json
// tsconfig.json (root)
{
  "compilerOptions": {
    "paths": {
      "@sgcarstrends/database": ["./packages/database/src"],
      "@sgcarstrends/types": ["./packages/types/src"],
      "@sgcarstrends/ui": ["./packages/ui/src"],
      "@sgcarstrends/utils": ["./packages/utils/src"]
    }
  }
}
```

## Workspace Scripts

### Root package.json Scripts

```json
{
  "scripts": {
    // Development
    "dev": "turbo dev",
    "dev:api": "pnpm -F @sgcarstrends/api dev",
    "dev:web": "pnpm -F @sgcarstrends/web dev",

    // Build
    "build": "turbo build",
    "build:api": "pnpm -F @sgcarstrends/api build",
    "build:web": "pnpm -F @sgcarstrends/web build",

    // Testing
    "test": "turbo test",
    "test:watch": "turbo test:watch",
    "test:coverage": "turbo test:coverage",

    // Linting
    "lint": "biome check .",
    "lint:fix": "biome check --write .",

    // Database
    "db:generate": "pnpm -F @sgcarstrends/database db:generate",
    "db:migrate": "pnpm -F @sgcarstrends/database db:migrate",
    "db:push": "pnpm -F @sgcarstrends/database db:push",

    // Deployment
    "deploy:dev": "turbo deploy:dev",
    "deploy:staging": "turbo deploy:staging",
    "deploy:prod": "turbo deploy:prod"
  }
}
```

### Package-Specific Scripts

```json
// apps/api/package.json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "esbuild src/index.ts --bundle --platform=node --outfile=dist/index.js",
    "test": "vitest run",
    "test:watch": "vitest",
    "deploy:dev": "sst deploy --stage dev",
    "deploy:staging": "sst deploy --stage staging",
    "deploy:prod": "sst deploy --stage prod"
  }
}
```

## Turbo Configuration

### turbo.json

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"]
    },
    "test:watch": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "outputs": []
    },
    "deploy:dev": {
      "dependsOn": ["build"],
      "cache": false
    },
    "deploy:staging": {
      "dependsOn": ["build", "test"],
      "cache": false
    },
    "deploy:prod": {
      "dependsOn": ["build", "test", "lint"],
      "cache": false
    }
  }
}
```

## Common Operations

### List All Packages

```bash
# List workspace packages
pnpm list --depth 0

# List recursively
pnpm -r list

# List specific package
pnpm -F @sgcarstrends/api list
```

### Run Commands in Parallel

```bash
# Run dev in all packages
pnpm -r dev

# Build all packages
pnpm -r build

# Test all packages
pnpm -r test
```

### Filter by Package

```bash
# Run command in specific package
pnpm -F @sgcarstrends/api dev

# Run in multiple packages
pnpm -F @sgcarstrends/api -F @sgcarstrends/web build

# Run in all packages matching pattern
pnpm -F "@sgcarstrends/*" build
```

### Execute Script in All Packages

```bash
# Clean all packages
pnpm -r exec rm -rf node_modules dist .turbo .next

# Update all package versions
pnpm -r exec npm version patch
```

## Workspace Optimization

### Hoisting

```yaml
# .npmrc
hoist=true
hoist-pattern[]=*
shamefully-hoist=false
```

### Shared Dependencies

```yaml
# pnpm-workspace.yaml
catalog:
  # Shared across all packages
  typescript: ^5.3.3
  vitest: ^2.1.8
  biome: ^1.9.4

# package.json uses:
{
  "devDependencies": {
    "typescript": "catalog:",
    "vitest": "catalog:",
    "biome": "catalog:"
  }
}
```

### Node Modules Structure

```
node_modules/
├── .pnpm/                    # Virtual store
│   ├── next@16.0.0/
│   ├── react@19.0.0/
│   └── ...
├── @sgcarstrends/
│   ├── database -> ../packages/database
│   ├── types -> ../packages/types
│   └── ...
└── next -> .pnpm/next@16.0.0/node_modules/next
```

## Package Publishing

### Prepare for Publishing

```json
// packages/ui/package.json
{
  "name": "@sgcarstrends/ui",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "default": "./dist/index.js"
    },
    "./components/*": {
      "types": "./dist/components/*.d.ts",
      "default": "./dist/components/*.js"
    }
  },
  "files": [
    "dist",
    "README.md",
    "LICENSE"
  ],
  "scripts": {
    "build": "tsc",
    "prepublishOnly": "pnpm build"
  },
  "publishConfig": {
    "access": "public"
  }
}
```

### Publish Package

```bash
# Build package
pnpm -F @sgcarstrends/ui build

# Publish to npm
pnpm -F @sgcarstrends/ui publish

# Publish all changed packages
pnpm -r publish
```

## Troubleshooting

### Dependency Not Found

```bash
# Issue: Module not found @sgcarstrends/database
# Solution: Rebuild workspace

pnpm install

# Or rebuild specific package
pnpm -F @sgcarstrends/database build
```

### Circular Dependencies

```bash
# Issue: Circular dependency detected
# Solution: Refactor to break circle

# Bad:
# A depends on B
# B depends on A

# Good:
# A depends on C
# B depends on C
# C has shared code
```

### Hoisting Issues

```bash
# Issue: Package not found due to hoisting
# Solution: Add to .npmrc

# .npmrc
public-hoist-pattern[]=*react*
public-hoist-pattern[]=*next*
```

### Workspace Protocol Issues

```bash
# Issue: workspace:* not resolving
# Solution: Ensure package exists and is built

pnpm -F @sgcarstrends/database build
pnpm install
```

## Best Practices

### 1. Organize by Type

```
# ✅ Good organization
apps/          # User-facing applications
packages/      # Shared libraries
infra/         # Infrastructure code

# ❌ Poor organization
src/           # Mixed apps and packages
lib/           # Unclear purpose
```

### 2. Use Catalog for Shared Versions

```yaml
# ✅ Centralized versions
catalog:
  react: ^19.0.0
  typescript: ^5.3.3

# ❌ Duplicate versions
# Each package.json has different versions
```

### 3. Minimize Cross-Dependencies

```typescript
// ❌ Deep cross-dependencies
// web → api → database → types → utils → config

// ✅ Flat dependencies
// web → database, types, utils
// api → database, types, utils
```

### 4. Document Package Purpose

```markdown
# packages/ui/README.md

# @sgcarstrends/ui

Shared UI component library built with shadcn/ui and Tailwind CSS.

## When to Use

Use this package when you need to share UI components between web and admin apps.

## Examples

\```typescript
import { Button } from "@sgcarstrends/ui/components/button";
\```
```

## References

- pnpm Workspaces: https://pnpm.io/workspaces
- Turbo: https://turbo.build/repo/docs
- Monorepo Tools: https://monorepo.tools
- Related files:
  - `pnpm-workspace.yaml` - Workspace configuration
  - `turbo.json` - Turbo configuration
  - Root CLAUDE.md - Workspace guidelines

## Best Practices Summary

1. **Clear Structure**: Organize packages by type (apps, packages, infra)
2. **Use Catalog**: Centralize dependency versions
3. **Workspace Protocol**: Use `workspace:*` for internal dependencies
4. **Turbo Pipeline**: Configure build dependencies correctly
5. **Minimal Cross-Deps**: Avoid deep dependency chains
6. **Document Packages**: Clear README for each package
7. **Consistent Scripts**: Use same script names across packages
8. **Optimize Hoisting**: Configure hoisting for performance
