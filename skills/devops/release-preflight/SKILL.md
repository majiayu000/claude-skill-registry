---
name: "Release Preflight Skill"
description: "Pre-checks, version consistency, and deployment discipline."
applyTo: "**/*release*,**/*publish*,**/*deploy*,**/*version*,**/package.json,**/CHANGELOG*"
---

# Release Preflight Skill

> Pre-checks, version consistency, and deployment discipline.

## The Golden Rule

> **NEVER publish without running the preflight checklist.**

## Quick Start

```powershell
# Full preflight check
scripts/release-preflight.ps1

# With packaging test
scripts/release-preflight.ps1 -Package

# Skip time-consuming tests
scripts/release-preflight.ps1 -SkipTests
```

## Version Locations (Must Stay Synchronized)

| # | Location | Field | Example |
| - | -------- | ----- | ------- |
| 1 | `platforms/vscode-extension/package.json` | `version` | `"5.1.0"` |
| 2 | `CHANGELOG.md` | Latest heading | `## [5.1.0] - 2026-02-07` |
| 3 | `.github/copilot-instructions.md` | `**Version**:` line | `**Version**: 5.1.0` |
| 4 | `platforms/vscode-extension/.github/copilot-instructions.md` | Same as #3 |
| 5 | `docs/index.html` | Footer version | `v5.1.0` |
| 6 | `ROADMAP-UNIFIED.md` | Quick Status table | Master 5.1.0 row |
| 7 | Git tag | Tag name | `v5.1.0` |

## Preflight Gates

| Gate | Check | Script Flag |
|------|-------|-------------|
| 0 | PAT configured | Always |
| 1 | Version sync (all 7 locations) | Always |
| 2 | Build passes | Always |
| 3 | Lint passes | Always |
| 4 | Tests pass | `-SkipTests` to skip |
| 5 | Package creates | `-Package` to include |
| 6 | Human review | Manual |

## Full Release Workflow

```powershell
# VS Code Extension release
scripts/release-vscode.ps1 -BumpType minor

# M365 Agent release  
scripts/release-m365.ps1 -Validate
```

## Version Bump Only

```powershell
# 1. Bump
npm version patch --no-git-tag-version

# 2. Get version
$v = (Get-Content package.json | ConvertFrom-Json).version

# 3. Update CHANGELOG, commit, tag, push
git add -A; git commit -m "release: v$v"; git tag "v$v"; git push --tags
```

## Common Mistakes

| Mistake | Prevention |
| ------- | ---------- |
| Published without version bump | Run preflight first |
| CHANGELOG not updated | Script checks this |
| Forgot to push tags | Script does this |
| Version mismatch | Grep entire repo for old version |
| PAT 401 error | Refresh PAT before release |

## Related Scripts

| Script | Purpose |
|--------|---------|
| `scripts/release-preflight.ps1` | Pre-release validation |
| `scripts/release-vscode.ps1` | Full VS Code release |
| `scripts/release-m365.ps1` | M365 agent packaging |
| `.github/muscles/build-extension-package.ps1` | Full build (sync + compile + PII scan) |
| `.github/muscles/sync-architecture.js` | Canonical Master → Heir sync |

## Triggers

- "release", "publish", "deploy"
- "preflight", "pre-release check"
- "version bump", "version sync"

---

*Scripts: `scripts/release-preflight.ps1`, `scripts/release-vscode.ps1`*
