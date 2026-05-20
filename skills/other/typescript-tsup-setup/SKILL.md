---
name: typescript-tsup-setup
description: Install, repair, or standardize tsup in TypeScript projects for library and Node app builds. Use when users ask to add tsup, set ESM/CJS outputs, generate `.d.ts`, fix `package.json` `exports`/entry fields, replace legacy build scripts, or verify dist artifacts and runtime entry resolution.
---

# Setup TSup

Use this workflow to set up tsup with minimal, production-safe defaults.

## Inputs to collect

- `projectRoot` (default: current working directory)
- `targetKind`: `library` or `node-app`
- `entry`: default `src/index.ts` for libraries, `src/main.ts` for apps
- `formats`: `esm`, `cjs`, or both
- `generateDts`: default `true` for libraries, `false` for apps
- `addWatchScript`: default `true`

## Workflow

1. Validate project context
   - Check `package.json` exists.
   - Detect package manager from lockfile (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`).
   - Detect module mode from `package.json.type`.
   - Confirm entry file(s) exist before writing config.
   - If `tsup.config.ts` exists, back up intent by preserving non-default options unless they conflict with explicit user requirements.

2. Ensure dependency
   - Install `tsup` as a dev dependency if missing:
     - `npm i -D tsup`
     - `pnpm add -D tsup`
     - `yarn add -D tsup`
   - Keep existing pinned version unless the user asks to upgrade.

3. Create or minimally update `tsup.config.ts`
   - Use `defineConfig` from `tsup`.
   - Preserve existing advanced options unless they are clearly wrong.

4. Apply target profile
   - Use this baseline for libraries:

```typescript
import { defineConfig } from 'tsup'

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,
  sourcemap: true,
  clean: true,
})
```

   - Use this baseline for Node apps:

```typescript
import { defineConfig } from 'tsup'

export default defineConfig({
  entry: ['src/main.ts'],
  format: ['cjs'],
  platform: 'node',
  sourcemap: true,
  clean: true,
})
```

   - Match output format to runtime expectations:
     - If `package.json.type` is `"module"`, prefer `esm`.
     - If runtime expects CommonJS, keep `cjs`.

5. Update `package.json` scripts
   - Add or update:
     - `"build": "tsup"`
     - `"build:watch": "tsup --watch"` when `addWatchScript = true`
   - For apps, add a production start script that matches output filename.
   - Preserve unrelated existing scripts.

6. Align package entry fields for libraries
   - Ensure `main`, `module`, `types`, and `exports` point to generated files.
   - Use explicit extensions when dual-format output is needed:

```typescript
outExtension({ format }) {
  return { js: format === 'cjs' ? '.cjs' : '.mjs' }
}
```

```json
{
  "main": "./dist/index.cjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs"
    }
  }
}
```

7. Verify
   - Run `npm run build` / `pnpm build` / `yarn build` based on detected package manager.
   - Confirm expected artifacts exist in `dist/`.
   - For libraries, verify `package.json` entry fields point to actual emitted files.
   - For apps, run built output with `node` to confirm runtime resolution.

## Guardrails

- Do not change module system (`type: module` vs CommonJS) unless explicitly asked.
- Do not force minification, treeshaking strategy, or code splitting unless requested.
- Do not overwrite non-trivial existing config; merge minimally.
- For monorepos, run install and build in the package directory, not the repo root.
- Note: tsup upstream is in maintenance mode. Keep using tsup when requested; suggest tsdown only if the user asks about long-term migration.
- Use Node package entry conventions conservatively: treat `exports` as authoritative when present, and keep `main` for backward compatibility where needed.

## Output checklist

- `tsup` exists in `devDependencies`.
- `tsup.config.ts` matches target kind and runtime format.
- `package.json` scripts build successfully.
- Library package entry fields (`exports` and `types`) match generated outputs.
- Build verification was executed and result reported.

## Additional resources

Use [reference.md](reference.md) for advanced options, edge cases, and troubleshooting.
