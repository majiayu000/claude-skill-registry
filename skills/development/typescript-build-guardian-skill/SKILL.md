---
name: typescript-build-guardian
description: Offensive TypeScript build pipeline optimization and validation. Triggered when reviewing tsconfig.json, TypeScript compilation errors, build performance issues, strict mode migration, module resolution problems, or preparing TypeScript projects for production. Framework-aware (Next.js/Remix). Scans for build output completeness, configuration issues, type safety opportunities, and performance bottlenecks. Produces auto-scan reports with migration paths.
---

# TypeScript Build Guardian

**Mission:** Prevent TypeScript build failures and optimize compilation pipelines through proactive scanning and evidence-based recommendations. This skill operates in **offensive mode** - finding type safety improvements and performance gains, not just catching errors.

## Activation Triggers

- User mentions tsconfig.json review
- TypeScript compilation errors
- "Should I enable strict mode?"
- Build performance issues
- Module resolution errors
- Pre-production TypeScript validation
- Import/export problems
- Source map debugging issues

## Framework Awareness

This skill understands framework-specific TypeScript configurations:

- **Next.js**: App Router vs Pages Router, server components, `next.config.js` integration
- **Remix**: Route modules, loader/action types, `.server` files
- **Pure Node.js**: Backend services, no framework
- **Express + TypeScript**: API servers, middleware typing

Claude should ask which framework if unclear from context.

## Scan Methodology

### 1. Initial Context Gathering

**Ask if not provided:**
- "What framework are you using?" (Next.js/Remix/Express/other)
- "Show me your tsconfig.json"
- "Show me your package.json" (to identify dependencies)
- "What build errors are you seeing?" (if any)
- "Are you using any template engines?" (EJS, Pug, Handlebars)

### 2. Critical Build Pipeline Scan

Execute ALL checks in this section. Each is based on real production incidents.

#### 🔴 CRITICAL: Build Output Completeness
**Historical Failure:** TypeScript doesn't copy .ejs files, causing production template rendering failures

**Scan for:**
- [ ] Template files (.ejs, .pug, .hbs) - are they copied to output?
- [ ] Static JSON files (configs, i18n) - are they in dist/?
- [ ] Public assets referenced by code - are they accessible?
- [ ] Package.json "files" field - does it include necessary assets?

**Red flags:**
- Only .ts/.tsx files in src/, but templates exist
- No copy script in package.json
- tsconfig excludes necessary files
- outDir doesn't match what gets deployed

**Optimization:**
```json
// package.json - Add copy script
{
  "scripts": {
    "build": "tsc && npm run copy-assets",
    "copy-assets": "cp -r src/views dist/ && cp -r src/public dist/"
  }
}
```

```javascript
// Or use build tool (tsup, esbuild)
// tsup.config.ts
export default {
  entry: ['src/index.ts'],
  loader: {
    '.ejs': 'copy',
    '.json': 'copy'
  }
}
```

**Framework-specific notes:**
- **Next.js**: Uses `public/` folder automatically, but check API routes for server-side templates
- **Remix**: Check `app/` folder structure, `.server` files need special handling
- **Express**: Manually copy views folder (this is the historical incident)

#### 🔴 CRITICAL: tsconfig.json Configuration
**Historical Failure:** Misconfigured paths cause import errors in production

**Scan for:**
- [ ] `outDir` matches deployment expectations
- [ ] `rootDir` correctly set (or left unset if flat structure)
- [ ] `moduleResolution` appropriate for Node.js ("node16" or "bundler")
- [ ] `esModuleInterop` enabled (prevents import quirks)
- [ ] `skipLibCheck` set to true (performance, avoids type conflicts)
- [ ] `target` matches Node.js version or browser support

**Red flags:**
- `outDir: "build"` but Dockerfile copies `dist/`
- `paths` with aliases but no `baseUrl`
- `module: "commonjs"` with ESM imports
- Missing `types` for @types packages
- `strict: true` when code has 45+ errors (too aggressive)

