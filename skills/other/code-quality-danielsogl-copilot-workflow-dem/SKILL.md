---
name: code-quality
description: Project-specific code quality standards and review checklist. Activates when reviewing code, discussing quality, refactoring, or checking for anti-patterns in this Angular 21 DDD project.
---

# Code Quality Checklist

For detailed patterns, read the instruction files in `.github/instructions/`.

## Critical Violations (Must Fix)

- [ ] No barrel files (`index.ts`)
- [ ] Components in own subfolders
- [ ] DDD boundaries respected (no cross-domain imports)
- [ ] `standalone: true` + `OnPush` on every component
- [ ] Signal inputs (`input()`) and outputs (`output()`), not decorators
- [ ] `@if`/`@for`/`@switch` control flow, never `*ngIf`/`*ngFor`
- [ ] `inject()` function, not constructor injection
- [ ] No `any` types — strict TypeScript
- [ ] kebab-case files, PascalCase classes without type suffixes

## Warnings (Should Fix)

- [ ] `@for` has `track` expression
- [ ] Heavy computations in `computed()`, not templates
- [ ] Every new file has a `.spec.ts` companion
- [ ] `provideZonelessChangeDetection()` in all tests
- [ ] Store uses `rxMethod` + `tapResponse` for async
- [ ] Loading/error states managed consistently

## Lint & Format

```bash
npm run lint          # ESLint + auto-fix
npx prettier --check . # Check formatting
```
