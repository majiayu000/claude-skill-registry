---
name: release-procedures
description: Version management, release verification, and deployment procedures for software releases. Includes semver guidance, version consistency checks, and platform-specific constraints.
license: MIT
metadata:
  author: groupzer0
  version: "1.0"
---

# Release Procedures

Systematic approach to packaging and releasing software. Use this skill when:
- DevOps prepares a release for deployment
- Implementer updates version files during milestones
- Planner specifies version bumps in plans

## Release Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Two-Stage Release Flow                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STAGE 1: Per-Plan (repeat for each plan in release)            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. QA Complete                                         │    │
│  │  2. UAT Approved                                        │    │
│  │  3. DevOps commits locally (NO PUSH)                    │    │
│  │  4. Update plan status: "Committed for vX.Y.Z"          │    │
│  │  5. Notify Roadmap of commit                            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  STAGE 2: Per-Release (once all plans committed)                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. All plans for release committed                     │    │
│  │  2. User approves release                               │    │
│  │  3. Git tag, push, publish                              │    │
│  │  4. Update all plan statuses: "Released"                │    │
│  │  5. Hand off to Retrospective                           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Semantic Versioning (SemVer)

### Version Format: MAJOR.MINOR.PATCH

| Bump | When | Examples |
|------|------|----------|
| **MAJOR** | Breaking changes | API signature change, removed feature |
| **MINOR** | New features (backward compatible) | New command, added option |
| **PATCH** | Bug fixes (backward compatible) | Fixed crash, corrected behavior |

### Pre-Release Versions

```
1.2.3-alpha.1    # Early development
1.2.3-beta.1     # Feature complete, testing
1.2.3-rc.1       # Release candidate
```

### When to Bump

| Change Type | Version | Rationale |
|-------------|---------|-----------|
| Fix typo in docs | PATCH | No code change |
| Fix bug | PATCH | Backward compatible |
| Add new feature | MINOR | New capability |
| Deprecate feature | MINOR | Still works |
| Remove deprecated | MAJOR | Breaking |
| Change API contract | MAJOR | Breaking |

---

## Version Consistency Checklist

All version references must match before release:

| File | Field | Example |
|------|-------|---------|
| `package.json` | `version` | `"version": "1.2.3"` |
| `CHANGELOG.md` | Latest heading | `## [1.2.3] - 2024-12-19` |
| `README.md` | Badge/install (if versioned) | May be "latest" |
| Platform config | Varies | See platform-specific |

### Verification Command

```bash
# Extract and compare versions
PACKAGE_VERSION=$(jq -r .version package.json)
CHANGELOG_VERSION=$(grep -oP '## \[\K[0-9]+\.[0-9]+\.[0-9]+' CHANGELOG.md | head -1)

if [ "$PACKAGE_VERSION" != "$CHANGELOG_VERSION" ]; then
  echo "VERSION MISMATCH: package.json=$PACKAGE_VERSION, CHANGELOG=$CHANGELOG_VERSION"
  exit 1
fi
```

---

## Platform-Specific Constraints

### VS Code Extensions

| Constraint | Requirement |
|------------|-------------|
| Version format | 3-part semver only (X.Y.Z) |
| Pre-release | Use odd minor version (e.g., 1.1.0) |
| Engine | Specify minimum VS Code version |

```json
{
  "version": "1.2.3",
  "engines": { "vscode": "^1.80.0" }
}
```

### npm Packages

| Constraint | Requirement |
|------------|-------------|
| Version | Standard semver |
| Pre-release | `-alpha.1`, `-beta.1` allowed |
| Deprecation | Use `npm deprecate` |

### Python Packages (PyPI)

| Constraint | Requirement |
|------------|-------------|
| Version | PEP 440 compliant |
| Pre-release | `a1`, `b1`, `rc1` suffixes |
| Location | `setup.py`, `pyproject.toml`, or `__version__` |

---

## CHANGELOG Format

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.2.3] - 2024-12-19

### Added
- New feature description

### Changed
- Modified behavior description

### Fixed
- Bug fix description

### Deprecated
- Feature to be removed

### Removed
- Removed feature

### Security
- Security fix description
```

### Categories Order

1. Added (new features)
2. Changed (changes to existing)
3. Deprecated (soon to be removed)
4. Removed (now removed)
5. Fixed (bug fixes)
6. Security (vulnerability fixes)

---

## Pre-Release Verification

### Mandatory Checks

| Check | Command/Action | Fail Response |
|-------|----------------|---------------|
| UAT Status | Read `agent-output/uat/` | STOP if not "APPROVED FOR RELEASE" |
| QA Status | Read `agent-output/qa/` | STOP if not "QA Complete" |
| Version Match | Compare all version files | STOP and fix |
| Tests Pass | Run test suite | STOP and fix |
| Clean Workspace | `git status` | Commit or stash |
| No Debug | Check for debug flags | Remove before release |

### Pre-Commit Cleanup

```bash
# Ensure no debug artifacts
grep -r "console.log" src/ --include="*.ts" && exit 1
grep -r "debugger" src/ --include="*.ts" && exit 1
grep -r "TODO: remove" src/ && exit 1
```

---

## Release Execution

### Git Tagging

```bash
# Create annotated tag
git tag -a v1.2.3 -m "Release v1.2.3"

# Push tag
git push origin v1.2.3
```

### Publication Commands

| Platform | Command |
|----------|---------|
| VS Code | `vsce publish` |
| npm | `npm publish` |
| PyPI | `twine upload dist/*` |
| GitHub | `gh release create v1.2.3` |

### Post-Publication Verification

| Check | Method |
|-------|--------|
| Version visible | Check marketplace/registry |
| Installable | Fresh install test |
| Changelog visible | Check release notes |
| No errors | Check for publish warnings |

---

## Agent Responsibilities

### DevOps Agent (Two-Stage Release)
- **Stage 1 (Per-Plan)**: After UAT approval, commit changes locally with detailed message. Do NOT push.
- **Stage 2 (Per-Release)**: After all plans committed and user approves release, push and publish.
- Track which plans are committed for current release
- Coordinate with Roadmap agent to maintain release→plan mappings
- Never push without explicit release approval
- Document in `agent-output/deployment/`

### Implementer Agent
- Update `package.json` version during milestones
- Update `CHANGELOG.md` with changes
- Commit version updates as part of implementation
- Follow plan's specified version bump

### Planner Agent
- Specify target release version in plan header
- Multiple plans may share the same target release
- Coordinate with Roadmap agent for release assignments
- Include version update in final milestone

### Roadmap Agent
- Maintain Active Release Tracker section
- Track current working release version
- Monitor plan→release mappings
- Notify when all plans for a release are committed

---

## Rollback Procedure

If release fails:

1. **Unpublish** (if platform allows)
   - npm: `npm unpublish package@version` (within 72h)
   - VS Code: Unpublish via dashboard

2. **Delete tag** (if needed)
   ```bash
   git tag -d v1.2.3
   git push origin :refs/tags/v1.2.3
   ```

3. **Document** in deployment log
4. **Notify** stakeholders of rollback

See [references/release-templates.md](references/release-templates.md) for deployment document templates.
