---
name: midnight-tooling:midnight-ci
description: Use when setting up CI/CD for Midnight projects, configuring GitHub Actions for Compact contract compilation, running TypeScript tests in CI, validating version consistency, or automating contract builds.
---

# Midnight CI/CD Setup

Configure continuous integration for Midnight smart contract projects using GitHub Actions.

## Overview

CI for Midnight projects should:
1. Verify contract compilation
2. Run TypeScript/JavaScript tests
3. Validate version consistency
4. Optionally run integration tests with proof server

## Quick Start

Copy the appropriate workflow template to your project:

```bash
mkdir -p .github/workflows

# For contract compilation
cp ${CLAUDE_PLUGIN_ROOT}/skills/midnight-ci/templates/github-workflows/compile-contracts.yml .github/workflows/

# For full dApp testing
cp ${CLAUDE_PLUGIN_ROOT}/skills/midnight-ci/templates/github-workflows/test-dapp.yml .github/workflows/
```

## Available Templates

| Template | Purpose |
|----------|---------|
| `compile-contracts.yml` | Basic contract compilation check |
| `test-dapp.yml` | Full dApp testing with proof server |
| `release.yml` | Release workflow with versioning |

## Workflow Configuration

### Environment Setup

All workflows need these tools:
- Node.js 18+
- Compact developer tools and compiler
- Docker (for proof server tests)

### Compact Installation in CI

```yaml
- name: Install Compact developer tools
  run: |
    curl --proto '=https' --tlsv1.2 -LsSf \
      https://github.com/midnightntwrk/compact/releases/latest/download/compact-installer.sh | sh
    echo "$HOME/.compact/bin" >> $GITHUB_PATH

- name: Install Compact compiler
  run: compact update
```

### Caching

Cache Compact compiler for faster builds:

```yaml
- name: Cache Compact compiler
  uses: actions/cache@v4
  with:
    path: ~/.compact
    key: compact-${{ runner.os }}-${{ hashFiles('.compact-version') }}
    restore-keys: |
      compact-${{ runner.os }}-
```

Create `.compact-version` file:
```
0.26.0
```

### Version Pinning

For reproducible CI, pin the compiler version:

```yaml
- name: Install specific compiler version
  run: |
    compact update 0.26.0
    compact compile --version  # Verify
```

## Template Details

### compile-contracts.yml

Minimal workflow for contract compilation:

```yaml
name: Compile Contracts
on: [push, pull_request]

jobs:
  compile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Compact
        run: |
          curl --proto '=https' --tlsv1.2 -LsSf \
            https://github.com/midnightntwrk/compact/releases/latest/download/compact-installer.sh | sh
          echo "$HOME/.compact/bin" >> $GITHUB_PATH
          compact update

      - name: Compile contracts
        run: compact compile contracts/*.compact build/
```

### test-dapp.yml

Full testing with proof server:

```yaml
name: Test dApp
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      proof-server:
        image: midnightnetwork/proof-server:latest
        ports:
          - 6300:6300
        options: >-
          --health-cmd "curl -f http://localhost:6300/health || exit 1"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      # ... setup steps ...

      - name: Run tests
        run: npm test
        env:
          PROOF_SERVER_URL: http://localhost:6300
```

## Best Practices

### 1. Pin All Versions

```yaml
env:
  NODE_VERSION: '20'
  COMPACT_VERSION: '0.26.0'
  PROOF_SERVER_TAG: '4.0.0'
```

### 2. Use npm ci

```yaml
- name: Install dependencies
  run: npm ci
```

### 3. Cache Dependencies

```yaml
- name: Cache node modules
  uses: actions/cache@v4
  with:
    path: node_modules
    key: npm-${{ hashFiles('package-lock.json') }}
```

### 4. Fail Fast on Version Mismatch

Add a version check step:

```yaml
- name: Verify version consistency
  run: |
    COMPILER_VERSION=$(compact compile --version)
    EXPECTED="0.26.0"
    if [[ "$COMPILER_VERSION" != *"$EXPECTED"* ]]; then
      echo "Version mismatch: expected $EXPECTED, got $COMPILER_VERSION"
      exit 1
    fi
```

### 5. Artifact Upload

Save compiled contracts:

```yaml
- name: Upload compiled contracts
  uses: actions/upload-artifact@v4
  with:
    name: contracts
    path: build/
    retention-days: 7
```

## Troubleshooting CI

### Compact not found

Ensure PATH is updated:
```yaml
echo "$HOME/.compact/bin" >> $GITHUB_PATH
```

### Proof server unhealthy

Increase startup time:
```yaml
options: >-
  --health-retries 10
  --health-start-period 30s
```

### Node version issues

Specify exact version:
```yaml
node-version: '20.10.0'
```

### Cache invalidation

Include version in cache key:
```yaml
key: compact-${{ env.COMPACT_VERSION }}-${{ runner.os }}
```

## Additional Resources

- **`templates/github-workflows/`** - Ready-to-use workflow files
- **`references/ci-best-practices.md`** - Detailed CI guidance

For local environment setup, see the `midnight-setup` skill.
