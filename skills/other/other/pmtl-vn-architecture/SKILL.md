---
name: pmtl-vn-architecture
description: architecture and implementation guide for the pmtl_vn stack using next.js 16, nestjs, postgres, caddy, docker compose, and session-based auth. use when creating, extending, reviewing, refactoring, or deploying this monorepo; when adding auth, roles, access control, search, docker/caddy setup, or domain features; and when the agent must preserve the repo's ai-friendly conventions, boundaries, and file placement rules.
---

# PMTL_VN Architecture

## Overview
Use this skill to keep work aligned with the real PMTL_VN architecture. It is for building new features, reviewing/refactoring code, evolving auth and access control, wiring search, and maintaining Docker/Caddy deployment without breaking monorepo boundaries or file conventions.

## Use When

- Creating, extending, or refactoring PMTL features across app boundaries.
- Changing auth, access control, search, deployment, or runtime service ownership.
- Reviewing placement decisions when multiple layers could own the work.

## Expected Output

- Code placed in the narrowest correct layer.
- Architecture changes documented in the same task when contracts move.

The current stack assumptions are:
- `apps/web` is Next.js 16 App Router
- `apps/api` is NestJS backend authority (business logic, auth, OpenAPI)
- `apps/admin` is custom admin frontend
- PostgreSQL is the primary database (source of truth)
- **Phase 1**: SQL/API search (tsvector/ILIKE); **Phase 2+**: Meilisearch
- Caddy terminates SSL and reverse proxies services
- Docker Compose is the operational boundary
- **Phase 2+**: Valkey, BullMQ workers, outbox_events — only when measured need

## Core Rules
Follow these rules on every task:
- Preserve the monorepo split: `apps/web`, `apps/api`, `apps/admin`, `packages/*`, `infra/*`, `docs/*`
- Keep web feature-first
- Keep NestJS modules clean: module + controller + service + dto + entities
- Keep `packages/shared` framework-agnostic: types, enums, zod schemas, constants, validators, mappers, pure utils only
- Do not move business logic into Next route/page files or admin configs
- Introduce Valkey, BullMQ, workers only when there is a concrete production need, and document the runtime contract
- In `apps/web`, prefer Next.js 16 `cacheComponents` with `"use cache"` helper functions over route-level `revalidate` or `unstable_cache`
- In `apps/web`, request-boundary logic belongs in `src/proxy.ts` for Next.js 16; do not blindly migrate to `middleware.ts`
- Prefer clear, maintainable code over clever abstractions
- When audit documents disagree, treat `AUDIT_VERIFIED_2026.md` as the checked baseline and older audits as hypotheses to validate
- Update docs and env examples when architecture, contracts, or runtime requirements change
- If you change project rules or AI-coding conventions, update the corresponding docs and skill files in the same task

## Repo Shape
Assume this structure unless the user explicitly changes it:
- `apps/web`: Next.js 16 frontend
- `apps/api`: NestJS backend authority
- `apps/admin`: Custom admin frontend
- `packages/ui`: optional shared UI
- `packages/shared`: pure shared domain code
- `packages/config`: shared eslint/typescript/prettier config
- `infra/docker`: compose files and env examples
- `infra/caddy`: Caddyfile and related files
- `infra/scripts`: deploy and backup scripts
- `docs/architecture`: decisions, domains, conventions, deployment
- `docs/api`: contracts
- `design/`: architecture design source of truth

Consult `references/repo-conventions.md` for placement and layering rules.

## Task Routing
### When working on web
Use `apps/web` and keep code feature-first.
Typical placement:
- pages/routes/layouts/loading/error/meta in `src/app`
- feature code in `src/features/<domain>`
- cross-feature web helpers in `src/lib`
- shared visual primitives in `src/components`

For auth in web:
- prefer `features/auth/*`
- add route protection in `proxy.ts` or the least invasive server-side guard that fits the existing setup
- treat `apps/api` as the auth authority

### When working on api (NestJS)
Use `apps/api` and keep modules focused and clean.
Per module/domain, prefer:
- `{module-name}.module.ts`: NestJS module declaration
- `{module-name}.controller.ts`: route handlers
- `{module-name}.service.ts`: business logic
- `dto/`: input/output DTOs with Zod validation
- `entities/`: Prisma entity types
- `guards/`: route guards if module-specific

Platform modules go in `apps/api/src/platform/`:
- sessions, audit, feature flags, rate limit, storage, health, metrics

### When working on shared domain code
Use `packages/shared` only for framework-agnostic code:
- `constants`
- `enums`
- `schemas`
- `types`
- `validators`
- `mappers`
- pure `utils`

