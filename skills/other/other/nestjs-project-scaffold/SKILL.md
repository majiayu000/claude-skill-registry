---
name: "nestjs-project-scaffold"
description: "Use this skill whenever the user wants to create, restructure, or standardize a NestJS backend project in TypeScript, including folder layout, config, environment setup, tooling, and initial integrations (TypeORM-ready, testing-ready, and deployment-friendly)."
---

# NestJS Project Scaffold Skill

## Purpose

You are a specialized assistant for **bootstrapping and reshaping NestJS projects** so they follow
consistent, production-ready conventions.

Use this skill to:

- Scaffold a **new NestJS project** (standalone or part of a monorepo)
- Restructure an **existing NestJS project** to match preferred folder & module layout
- Wire up base tooling:
  - TypeScript strict mode
  - ESLint + Prettier
  - Environment/config management
  - Basic logging & health check
- Make the project **TypeORM-ready**, **testing-ready**, and **deployment-ready** without fully
  implementing domain logic (other NestJS skills can do that).

Do **not** use this skill for:

- Implementing business logic (use modules/services/controllers skills)
- Advanced auth, caching, or microservices concerns
- Non-NestJS backend frameworks (Hono, Express-only, etc.)

If `CLAUDE.md` exists in the repo, treat it as authoritative for project layout, naming, and tooling preferences.

---

## When To Apply This Skill

Trigger this skill when the user says things like:

- “Create a new NestJS API project.”
- “Set up a clean NestJS backend skeleton with TypeORM and testing.”
- “Restructure this NestJS project to follow a standard layout.”
- “Prepare this repo for NestJS with good defaults and configs.”
- “Add NestJS to this monorepo in a consistent way.”

Avoid this skill when the task is clearly about:

- Adding a specific module/feature (e.g. `users`, `auth`) → use feature/module-oriented skills.
- Only touching TypeORM entities/migrations → use TypeORM skills.

---

## Project Assumptions

Unless the user or `CLAUDE.md` says otherwise, assume:

- Language: **TypeScript**
- Package manager preference:
  1. `pnpm` if `pnpm-lock.yaml` exists
  2. `yarn` if `yarn.lock` exists
  3. otherwise `npm`
- Framework: **NestJS** (latest stable @ the time), CLI-based
- Testing: **Jest** by default (can later swap or complement with other tools)
- ORM: TypeORM will be used, but concrete entities & config belong to the `nestjs-typeorm-integration` skill.
- Env management: `.env` files + Nest `ConfigModule` or equivalent.

---

## Target Project Structure

This skill aims to create or converge towards a structure like:

```text
project-root/
  src/
    app.module.ts
    main.ts
    config/
      app.config.ts
      database.config.ts   # optional, for TypeORM later
    common/
      filters/
      guards/
      interceptors/
      decorators/
      dto/
    modules/
      health/
        health.module.ts
        health.controller.ts
    infrastructure/
      # optional: cross-cutting infra, e.g. database, messaging
  test/
    app.e2e-spec.ts
    jest-e2e.json
  .env.example
  nest-cli.json
  tsconfig.json
  tsconfig.build.json
  package.json
  README.md
```

For monorepos, adapt to a `apps/api` or similar convention, but maintain the same internal NestJS structure.

---

## High-Level Workflow

When this skill is active, follow this process:

1. **Detect or create NestJS project**
   - If no NestJS project exists:
     - Use CLI-equivalent steps to create a new Nest project in the desired folder.
     - Set language to TypeScript.
   - If a NestJS project exists:
     - Inspect its structure (`main.ts`, `app.module.ts`, `src/` layout, `nest-cli.json`).
     - Plan restructuring to align with the target structure above.

2. **Set up config & environment management**
   - Install and configure `@nestjs/config` (or follow project’s preferences in `CLAUDE.md`).
   - Create `src/config` directory with at least `app.config.ts` and (optionally) `database.config.ts`.
   - Wire `ConfigModule.forRoot({ isGlobal: true, ... })` in `app.module.ts`.

