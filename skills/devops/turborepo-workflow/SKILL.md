---
name: turborepo-workflow
description: Expert guidance on Turborepo build orchestration and remote caching workflow. Use this skill when running build commands, troubleshooting caching issues, working with monorepo task execution, or investigating CI/CD pipeline problems. Covers the critical pattern of always using root-level pnpm scripts, understanding the turbo-wrapper.js authentication system, filter syntax for targeting packages, and remote cache configuration.
---

# Turborepo Workflow

This skill covers the build orchestration and remote caching patterns used in the Squareone monorepo.

## Critical Rules

⚠️ **ALWAYS use root-level pnpm scripts** - Never run individual package scripts or call turbo directly (unless environment variables are pre-set in CI/CD).

### Why This Matters

Only the root `package.json` scripts use the wrapper (`scripts/turbo-wrapper.js`) that enables remote caching with authentication.

**Individual package.json scripts bypass the wrapper and remote caching**, resulting in slower builds and missed cache hits.

## Correct vs Incorrect Usage

### ✅ Correct

```bash
# Root script with filter (from repository root)
pnpm test --filter @lsst-sqre/squared

# Root scripts for all packages
pnpm build
pnpm lint
pnpm type-check
pnpm dev --filter squareone
```

### ❌ Wrong

```bash
# Individual package script (bypasses wrapper!)
cd packages/squared && pnpm test

# Direct turbo call without env vars (bypasses wrapper!)
turbo run test --filter @lsst-sqre/squared

# Running from package directory (bypasses wrapper!)
cd apps/squareone && pnpm dev
```

### Exception: Direct Turbo Calls in CI/CD

Direct `turbo` calls are acceptable **only when** `TURBO_API`, `TURBO_TOKEN`, and `TURBO_TEAM` are already set as environment variables:

```bash
# In CI/CD pipelines with pre-set env vars
export TURBO_API="https://roundtable.lsst.cloud/turborepo-cache"
export TURBO_TOKEN="$SECRET_TOKEN"
export TURBO_TEAM="team_squareone"
turbo run build  # OK in this context
```

In Docker builds or CI/CD where these env vars are injected, direct turbo calls work because the wrapper script detects them first (Priority 1).

## Common Commands

### Build Commands

```bash
# Build all packages and apps
pnpm build

# Build specific package
pnpm build --filter @lsst-sqre/squared

# Build specific app
pnpm build --filter squareone

# Build with increased memory (if needed)
NODE_OPTIONS="--max_old_space_size=4096" pnpm build
```

### Development Commands

```bash
# Start all dev servers
pnpm dev

# Start specific app dev server
pnpm dev --filter squareone

# Start specific package dev server
pnpm dev --filter @lsst-sqre/squared
```

### Testing Commands

```bash
# Run all tests
pnpm test

# Run tests for specific package
pnpm test --filter @lsst-sqre/squared

# Run Storybook tests
pnpm test-storybook
pnpm test-storybook:watch
pnpm test-storybook --filter @lsst-sqre/squared
```

### Quality Commands

```bash
# Run ESLint
pnpm lint
pnpm lint --filter squareone

# Run TypeScript type checking
pnpm type-check
pnpm type-check --filter @lsst-sqre/squared

# Format code with Prettier
pnpm format
```

### Storybook Commands

```bash
# Start Storybook for all packages
pnpm storybook

# Start Storybook for specific package
pnpm storybook --filter @lsst-sqre/squared

# Build Storybook static site
pnpm build-storybook --filter squared
```

## Filter Syntax

Turborepo's filter syntax allows targeting specific packages:

```bash
# By package name
pnpm build --filter @lsst-sqre/squared

# By app name (no scope prefix for apps)
pnpm dev --filter squareone

# Multiple filters
pnpm test --filter @lsst-sqre/squared --filter squareone

# Dependents (packages that depend on this)
pnpm build --filter ...@lsst-sqre/squared

# Dependencies (packages this depends on)
pnpm build --filter @lsst-sqre/squared...
```

## Remote Cache Authentication

The monorepo uses a custom Turborepo cache server at `https://roundtable.lsst.cloud/turborepo-cache` for faster builds through remote caching.

