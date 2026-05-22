# Deploy Workflow

Multi-step workflow for deploying ccswarm releases.

## Overview

This skill guides you through the complete deployment process for ccswarm releases, from building to publishing.

## Pre-Deployment Checklist

### 1. Version Update
```bash
# Update version in Cargo.toml files
# Root workspace
# crates/ccswarm/Cargo.toml
# crates/ai-session/Cargo.toml
```

### 2. Quality Gates
```bash
# Run full quality check
cargo fmt --all
cargo clippy --workspace -- -D warnings
cargo test --workspace

# Check for security vulnerabilities
cargo audit

# Verify documentation
cargo doc --no-deps --workspace
```

### 3. Changelog Update
```bash
# Update CHANGELOG.md with new version
# Include: Features, Bug Fixes, Breaking Changes
```

## Build Process

### 1. Release Build
```bash
# Build all binaries in release mode
cargo build --release --workspace

# Verify binaries
ls -la target/release/ccswarm
ls -la target/release/ai-session
ls -la target/release/ai-session-server
```

### 2. Cross-Platform Builds
```bash
# Linux x86_64
cargo build --release --target x86_64-unknown-linux-gnu

# macOS ARM64
cargo build --release --target aarch64-apple-darwin

# macOS Intel
cargo build --release --target x86_64-apple-darwin
```

### 3. Package Artifacts
```bash
# Create release archives
tar -czvf ccswarm-linux-x86_64.tar.gz -C target/x86_64-unknown-linux-gnu/release ccswarm ai-session
tar -czvf ccswarm-macos-arm64.tar.gz -C target/aarch64-apple-darwin/release ccswarm ai-session
```

## Release Process

### 1. Git Tag
```bash
# Create annotated tag
git tag -a v0.X.Y -m "Release v0.X.Y"

# Push tag
git push origin v0.X.Y
```

### 2. GitHub Release
```bash
# Create release with gh CLI
gh release create v0.X.Y \
  --title "ccswarm v0.X.Y" \
  --notes-file CHANGELOG.md \
  ccswarm-linux-x86_64.tar.gz \
  ccswarm-macos-arm64.tar.gz
```

### 3. Crates.io (Optional)
```bash
# Publish ai-session first (dependency)
cd crates/ai-session
cargo publish

# Then publish ccswarm
cd crates/ccswarm
cargo publish
```

## Post-Deployment

### 1. Verify Release
```bash
# Test installation from release
cargo install ccswarm --version 0.X.Y

# Or download and test binary
curl -L https://github.com/nwiizo/ccswarm/releases/download/v0.X.Y/ccswarm-linux-x86_64.tar.gz | tar xz
./ccswarm --version
```

### 2. Update Documentation
- Update README with new features
- Update version references in docs
- Announce release (if applicable)

## Rollback Procedure

If issues are found after release:

```bash
# Delete release tag
git tag -d v0.X.Y
git push origin :refs/tags/v0.X.Y

# Delete GitHub release
gh release delete v0.X.Y

# Yank from crates.io (if published)
cargo yank --version 0.X.Y ccswarm
```

## Environment Variables

Required for deployment:
- `CARGO_REGISTRY_TOKEN`: For crates.io publishing
- `GITHUB_TOKEN`: For gh CLI operations
