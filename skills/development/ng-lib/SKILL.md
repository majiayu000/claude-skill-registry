---
name: ng-lib
description: |
  Angular library generator for Nx monorepo. This skill should be used when creating new Angular libraries
  with @nx/angular:library generator. Handles feature libs (landing/feature-*), shared libs (landing/shared/*),
  and global shared libs (shared/*). Auto-prefills tags, directory, prefix, importPath based on project conventions.
  Triggers: "create lib", "new library", "generate library", "ng-lib", "/ng-lib"
---

# Angular Library Generator

Generate Angular libraries following project conventions with proper scoping and module boundaries.

## Quick Reference

| Scope | Directory Pattern | Tags | Import Path |
|-------|------------------|------|-------------|
| Global shared | `libs/shared/{name}` | `scope:shared`, `type:{name}` | `@portfolio/shared/{name}` |
| Landing shared | `libs/landing/shared/{type}` | `scope:landing`, `type:shared-{type}` | `@portfolio/landing/shared/{type}` |
| Landing feature | `libs/landing/feature-{name}` | `scope:landing`, `type:feature` | `@portfolio/landing/feature-{name}` |

## Workflow

1. **Gather input** - Ask user for library name and purpose
2. **Classify** - Determine scope (global-shared, landing-shared, landing-feature)
3. **Prefill** - Auto-generate all options based on classification
4. **Confirm** - Show user the command before execution
5. **Execute** - Run nx generate command

## Interactive Questions

Ask user:
1. "What is the library name?" (e.g., `projects`, `data-access`, `ui`)
2. "What is the library's purpose?" (helps classify scope)
3. "Which scope?" - Offer options based on purpose:
   - **Feature** - Landing page section (projects, skills, experience, hero)
   - **Landing Shared** - Shared within landing app (data-access, ui, util, types)
   - **Global Shared** - Shared across FE+BE (types, utils, testing)

## Generator Options

Reference: `references/generator-options.md`

### Project Defaults (from nx.json)

```
linter: eslint
unitTestRunner: jest
style: scss (for components)
standalone: true
```

### Computed Options by Scope

**Global Shared** (`libs/shared/{name}`):
```bash
nx g @nx/angular:library {name} \
  --directory=libs/shared/{name} \
  --importPath=@portfolio/shared/{name} \
  --tags="scope:shared,type:{name}" \
  --prefix=shared \
  --standalone \
  --style=scss
```

**Landing Shared** (`libs/landing/shared/{type}`):
```bash
nx g @nx/angular:library {type} \
  --directory=libs/landing/shared/{type} \
  --importPath=@portfolio/landing/shared/{type} \
  --tags="scope:landing,type:shared-{type}" \
  --prefix=landing \
  --standalone \
  --style=scss
```

**Landing Feature** (`libs/landing/feature-{name}`):
```bash
nx g @nx/angular:library feature-{name} \
  --directory=libs/landing/feature-{name} \
  --importPath=@portfolio/landing/feature-{name} \
  --tags="scope:landing,type:feature" \
  --prefix=landing \
  --standalone \
  --style=scss
```

## Post-Generation

After generating, remind user to:
1. Update `tsconfig.base.json` paths if not auto-added
2. Verify tags in `project.json`
3. Run `pnpm lint` to verify module boundaries

## Module Boundary Rules

Reference: `references/module-boundaries.md` for ESLint enforce-module-boundaries configuration.
