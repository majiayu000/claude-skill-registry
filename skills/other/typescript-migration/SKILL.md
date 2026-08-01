---
name: typescript-migration
description: "TypeScript version migration guide (5.x to 6 to 7, tsgo native port). Use for TS 6 tsconfig breaking changes, TS 7 Go rewrite rollout, or TS5xxx deprecation codes."
license: MIT
---

# TypeScript Migration

Authoritative migration guide for TypeScript 5.x → 6 → 7 (native Go port). Sourced from Microsoft's official announcements.

## Status

- **Skill Status**: Production Ready
- **Last Updated**: 2026-07-09
- **TS 6.0 Released**: 2026-03-17 (Final) — last JavaScript-based release
- **TS 7.0 Released**: 2026-07-08 — native Go port ("Corsa"), stable
- **Authoritative Sources**:
  - TS 7.0 release: https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/
  - TS 6.0 beta: https://devblogs.microsoft.com/typescript/announcing-typescript-6-0-beta/
  - TS 6 → 7 diff tracker: https://github.com/microsoft/typescript-go/blob/main/CHANGES.md
  - ts5to6 tool: https://github.com/andrewbranch/ts5to6

## The Golden Rule

> NEVER skip TypeScript 6. The only supported paths are **5.x → 6 → 7**.
>
> Skipping TS 6 produces a wall of hard errors because TS 7 removes everything TS 6 deprecated. Use `"ignoreDeprecations": "6.0"` only as a temporary pause inside TS 6; it does NOT work in TS 7.

## Quick Triage (1 Minute)

1. **Detect current version** — run `scripts/detect-ts-version.sh` (reads `package.json`).
2. **Classify the path**:
   - `5.x` → start with `references/migration-playbooks.md` § "5.x → 6".
   - `6.x` → may go directly to TS 7 (see `references/ts7-go-rewrite.md`).
   - `5.x` wanting TS 7 → must go 5 → 6 → 7 (no shortcuts).
   - Intra-version strict-flag rollout (no version change) → see `references/ts-migrating-tool-guide.md` for the optional `ts-migrating` tool.
3. **Audit before changing anything** — run `scripts/audit-ts7-breakers.sh` to detect tooling that breaks under TS 7 (typescript-eslint, ts-morph, ts-node, Vue/Svelte/Astro/MDX/Angular templates, ts-patch, ttypescript, typia, `baseUrl`, `node10`, `ES5` target).

## Project-Type Decision Matrix

| Project type | Recommendation | Why |
|---|---|---|
| Greenfield, no API-dependent tooling | Adopt TS 7 directly | Full speedup, no blockers |
| Existing TS project, no special tooling | 5 → 6 → 7 sequentially | TS 6 surfaces every deprecation as a warning first |
| Uses typescript-eslint / ts-morph / API consumers | 5 → 6 → 7 via `@typescript/typescript6` side-by-side | TS 7 has no programmatic API until 7.1 |
| Vue / Svelte / Astro / MDX (Volar-based) | **Stay on TS 6** | Volar needs the programmatic API; not yet supported |
| Angular with template type-checking | TS 7 for CLI + TS 6 for editor | Microsoft's official split workaround |
| ts-patch / ttypescript / typia / custom AST transformers | **Stay on TS 6** until migrated to Oxc/SWC | Transformer API gone in TS 7 |

## TS 6 — Top Breaking Changes (Quick View)

| Change | Old default | TS 6 default | Fix |
|---|---|---|---|
| `strict` | false | **true** | Set explicitly or fix errors |
| `module` | CommonJS | **esnext** | Set `commonjs` if needed |
| `target` | ES3 | **es2025** (floating) | Set explicitly |
| `moduleResolution` | node10 | **bundler** | Set `nodenext` for Node targets |
| `rootDir` | inferred | **`.` (tsconfig dir)** | Set `"rootDir": "./src"` |
| `types` | all `@types` | **`[]`** | Set `"types": ["node"]` |
| `esModuleInterop` | false | **true** | Remove `:false`; fix `import * as` → `import` |
| `noUncheckedSideEffectImports` | false | **true** | Fix typos or set false for bundler CSS |
| `libReplacement` | true | **false** | — |
| `allowSyntheticDefaultImports` | varies | **true** | — |

