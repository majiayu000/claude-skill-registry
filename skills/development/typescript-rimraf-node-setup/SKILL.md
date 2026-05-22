---
name: typescript-rimraf-node-setup
description: Add, repair, audit, or standardize `rimraf`-based cleanup in Node.js/TypeScript projects with deterministic, cross-platform `package.json` scripts. Use when users ask to add or fix `clean`/`prebuild`, replace `rm -rf` or Windows delete commands (`rmdir`, `del`), clear artifacts (`dist`, `build`, `coverage`, `.cache`, `.turbo`, `*.tsbuildinfo`), enforce CI-safe script behavior, or verify cleanup reliability on Windows and Unix.
---

# Rimraf Node Cleanup

Use this workflow to implement portable cleanup scripts that behave consistently across shells.

## Preconditions

- Work from the project root that contains `package.json`.
- Keep the current package manager (`npm`, `pnpm`, or `yarn`).
- Check build tooling before adding redundant cleanup.
- Preserve existing script names unless the user requests a rename.
- If `package.json` is missing, stop and ask for the correct project path instead of creating files speculatively.

## Workflow

1. Confirm project root and package manager deterministically:
   - Detect lockfile priority: `pnpm-lock.yaml` -> `yarn.lock` -> `package-lock.json`.
   - If no lockfile exists, preserve existing workflow and default install commands to `npm`.
2. Inspect `package.json` scripts and list cleanup-related entries.
3. Identify shell-specific delete commands (`rm -rf`, `rmdir /s /q`, `del /f /q`) and cleanup targets.
4. Decide whether a dedicated script is needed:
   - If build tooling already guarantees cleanup and no standalone cleanup command is requested, keep existing behavior.
   - Otherwise continue with `rimraf` standardization.
5. Install `rimraf` as a dev dependency only when missing:
   - `npm i -D rimraf`
   - `pnpm add -D rimraf`
   - `yarn add -D rimraf`
6. Add or update scripts using direct `rimraf` calls:
   - Standalone clean: `"clean": "rimraf dist"`
   - Multi-folder clean: `"clean": "rimraf dist coverage .cache"`
   - Prebuild hook: `"prebuild": "rimraf dist"`
7. Replace shell-specific cleanup commands with equivalent `rimraf` commands.
8. Keep scripts minimal and deterministic:
   - Do not prefix `rimraf` with `npx` inside `package.json` scripts.
   - Keep target list explicit; do not add folders that are not present or requested.
   - For glob targets, use quotes in scripts when required for shell portability (for example `"*.tsbuildinfo"`).
9. Re-open `package.json` and verify JSON validity after edits.
10. If no edit is required, report a no-op result with exact reason (already portable or explicitly out of scope).

## Script patterns

Use direct `rimraf` calls inside `package.json` scripts. Do not prefix script commands with `npx`.

Example:

```json
{
  "scripts": {
    "clean": "rimraf dist coverage .cache",
    "prebuild": "rimraf dist",
    "build": "tsc -p tsconfig.build.json"
  }
}
```

Use `npx rimraf ...` only for one-off terminal commands outside `package.json` scripts.

## Decision rules

Use rimraf when:

- A dedicated clean step is needed.
- Multiple output folders must be removed.
- Scripts must run reliably across Windows and Unix shells.

Prefer alternatives when:

- The build tool already provides sufficient cleanup (for example, `tsup` with `clean: true`) and no standalone clean script is needed.
- Cleanup is done in application code paths (use Node `fs.rm` APIs in code instead of package scripts).

Do not change behavior when:

- The user asks only for an audit/review and does not request edits.
- Existing scripts are already cross-platform and satisfy requested targets.

## Verification

1. Run the updated cleanup script (`npm run clean`, `pnpm run clean`, or `yarn clean`).
2. If a prebuild hook is present, run the build command that depends on cleanup.
3. Confirm removed folders are recreated only by the build process.
4. Confirm no shell-specific delete commands remain in `package.json` scripts.
5. If using glob targets, confirm arguments are quoted when required by the shell.
6. Confirm `rimraf` is present in `devDependencies` only once and no duplicate installer artifacts were introduced.

## Additional resources

Use [reference.md](reference.md) for CLI options, glob behavior, and the programmatic API.
