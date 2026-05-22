---
name: docker-architect
description: SOTA Docker/Compose architecture, implementation, refactor, and security hardening. Use when working on containerization tasks such as creating or rewriting Dockerfiles, docker-compose files, buildx/bake configs, .dockerignore, and CI pipelines for build/test/scan/publish; auditing existing container setups for security, correctness, size/perf, and best practices (least privilege, non-root, minimal images, pinned base images, BuildKit secrets, healthchecks); debugging Docker build/run issues; or designing dev vs prod compose workflows across services (DB/cache/queues) with correct networking, volumes, secrets, and resource limits.
---

# Docker Architect

## Overview

Produce production-grade, secure, right-sized Docker images and Compose environments end-to-end: inventory → design → implement → test → CI. Prefer minimal, reproducible builds (multi-stage + BuildKit) and least-privilege runtime defaults.

## Quick Start (always do this first)

1. Inventory the repo and existing container config:
   - Run `python3 /home/bjorn/.codex/skills/docker-architect/scripts/docker_inventory.py --root .`
2. Choose the target:
   - **New containerization** → follow “New build workflow”
   - **Existing Dockerfiles/Compose** → follow “Audit + refactor workflow”
3. Validate locally:
   - `docker buildx version`
   - `docker buildx build ...` (or `docker build ...`)
   - `docker compose config` and `docker compose up --build`

Template rendering example (edit variables per repo):

- `python3 /home/bjorn/.codex/skills/docker-architect/scripts/render_template.py --template .dockerignore --out .dockerignore`
- `python3 /home/bjorn/.codex/skills/docker-architect/scripts/render_template.py --template compose/docker-compose.yml --out docker-compose.yml --var IMAGE_NAME=myapp:dev --var HOST_PORT=8000 --var CONTAINER_PORT=8000`
- `python3 /home/bjorn/.codex/skills/docker-architect/scripts/render_template.py --template compose/docker-compose.dev.yml --out docker-compose.dev.yml --var CONTAINER_PORT=8000 --var DEV_COMMAND='[\"python\",\"-m\",\"uvicorn\",\"myapp.api:app\",\"--host\",\"0.0.0.0\",\"--port\",\"8000\",\"--reload\"]'`

## Workflow Decision Tree

1. Scope:
   - **Dev-only** (fast iteration, source mounts, hot reload) → prefer `docker-compose.dev.yml`
   - **Prod-like** (immutable images, healthchecks, least privilege) → prefer `docker-compose.yml` + `docker-compose.prod.yml`
2. Artifact type:
   - **Single service** → one Dockerfile + optional compose for deps
   - **Multi-service** → compose with explicit networks/volumes and healthchecks
3. Publish target:
   - **Local only** → keep simple; optional CI smoke checks
   - **Registry publish** → add CI build/test/scan/push + provenance/SBOM (if available)

## New build workflow (Dockerfile + .dockerignore + compose)

1. Pick a base strategy (see `references/dockerfile_patterns.md`):
   - Multi-stage build; runtime image is minimal; build tools stay in builder stage.
   - Prefer slim/distroless where feasible; default to non-root user.
2. Add `.dockerignore` early (template in `assets/templates/.dockerignore`).
3. Create a Dockerfile from templates:
   - Prefer `assets/templates/python/Dockerfile.uv` for modern Python/`uv`
   - Prefer `assets/templates/node/Dockerfile.pnpm` for Node + pnpm
   - Use `python3 /home/bjorn/.codex/skills/docker-architect/scripts/render_template.py ...` to render with variables.
4. Add a compose file for dependencies (DB/cache) and dev/prod profiles:
   - Start from `assets/templates/compose/docker-compose.yml` + an override (`assets/templates/compose/docker-compose.dev.yml` or `assets/templates/compose/docker-compose.prod.yml`)
   - Optional deps file: `assets/templates/compose/docker-compose.deps.yml`
5. Local validation:
   - `bash /home/bjorn/.codex/skills/docker-architect/scripts/smoke_test_container.sh --help`
   - Optional: `--build-check` (Docker build checks) and `--pull` (fresh base images)
   - For compose: `bash /home/bjorn/.codex/skills/docker-architect/scripts/smoke_test_compose.sh --help`

## Audit + refactor workflow (existing Dockerfiles/Compose)

1. Inventory + static audit:
   - `python3 /home/bjorn/.codex/skills/docker-architect/scripts/docker_audit.py --root .`
2. Identify high-risk issues (see `references/security_hardening.md`):
   - Secrets in image/build args, root/privileged runtime, overly broad mounts, host networking, “latest” tags, missing healthchecks.
3. Refactor incrementally:
   - Keep behavior stable, then tighten (non-root, read-only fs, drop caps, pin images, shrink layers).
4. Validate end-to-end:
   - `docker buildx build ...`
   - `docker compose up --build` and run the app’s normal test/health commands.
5. Produce a concise report (template in `references/review_template.md`).

## CI integration workflow (GitHub Actions default)

1. Start from `assets/templates/ci/github-actions-docker-ci.yml`.
   - For publish + SBOM/provenance to GHCR: `assets/templates/ci/github-actions-docker-publish.yml`
2. Ensure CI runs:
   - `docker buildx build` (cache enabled)
   - `docker compose config` (compose validation)
   - optional: build checks (`docker build --check`) and scan/SBOM/provenance steps
3. Prefer pinned action versions and least-privilege permissions (see `references/ci_github_actions.md`).

## “Latest/correct” research rule (do not guess)

When “latest” matters (base images, distro versions, language runtimes, CVEs):
1. Use Exa to confirm current official guidance and tags (official sources preferred).
2. Use `docker buildx imagetools inspect <image:tag>` to confirm manifests/platforms.
3. If unsure, mark as `UNVERIFIED` and propose a safe default with a verification step.

## Tooling leverage (when it helps)

- **Exa**: find current best practices, base image changes, CVE guidance, GitHub Actions deprecations.
- **Context7**: confirm framework-specific build outputs (e.g., Next.js, FastAPI, uvicorn/gunicorn, etc.).
- **Zen**: use `zen.secaudit` for a structured container/security audit and `zen.analyze` for architecture-sensitive compose design.
- **gh_grep**: search public repos for battle-tested patterns (entrypoints, healthchecks, buildx/bake, compose profiles).
- **opensrc**: inspect dependency internals when container behavior depends on packaging details.

## Bundled resources

### Scripts

- `scripts/docker_inventory.py`: detect stack + existing Docker/Compose files.
- `scripts/docker_audit.py`: heuristic linting of Dockerfiles/Compose for security/correctness.
- `scripts/render_template.py`: render templates with `{{VARS}}` into repo files.
- `scripts/smoke_test_container.sh`: build/run basic health check locally.
- `scripts/smoke_test_compose.sh`: validate + bring up compose and check health.

### References (load as needed)

- `references/dockerfile_patterns.md`: BuildKit, caching, multi-stage, runtime hardening.
- `references/compose_patterns.md`: compose patterns, profiles, healthchecks, secrets/configs.
- `references/security_hardening.md`: least privilege, capabilities, read-only fs, supply chain.
- `references/ci_github_actions.md`: CI build/test/scan/publish patterns.
- `references/review_template.md`: audit report format and deliverables checklist.

### Assets (templates)

Templates live under `assets/templates/` (Dockerfile variants, compose variants, CI workflow, `.dockerignore`, `docker-bake.hcl`).
