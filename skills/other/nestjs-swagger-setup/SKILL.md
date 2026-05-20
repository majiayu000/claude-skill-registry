---
name: nestjs-swagger-setup
description: Install, repair, and verify OpenAPI documentation in NestJS using `@nestjs/swagger` with `@nestjs/config`-driven `SWAGGER_*` controls, optional bearer auth, explicit JSON endpoint configuration (`jsonDocumentUrl`), and deterministic UI/raw exposure gates. Use when users ask to add Swagger UI, expose or move OpenAPI JSON routes, fix broken Swagger wiring, standardize environment-based docs toggles, or validate production-safe docs behavior.
---

# NestJS Swagger Setup

Use this workflow to install or repair Swagger UI and OpenAPI JSON endpoints in a NestJS application.

## Inputs

Collect before changes:
- Project root path
- Package manager (`npm`, `pnpm`, or `yarn`)
- Existing global prefix usage (`app.setGlobalPrefix(...)`)
- Desired docs exposure in production (`enabled` or `disabled`)

If a required input is missing, ask one precise question and pause implementation.

## Preconditions

1. Confirm the target is a NestJS project with `main.ts` and a root module.
2. Confirm Node and dependency compatibility for the workspace.
3. Confirm write access to source files and environment files.

If preconditions fail, stop and report the exact blocker.

## Deterministic Workflow

1. Install required dependencies from project root:
   - `@nestjs/swagger`
   - `@nestjs/config`
2. Verify major-version alignment:
   - Nest 11 -> `@nestjs/swagger` ^11
   - Nest 10 -> `@nestjs/swagger` ^10
3. Ensure `ConfigModule.forRoot({ isGlobal: true })` is configured in the root module (or preserve an equivalent existing global config strategy).
4. Create or repair bootstrap helper using [reference.md](reference.md):
   - `src/libs/swagger/setup-swagger.ts`
5. Wire `setupSwagger(app)` in `main.ts` after app creation and before `listen(...)`.
6. Create or update `.env` keys for Swagger behavior:
   - `SWAGGER_ENABLED`
   - `SWAGGER_PATH`
   - `SWAGGER_UI_ENABLED`
   - `SWAGGER_RAW_ENABLED`
   - `SWAGGER_JSON_URL`
   - `SWAGGER_USE_GLOBAL_PREFIX`
   - optional `SWAGGER_BEARER_AUTH`
7. Ensure `.env` is ignored by git when repository policy requires local secrets.
8. Preserve unrelated project code and avoid refactoring outside Swagger/config scope.

## Route Rules

- Default docs path: `SWAGGER_PATH=api/docs`
- Default JSON route segment: `SWAGGER_JSON_URL=openapi.json`
- If `SWAGGER_USE_GLOBAL_PREFIX=true`, JSON endpoint is prefixed by the app global prefix.
- If `SWAGGER_UI_ENABLED=false`, only raw definition endpoints are served when `SWAGGER_RAW_ENABLED=true`.
- If both UI and raw are disabled, no Swagger surface should be exposed.

## Security Defaults

- Default production stance: `SWAGGER_ENABLED=false` unless explicitly required.
- If enabled in production, require upstream protection (gateway auth, app guard, or network allowlist).
- Do not use sensitive secrets as feature flags for Swagger enablement.

## Verification Gates

1. Start the app (`start` or `start:dev`).
2. Validate docs UI route when enabled:
   - `http://localhost:<PORT>/<SWAGGER_PATH>`
3. Validate OpenAPI JSON route when raw is enabled:
   - without prefix: `http://localhost:<PORT>/<SWAGGER_JSON_URL>`
   - with prefix: `http://localhost:<PORT>/<global-prefix>/<SWAGGER_JSON_URL>`
4. Validate bearer auth button only when `SWAGGER_BEARER_AUTH=true`.
5. Validate the Swagger top bar includes the `Download OpenAPI` button pointing to configured JSON route.
6. Report exact pass/fail status for each gate.

## Failure Handling

- If dependency installation fails, report command and error context and stop before partial wiring.
- If required files are missing (`main.ts`, root module), stop and request the correct project path.
- If an existing Swagger setup is present, perform minimal edits instead of replacing unrelated options.

## Deliverables

- Updated dependency manifest
- Updated root module config import/wiring
- Updated `main.ts` bootstrap call
- Added or updated `src/libs/swagger/setup-swagger.ts`
- Added or updated `.env` Swagger variables
- Verification summary with concrete tested routes

## Checklist

- [ ] Dependencies installed and version-aligned
- [ ] `ConfigModule` globally available
- [ ] `setupSwagger` helper added or repaired
- [ ] `setupSwagger(app)` called before `listen(...)`
- [ ] `.env` contains required `SWAGGER_*` keys
- [ ] Swagger exposure matches UI/raw/global-prefix toggles
- [ ] `Download OpenAPI` button visible and functional when UI enabled
- [ ] Verification results documented with exact routes

## Additional Resources

- Full implementation: [reference.md](reference.md)
- Minimal snippets: [examples.md](examples.md)
