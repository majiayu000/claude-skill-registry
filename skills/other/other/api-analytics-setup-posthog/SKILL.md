---
name: api-analytics-setup-posthog
description: PostHog analytics and feature flags setup
---

# PostHog Analytics & Feature Flags Setup

> **Quick Guide:** One-time setup for PostHog in Next.js App Router monorepo. Covers `posthog-js` client provider, `posthog-node` server client, environment variables, and Vercel deployment. PostHog handles both analytics AND feature flags with a generous free tier (1M events + 1M flag requests/month).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `NEXT_PUBLIC_` prefix for client-side PostHog environment variables)**

**(You MUST create PostHogProvider as a 'use client' component - posthog-js requires browser APIs)**

**(You MUST call `posthog.shutdown()` or `posthog.flush()` after server-side event capture to prevent lost events)**

**(You MUST use `defaults: '2025-11-30'` or `capture_pageview: 'history_change'` for automatic SPA page tracking)**

**(You MUST use a single PostHog organization for all monorepo apps - projects are usage-based, not per-project pricing)**

</critical_requirements>

---

**Auto-detection:** PostHog setup, posthog-js, posthog-node, PostHogProvider, analytics setup, feature flags setup, event tracking setup, NEXT_PUBLIC_POSTHOG_KEY

**When to use:**

- Initial PostHog setup in a Next.js App Router project
- Configuring PostHogProvider for client-side analytics
- Setting up posthog-node for server-side/API route event capture
- Deploying to Vercel with PostHog environment variables

**When NOT to use:**

- Event tracking patterns (use `backend/analytics.md` for that)
- Feature flag usage patterns (use `backend/feature-flags.md` for that)
- Complex multi-environment setups with separate staging/production projects

**Key patterns covered:**

- PostHog project creation (single org for monorepo)
- Client-side setup with PostHogProvider
- Server-side setup with posthog-node
- Environment variables configuration
- Vercel deployment integration
- Initial dashboard recommendations

**Detailed Resources:**

- For code examples, see [examples/](examples/):
  - [core.md](examples/core.md) - Provider setup, layout integration, user identification
  - [server.md](examples/server.md) - Server client singleton, API routes, Hono middleware
  - [deployment.md](examples/deployment.md) - Environment variables, Vercel deployment
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

PostHog is a **product analytics + feature flags platform** that consolidates multiple tools into one. It's open-source, can be self-hosted, and has a generous free tier. For solo developers and small teams, PostHog eliminates the need for separate analytics (Mixpanel/Amplitude) and feature flag (LaunchDarkly) services.

**Core principles:**

1. **One platform for analytics + feature flags** - Reduces tool sprawl and cost
2. **Usage-based pricing** - Pay for what you use, not per-project
3. **Autocapture by default** - Automatic event tracking reduces manual instrumentation
4. **Server and client SDKs** - Full coverage for SSR and client-side apps

**When to use PostHog:**

- Need both analytics and feature flags in one platform
- Want generous free tier (1M events + 1M flag requests/month)
- Prefer open-source with self-host option
- Building product analytics (funnels, retention, sessions)

**When NOT to use PostHog:**

- Need advanced A/B testing with statistical rigor (use Statsig)
- Require real-time event streaming (use Segment)
- Need complex user journey mapping (use Amplitude)
- Already have established analytics + flag tools

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: PostHog Project Setup

Create a single PostHog organization for your monorepo. You can either use one project for all apps or create separate projects per app.

#### Organization Structure

```
PostHog Organization: "Your Company"
├── Project: "Main App" (or separate per app)
│   ├── API Key: phc_xxx
│   └── Host: https://us.i.posthog.com (or eu.i.posthog.com)
```

#### Getting API Keys

1. Sign up at [posthog.com](https://posthog.com)
2. Create a new organization (or use existing)
3. Create a project for your app(s)
4. Copy the Project API Key from Settings > Project > API Keys

```bash
# Example API key format
phc_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Why good:** Single organization pools billing across all projects, 6 projects included on paid tier, usage-based pricing means you're not penalized for multiple apps

---

### Pattern 2: Client-Side Setup

Install dependencies and configure for Next.js App Router.

#### Installation

```bash
# Install client-side SDK
bun add posthog-js
```

#### Environment Variables

```bash
# apps/client-next/.env.local

# PostHog Configuration
NEXT_PUBLIC_POSTHOG_KEY=phc_your_project_api_key_here
NEXT_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com
```

#### Setup Options

**Next.js 15.3+:** Use `instrumentation-client.js` (simpler, recommended)
**Next.js < 15.3:** Use PostHogProvider component (traditional approach)

See [examples/core.md](examples/core.md) for both approaches with full implementation examples.

**Why good:** `defaults: "2025-11-30"` enables automatic SPA page/leave tracking, `person_profiles: "identified_only"` reduces event costs, debug mode in development aids troubleshooting

---

### Pattern 3: Server-Side Setup with posthog-node

Install and configure the Node.js SDK for server-side event capture in API routes and Hono middleware.

#### Installation

```bash
# Install server-side SDK
bun add posthog-node
```

#### Environment Variables

```bash
# apps/client-next/.env.local (or apps/server/.env.local)

# Server-side PostHog (no NEXT_PUBLIC_ prefix needed)
POSTHOG_API_KEY=phc_your_project_api_key_here
POSTHOG_HOST=https://us.i.posthog.com
```

Create a server client singleton for reuse across API routes. See [examples/server.md](examples/server.md) for the full implementation including API route and Hono middleware examples.

#### Serverless Options

**Option 1:** Use `captureImmediate()` - simplest, awaits HTTP request directly
**Option 2:** Use `capture()` + `await flush()` - batched, requires explicit flush

**Why good:** Singleton prevents multiple client instances, flushInterval/flushAt configure batching, shutdown function for graceful cleanup, captureImmediate for simple serverless usage

</patterns>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `NEXT_PUBLIC_` prefix for client-side PostHog environment variables)**

**(You MUST create PostHogProvider as a 'use client' component - posthog-js requires browser APIs)**

**(You MUST call `posthog.shutdown()` or `posthog.flush()` after server-side event capture to prevent lost events)**

**(You MUST use `defaults: '2025-11-30'` or `capture_pageview: 'history_change'` for automatic SPA page tracking)**

**(You MUST use a single PostHog organization for all monorepo apps - projects are usage-based, not per-project pricing)**

**Failure to follow these rules will cause lost analytics events, broken tracking, or security vulnerabilities.**

</critical_reminders>

---

## Sources

- [PostHog Next.js Documentation](https://posthog.com/docs/libraries/next-js)
- [PostHog Node.js Documentation](https://posthog.com/docs/libraries/node)
- [PostHog Hono Integration](https://posthog.com/docs/libraries/hono)
- [Vercel + PostHog Guide](https://vercel.com/kb/guide/posthog-nextjs-vercel-feature-flags-analytics)
- [PostHog JavaScript Configuration](https://posthog.com/docs/libraries/js/config)
- [PostHog SPA Pageview Tracking](https://posthog.com/tutorials/single-page-app-pageviews)
