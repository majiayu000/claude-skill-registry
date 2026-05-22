---
name: elastic-beanstalk-deployment
description: Use when deploying Node.js applications to AWS Elastic Beanstalk or troubleshooting deployment issues - provides dependency installation strategies, monorepo handling, and deployment best practices
---

# Elastic Beanstalk Node.js Deployment

## Overview

AWS Elastic Beanstalk automates Node.js application deployment but has specific behaviors around dependency installation that can cause issues, especially with monorepos. Understanding when EB installs dependencies vs when it skips installation is critical for successful deployments.

**Core principle**: Choose between letting EB install dependencies (smaller packages, slower) or bundling node_modules (larger packages, more reliable).

## When to Use

**Use when:**
- Deploying Node.js applications to AWS Elastic Beanstalk
- Encountering "Cannot find package" errors during deployment
- Working with monorepo workspace packages
- Need reliable deployments without npm registry dependencies
- Deploying applications with private packages

**Don't use for:**
- Non-AWS deployments
- Docker-based deployments (different dependency strategy)
- Simple apps with only public npm packages (standard approach works fine)

## Official AWS Documentation

Reference: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/nodejs-platform-dependencies.html

## Quick Reference: EB Dependency Installation Behavior

| Condition | EB Action | npm Command |
|-----------|-----------|-------------|
| `package.json` exists, NO `node_modules/` | Installs dependencies | `npm install --omit=dev` (npm 7+) |
| `node_modules/` directory present | Skips installation | None - uses bundled modules |

## Deployment Strategies

### Strategy 1: Let EB Install Dependencies (Standard)

**Best for**: Simple apps, all packages in npm registry, no monorepo

```yaml
# GitHub Actions workflow
- name: Build application
  run: npm run build

- name: Create deployment package
  run: |
    zip -r app.zip \
      dist/ \
      package.json \
      package-lock.json \
      .ebextensions/
```

**Pros:**
- Smaller deployment packages (5-10MB typical)
- Consistent with npm ecosystem
- Uses platform's npm version

**Cons:**
- Slower deployments (installs on every deploy)
- Requires all packages in npm registry
- Can fail with network/registry issues

### Strategy 2: Bundle node_modules (AWS Recommended for Special Cases)

**Best for**: Monorepos, private packages, reliability requirements

**AWS official quote**: "Bundle node_modules to bypass potential npm registry installation issues."

```yaml
# GitHub Actions workflow
- name: Install production dependencies
  run: npm install --omit=dev

- name: Create deployment package
  run: |
    zip -r app.zip \
      dist/ \
      package.json \
      node_modules/ \
      .ebextensions/
```

**Pros:**
- Bypasses npm registry issues
- Faster deployments (no install phase)
- Works with workspace packages
- Reliable and predictable

**Cons:**
- Larger packages (50-100MB typical)
- Must ensure platform-compatible binaries

## Monorepo / Workspace Package Strategy

### The Problem

Running `npm ci --production` inside a monorepo workspace:
- Creates symlinks to workspace packages (not actual files)
- Results in incomplete `node_modules` (~3MB instead of ~50MB)
- Causes "Cannot find package" errors during EB deployment

**Example error**:
```
Error: Cannot find module '@prpm/types'
```

### The Solution: Clean Context Installation

Install dependencies **outside** the workspace context to get real files instead of symlinks:

```yaml
- name: Create standalone package.json
  run: |
    mkdir -p /tmp/clean-install
    cd /tmp/clean-install

    # Copy package.json and replace workspace refs with file paths
    cp $GITHUB_WORKSPACE/packages/app/package.json .
    jq --arg workspace "$GITHUB_WORKSPACE" \
      '.dependencies["@workspace/pkg"] = "file:\($workspace)/packages/pkg"' \
      package.json > package.json.tmp
    mv package.json.tmp package.json

- name: Install dependencies (outside workspace)
  run: |
    cd /tmp/clean-install
    npm install --omit=dev --legacy-peer-deps

    # Verify critical packages (real directories, not symlinks)
    test -d node_modules/pg || exit 1
    test -d node_modules/@workspace/pkg/dist || exit 1

- name: Copy to deployment location
  run: |
    rm -rf packages/app/node_modules
    cp -r /tmp/clean-install/node_modules packages/app/
```

**Key steps**:
1. Install outside workspace context
2. Convert workspace dependencies to `file:` references
3. Verify packages are real directories (not symlinks)
4. Bundle complete `node_modules` in deployment

## Environment Configuration

### Override Production Install Mode

Set in Beanstalk console:
```
NPM_USE_PRODUCTION=false
```

### Specify Node.js Version

In `package.json`:
```json
{
  "engines": {
    "node": "20.x"
  }
}
```

**Note**: Version range feature not available on Amazon Linux 2023

## Container Commands for Migrations

When bundling `node_modules`, migrations can run immediately:

```yaml
# .ebextensions/migrations.config
container_commands:
  01_run_migrations:
    command: npm run migrate
    leader_only: true
```

