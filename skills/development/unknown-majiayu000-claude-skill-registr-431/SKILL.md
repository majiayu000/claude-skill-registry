---
name: innozverse-repo-structure
description: Navigate and understand the innozverse repository structure, file organization, naming conventions, and module boundaries. Use when creating new files, organizing code, or understanding where to add features.
---

# innozverse Repository Structure Skill

When navigating and modifying the innozverse repository, follow these structure conventions.

## Top-Level Structure

```
innozverse/
├── apps/                 # Applications
├── packages/             # Shared packages
├── docs/                 # Documentation
├── .claude/              # Claude AI skills
├── .github/              # GitHub workflows
├── package.json          # Root package.json
├── pnpm-workspace.yaml   # pnpm workspace config
├── turbo.json            # Turborepo config
└── README.md             # Main README
```

## Apps Directory

### apps/web (Next.js)
```
apps/web/
├── src/
│   └── app/              # App Router pages
│       ├── layout.tsx    # Root layout
│       ├── page.tsx      # Home page
│       └── globals.css   # Global styles
├── public/               # Static assets
├── next.config.js        # Next.js config
├── tsconfig.json         # TypeScript config
├── .eslintrc.json        # ESLint config
├── .env.example          # Environment template
└── package.json          # Package dependencies
```

**Key Points**:
- Use App Router (not Pages Router)
- Pages in `src/app/`
- Static files in `public/`
- Environment vars start with `NEXT_PUBLIC_`

### apps/api (Fastify)
```
apps/api/
├── src/
│   ├── index.ts          # Server entry point
│   └── routes/
│       ├── health.ts     # Health check route
│       └── v1/           # Versioned API routes
│           └── index.ts  # v1 routes
├── Dockerfile            # Fly.io deployment
├── fly.toml              # Fly.io config
├── tsconfig.json         # TypeScript config
├── .eslintrc.js          # ESLint config
├── .env.example          # Environment template
└── package.json          # Package dependencies
```

**Key Points**:
- Routes organized by version (`v1/`, `v2/`)
- Health check at root level
- Dockerfile for Fly.io deployment
- Environment vars in `.env` (never commit)

### apps/mobile (Flutter)
```
apps/mobile/
├── lib/
│   ├── main.dart         # App entry point
│   └── services/
│       └── api_service.dart  # API client
├── android/              # Android-specific
├── ios/                  # iOS-specific
├── pubspec.yaml          # Dart dependencies
├── README.md             # Mobile-specific docs
└── analysis_options.yaml # Dart linter config
```

**Key Points**:
- Main app in `lib/main.dart`
- Services in `lib/services/`
- Models in `lib/models/` (when added)
- Widgets in `lib/widgets/` (when added)

## Packages Directory

### packages/shared
```
packages/shared/
├── src/
│   ├── index.ts          # Main export
│   ├── types.ts          # Type definitions
│   ├── schemas.ts        # Zod schemas
│   └── constants.ts      # Shared constants
├── dist/                 # Compiled output (gitignored)
├── tsconfig.json
├── .eslintrc.js
└── package.json
```

**Purpose**: Domain types, Zod schemas, shared constants

**Usage**:
```typescript
import { HealthResponse, healthResponseSchema } from '@innozverse/shared';
```

### packages/api-client
```
packages/api-client/
├── src/
│   └── index.ts          # API client implementation
├── dist/                 # Compiled output (gitignored)
├── tsconfig.json
├── .eslintrc.js
└── package.json
```

**Purpose**: Typed HTTP client for web app

**Usage**:
```typescript
import { ApiClient } from '@innozverse/api-client';
const client = new ApiClient('http://localhost:8080');
```

### packages/config
```
packages/config/
├── eslint-preset.js      # Shared ESLint config
├── tsconfig.base.json    # Base TypeScript config
└── package.json
```

**Purpose**: Shared tooling configuration

**Usage**:
```json
// tsconfig.json
{
  "extends": "@innozverse/config/tsconfig.base.json"
}
```

## Documentation

```
docs/
├── architecture.md       # System architecture
├── conventions.md        # Coding conventions
├── deployment-flyio.md   # Fly.io deployment
└── contracts.md          # API contracts strategy
```

