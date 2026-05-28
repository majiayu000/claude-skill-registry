---
name: typescript-winston-setup
description: Install, repair, and verify Winston logging in NestJS TypeScript backends with ConfigService-driven settings, DI-based logger wiring, and deterministic development/production outputs. Use when users ask to add Winston, replace Nest default logging, fix broken structured logs, or standardize JSON file logging behavior.
---

# Setup Winston For NestJS

Use this workflow to install or repair Winston-backed logging in a NestJS application.

## Prerequisites

- Existing NestJS TypeScript backend with `AppModule` and `main.ts`
- Node.js 20 or later
- Package manager available (`npm`, `pnpm`, or `yarn`)

## Step 1: Preflight checks

1. Confirm the project root contains `package.json`.
2. Confirm Nest entry files exist: `src/app.module.ts` and `src/main.ts`.
3. If either file is missing, stop and ask for the correct Nest app path.
4. Check whether `@nestjs/config` is already installed.

## Step 2: Install required packages

Install `winston` with the active package manager:

- `npm`: `npm install winston`
- `pnpm`: `pnpm add winston`
- `yarn`: `yarn add winston`

If `@nestjs/config` is missing, install it:

- `npm`: `npm install @nestjs/config`
- `pnpm`: `pnpm add @nestjs/config`
- `yarn`: `yarn add @nestjs/config`

Do not install `@types/winston` because Winston v3 ships TypeScript types.

## Step 3: Add logger implementation files

Create the logger library under `src/libs/logger/`:

- `src/libs/logger/logger.module.ts`
- `src/libs/logger/logger.service.ts`

Use the implementation in [reference.md](reference.md). It provides:

- Required env validation for `LOGGER_LEVEL`, `LOGGER_SERVICE_NAME`, and `LOGGER_PATH`
- Pretty colorized console logs in development
- JSON console logs in production
- JSON file transports: `combined.log` and `error.log`
- Exception and rejection transports: `exceptions.log` and `rejections.log`
- `OnModuleDestroy` cleanup (`exceptions.unhandle()`, `rejections.unhandle()`, `logger.close()`)
- Automatic log-directory creation

## Step 4: Wire logger into Nest

1. Add `LoggerModule` to `AppModule.imports`.
2. Ensure `ConfigModule.forRoot({ isGlobal: true })` is present (or import `ConfigModule` where needed).
3. In `main.ts`, set the application logger after app creation:

```typescript
const app = await NestFactory.create(AppModule);
app.useLogger(app.get(LoggerService));
```

4. If `moduleResolution` is `nodenext` or `node16`, use `.js` extensions in relative runtime imports (for example `./logger.service.js`).

## Step 5: Configure environment variables

Create or update `.env`:

```env
LOGGER_LEVEL=info
LOGGER_SERVICE_NAME=my-service
LOGGER_PATH=logs
```

Rules:

- `NODE_ENV=production` must be set in production to enable JSON console format.
- Add `logs/` to `.gitignore` if log files should not be committed.

## Step 6: Verify behavior

1. Start the app with the repository's dev command (for example, `npm run start:dev`).
2. In development (`NODE_ENV` not production), confirm readable colorized console output.
3. In production mode, confirm JSON console output.
4. Confirm files are created under `LOGGER_PATH`:
   - `combined.log`
   - `error.log`
5. Trigger one uncaught exception and one unhandled rejection in a safe local run, then confirm:
   - `exceptions.log`
   - `rejections.log`

If verification fails, check import paths, missing env values, and whether `LoggerModule` is imported by `AppModule`.

## Deterministic checklist

- [ ] Pass preflight checks (Nest files + package manager + target path)
- [ ] Install `winston` and `@nestjs/config` when missing
- [ ] Add `LoggerModule` and `LoggerService` from [reference.md](reference.md)
- [ ] Ensure `LoggerService` implements `OnModuleDestroy` cleanup for Winston handlers
- [ ] Import `LoggerModule` and configure `ConfigModule` usage
- [ ] Call `app.useLogger(app.get(LoggerService))` in `main.ts`
- [ ] Set `LOGGER_LEVEL`, `LOGGER_SERVICE_NAME`, and `LOGGER_PATH` in `.env`
- [ ] Verify development, production, file, exception, and rejection logging outputs

## Additional resources

Full implementation snippets: [reference.md](reference.md)
