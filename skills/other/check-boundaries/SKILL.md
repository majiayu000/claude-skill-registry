---
name: check-boundaries
description: Audit for convention violations and dependency boundary issues
---

# Check Boundaries Skill

Audit the x4-mono codebase for convention violations and dependency boundary issues.

## Workflow

1. **Run ESLint**: `bun turbo lint` to catch boundary violations
2. **Check for console.log**: Grep for `console.log` in production code (not test files)
3. **Check for `any` type**: Grep for `: any` and `as any` in TypeScript files
4. **Check for hard-coded env vars**: Grep for patterns like `process.env.` outside `env.ts`
5. **Check import paths**: Verify no relative imports cross package boundaries
6. **Check file naming**: Verify kebab-case for files, PascalCase for components
7. **Check for forbidden patterns**: Items from the "Do NOT" list in CLAUDE.md
8. **Report all violations**: Structured output with fix suggestions

## Checks

### 1. Dependency Boundaries

```
packages/shared/types    → imports NOTHING
packages/shared/utils    → can import: shared/types
packages/database        → can import: shared/types
packages/auth            → can import: database, shared/types
packages/ai-integrations → can import: shared/types
apps/*                   → can import: any package
```

**Critical**: Never import from `apps/*` in `packages/*`.

### 2. No console.log

Search for `console.log`, `console.warn`, `console.error` in:

- `apps/api/src/` (excluding test files)
- `packages/` (excluding test files)

Exceptions: `apps/api/src/lib/env.ts` (startup validation only)

### 3. No `any` Type

Search for `: any`, `as any`, `<any>` in `.ts` and `.tsx` files.

### 4. No Hard-coded Env Vars

Search for `process.env.` outside of `apps/api/src/lib/env.ts`.

### 5. Import Path Conventions

- Cross-package: Must use `@packages/*` or `@x4/*`
- Intra-workspace: Must use `@/*`
- No relative paths crossing package boundaries (e.g., `../../../packages/`)

### 6. File Naming

- Files: kebab-case (`user-profile.ts`, not `userProfile.ts`)
- Components: PascalCase exports
- Constants: SCREAMING_SNAKE_CASE

### 7. Forbidden Patterns

- No Express imports
- No Prisma imports
- No NextAuth/Auth.js imports
- No jest imports (use `bun:test`)
- No API routes in `apps/web` (API is in `apps/api`)

## Output Format

```markdown
## Boundary Check Results

### Summary

- Violations found: N
- Categories: [list]

### Violations

#### [CATEGORY] Description

**File**: path/to/file.ts:line
**Rule**: Which convention was violated
**Fix**: How to fix it

---

### Clean

- [x] ESLint passes
- [x] No console.log in production
- [x] No `any` types
- [x] No hard-coded env vars
- [x] Import paths correct
- [x] File naming correct
- [x] No forbidden patterns
```
