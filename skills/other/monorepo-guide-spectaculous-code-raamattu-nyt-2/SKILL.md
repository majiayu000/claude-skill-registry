---
name: monorepo-guide
description: Guide for working with the Raamattu Nyt monorepo structure. Use when creating new packages, adding apps, managing workspace dependencies, understanding import patterns, or troubleshooting monorepo issues. Covers npm workspaces, shared packages, cross-app code sharing, and Lovable Cloud deployment.
---

# Monorepo Guide

## Context Files (Read First)

For structure and conventions, read from `Docs/context/`:
- `Docs/context/repo-structure.md` - Monorepo layout
- `Docs/context/packages-map.md` - Package index and boundaries
- `Docs/context/conventions.md` - Naming and architecture rules

## Quick Reference

### Import Patterns
```typescript
import { useAuth } from "@shared-auth/hooks/useAuth";
import { Button } from "@ui/button";
import { supabase } from "@/integrations/supabase/client";
```

### Dependency Commands
```bash
# Add to root (shared)
npm install <pkg> -w root

# Add to specific app
npm install <pkg> -w apps/raamattu-nyt

# Add to package
npm install <pkg> -w packages/shared-auth

# Always commit package-lock.json after changes
```

### Common Commands
```bash
npm run dev          # Start dev server (port 5173)
npm run build        # Production build
npm test             # Run tests in apps/raamattu-nyt
npx @biomejs/biome check --write .  # Lint & format
```

## Creating New Packages

### 1. Create Package Structure
```bash
mkdir -p packages/my-package/src
```

### 2. Add package.json
```json
{
  "name": "@raamattu-nyt/my-package",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": {
    "./*": "./src/*"
  }
}
```

### 3. Create Index Export
```typescript
// packages/my-package/src/index.ts
export * from './hooks/useMyHook';
export * from './utils/myUtil';
```

### 4. Add Path Alias
In `apps/raamattu-nyt/vite.config.ts`:
```typescript
resolve: {
  alias: {
    "@my-package": path.resolve(__dirname, "../../packages/my-package/src"),
  }
}
```

In `apps/raamattu-nyt/tsconfig.json`:
```json
{
  "compilerOptions": {
    "paths": {
      "@my-package/*": ["../../packages/my-package/src/*"]
    }
  }
}
```

### 5. Use in App
```typescript
import { useMyHook } from "@my-package/hooks/useMyHook";
```

## Creating New Apps

### 1. Scaffold App
```bash
mkdir -p apps/new-app/src
```

### 2. Add Package Dependencies
```json
{
  "name": "new-app",
  "dependencies": {
    "@raamattu-nyt/shared-auth": "*",
    "@raamattu-nyt/ui": "*"
  }
}
```

### 3. Configure Vite & TypeScript
Copy and adapt from `apps/raamattu-nyt/`:
- `vite.config.ts` - Path aliases
- `tsconfig.json` - Path mappings

### 4. Share Supabase Client
Import from shell or create app-specific client pointing to same project.

## Troubleshooting

### "packages not in sync"
```bash
npm install  # Regenerate lockfile
git add package-lock.json && git commit
```

### Import Resolution Errors
1. Check path alias in `vite.config.ts`
2. Check paths in `tsconfig.json`
3. Ensure package has proper `exports` field

### Build Fails with Type Errors
```bash
# Check if tsconfig includes all needed files
npx tsc --noEmit
```

**Cross-cutting learnings:** See `.claude/LEARNINGS.md` → "Monorepo/Package Management" section for package resolution patterns.

## References

- **Context docs**: `Docs/context/` (authoritative source)
- **CI/CD details**: See [references/ci-cd.md](references/ci-cd.md) for workflow configuration
