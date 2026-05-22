---
name: github-actions-testing
description: Expert guidance for testing and validating GitHub Actions workflows before deployment - catches cache errors, path issues, monorepo dependencies, and service container problems that local testing misses
---

# SKILL: GitHub Actions Testing & Validation Expert

## Description

Interactive expert for testing and validating GitHub Actions workflows before deployment. Prevents common CI failures by catching cache configuration errors, path issues, monorepo dependency problems, and service container configuration mistakes.

## Capabilities

This skill provides:

1. **Pre-Push Validation**: Complete workflow validation before pushing to GitHub
2. **Cache Configuration**: Ensure cache-dependency-path is correctly specified
3. **Monorepo Build Order**: Validate workspace dependency build sequences
4. **Service Container Setup**: Guide proper service container configuration
5. **Path Validation**: Verify all paths exist and are accessible
6. **Local Testing**: Run workflows locally with act (Docker-based simulation)
7. **Static Analysis**: Lint workflows with actionlint and yamllint

## When to Use This Skill

Invoke this skill when:
- Creating or modifying GitHub Actions workflows
- Debugging workflow failures in CI
- Setting up new repositories with CI/CD
- Migrating to monorepo architecture
- Adding service containers to workflows
- Experiencing cache-related failures
- Getting "module not found" errors in CI but not locally

## Usage

### Quick Validation

"Validate my GitHub Actions workflows before I push"

I'll:
1. Run actionlint on all workflow files
2. Check for missing cache-dependency-path configurations
3. Validate all working-directory paths exist
4. Verify monorepo build order is correct
5. Check service container configurations
6. Provide a pre-push checklist

### Debugging Workflow Failures

"My GitHub Actions workflow is failing with [error message]"

I'll:
1. Analyze the error message
2. Identify the root cause
3. Explain why local testing didn't catch it
4. Provide the correct configuration
5. Show how to test the fix locally

### Setup New Repository

"Set up GitHub Actions testing for my new project"

I'll:
1. Install required tools (act, actionlint, yamllint)
2. Create validation scripts
3. Set up pre-push hooks
4. Configure recommended workflows
5. Provide testing procedures

## Critical Rules I Enforce

### 1. Cache Configuration

**ALWAYS specify cache-dependency-path explicitly:**

```yaml
# ❌ WRONG
- uses: actions/setup-node@v4
  with:
    cache: 'npm'

# ✅ CORRECT
- uses: actions/setup-node@v4
  with:
    cache: 'npm'
    cache-dependency-path: package-lock.json
```

**Why**: GitHub Actions cache resolution fails silently in local testing but errors in CI with "Some specified paths were not resolved, unable to cache dependencies."

### 2. Monorepo Build Order

**ALWAYS build workspace dependencies before type checking:**

```yaml
# ❌ WRONG
- run: npm ci
- run: npx tsc --noEmit

# ✅ CORRECT
- run: npm ci
- run: npm run build --workspace=@prpm/types
- run: npm run build --workspace=@prpm/registry-client
- run: npx tsc --noEmit
```

**Why**: TypeScript needs compiled output from workspace dependencies. Local development has pre-built artifacts, but CI starts clean.

### 3. npm ci in Monorepos

**ALWAYS run npm ci from root, not workspace directories:**

```yaml
# ❌ WRONG
- working-directory: packages/infra
  run: npm ci

# ✅ CORRECT
- run: npm ci
- working-directory: packages/infra
  run: pulumi preview
```

**Why**: npm workspaces are managed from root. Workspace directories don't have their own package-lock.json.

### 4. Service Containers

**Service containers can't override CMD via options:**

```yaml
# ❌ WRONG
services:
  minio:
    image: minio/minio:latest
    options: server /data  # Ignored!

# ✅ CORRECT
services:
  minio:
    image: minio/minio:latest

steps:
  - run: |
      docker exec $(docker ps -q --filter ancestor=minio/minio:latest) \
        sh -c "minio server /data &"
```

**Why**: GitHub Actions service containers ignore custom commands. They must be started manually in steps.

## Validation Tools

### Required Tools

```bash
# macOS
brew install act actionlint yamllint

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
bash <(curl https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
pip install yamllint
```

### Validation Script

I'll create `.github/scripts/validate-workflows.sh`:

```bash
#!/bin/bash
set -e

echo "🔍 Validating GitHub Actions workflows..."

# 1. Static analysis
actionlint .github/workflows/*.yml
yamllint .github/workflows/*.yml

# 2. Cache configuration check
for file in .github/workflows/*.yml; do
    if grep -q "cache: 'npm'" "$file"; then
        if ! grep -A 2 "cache: 'npm'" "$file" | grep -q "cache-dependency-path"; then
            echo "❌ $file: Missing explicit cache-dependency-path"
            exit 1
        fi
    fi
done

# 3. Path validation
grep -r "working-directory:" .github/workflows/*.yml | while read -r line; do
    dir=$(echo "$line" | sed 's/.*working-directory: //' | tr -d '"')
    if [ ! -d "$dir" ]; then
        echo "❌ Directory does not exist: $dir"
        exit 1
    fi
done

# 4. Check for explicit cache paths
grep -r "cache-dependency-path:" .github/workflows/*.yml | while read -r line; do
    path=$(echo "$line" | sed 's/.*cache-dependency-path: //' | tr -d '"')
    if [ ! -f "$path" ]; then
        echo "❌ Cache dependency path does not exist: $path"
        exit 1
    fi
done

echo "✅ All workflow validations passed"
```

