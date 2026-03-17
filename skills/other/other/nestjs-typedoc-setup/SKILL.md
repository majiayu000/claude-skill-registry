---
name: nestjs-typedoc-setup
description: Install, repair, standardize, and validate TypeDoc in NestJS backends with deterministic preflight checks, non-destructive config updates, package-manager-aware commands, and verification gates. Use when users ask to add TypeDoc, fix broken docs builds, repair typedoc config/scripts, or standardize NestJS API documentation workflows.
---

# NestJS TypeDoc Setup and Repair

Use this workflow to add or repair TypeDoc documentation in a NestJS application.

## Scope and safety

- This skill configures TypeDoc tooling and docs generation only.
- Do not modify runtime application behavior unless the user explicitly asks.
- Do not remove existing docs tooling unless there is a proven conflict.
- Run commands from the Nest app root unless the user targets a monorepo package.

## Deterministic workflow

### 1. Preflight checks (required)

Confirm all required markers before editing:

- `package.json` exists in target root.
- `src/main.ts` exists (or the user explicitly confirms a non-standard entry path).
- `tsconfig.json` or another project `tsconfig*.json` exists.

Detect package manager from lockfile:

- `package-lock.json` -> npm
- `pnpm-lock.yaml` -> pnpm
- `yarn.lock` -> yarn
- `bun.lockb` -> bun
- If none exist, default to npm and state that assumption.

Detect existing TypeDoc configuration in this order:

1. `typedoc.json`
2. `typedoc.config.{json,cjs,mjs,js}`
3. `package.json#typedoc`

If config already exists, patch minimally and preserve unrelated keys.

### 2. Install dependencies (required)

Install required packages with the detected package manager:

```bash
npm install --save-dev typedoc typedoc-material-theme
pnpm add -D typedoc typedoc-material-theme
yarn add -D typedoc typedoc-material-theme
bun add -d typedoc typedoc-material-theme
```

### 3. Create or update TypeDoc config (required)

Preferred config file: `typedoc.json` at target root.

If no config exists, create:

```json
{
  "entryPoints": ["src"],
  "out": "docs/api",
  "tsconfig": "tsconfig.json",
  "plugin": ["typedoc-material-theme"],
  "entryPointStrategy": "expand",
  "exclude": [
    "**/*.spec.ts",
    "**/*.test.ts",
    "dist/**",
    "node_modules/**"
  ],
  "excludePrivate": true,
  "excludeProtected": true,
  "cleanOutputDir": true
}
```

Merge policy when config already exists:

- Preserve existing `entryPoints`, `tsconfig`, and output location when they are valid and intentional.
- Add missing required defaults only when absent.
- Preserve user excludes and append missing Nest-safe excludes.
- Keep existing plugins and append `"typedoc-material-theme"` only if missing.

Exclude policy:

- Ensure these excludes exist: `"**/*.spec.ts"`, `"**/*.test.ts"`, `"dist/**"`, `"node_modules/**"`.
- When Prisma is installed, ensure `"**/prisma/generated/**"` is present.

Entry point policy:

- Default `entryPoints: ["src"]` for full backend docs.
- Use `["src/main.ts"]` only when user asks for a constrained public surface.
- Default `entryPointStrategy: "expand"` unless existing config intentionally uses another strategy.

### 4. Ensure scripts in `package.json` (required)

Ensure docs scripts exist without destructive rewrites:

- Add `docs:api` as `typedoc` when missing.
- Add `docs:api:watch` as `typedoc --watch` when missing.
- Preserve existing docs script names and values unless broken.

```json
"docs:api": "typedoc",
"docs:api:watch": "typedoc --watch"
```

### 5. Update `.gitignore` idempotently (required)

Add docs output ignore entry once:

```gitignore
docs/api/
```

If the project already ignores a broader path like `docs/`, keep it and do not duplicate entries.

### 6. Verify and troubleshoot (required)

Run docs generation with the local script:

```bash
npm run docs:api
```

Verification gates:

1. Command completes without TypeDoc errors.
2. Output directory exists at configured `out` (default `docs/api/`).
3. Main HTML entry exists (`index.html`).
4. Test/build/generated files in exclude list are not documented.

Troubleshooting branch when generation fails:

- Check Node.js version compatibility with the Nest workspace.
- Check `tsconfig` path in TypeDoc config.
- Confirm `typedoc-material-theme` is installed and listed in `plugin`.
- If plugin errors persist, run once without plugin to isolate root cause.
- If monorepo pathing fails, rerun from the package root containing `src/main.ts`.

## JSDoc quality conventions

- Prefer behavior-first docs on public API surfaces only.
- Use `@param`, `@returns`, and `@example` for method-level clarity.
- Use `@remarks` for non-obvious service or module context.
- Avoid repeating type syntax already captured by TypeScript signatures.

See [examples.md](examples.md) for concrete snippets.

## Optional enhancements

- Add `themeColor` for `typedoc-material-theme` branding alignment.
- Add `typedoc-plugin-markdown` when markdown output is required.
- Run docs generation in CI and publish static output as needed.

See [reference.md](reference.md) for full option details.

## Checklist

- [ ] Validate Nest workspace markers and package manager
- [ ] Detect existing TypeDoc config and choose non-destructive merge path
- [ ] Install `typedoc` and `typedoc-material-theme`
- [ ] Create or patch TypeDoc config with required excludes and plugin
- [ ] Ensure docs scripts exist in `package.json`
- [ ] Add docs output ignore rule idempotently
- [ ] Run docs generation and pass verification gates

## References

- TypeDoc options and CI notes: [reference.md](reference.md)
- NestJS-focused config and JSDoc examples: [examples.md](examples.md)
