---
name: configuring-github-actions
description: Create and troubleshoot GitHub Actions workflows. Use when editing .github/workflows files, setting up CI/CD pipelines, configuring matrix builds for multi-platform testing, debugging failing workflows, adding caching or artifacts, running E2E tests in containers, or asking "why is my workflow failing" or "how do I test on multiple OSes".
---

# GitHub Actions CI/CD Guide

## Quick Reference

| Topic | Reference |
|-------|-----------|
| E2E tests, containers, expect | [testing-patterns.md](references/testing-patterns.md) |
| Permissions, secrets, security | [security.md](references/security.md) |
| Debugging, caching, performance | [optimization.md](references/optimization.md) |

**Triggers**: `push`, `pull_request`, `release`, `workflow_dispatch`, `schedule`
**Runners**: `ubuntu-latest`, `macos-latest`, `macos-13`, `windows-latest`
**Contexts**: `${{ github.event_name }}`, `${{ github.ref }}`, `${{ runner.os }}`, `${{ matrix.* }}`

## Project Workflows

- **installer-ci.yml**: Build → test → E2E (matrix: ubuntu, debian, fedora, centos containers + macOS)
- **release.yml**: GoReleaser on version tags

## Core Template

```yaml
name: CI

on:
  pull_request:
    paths: ["component/**", ".github/workflows/ci.yml"]
  push:
    branches: [main]
    paths: ["component/**"]

concurrency:
  group: ${{ github.workflow }}-${{ github.head_ref || github.ref }}
  cancel-in-progress: true

permissions: {}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
      - run: go build -v ./...
```

## Essential Patterns

### Concurrency Control
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.head_ref || github.ref }}
  cancel-in-progress: true
```

### Permissions (least privilege)
```yaml
permissions: {}  # Top-level default

jobs:
  build:
    permissions:
      contents: read  # Job-level grants
```

### Caching
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/go-build
      ~/go/pkg/mod
    key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
    restore-keys: ${{ runner.os }}-go-
```

### Artifacts
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: build-artifacts
    path: dist/
    retention-days: 1
    if-no-files-found: error

- uses: actions/download-artifact@v4
  with:
    name: build-artifacts
    path: dist/
```

### Matrix Builds
```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      - os: ubuntu-latest
        platform: ubuntu
      - os: ubuntu-latest
        platform: debian
        container: debian:bookworm
      - os: macos-latest
        platform: macos

runs-on: ${{ matrix.os }}
container: ${{ matrix.container }}
```

## Common Actions

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0  # Full history

- uses: actions/setup-go@v5
  with:
    go-version-file: go.mod

- uses: goreleaser/goreleaser-action@v6
  with:
    version: latest
    args: build --clean --snapshot
    workdir: installer
```
