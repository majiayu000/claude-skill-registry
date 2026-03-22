---
name: bun-dev
description: "Definitive, rule-first Bun development/build/runtime guidance + automation. Use when adopting Bun, migrating a repo from Node.js, auditing/fixing Bun package management (bun.lockb, bun install), optimizing scripts/monorepos (bun run --parallel/--sequential, --workspaces/--filter), configuring Bun + TypeScript, using bun test/build, tuning performance, or deploying Bun workloads/Vercel Functions with the Bun runtime (bunVersion, limitations, Next.js ISR scripts)."
---

# Bun Dev

Rule-first Bun guidance plus a shared audit/remediation engine.

Use `bun-dev` for operating-model decisions, rule lookup, release sync, and
platform routing. Use `bun-audit` when the task is specifically about scanning a
repo, planning safe fixes, applying deterministic remediations, or validating
changes against Bun policy.

Start with `rules/_index.md` for discovery, then route by the Priority Table below.

## Navigation (How To Use This Skill)

1. If changing package manager/runtime, open P1 rules first:
   `pm-*`, `runtime-*`, `vercel-*`.
2. If working in a monorepo, open:
   `scripts-bun-run-parallel-sequential`, `scripts-bun-filter-and-workspaces`.
3. If deploying to Vercel, open:
   `vercel-bun-runtime-enable`, `vercel-bun-runtime-limitations`.
4. For repo-wide enforcement, use the shared CLI:
   `bun-platform audit`, `plan-fixes`, `apply-safe-fixes`, `validate`.
5. For “what changed recently?” (Bun v1.3.10), refresh references and open:
   `references/ref-bun-release-notes-bun-v1.3.10.md`.

## Quick Start (Audit -> Fix -> Verify)

Audit (report-only):

```bash
bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts audit --root . --format text
```

Plan safe fixes:

```bash
bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts plan-fixes --root .
```

Apply safe fixes:

```bash
bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts apply-safe-fixes --root .
```

Validate after remediation:

```bash
bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts validate --root . --fail-on warn
```

## Priority Table (Route To The Right Rules)

| Priority | Category | Impact | Prefix |
| --- | --- | --- | --- |
| 1 | Package manager + lockfiles | CRITICAL | `pm-` |
| 1 | Runtime selection + “one runtime where possible” | CRITICAL | `runtime-` |
| 1 | Vercel Bun runtime | CRITICAL | `vercel-` |
| 2 | Scripts + monorepo orchestration | HIGH | `scripts-` |
| 2 | TypeScript + tooling | HIGH | `tsconfig-` |
| 3 | Testing | MEDIUM | `test-` |
| 3 | Bundling + build | MEDIUM | `build-` |
| 4 | Performance | MEDIUM | `perf-` |
| 5 | Migration + troubleshooting | LOW/MED | `migrate-`, `troubleshooting-` |

## Quick Reference (Start Here)

### 1) Package Manager + Lockfiles (CRITICAL)

- `pm-bun-add-remove-update`
- `pm-no-mixed-lockfiles`
- `pm-commit-bun-lockb`
- `pm-bun-install-ci-frozen-lockfile`
- `pm-package-manager-field`
- `pm-bunx-vs-npx`

### 2) Runtime Selection (CRITICAL)

- `runtime-bun-vs-node-choose`
- `runtime-bun-run-bun-flag`
- `runtime-ts-direct-execution`
- `runtime-watch-and-hot-reload`
- `runtime-env-files`

### 3) Vercel Bun Runtime (CRITICAL)

- `vercel-bun-install-detection`
- `vercel-bun-runtime-enable`
- `vercel-bun-runtime-limitations`
- `vercel-nextjs-bun-runtime-scripts`
- `vercel-bun-function-fetch-handler`

### 4) Scripts + Monorepos (HIGH)

- `scripts-bun-run-parallel-sequential`
- `scripts-bun-filter-and-workspaces`
- `scripts-no-npm-in-bun-repos`

### 5) TypeScript (HIGH)

- `tsconfig-bun-recommended`
- `tsconfig-bun-types`
- `tsconfig-module-resolution-bundler`

### 6) Testing + Build (MEDIUM)

- `test-bun-test-runner`
- `test-bun-retry`
- `test-mocking-and-spying`
- `build-bun-build-bundler`
- `build-compile-executables`
- `build-bun-compile-browser`

### 7) Performance (MEDIUM)

- `perf-prefer-bun-native-apis`
- `perf-avoid-node-fs-promises-hot-paths`

### 8) Migration + Troubleshooting (LOW/MED)

- `migrate-node-to-bun-checklist`
- `troubleshooting-esm-cjs-and-exports`
- `troubleshooting-types-bun`

## References (Vendor Docs Snapshots)

Start with `references/index.md`.

## Shared Platform Commands

- `audit`: report Bun findings in `text`, `md`, or `json`
- `list-rules`: print all rule ids
- `explain <rule-id>`: print the matching rule file
- `plan-fixes`: print deterministic safe fix candidates
- `apply-safe-fixes`: apply safe file rewrites only
- `validate`: rerun the audit and fail on a severity threshold
- `benchmark`: emit audit/fix-planning timings
- `release-sync`: refresh Bun/Vercel references and rebuild rule indexes

Platform state:

- `.bun-platform/cache.sqlite`: shared scan cache
- `.bun-platform/rollbacks/`: safe-fix rollback artifacts
- `references/release-sync-report.json`: local generated release intelligence summary (ignored; not committed)

Config file:

- `bun-platform.config.json`
  - `disabledRules`
  - `severityOverrides`
  - `adapters`
  - `includePaths`
  - `excludeDirs`
  - `baseline`
  - `maxFiles`
  - `maxBytes`
  - `validationCommands`
  - `manageGitignore`
- Example template: `assets/templates/bun-platform.config.example.json`

## Reference Map

| Topic | Reference | Start with rules |
| --- | --- | --- |
| Bun v1.3.10 release notes | `references/ref-bun-release-notes-bun-v1.3.10.md` | `scripts-bun-run-parallel-sequential`, `build-bun-compile-browser`, `test-bun-retry`, `test-bun-test-runner` |
| Vercel Bun runtime | `references/ref-vercel-bun-runtime.md` | `vercel-bun-runtime-enable`, `vercel-bun-runtime-limitations` |

Refresh reference snapshots:

```bash
bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts release-sync
```

## Automation

Shared CLI:

```bash
bun ~/.agents/skills/bun-dev/scripts/bun-platform.ts audit --root .
```

Compatibility wrapper:

```bash
bun ~/.agents/skills/bun-dev/scripts/bun-audit.ts audit --root .
```

Skill integrity check (rule ids, indexes, flat references):

```bash
bun ~/.agents/skills/bun-dev/scripts/check-skill-integrity.ts
```
