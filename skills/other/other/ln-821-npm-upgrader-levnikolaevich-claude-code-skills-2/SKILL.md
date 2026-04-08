---
name: ln-821-npm-upgrader
description: "Upgrades npm/yarn/pnpm dependencies with breaking change handling. Use when updating JavaScript/TypeScript dependencies."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-821-npm-upgrader

**Type:** L3 Worker
**Category:** 8XX Optimization

Upgrades Node.js dependencies using npm, yarn, or pnpm with automatic breaking change detection and migration.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project path, package manager type, upgrade policy |
| **Output** | Updated package manifest and a machine-readable dependency upgrade summary |
| **Supports** | npm, yarn (classic and berry), pnpm |

---

## Workflow

**Phases:** Pre-flight -> Analyze -> Security Audit -> Check Outdated -> Identify Breaking -> Apply Upgrades -> Apply Migrations -> Verify Build -> Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| `package.json` | Yes | Block upgrade |
| Lock file (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`) | No | Warn and regenerate before final verification |
| Package manager available | Yes | Block upgrade |
| Workspace baseline safe | Yes | In managed runs coordinator already prepared it; in standalone runs protect rollback locally |

### Runtime Coordination

Managed runs receive deterministic `runId` and exact `summaryArtifactPath` from `ln-820`.
Standalone runs remain supported; if runtime arguments are omitted, generate a standalone run-scoped artifact before returning.

---

## Phase 1: Analyze Dependencies

Read `package.json` and categorize dependencies for upgrade priority.

| Category | Examples | Priority |
|----------|----------|----------|
| peer | `typescript`, `@types/*` | 1 |
| framework | `react`, `vue`, `next` | 2 |
| build | `vite`, `webpack`, `esbuild` | 3 |
| ui | `@radix-ui/*`, `tailwindcss` | 4 |
| state | `@tanstack/react-query`, `zustand` | 5 |
| utils | `lodash`, `date-fns` | 6 |
| dev | `eslint`, `prettier`, test tooling | 7 |

---

## Phase 2: Security Audit

| Manager | Command |
|---------|---------|
| npm | `npm audit --audit-level=high` |
| yarn | `yarn audit --level high` |
| pnpm | `pnpm audit --audit-level high` |

Actions:

| Severity | Action |
|----------|--------|
| Critical | Block and report |
| High | Warn and continue |
| Moderate/Low | Log only |

---

## Phase 3: Check Outdated

| Manager | Command |
|---------|---------|
| npm | `npm outdated --json` |
| yarn | `yarn outdated --json` |
| pnpm | `pnpm outdated --json` |

---

## Phase 4: Identify Breaking Changes

**MANDATORY READ:** Load [breaking_changes_patterns.md](../ln-820-dependency-optimization-coordinator/references/breaking_changes_patterns.md) for full patterns.

Detection flow:
1. Compare current vs latest major versions.
2. Check shared breaking-change patterns.
3. Query Context7 or Ref for migration guides before changing code.

Common breaking examples:

| Package | Breaking Version | Key Changes |
|---------|------------------|-------------|
| react | 18 -> 19 | JSX transform, refs as props |
| vite | 5 -> 6 | ESM-only, newer Node baseline |
| eslint | 8 -> 9 | Flat config |
| tailwindcss | 3 -> 4 | CSS-first config |
| typescript | 5.4 -> 5.5+ | Stricter inference |

---

## Phase 5: Apply Upgrades

Upgrade order:
1. peer dependencies
2. framework packages
3. build tools
4. UI libraries
5. utilities
6. dev dependencies

| Manager | Command |
|---------|---------|
| npm | `npm install <package>@latest --save` |
| yarn | `yarn add <package>@latest` |
| pnpm | `pnpm add <package>@latest` |

Peer dependency conflicts:

| Situation | Solution |
|-----------|----------|
| ERESOLVE | `npm install --legacy-peer-deps` |
| Still fails | `npm install --force` only as last resort |

---

## MCP Tools for Migration Search

| Priority | Tool | When to Use |
|----------|------|-------------|
| 1 | `mcp__context7__query-docs` | First choice for library docs |
| 2 | `mcp__Ref__ref_search_documentation` | Official docs and GitHub |
| 3 | WebSearch | Latest info and community fixes |

Use MCP tools to fetch migration guides before applying non-trivial changes.

---

## Phase 6: Apply Migrations

1. Use MCP tools to find the current migration guide.
2. Apply automated code transforms only when the guide supports them.
3. Log manual follow-up steps for the final report.

Do not hardcode migrations without checking current documentation.

---

## Phase 7: Verify Build

| Check | Command |
|-------|---------|
| TypeScript | `npm run check` or `npx tsc --noEmit` |
| Build | `npm run build` |
| Tests | `npm test` if available |

On failure:
1. Identify the failing package.
2. Search Context7 or Ref for the fix.
3. If unresolved, rollback that package and continue with the remaining candidates.

---

## Phase 8: Report Results

| Field | Description |
|-------|-------------|
| `project` | Project path |
| `packageManager` | npm, yarn, or pnpm |
| `duration` | Total time |
| `upgrades.major[]` | Breaking changes applied |
| `upgrades.minor[]` | Feature updates |
| `upgrades.patch[]` | Bug fixes |
| `migrations[]` | Applied migrations |
| `skipped[]` | Already latest or policy-skipped |
| `verification` | Build/test/type-check verdict |
| `warnings[]` | Non-blocking issues |
| `artifact_path` | Durable worker report path, if written |

---

## Configuration

```yaml
Options:
  upgradeType: major          # major | minor | patch
  allowBreaking: true
  autoMigrate: true
  queryMigrationGuides: true
  auditLevel: high
  minimumReleaseAge: 14
  legacyPeerDeps: false
  force: false
  runBuild: true
  runTests: false
  runTypeCheck: true
  rollbackOnFailure: true
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| ERESOLVE | Peer dependency conflict | Retry with legacy peer dependency mode |
| ENOENT | Missing lock file | Regenerate dependencies first |
| Build fail | Breaking change | Apply migration guide or rollback offending package |
| Type errors | Version mismatch | Update types or framework peer packages |

Rollback:
Restore `package.json` and the lock file, then run a clean install to restore the previous state.

---

## References

- [breaking_changes_patterns.md](../ln-820-dependency-optimization-coordinator/references/breaking_changes_patterns.md)
- [npm_peer_resolution.md](references/npm_peer_resolution.md)

---

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`

Emit a `dependency-worker` summary envelope.

Managed mode:
- `ln-820` passes deterministic `runId` and exact `summaryArtifactPath`
- write the summary to the provided `summaryArtifactPath`

Standalone mode:
- omit `runId` and `summaryArtifactPath`
- write `.hex-skills/runtime-artifacts/runs/{run_id}/dependency-worker/ln-821--{identifier}.json`

## Definition of Done

- [ ] Package manifest analyzed and dependencies prioritized
- [ ] Security audit completed for the selected package manager
- [ ] Outdated packages identified
- [ ] Breaking changes checked via patterns plus current docs
- [ ] Upgrades applied with rollback on failure
- [ ] Build and relevant verification commands pass after upgrades
- [ ] `dependency-worker` summary artifact written to the managed or standalone path

---

**Version:** 1.1.0
**Last Updated:** 2026-01-10
