---
name: "Project Deployment Skill"
description: "Universal deployment patterns for any project type."
applyTo: "**/*release*,**/*deploy*,**/*publish*,**/package.json,**/pyproject.toml,**/*.csproj,**/Cargo.toml"
---

# Project Deployment Skill

> Universal deployment patterns for any project type.

**Inheritance**: `inheritable` — Available to all heirs

## Purpose

Generic deployment knowledge that helps with releasing, publishing, and deploying any type of project. Works across package managers, languages, and platforms.

---

## Quick Reference

### Deployment Decision Tree

```text
Need to deploy?
├─ Is it a package/library?
│   ├─ npm → npm publish
│   ├─ PyPI → twine upload
│   ├─ NuGet → dotnet nuget push
│   └─ Cargo → cargo publish
├─ Is it a web app?
│   ├─ Static → Deploy to CDN/hosting
│   ├─ Server → Container or VM deployment
│   └─ Serverless → Function deployment
└─ Is it a desktop app?
    ├─ Installer → Build & sign installer
    └─ App store → Platform-specific process
```

---

## Pre-Deployment Checklist

**Always complete before deploying:**

- [ ] **Version bumped** — Follow semantic versioning
- [ ] **Changelog updated** — Document what changed
- [ ] **Tests passing** — All automated tests green
- [ ] **Build succeeds** — Clean build from scratch
- [ ] **Credentials valid** — API keys, tokens not expired
- [ ] **Git clean** — No uncommitted changes

---

## Common Package Managers

### npm (Node.js)

```bash
# Check what will be published
npm pack --dry-run

# Publish to npm
npm publish

# Publish scoped package publicly
npm publish --access public

# Publish beta/prerelease
npm publish --tag beta
```

### PyPI (Python)

```bash
# Build distribution
python -m build

# Check package
twine check dist/*

# Upload to PyPI
twine upload dist/*

# Upload to TestPyPI first
twine upload --repository testpypi dist/*
```

### NuGet (.NET)

```bash
# Pack
dotnet pack -c Release

# Push to NuGet
dotnet nuget push *.nupkg --api-key YOUR_API_KEY --source https://api.nuget.org/v3/index.json
```

### Cargo (Rust)

```bash
# Dry run
cargo publish --dry-run

# Publish to crates.io
cargo publish
```

---

## Versioning

### Semantic Versioning (SemVer)

```text
MAJOR.MINOR.PATCH

MAJOR = Breaking changes (1.0.0 → 2.0.0)
MINOR = New features, backward compatible (1.0.0 → 1.1.0)
PATCH = Bug fixes, backward compatible (1.0.0 → 1.0.1)
```

### Pre-release Versions

```text
1.0.0-alpha.1    # Early testing
1.0.0-beta.1     # Feature complete, testing
1.0.0-rc.1       # Release candidate
```

### Version Commands

```bash
# npm
npm version patch  # 1.0.0 → 1.0.1
npm version minor  # 1.0.0 → 1.1.0
npm version major  # 1.0.0 → 2.0.0

# Python (in pyproject.toml or setup.py)
# Manual edit or use bump2version

# .NET (in .csproj)
# <Version>1.0.0</Version>
```

---

## Changelog Best Practices

### Keep a CHANGELOG Format

```markdown
# Changelog

## [Unreleased]

## [1.1.0] - 2026-02-01

### Added
- New feature X

### Changed
- Improved performance of Y

### Fixed
- Bug in Z

### Deprecated
- Old API method (use new method instead)

### Removed
- Legacy support for A

### Security
- Fixed vulnerability in B
```

### Categories

| Category | When to Use |
|----------|-------------|
| Added | New features |
| Changed | Changes in existing functionality |
| Deprecated | Features that will be removed |
| Removed | Features that were removed |
| Fixed | Bug fixes |
| Security | Security-related fixes |

---

## CI/CD Patterns

### GitHub Actions Release

```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: npm ci && npm run build
      - name: Publish
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Azure Pipelines Release

```yaml
trigger:
  tags:
    include:
      - v*

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: '20.x'
  - script: npm ci && npm run build
  - script: npm publish
    env:
      NODE_AUTH_TOKEN: $(NPM_TOKEN)
```

---

## Rollback Strategies

### npm

```bash
# Unpublish within 72 hours
npm unpublish package@version

# Deprecate (preferred over unpublish)
npm deprecate package@version "Security issue, use version X"
```

### PyPI

```bash
# Cannot delete, but can yank
# Go to PyPI web interface → Manage → Yank
```

### General Rollback

1. **Don't panic** — Most package managers support quick fixes
2. **Document the issue** — Update changelog
3. **Publish fix** — New patch version with fix
4. **Communicate** — Notify users if critical

---

## Troubleshooting

### Authentication Errors

| Error | Likely Cause | Solution |
|-------|--------------|----------|
| 401 Unauthorized | Token expired | Generate new token |
| 403 Forbidden | Wrong permissions | Check token scopes |
| 404 Not Found | Wrong registry URL | Verify registry config |

### Common Issues

| Issue | Solution |
|-------|----------|
| "Package already exists" | Bump version number |
| "Invalid package name" | Check naming conventions |
| "Missing files" | Check `.npmignore` or equivalent |
| "Build failed" | Run build locally first |

---

## Project-Specific Deployment

When deploying a specific project type, ask Alex to help identify:

1. **What type of project is this?** (library, app, service)
2. **Where does it deploy to?** (npm, PyPI, Azure, AWS, etc.)
3. **What are the project's deployment scripts?** (check package.json, Makefile, etc.)
4. **Are there environment-specific configs?** (staging vs production)

Alex will adapt this general knowledge to your specific project context.

---

## Related Skills

- **git-workflow** — Version control and tagging
- **infrastructure-as-code** — Cloud resource deployment
- **security-review** — Pre-deployment security checks
