---
name: install-workflow
description: Create GitHub Actions workflows for automated package building and distribution. Use in package phase to automate .mojopkg building and release creation.
mcp_fallback: none
category: ci
user-invocable: false
---

# CI Package Workflow Skill

Create GitHub Actions workflows for automated packaging.

## When to Use

- Package phase of development
- Automating release process
- Building distributable packages
- Creating GitHub releases

## Quick Reference

```yaml
name: Build Packages
on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Packages
        run: ./scripts/build_all_packages.sh
      - uses: softprops/action-gh-release@v1
        with:
          files: packages/*.mojopkg
```

## Workflow Structure

### Triggers

```yaml
on:
  push:
    tags:
      - 'v*.*.*'  # Semantic versioning
  workflow_dispatch:    # Manual trigger
```

### Jobs

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Mojo
        run: # Install Mojo environment
      - name: Build Packages
        run: ./scripts/build_all_packages.sh
      - name: Create Release
        uses: softprops/action-gh-release@v1
```

## Workflow Types

### 1. Build on Tag Release

Automatically build when version tag created:

```yaml
on:
  push:
    tags:
      - 'v*'
```

### 2. Build on PR

Validate packaging on pull requests:

```yaml
on:
  pull_request:
    paths:
      - 'src/**'
      - 'scripts/build_*.sh'
```

### 3. Manual Trigger

Allow on-demand builds with parameters:

```yaml
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to build'
        required: true
```

## Best Practices

- Cache dependencies between runs
- Upload artifacts for inspection
- Create GitHub releases with notes
- Test installation in clean environment
- Tag releases with semantic versioning
- Document build requirements

## Error Handling

| Error | Fix |
|-------|-----|
| Action version invalid | Use latest stable version (v4, not @main) |
| Missing environment | Add setup step before build |
| Build script not found | Verify script path and permissions |
| Artifact not uploaded | Check build produces expected files |

## References

- Related skill: `validate-workflow` for syntax validation
- Workflow examples: `.github/workflows/`
- GitHub Actions docs: <https://docs.github.com/en/actions>