Deprecated in 6, **HARD ERRORS in 7**: `target: es5`; `downlevelIteration`; `moduleResolution: node | node10 | classic`; `module: amd | umd | systemjs | none`; `baseUrl`; `esModuleInterop: false`; `allowSyntheticDefaultImports: false`; `alwaysStrict: false`; `outFile`; `module Foo {}` keyword; `assert { }` on imports; `/// <reference no-default-lib="true"/>`; `tsc <file>` + tsconfig present (use `--ignoreConfig`).

For full detail per change including PR citations, examples, and the official `ts5to6` codemod usage, load `references/ts6-breaking-changes.md`.

## TS 7 — What Changed (Quick View)

- Native Go port; the standard `typescript` npm package IS TS 7 (`npm install -D typescript`).
- All TS 6 deprecations become hard errors (see table above).
- **No programmatic Compiler API** in 7.0 — TS 7.1 will ship a new one. Affects ts-morph, ts-node, ts-jest, ts-loader, ts-patch, ttypescript, typia, typescript-eslint (use the side-by-side pattern below).
- `preserveConstEnums` removed — always emits const enums.
- `stableTypeOrdering` now `true` by default; cannot be turned off.
- NEW flags: `--checkers N` (default 4), `--builders N`, `--singleThreaded`.
- NEW breaking change: template literal types preserve Unicode code points (not UTF-16 code units).
- NEW: JS file handling reworked (Closure-style `@enum`, `@class`, `?`, postfix `!` no longer special).
- Performance (official, real OSS codebases): 7.7x–11.9x faster builds (up to 16.7x with `--checkers 8`); 6–26% lower memory.

Full install options, compatibility matrix, performance tables, and known issues in `references/ts7-go-rewrite.md`.

## The Official Side-by-Side Pattern (TS 7 + TS 6 API)

Microsoft's recommended path for projects whose tooling depends on the TS Compiler API. Declare an alias in `package.json`:

```json
{
  "devDependencies": {
    "@typescript/native": "npm:typescript@^7.0.2",
    "typescript": "npm:@typescript/typescript6@^6.0.2"
  }
}
```

- `npx tsc` runs TS 7 (via the `@typescript/native` alias).
- Tools importing `typescript` (typescript-eslint, ts-morph) transparently get TS 6's API via `@typescript/typescript6`.
- A `tsc6` executable is also available if a TS 6 invocation is needed directly.
- Remove this workaround once TS 7.1 ships the new API.

## The 4-Step Standard Workflow

1. **Detect** — `scripts/detect-ts-version.sh` reports the installed version.
2. **Audit** — `scripts/audit-ts7-breakers.sh` detects breakers BEFORE any upgrade. `scripts/ts6-deprecation-scan.sh` extracts TS5xxx codes from `tsc` output.
3. **Migrate** — follow `references/migration-playbooks.md` for the appropriate path. Run `ts5to6 --fixBaseUrl` and `ts5to6 --fixRootDir` if the user explicitly approves (these are official Microsoft-endorsed codemods). All other changes are manual.
4. **Verify** — `scripts/compare-tsc7-tsc6.sh` diffs diagnostic codes between TS 7 `tsc` and TS 6 `tsc6`. Match on TSxxxx codes, NOT message text (wording differs between compilers). Delete stale `.tsbuildinfo` files before the first TS 7 run (incompatible between the JS and Go compilers).

## Critical Rules

### Always

- ✅ Migrate through TS 6 — never skip it.
- ✅ Match on diagnostic codes (TSxxxx), not message wording.
- ✅ Delete stale `.tsbuildinfo` before the first TS 7 run.
- ✅ Cite Microsoft's official blog posts as authoritative; treat third-party tutorials as secondary.
- ✅ Run `audit-ts7-breakers.sh` BEFORE any upgrade.

### Never

