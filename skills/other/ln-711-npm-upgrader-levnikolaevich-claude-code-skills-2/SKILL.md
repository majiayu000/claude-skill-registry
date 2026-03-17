---
name: ln-711-npm-upgrader
description: Upgrades npm/yarn/pnpm dependencies with breaking change handling
---

# ln-711-npm-upgrader

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-710-dependency-upgrader

Upgrades Node.js dependencies using npm, yarn, or pnpm with automatic breaking change detection and migration.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project path, package manager type |
| **Output** | Updated package.json, lock file, migration report |
| **Supports** | npm, yarn (classic & berry), pnpm |

---

## Workflow

See [diagram.html](diagram.html) for visual workflow.

**Phases:** Pre-flight → Analyze → Security Audit → Check Outdated → Identify Breaking → Apply Upgrades → Apply Migrations → Verify Build → Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| Lock file (package-lock.json, yarn.lock, pnpm-lock.yaml) | Yes | Warn and run `npm install` first |
| package.json | Yes | Block upgrade |

> Workers assume coordinator (ln-710) already verified git state and created backup.

---

## Phase 1: Analyze Dependencies

Read package.json and categorize dependencies for upgrade priority.

### Dependency Categories

| Category | Examples | Priority |
|----------|----------|----------|
| framework | react, vue, angular | 2 (after peer deps) |
| build | vite, webpack, esbuild | 3 |
| ui | @radix-ui/*, tailwindcss | 4 |
| state | @tanstack/react-query, zustand | 5 |
| utils | lodash, date-fns | 6 |
| dev | eslint, prettier, typescript | 7 |
| peer | @types/*, typescript | 1 (first) |

---

## Phase 2: Security Audit

### Commands

| Manager | Command |
|---------|---------|
| npm | `npm audit --audit-level=high` |
| yarn | `yarn audit --level high` |
| pnpm | `pnpm audit --audit-level high` |

### Actions

| Severity | Action |
|----------|--------|
| Critical | Block upgrade, report |
| High | Warn, continue |
| Moderate/Low | Log only |

---

## Phase 3: Check Outdated

### Commands

| Manager | Command |
|---------|---------|
| npm | `npm outdated --json` |
| yarn | `yarn outdated --json` |
| pnpm | `pnpm outdated --json` |

---

## Phase 4: Identify Breaking Changes

### Detection

1. Compare current vs latest major versions
2. Check [breaking_changes_patterns.md](../ln-710-dependency-upgrader/references/breaking_changes_patterns.md)
3. Query Context7/Ref for migration guides

### Common Breaking Changes

**MANDATORY READ:** Load [breaking_changes_patterns.md](../ln-710-dependency-upgrader/references/breaking_changes_patterns.md) for full patterns.

| Package | Breaking Version | Key Changes |
|---------|------------------|-------------|
| react | 18 → 19 | JSX Transform, ref as prop |
| vite | 5 → 6 | ESM only, Node 18+ |
| eslint | 8 → 9 | Flat config required |
| tailwindcss | 3 → 4 | CSS-based config |
| typescript | 5.4 → 5.5+ | Stricter inference |

---

## Phase 5: Apply Upgrades

### Upgrade Order

1. **Peer dependencies** (TypeScript, @types/*)
2. **Framework packages** (React, Vue core)
3. **Build tools** (Vite, webpack)
4. **UI libraries** (after framework)
5. **Utilities** (lodash, date-fns)
6. **Dev dependencies** (testing, linting)

### Commands

| Manager | Command |
|---------|---------|
| npm | `npm install <package>@latest --save` |
| yarn | `yarn add <package>@latest` |
| pnpm | `pnpm add <package>@latest` |

### Peer Dependency Conflicts

| Situation | Solution |
|-----------|----------|
| ERESOLVE error | `npm install --legacy-peer-deps` |
| Still fails | `npm install --force` (last resort) |

---

## MCP Tools for Migration Search

### Priority Order (Fallback Strategy)

| Priority | Tool | When to Use |
|----------|------|-------------|
| 1 | mcp__context7__query-docs | First choice for library docs |
| 2 | mcp__Ref__ref_search_documentation | Official docs and GitHub |
| 3 | WebSearch | Latest info, community solutions |

### Context7 Usage

| Step | Tool | Parameters |
|------|------|------------|
| 1. Find library | mcp__context7__resolve-library-id | libraryName: "react", query: "migration guide" |
| 2. Query docs | mcp__context7__query-docs | libraryId: "/facebook/react", query: "react 18 to 19 migration" |

### MCP Ref Usage

| Action | Tool | Query Example |
|--------|------|---------------|
| Search | mcp__Ref__ref_search_documentation | "react 19 migration guide breaking changes" |
| Read | mcp__Ref__ref_read_url | URL from search results |

### WebSearch Fallback

Use when Context7/Ref return no results:
- `"<package> <version> breaking changes migration 2025"`
- `"<package> <error message> fix stackoverflow"`

---

## Phase 6: Apply Migrations

### Process

1. Use MCP tools (see section above) to find migration guide
2. Apply automated code transforms via Edit tool
3. Log manual migration steps for user

> Do NOT apply hardcoded migrations. Always fetch current guides via MCP tools.

---

## Phase 7: Verify Build

### Commands

| Check | Command |
|-------|---------|
| TypeScript | `npm run check` or `npx tsc --noEmit` |
| Build | `npm run build` |
| Tests | `npm test` (if available) |

### On Failure

1. Identify failing package from error
2. Search Context7/Ref for fix
3. If unresolved: rollback package, continue with others

---

## Phase 8: Report Results

### Report Schema

| Field | Description |
|-------|-------------|
| project | Project path |
| packageManager | npm, yarn, or pnpm |
| duration | Total time |
| upgrades.major[] | Breaking changes applied |
| upgrades.minor[] | Feature updates |
| upgrades.patch[] | Bug fixes |
| migrations[] | Applied migrations |
| skipped[] | Already latest |
| buildVerification | PASSED or FAILED |
| warnings[] | Non-blocking issues |

---

## Configuration

```yaml
Options:
  # Upgrade scope
  upgradeType: major          # major | minor | patch

  # Breaking changes
  allowBreaking: true
  autoMigrate: true
  queryMigrationGuides: true  # Use Context7/Ref

  # Security
  auditLevel: high            # none | low | moderate | high | critical
  minimumReleaseAge: 14       # days

  # Peer dependencies
  legacyPeerDeps: false
  force: false

  # Verification
  runBuild: true
  runTests: false
  runTypeCheck: true

  # Rollback
  createBackup: true
  rollbackOnFailure: true
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| ERESOLVE | Peer dep conflict | --legacy-peer-deps |
| ENOENT | Missing lock file | npm install first |
| Build fail | Breaking change | Apply migration via Context7 |
| Type errors | Version mismatch | Update @types/* |

### Rollback

Restore package.json and lock file from git, then run clean install to restore previous state.

---

## References

- [breaking_changes_patterns.md](../ln-710-dependency-upgrader/references/breaking_changes_patterns.md)
- [npm_peer_resolution.md](references/npm_peer_resolution.md)

---

**Version:** 1.1.0
**Last Updated:** 2026-01-10
