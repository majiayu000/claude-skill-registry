---
name: release-workflow
description: Use when preparing or executing a release of peek-stash-browser. Covers the full release lifecycle from validation through Docker image publishing.
---

# Release Workflow

## Overview

Releases are triggered by pushing git tags. GitHub Actions builds and publishes Docker images automatically.

```
Pre-release validation → Version bump → Commit → Tag → Push → GitHub Actions → Docker Hub
```

## Version Scheme

- **Stable**: `X.Y.Z` (e.g., `3.3.1`)
- **Beta**: `X.Y.Z-beta.N` (e.g., `3.3.2-beta.1`)
- **Tag format**: `vX.Y.Z` or `vX.Y.Z-beta.N`

Both `client/package.json` and `server/package.json` must always have identical versions.

## Step 1: Pre-Release Validation

Run `/pre-release` to execute all checks:

1. Server unit tests: `cd server && npm test`
2. Server linting: `cd server && npm run lint`
3. Client unit tests: `cd client && npm test`
4. Client linting: `cd client && npm run lint`
5. Integration tests: `cd server && npm run test:integration`
6. Client build: `cd client && npm run build`
7. Docker production build: `docker build -f Dockerfile.production -t peek:test .`

All 7 checks must pass before proceeding.

## Step 2: Version Bump & Tag

### Beta Release

Run `/release-beta`:

- Increment beta number: `3.3.2-beta.1` → `3.3.2-beta.2`
- Or start new beta: `3.3.1` → `3.3.2-beta.1`

### Stable Release

Run `/release-stable`:

- Remove beta suffix: `3.3.2-beta.8` → `3.3.2`
- Or increment: `3.3.2` → `3.3.3` or `3.4.0`

### What the Release Skills Do

1. Verify on `main` branch and up to date
2. Update version in `client/package.json` and `server/package.json`
3. Commit: `chore: bump version to X.Y.Z`
4. Push commit to main
5. Create tag: `git tag vX.Y.Z`
6. Push tag: `git push origin vX.Y.Z`

## Step 3: Automated CI/CD

GitHub Actions (`.github/workflows/docker-build.yml`) triggers on `v*` tags:

1. **Build**: Multi-stage Dockerfile.production (frontend → backend → runtime)
2. **Platforms**: `linux/amd64` + `linux/arm64`
3. **Push to Docker Hub**: `carrotwaxr/peek-stash-browser`
4. **Tag strategy**:
   - Semver: `3.3.2`
   - Major.minor: `3.3`
   - `latest` (stable releases only)
   - `stable` (stable releases only)
   - `beta` (beta releases only)
5. **GitHub Release**: Auto-created with generated release notes, marked as prerelease if beta

## Docker Hub Tags After Release

| Release Type | Tags Applied |
|-------------|-------------|
| `v3.3.2` (stable) | `3.3.2`, `3.3`, `latest`, `stable` |
| `v3.3.2-beta.1` | `3.3.2-beta.1`, `beta` |

## Updating on unRAID

After GitHub Actions completes:

```bash
# SSH to your deployment server
ssh root@<server-ip>

# Pull new image
docker pull carrotwaxr/peek-stash-browser:latest  # or :beta

# Restart container via unRAID WebGUI or CLI
docker stop peek-stash-browser && docker start peek-stash-browser
```

## Semantic Versioning Guide

- **Patch** (3.3.X): Bug fixes, minor tweaks, no new features
- **Minor** (3.X.0): New features, backward-compatible changes
- **Major** (X.0.0): Breaking changes (rare — major UI overhauls, API changes)
