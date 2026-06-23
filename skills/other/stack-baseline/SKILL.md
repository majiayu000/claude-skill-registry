---
name: stack-baseline
description: The pinned default technology stack for SMB Product-Builder products. One source of truth so the architect, app-scaffolder, auth-engineer, and senior-dev never re-decide the stack per build — they build ON it. Covers framework, ORM/DB, auth, UI, payments/email/SMS, files, jobs, testing, hosting, and observability, with the chosen default + the one sanctioned alternative for each. Applied whenever a new product is scaffolded or a stack choice would otherwise be improvised. Re-deciding the stack every build is the biggest silent time sink; this kills it.
when_to_use: |
  Apply when:
  - architect writes the Components / stack section of ARCH-{slug}.md
  - app-scaffolder stands up a new product skeleton
  - auth-engineer or senior-dev would otherwise pick a library/provider ad hoc
  Do NOT override a choice already pinned in PROJECT.md (an existing project's stack wins).
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - ".great_cto/**"
---

# Stack baseline — decide once, build on it

Every SMB product builds on the SAME proven stack unless there's a concrete reason not to.
Re-deciding framework/ORM/auth/host per build wastes the first hour of every project and
fragments the codebase across products. **This is the default; deviate only with a written
reason in ARCH.**

## The pinned stack

| Layer | Default | Sanctioned alternative | Notes |
|---|---|---|---|
| **Framework** | Next.js (App Router, TS) | Remix | Server actions + RSC; one repo front+back |
| **UI** | Tailwind + shadcn/ui | — | matches the site; design-advisor tokens map to it |
| **DB** | Postgres | — | the only DB; integer cents, tz-aware timestamps |
| **ORM / migrations** | Drizzle | Prisma | typed schema + SQL migrations; migration-ready-schema applies |
| **Auth** | Auth.js (NextAuth v5) | Clerk (fast path, per-MAU cost) | owned by **auth-engineer**; session + RBAC + multi-tenant |
| **Payments** | Stripe (+ Connect) | — | owned by subscription-billing-engineer / integrations-engineer |
| **Email** | Resend | Postmark | transactional; SPF/DKIM/DMARC via lifecycle-messaging |
| **SMS** | Twilio (Messaging Service) | Telnyx | 10DLC; consent via lifecycle-messaging |
| **File storage** | Cloudflare R2 / S3 | — | private buckets, presigned URLs |
| **Background jobs** | Inngest | a Postgres-backed queue | reminders, syncs, dunning |
| **Testing** | Vitest (unit) + Playwright (e2e) | — | senior-dev unit; e2e-test-engineer browser |
| **Hosting** | Vercel | Cloudflare Pages/Workers | Next.js-native; preview per PR |
| **DB host** | Neon (serverless PG) | Supabase | branchable; env-wired by infra-provisioner |
| **Observability** | Sentry | — | errors + traces on the deployed product |
| **Analytics** | privacy-light (Plausible) | — | no heavy 3rd-party trackers |

## Rules

1. **One framework, one DB, one ORM, one auth lib** across all products. Consistency >
   per-product optimization.
2. **Pin it in `.great_cto/PROJECT.md`** at scaffold time (`stack:` line) so every later
   agent reads it instead of guessing — and an existing PROJECT.md's stack always wins.
3. **Money in integer cents; timestamps tz-aware; IDs are stable** (compose with
   `migration-ready-schema`).
4. **Auth, payments, email/SMS, jobs are owned by their specialist** (auth-engineer,
   billing/integrations, lifecycle-messaging) — this skill only names the default library;
   the specialist owns the contract.
5. **Deviation needs a written reason** in ARCH's Components section (e.g. "Clerk over Auth.js
   because the customer needs SSO/SCIM on day one").

## Output

When applied, write the stack into ARCH's Components section and PROJECT.md:

```
## Stack (baseline)
framework: Next.js (App Router, TS) · UI: Tailwind + shadcn
db: Postgres (Neon) · orm: Drizzle · auth: Auth.js (→ auth-engineer)
payments: Stripe · email: Resend · sms: Twilio · files: R2 · jobs: Inngest
test: Vitest + Playwright · host: Vercel · obs: Sentry
deviations: <none | reason>
```
