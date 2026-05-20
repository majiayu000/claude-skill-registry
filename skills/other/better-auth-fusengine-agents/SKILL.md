---
name: better-auth
description: Complete Better Auth - 40+ OAuth providers, 20+ plugins, all adapters, all frameworks. Use when implementing authentication, login, OAuth, 2FA, magic links, SSO, Stripe, SCIM, or session management.
versions:
  better-auth: 1.2
user-invocable: true
references: references/installation.md, references/basic-usage.md, references/comparison.md, references/server-config.md, references/client.md, references/session.md, references/middleware.md, references/server-actions.md, references/hooks.md, references/email.md, references/rate-limiting.md, references/cli.md, references/security.md, references/api.md, references/migrations.md, references/typescript.md, references/user-accounts.md, references/errors.md, references/telemetry.md, references/faq.md, references/concepts/sessions.md, references/concepts/database.md, references/concepts/plugins.md, references/concepts/users.md, references/concepts/oauth.md, references/concepts/security.md, references/concepts/cookies.md, references/adapters/prisma.md, references/adapters/drizzle.md, references/adapters/mongodb.md, references/adapters/sql-databases.md, references/adapters/community-adapters.md, references/providers/overview.md, references/providers/google.md, references/providers/github.md, references/providers/discord.md, references/providers/apple.md, references/providers/microsoft.md, references/providers/social-providers.md, references/providers/generic-oauth.md, references/providers/oauth-providers-all.md, references/plugins/overview.md, references/plugins/2fa.md, references/plugins/admin.md, references/plugins/organization.md, references/plugins/passkey.md, references/plugins/magic-link.md, references/plugins/email-otp.md, references/plugins/phone.md, references/plugins/anonymous.md, references/plugins/username.md, references/plugins/sso.md, references/plugins/jwt.md, references/plugins/bearer.md, references/plugins/multi-session.md, references/plugins/oidc-provider.md, references/plugins/api-key.md, references/plugins/captcha.md, references/plugins/stripe.md, references/plugins/polar.md, references/plugins/scim.md, references/plugins/siwe.md, references/plugins/device-auth.md, references/integrations/nextjs.md, references/integrations/other-frameworks.md, references/integrations/frameworks-all.md, references/examples/nextjs-app-router.md, references/examples/oauth-complete.md, references/examples/2fa-complete.md, references/examples/organization-complete.md, references/examples/passkey-complete.md, references/guides/performance.md, references/guides/plugin-development.md, references/guides/saml-okta.md, references/guides/database-adapter.md, references/guides/auth0-migration.md, references/guides/clerk-migration.md, references/guides/authjs-migration.md, references/guides/supabase-migration.md, references/guides/workos-migration.md, references/guides/browser-extension.md
related-skills: nextjs-16, prisma-7, solid-nextjs
---

# Better Auth - Complete Authentication

TypeScript-first authentication library with 40+ OAuth providers and 20+ plugins.

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing auth setup and patterns
2. **fuse-ai-pilot:research-expert** - Verify latest Better Auth docs via Context7/Exa
3. **mcp__context7__query-docs** - Check providers/plugins availability

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Implementing authentication in TypeScript/JavaScript applications
- Need OAuth providers (Google, GitHub, Discord, Apple, Microsoft, etc.)
- Adding 2FA, magic links, passkeys, or phone authentication
- Enterprise SSO with SAML, SCIM provisioning, or organizations
- Integrating payments with Stripe or Polar subscriptions
- Web3 authentication with Sign-In with Ethereum (SIWE)
- Migrating from Auth.js, Clerk, Auth0, Supabase, or WorkOS

### Why Better Auth

| Feature | Benefit |
|---------|---------|
| Framework agnostic | Next.js, SvelteKit, Nuxt, Remix, Astro, Expo, NestJS |
| Plugin architecture | Add only the features you need (20+ plugins) |
| Full TypeScript | End-to-end type safety, inference included |
| Self-hosted | Your data stays on your infrastructure |
| Database flexible | Prisma, Drizzle, MongoDB, PostgreSQL, MySQL, SQLite |
| Enterprise ready | SSO, SCIM, organizations, audit logs |

---

## Coverage

### OAuth Providers (40+)

Google, GitHub, Discord, Apple, Microsoft, Slack, Spotify, Twitter/X, Facebook, LinkedIn, GitLab, Bitbucket, Dropbox, Twitch, Reddit, TikTok, and 25+ more documented in [providers/](references/providers/).

### Plugins (20+)

| Plugin | Purpose |
|--------|---------|
| 2FA | TOTP authenticator, backup codes |
| Magic Link | Passwordless email login |
| Passkey | WebAuthn biometric authentication |
| Organization | Multi-tenant, roles, invitations |
| SSO | Enterprise SAML/OIDC single sign-on |
| SCIM | Directory sync, user provisioning |
| Stripe | Subscription billing integration |
| API Key | Machine-to-machine authentication |
| JWT/Bearer | Token-based API authentication |

### Database Adapters

Prisma, Drizzle, MongoDB, raw SQL (PostgreSQL, MySQL, SQLite), and community adapters.

---

## SOLID Architecture (Next.js 16)

Components organized in `modules/auth/` following separation of concerns:

- **Services**: `betterAuth` configuration and initialization
- **Hooks**: `createAuthClient` for client-side auth state
- **API Route**: `app/api/auth/[...all]/route.ts` handler
- **Proxy**: `proxy.ts` for route protection (replaces middleware)

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Initial setup | [installation.md](references/installation.md), [server-config.md](references/server-config.md) |
| Client usage | [client.md](references/client.md), [session.md](references/session.md) |
| OAuth providers | [providers/overview.md](references/providers/overview.md), individual provider docs |
| Add plugins | [plugins/overview.md](references/plugins/overview.md), individual plugin docs |
| Database setup | [adapters/prisma.md](references/adapters/prisma.md), [adapters/drizzle.md](references/adapters/drizzle.md) |
| Enterprise SSO | [plugins/sso.md](references/plugins/sso.md), [guides/saml-okta.md](references/guides/saml-okta.md) |
| Payments | [plugins/stripe.md](references/plugins/stripe.md), [plugins/polar.md](references/plugins/polar.md) |
| Migration | [guides/clerk-migration.md](references/guides/clerk-migration.md), other migration guides |
| Complete examples | [examples/](references/examples/) for full implementations |

---

## Best Practices

1. **Plugins on demand** - Only add plugins you actually need
2. **Type-safe client** - Use generated types from server config
3. **Session caching** - Enable session caching for performance
4. **Rate limiting** - Configure rate limits for auth endpoints
5. **Secure cookies** - Use secure, httpOnly, sameSite cookies
6. **Database indexes** - Add indexes on user lookup fields

---

## Concepts

Core concepts explained in [concepts/](references/concepts/):

- **Sessions** - Token management, refresh, revocation
- **Database** - Schema design, migrations, adapters
- **Plugins** - Extension system, composition
- **OAuth** - Provider configuration, callbacks
- **Security** - CSRF, rate limiting, password hashing
- **Cookies** - Session storage, cross-domain
