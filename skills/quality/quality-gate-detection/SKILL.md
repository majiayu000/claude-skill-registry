---
name: Quality Gate Detection
description: >-
  Detect and configure quality gate commands for Ralph's autonomous execution.
  Use when: (1) Analyzing a project to determine available test, lint, and build scripts,
  (2) Generatiing a task-specific verification checklist based on project reality.
  This skill enables Ralph to adapt verification to the specific project context.
---

# Quality Gate Detection

Dynamically detect project quality gates from `package.json` scripts and frameworks.

## Prerequisites

- Read access to `package.json` in the project root

## Detection Process

### Step 1: Analyze Project Scripts (Hybrid Diagnosis)

Read `package.json` and inspect the `scripts` section to identify verification commands.

**Priority Heuristics:**
1. **Test:** Look for `test`, `test:unit`, `test:ci`. Preference: `npm test` or specific script.
2. **Lint:** Look for `lint`, `lint:fix`, `eslint`. Preference: `npm run lint`.
3. **Typecheck:** Look for `typecheck`, `tsc`, `build`. Preference: `npm run typecheck` or `tsc --noEmit`.
4. **Browser/E2E:** Look for `test:browser`, `e2e`, `cypress`, `playwright`. Preference: `npm run test:browser`.

**Framework Detection:**
- Identify test runner: `jest`, `vitest`, `mocha`, `ava`.
- Identify linter: `eslint`, `tslint`, `biome`.
- Identify builder/runtime: `tsc`, `vite`, `next`, `webpack`.

### Step 2: Formulate Verification Commands

Construct the actual commands to be run by the agent.
- If a script exists (e.g., `"test": "jest"`), use `npm run test`.
- If no script exists but framework is detected (e.g., `jest` in dependencies), try standard binary `npx jest`.
- **MISSING:** If no scripts/frameworks are detected for a category, leave the command empty. Do NOT assume defaults like `npm test` exist.

### Step 3: Execution (Just-in-Time)

Use the detected commands immediately to verify your work.
- Do **not** write a `quality-gates.json` file.
- Do **not** ask for permission to run standard checks unless they are destructive.
- Simply execute the commands as part of your verification loop.

## Edge Cases

**Ambiguous Scripts:**
- If multiple scripts match (e.g., `test` and `test:all`), prefer the one that seems most appropriate for *local* verification (often `test` or `test:unit`).
- When in doubt, note the ambiguity in the "rationale".

**Missing Scripts:**
- If a category (e.g., `lint`) has no script and no detected config, omit it from the *required* gates. Report it as "Not Detected".

## Validation

1. Verify `package.json` exists and is valid JSON.
2. Ensure derived commands are executable (e.g., don't suggest `npm run lint` if `lint` script is missing).

## Reference Documentation

- **Config Template**: See `tools/config.json` for full configuration structure
