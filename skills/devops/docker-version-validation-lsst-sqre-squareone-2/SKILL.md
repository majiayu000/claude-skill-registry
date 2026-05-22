---
name: docker-version-validation
description: |
  Validates that version strings in Dockerfiles match package.json dependencies and constraints.
  Use when updating Docker base images, Node.js versions, pnpm versions, turbo versions, or other
  tool versions in Dockerfiles. Ensures consistency between Dockerfile versions and package.json
  engines, devDependencies, and packageManager fields. Automatically runs on pre-commit for
  Dockerfile changes and in CI pipeline. Trigger keywords: Dockerfile, Docker version, Node version,
  pnpm version, turbo version, version mismatch, version sync, Docker update.
allowed-tools:
  - Bash(node scripts/validate-docker-versions.js:*)
  - Bash(pnpm validate-docker:*)
---

# Docker Version Validation

This skill ensures that version declarations in Dockerfiles stay synchronized with their corresponding `package.json` files. The validation system automatically runs on pre-commit hooks and in CI, preventing version drift between Docker builds and package configurations.

## When to Use This Skill

Use this skill when:

- **Updating Node.js versions** in Dockerfile base images
- **Updating pnpm versions** via `corepack prepare`
- **Updating Turbo versions** in Docker build commands
- **Creating new Dockerfiles** that use versioned tools
- **Troubleshooting version mismatch errors** from validation failures
- **Understanding why a commit was rejected** due to version inconsistencies

## What Gets Validated

The validation system checks three critical version synchronization points:

### 1. Node.js Version

**Dockerfile location:**
```dockerfile
FROM node:22.21.1-alpine AS base
```

**package.json source:**
```json
{
  "engines": {
    "node": "^22.21.1"
  }
}
```

**Validation rule:** Major.minor versions must match (patch differences allowed)
- ✅ Docker `22.21.1` matches package.json `^22.21.1`
- ✅ Docker `22.21.2` matches package.json `^22.21.1` (patch difference OK)
- ❌ Docker `22.22.0` does NOT match package.json `^22.21.1` (minor mismatch)

### 2. pnpm Version

**Dockerfile location:**
```dockerfile
RUN corepack prepare pnpm@10.20.0 --activate
```

**package.json source:**
```json
{
  "packageManager": "pnpm@10.20.0+sha512..."
}
```

**Validation rule:** Exact version match required
- ✅ Docker `10.20.0` matches package.json `pnpm@10.20.0+sha512...`
- ❌ Docker `10.20.1` does NOT match package.json `pnpm@10.20.0+sha512...`

### 3. Turbo Version

**Dockerfile location:**
```dockerfile
RUN pnpm dlx turbo@2.6.0 prune --scope=squareone --docker
```

**package.json source:**
```json
{
  "devDependencies": {
    "turbo": "2.6.0"
  }
}
```

**Validation rule:** Exact version match required
- ✅ Docker `2.6.0` matches package.json `2.6.0`
- ❌ Docker `2.6.1` does NOT match package.json `2.6.0`

## How Validation Works

### Automatic Validation Points

The validation runs automatically at three integration points:

**1. Pre-commit Hook (via lint-staged)**
```javascript
// .lintstagedrc.mjs
export default {
  '**/Dockerfile*': ['node scripts/validate-docker-versions.js'],
};
```

- **Triggers:** When you stage any Dockerfile for commit
- **Behavior:** Validates before commit completes
- **Outcome:** Blocks commit if versions mismatch

**2. CI Pipeline (GitHub Actions)**
```yaml
# .github/workflows/ci.yaml
- name: Validate Docker versions
  run: node scripts/validate-docker-versions.js
```

- **Triggers:** On every push and pull request
- **Behavior:** Runs early in test job (before formatting, linting, building)
- **Outcome:** Fails CI if versions mismatch

**3. Manual Validation**
```bash
pnpm validate-docker
```

- **Triggers:** On-demand when you run the command
- **Behavior:** Scans all Dockerfiles in repository
- **Outcome:** Exits with code 1 if mismatches found

### Discovery and Mapping

The validation script automatically:

1. **Discovers all Dockerfiles** in the repository (excluding `node_modules`, `.git`, etc.)
2. **Maps each Dockerfile** to its nearest `package.json` (walks up directory tree)
3. **Extracts versions** from both files using regex patterns
4. **Compares versions** according to validation rules
5. **Reports results** with clear error messages

## Running Manual Validation

### Check All Dockerfiles

```bash
pnpm validate-docker
```

