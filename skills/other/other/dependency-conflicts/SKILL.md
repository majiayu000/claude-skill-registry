---
name: dependency-conflicts
description: Resolve pnpm workspace dependency issues. Use when you see ERESOLVE errors, peer dependency mismatches, "Cannot find module" after install, or version conflicts between packages.
---

# Dependency Conflict Resolution

## When to Use

Use this skill when you encounter package dependency issues in this monorepo.

## Trigger Patterns

You likely need this skill when you see:
- `ERESOLVE unable to resolve dependency tree`
- `peer dependency` warnings or errors
- Version mismatch errors between packages
- `Cannot find module` after install
- Turborepo or pnpm workspace errors

## Quick Diagnosis

```bash
# Check what's installed
pnpm why <package-name>

# See workspace structure
pnpm ls --depth 0

# Check for duplicate versions
pnpm why <package-name> --json | jq '.[] | .version'
```

## Common Scenarios

### Scenario 1: Peer Dependency Mismatch

**Symptom**: Warning about unmet peer dependency

**Fix**: Add the peer dependency to root `package.json`:
```bash
pnpm add -D <peer-package>@<required-version> -w
```

### Scenario 2: Version Conflict Between Packages

**Symptom**: Different workspace packages require different versions

**Fix**: Use `pnpm.overrides` in root `package.json`:
```json
{
  "pnpm": {
    "overrides": {
      "<package-name>": "<unified-version>"
    }
  }
}
```

Then reinstall:
```bash
pnpm install
```

### Scenario 3: Module Not Found After Install

**Symptom**: `Cannot find module` despite being in package.json

**Fixes** (try in order):
1. Clean and reinstall:
   ```bash
   rm -rf node_modules && pnpm install
   ```

2. Rebuild workspace links:
   ```bash
   pnpm install --force
   ```

3. Check if package exports the path you're importing:
   ```bash
   pnpm --filter <package> exec node -e "console.log(require.resolve('<import-path>'))"
   ```

### Scenario 4: Turborepo Cache Issues

**Symptom**: Build works locally but fails in CI, or vice versa

**Fix**: Clear Turborepo cache:
```bash
pnpm exec turbo clean
# Or more aggressive:
rm -rf .turbo node_modules/.cache
pnpm install
```

## Workspace Package Rules

This monorepo uses workspace protocol references:

```json
{
  "dependencies": {
    "@acme/ui": "workspace:^",
    "@acme/platform-core": "workspace:^"
  }
}
```

**Rules**:
- Internal packages use `workspace:^`
- External packages use specific versions
- Root devDependencies are shared across workspace
- Package-specific deps go in that package's `package.json`

## Adding New Dependencies

```bash
# Add to root (shared across workspace)
pnpm add -D <package> -w

# Add to specific package
pnpm --filter <package-name> add <dependency>

# Add to specific app
pnpm --filter @apps/cms add <dependency>
```

## Common Pitfalls

- Don't use `npm` or `yarn` — this is a pnpm workspace
- Don't manually edit `pnpm-lock.yaml`
- Don't use `*` or `latest` versions in production deps
- Do use `pnpm why` to understand dependency trees
- Do use workspace protocol for internal packages
- Do pin versions for external dependencies

## Quality Checks

- [ ] `pnpm install` completes without errors
- [ ] `pnpm build` succeeds
- [ ] `pnpm typecheck` passes
- [ ] No duplicate versions of critical packages
