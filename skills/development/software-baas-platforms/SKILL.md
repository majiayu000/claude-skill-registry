---
name: software-baas-platforms
description: "Chooses managed backend platforms such as Supabase, Convex, and Firebase. Use when comparing database, auth, realtime, and backend-service tradeoffs."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Managed App Backends

Use this skill to choose between managed app-backend platforms when the real decision is not just "which database," but which product backend bundle should own auth, data, realtime, storage, server-side functions, and early operational tradeoffs.

This skill covers:

- SQL-first and NoSQL-first managed backend platform choice
- auth, permissions, and data-ownership model tradeoffs
- realtime sync and offline behavior differences
- self-hosted versus hosted operational tradeoffs
- migration and exit paths when a platform stops fitting

## Quick Reference

| Need | Default path | Notes |
|------|--------------|-------|
| Postgres-first product backend with RLS, auth, storage, and realtime | Supabase | Best fit when SQL portability and browser-safe Postgres workflows matter |
| TypeScript-first reactive backend with durable workflows | Convex | Best fit when live subscriptions and function-centric app logic matter more than SQL |
| Mobile/offline-first app with mature client SDKs | Firebase / Firestore | Strong default when device sync and mobile SDK ergonomics dominate |
| Self-hosted full backend bundle with auth, DB, storage, and functions | Appwrite | Good fit when self-hosting is a first-order requirement |
| Small single-binary app backend or internal tool | PocketBase | Good fit for prototypes and lightweight deployments, not the default for high-criticality systems; still pre-1.0 — verify current version and breaking-change posture before betting production on it |
| Pure Postgres host without a bundled auth/storage/realtime layer | Neon or PlanetScale Postgres | Use when you want serverless Postgres (branching, scale-to-zero) but plan to build auth/storage/realtime yourself or already own them elsewhere; not a like-for-like Supabase substitute |
| Complex compliance, bespoke domain logic, or multi-service boundaries | [../software-backend/SKILL.md](../software-backend/SKILL.md) + [../software-database-design/SKILL.md](../software-database-design/SKILL.md) | Use custom services when you need stronger control than a BaaS can provide |
| Picking the **compute host** (Vercel, Fly.io, Railway, Render, Cloudflare Workers, Deno Deploy) | [../software-paas-hosting/SKILL.md](../software-paas-hosting/SKILL.md) | Sibling skill for the compute layer; this skill is data/auth-layer only |

## Default Workflow

1. Identify the dominant constraint: SQL portability, reactive UX, mobile/offline sync, self-hosting, or speed to first product.
2. Decide whether the platform should own auth, storage, and server-side logic or only the database.
3. Choose the simplest platform that matches the product shape without hiding the security model.
4. Validate the exit path before committing: schema portability, auth migration, storage migration, and server-side workflow replacement.
5. If the app has outgrown the platform boundary, move the hot path into custom backend services instead of stretching the platform indefinitely.

## ASCII Flow

```text
BaaS platform decision
  -> Identify app shape, data model, auth, realtime, and ops needs
  -> Compare managed platform defaults against lock-in and scale risks
  -> Decide system-of-record boundary and exit path
  -> Design auth, data ownership, migrations, and runbooks
  -> Verify current vendor limits, pricing, and product changes
  -> Recommend platform, rejected options, and proof plan
```

## Platform Selection Rules

| Platform | Primary Signal | Security Starting Point |
|----------|----------------|------------------------|
| Supabase | Postgres as source of truth; SQL, RLS, Realtime, Auth, Storage, Edge Functions in one stack | Schema design + RLS policy quality |
| Convex | TypeScript-heavy interactive product; queries, mutations, actions, subscriptions, durable workflows | Function boundaries, auth propagation, server-owned writes |
| Firebase / Firestore | Offline-first; mature mobile/web SDKs; client-driven sync more important than SQL portability | Rules quality, offline conflict expectations, client trust boundaries |
| Appwrite | Self-hosting first; project-level permissions; integrated auth/DB/functions/storage | Hosting model, admin surface exposure, secrets isolation |
| PocketBase | Extremely small deployment; operational simplicity over ecosystem depth, HA, or long-term guarantees | Admin surface exposure; not for high-criticality systems |
| Custom backend | Complex compliance, highly specific domain services, independent scaling across services | Use [../software-backend/SKILL.md](../software-backend/SKILL.md) + threat model |

If the team cannot clearly explain who is allowed to read and write each record, do not pick the platform yet.

**Supabase vs. Firebase, as an actual decision (not a preference)**: pick Supabase/Postgres+RLS when the team already thinks in SQL, needs ad-hoc joins/reporting, or wants a schema that is trivially portable to any Postgres host (RDS, Neon, PlanetScale, self-hosted). Pick Firebase/Firestore when the product is mobile-first, needs best-in-class offline sync and conflict resolution out of the box, and the data shape is naturally document-like with shallow queries. The tie-breaker is usually query complexity: complex relational queries and reporting favor Supabase; simple per-document reads/writes at high device-offline tolerance favor Firebase. Do not decide this on team familiarity alone — RLS policy bugs and permissive Firestore rules are both common breach vectors, so budget real review time either way.

