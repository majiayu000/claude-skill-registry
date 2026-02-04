---
name: treido-rails
description: Treido non-negotiables and safety rails. Use for pause conditions (DB/auth/payments), security/PII rules, i18n, Tailwind token rails, and caching constraints.
---

# treido-rails

Small set of invariants that should hold across the repo, regardless of which feature you’re changing.

## When to Apply

- Any time you touch Treido code
- Especially when work involves auth, data access, payments, caching, UI copy, or styling

## Always True (Non-Negotiables)

- **No secrets/PII in logs** (server or client). Don’t log headers/cookies/tokens/user objects.
- **All user-facing strings use `next-intl`**. Add keys to both `messages/en.json` and `messages/bg.json`.
- **Tailwind v4 tokens only**. No palette classes, gradients, arbitrary values, or hardcoded colors.
- **Default to Server Components**. Add `"use client"` only for hooks/events/browser APIs.
- **Cached server code must be pure**. In `'use cache'` functions: never touch `cookies()`, `headers()`, or auth.
- **Supabase queries select explicit fields** (avoid `select('*')` on hot paths).
- **Stripe webhooks must be signature-verified and idempotent**.

## Stop / Ask First (Pause Conditions)

**STOP and request human approval before:**

### Database Changes
- New tables or columns
- Column type changes
- Migration files
- RLS policy changes

### Security Changes
- Auth/access control logic
- Session handling
- Permission checks

### Payment Changes
- Stripe integration
- Billing logic
- Webhook handlers

### Data Operations
- Data deletion
- Data truncation
- Bulk updates

### External Integrations
- Adding new third-party APIs, OAuth flows, webhooks, or background jobs

## Repo Conventions (Stable)

- **Request entrypoint**: `proxy.ts` (do not add root `middleware.ts` unless explicitly requested)
- **Token SSOT**: `app/globals.css`
- **shadcn config**: `components.json`
- **Supabase migrations**: `supabase/migrations/*` (append-only mindset)

## Review Checklist

- No hardcoded user-facing strings (all via `next-intl`)
- No Tailwind rail violations (tokens only)
- No cached function touches request APIs (`cookies()`/`headers()`) or auth
- No wildcard selects (`select('*')`) in hot paths
- Webhooks: signature verification + idempotency + safe logging

## SSOT Documents (Stable Docs Live in /docs)

| Topic | Location |
|-------|----------|
| Agent entry point | `docs/AGENTS.md` |
| Workflow | `docs/WORKFLOW.md` |
| Product requirements | `docs/01-PRD.md` |
| Features | `docs/02-FEATURES.md` |
| Architecture | `docs/03-ARCHITECTURE.md` |
| Design system | `docs/04-DESIGN.md` |
| Routes | `docs/05-ROUTES.md` |
| Database | `docs/06-DATABASE.md` |
| API | `docs/07-API.md` |
| Payments | `docs/08-PAYMENTS.md` |
| Auth | `docs/09-AUTH.md` |
| i18n | `docs/10-I18N.md` |
