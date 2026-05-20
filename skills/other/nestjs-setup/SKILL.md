---
name: nestjs-typescript-setup
description: Scaffold or repair a NestJS TypeScript backend with deterministic Nest CLI commands, package-manager aware scripts, strict mode defaults, optional SWC enablement, and verification gates. Use when users ask to install NestJS, bootstrap a new Nest API, add NestJS into an existing repository, fix broken setup commands, or validate Node/CLI version compatibility.
---

# NestJS TypeScript Setup

## Scope and trigger

Use this skill when the request is about creating, repairing, or validating a NestJS + TypeScript project setup.

## Inputs to resolve before execution

Collect or confirm these inputs first:

- `projectPathOrName`: required; do not assume a name when missing.
- `packageManager`: one of `npm`, `pnpm`, `yarn`.
- `targetParentDir`: directory where scaffolding should run.
- `existingGitRepo`: whether the target parent already has `.git`.
- `useSwc`: optional; default `false` unless requested.

If any required input is missing, ask one precise question.

## Preconditions

Run preflight checks before scaffolding:

1. Confirm Node version satisfies Nest docs baseline (`>= 20`) and current CLI engine floor.
   - `node -v`
   - `npm view @nestjs/cli engines --json`
2. Confirm package manager is installed.
   - `npm -v` or `pnpm -v` or `yarn -v`
3. Confirm target parent exists and is writable.

Stop and report blocker details if preflight fails.

## Deterministic scaffold workflow

1. Build scaffold command from target parent directory:
   - `npx @nestjs/cli@latest new <projectPathOrName> --package-manager <packageManager> --strict`
2. If `existingGitRepo=true`, append `--skip-git`.
3. Execute scaffold command from `targetParentDir`.
4. Change directory into created Nest app root.
5. Run startup command with chosen package manager:
   - `npm run start:dev`
   - `pnpm start:dev`
   - `yarn start:dev`
6. Verify app responds at `http://localhost:3000` with default starter response.

## Existing repository integration

When adding Nest inside an already versioned repository:

1. Run scaffold from repository root or chosen subfolder parent.
2. Always include `--skip-git`.
3. Keep all subsequent install/run/lint/test commands in the generated Nest app root.

## Optional SWC enablement

Only apply when explicitly requested.

1. Install SWC dependencies in project root:
   - `npm i --save-dev @swc/cli @swc/core`
2. Update `nest-cli.json`:

```json
{
  "compilerOptions": {
    "builder": "swc",
    "typeCheck": true
  }
}
```

3. Verify with one command:
   - `npx nest start -b swc --type-check`

## Verification gates

Mark complete only when all checks pass:

- [ ] Preflight checks passed (Node, package manager, writable target)
- [ ] Scaffold command completed without interactive ambiguity
- [ ] Commands executed from generated Nest app root
- [ ] Dev server starts successfully
- [ ] Local HTTP response check passes (`http://localhost:3000`)
- [ ] Optional SWC path verified when enabled

## Recovery rules

- If scaffolding partially succeeds (folder created, install failed), continue from project root and fix dependency/install issues without re-scaffolding unless user requests reset.
- If package manager mismatch is detected after scaffold, align scripts and lockfile usage to the user-selected manager.
- Do not delete user files to recover from setup failures.

## Official references

Use `reference.md` for authoritative links and command details.