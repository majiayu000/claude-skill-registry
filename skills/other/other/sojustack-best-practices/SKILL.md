---
name: sojustack-best-practices
description: Best-practice guidance for the SojuStack monorepo (NestJS + Drizzle + Better Auth + TanStack Start). Use when editing files in apps/api or apps/web, designing routes, query/form patterns, auth/transaction flows, or implementing cross-stack features.
---

# SojuStack Best Practices

Use this skill to keep changes idiomatic and safe in this repository.

## Repository Map

- Backend: `apps/api/` (NestJS + Drizzle ORM + Better Auth)
- Frontend: `apps/web/` (TanStack Start + TanStack Query + TanStack Form + ShadCN/Base UI)
- Shared config: `packages/typescript-config/`

## Universal Rules

- Keep scope tight to the user request; avoid opportunistic refactors.
- Maintain strict typing; avoid `any` and unsafe casts.
- Match naming and folder conventions already used in the touched area.
- Prefer small reusable helpers over duplicate logic.
- If behavior changes, update/add tests for the impacted area.

## Frontend Rules (`apps/web`)

### Routing (TanStack Start)

- Keep route modules focused; move reusable logic to hooks or components.

### Data Fetching (TanStack Query)

- Use stable query keys like `['resource', id, 'sub-resource']`.
- Use `invalidateQueries()` without parameters when broad refresh is intended.
- Keep server-state logic in query/mutation hooks, not presentational components.

### UI (ShadCN + Base UI)

- Prefer components from `apps/web/src/components/ui/`.
- Prefer Base UI primitives over raw HTML where an equivalent exists.
- Use `cn()` from `apps/web/src/lib/utils.ts` for class composition.
- Keep Tailwind usage aligned with existing tokens and utility patterns.

## Backend Rules (`apps/api`)

### Database (Drizzle)

- Add tables in `apps/api/src/databases/tables/{name}.table.ts`.
- Export new tables from `drizzle.schema.ts`.
- Add/update relations in `drizzle.relations.ts`.

### Auth (Better Auth)

- Follow existing setup in `apps/api/src/auth/better-auth.provider.ts`.
- Use framework auth helpers (`@Auth()`, `@ActiveUser()`, `@ActiveSession()`) rather than ad hoc request parsing.

### Transactions

- Use `@Transactional()` with `TransactionHost<DrizzleTransactionClient>`.
- Do not manually nest/start transactions via `tx.transaction()`.

### Services and Errors

- Keep controllers thin; place business logic in services or providers.
- Use NestJS exceptions (`NotFoundException`, `UnauthorizedException`, etc.) for expected failures.

### API Type Safety

- Treat `apps/api/generated/openapi.d.ts` as generated source of truth for E2E typing.
- Use existing DTO and serialization patterns in the module.

## Execution Workflow

1. Read nearby code and existing module patterns.
2. Implement the smallest correct change.
3. Run repository validation commands from the repo root:
   - `pnpm typecheck`
   - `pnpm format`
   - `pnpm lint`
4. If any of those commands fail, fix the issues and re-run until they pass.
5. Ensure unrelated files are not modified.
6. Report what changed, why, and how it was validated.

## Do / Don't

### Do

- Prefer simplicity and human readability of code over complex or verbose implementations.
- Heir on asking more questions rather than too little.
- Beware of premature optimization
- Reuse existing providers/utilities before adding abstractions.
- Keep functions cohesive and predictable.
- Add short comments only for non-obvious logic.

### Don't

- Introduce architectural shifts unless requested.
- Add dependencies when existing stack primitives are sufficient.
- Bypass validation, auth, or typing conventions.