## Operational Gotchas

Critical production patterns documented from real incidents. See [references/platform-comparison.md](references/platform-comparison.md) for full details.

- **PostgREST-style filter APIs can hit URL or proxy length limits** when large ID lists are serialized into query parameters. Batch aggressively and verify the deployed edge limit before assuming giant `.in()` filters are safe.
- **Admin and user-list APIs are usually paginated**. Never assume a single call enumerates the full tenant; check current page-size defaults and iterate explicitly.
- **Egress/bandwidth overages are a recurring hidden-cost trap**, not a rounding error, on Postgres-hosted BaaS (Supabase, Neon, PlanetScale): media-heavy or high-read apps can blow past included egress allowances quickly, and the per-GB overage rate is a volatile, frequently-revised number. Model expected monthly egress (database + storage + cached vs. uncached) before committing, and verify the current allowance and $/GB rate at the platform's official pricing page — do not rely on a remembered figure.

## When To Use This Skill

Use this skill when the user asks:

- "Should I use Supabase or Convex?"
- "Is Firebase still the better choice for this app?"
- "What is the best managed backend for a startup MVP?"
- "Should I keep Supabase or move to a custom backend?"
- "How do Appwrite and PocketBase compare to Supabase?"

## When NOT To Use This Skill

- Native iOS app skeletons that explicitly want iCloud/CloudKit instead of Supabase, Vercel, Firebase, or another backend platform -> [software-ios-native](../software-ios-native/SKILL.md).
- Apple-only private user data synced through SwiftData/Core Data + CloudKit -> [software-ios-native](../software-ios-native/SKILL.md).
- On-device Apple Foundation Models, local semantic search, or iOS-local retrieval/vector storage -> [software-ios-ai-engine](../software-ios-ai-engine/SKILL.md).
- App Intents, Siri, Spotlight, widgets, controls, or Apple Intelligence system exposure for a native iOS app -> [software-ios-native](../software-ios-native/SKILL.md), then [software-ios-ai-engine](../software-ios-ai-engine/SKILL.md) if local AI is involved.

## Pre-Commit Checklist

Before committing to a BaaS platform, verify:

- [ ] Permission model documented: who can read and write each record type
- [ ] Security model tested: two isolated tenants or users cannot access each other's data
- [ ] Exit path audited: schema portability, auth migration, storage migration, client-SDK lock-in assessed
- [ ] Compliance requirements mapped: no pending compliance gap that requires custom service boundaries
- [ ] Operational budget confirmed: self-hosted option has budget for upgrades, backups, monitoring, secrets rotation
- [ ] Server-owned writes identified: writes that must not originate from client code are protected at the platform layer

## Known Traps

- Choosing a platform from a feature checklist without first validating its permission model, trust boundaries, and operator responsibilities.
- Assuming an exit path is cheap because the underlying database looks portable, while ignoring auth, storage, realtime, function, and client-SDK coupling.
- Stretching a managed platform into compliance-heavy or domain-heavy workflows that need custom service boundaries.
- Picking self-hosting as the “safer” answer without budgeting for upgrades, secrets handling, backups, monitoring, and operational ownership.
- Letting frontend convenience determine the backend boundary before deciding which writes must stay server-owned.
- Sizing total cost of ownership on the advertised plan price alone while ignoring egress, compute add-ons, and overage rates that materially change the real bill at scale.

## Common Anti-Patterns

- Treating BaaS adoption as a permanent architecture commitment instead of a product-speed tradeoff with explicit revisit points.
- Rebuilding missing backend behavior inside edge functions and client code until the platform effectively becomes an unmanaged custom backend.
- Using broad service-role or admin credentials to bypass the platform security model rather than fixing policy design.
- Comparing Supabase, Convex, Firebase, Appwrite, and PocketBase as if they are interchangeable database choices rather than opinionated backend bundles.
- Defaulting to the platform with the best developer demo instead of the one with the cleanest long-term ownership and migration story.

## Scenarios

Recipes keyed to platform-selection or integration moments. Each lists the shortest path to a correct, safe implementation.

### S1 — Supabase RLS for multi-tenant SaaS

