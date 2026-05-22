---
name: nestjs-cqrs-setup
description: Install, repair, and verify NestJS CQRS with environment-gated module loading via @nestjs/config and CQRS_ENABLED. Use when users ask to add CQRS, wire CommandBus/QueryBus/EventBus, create command or query handlers, or prevent DI failures by conditionally enabling CQRS modules.
---

# NestJS CQRS Setup

Use this workflow to add or fix CQRS in NestJS with deterministic environment-based enable or disable behavior.

## Prerequisites

- NestJS project with `src/main.ts` and a root module (typically `src/app.module.ts`).
- Node.js runtime compatible with the project Nest major version.
- Package manager lockfile present (`package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock`).

## Step 1: Preflight checks

1. Run all commands from project root.
2. Confirm required files exist:
   - `src/main.ts`
   - root module file (`src/app.module.ts` or project equivalent)
3. Detect package manager from lockfile and use only that manager for install and scripts.
4. Detect Nest major version from `package.json` (`@nestjs/common`).
5. If Nest 11 is detected, require Node.js 20+ before proceeding.

If preflight fails, stop and report the exact blocker before making edits.

## Step 2: Install dependencies

Install required packages:

```bash
npm install @nestjs/cqrs @nestjs/config
```

Package-manager equivalents are allowed (`pnpm add`, `yarn add`) when matching the repository lockfile.

## Step 3: Align package majors

Match package majors to the Nest major:

- Nest 11 -> `@nestjs/cqrs` ^11 and `@nestjs/config` ^4
- Nest 10 -> `@nestjs/cqrs` ^10 and `@nestjs/config` ^3

Resolve peer dependency or major-version mismatches before wiring modules.

## Step 4: Add environment toggle

Create or update `.env` with a single CQRS gate:

```env
CQRS_ENABLED=true
```

Behavior contract:

- `true` or unset: CQRS enabled
- `false`: CQRS disabled

## Step 5: Wire AppModule deterministically

In the root module imports:

1. Add `ConfigModule.forRoot({ isGlobal: true })`.
2. Add `ConditionalModule.registerWhen(CqrsModule.forRoot(), 'CQRS_ENABLED')`.
3. Gate CQRS-dependent feature modules with the same flag using `ConditionalModule.registerWhen(...)`.

Use the same toggle for infrastructure and CQRS-consuming modules to avoid DI failures when disabled.

## Step 6: Wire feature modules and handlers

1. In each CQRS feature module, import `CqrsModule`.
2. Register command/query/event handlers in `providers`.
3. Use `CommandBus`, `QueryBus`, and `EventBus` only in modules that are CQRS-enabled or conditionally imported.

## Step 7: NodeNext and ESM safeguard

If `tsconfig` uses `moduleResolution: "nodenext"` or `"node16"`, use `.js` file extensions in relative TypeScript imports.

## Step 8: Verification gates

1. Set `CQRS_ENABLED=true`, run the app, and confirm startup without CQRS DI errors.
2. Execute one command and one query flow and confirm handlers run.
3. Set `CQRS_ENABLED=false`, restart, and confirm:
   - app still boots
   - CQRS-gated modules are not loaded
   - no `CommandBus`/`QueryBus`/`EventBus` injection failures occur

## Failure handling

- If dependency installation fails, report exact failing command and error output, then stop before partial wiring.
- If required Nest files are missing, stop and request the correct project path.
- If existing architecture already contains CQRS setup, prefer minimal non-destructive edits.

## References in this skill

- AppModule conditional wiring pattern: [reference.md](reference.md)
- Minimal command/query flow: [examples.md](examples.md)