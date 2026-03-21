---
name: ln-820-dependency-optimization-coordinator
description: "Upgrades dependencies across all detected package managers. Use when updating npm, NuGet, or pip packages project-wide."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# ln-820-dependency-optimization-coordinator

**Type:** L2 Domain Coordinator
**Category:** 8XX Optimization
**Parent:** ln-700-project-bootstrap

Coordinates dependency upgrades by detecting package managers and delegating to appropriate L3 workers.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Detected stack from ln-700 |
| **Output** | All dependencies upgraded to latest compatible versions |
| **Workers** | ln-821 (npm), ln-822 (nuget), ln-823 (pip) |

---

## Workflow

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
| npm | package.json + package-lock.json | ln-821 |
| yarn | package.json + yarn.lock | ln-821 |
| pnpm | package.json + pnpm-lock.yaml | ln-821 |
| nuget | *.csproj files | ln-822 |
| pip | requirements.txt | ln-823 |
| poetry | pyproject.toml + poetry.lock | ln-823 |
| pipenv | Pipfile + Pipfile.lock | ln-823 |

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

> **CRITICAL:** All delegations use Agent tool with `subagent_type: "general-purpose"` and `isolation: "worktree"` — each worker creates its own branch per `shared/references/git_worktree_fallback.md`.

**Prompt template:**
```
Agent(description: "Upgrade deps via ln-82X",
     prompt: "Execute dependency upgrade worker.

Step 1: Invoke worker:
  Skill(skill: \"ln-82X-{worker}\")

CONTEXT:
{delegationContext}",
     subagent_type: "general-purpose",
     isolation: "worktree")
```

**Anti-Patterns:**
- ❌ Direct Skill tool invocation without Agent wrapper
- ❌ Any execution bypassing subagent context isolation

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
| npm, yarn, pnpm | ln-821-npm-upgrader | Handles all Node.js |
| nuget | ln-822-nuget-upgrader | Handles .NET projects |
| pip, poetry, pipenv | ln-823-pip-upgrader | Handles all Python |

---

## Phase 4: Collect Results

Each worker produces an isolated branch. Coordinator aggregates branch reports.

### Worker Branches

| Worker | Branch Pattern | Contents |
|--------|---------------|----------|
| ln-821 | `upgrade/ln-821-npm-{ts}` | npm/yarn/pnpm dependency upgrades |
| ln-822 | `upgrade/ln-822-nuget-{ts}` | NuGet dependency upgrades |
| ln-823 | `upgrade/ln-823-pip-{ts}` | pip/poetry/pipenv dependency upgrades |

### Result Schema

| Field | Type | Description |
|-------|------|-------------|
| worker | string | ln-821, ln-822, or ln-823 |
| status | enum | success, partial, failed |
| branch | string | Worker's result branch name |
| upgrades[] | array | List of upgraded packages |
| upgrades[].package | string | Package name |
| upgrades[].from | string | Previous version |
| upgrades[].to | string | New version |
| upgrades[].breaking | bool | Is breaking change |
| warnings[] | array | Non-blocking warnings |
| errors[] | array | Blocking errors |

---

## Phase 5: Aggregate Reports

Each worker verified independently in its branch (build, tests run by worker itself). Coordinator does NOT rerun verification or rollback packages.

### On Failure

1. Branch with failing build/tests logged as "failed" in report
2. User reviews failed branch independently

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

## Definition of Done

- [ ] Pre-flight checks passed (clean git state)
- [ ] All package managers detected from indicator files
- [ ] Security audit completed per manager (critical vulns block upgrade)
- [ ] Workers delegated with worktree isolation (`isolation: "worktree"`)
- [ ] Each worker produces isolated branch, pushed to remote
- [ ] Coordinator report aggregates per-worker results (branch, upgrades, status)

---

## Phase 7: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `optimization-coordinator`. Run after all phases complete. Output to chat using the `optimization-coordinator` format.

---

**Version:** 1.1.0
**Last Updated:** 2026-01-10
