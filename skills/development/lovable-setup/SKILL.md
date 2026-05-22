---
name: lovable-setup
description: |
  Debug and fix Lovable preview/build issues including white screens, module import failures,
  and monorepo configuration. Use when: (1) Lovable preview shows white/blank screen,
  (2) "Failed to fetch dynamically imported module" errors, (3) Missing script errors,
  (4) PostCSS/Tailwind resolution failures, (5) Workspace package resolution errors,
  (6) 504 Gateway Timeout on dependencies, (7) Setting up monorepo for Lovable deployment.
  Triggers: "lovable broken", "white screen", "preview not loading", "lovable build failed",
  "dynamic import error", "module not found lovable".
---

# Lovable Setup & Debugger

## Diagnostic Workflow

```
1. GET ERROR    → User provides error message or screenshot
2. ASK USER     → Request browser console info (see "What to Ask User" below)
3. DIFF CHECK   → Compare user files to working examples (see references/working-examples.md)
4. CATEGORIZE   → Match to error pattern below (or case study)
5. FIX          → Apply corresponding solution
6. VERIFY       → Build locally, push, refresh Lovable
```

**For complex issues**:
- Read `references/working-examples.md` for complete working file examples to diff against
- Read `references/case-studies.md` for real debugging examples with symptoms and fixes

## What to Ask User

When user reports "white screen" or "not loading", ask them to check browser DevTools:

1. **Console tab**: Any JavaScript errors?
2. **Network tab**: Any requests with non-200 status codes?
   - 404 = Missing file
   - 500 = Server/build error
   - 504 = Dependency timeout (needs optimizeDeps fix)

This info immediately narrows down the issue category.

## Error Categories & Fixes

### Supabase Types Out of Sync

**Error**: TypeScript errors referencing missing tables, RPC functions, or columns

**Cause**: `types.ts` not regenerated after database migrations

**Fix**:
```bash
npx supabase gen types typescript --project-id iryqgmjauybluwnqhxbg > apps/raamattu-nyt/src/integrations/supabase/types.ts
git add apps/raamattu-nyt/src/integrations/supabase/types.ts
git commit -m "chore: Regenerate Supabase types"
git push
```

**Workaround** (when regeneration not possible):
```typescript
// biome-ignore lint/suspicious/noExplicitAny: RPC not in generated types
const { data, error } = await supabase.rpc("new_function" as any, { p_id: id });
```

**See also**: `/supabase-migration-writer` skill for migration best practices.

### White Screen / Dynamic Import Failure

**Error**: `Failed to fetch dynamically imported module: .../AppEntry.tsx`

**Diagnosis**:
```bash
# Check TypeScript
npm run typecheck --workspace=apps/raamattu-nyt

# Check build
npm run build --workspace=apps/raamattu-nyt
```

**Common causes & fixes**:

| Cause | Fix |
|-------|-----|
| Re-export syntax | Change `export { default } from "./App"` to `import App from "./App"; export default App;` |
| Missing dependency in root | Add to root `package.json` dependencies, not just app |
| Lock file out of sync | `rm package-lock.json && npm install && git add package-lock.json && git push` |
| Schema not in types | Add `.schema("schema_name")` when querying non-public schemas |