Do not import Next.js internals, NestJS internals, or runtime-only server utilities here.

### When working on infra or deployment
Use:
- `infra/docker` for compose files and env examples
- `infra/caddy` for reverse proxy and SSL config
- `infra/scripts` for deployment and DB backup scripts
- GitHub Actions for build/push/deploy automation

Prefer the production model:
- build images locally or in CI
- push to registry
- VPS only pulls and runs containers

## Auth Strategy
NestJS (`apps/api`) is the auth authority using session-based auth with Argon2id password hashing.

Required assumptions:
- auth lives in `apps/api/src/modules/auth/`
- web calls API for auth operations
- session strategy uses httpOnly cookies with refresh token rotation
- do not add Auth.js, Better Auth, or a second auth authority unless the user explicitly asks for it

Typical auth scope:
- register
- login
- logout / logout-all
- forgot password
- reset password
- current user / session
- role-based access
- protected routes
- user profile basics

Default roles:
- `super_admin`
- `admin`
- `member`

Consult `design/01-identity/` for auth and identity design.

## Search Strategy
**Phase 1** (current): SQL/API search using PostgreSQL tsvector or ILIKE.
**Phase 2+**: Meilisearch is the preferred search engine when `search.meilisearch.enabled` feature flag is on.

Keep search concerns separated:
- search service in `apps/api/src/modules/search/`
- search UI and query composition in web features
- shared search DTOs or schemas in `packages/shared`

Do not expose Meilisearch publicly unless explicitly intended. Prefer internal network access behind API services.

## Phase Model
### Phase 1
Supported and preferred:
- Next.js 16 web
- NestJS backend authority (`apps/api`)
- PostgreSQL
- SQL/API search (tsvector/ILIKE)
- Caddy
- Docker Compose dev/prod
- Session-based auth via NestJS
- docs/conventions/contracts maintenance

### Phase 2+ (Operational Expansion)
Add when the production runtime benefits clearly justify the added complexity:
- Meilisearch (search.meilisearch.enabled)
- Valkey (cache)
- BullMQ worker service
- outbox_events + dispatcher
- monitoring dashboards
- alerting
- log aggregation
- backup automation beyond simple scripts

## Security Baseline
Always preserve these defaults:
- least privilege access control
- guest access only to public content
- protect admin/moderation areas by role
- keep secrets in env, not code
- keep Postgres and Valkey internal-only unless explicitly exposed
- keep Meilisearch internal-only unless explicitly exposed
- use Caddy for TLS termination and reverse proxy
- add limits and guardrails to sensitive routes when implementing auth, comments, abuse reporting, or search

Consult `design/baseline/` for security and infrastructure design.

## Documentation Duties
When you change behavior or architecture, update docs as part of the same task when appropriate:
- `README.md` for run/build/deploy changes
- `design/` for architecture design changes
- `docs/architecture/` for implementation conventions
- `docs/api/` for request/response or auth contract changes
- `.env.example` or env example files for runtime configuration changes

## Verification

- Recheck the chosen file placement against `references/repo-conventions.md`.
- If service boundaries or public/private exposure changed, recheck the relevant security and deployment references.
- Pair with `pmtl-verify-quality-gate` after meaningful implementation changes.

## Recommended Working Style
When given a task:
1. Read the architecture docs the repo points to first.
2. Identify the domain and the correct layer.
3. Place new code in the narrowest correct location.
4. Keep NestJS modules clean: thin controllers, business logic in services.
5. Keep feature code grouped by domain in web.
6. Preserve type safety without over-engineering.
7. Explain file placement and architectural choices briefly when useful.
8. Do not introduce broad refactors unless they are required.

## Common Good Decisions
- Put auth UI and fetch helpers under `apps/web/src/features/auth`
- Put ownership/moderation logic in NestJS services, not only controller guards
- Put DTO validation in `packages/shared/src/schemas`
- Put search logic in `apps/api/src/modules/search/`
- Put deploy and backup logic under `infra/scripts`
- Put Docker/Caddy changes under `infra/*` and document them

## Common Bad Decisions
- Mixing framework internals into `packages/shared`
- Putting all module logic inside a single controller file
- Adding Valkey/BullMQ without a concrete runtime use case or deployment plan
- Adding a second auth system without a clear reason
- Building production images directly on the VPS by default
- Exposing internal services publicly without an explicit need

## References
- For repo layout and file placement, read `references/repo-conventions.md`
- For auth, access, and security defaults, read `references/auth-and-security.md`
- For Docker, Caddy, deployment, and service boundaries, read `references/deploy-and-ops.md`
- For architecture design source of truth, read `design/DECISIONS.md`
