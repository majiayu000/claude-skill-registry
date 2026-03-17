---
name: api-observability-setup-axiom-pino-sentry
description: Pino, Axiom, Sentry installation - one-time project setup for logging and error tracking with source maps upload
---

# Observability Setup (Pino + Axiom + Sentry)

> **Quick Guide:** One-time project setup for observability. Install `pino`, `next-axiom`, `@sentry/nextjs`. Configure Axiom dataset + Vercel integration. Set up Sentry DSN and config files. Wrap `next.config.js` with `withAxiom`. Add source maps upload to GitHub Actions.

---

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder:
  - [examples/core.md](examples/core.md) - Essential setup patterns (dependencies, env vars, next.config.js)
  - [examples/sentry-config.md](examples/sentry-config.md) - Sentry configuration files and instrumentation
  - [examples/pino-logger.md](examples/pino-logger.md) - Pino logger setup with redaction
  - [examples/axiom-integration.md](examples/axiom-integration.md) - Web Vitals and dashboard queries
  - [examples/ci-cd.md](examples/ci-cd.md) - GitHub Actions source maps upload
  - [examples/health-check.md](examples/health-check.md) - Health check endpoints
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST create separate Axiom datasets for each environment - development, staging, production)**

**(You MUST use `NEXT_PUBLIC_` prefix for client-side Axiom token but NEVER for Sentry DSN in production)**

**(You MUST configure all three Sentry config files - `sentry.client.config.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`)**

**(You MUST add source maps upload to CI/CD - Sentry needs source maps for readable stack traces)**

**(You MUST install `pino-pretty` as a devDependency only - never use in production)**

</critical_requirements>

---

**Auto-detection:** pino, next-axiom, @sentry/nextjs, Axiom, Sentry, observability, logging, error tracking, source maps, health check

**When to use:**

- Setting up a new Next.js application that needs logging and error tracking
- Adding observability to an existing project without it
- Migrating from another logging/error tracking solution to Axiom + Sentry

**When NOT to use:**

- Adding new log statements to existing code (use `backend/observability.md` instead)
- Configuring alerts and monitors (use `backend/observability.md` instead)
- Debugging production issues (use `backend/observability.md` instead)

**Key patterns covered:**

- Dependency installation (Pino, next-axiom, @sentry/nextjs, pino-pretty)
- Environment variables template (`.env.example`)
- Axiom dataset creation and Vercel integration
- Sentry project setup with DSN configuration
- `next.config.js` with `withAxiom()` wrapper
- Sentry configuration files (client, server, edge)
- `instrumentation.ts` for Sentry initialization
- GitHub Actions for source maps upload
- Health check endpoint for Hono API
- Initial Axiom dashboard setup

---

<philosophy>

## Philosophy

**Observability is not optional for production apps.** Without logging and error tracking, debugging production issues becomes guesswork. The Pino + Axiom + Sentry stack provides:

- **Pino**: Fast structured JSON logging (5x faster than Winston)
- **Axiom**: Unified logs, traces, and metrics with 1TB free tier and Vercel integration
- **Sentry**: Best-in-class error tracking with source maps and release tracking

**This skill covers one-time setup. For ongoing usage patterns (log levels, structured fields, correlation IDs), see `backend/observability.md`.**

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Dependency Installation

Install all observability packages with correct dependency types.

```bash
# Production dependencies
npm install pino next-axiom @sentry/nextjs

# Development dependencies (pretty printing for local dev)
npm install -D pino-pretty
```

**Why:** `pino-pretty` as devDependency prevents production bundle bloat (~500KB), all core packages are production dependencies for runtime use.

