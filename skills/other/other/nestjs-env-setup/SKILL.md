---
name: nestjs-env-setup
description: Set up NestJS .env configuration with @nestjs/config and global ConfigModule, with optional typed ConfigService wrappers and env key sync from code usage. Use when users ask to add ConfigModule/ConfigService, centralize environment access, support NodeNext/ESM imports, or sync missing env keys without overwriting existing values.
---

# NestJS env setup

Follow this workflow when configuring environment handling in an existing NestJS backend.

## Prerequisites

- Work from a NestJS project root that contains `src/` and at least one root module.
- Match `@nestjs/config` to the existing Nest major version.
- Preserve user changes in `.env`, config files, and module wiring.

## 1) Install configuration package

Install `@nestjs/config` with the project package manager.

```bash
npm install @nestjs/config
```

Install missing core Nest packages only when the project is incomplete.

## 2) Register ConfigModule globally

Locate the root module (typically `src/app.module.ts`) and add:

```ts
ConfigModule.forRoot({ isGlobal: true })
```

Add additional options only when required:

- `envFilePath` for non-default env file paths.
- `cache: true` to reduce repeated reads.
- `expandVariables: true` for `${VAR}` expansion.

## 3) Add typed environment wrapper when needed (optional)

If the project needs centralized typed access, add `EnvironmentModule` and `EnvironmentService` around `ConfigService`.

Use [reference.md](reference.md) for concrete file layout and code:

- `src/libs/environment/environment.module.ts`
- `src/libs/environment/environment.service.ts`
- `src/libs/environment/environment.utils.ts`

Expose typed getters (for example `port`) and throw explicit errors for required missing variables.

## 4) Apply NodeNext/ESM import rule deterministically

If `tsconfig.json` uses `moduleResolution: "nodenext"` or `"node16"`, all relative runtime imports in TypeScript must use emitted `.js` suffixes.

Examples:

- `./environment.service.js`
- `./libs/environment/environment.module.js`

## 5) Run env-key sync only when requested (optional)

When asked to sync `.env` with code usage, run an assistant-agnostic scan-and-merge workflow:

- Scan `src/**/*.ts` (and optionally `test/**/*.ts`).
- Collect keys from `configService.get('KEY')` and `process.env.KEY` patterns.
- Parse existing `.env`.
- Append only missing keys as `KEY=`.
- Preserve existing keys, values, comments, and blank lines.

Use [reference.md](reference.md) for regex patterns and merge pseudocode.

Optional provider adaptation: if a team uses command files (for example `.cursor/commands/env-sync.md`), store the same workflow there, but keep behavior identical.

## 6) Protect secrets and verify runtime behavior

- Ensure `.env` is listed in `.gitignore` (unless project policy uses tracked templates only).
- Never commit real secrets.
- Start the app and confirm required config values resolve.
- If env-sync ran, verify only missing keys were appended.

## Validation checklist

- [ ] `@nestjs/config` is installed and version-aligned with Nest.
- [ ] Root module imports `ConfigModule.forRoot({ isGlobal: true })`.
- [ ] Optional EnvironmentModule/EnvironmentService are wired when typed access is required.
- [ ] NodeNext/ESM projects use `.js` suffixes in relative runtime imports.
- [ ] `.env` handling preserves existing values and comments.
- [ ] Secrets are not committed.

## References

- Local implementation details and env-sync algorithm: [reference.md](reference.md)
- Local `.env` templates and output examples: [examples.md](examples.md)
- NestJS Configuration: https://docs.nestjs.com/techniques/configuration
- Node.js Environment Variables: https://nodejs.org/api/environment_variables.html
- YAML 1.2.2 specification: https://yaml.org/spec/1.2.2/
- CommonMark specification: https://spec.commonmark.org/
