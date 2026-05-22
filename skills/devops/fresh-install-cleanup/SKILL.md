---
name: fresh-install-cleanup
description: Clean up and perform a fresh install of the Orient monorepo. Use when asked to "fresh install", "clean install", "rebuild from scratch", "fix build issues", "clean node_modules", or when encountering stale build artifacts, tsbuildinfo issues, or turbo cache problems.
---

# Fresh Install Cleanup

## Quick Reference

```bash
# Full cleanup and reinstall
rm -rf node_modules .turbo packages/*/node_modules packages/*/.turbo packages/*/dist
find packages/*/src -type f \( -name "*.js" -o -name "*.js.map" -o -name "*.d.ts" -o -name "*.d.ts.map" \) -delete
find packages -name "*.tsbuildinfo" -delete
rm -f .tsbuildinfo
pnpm install
pnpm run build:packages
```

## Common Issues & Fixes

### 1. Stale tsbuildinfo Files (Incremental Compilation)

**Symptoms**:

- `tsc` runs without error but produces no output
- Turbo shows "cache hit" but dist/ folders are empty
- Turbo warns: "no output files found for task @orient/mcp-tools#build"
- Build completes "successfully" but dependent packages fail with TS2307

**Cause**: TypeScript's `.tsbuildinfo` files store incremental compilation state. When stale, tsc believes everything is up-to-date and skips compilation entirely - even when dist/ is empty.

**Key indicator**: The warning "no output files found" after a build means tsbuildinfo is stale.

**Fix**:

```bash
find packages -name "*.tsbuildinfo" -delete
rm -f .tsbuildinfo
```

**Verification** (critical step after cleaning):

```bash
# Rebuild
pnpm run build:packages

# Verify dist directories are populated BEFORE proceeding
ls packages/mcp-tools/dist/index.js
ls packages/core/dist/index.js
ls packages/agents/dist/index.js
```

If dist/ is still empty after rebuild, check for other issues (stray files in src/, turbo cache).

### 2. Stray Compiled Files in src/

**Symptom**: Build errors about missing modules even though dependencies are installed.

**Cause**: Previous builds left `.js`, `.d.ts`, `.js.map`, `.d.ts.map` files in `src/` directories instead of `dist/`.

**Fix**:

```bash
find packages/*/src -type f \( -name "*.js" -o -name "*.js.map" -o -name "*.d.ts" -o -name "*.d.ts.map" \) -delete
```

### 3. Turbo Cache Issues

**Symptom**: Build appears cached but dist folders are empty or stale.

**Fix**:

```bash
rm -rf .turbo packages/*/.turbo
```

### 4. Stale Worktrees

**Symptom**: Many old worktrees consuming disk space.

**Check**:

```bash
git worktree list
```

**Fix**:

```bash
# Remove worktree directories
rm -rf ~/claude-worktrees/orient/*
rm -rf ~/.cursor/worktrees/orient/*
# Prune git references
git worktree prune
```

### 5. Stale Fresh Install Folders

**Symptom**: Multiple `orient-fresh-*` directories in parent folder.

**Fix**:

```bash
rm -rf ../orient-fresh-*
```

### 6. Module Resolution Errors (TS2307)

**Symptom**: Build fails with `error TS2307: Cannot find module '@orient/mcp-tools'` or similar.

**Cause**: Turbo's dependency graph wasn't respected because:

- Stale tsbuildinfo made turbo think prerequisite packages were already built
- The `dist/` folder was empty or missing despite turbo showing "cache hit"

**Troubleshooting**:

1. Verify turbo.json has `"dependsOn": ["^build"]` for the build task
2. Check package.json has correct `workspace:*` dependencies
3. Manually verify prerequisite package dist exists:
   ```bash
   ls packages/mcp-tools/dist/index.js
   ```

**Fix**: Clean tsbuildinfo and turbo cache, then rebuild:

```bash
find packages -name "*.tsbuildinfo" -delete
rm -rf .turbo packages/*/.turbo packages/*/dist
pnpm run build:packages
```

## Full Cleanup Procedure

1. **Remove node_modules and build artifacts**:

   ```bash
   rm -rf node_modules .turbo packages/*/node_modules packages/*/.turbo packages/*/dist
   ```

2. **Clean stray compiled files from src directories**:

   ```bash
   find packages/*/src -type f \( -name "*.js" -o -name "*.js.map" -o -name "*.d.ts" -o -name "*.d.ts.map" \) -delete
   ```

3. **Clean tsbuildinfo files**:

   ```bash
   find packages -name "*.tsbuildinfo" -delete
   rm -f .tsbuildinfo
   ```

4. **Clean worktrees** (optional):

   ```bash
   rm -rf ~/claude-worktrees/orient/* ~/.cursor/worktrees/orient/*
   git worktree prune
   ```

5. **Fresh install**:

   ```bash
   pnpm install
   ```

6. **Build packages**:

   ```bash
   pnpm run build:packages
   ```

7. **Verify build completion** (critical - don't skip):

   ```bash
   # Turbo's "cache hit" can be misleading - always verify dist/ exists
   ls packages/*/dist/index.js
   ```

   If any package is missing dist/index.js, clean tsbuildinfo and rebuild that package.

## Docker Testing Mode

### Running Tests with Docker Stack

```bash
./run.sh test        # Build and start full Docker stack
./run.sh test pull   # Use pre-built images from ghcr.io (requires auth)
./run.sh test status # Check container health
./run.sh test stop   # Stop containers
```

### 7. Docker Build Hangs on Metadata Loading

**Symptom**: `./run.sh test` hangs at "load metadata for docker.io/library/node:20-alpine"

**Cause**: Docker buildx can be slow to fetch metadata from Docker Hub on macOS.

**Workaround**: Use existing local images without rebuilding:

```bash
cd docker
docker compose --env-file ../.env -f docker-compose.v2.yml -f docker-compose.local.yml --profile slack up -d --no-build
```

### 8. Port Conflicts (9000, 5432, 80)

**Symptom**: `Bind for 0.0.0.0:9000 failed: port is already allocated`

**Cause**: Dev containers (orienter-_-0) share ports with test containers (orienter-_).

**Fix**: Stop dev containers first:

```bash
docker stop orienter-nginx-0 orienter-postgres-0 orienter-minio-0
docker rm orienter-nginx-0 orienter-postgres-0 orienter-minio-0
```

Then start test containers:

```bash
./run.sh test
```

### 9. ghcr.io Authentication Required

**Symptom**: `./run.sh test pull` fails with 401 Unauthorized

**Cause**: Private images require GitHub authentication.

**Fix**: Either authenticate to ghcr.io or use local builds:

```bash
# Option 1: Authenticate
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Option 2: Use local images (skip pull)
./run.sh test  # builds locally
```

## Verification

After cleanup and rebuild, verify:

```bash
# Check dist directories exist
ls packages/*/dist

# Run unit tests
pnpm run test:ci

# Run e2e tests with Docker stack
./run.sh test status  # Ensure all healthy
E2E_TESTS=true pnpm vitest run tests/e2e
```