### Pre-Push Checklist

Before pushing workflow changes:

1. **Lint**: `actionlint .github/workflows/*.yml`
2. **Validate**: `.github/scripts/validate-workflows.sh`
3. **Dry Run**: `act pull_request -W .github/workflows/[workflow].yml -n`
4. **Check Cache Paths**: Verify all cache-dependency-path values exist
5. **Check Build Order**: Ensure workspace dependencies built before type checks
6. **Service Containers**: Confirm manual startup if custom commands needed

## Common Failure Patterns

### "Cannot find module '@prpm/types'"

**Root Cause**: Workspace dependency not built before type checking

**Why Local Works**: Previous builds exist in node_modules/

**Fix**:
```yaml
- name: Build @prpm/types
  run: npm run build --workspace=@prpm/types
- name: Type check
  run: npx tsc --noEmit
```

### "Cache resolution error"

**Root Cause**: Missing or incorrect cache-dependency-path

**Why act Doesn't Catch**: act skips caching entirely

**Fix**:
```yaml
- uses: actions/setup-node@v4
  with:
    cache: 'npm'
    cache-dependency-path: package-lock.json  # Explicit!
```

### "npm ci requires package-lock.json"

**Root Cause**: Running npm ci from workspace directory

**Why Local Works**: May have workspace-specific package-lock.json

**Fix**:
```yaml
# Run from root
- run: npm ci
# Then use working-directory for commands
- working-directory: packages/infra
  run: pulumi preview
```

### "Service container not starting"

**Root Cause**: Custom command in options is ignored

**Why Local Works**: docker-compose uses different container runtime

**Fix**:
```yaml
steps:
  - run: docker exec [container] sh -c "command &"
```

## Why act Alone Isn't Enough

Local testing with `act` doesn't catch:

1. **Cache Validation**: act skips GitHub's cache system entirely
2. **Service Commands**: Different container runtime, different behavior
3. **Build Artifacts**: Local has pre-built workspace dependencies
4. **Clean Environment**: CI starts completely fresh every time
5. **GitHub-Specific Features**: Some actions only work on GitHub's runners

**Solution**: Use the complete validation suite (actionlint + custom validators + act dry run)

## Interactive Debugging

When you encounter a workflow failure:

1. **Share the error**: Paste the exact GitHub Actions error message
2. **I'll analyze**: Identify the root cause and why local testing didn't catch it
3. **I'll fix**: Provide corrected workflow configuration
4. **I'll validate**: Show how to test the fix locally
5. **I'll explain**: Clarify why the issue occurred and how to prevent it

## Example Interactions

**User**: "My workflow is failing with 'Some specified paths were not resolved, unable to cache dependencies'"

**Me**: This is a cache resolution error. You're using `cache: 'npm'` without specifying `cache-dependency-path`. GitHub Actions is trying to find package-lock.json but can't locate it.

Here's the fix:
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
    cache-dependency-path: package-lock.json  # Add this
```

This wasn't caught by `act` because it skips caching entirely. To prevent this in the future, run:
```bash
.github/scripts/validate-workflows.sh
```

This script checks for missing cache-dependency-path configurations.

---

**User**: "TypeScript can't find '@prpm/types' in CI but works locally"

**Me**: This is a monorepo build order issue. Your local environment has previously built `@prpm/types`, but CI starts clean.

Add this before your type check:
```yaml
- name: Build @prpm/types
  run: npm run build --workspace=@prpm/types
```

Why local worked: You've previously run `npm run build` which compiled @prpm/types to dist/. That compiled output exists in your node_modules. CI doesn't have this.

To test this scenario locally, delete your dist/ folders and try again:
```bash
rm -rf packages/*/dist
npx tsc --noEmit  # Should fail
npm run build --workspace=@prpm/types
npx tsc --noEmit  # Should pass
```

## Continuous Improvement

After each workflow failure in CI:

1. **Analyze**: Why didn't local testing catch this?
2. **Document**: Add to the common failure patterns
3. **Validate**: Update validation scripts to catch it next time
4. **Test**: Ensure the validator actually catches the issue

## Best Practices

1. **Always validate before pushing**: Run the complete validation suite
2. **Keep tools updated**: `brew upgrade act actionlint yamllint`
3. **Test in clean environment occasionally**: Use Docker to simulate fresh CI
4. **Document failures**: Add new patterns to validation scripts
5. **Use explicit configurations**: Never rely on defaults for cache, paths, or commands

## Summary

This skill helps you:
- ✅ Catch 90%+ of workflow failures before pushing
- ✅ Understand why local testing didn't catch issues
- ✅ Fix common GitHub Actions problems quickly
- ✅ Build confidence in your CI/CD pipeline
- ✅ Reduce iteration time (no more push-fail-fix-push cycles)

Invoke me whenever you're working with GitHub Actions to ensure your workflows are solid before they hit CI.
