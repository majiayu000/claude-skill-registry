---
name: typescript-husky-setup
description: Install, repair, and verify Husky + lint-staged pre-commit hooks in Node.js TypeScript repositories with staged-file-only checks and deterministic validation. Use when users ask to add Git hooks, fix broken pre-commit execution, standardize commit-time lint/format checks, or align cross-platform hook behavior.
---

# TypeScript Husky Setup

Set up fast, staged-file-only pre-commit quality checks using Husky and lint-staged.

## Scope and outcomes

- Install or repair Husky and lint-staged.
- Ensure pre-commit runs only staged file checks.
- Preserve existing scripts and repository conventions.
- Verify the hook path actually executes during `git commit`.

## Preconditions

- Repository contains `package.json` and is intended for Node.js tooling.
- Git repository is initialized (`.git` exists).
- Formatter/linter commands used by lint-staged exist (direct binaries or package scripts).
- Use the repository's existing package manager when detectable; otherwise default to `npm`.

## Step 1: Baseline detection

1. Read `package.json` and detect package manager from lockfiles.
2. Check whether Husky is already initialized (`.husky/` folder and hook files).
3. Check whether `lint-staged` config exists (`package.json` key or dedicated config file).
4. Identify project file types in scope (`ts`, `tsx`, optionally `js`, `json`, `md`) before editing globs.

## Step 2: Install and initialize safely

Run from repository root.

```bash
npm install --save-dev husky lint-staged
npx husky init
```

Required `package.json` behavior:

- Ensure a `prepare` script exists and runs Husky.
- If `prepare` already exists, merge behavior without deleting existing commands.

## Step 3: Configure lint-staged deterministically

Add or repair lint-staged rules so they target staged files only.

Baseline example:

```json
"lint-staged": {
  "*.{ts,tsx}": [
    "prettier --write",
    "eslint --fix"
  ]
}
```

Rules:

- Match actual repository file types; do not invent unsupported commands.
- Prefer existing project scripts when direct commands are unavailable.
- Keep commands fast; avoid full-project checks in pre-commit.

## Step 4: Configure pre-commit hook

Set `.husky/pre-commit` to execute lint-staged.

```sh
npx lint-staged
```

Only add tests in pre-commit when explicitly requested, and keep them fast (non-coverage). Additional guidance is in [reference.md](reference.md).

## Step 5: Verification gate (required)

1. Stage a deliberately misformatted file matched by lint-staged.
2. Run `git commit -m "test hooks"`.
3. Confirm the pre-commit hook executes and only staged files are processed.
4. If files were auto-fixed, re-stage and re-run commit.
5. Confirm commit succeeds after fixes with no unrelated file processing.

## Repair matrix

- Hook not executing: run `npm run prepare`, then verify `.husky/pre-commit` exists.
- `lint-staged` reports no files: adjust glob patterns to actual staged paths.
- Permission issues on hook files: re-run `npx husky init` and ensure hook file is executable.
- Command not found inside hook: use local binaries via package scripts or install missing tool.
- Monorepo mismatch: run from repo root and scope globs/commands to affected packages.

## Non-goals

- Do not add heavy CI gates (coverage/e2e) to pre-commit by default.
- Do not rewrite unrelated npm scripts or lint configs.
- Do not enforce a package manager switch.