For detailed code examples with good/bad comparisons, see [examples/core.md](examples/core.md#pattern-1-dependency-installation).

---

### Pattern 2: Environment Variables Template

Create `.env.example` with all required observability variables documented. Group by service for easy navigation, use comments to explain where to get each value, and maintain separate datasets per environment.

Key variables needed:

- `NEXT_PUBLIC_AXIOM_DATASET` - Dataset name (e.g., `myapp-dev`, `myapp-prod`)
- `NEXT_PUBLIC_AXIOM_TOKEN` - API token with ingest permission
- `NEXT_PUBLIC_SENTRY_DSN` - Sentry DSN from project settings
- `SENTRY_AUTH_TOKEN` - For source maps upload in CI
- `SENTRY_ORG` / `SENTRY_PROJECT` - Organization and project slugs
- `NEXT_PUBLIC_ENVIRONMENT` - Current environment identifier
- `NEXT_PUBLIC_APP_VERSION` - App version for Sentry releases

For complete template with all variables, see [examples/core.md](examples/core.md#pattern-2-environment-variables-template).

---

### Pattern 3: next.config.js with withAxiom

Wrap Next.js config with `withAxiom` for automatic logging integration, then wrap with `withSentryConfig` for source map handling.

Key configuration points:

- `withAxiom` wraps first for logging integration
- Sentry wraps outer for source map handling
- Source map upload disabled locally (`!process.env.CI`)
- `hideSourceMaps: true` prevents exposing source code

For complete configuration example, see [examples/core.md](examples/core.md#pattern-3-nextconfigjs-with-withaxiom).

---

### Pattern 4: Sentry Configuration Files

Create all three Sentry config files for client, server, and edge runtimes.

**Required files:**

- `sentry.client.config.ts` - Client-side with replay integration
- `sentry.server.config.ts` - Server-side with local variables capture
- `sentry.edge.config.ts` - Edge runtime with limited features

Key considerations:

- Use named constants for sample rates
- Environment-specific configuration (debug mode, sample rates)
- Filter expected errors with `beforeSend`
- Configure replay for debugging user sessions

For complete file templates, see [examples/sentry-config.md](examples/sentry-config.md#pattern-4-sentry-configuration-files).

---

### Pattern 5: Instrumentation File

Create `instrumentation.ts` for proper Sentry initialization in Next.js. Uses dynamic imports to load the correct config for each runtime.

```typescript
export async function register() {
  if (process.env.NEXT_RUNTIME === "nodejs") {
    await import("./sentry.server.config");
  }

  if (process.env.NEXT_RUNTIME === "edge") {
    await import("./sentry.edge.config");
  }
}

// Next.js 15+ error handling hook
export const onRequestError = Sentry.captureRequestError;
```

**Why:** Dynamic imports prevent loading wrong config for runtime, `onRequestError` hook captures Server Component errors automatically (Next.js 15+).

---

### Pattern 6: Web Vitals Component

Add `<AxiomWebVitals />` component to root layout for automatic Core Web Vitals (LCP, FID, CLS) reporting to Axiom.

**Note:** Web Vitals are only sent from production deployments, not local development.

For implementation example, see [examples/axiom-integration.md](examples/axiom-integration.md#pattern-6-web-vitals-component).

---

### Pattern 7: GitHub Actions Source Maps Upload

Configure CI/CD to upload source maps to Sentry on deployment. Key requirements:

- Set `CI=true` to enable source map upload during build
- Use GitHub secrets for credentials (never hardcode)
- Create Sentry release with `getsentry/action-release@v1`
- Tie version to git SHA for release tracking

For complete workflow template, see [examples/ci-cd.md](examples/ci-cd.md#pattern-7-github-actions-source-maps-upload).

---

### Pattern 8: Health Check Endpoint

Add health check endpoints for monitoring and load balancer integration:

- **Shallow check** (`/health`) - Fast, for frequent LB checks
- **Deep check** (`/health/deep`) - With dependency checks (database, etc.)

For Hono and Next.js implementations, see [examples/health-check.md](examples/health-check.md#pattern-8-health-check-endpoint).

---

### Pattern 9: Pino Logger Setup

Configure Pino with development/production modes:

- Development: `pino-pretty` for human-readable output
- Production: JSON for Axiom ingestion
- Base fields for context in every log
- Redaction of sensitive fields

For complete configuration, see [examples/pino-logger.md](examples/pino-logger.md#pattern-9-pino-logger-setup).

---

### Pattern 10: Axiom Dashboard Setup

After setting up, create initial dashboards in Axiom:

- Request volume per minute
- Error rate percentage
- Response time P95
- Top errors
- Web Vitals metrics

For APL query examples, see [examples/axiom-integration.md](examples/axiom-integration.md#pattern-10-axiom-dashboard-setup).

</patterns>

---

<decision_framework>

## Decision Framework

See [reference.md](reference.md#decision-framework) for complete decision trees:

- **Log Destinations**: Where logs should go in each environment
- **Sentry vs Axiom for Errors**: Which system handles which error types

</decision_framework>

---

<red_flags>

## RED FLAGS

See [reference.md](reference.md#red-flags) for complete list.

**High Priority:**

- Committing Axiom tokens or Sentry DSN to version control
- Using pino-pretty in production
- Missing source maps upload
- Same Axiom dataset for all environments

**Common Mistakes:**

- Forgetting to wrap `next.config.js` with `withAxiom`
- Missing `instrumentation.ts`
- Hardcoding sample rates instead of named constants

</red_flags>

---

<integration>

## Integration Guide

**Works with:**

- **backend/api.md**: Hono health check endpoints, logging middleware
- **backend/database.md**: Database connection health checks
- **setup/env.md**: Environment variable patterns for secrets
- **backend/ci-cd.md**: GitHub Actions source maps upload

**Replaces:**

- console.log debugging (use structured logging instead)
- Manual error tracking (Sentry automates this)
- Custom logging solutions (standardize on Pino + Axiom)

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST create separate Axiom datasets for each environment - development, staging, production)**

**(You MUST use `NEXT_PUBLIC_` prefix for client-side Axiom token but NEVER for Sentry DSN in production)**

**(You MUST configure all three Sentry config files - `sentry.client.config.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`)**

**(You MUST add source maps upload to CI/CD - Sentry needs source maps for readable stack traces)**

**(You MUST install `pino-pretty` as a devDependency only - never use in production)**

**Failure to follow these rules will result in missing logs, unreadable errors, and security vulnerabilities.**

</critical_reminders>
