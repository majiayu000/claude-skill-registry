---
name: ln-822-nuget-upgrader
description: "Upgrades .NET NuGet packages with breaking change handling. Use when updating .NET dependencies."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-822-nuget-upgrader

**Type:** L3 Worker
**Category:** 8XX Optimization

Upgrades .NET NuGet packages with automatic breaking change detection and migration.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Solution or project path plus upgrade policy |
| **Output** | Updated `.csproj` files and a machine-readable dependency upgrade summary |
| **Supports** | .NET 6, 7, 8, 9, 10 |

---

## Workflow

**Phases:** Pre-flight -> Find Projects -> Security Audit -> Check Outdated -> Identify Breaking -> Apply Upgrades -> Restore and Build -> Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| `.csproj` file(s) | Yes | Block upgrade |
| `.sln` file | No | Fall back to recursive project discovery |
| `dotnet` CLI | Yes | Block upgrade |
| Workspace baseline safe | Yes | In managed runs coordinator already prepared it; in standalone runs protect rollback locally |

### Runtime Coordination

Managed runs receive deterministic `runId` and exact `summaryArtifactPath` from `ln-820`.
Standalone runs remain supported; if runtime arguments are omitted, generate a standalone run-scoped artifact before returning.

---

## Phase 1: Find Projects

| Method | Command |
|--------|---------|
| Find `.csproj` files | `Get-ChildItem -Recurse -Filter *.csproj` |
| Read solution members | `dotnet sln list` |

---

## Phase 2: Security Audit

| Check | Command |
|-------|---------|
| Vulnerable packages | `dotnet list package --vulnerable` |
| Outdated packages | `dotnet list package --outdated` |

Actions:

| Severity | Action |
|----------|--------|
| Critical | Block and report |
| High | Warn and continue |
| Moderate/Low | Log only |

---

## Phase 3: Check Outdated

| Step | Command |
|------|---------|
| Install helper | `dotnet tool install --global dotnet-outdated-tool` |
| Detect outdated packages | `dotnet outdated --output json` |

---

## Phase 4: Identify Breaking Changes

Detection flow:
1. Compare current vs latest major versions.
2. Check [breaking_changes_patterns.md](../ln-820-dependency-optimization-coordinator/references/breaking_changes_patterns.md).
3. Use MCP tools for migration guides before changing code.

Common examples:

| Package | Breaking Version | Key Changes |
|---------|------------------|-------------|
| Microsoft.EntityFrameworkCore | 8 -> 9 | Query and migration changes |
| Serilog.AspNetCore | 7 -> 8 | Configuration updates |
| Swashbuckle.AspNetCore | 6 -> 7 | Minimal API integration changes |

---

## MCP Tools for Migration Search

| Priority | Tool | When to Use |
|----------|------|-------------|
| 1 | `mcp__context7__query-docs` | First choice for library docs |
| 2 | `mcp__Ref__ref_search_documentation` | Official Microsoft docs |
| 3 | WebSearch | Latest info and community fixes |

Use the tool chain to confirm migrations before applying them.

---

## Phase 5: Apply Upgrades

Priority order:
1. SDK or runtime packages
2. framework packages
3. EF Core
4. logging packages
5. everything else

| Action | Command |
|--------|---------|
| Update one package | `dotnet add package <name> --version <ver>` |
| Update many packages | `dotnet outdated --upgrade` |

---

## Phase 6: Restore and Build

| Step | Command |
|------|---------|
| Restore | `dotnet restore` |
| Build | `dotnet build --configuration Release` |
| Test | `dotnet test` |

On failure:
1. Identify the failing package.
2. Search Context7 or Ref for the migration guide.
3. If unresolved, rollback that package and continue.

---

## Phase 7: Report Results

| Field | Description |
|-------|-------------|
| `solution` | Solution path |
| `projects[]` | Updated projects |
| `duration` | Total time |
| `upgrades[]` | Applied upgrades |
| `verification` | Restore/build/test verdict |
| `warnings[]` | Non-blocking issues |
| `artifact_path` | Durable worker report path, if written |

---

## Configuration

```yaml
Options:
  upgradeType: major          # major | minor | patch
  auditLevel: high
  minimumReleaseAge: 14
  includePrerelease: false
  targetFramework: net10.0
  runTests: true
  runBuild: true
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| CS0246 | Missing type | Search for replacement API |
| NU1605 | Downgrade detected | Check package constraints |
| Build fail | Breaking change | Apply migration guide or rollback offending package |

---

## References

- [breaking_changes_patterns.md](../ln-820-dependency-optimization-coordinator/references/breaking_changes_patterns.md)
- [dotnet_version_matrix.md](references/dotnet_version_matrix.md)

---

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`

Emit a `dependency-worker` summary envelope.

Managed mode:
- `ln-820` passes deterministic `runId` and exact `summaryArtifactPath`
- write the summary to the provided `summaryArtifactPath`

Standalone mode:
- omit `runId` and `summaryArtifactPath`
- write `.hex-skills/runtime-artifacts/runs/{run_id}/dependency-worker/ln-822--{identifier}.json`

## Definition of Done

- [ ] All target `.csproj` files discovered
- [ ] Security audit completed for NuGet dependencies
- [ ] Outdated packages identified
- [ ] Breaking changes checked via patterns plus current docs
- [ ] Upgrades applied in a safe order with rollback on failure
- [ ] `dotnet restore`, `dotnet build`, and required tests succeed
- [ ] `dependency-worker` summary artifact written to the managed or standalone path

---

**Version:** 1.1.0
**Last Updated:** 2026-01-10