**Optimization for Next.js:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "ES2022"],
    "jsx": "preserve",
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "incremental": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "strict": false,  // Migrate gradually
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
```

**Optimization for Remix:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "jsx": "react-jsx",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "types": ["@remix-run/node", "vite/client"],
    "isolatedModules": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "strict": false,  // Migrate gradually
    "paths": {
      "~/*": ["./app/*"]
    }
  }
}
```

#### 🟡 HIGH: Strict Mode Migration Path
**Historical Failure:** Enabling strict mode all at once revealed 45 errors, blocking development

**Scan for:**
- [ ] Current strictness level
- [ ] Number of type errors if strict enabled
- [ ] Which strict flags are most impactful

**Red flags:**
- `strict: true` with 45+ errors (too aggressive)
- All strict flags disabled (missing safety)
- No plan to improve type safety

**Offensive Migration Strategy:**

**Phase 1: Low-hanging fruit (Enable immediately)**
```json
{
  "compilerOptions": {
    "strict": false,
    "noImplicitAny": true,           // ✅ Start here
    "strictFunctionTypes": true,      // ✅ Low impact
    "esModuleInterop": true,          // ✅ Import safety
    "skipLibCheck": true              // ✅ Performance win
  }
}
```

**Phase 2: Gradual tightening (1-2 weeks)**
```json
{
  "compilerOptions": {
    "noImplicitAny": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,      // ➕ Add this
    "strictPropertyInitialization": true  // ➕ Add this
  }
}
```

**Phase 3: Full strict (When ready)**
```json
{
  "compilerOptions": {
    "strict": true  // Equivalent to all flags enabled
  }
}
```

**Impact analysis:**
- `noImplicitAny`: Catches ~60% of type bugs with minimal refactoring
- `strictNullChecks`: Catches ~30% but requires significant refactoring
- `strictPropertyInitialization`: Low value in Next.js/Remix (class components rare)

**Recommendation:** Start with Phase 1, fix errors over 2 weeks, then move to Phase 2.

#### 🟡 HIGH: Module Resolution Nightmares
**Historical Pattern:** Import errors that work in dev but fail in production

**Scan for:**
- [ ] Path aliases configured correctly (`@/`, `~/`)
- [ ] `baseUrl` set when using `paths`
- [ ] Consistent import styles (ESM vs CommonJS)
- [ ] Extension handling (.js vs .ts in imports)
- [ ] Barrel exports creating circular dependencies

**Red flags:**
```typescript
// ❌ Extension in import (breaks some bundlers)
import { foo } from './utils.ts'

// ❌ Mixing default and named imports inconsistently
import express from 'express'
import * as express from 'express'

// ❌ Path alias without baseUrl
// tsconfig: { "paths": { "@/*": ["src/*"] } }
// Missing: "baseUrl": "."

// ❌ Circular dependency via barrel export
// src/index.ts exports from src/utils.ts
// src/utils.ts imports from src/index.ts
```

**Optimization:**
```json
// tsconfig.json - Proper path aliases
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}
```

```typescript
// ✅ Consistent import style
import express from 'express'  // Default export
import { Router } from 'express'  // Named export

// ✅ No extensions in imports
import { foo } from './utils'  // Not ./utils.ts

// ✅ Avoid deep barrel exports
// Instead of: src/components/index.ts exporting everything
// Use direct imports: import { Button } from '@components/Button'
```

**Framework-specific:**
- **Next.js**: `@/*` alias configured by default in `tsconfig.json`
- **Remix**: `~/*` is convention for `app/` folder
- **Express**: Manual `paths` configuration required

#### 🟠 MEDIUM: Source Map Configuration
**Historical Issue:** Can't debug production builds due to missing source maps

**Scan for:**
- [ ] `sourceMap: true` in tsconfig.json
- [ ] Source maps deployed with production build
- [ ] Source map paths resolve correctly
- [ ] Debugging works in production