3. **Create base common infrastructure**
   - Create `src/common` with subfolders for:
     - `filters` (e.g. `http-exception.filter.ts`)
     - `guards` (e.g. auth guards to be filled later)
     - `interceptors` (e.g. logging/transform interceptors)
     - `decorators` (custom decorators go here)
     - `dto` (shared DTOs)
   - Provide at least one example (like a basic logging interceptor or global exception filter) if it fits the project direction.

4. **Add a health module**
   - Create `HealthModule` in `src/modules/health` or `src/health`:
     - `health.module.ts`
     - `health.controller.ts` with a simple `GET /health` endpoint.
   - Optionally integrate with Nest’s health checks later (e.g. Terminus) via another skill.

5. **Configure main bootstrap**
   - In `main.ts`, configure:
     - `NestFactory.create(AppModule)`
     - Global prefix if desired (e.g. `/api`)
     - Validation pipe (can be added here or in a future validation skill)
     - Basic logging

   Example outline (pseudocode-level, adjusted per project):

   ```ts
   async function bootstrap() {
     const app = await NestFactory.create(AppModule);
     app.setGlobalPrefix("api");
     await app.listen(process.env.PORT ?? 3000);
   }
   bootstrap();
   ```

   Maintain flexibility; actual details may depend on other skills (auth, validation).

6. **Prepare TypeORM integration points (without full config)**
   - Ensure structure allows adding database modules later:
     - `src/config/database.config.ts` placeholder
     - `src/infrastructure/database` placeholder directory if desired
   - Do **not** fully wire TypeORM here; leave detailed config to `nestjs-typeorm-integration` skill.

7. **Tooling & quality gates**
   - Ensure `tsconfig.json` and `tsconfig.build.json` are present and sane:
     - Strict type checking preferred (unless `CLAUDE.md` says otherwise).
   - Ensure ESLint is set up (via Nest CLI defaults or project conventions).
   - Ensure basic `lint`, `build`, `start`, `start:dev`, `test`, `test:e2e` scripts in `package.json` are present or corrected.

8. **Testing scaffold**
   - Ensure Jest config exists (default from Nest CLI).
   - Make sure `test/app.e2e-spec.ts` and `jest-e2e.json` exist or create them if missing.
   - Don’t add detailed tests here (that’s for `nestjs-testing-skill`), but confirm scaffolding is ready.

9. **Monorepo awareness (if applicable)**
   - If the project is part of a monorepo (e.g. `apps/api`):
     - Respect workspace structure (PNPM/Yarn/Nx/Turbo).
     - Place Nest app under correct folder (`apps/api` or similar).
     - Ensure scripts work from root (`pnpm dev:api`, etc.) if conventions exist.

10. **Documentation**
    - Update or create `README.md` with:
      - How to run the project (`install`, `start:dev`, `test`)
      - Basic architecture overview (where modules live)
      - Where to add new modules (`src/modules`)
      - Where config and env files live

---

## Safe Defaults & Conventions

When making decisions:

- Use **convention over configuration**:
  - `src/modules/...` for feature modules
  - `src/common/...` for shared utilities
  - Config modules in `src/config/...`

- Don’t enforce a specific hexagonal/onion architecture unless `CLAUDE.md` says so, but do:
  - Separate pure domain modules from infrastructure when it’s clearly beneficial.
  - Be consistent across the project.

- Keep bootstrapping minimal and extensible:
  - Don’t hardcode features that belong to dedicated skills (auth, caching, microservices).
  - Provide hooks/placeholders so those skills can plug in cleanly.

---

## Example Prompts That Should Use This Skill

- “Create a new NestJS API service in `apps/api` with our usual setup.”
- “Reshape this messy NestJS codebase into a clean structure with modules and common utilities.”
- “Scaffold a NestJS project that we can later plug TypeORM and auth into.”
- “Set up a standard NestJS backend with config, health check, and testing ready.”

For these prompts, this skill should:

- Either create the NestJS app from scratch **or** refactor the existing project.
- Leave clear, well-structured hooks for other NestJS skills (auth, TypeORM integration, testing, microservices)
  to extend the backend cleanly.
