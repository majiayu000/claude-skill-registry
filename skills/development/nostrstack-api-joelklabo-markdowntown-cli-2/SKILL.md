---
name: nostrstack-api
description: Nostrstack API development (Fastify + Prisma) including routing patterns, services, tenancy resolution, LightningProvider integration, and Nostr endpoints. Use when editing apps/api (routes, services, providers, Prisma schema, OpenAPI) or adding API features/tests.
---

# Nostrstack API

Use this skill when working inside `apps/api`.

## Workflow

- Read `references/architecture.md` for system context and data flow.
- Consult `references/api-structure.md` for code layout and key files.
- For Nostr endpoints or ID parsing, also read `references/nostr.md`.
- Update or add tests per `references/testing.md`.

## Guardrails

- Keep tenant resolution consistent (`tenant-resolver.ts` and host/domain rules).
- Lightning provider changes must preserve webhook/payment flow and retry behavior.
- Ensure Prisma migrations and seeds stay aligned with schema changes.

## When to add docs

- If routes or response shapes change, update `apps/api/openapi.json` and relevant docs.