**AppEntry.tsx Pattern** (Lovable's entry point):
```tsx
// apps/raamattu-nyt/src/AppEntry.tsx
import App from "./App";
export default App;
```

### 504 Gateway Timeout on Dependencies

**Error**: `GET .../node_modules/.vite/deps/[package].js 504 (Gateway Timeout)`

**Cause**: Lovable server timeout during dependency pre-bundling.

**Fix**: Add problematic dependency to `optimizeDeps.include` in vite.config.ts:
```typescript
optimizeDeps: {
  include: [
    "react",
    "react-dom",
    "framer-motion",  // Add timeout-causing package here
  ],
}
```

### Missing Script

**Error**: `npm error Missing script: "build:dev"`

**Fix**: Add delegation scripts to root `package.json`:
```json
{
  "scripts": {
    "dev": "npm run dev --workspace=apps/[app-name]",
    "build": "npm run build --workspace=apps/[app-name]",
    "build:dev": "npm run build:dev --workspace=apps/[app-name]"
  }
}
```

### PostCSS/Tailwind Resolution

**Error**: `[plugin:vite:css] [postcss] Cannot find package 'postcss'` or `Cannot find module 'tailwindcss'`

**Cause**: Build toolchain dependency not available in Lovable preview (installs only production deps).

**Quick fix**:
```bash
# Add to root package.json dependencies (not devDependencies)
npm install --save postcss autoprefixer tailwindcss
git add package.json package-lock.json
git push
```

**Full playbook**: See `references/postcss-white-screen-playbook.md` for complete triage checklist covering:
- Dependency placement verification
- Lockfile consistency
- PostCSS config conflicts (root vs app-level)
- Tailwind v4 plugin requirements
- Prevention guardrails

### Workspace Package Resolution

**Error**: `Rollup failed to resolve import "react/jsx-runtime"`

**Fix**: Update `vite.config.ts`:
```typescript
optimizeDeps: {
  include: ["react", "react-dom", "react/jsx-runtime"],
},
build: {
  commonjsOptions: {
    include: [/packages\/.*/, /node_modules/],
  },
},
```

### Lock File Out of Sync

**Error**: `npm ci can only install packages when package.json and package-lock.json are in sync`

**Fix**:
```bash
rm package-lock.json
npm install
git add package-lock.json
git commit -m "Refresh package-lock.json"
git push
```

### Schema Query Errors

**Error**: `Could not find the table 'public.table_name' in the schema cache`

**Fix**: Add `.schema()` before `.from()`:
```typescript
// Before (wrong - queries public schema)
const { data } = await supabase.from("table_name").select("*");

// After (correct - queries specific schema)
const { data } = await (supabase as any)
  .schema("bible_schema")
  .from("table_name")
  .select("*");
```

## Quick Diagnostic Commands

```bash
# 1. Check if code compiles
npm run typecheck --workspace=apps/raamattu-nyt

# 2. Check if build works
npm run build --workspace=apps/raamattu-nyt

# 3. Check lock file sync
npm ci --dry-run

# 4. Check workspace structure
npm ls --depth=0

# 5. Find missing dependencies
npm ls 2>&1 | grep -E "missing|extraneous"
```

## Vite Config Template

Complete `vite.config.ts` for Lovable monorepo:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

export default defineConfig(({ mode }) => ({
  plugins: [react(), mode === "development" && componentTagger()].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@ui": path.resolve(__dirname, "../../packages/ui/src"),
      "@shared-auth": path.resolve(__dirname, "../../packages/shared-auth/src"),
    },
  },
  optimizeDeps: {
    include: [
      "react",
      "react-dom",
      "react/jsx-runtime",
      "framer-motion",
      // Add any packages that cause 504 timeouts
    ],
  },
  build: {
    commonjsOptions: {
      include: [/packages\/.*/, /node_modules/],
    },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
}));
```

## Test Mock Updates

When adding `.schema()` calls, update test mocks:

```typescript
// Mock Supabase with schema() support
vi.mock("@/integrations/supabase/client", () => ({
  supabase: {
    schema: (_schemaName: string) => ({
      from: (table: string) => ({
        select: () => ({ or: () => ({ maybeSingle: () => mockData }) }),
        upsert: () => Promise.resolve({ error: null }),
      }),
    }),
  },
}));
```

## Lovable-Specific Notes

- Lovable uses `AppEntry.tsx` as dynamic import entry point
- Editor runtime: `/projects/...` uses dynamic ESM imports
- Preview: `id-preview--*.lovable.app` is built bundle
- Dependencies must be in root `package.json` for Lovable to install them
- Use "Rebuild" in Lovable UI to clear cache
- 504 errors = Lovable infrastructure issue, retry or add to optimizeDeps

## Pre-Push Checklist

**Before pushing, always run:**
```bash
npm ci --dry-run
```
This catches lockfile drift which is the #1 cause of Lovable white screens.

## Health Check Page

A `/health` page exists (`src/main.tsx`) for diagnosing white screens:

| /health result | Meaning |
|----------------|---------|
| Green ✅ visible | Preview serves static files, but React app crashes during initialization |
| Page doesn't load | Preview isn't serving at all (build/deploy issue) |

Use this to quickly distinguish between:
1. **React crash** (health shows ✅) → Check console for JS errors, likely code bug
2. **Build/serve failure** (health doesn't load) → Check lockfile, deps, PostCSS

## Reference Files

- **`Docs/16-DEBUG-LOVABLE-WHITE.md`** - Comprehensive white screen playbook (project-level docs):
  - Golden rule: white screen ≠ UI bug
  - Root causes ranked by frequency
  - Step-by-step fix checklist
  - Prevention strategies (CI guardrails)
  - Runtime error logging architecture (globalErrorLogger, DebugErrorOverlay)
  - /health page diagnostics

- **`references/postcss-white-screen-playbook.md`** - Complete triage for "Cannot find package 'postcss'" errors:
  - Root cause analysis (dependency placement, Tailwind v4, config conflicts)
  - Step-by-step verification checklist
  - Quick fix commands
  - Prevention guardrails (CI checks, single config rule)
  - AI agent prompt for automated diagnosis

- **`references/working-examples.md`** - Complete working configuration files for diffing:
  - AppEntry.tsx (correct vs incorrect patterns)
  - vite.config.ts (full working template)
  - package.json (root and app versions)
  - tsconfig.json (paths configuration)
  - postcss.config.js (correct location)
  - Diff checklist for quick comparison

- **`references/case-studies.md`** - Real debugging sessions (10 case studies):
  - Case 1: 504 Gateway Timeout → optimizeDeps fix
  - Case 2: AppEntry.tsx dynamic import failure → export pattern fix
  - Case 3: Schema query error → `.schema()` fix
  - Case 4: Package lock out of sync → regenerate lock file
  - Case 5: Vite root misconfigured → remove custom root
  - Case 6: Security headers blocking imports → conditional headers
  - Case 7: Missing error boundary → silent crash, add boundary
  - Case 8: Dependency in workspace only → move to root
  - Case 9: Incorrect base path → conditional base config
  - Case 10: Service worker caching old chunk → disable SW in dev
  - User Debugging Guide: How users can help diagnose issues

## Quick Pattern Matching

| Error Signal | Likely Fix |
|--------------|------------|
| `[postcss] Cannot find package 'postcss'` | **PostCSS playbook** - deps in root package.json |
| `/health` shows ✅ but app white | React crash - check console for JS errors |
| `/health` doesn't load | Build/serve failure - check lockfile, deps |
| 504 status code | Case 1: optimizeDeps |
| `Failed to fetch dynamically imported module` | Case 2: AppEntry export |
| `PGRST205` / table not found | Case 3: schema() |
| `npm ci` sync error | Case 4: lock file |
| MIME type "text/html" for JS | Case 5: Vite root |
| `Cross-Origin-Opener-Policy` | Case 6: security headers |
| Uncaught exception, silent white screen | Case 7: error boundary |
| `Failed to resolve module` (local works) | Case 8: root deps |
| 404 on `/assets/...` | Case 9: base path |
| Works in incognito only | Case 10: service worker |
