---
name: github-actions
# prettier-ignore
description: Use when creating GitHub Actions workflows - covers CI/CD, matrix testing, and release automation
---

# GitHub Actions Best Practices

## Quick Start

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm test
```

## Core Patterns

### Matrix Testing

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm
      - run: npm ci
      - run: npm test
```

### Caching Dependencies

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: npm  # Automatic npm caching

# Or manual caching
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
```

### Code Coverage

```yaml
- run: npm run test:coverage
- uses: codecov/codecov-action@v4
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
    files: ./coverage/lcov.info
```

### npm Publishing

```yaml
# .github/workflows/publish.yml
name: Publish

on:
  push:
    tags: ["v*"]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # For provenance
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: https://registry.npmjs.org
      - run: npm ci
      - run: npm run build
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### VSCode Extension Publishing

```yaml
- uses: HaaLeo/publish-vscode-extension@v1
  with:
    pat: ${{ secrets.VSCE_TOKEN }}
    registryUrl: https://marketplace.visualstudio.com
```

### Conditional Jobs

```yaml
jobs:
  coverage:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

## Workflow Triggers

```yaml
on:
  push:
    branches: [main]
    paths: ["src/**", "tests/**"]
  pull_request:
  release:
    types: [published]
  workflow_dispatch:  # Manual trigger
```

## Reference Files

- [references/triggers.md](references/triggers.md) - Event triggers
- [references/secrets.md](references/secrets.md) - Secret management
