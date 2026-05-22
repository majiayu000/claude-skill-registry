---
name: goreleaser
description: Initialize or update GoReleaser configuration for automated Go releases with multi-architecture Docker builds, binary distribution, and Homebrew publishing
---

# GoReleaser Setup Skill

Automate Go project releases with cross-platform binaries, multi-architecture Docker images, and package distribution.

## Overview

GoReleaser handles complete release automation for Go projects:
- Building binaries for multiple OS/architectures
- Creating multi-architecture Docker images and manifests
- Publishing to GitHub/GitLab releases
- Generating Homebrew formulas
- Creating automated changelogs
- Calculating checksums and signatures

This skill provides templates and guidance for professional release automation.

## Prerequisites

1. **GoReleaser installed**: `brew install goreleaser` or see https://goreleaser.com/install/
2. **Docker with buildx**: For multi-architecture builds (`docker buildx version`)
3. **Git tags**: GoReleaser works with semantic versioning tags (e.g., `v1.0.0`)
4. **GitHub/GitLab token**: For release creation and Homebrew tap updates
5. **Project structure**: Go module with `cmd/` directory (or adjust `dir` field)

## Quick Start

### Step 1: Analyze Project Structure

Understand your project:

```bash
# Check for existing configuration
ls -la .goreleaser.yml .goreleaser.yaml

# Identify build entry point
find . -name "main.go" -type f

# Verify Go module
cat go.mod
```

### Step 2: Copy Template Files

Copy templates from `assets/` directory:

```bash
# Copy GoReleaser config
cp assets/.goreleaser.yml .

# Copy Dockerfile
cp assets/Dockerfile .

# Copy resources (for Docker)
mkdir -p resources/etc
cp assets/resources/etc/passwd resources/etc/
```

### Step 3: Customize Configuration

Update `.goreleaser.yml` with project-specific values:

1. **Project name**: Replace `PROJECT_NAME` with actual name
2. **Build configuration**:
   - Set `dir` if main.go is not in `cmd/`
   - Adjust `ldflags` for version injection
   - Configure target OS/architectures
3. **Docker registry**: Update image templates
   - GitHub: `ghcr.io/OWNER/PROJECT`
   - GitLab: `registry.gitlab.com/OWNER/PROJECT`
   - Docker Hub: `docker.io/OWNER/PROJECT`
4. **Homebrew tap** (optional): Configure repository and token

### Step 4: Update Dockerfile

Customize the Dockerfile:

1. Replace `PROJECT_BINARY` with actual binary name
2. Adjust user name in both Dockerfile and `resources/etc/passwd`
3. Add any additional runtime dependencies

### Step 5: Set Up CI/CD Integration

Add environment variables to CI/CD:

```bash
# GitHub Actions
GITHUB_TOKEN          # Automatic in GitHub Actions
HOMEBREW_TAP_TOKEN    # If publishing to Homebrew

# GitLab CI
GITLAB_TOKEN          # Automatic in GitLab CI
HOMEBREW_TAP_TOKEN    # If publishing to Homebrew
```

### Step 6: Test Configuration

Validate before tagging:

```bash
# Check configuration
goreleaser check

# Create snapshot build (no release)
goreleaser build --snapshot --clean

# Test full release process
goreleaser release --snapshot --clean --skip=publish
```

### Step 7: Create Release

When ready:

```bash
# Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Run GoReleaser (usually in CI/CD)
goreleaser release --clean
```

## Template Files & Patterns

Templates in `assets/` directory:
- `.goreleaser.yml` - Complete config with multi-arch Docker, Homebrew, archives
- `Dockerfile` - Optimized multi-stage Docker build
- `resources/etc/passwd` - Non-root container user config

For simpler patterns (binary-only, Docker-only, private registries), see [REFERENCE.md](REFERENCE.md).

## Task Runner Integration

Integrate with Taskfile.yml:

```yaml
version: '3'

tasks:
  release:check:
    desc: Validate GoReleaser config
    cmds:
      - goreleaser check

  release:snapshot:
    desc: Test release build
    cmds:
      - goreleaser release --snapshot --clean --skip=publish

  release:
    desc: Create production release
    cmds:
      - goreleaser release --clean
```

## Expected Output

After using this skill, the project will have:
- ✓ `.goreleaser.yml` configured for the project
- ✓ `Dockerfile` for multi-architecture builds
- ✓ `resources/etc/passwd` for non-root container user
- ✓ CI/CD pipeline ready for automated releases
- ✓ Tested snapshot builds

Users can then create releases by simply pushing Git tags.

## Additional Documentation

- **Configuration patterns and examples**: See [REFERENCE.md](REFERENCE.md)
- **Troubleshooting common issues**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Template files**: Available in `assets/` directory

## Best Practices

1. **Semantic Versioning**: Use `v1.2.3` format for tags
2. **Conventional Commits**: Enables automatic changelog generation
3. **Test Snapshots**: Always test with `--snapshot` before tagging
4. **Multi-arch Testing**: Verify builds work on target architectures
5. **Secret Management**: Never commit tokens, use CI/CD secrets

## Resources

- **Official docs**: https://goreleaser.com
- **Example configs**: https://github.com/goreleaser/goreleaser/tree/main/.github/workflows
- **Docker buildx**: https://docs.docker.com/buildx/working-with-buildx/
- **Conventional commits**: https://www.conventionalcommits.org/
