---
name: release-please-development
description: This skill should be used when the user asks to "set up release please", "configure automated releases", "manage version numbers", "add changelog automation", or mentions release-please, semantic versioning, or monorepo versioning.
---

# Release Please Development

Configure automated versioning, changelog generation, and releases using Google's release-please.

## Quick Reference

- [Single Package Pattern](./references/examples/single-package.md) - Simple repos with one version
- [Multi-Package Pattern](./references/examples/multi-package.md) - Monorepos with independent versions
- [Configuration Options](./references/configuration.md) - All available settings

## Overview

Release-please automates:
- Version bumping based on conventional commits
- CHANGELOG.md generation
- GitHub release creation
- Version updates in files (package.json, Chart.yaml, etc.)

## Core Files

```
.github/
├── release-please-config.json    # Package configuration
├── release-please-manifest.json  # Current version tracking
└── workflows/
    └── release.yaml              # GitHub Actions workflow
```

## When to Use Each Pattern

| Pattern | Use Case |
|---------|----------|
| Single Package | Libraries, CLIs, simple apps with one version |
| Multi-Package | Monorepos, services with independent release cycles |

## Basic Setup

### 1. Create Config File

`.github/release-please-config.json`:

```json
{
  "release-type": "simple",
  "packages": {
    ".": {
      "changelog-path": "CHANGELOG.md"
    }
  }
}
```

### 2. Create Manifest

`.github/release-please-manifest.json`:

```json
{
  ".": "0.0.1"
}
```

### 3. Add GitHub Workflow

`.github/workflows/release.yaml`:

```yaml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          config-file: .github/release-please-config.json
          manifest-file: .github/release-please-manifest.json
```

## Release Types

| Type | Use Case | Versions |
|------|----------|----------|
| `simple` | Generic projects | CHANGELOG only |
| `node` | npm packages | package.json |
| `python` | Python packages | setup.py, pyproject.toml |
| `go` | Go modules | go.mod |
| `helm` | Helm charts | Chart.yaml |

## Updating Extra Files

Use `extra-files` to update versions in arbitrary files:

```json
{
  "packages": {
    ".": {
      "extra-files": [
        {
          "type": "json",
          "path": "manifest.json",
          "jsonpath": "$.version"
        }
      ]
    }
  }
}
```

## Conventional Commits

Release-please uses commit prefixes to determine version bumps:

| Prefix | Version Bump | Example |
|--------|--------------|---------|
| `feat:` | Minor (0.x.0) | New feature |
| `fix:` | Patch (0.0.x) | Bug fix |
| `feat!:` or `BREAKING CHANGE` | Major (x.0.0) | Breaking change |
| `docs:`, `chore:`, etc. | None | No release |

## How It Works

1. Push commits to main with conventional commit messages
2. Release-please creates/updates a release PR
3. Merge the release PR to create a GitHub release
4. Tags and changelog are automatically generated

## See Also

- [Single Package Example](./references/examples/single-package.md) - Detailed single-package setup
- [Multi-Package Example](./references/examples/multi-package.md) - Monorepo configuration
- [Configuration Reference](./references/configuration.md) - All options explained
