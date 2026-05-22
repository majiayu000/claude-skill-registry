---
name: angular-docker-compose-env-coverage
description: Create, repair, and verify Dockerfile plus Docker Compose setup for Angular 20, with deterministic checks that every variable declared in `.env` files is covered by compose configuration. Use when users ask to dockerize Angular 20, add or fix compose files, enforce `.env` coverage, prevent missing runtime/build variables, or standardize repeatable container validation.
---

# Angular 20 Docker Compose Env Coverage

## Goal

Build or fix a production-safe Angular 20 container setup and enforce that every variable defined in targeted `.env` files is represented in Compose usage.

## Inputs

- `projectRoot` (default: current working directory)
- `composeFile` (optional, auto-detect when omitted)
- `envFiles` (optional, default: `.env` and `.env.*` except examples)
- `strictCoverage` (boolean, default: `false`)

## Success Criteria

- Angular 20 app has a valid Docker build path (`Dockerfile`).
- `docker-compose.yml` (or `.yaml`) exists and is valid.
- Every variable in targeted `.env` files is covered by compose.
- Coverage check is automated and repeatable.

## Workflow

1. Validate workspace and scope
- Resolve `projectRoot` first; default to current working directory.
- Confirm `package.json` and `angular.json` exist under `projectRoot`.
- Confirm `@angular/core` major version is `20`.
- Stop and report before any Docker changes if workspace is missing or version is not Angular 20.

2. Create or repair Dockerfile
- Use a multi-stage build by default.
- Builder stage: install dependencies deterministically (`npm ci`) and build Angular output.
- Runtime stage: serve built artifacts from a lightweight web image (for example Nginx).
- Keep build arguments and runtime environment handling explicit; do not rely on hidden defaults.

3. Create or repair Compose configuration
- Detect or create one canonical compose file (`docker-compose.yml`, `docker-compose.yaml`, `compose.yml`, or `compose.yaml`).
- Ensure services, ports, build context, restart policy, and image naming are coherent.
- Prefer explicit `environment` mappings for app-relevant variables.
- If `env_file` is used, keep file paths explicit and stable.

4. Enforce `.env` variable coverage
- Run coverage check in referenced mode:
```bash
python .agents/skills/angular/angular-docker-compose-env-coverage/scripts/check_env_compose_coverage.py --project-root .
```
- The script must exit non-zero when variables are missing from compose coverage.
- In `strictCoverage` mode, require explicit environment wiring:
```bash
python .agents/skills/angular/angular-docker-compose-env-coverage/scripts/check_env_compose_coverage.py --project-root . --mode strict
```

5. Fix uncovered variables
- Add missing variables to compose `environment:` with explicit mapping (preferred), or ensure they are referenced via `${VAR}` where appropriate.
- Re-run the script until it reports full coverage.

6. Verify compose model and runtime
- Validate merged Compose model first:
```bash
docker compose -f <compose-file> config
```
- Build and start services:
```bash
docker compose -f <compose-file> up --build
```
- Confirm containers start and Angular app is reachable at the configured port.
- If runtime verification cannot be executed (for example Docker engine unavailable), report that clearly with the exact blocker.

## Guardrails

- Do not silently ignore missing variables.
- Do not rely on implicit assumptions about `.env` loading behavior.
- Keep variable names consistent across `.env`, compose, and any build args.
- Preserve unrelated compose services and existing user configuration.
- Do not reorder or remove unrelated keys unless required for correctness.

## Script Behavior

`check_env_compose_coverage.py`:
- Detects compose file automatically unless overridden.
- Reads `.env` style files and extracts variable keys.
- Validates each key is covered in compose.
- Supports `referenced` mode (default) and `strict` mode.

Coverage definition:
- `referenced`: key is considered covered when compose references it (for example `${KEY}`), explicitly maps it in environment style lines, or includes the exact env file via `env_file`.
- `strict`: key is considered covered only when explicitly mapped in environment/argument style declarations.

## Definition of Done

- Dockerfile and compose are valid for Angular 20 deployment flow.
- Coverage script passes with requested mode.
- Compose config validation passes before runtime startup.
- User can run one deterministic verification command sequence for future changes.
