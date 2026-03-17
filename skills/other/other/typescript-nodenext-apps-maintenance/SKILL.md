---
name: nodenext-apps
description: "Audit and repair TypeScript relative import specifiers for NodeNext/Node16 projects by enforcing runtime-valid emitted extensions (`.js`, `.mjs`, `.cjs`). Use when `module` or `moduleResolution` is `nodenext|node16`, when Node ESM/CJS runs fail with extension-related import errors, or when standardizing import specifiers across `src` and test files."
---

# NodeNext Apps Maintenance

## Scope and outcome

Use this skill to detect NodeNext/Node16 TypeScript projects, audit relative imports, and apply safe, deterministic fixes so compiled runtime imports are valid in Node.

Success criteria:
- Project is confirmed to use NodeNext or Node16 semantics.
- Relative imports in compiled TypeScript source use emitted-file extensions.
- Package/bare imports remain unchanged.
- Audit exits cleanly after fixes.

## Detection gate (required)

1. Inspect `tsconfig.json` and any build/test tsconfig files (for example `tsconfig.build.json`, `tsconfig.spec.json`).
2. Continue only if one of these is true:
- `compilerOptions.module` is `nodenext` or `node16`
- `compilerOptions.moduleResolution` is `nodenext` or `node16`
3. If neither condition is met, stop and report: this skill is not applicable.

## Import rules to enforce

Apply only to relative specifiers in `.ts`, `.tsx`, `.mts`, `.cts` files:

- Preserve bare/package imports (for example `@nestjs/core`, `node:fs`, `undici`).
- Keep non-relative aliases unchanged (for example TS path aliases like `@app/*`).
- Rewrite relative specifiers to emitted extensions:
- `.ts` and `.tsx` targets -> `.js`
- `.mts` targets -> `.mjs`
- `.cts` targets -> `.cjs`
- Extensionless relative imports -> emitted extension based on importing file type.
- Use forward slashes in import specifiers.

Examples:
- `from './service.js'`
- `import '../lib/index.mjs'`
- `export * from './adapter.cjs'`

## Deterministic workflow

1. Run audit mode first.
2. Review findings and confirm only relative specifiers are targeted.
3. Run fix mode.
4. Re-run audit mode; require zero findings.
5. Run project verification commands (build/tests) and report results.

## Commands

Run from repository root:

```bash
node skills/typescript/typescript-nodenext-apps-maintenance/scripts/nodenext-audit-imports.js
```

Fix mode:

```bash
node skills/typescript/typescript-nodenext-apps-maintenance/scripts/nodenext-audit-imports.js --fix
```

Target multiple directories:

```bash
node skills/typescript/typescript-nodenext-apps-maintenance/scripts/nodenext-audit-imports.js --dir=src --dir=test --fix
```

## Verification and reporting

- Audit mode must return exit code `1` when issues exist; after fixes it should return `0`.
- If build or tests fail after fixes, report failing command and first actionable error.
- If ambiguous imports cannot be safely rewritten, leave them unchanged and report exact file paths.

## Reference usage

Use `reference.md` for Node/TypeScript behavior details and edge cases before applying non-trivial rewrites.