**Why this works with bundled approach**:
1. EB extracts deployment to `/var/app/staging/`
2. `node_modules/` already present (bundled)
3. EB skips `npm install` step
4. Migrations run with all dependencies available

## Common Issues and Solutions

### Issue: "Cannot find package 'X'"

**Symptoms**:
```
Error: Cannot find module 'pg'
Error: Cannot find module '@prpm/types'
```

**Cause**: Package not installed or symlinked

**Solution**:
```bash
# Verify package exists as real directory
ls -la node_modules/pg
file node_modules/@prpm/types  # Should show "directory", not "symbolic link"

# If symlink, use clean context installation (see above)
```

### Issue: "npm install fails with workspace package not found"

**Symptoms**:
```
npm ERR! Could not resolve dependency: @workspace/package
```

**Cause**: Workspace package not in npm registry

**Solution**: Use bundled `node_modules` approach with clean context installation

### Issue: Binary compatibility errors

**Symptoms**:
```
Error: The module was compiled against a different Node.js version
```

**Cause**: Native modules compiled for macOS/Windows, deployed to Linux

**Solution**:
- Install dependencies in Linux environment (Docker, GitHub Actions with ubuntu-latest)
- Or use `--platform=linux` flag for specific packages

### Issue: Deployment package too large (>500MB)

**Cause**: Dev dependencies or unnecessary files included

**Solution**:
```bash
# Use --omit=dev flag
npm install --omit=dev

# Exclude unnecessary files
zip -r app.zip dist/ package.json node_modules/ .ebextensions/ \
  -x "*.cache/*" "*.test.js" "*.spec.js"

# Use .ebignore file
echo "*.test.js" >> .ebignore
echo "*.spec.js" >> .ebignore
```

## Verification Steps

Before deploying, always verify:

```bash
# 1. Check node_modules size (should be 50MB+ for typical apps)
du -sh node_modules
# Expected: 50M-100M (if bundled)
# Red flag: 3M-5M (likely symlinks)

# 2. Verify critical packages exist
ls -la node_modules/pg
ls -la node_modules/fastify
ls -la node_modules/@your-workspace/package

# 3. Check for symlinks (should see real directories)
file node_modules/@your-workspace/package
# Expected: "directory"
# Red flag: "symbolic link to ../../packages/your-package"

# 4. Verify dist directories for workspace packages
test -d node_modules/@your-workspace/package/dist || echo "ERROR: dist missing"

# 5. Test the deployment package locally
unzip -q app.zip -d /tmp/test-deploy
cd /tmp/test-deploy
node dist/index.js  # Should start without errors
```

## Best Practices

### 1. Always Include package-lock.json

✅ **Do**: Include `package-lock.json` for reproducible builds
```yaml
zip -r app.zip dist/ package.json package-lock.json node_modules/
```

❌ **Don't**: Omit lock file or use only `package.json`

### 2. Verify Deployment Package

```bash
# Inspect before uploading
unzip -l app.zip | grep node_modules | head -20

# Check size
ls -lh app.zip
# Should be: 50-100MB (bundled) or 5-10MB (unbundled)
```

### 3. Test Locally First

```bash
# Extract and test the exact deployment package
unzip app.zip -d /tmp/deployment-test
cd /tmp/deployment-test
npm start  # Should work without any npm install
```

### 4. Monitor First Deployment

When switching from unbundled to bundled (or vice versa):
- Watch EB console logs carefully
- Verify application starts successfully
- Check for dependency-related errors
- Have rollback plan ready

### 5. Keep Deployment Packages

Save successful deployment packages for rollback:
```bash
aws s3 cp app.zip s3://my-bucket/deployments/app-$(date +%Y%m%d-%H%M%S).zip
```

## Decision Tree: Which Strategy to Use?

```
Does your app use monorepo workspace packages?
├─ Yes → Use bundled node_modules (Strategy 2)
│   └─ Install in clean context (outside workspace)
└─ No → Do you need maximum reliability?
    ├─ Yes → Use bundled node_modules (Strategy 2)
    │   └─ Faster deploys, no registry issues
    └─ No → Are all packages in public npm registry?
        ├─ Yes → Let EB install (Strategy 1)
        │   └─ Smaller packages, standard approach
        └─ No (private packages) → Use bundled node_modules (Strategy 2)
```

## Real-World Example: PRPM Registry

This project uses bundled `node_modules` approach because:
- `@prpm/types` is a workspace package (not in npm registry)
- Requires reliable deployments without registry dependencies
- Migrations need `pg` package available immediately
- Speed and predictability are critical

See `.github/workflows/deploy-registry.yml` for full implementation.

## Additional Resources

- [AWS EB Node.js Platform](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/nodejs-platform-dependencies.html)
- [npm workspaces documentation](https://docs.npmjs.com/cli/v8/using-npm/workspaces)
- [Elastic Beanstalk container commands](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customize-containers-ec2.html#linux-container-commands)