See the complete documentation at `docs/dev/remote-cache.rst`.

### Authentication Methods

The `turbo-wrapper.js` script checks for authentication in priority order:

1. **Environment variables** - `TURBO_API`, `TURBO_TOKEN`, `TURBO_TEAM` all set (CI/CD)
2. **1Password** - `.env.op` file + `op` CLI available (secure local development)
3. **Plain .env file** - `.env` file present (local development without 1Password)
4. **No authentication** - Local cache only (external contributors)

### Authentication Messages

When running commands, you'll see:

- ✅ `🔑 Using environment variables for Turborepo remote cache authentication`
- ✅ `🔐 Using 1Password for Turborepo remote cache authentication`
- ✅ `🔑 Using .env for Turborepo remote cache authentication`
- ℹ️ `ℹ️  Running Turborepo without remote cache (local cache only)`

### Setting Up Authentication

#### For 1Password Users

1. Create `.env.op` file from template:
   ```bash
   cp .env.op.example .env.op
   ```

2. Edit `.env.op` to reference your 1Password vault items

3. Install 1Password CLI:
   ```bash
   brew install 1password-cli
   ```

4. Sign in to 1Password:
   ```bash
   op signin lsstit.1password.com
   ```

#### For Plain .env Users

1. Create `.env` file from template:
   ```bash
   cp .env.example .env
   ```

2. Add your credentials to `.env`:
   ```bash
   TURBO_API=https://roundtable.lsst.cloud/turborepo-cache
   TURBO_TOKEN=your_token_here
   TURBO_TEAM=team_squareone
   ```

3. **Never commit .env files** - they're in `.gitignore`

#### Obtaining Access Tokens

1. Visit https://roundtable.lsst.cloud
2. Log in with your credentials
3. Navigate to the token management page
4. Create a new token with the **`write:turborepo`** scope
5. Store it securely in 1Password or `.env` file

## Verifying Remote Cache

### Cache Hit Messages

Look for these indicators in Turborepo output:

```text
>>> FULL TURBO
>>> Remote caching enabled

@lsst-sqre/squared:build: cache hit, replaying output...
squareone:build: cache hit, replaying output...
```

### Debug Mode

For detailed caching information:

```bash
TURBO_LOG_LEVEL=debug pnpm build
```

## Troubleshooting

### Remote Cache Not Working

**Symptoms**: No "Remote caching enabled" message, slow builds

**Solutions**:
1. Verify authentication message shows up
2. Check network connectivity to https://roundtable.lsst.cloud
3. Ensure token hasn't expired
4. Verify token has the `write:turborepo` scope
5. Try with `TURBO_LOG_LEVEL=debug` to see detailed logs
6. Verify credentials are correct in `.env` or `.env.op`

### 1Password CLI Not Found

**Symptoms**: Warning message about 1Password CLI not available

**Solutions**:
```bash
# Verify installation
op --version

# Install if needed
brew install 1password-cli

# Sign in
op signin lsstit.1password.com
```

### Cache Poisoning / Stale Cache

**Symptoms**: Build failures or incorrect behavior despite clean checkout

**Solutions**:
```bash
# Force rebuild (ignore cache)
pnpm build --force

# Clear local turbo cache
rm -rf node_modules/.cache/turbo

# Clear all node_modules and reinstall
pnpm clean && pnpm install
```

### Build Errors in Monorepo

**Symptoms**: Build fails with mysterious errors

**Solutions**:
1. Ensure you're using root-level scripts (not running from package directories)
2. Check that all dependencies are installed: `pnpm install`
3. Try a clean build: `pnpm clean && pnpm build`
4. Verify turbo.json configuration is correct
5. Check for circular dependencies

### Package Not Building

**Symptoms**: Specific package fails to build or isn't found

**Solutions**:
```bash
# Verify package name is correct
ls packages/

# Check turbo.json for correct package name
cat turbo.json

# Try building just that package
pnpm build --filter @lsst-sqre/package-name

# Check package.json for valid build script
cat packages/package-name/package.json
```

## Temporarily Disabling Remote Cache

Sometimes useful for testing local-only builds:

```bash
# Rename config files
mv .env .env.backup
mv .env.op .env.op.backup

# Or use build:local script (if available)
pnpm build:local

# Or call turbo directly (bypasses wrapper)
npx turbo build
```

