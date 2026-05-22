---
name: monorepo-patterns
description: Monorepo workflows - navigation, cross-package changes, tooling
version: 1.0.0
author: Claude Code SDK
tags: [monorepo, navigation, packages, workspace]
---

# Monorepo Patterns

Efficient workflows for navigating and working in monorepo codebases with Claude Code.

## Quick Reference

| Challenge | Solution |
|-----------|----------|
| Large codebase | Scope context to relevant packages |
| Cross-package changes | Follow dependency graph order |
| Build coordination | Use workspace-aware commands |
| Package discovery | Leverage workspace config files |

| Tool | Config File | Key Commands |
|------|-------------|--------------|
| Turborepo | `turbo.json` | `turbo run build --filter=pkg` |
| Nx | `nx.json` | `nx run pkg:build`, `nx affected` |
| Lerna | `lerna.json` | `lerna run build --scope=pkg` |
| pnpm | `pnpm-workspace.yaml` | `pnpm --filter pkg build` |

## Monorepo Structures

### Common Layouts

```
# Packages Layout (Most Common)
monorepo/
  packages/
    core/
    ui/
    utils/
  package.json

# Apps + Packages Layout
monorepo/
  apps/
    web/
    api/
  packages/
    shared/
    ui/
  package.json

# Domain Layout
monorepo/
  domains/
    auth/
    billing/
    users/
  shared/
  package.json
```

### Identifying Monorepo Type

```bash
# Check for workspace configuration
cat package.json | grep -A5 "workspaces"
ls turbo.json nx.json lerna.json pnpm-workspace.yaml 2>/dev/null
```

## Context Scoping

### Rule: Always Scope Before Working

Before making changes, identify which packages are relevant:

```bash
# Find the package you need to modify
rg -l "FunctionName" --type ts

# Check which workspace it belongs to
ls -la packages/*/package.json | head -20

# Read only the relevant package.json
cat packages/target-package/package.json
```

### Scoping Workflow

1. **Identify entry point** - What file/feature are you modifying?
2. **Find package boundary** - Which package contains it?
3. **Map dependencies** - What does this package depend on?
4. **Limit context** - Only read files within scope

```bash
# Find package for a file
dirname $(rg -l "targetFunction" --type ts | head -1)

# List package dependencies
cat packages/target/package.json | grep -A20 "dependencies"
```

## Navigating Large Codebases

### Discovery Commands

```bash
# List all packages
ls packages/ 2>/dev/null || ls apps/ 2>/dev/null

# Find package by name
rg -l '"name".*"@org/package-name"' packages/

# Find packages using a dependency
rg '"dependency-name"' packages/*/package.json

# Find entry points
rg -l "export.*from" packages/*/src/index.ts
```

### Understanding Package Relationships

```bash
# Show all internal dependencies
rg "@org/" packages/*/package.json --no-filename | sort -u

# Find packages depending on target
rg '"@org/target-package"' packages/*/package.json

# Visualize with tool (if available)
turbo run build --graph  # Opens browser
nx graph                 # Opens browser
```

## Cross-Package Change Workflow

### Step 1: Identify Scope

```bash
# What packages does this change affect?
rg -l "AffectedInterface" --type ts

# Check dependency direction
cat packages/affected/package.json | grep dependencies
```

### Step 2: Determine Edit Order

Follow dependency graph - edit dependencies before dependents:

```
shared (no deps)      <- Edit first
    |
    v
utils (deps: shared)
    |
    v
core (deps: utils)
    |
    v
app (deps: core)      <- Edit last
```

### Step 3: Edit in Order

- [ ] Edit shared types/interfaces first
- [ ] Update utility packages
- [ ] Modify core packages
- [ ] Update consuming apps
- [ ] Run affected tests

### Step 4: Build and Test

```bash
# Build only affected packages
turbo run build --filter=...[HEAD^]
nx affected --target=build

# Test only affected packages
turbo run test --filter=...[HEAD^]
nx affected --target=test
```

## Package-Specific Rules

### Using Package-Level CLAUDE.md

Create `.claude/CLAUDE.md` in each package for specific instructions:

```markdown
# packages/api/.claude/CLAUDE.md

## API Package Rules

- All routes in `src/routes/`
- Use Zod schemas from `@org/schemas`
- Tests must use `supertest`
- Run `bun test` before committing

## Common Patterns

- Route handlers export from index
- Middleware in `src/middleware/`
```

### Workspace Root CLAUDE.md

```markdown
# .claude/CLAUDE.md (root)

## Monorepo Rules

- Use `pnpm` for package management
- Run `turbo run build` for full build
- Run `turbo run test --filter=changed` for affected tests

## Package Locations

| Package | Purpose |
|---------|---------|
| `packages/core` | Business logic |
| `packages/ui` | React components |
| `apps/web` | Next.js frontend |
| `apps/api` | Express backend |
```

## Build Optimization

### Filtering Builds

```bash
# Build single package
turbo run build --filter=@org/package
pnpm --filter @org/package build
nx run @org/package:build

# Build package + dependencies
turbo run build --filter=@org/package...
pnpm --filter @org/package... build

# Build package + dependents
turbo run build --filter=...@org/package
pnpm --filter ...@org/package build

# Build only changed
turbo run build --filter=...[HEAD^]
nx affected --target=build
```

### Cache Utilization

```bash
# Check cache status
turbo run build --dry-run

# Force rebuild (skip cache)
turbo run build --force

# Remote cache (if configured)
turbo run build --remote-only
```

## Validation Checklist

After cross-package changes:

- [ ] Changed packages build successfully
- [ ] Dependent packages build successfully
- [ ] All affected tests pass
- [ ] No circular dependency introduced
- [ ] TypeScript resolves all cross-package types
- [ ] Exports are correctly defined in package.json

```bash
# Full validation
turbo run build test typecheck --filter=...@org/changed-package
```

## Common Scenarios

### Adding a New Shared Type

1. Add type to shared package
2. Export from package index
3. Rebuild shared package
4. Update consuming packages
5. Run affected tests

### Moving Code Between Packages

1. Copy code to target package
2. Add re-export from source (temporary)
3. Update all imports to new location
4. Remove old code and re-export
5. Build and test affected packages

### Updating a Shared Dependency

1. Update in root package.json or package
2. Run `pnpm install` / `bun install`
3. Build all packages
4. Test affected functionality

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Reading entire monorepo | Scope to relevant packages |
| Building everything | Filter to affected packages |
| Ignoring package boundaries | Respect workspace structure |
| Direct file imports across packages | Use package exports |
| Skipping dependency order | Edit deps before dependents |

## Reference Files

| File | Contents |
|------|----------|
| [NAVIGATION.md](./NAVIGATION.md) | Navigating large codebases |
| [CROSS-PACKAGE.md](./CROSS-PACKAGE.md) | Cross-package changes, dependency management |
| [TOOLING.md](./TOOLING.md) | Turborepo, Nx, Lerna integration |

## Quick Diagnostic

```bash
# Identify monorepo type
echo "=== Monorepo Config ===" && \
ls -la turbo.json nx.json lerna.json pnpm-workspace.yaml 2>/dev/null || echo "No config found"

# List all packages
echo "=== Packages ===" && \
ls packages/ apps/ 2>/dev/null

# Check for common issues
echo "=== Recent Changes ===" && \
git status --short
```
