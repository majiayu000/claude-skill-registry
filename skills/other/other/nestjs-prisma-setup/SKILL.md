---
name: nestjs-prisma-setup
description: Install, repair, and verify Prisma ORM in NestJS backends with deterministic package-manager-aware commands, SQLite-first defaults using @prisma/adapter-better-sqlite3, prisma.config.ts datasource wiring, PrismaService/PrismaModule integration, and migration plus runtime verification gates. Use when users ask to add Prisma, fix broken Prisma setup, initialize schema/migrations, wire Prisma into Nest DI, or align CommonJS vs NodeNext/ESM import behavior.
---

# NestJS Prisma Setup

Use this workflow to install or repair Prisma in a NestJS backend with reproducible verification.

## Scope and outcomes

- Add Prisma CLI and client dependencies.
- Initialize `prisma/schema.prisma` and `prisma.config.ts` with SQLite defaults.
- Wire a reusable `PrismaService` and global `PrismaModule` for Nest DI.
- Run migrations and client generation.
- Verify runtime read/write behavior through application endpoints.

## Preflight checks (required)

1. Confirm repository contains Nest bootstrap files (`src/main.ts` and app module).
2. Detect package manager from lockfile:
   - `package-lock.json` -> npm
   - `pnpm-lock.yaml` -> pnpm
   - `yarn.lock` -> yarn
3. Confirm Node runtime compatibility for installed Nest/Prisma versions.
4. If Prisma already exists, do repair mode only (preserve existing schema/models unless user requests schema rewrite).

## Install dependencies

Run commands from repository root using the detected package manager.

### npm

```bash
npm install --save-dev prisma dotenv
npm install @prisma/client @prisma/adapter-better-sqlite3 better-sqlite3
npm install @nestjs/config
```

### pnpm

```bash
pnpm add -D prisma dotenv
pnpm add @prisma/client @prisma/adapter-better-sqlite3 better-sqlite3
pnpm add @nestjs/config
```

### yarn

```bash
yarn add -D prisma dotenv
yarn add @prisma/client @prisma/adapter-better-sqlite3 better-sqlite3
yarn add @nestjs/config
```

Notes:
- Install `@nestjs/config` only if not already present.
- Keep `prisma` and `@prisma/client` on the same major version.

## Initialize Prisma

Run from repository root using the selected package manager runner:

```bash
npx prisma init --datasource-provider sqlite --output ../src/libs/prisma/generated
```

Equivalent runners are acceptable (`pnpm prisma init`, `yarn prisma init`) if they produce the same files.

Expected outputs:
- `prisma/schema.prisma`
- `prisma.config.ts`
- `.env` (merge entries if file already exists)

## Configure schema and Prisma config

1. Apply generator and datasource scaffolding from [reference.md](reference.md).
2. Keep datasource URL in `prisma.config.ts` when using driver adapters.
3. For CommonJS projects, set `moduleFormat = "cjs"`.
4. For NodeNext/ESM projects, keep generator/module settings and emitted `.js` import paths aligned.
5. Add or preserve project models in `prisma/schema.prisma`.

## Add Prisma runtime integration

1. Create or repair files from [reference.md](reference.md):
   - `src/libs/prisma/prisma.service.ts`
   - `src/libs/prisma/prisma.module.ts`
2. `PrismaService` requirements:
   - Extend generated `PrismaClient`.
   - Inject `ConfigService` and read `DATABASE_URL`.
   - Construct `PrismaBetterSqlite3` adapter and pass `super({ adapter })`.
   - Implement `OnModuleInit` and `OnModuleDestroy`.
   - Optionally run startup `VACUUM` with non-fatal failure handling.
3. Enforce constructor safety: do not access `this` before `super()`.
4. Do not use `this.$on('beforeExit', ...)` with driver adapters.

## Wire Nest module graph

1. Ensure `ConfigModule.forRoot({ isGlobal: true })` exists in `AppModule` (or equivalent bootstrap config).
2. Import `PrismaModule` into `AppModule`.
3. Keep `PrismaModule` global so feature modules can inject `PrismaService` without repeated imports.

## Environment configuration

For SQLite, ensure `.env` contains:

```env
DATABASE_URL="file:./dev.db"
```

Use an absolute path when runtime cwd differs from project root. Keep `.env` excluded from source control when required by repository policy.

## Migrations and client generation

After schema changes:

```bash
npx prisma migrate dev --name init
npx prisma generate
```

Optional scripts:

```json
"prisma:generate": "prisma generate",
"prisma:migrate": "prisma migrate dev"
```

## Verification gates (required)

1. Start application (`npm run start:dev` or project equivalent).
2. Confirm no Prisma connection or adapter initialization errors at startup.
3. Execute at least one read and one write path through endpoints/services that inject `PrismaService`.
4. Confirm generated client artifacts exist under `src/libs/prisma/generated`.
5. Confirm migration files and SQLite db file are created as expected.
6. If NodeNext/ESM is enabled, confirm runtime imports resolve with emitted `.js` extensions.

## Repair mode guidance

Use this when Prisma already exists but is broken:
- Reconcile `prisma` and `@prisma/client` major versions.
- Verify `prisma.config.ts` datasource URL is present and points to `DATABASE_URL`.
- Fix incorrect generated client import paths (CJS vs ESM mismatch).
- Remove unsupported `beforeExit` hook usage for adapter-based clients.
- Re-run `prisma generate` and app startup verification gates.

## Checklist

- [ ] Detect package manager and execute matching commands
- [ ] Install Prisma dependencies and `@nestjs/config` when needed
- [ ] Initialize Prisma with SQLite provider and generated client output path
- [ ] Configure `schema.prisma` and `prisma.config.ts`
- [ ] Add or repair `PrismaService` and `PrismaModule`
- [ ] Wire `ConfigModule` and `PrismaModule` in app module graph
- [ ] Run migrations and generate client
- [ ] Verify runtime read/write behavior and generated artifacts
- [ ] Validate ESM/CJS alignment when applicable

## Additional resources

- Full implementation snippets: [reference.md](reference.md)
- Usage pattern examples: [examples.md](examples.md)
- [NestJS Prisma recipe](https://docs.nestjs.com/recipes/prisma)
- [Prisma CLI init reference](https://www.prisma.io/docs/orm/reference/prisma-cli-reference#init)
- [Prisma driver adapters](https://www.prisma.io/docs/orm/overview/databases/database-drivers)