## Turborepo Configuration

The monorepo's build pipeline is configured in `turbo.json`:

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**", "build/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {},
    "type-check": {}
  }
}
```

### Understanding Pipeline

- **`build`** - Depends on dependencies' builds (`^build`), caches outputs
- **`test`** - Depends on build, caches coverage
- **`lint`** - No dependencies, can run in parallel
- **`type-check`** - No dependencies, can run in parallel

### Cache Outputs

Turborepo caches specified output directories:
- `.next/**` - Next.js build output
- `dist/**` - Package build output
- `build/**` - Other build artifacts
- `coverage/**` - Test coverage reports

## Package Dependencies

The monorepo has these package relationships:

```
@lsst-sqre/squared (component library)
├── @lsst-sqre/global-css (styles)
│   └── @lsst-sqre/rubin-style-dictionary (tokens)
├── @lsst-sqre/eslint-config
└── @lsst-sqre/tsconfig

squareone (Next.js app)
├── @lsst-sqre/squared
├── @lsst-sqre/global-css
└── @lsst-sqre/eslint-config
```

Building `squared` automatically builds its dependencies (`global-css`, `rubin-style-dictionary`).

## CI/CD Integration

In CI/CD pipelines:

```yaml
# GitHub Actions example
env:
  TURBO_API: ${{ secrets.TURBO_API }}
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ secrets.TURBO_TEAM }}

steps:
  - run: pnpm install
  - run: pnpm build  # Uses environment variables for remote cache
  - run: pnpm test
```

Environment variables take priority, so the wrapper automatically uses them without needing `.env` files.

## Best Practices

1. **Always run from repository root** with filters
2. **Use root-level pnpm scripts** for all Turborepo commands
3. **Never commit .env or .env.op files** (in .gitignore)
4. **Verify remote cache is working** via authentication messages
5. **Use filters** to target specific packages for faster iteration
6. **Check turbo.json** when adding new scripts or packages
7. **Clean caches** if experiencing unexplained build issues
8. **Document new scripts** in root package.json with clear names

## Performance Tips

```bash
# Increase Node.js memory for large builds
NODE_OPTIONS="--max_old_space_size=4096" pnpm build

# Parallel execution is automatic via Turborepo
# No need to manually parallelize

# Use filters to avoid unnecessary work
pnpm test --filter @lsst-sqre/squared  # Only test one package

# Remote cache dramatically speeds up CI/CD
# and switching branches
```

## Common Patterns

### After Pulling Changes

```bash
pnpm install  # Update dependencies
pnpm build    # Rebuild (uses remote cache if possible)
```

### Before Committing

```bash
pnpm lint       # Check code style
pnpm type-check # Check TypeScript
pnpm test       # Run tests
```

### Adding New Package

1. Create package in `packages/` or `apps/`
2. Add to `pnpm-workspace.yaml` (usually automatic)
3. Add scripts to package's `package.json`
4. Update `turbo.json` if needed
5. Run `pnpm install` from root

### Debugging Build Issues

```bash
# 1. Clean everything
pnpm clean

# 2. Reinstall dependencies
pnpm install

# 3. Build with debug logging
TURBO_LOG_LEVEL=debug pnpm build --force

# 4. Check specific package
pnpm build --filter @lsst-sqre/package-name --force
```

## Related Documentation

- `docs/dev/remote-cache.rst` - Complete remote cache documentation
- `scripts/turbo-wrapper.js` - Wrapper script source code
- `turbo.json` - Pipeline configuration
- `pnpm-workspace.yaml` - Workspace configuration

## Infrastructure

The Turborepo cache server is deployed as part of the Rubin Science Platform:

- **URL**: https://roundtable.lsst.cloud/turborepo-cache
- **Authentication**: Gafaelfawr tokens with `write:turborepo` scope
- **Storage**: Google Cloud Storage
- **Documentation**: See Phalanx turborepo-cache application docs

Components:
- `turborepo-cache-proxy` - Exchanges Gafaelfawr token for cache authentication
- `turborepo-remote-cache` - Cache server implementation
- Google Cloud Storage - Backend storage for artifacts
