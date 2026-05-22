---
name: ln-710-dependency-upgrader
description: Coordinates dependency upgrades across all detected package managers
---

# ln-710-dependency-upgrader

**Type:** L2 Domain Coordinator
**Category:** 7XX Project Bootstrap
**Parent:** ln-700-project-bootstrap

Coordinates dependency upgrades by detecting package managers and delegating to appropriate L3 workers.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Detected stack from ln-700 |
| **Output** | All dependencies upgraded to latest compatible versions |
| **Workers** | ln-711 (npm), ln-712 (nuget), ln-713 (pip) |

---

## Workflow

See [diagram.html](diagram.html) for visual workflow.

**Phases:** Pre-flight → Detect → Security Audit → Delegate → Collect → Verify → Report

---

## Phase 0: Pre-flight Checks

Verify project state before starting upgrade.

| Check | Method | Block if |
|-------|--------|----------|
| Uncommitted changes | `git status --porcelain` | Non-empty output |
| Create backup branch | `git checkout -b upgrade-backup-{timestamp}` | Failure |
| Lock file exists | Check for lock file | Missing (warn only) |

> Skip upgrade if uncommitted changes exist. User must commit or stash first.

---

## Phase 1: Detect Package Managers

### Detection Rules

| Package Manager | Indicator Files | Worker |
|-----------------|-----------------|--------|
| npm | package.json + package-lock.json | ln-711 |
| yarn | package.json + yarn.lock | ln-711 |
| pnpm | package.json + pnpm-lock.yaml | ln-711 |
| nuget | *.csproj files | ln-712 |
| pip | requirements.txt | ln-713 |
| poetry | pyproject.toml + poetry.lock | ln-713 |
| pipenv | Pipfile + Pipfile.lock | ln-713 |

---

## Phase 2: Security Audit (Pre-flight)

### Security Checks

| Package Manager | Command | Block Upgrade |
|-----------------|---------|---------------|
| npm | `npm audit --audit-level=high` | Critical only |
| pip | `pip-audit --json` | Critical only |
| nuget | `dotnet list package --vulnerable` | Critical only |

### Release Age Check

| Option | Default | Description |
|--------|---------|-------------|
| minimumReleaseAge | 14 days | Skip packages released < 14 days ago |
| ignoreReleaseAge | false | Override for urgent security patches |

> Per Renovate best practices: waiting 14 days gives registries time to pull malicious packages.

---

## Phase 3: Delegate to Workers

### Delegation Context

Each worker receives standardized context:

| Field | Type | Description |
|-------|------|-------------|
| projectPath | string | Absolute path to project |
| packageManager | enum | npm, yarn, pnpm, nuget, pip, poetry, pipenv |
| options.upgradeType | enum | major, minor, patch |
| options.allowBreaking | bool | Allow breaking changes |
| options.testAfterUpgrade | bool | Run tests after upgrade |

### Worker Selection

| Package Manager | Worker | Notes |
|-----------------|--------|-------|
| npm, yarn, pnpm | ln-711-npm-upgrader | Handles all Node.js |
| nuget | ln-712-nuget-upgrader | Handles .NET projects |
| pip, poetry, pipenv | ln-713-pip-upgrader | Handles all Python |

---

## Phase 4: Collect Results

### Result Schema

| Field | Type | Description |
|-------|------|-------------|
| status | enum | success, partial, failed |
| upgrades[] | array | List of upgraded packages |
| upgrades[].package | string | Package name |
| upgrades[].from | string | Previous version |
| upgrades[].to | string | New version |
| upgrades[].breaking | bool | Is breaking change |
| warnings[] | array | Non-blocking warnings |
| errors[] | array | Blocking errors |

---

## Phase 5: Verify Build

### Build Commands by Stack

| Stack | Command |
|-------|---------|
| Node.js | `npm run build` or `yarn build` |
| .NET | `dotnet build --configuration Release` |
| Python | `pytest` or `python -m pytest` |

### On Build Failure

1. Identify failing package from error
2. Search Context7/Ref for migration guide
3. Apply known fixes
4. If still fails: rollback package, log warning

---

## Phase 6: Report Summary

### Report Schema

| Field | Type | Description |
|-------|------|-------------|
| totalPackages | int | Total packages analyzed |
| upgraded | int | Successfully upgraded |
| skipped | int | Already latest |
| failed | int | Rolled back |
| breakingChanges | int | Major version upgrades |
| buildVerified | bool | Build passed after upgrade |
| duration | string | Total time |

---

## Configuration

```yaml
Options:
  # Upgrade scope
  upgradeType: major          # major | minor | patch

  # Breaking changes
  allowBreaking: true
  autoMigrate: true           # Apply known migrations

  # Security
  auditLevel: high            # none | low | moderate | high | critical
  minimumReleaseAge: 14       # days, 0 to disable
  blockOnVulnerability: true

  # Scope
  skipDev: false              # Include devDependencies
  skipOptional: true          # Skip optional deps

  # Verification
  testAfterUpgrade: true
  buildAfterUpgrade: true

  # Rollback
  rollbackOnFailure: true
```

---

## Error Handling

### Recoverable Errors

| Error | Recovery |
|-------|----------|
| Peer dependency conflict | Try --legacy-peer-deps |
| Build failure | Rollback package, continue |
| Network timeout | Retry 3 times |

### Fatal Errors

| Error | Action |
|-------|--------|
| No package managers found | Skip this step |
| All builds fail | Report to parent, suggest manual review |

---

## References

- [breaking_changes_patterns.md](references/breaking_changes_patterns.md)
- [security_audit_guide.md](references/security_audit_guide.md)

---

**Version:** 1.1.0
**Last Updated:** 2026-01-10