## File Naming Conventions

### TypeScript
- **Files**: `kebab-case.ts` (e.g., `api-client.ts`)
- **React Components**: `PascalCase.tsx` (e.g., `Button.tsx`)
- **Tests**: `*.test.ts` or `*.test.tsx`
- **Types**: `types.ts` or `<module>.types.ts`

### Dart
- **Files**: `snake_case.dart` (e.g., `api_service.dart`)
- **Tests**: `*_test.dart`

### Configuration
- **ESLint**: `.eslintrc.js` or `.eslintrc.json`
- **TypeScript**: `tsconfig.json`
- **Environment**: `.env.example` (committed), `.env` (gitignored)

## Where to Add New Code

### New API Endpoint
```
apps/api/src/routes/v1/users.ts  # New endpoint file
```

Update `apps/api/src/routes/v1/index.ts` to register

### New Shared Type
```
packages/shared/src/types.ts  # Add interface
packages/shared/src/schemas.ts  # Add Zod schema
```

Export from `packages/shared/src/index.ts`

### New Web Page
```
apps/web/src/app/users/page.tsx  # New page at /users
```

### New Mobile Screen
```
apps/mobile/lib/screens/users_screen.dart  # New screen
```

### New Shared Utility
```
packages/shared/src/utils/helper.ts  # New utility
```

Export from `packages/shared/src/index.ts`

## Import Paths

### Within innozverse Packages
```typescript
// ✅ Use package name
import { HealthResponse } from '@innozverse/shared';

// ❌ Don't use relative paths across packages
import { HealthResponse } from '../../../packages/shared/src/types';
```

### Within the Same Package
```typescript
// ✅ Use relative imports
import { helper } from './utils/helper';

// ❌ Don't use absolute package imports for same package
import { helper } from '@innozverse/shared/utils/helper';
```

### Next.js @ Alias
```typescript
// In apps/web only
import { Component } from '@/app/components/Component';
```

## Build Artifacts

### What's Gitignored
```
node_modules/
dist/
.next/
.turbo/
build/
.env
.env.local
*.log
```

### What's Committed
```
src/
public/
package.json
tsconfig.json
.env.example
README.md
```

## Scripts Organization

### Root package.json
- `dev`: Run web + API
- `build`: Build all packages and apps
- `lint`: Lint everything
- `test`: Run all tests

### Individual Packages
- `dev`: Start dev server
- `build`: Build package
- `lint`: Lint package
- `typecheck`: Type check

## Adding New Packages

1. **Create directory**: `mkdir packages/new-package`
2. **Initialize**: `cd packages/new-package && pnpm init`
3. **Name**: Use `@innozverse/` prefix
4. **Add to workspace**: Already covered by `packages/*` in `pnpm-workspace.yaml`
5. **Build config**: Copy `tsconfig.json` from similar package
6. **Add scripts**: `build`, `lint`, `typecheck`

## Directory Depth Guidelines

### Maximum Nesting
- **Apps**: 3-4 levels deep
  ```
  apps/web/src/app/users/[id]/page.tsx  ✅
  ```

- **Packages**: 2-3 levels deep
  ```
  packages/shared/src/utils/validation.ts  ✅
  ```

### When to Create Subdirectories
- **3+ related files**: Create a subdirectory
- **Single file**: Keep at current level
- **Shared concern**: Extract to `utils/` or `lib/`

## Module Boundaries

### Apps Cannot Import from Other Apps
```typescript
// ❌ Never do this
import { something } from '../../api/src/utils';
```

### Apps Can Import from Packages
```typescript
// ✅ This is fine
import { HealthResponse } from '@innozverse/shared';
```

### Packages Can Import from Other Packages
```typescript
// ✅ This is fine (with workspace dependency)
import { schema } from '@innozverse/shared';
```

## Special Directories

### .claude/skills/
AI agent instructions for project-specific patterns

### .github/workflows/
GitHub Actions CI/CD pipelines

### public/ (in apps/web)
Static assets served at root URL

### dist/ (in packages)
Compiled TypeScript output (gitignored, created on build)
