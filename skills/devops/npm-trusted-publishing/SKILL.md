---
name: npm-trusted-publishing
description: Use when setting up npm publishing with GitHub Actions - provides trusted publishing with OIDC, provenance attestations, and monorepo configuration
---

# NPM Trusted Publishing

## Overview

Set up secure npm publishing from GitHub Actions using OIDC trusted publishing instead of long-lived NPM_TOKEN secrets.

## When to Use

- Setting up npm publish workflow in GitHub Actions
- Migrating from NPM_TOKEN to trusted publishing
- Adding provenance attestations to packages
- Publishing monorepo packages

## Quick Reference

| Requirement | Implementation |
|-------------|----------------|
| GitHub Actions permission | `id-token: write` |
| package.json field | `repository.url` matching GitHub repo |
| npm publish flag | `--provenance` |
| npmjs.com setup | Configure trusted publisher per package |

## Implementation

### 1. GitHub Actions Workflow

```yaml
permissions:
  contents: write
  id-token: write  # Required for OIDC

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          registry-url: "https://registry.npmjs.org"

      - run: npm ci
      - run: npm run build

      # No NODE_AUTH_TOKEN needed - uses OIDC
      - run: npm publish --access public --provenance
```

### 2. package.json Repository Field

```json
{
  "name": "@scope/package",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/owner/repo.git",
    "directory": "packages/subpackage"
  }
}
```

**Monorepo note:** Include `directory` field for packages not at repo root.

### 3. npmjs.com Configuration

For each package, go to **Settings > Publishing access** and add:
- Repository: `owner/repo`
- Workflow: `publish.yml` (or your workflow filename)
- Environment: (optional)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing `--provenance` flag | Add to npm publish command |
| Wrong URL format | Use `git+https://github.com/...` |
| Missing `id-token: write` | Add to workflow permissions |
| Forgot npmjs.com setup | Configure trusted publisher in package settings |
| Using NODE_AUTH_TOKEN | Remove - OIDC handles auth |
| Outdated npm version | Add `npm install -g npm@latest` step (see below) |

## npm Version Requirement

GitHub Actions runners may have an outdated npm version that doesn't properly support OIDC trusted publishing. This causes a confusing error:

```
npm notice Access token expired or revoked. Please try logging in again.
npm error code E404
npm error 404 Not Found - PUT https://registry.npmjs.org/@scope%2fpackage - Not found
```

**Solution:** Update npm to latest before publishing:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: "20"
    registry-url: "https://registry.npmjs.org"

- name: Update npm to latest
  run: npm install -g npm@latest

- run: npm publish --access public --provenance
```

See [GitHub Community Discussion #173102](https://github.com/orgs/community/discussions/173102) for details.

## Reference

- npm docs: https://docs.npmjs.com/trusted-publishers
