---
name: clerk
description: Clerk authentication router. Use when user asks about adding authentication, setting up Clerk, custom sign-in flows, Next.js patterns, organizations, syncing users, or testing. Automatically routes to the specific skill based on their task.
---

# Clerk Skills Router

Based on what you're trying to do, here's the right skill to use:

## By Task

**Adding Clerk to your project** → Use `clerk-setup`
- Framework detection and quickstart
- Environment setup, API keys, Keyless flow
- Migration from other auth providers

**Custom sign-in/sign-up UI** → Use `clerk-custom-ui`
- Custom authentication flows
- Appearance and styling
- OAuth, magic links, passkeys, MFA

**Advanced Next.js patterns** → Use `clerk-nextjs-patterns`
- Server vs Client auth APIs
- Middleware strategies
- Server Actions, caching
- API route protection

**B2B / Organizations** → Use `clerk-orgs`
- Multi-tenant apps
- Organization slugs in URLs
- Roles, permissions, RBAC
- Member management

**Webhooks** → Use `clerk-webhooks`
- Real-time events
- Data syncing
- Notifications & integrations

**E2E Testing** → Use `clerk-testing`
- Playwright/Cypress setup
- Auth flow testing
- Test utilities

## Quick Navigation

If you know your task, you can directly access:
- `/clerk-setup` - Framework setup
- `/clerk-custom-ui` - Custom flows
- `/clerk-nextjs-patterns` - Next.js patterns
- `/clerk-orgs` - Organizations
- `/clerk-webhooks` - Webhooks
- `/clerk-testing` - Testing

Or describe what you need and I'll recommend the right one.
