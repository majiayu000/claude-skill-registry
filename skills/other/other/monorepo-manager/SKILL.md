---
name: monorepo-manager
description: >-
  Manage dependencies, workspace configurations, and cross-package relationships
  in monorepos using npm workspaces, pnpm, Yarn, Turborepo, or Nx. Use when
  syncing dependency versions across packages, resolving version conflicts,
  analyzing the dependency graph, or setting up build orchestration. Trigger
  words: monorepo, workspace, dependency sync, version conflict, turborepo,
  nx, pnpm workspace, cross-package, internal dependency.
license: Apache-2.0
compatibility: "Node.js monorepos (npm/pnpm/yarn workspaces, Turborepo, Nx)"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["monorepo", "dependencies", "workspaces", "turborepo"]
---

# Monorepo Manager

## Overview

Analyze, maintain, and optimize monorepo dependency graphs. Detect version mismatches across packages, sync shared dependencies, configure build pipelines, and resolve workspace conflicts that slow teams down.

## Instructions

### 1. Detect monorepo structure

Identify the monorepo tool in use:
- Check for `pnpm-workspace.yaml` → pnpm workspaces
- Check `package.json` for `"workspaces"` → npm/yarn workspaces
- Check for `turbo.json` → Turborepo
- Check for `nx.json` → Nx
- Check for `lerna.json` → Lerna (legacy)

Map all packages:
```
Monorepo: pnpm workspaces + Turborepo
Packages (14):
  apps/
    web          → Next.js 14 app
    api          → Express server
    admin        → React admin panel
  packages/
    ui           → Shared component library
    config       → ESLint/TS configs
    database     → Prisma schema + client
    utils        → Shared utilities
    types        → TypeScript type definitions
```

### 2. Audit dependency versions

Scan all package.json files and flag mismatches:
```
## Dependency Version Mismatches

| Package    | apps/web | apps/api | apps/admin | packages/ui |
|------------|----------|----------|------------|-------------|
| react      | 18.3.1   | —        | 18.2.0 ⚠️  | 18.3.1      |
| typescript | 5.4.2    | 5.3.3 ⚠️ | 5.4.2      | 5.4.2       |
| zod        | 3.22.4   | 3.21.1 ⚠️| —          | —           |

3 mismatches found across 14 packages.
```

### 3. Resolve conflicts

For each mismatch, recommend and apply fixes:
- Identify which version to standardize on (usually latest)
- Check for breaking changes between versions
- Update all package.json files
- Run the appropriate install command
- Verify build still passes

### 4. Analyze internal dependency graph

Map which packages depend on which:
```
packages/types ← packages/utils ← packages/ui ← apps/web
                                                ← apps/admin
               ← packages/database ← apps/api
```

Flag circular dependencies and suggest extraction points.

### 5. Optimize build configuration

For Turborepo/Nx, ensure:
- Build tasks declare correct `dependsOn` relationships
- Caching is configured for all cacheable tasks
- Only affected packages rebuild on changes
- CI pipeline uses remote caching

## Examples

### Example 1: Sync React versions

**Input:** "Our monorepo has 6 apps using different React versions. Sync them all."

**Output:**
```
Found React version mismatches:

| Package       | Current | Target |
|---------------|---------|--------|
| apps/web      | 18.3.1  | 18.3.1 ✅ |
| apps/admin    | 18.2.0  | 18.3.1 ⬆️ |
| apps/mobile   | 18.2.0  | 18.3.1 ⬆️ |
| packages/ui   | 18.3.1  | 18.3.1 ✅ |

Updated 2 package.json files. Run `pnpm install` to apply.

Breaking changes in 18.2→18.3: None (patch release).
Recommend running `pnpm turbo build` to verify all packages compile.
```

### Example 2: Add shared dependency

**Input:** "Add date-fns to packages/utils and make sure all apps use the same version"

**Output:**
```
Current date-fns usage:
- apps/web: date-fns@3.3.1
- apps/api: date-fns@2.30.0 (major version behind!)
- apps/admin: not installed

Plan:
1. Add date-fns@3.6.0 to packages/utils
2. Upgrade apps/web from 3.3.1 → 3.6.0
3. Upgrade apps/api from 2.30.0 → 3.6.0 (breaking changes — see migration notes)
4. Remove direct date-fns deps from apps, import via packages/utils

⚠️ date-fns v2→v3 breaking changes:
- Named exports only (no default import)
- `format` tokens changed: `DD` → `dd`, `YY` → `yy`

Updated 4 package.json files. Review the v3 migration in apps/api.
```

## Guidelines

- Always map the full dependency graph before making changes
- Check for breaking changes before bumping major versions
- Prefer hoisting shared deps to the root when possible
- Use `catalog:` protocol in pnpm or `resolutions` in yarn for version pinning
- After any dependency change, verify builds across all affected packages
- Circular dependencies between packages are a code smell — suggest extraction
- For large monorepos (50+ packages), prioritize the most impactful mismatches first
- Internal packages should use `workspace:*` protocol, not pinned versions
