---
name: monorepo-structure
description: Set up a Turborepo + pnpm monorepo for sharing code between frontend, backend, and workers. One repo, multiple packages, shared types, parallel builds.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: foundations
  time: 2h
  source: drift-masterguide
---

# Monorepo Structure

One repo, multiple packages, shared types, parallel builds.

## When to Use This Skill

- Sharing code between frontend and backend
- Multiple apps need common types/utilities
- Want atomic commits across packages
- Tired of version hell with separate repos
- Need parallel builds with caching

## Core Concepts

1. **Workspaces** - pnpm manages multiple packages in one repo
2. **Turborepo** - Orchestrates builds with caching and parallelization
3. **Shared types** - Single source of truth for TypeScript types
4. **Build order** - Dependencies build before dependents

## Project Structure

```
project-root/
├── apps/
│   ├── web/                    # Next.js frontend
│   │   ├── app/
│   │   ├── components/
│   │   └── package.json
│   ├── api/                    # Backend API
│   │   ├── src/
│   │   └── package.json
│   └── worker/                 # Background worker
│       ├── src/
│       └── package.json
│
├── packages/
│   ├── types/                  # Shared TypeScript types
│   │   ├── src/
│   │   │   ├── index.ts
│   │   │   ├── user.ts
│   │   │   └── schemas.ts
│   │   └── package.json
│   ├── utils/                  # Shared utilities
│   │   └── package.json
│   └── config/                 # Shared configs (eslint, tsconfig)
│       └── package.json
│
├── package.json                # Root package.json
├── pnpm-workspace.yaml
├── turbo.json
└── tsconfig.base.json
```

## TypeScript Implementation

### pnpm-workspace.yaml

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

### Root package.json

```json
{
  "name": "my-saas",
  "private": true,
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "test": "turbo test",
    "lint": "turbo lint",
    "typecheck": "turbo typecheck",
    "clean": "turbo clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.4.0"
  },
  "packageManager": "pnpm@9.0.0"
}
```

### turbo.json

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "test": {
      "dependsOn": ["^build"]
    },
    "typecheck": {
      "dependsOn": ["^build"]
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "clean": {
      "cache": false
    }
  }
}
```

### tsconfig.base.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "resolveJsonModule": true,
    "isolatedModules": true
  }
}
```

### Shared Types Package

```json
// packages/types/package.json
{
  "name": "@myapp/types",
  "version": "0.0.1",
  "private": true,
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    }
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "typescript": "^5.4.0"
  },
  "dependencies": {
    "zod": "^3.23.0"
  }
}
```

```json
// packages/types/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
```

```typescript
// packages/types/src/index.ts
export * from './user';
export * from './schemas';
```

```typescript
// packages/types/src/user.ts
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'guest';
  createdAt: Date;
}

export interface CreateUserInput {
  email: string;
  name: string;
  role?: 'admin' | 'user' | 'guest';
}
```

```typescript
// packages/types/src/schemas.ts
import { z } from 'zod';

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.coerce.date(),
});

export const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
  role: z.enum(['admin', 'user', 'guest']).default('user'),
});
```

### App Package Using Shared Types

```json
// apps/web/package.json
{
  "name": "@myapp/web",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "@myapp/types": "workspace:*",
    "next": "^14.0.0",
    "react": "^18.0.0"
  }
}
```

```typescript
// apps/web/app/api/users/route.ts
import type { User, CreateUserInput } from '@myapp/types';
import { CreateUserSchema } from '@myapp/types';

export async function POST(request: Request) {
  const body = await request.json();
  
  // Validate with shared schema
  const input = CreateUserSchema.parse(body);
  
  // Create user...
  const user: User = await createUser(input);
  
  return Response.json(user);
}
```

### Shared Utils Package

```json
// packages/utils/package.json
{
  "name": "@myapp/utils",
  "version": "0.0.1",
  "private": true,
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "devDependencies": {
    "typescript": "^5.4.0"
  }
}
```

```typescript
// packages/utils/src/index.ts
export function formatDate(date: Date): string {
  return date.toISOString().split('T')[0];
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-');
}

export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
```

## Common Commands

```bash
# Install all dependencies
pnpm install

# Run all dev servers in parallel
pnpm dev

# Build everything (respects dependency order)
pnpm build

# Run tests across all packages
pnpm test

# Add dependency to specific package
pnpm add zod --filter @myapp/types

# Add dev dependency to root
pnpm add -D prettier -w

# Run command in specific package
pnpm --filter @myapp/web dev

# Run command in all packages matching pattern
pnpm --filter "@myapp/*" build
```

## Dependency Flow

```
packages/types (source of truth)
    ↓
packages/utils (may import types)
    ↓
apps/web, apps/api, apps/worker (import both)
```

Turborepo handles build order via `dependsOn: ["^build"]` - packages always build before apps that depend on them.

## .gitignore

```gitignore
# Dependencies
node_modules/

# Build outputs
dist/
.next/
.turbo/

# Environment
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/

# OS
.DS_Store
```

## Best Practices

1. **Use `workspace:*`** - Always for internal dependencies
2. **Types flow down** - Shared types package is the source of truth
3. **One tsconfig.base** - Extend from root, override only what's needed
4. **Atomic commits** - Change types and consumers in same commit
5. **Cache builds** - Turborepo caches unchanged packages

## Common Mistakes

- Using `^1.0.0` instead of `workspace:*` for internal deps
- Building packages individually instead of `turbo build`
- Circular dependencies between packages
- Not including `dist/` in `.gitignore`
- Forgetting `dependsOn: ["^build"]` in turbo.json

## Related Skills

- [TypeScript Strict](../typescript-strict/)
- [Environment Config](../environment-config/)