**Example output (all valid):**
```
Docker Version Validator
Checking Dockerfiles in: /Users/you/squareone

Found 1 Dockerfile(s) to validate

Validating: apps/squareone/Dockerfile
Against: apps/squareone/package.json
  ✓ Node.js: 22.21.1 matches 22.21.1 (from constraint: ^22.21.1)
  ✓ pnpm: 10.20.0 matches package.json
  ✓ Turbo: 2.6.0 matches package.json

Summary:
  Dockerfiles validated: 1
  ✓ All versions match!
```

**Example output (version mismatch):**
```
Docker Version Validator
Checking Dockerfiles in: /Users/you/squareone

Found 1 Dockerfile(s) to validate

Validating: apps/squareone/Dockerfile
Against: apps/squareone/package.json
  ✓ Node.js: 22.21.1 matches 22.21.1 (from constraint: ^22.21.1)
  ✗ pnpm version mismatch:
    Dockerfile: 10.20.1
    package.json: 10.20.0
  ✓ Turbo: 2.6.0 matches package.json

Summary:
  Dockerfiles validated: 1
  ✗ Found 1 version mismatch(es)

To fix:
  1. Update the Dockerfile to match package.json versions, or
  2. Update package.json to match Dockerfile versions

Validation rules:
  - Node.js: Major.minor must match (patch differences allowed)
  - pnpm: Exact version match required
  - Turbo: Exact version match required
```

## Updating Versions Correctly

Follow this workflow when updating tool versions to keep everything synchronized:

### Option 1: Update package.json First (Recommended)

1. **Update package.json:**
   ```json
   {
     "packageManager": "pnpm@10.21.0+sha512...",
     "devDependencies": {
       "turbo": "2.7.0"
     },
     "engines": {
       "node": "^22.22.0"
     }
   }
   ```

2. **Update Dockerfile to match:**
   ```dockerfile
   FROM node:22.22.0-alpine AS base
   RUN corepack prepare pnpm@10.21.0 --activate
   RUN pnpm dlx turbo@2.7.0 prune --scope=squareone --docker
   ```

3. **Validate changes:**
   ```bash
   pnpm validate-docker
   ```

4. **Stage and commit:**
   ```bash
   git add package.json apps/squareone/Dockerfile
   git commit -m "Update Node.js to 22.22.0, pnpm to 10.21.0, turbo to 2.7.0"
   ```

### Option 2: Update Dockerfile First

1. **Update Dockerfile:**
   ```dockerfile
   FROM node:22.22.0-alpine AS base
   RUN corepack prepare pnpm@10.21.0 --activate
   RUN pnpm dlx turbo@2.7.0 prune --scope=squareone --docker
   ```

2. **Update package.json to match:**
   ```json
   {
     "packageManager": "pnpm@10.21.0+sha512...",
     "devDependencies": {
       "turbo": "2.7.0"
     },
     "engines": {
       "node": "^22.22.0"
     }
   }
   ```

3. **Validate and commit** (same as Option 1)

### Updating Only One Version

If you're updating just Node.js, pnpm, or Turbo (not all three):

1. **Update both files** (package.json and Dockerfile) for that specific version
2. **Run validation** to confirm: `pnpm validate-docker`
3. **Commit both changes together**

**Example: Update only pnpm version**
```bash
# Edit package.json: packageManager: "pnpm@10.21.0+sha512..."
# Edit Dockerfile: RUN corepack prepare pnpm@10.21.0 --activate
pnpm validate-docker
git add package.json apps/squareone/Dockerfile
git commit -m "Update pnpm to 10.21.0"
```

## Troubleshooting

### Pre-commit Hook Rejected My Commit

**Problem:** You staged a Dockerfile change but the commit was blocked:
```
✗ pnpm version mismatch:
  Dockerfile: 10.20.1
  package.json: 10.20.0
```

**Solution:**
1. Fix the version mismatch in either Dockerfile or package.json
2. Stage the corrected file: `git add <file>`
3. Try committing again

**Quick fix:**
```bash
# Option A: Update Dockerfile to match package.json
# Edit apps/squareone/Dockerfile manually
git add apps/squareone/Dockerfile
git commit

# Option B: Update package.json to match Dockerfile
# Edit package.json manually
git add package.json
git commit
```

### CI Pipeline Failing on Version Validation

**Problem:** CI fails early with "Validate Docker versions" step

**Solution:**
1. Check the CI logs for the specific version mismatch
2. Pull the latest changes if working on a branch
3. Update versions locally to match
4. Push the fix