- ❌ Never install `@typescript/native-preview` for stable use — it's the legacy nightly package; stable is the standard `typescript` package.
- ❌ Never assert the unverified third-party claims listed in `references/unverified-claims.md` (e.g. "moduleResolution default is node16", "`--ts6-migration` flag exists", "ES5 target is removed in 6", "`--keyofStringsOnly` was removed").
- ❌ Never recommend `ts-migrating` (the tool) for TS version migration — it only helps tighten compilerOptions within a version.
- ❌ Never assume VS Code needs a setting key to enable TS 7 — install the official extension; it auto-enables.
- ❌ Never auto-edit user source via custom scripts — only detection/audit scripts and officially-blessed codemods (`ts5to6`).

## The `ts-migrating` Tool — Conditional Offer

Offer this tool ONLY when the user wants to enable a stricter `compilerOption` (e.g. `noUncheckedIndexedAccess`, `strict`, `erasableSyntaxOnly`) on an existing large codebase — NOT for version migration.

Gate conditions (all must hold):

- Existing, non-greenfield TypeScript project.
- The goal is enabling a `compilerOption` incrementally.
- This is not a tsgo / TS-7 migration.

Warnings:

- The `annotate` subcommand rewrites source — run on a clean git tree and review the diff.
- The IDE plugin has ZERO effect on `tsc`; wire `ts-migrating check` into CI for it to matter.
- `// @ts-migrating` markers are tech debt needing a cleanup sweep.
- This is NOT Airbnb's `ts-migrate` (different tool — JS → TS conversion).

Full install, commands, and gate logic in `references/ts-migrating-tool-guide.md`.

## Common Error Codes

| Code | Meaning | Action |
|---|---|---|
| TS5011 | rootDir mismatch | Set `"rootDir": "./src"` |
| TS5101 | Option deprecated, stops in TS {ver} | Add `"ignoreDeprecations": "6.0"` (TS 6 only) or fix |
| TS5102 | Option removed | Remove from tsconfig |
| TS5107 | Option=value deprecated | Same as TS5101 |
| TS5108 | Option=value removed | Remove |
| TS5111 | Migration info (baseUrl, node10) | See `references/ts6-breaking-changes.md` |
| TS5112 | tsc file-args + tsconfig present | Use `--ignoreConfig` |

## When to Load References

Load these reference files when the user needs detail beyond the quick-reference above:

| Load This File | When |
|---|---|
| `references/ts6-breaking-changes.md` | Migrating to TS 6; need full PR-cited detail on each default change, deprecation, or syntax change |
| `references/ts7-go-rewrite.md` | Adopting TS 7; need install detail, compat matrix, performance tables, known gaps |
| `references/ecosystem-compatibility.md` | Checking whether a specific tool (typescript-eslint, ts-morph, ts-node, vite, webpack, vitest, etc.) works under TS 7 |
| `references/migration-playbooks.md` | Need ordered checklists for 5→6, 6→7, or 5→7-via-6 |
| `references/ts-migrating-tool-guide.md` | User wants to enable a stricter compilerOption incrementally on an existing large codebase |
| `references/unverified-claims.md` | Encountering a claim that contradicts official sources; verify before asserting |

## Dependencies

- **Required for migration**: `typescript` (target version), `tsconfig.json` in the project root.
- **Optional helpers**:
  - `@andrewbranch/ts5to6` — official codemod for `baseUrl` / `rootDir`.
  - `@typescript/typescript6` — side-by-side API compat for TS 7.
  - `ts-migrating` — incremental strict-flag rollout (see guide).

## Package Versions (Verified 2026-07-09)

```json
{
  "devDependencies": {
    "typescript": "^7.0.2",
    "@typescript/typescript6": "^6.0.2"
  },
  "optionalHelpers": {
    "@andrewbranch/ts5to6": "latest",
    "ts-migrating": "latest"
  }
}
```

All facts in this skill are cited to Microsoft's official TypeScript blog (devblogs.microsoft.com/typescript). Third-party tutorial claims that conflict with official sources are catalogued in `references/unverified-claims.md` and treated as suspect.