1. Add a `tenant_id` column (FK to `tenants`) to every data table; never rely on application-layer filtering alone.
2. Enable RLS on each table: `ALTER TABLE foo ENABLE ROW LEVEL SECURITY;`.
3. Write a `SELECT` policy: `USING (tenant_id = auth.jwt() ->> 'tenant_id')` — verify the JWT claim exists for every auth path.
4. Repeat for `INSERT`, `UPDATE`, `DELETE` policies; never leave a table with RLS enabled but no policy (blocks all access).
5. Test with two separate authenticated users: confirm cross-tenant data is invisible. See [references/security-and-ownership-models.md](references/security-and-ownership-models.md).
6. Add a CI integration test that asserts a tenant-B token cannot read tenant-A rows.

### S2 — Convex action vs mutation routing

1. Identify whether the operation reads/writes Convex tables only, or calls an external service or API.
2. Use a **mutation** for pure Convex reads/writes: transactional, deterministic, retryable by the runtime.
3. Use an **action** for any external I/O (HTTP calls, third-party APIs, file uploads); actions are not transactional.
4. From an action, call internal mutations to persist results; never write to the database directly in an action.
5. Verify scheduling: use `ctx.scheduler.runAfter` inside mutations for deferred work; do not spawn actions ad-hoc from the client.

### S3 — Firebase rules + App Check for mobile-only client

1. Enable App Check with the appropriate attestation provider (Play Integrity on Android, App Attest on iOS).
2. In Firebase console, enforce App Check for Firestore and Storage — unverified clients are blocked at the platform level.
3. Write Firestore security rules that restrict reads/writes to `request.auth.uid == resource.data.userId`.
4. Add `allow read, write: if false;` as the default catch-all at the top of every collection group not explicitly covered.
5. Test rules with the Firebase Emulator Suite: run the rules unit-test suite on every PR. See [references/security-and-ownership-models.md](references/security-and-ownership-models.md).

### S4 — BaaS-to-self-hosted exit plan trigger

1. Identify the exit trigger: vendor pricing change, compliance requirement, or outgrown platform boundary.
2. Audit coupling: schema portability, auth migration path, storage bucket ownership, edge function replacement, client SDK lock-in.
3. For Supabase: export schema via `pg_dump`; migrate auth users with the Supabase admin API; replicate storage objects to S3-compatible storage.
4. Run the self-hosted stack in parallel for 2 weeks; verify parity on auth flows, realtime subscriptions, and RLS behavior.
5. Cut over DNS/config; decommission the managed instance after a 30-day retention window. See [references/migration-exit-strategies.md](references/migration-exit-strategies.md).

### S5 — Per-platform secrets boundary

1. Never commit service-role keys or admin credentials to the repo; use environment variables in the deployment platform.
2. For mobile clients: use Supabase `anon` key + RLS, or Firebase `apiKey` + rules — these are intentionally public-facing but constrained by policy.
3. For server-side operations (webhooks, admin tasks): use service-role or admin credentials only in backend functions, never in client bundles.
4. Rotate secrets after any suspected exposure; verify rotation does not break existing auth sessions before cutting over.
5. Document required env vars in the sibling YAML with descriptive placeholders; never real values.

## Navigation

**References**
- [references/platform-comparison.md](references/platform-comparison.md) - platform fit, data model, and strongest-use-case matrix
- [references/security-and-ownership-models.md](references/security-and-ownership-models.md) - RLS, function auth, rules engines, and permission surfaces
- [references/migration-exit-strategies.md](references/migration-exit-strategies.md) - signals that a platform no longer fits and practical exit paths
- [references/aws-bedrock-as-agent-baas.md](references/aws-bedrock-as-agent-baas.md) - AWS Bedrock AgentCore as a BaaS-for-agents: primitives, platform fit, and pairing
- [data/sources.json](data/sources.json) - official platform docs and supporting primary sources

**Related Skills**
- [../software-database-design/SKILL.md](../software-database-design/SKILL.md) - schema shape, migrations, and relational/document modeling
- [../software-backend/SKILL.md](../software-backend/SKILL.md) - custom backend services when a managed platform is no longer enough
- [../software-realtime/SKILL.md](../software-realtime/SKILL.md) - transport and collaboration decisions after platform choice
- [../software-mobile/SKILL.md](../software-mobile/SKILL.md) - mobile product delivery and offline-first client decisions
- [../software-ios-native/SKILL.md](../software-ios-native/SKILL.md) - Apple-native iOS app skeletons, SwiftData/Core Data, CloudKit/iCloud, App Intents, and release gates
- [../software-ios-ai-engine/SKILL.md](../software-ios-ai-engine/SKILL.md) - Apple Foundation Models, on-device local AI, and iOS-local retrieval/vector search
- [../software-security-appsec/SKILL.md](../software-security-appsec/SKILL.md) - secure design, auth, and secrets handling

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Start from `data/sources.json` for the platform's official docs.
- Verify current auth, realtime, storage, branching, deployment, self-hosting, and durability claims before platform-specific recommendations.
- Prefer official documentation over launch tweets or comparison blog posts.
- If web access is unavailable, mark platform-specific guidance as potentially stale.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
