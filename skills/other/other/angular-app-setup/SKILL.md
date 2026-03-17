---
name: angular-app-setup
description: Creates an Angular 20 app directly in the current folder with strict defaults, deterministic non-interactive flags, and preflight safety checks. Use when the user asks to create, scaffold, or initialize Angular 20 in place and wants build/test verification.
---

# Angular 20 App Setup
Create a production-ready Angular 20 app directly in the current directory with strict defaults and explicit safety checks.

## Purpose

Create a production-ready Angular 20 app directly in the current directory using strict defaults, while preventing unsafe scaffolding in the wrong folder.

## Use this skill when

- The user asks to create, initialize, or scaffold an Angular app.
- The user wants Angular 20 with strict TypeScript and minimal defaults.
- The user wants to scaffold in the current folder (no nested app directory).

## Do not use this skill when

- The user asks to add Angular into an existing non-empty project that should not be overwritten.
- The user asks for a different Angular major version.
- The user asks for a monorepo workspace strategy (Nx, multi-project workspace, custom builders).

## Required inputs

Ask the user for the project name when it is not explicitly provided.
Do not invent or infer a project name.
If routing or standalone preference is not provided, keep CLI defaults and run non-interactively.

## Preflight safety checks (required)

Before running `ng new`:

1. Confirm current directory is the intended app root.
2. List existing top-level files and classify folder safety using this allowlist:
   - Allowed for in-place scaffold without extra confirmation when these are the only entries: `.git`, `.gitignore`, `.gitattributes`, `README.md`, `LICENSE`, `LICENSE.md`.
   - Treat everything else as non-empty project state and require explicit confirmation before continuing.
3. Always treat existing Angular/workspace markers as high-risk and require explicit confirmation:
   - `angular.json`, `workspace.json`, `package.json`, `src/`, `projects/`, `tsconfig.json`.
4. If target major version is not 20, stop and ask whether to continue with Angular 20 or switch to a version-appropriate flow.
5. If `npx` is unavailable, stop and ask to install Node.js/npm before proceeding.

## Root directory rule

Scaffold in the intended app root and keep all commands in that root.
Use `--directory .` so Angular CLI writes into the current folder instead of creating a nested subfolder.
If the current directory is not the intended app root, stop and ask the user to confirm or change directories before running scaffold commands.

## Scaffold command (baseline)

Use this command from the target root:

```bash
npx -y @angular/cli@20 new <project-name> --directory . --style=css --strict --skip-git --ai-config=none --defaults
```

Defaults:

- Package manager: `npm`
- Routing: Angular CLI default unless user specifies `--routing` or `--no-routing`.
- Standalone: Angular CLI default unless user specifies `--standalone` or `--no-standalone`.
- AI configuration: `none` unless user explicitly requests a supported value.

## Optional user-driven variants

Apply only when user explicitly asks:

- Change style extension (`--style=scss`, etc.).
- Force routing on/off (`--routing` or `--no-routing`).
- Change package manager (`--package-manager pnpm|yarn|bun|npm`).
- Set `--ai-config` to a supported value from `reference.md`.
- Override standalone mode (`--standalone` or `--no-standalone`).

If the user requests an unsupported `--ai-config`, stop and ask for a supported value instead of guessing.

## Verification

Run from app root:

```bash
npm install
```

```bash
npm run build
```

```bash
npm run test -- --watch=false
```

If tests are not configured yet, report that clearly and provide the next fix step instead of claiming success.
If build or tests fail, report the failing command and first actionable fix.

## Output contract

After execution, report:

1. Exact command run.
2. Any prompts/flags chosen from defaults.
3. Build result.
4. Test result.
5. Files of interest created (for example: `angular.json`, `package.json`, `src/main.ts`).
6. Any follow-up action needed.
7. Whether the folder required explicit overwrite confirmation and what was confirmed.

## Acceptance checklist

- Correctly triggers for Angular 20 setup requests.
- Does not assume a project name.
- Prevents unsafe generation in unintended folders.
- Uses in-place scaffolding (`--directory .`).
- Verifies with build and test commands.
- Reports outcomes with concrete command/results summary.
- Handles non-empty folder, unsupported flags, and missing tool prerequisites explicitly.

## Assistant Portability Rules

- Use generic tool-language such as "assistant" and "workspace root"; do not assume a specific editor or agent runtime.
- Prefer deterministic non-interactive commands and explicit flags over conversational defaults.
- If blocked, report one concrete blocker and the exact next command or input required.

## Reference
[Angular 20 documentation](reference.md)

## Tips

- Prefer `npx -y @angular/cli@20` over global `ng` to avoid version drift.
- Always confirm folder intent when any non-scaffold files are present.
- Keep `--directory .` in every in-place scaffold command to avoid accidental nested folders.
- Do not infer project names from directory names; ask explicitly when missing.
- Keep `--ai-config=none` unless the user asks for a supported alternative.
- Use `npm run build` before tests to catch configuration issues faster.
- When `npm run test -- --watch=false` hangs in CI-like shells, add `--browsers=ChromeHeadless` only if the project already supports it.