**Example fix:**
```bash
# Check what's wrong
pnpm validate-docker

# Fix the mismatch (edit files)

# Validate locally
pnpm validate-docker

# Commit and push
git add package.json apps/squareone/Dockerfile
git commit -m "Fix Docker version mismatch"
git push
```

### Version Found in Only One File

**Warning:** `⚠ pnpm version found in only one file (Docker: 10.20.0, package.json: none)`

**Explanation:** This is a warning (not an error). The validation found a version declaration in the Dockerfile but not in package.json, or vice versa.

**Common causes:**
- New Dockerfile added without updating package.json
- Version removed from package.json but still in Dockerfile
- Parsing failed to find the version (incorrect format)

**Solution:**
1. Ensure both files declare the version
2. Check that the format matches the expected pattern (see "What Gets Validated" above)

### Validation Script Not Finding Versions

**Problem:** Validation reports versions as "not found" even though they exist

**Cause:** The version format in the Dockerfile doesn't match the expected regex pattern

**Dockerfile patterns expected:**
```dockerfile
# Node.js
FROM node:22.21.1-alpine

# pnpm
RUN corepack prepare pnpm@10.20.0 --activate

# Turbo
RUN pnpm dlx turbo@2.6.0 prune ...
# OR
RUN pnpx turbo@2.6.0 prune ...
```

**Solution:** Ensure your Dockerfile uses these exact patterns. If using a different format, the validation script may need updates.

## Technical Details

### Validation Script

**Location:** `scripts/validate-docker-versions.js`

**Key functions:**
- `findDockerfiles(dir)` - Recursively finds all Dockerfiles
- `findNearestPackageJson(filePath)` - Walks up directory tree to find package.json
- `parseDockerfile(path)` - Extracts versions using regex patterns
- `parsePackageJson(path)` - Reads and extracts versions from JSON
- `compareVersions(v1, v2, matchType)` - Compares versions according to rules
- `validateDockerfile(path, rootDir)` - Main validation logic

**Exit codes:**
- `0` - All versions match
- `1` - Version mismatches found
- `2` - Validation error (missing files, parse errors)

### Validation Rules Implementation

**Major.minor matching (Node.js):**
```javascript
function compareVersions(v1, v2, matchType = 'exact') {
  const cleanV1 = v1.replace(/^[\^~>=<]+/, '');
  const cleanV2 = v2.replace(/^[\^~>=<]+/, '');

  if (matchType === 'major.minor') {
    const [major1, minor1] = cleanV1.split('.');
    const [major2, minor2] = cleanV2.split('.');
    return major1 === major2 && minor1 === minor2;
  }

  return cleanV1 === cleanV2;
}
```

### Integration Points

**Pre-commit (lint-staged):**
- Configured in `.lintstagedrc.mjs`
- Runs only when `**/Dockerfile*` files are staged
- Blocks commit on validation failure

**CI (GitHub Actions):**
- Configured in `.github/workflows/ci.yaml`
- Runs in `test` job after installing packages
- Fails CI build on validation error

**Manual:**
- Accessible via `pnpm validate-docker`
- Runs full validation across all Dockerfiles
- Useful for debugging and development

## Best Practices

### When Creating New Dockerfiles

1. **Copy version patterns** from existing Dockerfiles (e.g., `apps/squareone/Dockerfile`)
2. **Use the same tool versions** as package.json from the start
3. **Run validation** before first commit: `pnpm validate-docker`
4. **Commit both files** (Dockerfile + package.json) together

### When Updating Versions

1. **Update package.json first** (single source of truth)
2. **Update all Dockerfiles** that use the version
3. **Run validation** locally before committing
4. **Group related version updates** in single commits

### During Code Review

1. **Check for version updates** in both Dockerfile and package.json
2. **Verify validation passed** in CI
3. **Ask about version choices** if major/minor updates
4. **Ensure changeset exists** for version changes

## Related Documentation

- **Turborepo workflow:** `.claude/skills/turborepo-workflow/` - Build and caching patterns
- **Remote cache docs:** `docs/dev/remote-cache.rst` - Turborepo remote caching infrastructure
- **Docker builds:** `.github/workflows/build-squareone.yaml` - Docker build workflow
- **CLAUDE.md:** General development commands and patterns

## Questions?

- **What versions should I use?** Check `package.json` for the current versions
- **Why exact match for pnpm/turbo but not Node?** Patch versions of Node are typically compatible, but pnpm/turbo can have breaking changes
- **Can I disable validation?** Not recommended, but you can remove the pre-commit hook or CI step
- **What if I need different versions?** Update package.json to reflect the desired state, then update Dockerfiles to match