**Red flags:**
- `sourceMap: false` (can't debug)
- Source maps in .gitignore (won't deploy)
- `inlineSourceMap: true` in production (security risk - exposes source code)

**Optimization:**
```json
// Development
{
  "compilerOptions": {
    "sourceMap": true,
    "inlineSourceMap": false
  }
}

// Production (separate build config)
{
  "compilerOptions": {
    "sourceMap": true,        // External source maps
    "inlineSourceMap": false, // Never inline in production
    "declarationMap": true    // For libraries
  }
}
```

**Security consideration:** Don't deploy source maps to public production if you want to protect IP. Upload to error tracking services (Sentry) instead.

#### 🟠 MEDIUM: Build Performance
**Historical Issue:** Slow TypeScript compilation blocking development

**Scan for:**
- [ ] Incremental compilation enabled
- [ ] `skipLibCheck: true` (huge performance win)
- [ ] Project references for monorepos
- [ ] Unnecessary `include` patterns

**Red flags:**
- `skipLibCheck: false` (slow, unnecessary)
- No `incremental: true` (rebuilds from scratch)
- Including `node_modules` in compilation
- No `.tsbuildinfo` in .gitignore

**Optimization:**
```json
{
  "compilerOptions": {
    "incremental": true,      // ✅ 2-5x faster rebuilds
    "skipLibCheck": true,     // ✅ 10-50% faster builds
    "tsBuildInfoFile": ".tsbuildinfo"
  },
  "exclude": [
    "node_modules",
    "dist",
    ".next",
    "build"
  ]
}
```

**Advanced: Project References (Monorepos)**
```json
// packages/shared/tsconfig.json
{
  "compilerOptions": { "composite": true },
  "references": []
}

// apps/api/tsconfig.json
{
  "references": [
    { "path": "../../packages/shared" }
  ]
}
```

**Build time expectations:**
- Small project (<100 files): <3s
- Medium project (100-500 files): <10s
- Large project (500+ files): <30s with incremental

If slower, investigate with `tsc --diagnostics`.

#### 🟢 LOW: Linting & Formatting Integration
**Not failure-critical but improves team workflow**

**Scan for:**
- [ ] ESLint configured for TypeScript
- [ ] Prettier integrated
- [ ] Pre-commit hooks (Husky + lint-staged)
- [ ] IDE settings shared (.vscode/settings.json)

**Optimization:**
```json
// .eslintrc.json
{
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  }
}
```

### 3. Cross-Reference: Docker Integration

**If Docker skill is also active**, validate that TypeScript build outputs match Docker expectations:

```markdown
⚠️ CROSS-SKILL ALERT: Docker + TypeScript

Your TypeScript config outputs to: `dist/`
Your Dockerfile copies from: `dist/`  ✅ Match!

But TypeScript doesn't copy:
- src/views/*.ejs (missing in dist/)
- src/public/* (missing in dist/)

ACTION: Add copy script or update Dockerfile:
  COPY views/ /app/views/
  COPY public/ /app/public/
```

### 4. Production Readiness Checklist

Generate this checklist in the auto-scan report:

```
TYPESCRIPT BUILD READINESS SCORE: X/10

✅ tsconfig.json properly configured
✅ Build output includes all necessary files
✅ Source maps enabled for debugging
✅ Incremental compilation enabled
⚠️  Strict mode partially enabled (migration in progress)
⚠️  Some path aliases not in baseUrl
❌ Missing: Copy script for .ejs templates
❌ Critical: Import errors in 3 files
❌ Performance: Build time >60s (should be <30s)

RISK LEVEL: [LOW/MEDIUM/HIGH/CRITICAL]
BLOCKERS: X critical issues must be resolved
OPTIMIZATIONS: Y performance wins available
```

## Output Format: Auto-Scan Report

```
═══════════════════════════════════════════════
🛡️ TYPESCRIPT BUILD GUARDIAN - SCAN RESULTS
═══════════════════════════════════════════════

📊 SCAN SCOPE
• Framework: Next.js 14 (App Router)
• TypeScript: 5.3.2
• tsconfig: Found
• Build time: 45s (target: <30s)

🚨 CRITICAL FINDINGS: [count]
[List each critical issue with:
 - What's wrong
 - Why it's dangerous (cite historical incident)
 - How to fix (code example)]

⚠️  HIGH PRIORITY: [count]
[Same format as critical]

💡 OPTIMIZATIONS: [count]
[Performance improvements, type safety upgrades]

🎯 STRICT MODE MIGRATION PATH:
Current: Phase 0 (no strict flags)
Recommendation: Enable Phase 1 flags (noImplicitAny, strictFunctionTypes)
Estimated errors: ~12 (fixable in 2-3 hours)
Full strict timeline: 2-3 weeks

⚡ PERFORMANCE ANALYSIS:
Current build time: 45s
With skipLibCheck: ~30s (33% faster)
With incremental: ~20s (56% faster)
Target achieved: 20s < 30s ✅

═══════════════════════════════════════════════
FINAL VERDICT
═══════════════════════════════════════════════
Production Ready: [YES/NO/BLOCKED]
Risk Level: [LOW/MEDIUM/HIGH/CRITICAL]
Estimated Fix Time: [X hours]

NEXT ACTIONS:
1. [Most critical fix]
2. [Second priority]
3. [Optional optimization]

═══════════════════════════════════════════════
```

## Reference Materials

For detailed error patterns and historical incidents, see:
- `references/error-patterns.md` - TypeScript incident database with resolutions
- `references/strict-mode-migration.md` - Comprehensive strict mode migration guide

## Advanced Scanning

**When to escalate:**
- User says "comprehensive TypeScript audit"
- Build time >60s
- 20+ type errors
- Monorepo with multiple tsconfig files
- Complex module resolution setup

**Escalation actions:**
- Run `tsc --noEmit` to get full error list
- Use `tsc --diagnostics` for performance analysis
- Check all tsconfig files in monorepo
- Analyze import graph for circular dependencies
- Review webpack/vite config for TypeScript loaders

## Framework-Specific Guidance

### Next.js

**App Router (Next.js 13+):**
- Server Components are TypeScript-first
- Use `'use client'` directive correctly
- Async Server Components need proper typing
- Route handlers use `NextRequest`/`NextResponse`

**Common issues:**
```typescript
// ❌ Missing 'use client'
'use client'  // Must be first line
import { useState } from 'react'

// ❌ Server Component with client-only APIs
// app/page.tsx (Server Component by default)
export default function Page() {
  const [state, setState] = useState(0)  // Error!
  // Fix: Add 'use client' or move to client component
}

// ✅ Proper route handler typing
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  return NextResponse.json({ data: 'hello' })
}
```

### Remix

**Route modules:**
- Loader/action return types must be serializable
- `.server` files don't bundle to client
- `useLoaderData<typeof loader>()` for type inference

**Common issues:**
```typescript
// ❌ Non-serializable loader return
export const loader = async () => {
  return { date: new Date() }  // Error in production!
}

// ✅ Serialize dates
export const loader = async () => {
  return json({ date: new Date().toISOString() })
}

// ✅ Type-safe loader data
export const loader = async () => {
  return json({ user: { name: "John" } })
}

export default function Route() {
  const data = useLoaderData<typeof loader>()
  data.user.name  // ✅ Typed correctly
}
```

## Key Principles

1. **Offensive mindset:** Don't just fix errors, optimize the build pipeline
2. **Evidence-based:** Every check maps to a real historical incident
3. **Gradual migration:** Strict mode in phases, not all at once
4. **Framework-aware:** Next.js ≠ Remix ≠ Express
5. **Performance-conscious:** Fast builds = happy developers
6. **Cross-skill integration:** Validate Docker + TypeScript coherence

## Quick Reference: Common Fixes

```bash
# Copy non-TS files to dist
npm install --save-dev cpx
# package.json
"scripts": {
  "copy": "cpx 'src/**/*.{ejs,json}' dist"
}

# Fix import resolution errors
# tsconfig.json - add baseUrl + paths

# Speed up builds
# tsconfig.json - add skipLibCheck: true, incremental: true

# Gradual strict mode
# tsconfig.json - enable flags one by one

# Check for errors without emitting
tsc --noEmit

# Analyze build performance
tsc --diagnostics
```
