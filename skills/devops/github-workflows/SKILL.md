---
name: github-workflows
description: Initialize or update GitHub Actions workflows for Go projects with comprehensive CI/CD pipelines including linting, testing, coverage, snapshot builds, and releases
---

# GitHub Workflows Setup Skill

Automate Go project CI/CD with production-ready GitHub Actions workflows for testing, linting, coverage reporting, and releases.

## Overview

This skill provides a complete GitHub Actions CI/CD setup for Go projects:

- **Linting**: Automated code quality checks with golangci-lint
- **Coverage**: Test coverage reporting with badge generation
- **Snapshot**: Test release builds on every push
- **Release**: Automated releases with GoReleaser on tag push
- **Dependabot**: Automated dependency updates
- **Funding**: GitHub Sponsors configuration

All workflows integrate with [Task](https://taskfile.dev) for consistent build commands.

## Prerequisites

1. **GitHub repository**: Project hosted on GitHub
2. **Go module**: Project uses Go modules (`go.mod` present)
3. **Task runner** (recommended): Taskfile.yml for build commands
   - Install: `brew install go-task/tap/go-task`
   - Docs: https://taskfile.dev
4. **GoReleaser config** (for releases): `.goreleaser.yml` in repository root
5. **GitHub Container Registry**: Enabled for Docker image publishing

## Workflow Architecture

| Workflow | Trigger | Purpose | Permissions |
|----------|---------|---------|-------------|
| **linter.yml** | Every push | Code quality validation | `contents: read` |
| **snapshot.yml** | Every push | Test release process | `contents: read` |
| **coverage.yml** | Push to main | Generate coverage badge | `contents: write` |
| **release.yml** | Push tags | Production release | `contents: write`, `packages: write` |

Workflow files are located in `assets/workflows/` directory.

## Quick Start

### Step 1: Copy Workflow Files

```bash
# Create directories
mkdir -p .github/workflows

# Copy workflows from assets
cp assets/workflows/*.yml .github/workflows/

# Copy configurations
cp assets/dependabot.yml .github/dependabot.yml
cp assets/FUNDING.yml .github/FUNDING.yml
```

### Step 2: Configure Taskfile (Recommended)

Create or update `Taskfile.yml`:

```yaml
version: '3'

tasks:
  linter:
    desc: Run golangci-lint
    cmds:
      - golangci-lint run ./...

  test:
    desc: Run tests
    cmds:
      - go test -v ./...

  snapshot:
    desc: Create snapshot build (test release)
    cmds:
      - goreleaser release --snapshot --clean --skip=publish

  release:
    desc: Create production release
    cmds:
      - goreleaser release --clean
```

### Step 3: Customize Go Version

Update Go version in all workflows:

```yaml
- uses: actions/setup-go@v6
  with:
    go-version: '1.24'  # CUSTOMIZE: Use your Go version
```

### Step 4: Customize Coverage Settings

In `.github/workflows/coverage.yml`:

```yaml
- name: Generate coverage badge
  with:
    limit-coverage: "70"  # CUSTOMIZE: Set your coverage threshold
```

### Step 5: Update Funding Configuration

Update `.github/FUNDING.yml`:

```yaml
github: [YOUR_GITHUB_USERNAME]  # CUSTOMIZE
```

### Step 6: Configure GitHub Settings

Enable required GitHub features:

**Actions Permissions**:
- Settings → Actions → General
- Set "Workflow permissions" to "Read and write permissions"

**GitHub Container Registry**:
- Settings → Packages
- Enable "Inherit access from repository"

**Branch Protection** (optional):
- Settings → Branches → Add rule
- Require status checks: `linter`, `goreleaser-snapshot`

**Secrets** (if needed):
- Settings → Secrets → Actions
- Add `HOMEBREW_TAP_TOKEN` (if using Homebrew in GoReleaser)

### Step 7: Test Workflows

```bash
# 1. Push changes to trigger linter and snapshot
git add .github/
git commit -m "ci: add GitHub Actions workflows"
git push origin main

# 2. Check workflow runs at: https://github.com/OWNER/REPO/actions

# 3. Test release workflow (without publishing)
git tag -a v0.1.0-test -m "Test release"
git push origin v0.1.0-test

# 4. If successful, create real release
git tag -a v1.0.0 -m "First release"
git push origin v1.0.0
```

## Status Badges (Optional)

Add workflow badges to README.md:

```markdown
[![Linter](https://github.com/OWNER/REPO/actions/workflows/linter.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/linter.yml)
[![Release](https://github.com/OWNER/REPO/actions/workflows/release.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/release.yml)
![Coverage](https://raw.githubusercontent.com/OWNER/REPO/main/coverage-badge.svg)
```

## Expected Output

After using this skill, your repository will have:
- ✓ Complete CI/CD pipeline with 4 workflows
- ✓ Automated linting on every push
- ✓ Snapshot builds to validate releases
- ✓ Coverage badges showing test coverage
- ✓ Automated releases on Git tags
- ✓ Dependabot for dependency updates
- ✓ GitHub Sponsors configuration
- ✓ Production-ready workflow structure

Your project will have professional-grade CI/CD matching industry best practices.

## Additional Documentation

- **Detailed configurations and customization**: See [REFERENCE.md](REFERENCE.md)
- **Troubleshooting common issues**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Workflow templates**: Available in `assets/workflows/` directory

## Resources

- **GitHub Actions**: https://docs.github.com/en/actions
- **Task Runner**: https://taskfile.dev
- **golangci-lint**: https://golangci-lint.run
- **GoReleaser**: https://goreleaser.com
- **Dependabot**: https://docs.github.com/en/code-security/dependabot
