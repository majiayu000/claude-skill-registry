---
name: nestjs-maintenance
description: Run a deterministic NestJS maintenance verification loop after backend changes: execute docs, clean, build, format, lint, and test:cov in order for scripts that exist; fix failures and rerun from the top until all pass. Use for pre-commit checks, post-refactor validation, CI parity, or when asked to verify backend quality gates.
---

# NestJS Maintenance Verification

## When to use

- Backend code, config, or dependencies changed and quality gates must be revalidated.
- The user asks to run verification, maintenance checks, or pre-commit validation.
- You need local parity with CI script execution order.

## Required inputs

- Project root containing `package.json`.
- A working package manager command for this repository (`npm`, `pnpm`, or `yarn`).

## Ordered verification scripts

Run only scripts that exist in `package.json`, in this strict order:

1. `docs`
2. `clean`
3. `build`
4. `format`
5. `lint`
6. `test:cov`

## Deterministic workflow

1. Read `package.json` and load the `scripts` object.
2. Build the runnable list by filtering the ordered script names to only those present in `scripts`.
3. If no scripts from the ordered list are present, stop and report that nothing matched the maintenance pipeline.
4. If source/API files were changed and the `typescript-jsdoc-develop` skill is installed, run it before `docs` so generated documentation matches current exports.
   - If `typescript-jsdoc-develop` is not installed, continue the maintenance pipeline and report `jsdoc pre-step skipped (skill unavailable)` in the final output.
5. Execute each runnable script from repository root using the repo package manager:
   - `npm run <script>`
   - `pnpm run <script>`
   - `yarn <script>`
6. If any step fails, fix the root cause and restart from step 5 at the first script in the ordered list.
7. Repeat until the full runnable list succeeds in one uninterrupted pass.

## Failure handling rules

- Do not skip a script that exists in `package.json`.
- Do not continue to later scripts after a failure.
- Prefer code/config/dependency fixes over bypasses (`--force`, disabling checks, or script removal).
- Keep fixes minimal and aligned with existing repository conventions.

## Coverage-specific policy (`test:cov`)

1. Prefer adding/updating tests for uncovered statements and branches identified in coverage output.
2. Do not lower thresholds or exclude real project source as the default fix.
3. Exclusions are acceptable for generated/tooling files only (for example generated Prisma client, bootstrap files, framework wiring).
4. If thresholds are temporarily reduced, mark it as technical debt and add a clear follow-up note.
5. For deeper coverage remediation workflows, use `nestjs-vitest-coverage`.

## Success criteria

- Every script that exists from the ordered list passed in order during a single final run.
- No required script in the ordered list was skipped.
- The final report includes: scripts executed, failure(s) fixed, and final pass confirmation.

## Output contract

Report:

- Detected package manager and script list.
- Execution order and pass/fail status by step.
- Root-cause fix summary for each encountered failure.
- Final all-pass confirmation.
