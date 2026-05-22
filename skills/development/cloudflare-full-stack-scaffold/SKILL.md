---
name: cloudflare-full-stack-scaffold
description: Production React + Cloudflare Workers + Hono starter with D1, KV, R2, Workers AI. Use for full-stack projects, MVPs, AI apps on Cloudflare.

  Keywords: cloudflare scaffold, full-stack starter, react cloudflare, hono template, production boilerplate,
  AI SDK integration, workers AI, complete starter project, D1 KV R2 setup, web app template,
  chat application scaffold, RAG starter, planning docs included, session handoff,
  tailwind v4 shadcn, typescript starter, vite cloudflare plugin, all services configured
license: MIT
metadata:
  version: 1.1.0
  last_updated: 2025-12-09
  packages:
    - "react: ^19.2.0"
    - "react-router-dom: ^7.1.3"
    - "hono: ^4.10.6"
    - "@cloudflare/vite-plugin: ^1.15.2"
    - "ai: ^5.0.98"
    - "@ai-sdk/openai: ^2.0.71"
    - "@ai-sdk/anthropic: ^2.0.45"
    - "workers-ai-provider: ^2.0.0"
    - "@ai-sdk/react: ^2.0.88"
    - "@clerk/clerk-react: ^5.56.1"
    - "tailwindcss: ^4.1.17"
  production_tested: true
  token_savings: "75-80%"
  errors_prevented: "12+ setup and configuration errors"
  progressive_disclosure: true
  refactoring_date: 2025-12-09
  skill_structure:
    main_file_lines: 345
    reference_files: 9
    total_reference_lines: 3043
    reduction_achieved: "55% (773 → 345 lines)"
---

# Cloudflare Full-Stack Scaffold

Complete, production-ready starter project for building full-stack applications on Cloudflare with React, Hono, AI SDK, and all Cloudflare services pre-configured.

## When to Use This Skill

Use this skill when you need to:

- **Start a new full-stack Cloudflare project** in minutes instead of hours
- **Build AI-powered applications** with chat interfaces, RAG, or tool calling
- **Have core Cloudflare services ready** (D1, KV, R2, Workers AI)
- **Opt-in to advanced features** (Clerk Auth, AI Chat, Queues, Vectorize)
- **Use modern best practices** (Tailwind v4, shadcn/ui, AI SDK, React 19)
- **Include planning docs and session handoff** from the start
- **Choose your AI provider** (Workers AI, OpenAI, Anthropic, Gemini)
- **Enable features only when needed** with simple npm scripts
- **Avoid configuration errors** and integration issues

## When to Load References

This skill includes 9 comprehensive reference files. Load them progressively based on your task:

### Setting Up New Project
- **`references/quick-start-guide.md`** - Load when: user wants to create new project, needs setup walkthrough, first-time setup
- **`references/project-overview.md`** - Load when: user asks about scaffold structure, what's included, helper scripts, directory organization

### Working with Cloudflare Services
- **`references/service-configuration.md`** - Load when: configuring D1/KV/R2/Workers AI, setting up bindings, service integration, wrangler.jsonc questions

### AI Integration
- **`references/ai-sdk-guide.md`** - Load when: implementing AI chat, using AI SDK, text generation, streaming responses, tool calling, AI provider setup

### Forms and Data Management
- **`references/full-stack-patterns.md`** - Load when: building forms, implementing validation, data fetching, React Hook Form questions, TanStack Query usage, full-stack validation patterns
- **`references/supporting-libraries-guide.md`** - Load when: deep dive into specific libraries (React Hook Form, Zod, TanStack Query, Hono routing), API reference needed

### Authentication
- **`references/enabling-auth.md`** - Load when: setting up Clerk auth, implementing authentication, user management, JWT verification, protected routes

### Architecture and Configuration
- **`references/architecture-patterns.md`** - Load when: frontend-backend connection issues, CORS errors, environment variables confusion, API not responding, auth race conditions

### Customization
- **`references/customization-guide.md`** - Load when: removing services, adding features, customizing theme, creating routes, switching AI providers, modifying scaffold

**Strategy**: Start with SKILL.md quick start. Load references only when user needs detailed implementation guidance for specific areas.

## What This Skill Provides

**Complete production-ready scaffold** you can copy and customize immediately.

### Quick Start

```bash
cp -r scaffold/ my-new-app/ && cd my-new-app/
bun install
./scripts/init-services.sh  # Creates D1, KV, R2
npm run d1:local && npm run dev
```

**Result in ~5 minutes**:
- ✅ Full-stack app running (React + Hono + Cloudflare Workers)
- ✅ Core services configured (D1, KV, R2, Workers AI)
- ✅ AI SDK ready (OpenAI, Anthropic, Gemini, Workers AI)
- ✅ Planning docs and session handoff protocol included
- ✅ Optional features enabled with one command each:
  - `npm run enable-auth` (Clerk)
  - `npm run enable-ai-chat` (AI SDK UI)
  - `npm run enable-queues` (async processing)
  - `npm run enable-vectorize` (vector search & RAG)

### What's Included

**Frontend**: React 19, Vite, Tailwind v4, shadcn/ui, React Router, dark mode
**Backend**: Hono, Cloudflare Workers, CORS middleware, typed routes
**Services**: D1 (SQL), KV (cache), R2 (storage), Workers AI, Queues, Vectorize
**AI**: AI SDK v5 with multi-provider support (OpenAI, Anthropic, Gemini, Workers AI)
**Auth**: Clerk integration (optional, enable script provided)
**Planning**: Complete docs (Architecture, Database, API, Phases, UI, Testing), SCRATCHPAD.md for session handoff
**Scripts**: 6 helper scripts for setup, service initialization, and feature enabling

**Full structure, helper scripts, and reference docs**: Load `references/project-overview.md` for complete details.

## Key Integrations

### 1. AI SDK v5 - Multi-Provider AI

Three flexible approaches:
- **Direct Workers AI Binding**: No API key, fastest (`c.env.AI.run()`)
- **AI SDK + Workers AI**: Portable code, same infrastructure (`workers-ai-provider`)
- **AI SDK + External**: OpenAI, Anthropic, Gemini - switch in one line

**Chat UI** (optional): Enable with `npm run enable-ai-chat` for complete `useChat` hook interface

**Details**: Load `references/ai-sdk-guide.md` for streaming, tool calling, RAG patterns, provider switching

### 2. Forms & Data (React Hook Form + Zod + TanStack Query)

Industry-standard pattern for production apps:
- **React Hook Form**: Performance-focused form state
- **Zod v4**: Type-safe validation, shared frontend/backend
- **TanStack Query v5**: Smart caching, optimistic updates

**Full-stack validation**: Define schema once in `shared/schemas/`, use everywhere with type inference

**Details**: Load `references/full-stack-patterns.md` for complete working examples and patterns

### 3. Cloudflare Services Ready

**Core** (init script provided): D1 (SQL), KV (cache), R2 (storage), Workers AI (inference)
**Optional** (enable scripts): Queues (async), Vectorize (RAG)

All services have example routes with CRUD operations, typed helpers, and best practices

**Details**: Load `references/service-configuration.md` for binding config and usage patterns

### 3. Optional Clerk Authentication

All auth patterns included but **COMMENTED** - uncomment to enable:

```bash
./scripts/enable-auth.sh
# Prompts for Clerk keys, uncomments all patterns
```

**What gets enabled**:
- Frontend: ProtectedRoute component, auth in api-client
- Backend: JWT verification middleware
- Protected API routes
- Auth loading states
- Session management

### 4. Planning Docs + Session Handoff Protocol

**docs/ directory** - Complete planning structure:
- ARCHITECTURE.md: System design
- DATABASE_SCHEMA.md: D1 schema docs
- API_ENDPOINTS.md: All routes documented
- IMPLEMENTATION_PHASES.md: Phased build approach
- UI_COMPONENTS.md: Component hierarchy
- TESTING.md: Test strategy

**SCRATCHPAD.md** - Session handoff protocol:
- Current phase tracking
- Progress checkpoints
- Next actions
- References to planning docs

## Usage Guide

### Setup (5 Minutes)

```bash
cp -r scaffold/ my-new-app/ && cd my-new-app/
bun install
./scripts/init-services.sh  # Creates D1, KV, R2, updates wrangler.jsonc
npm run d1:local && npm run dev  # http://localhost:5173
```

### Enable Optional Features

```bash
npm run enable-auth        # Clerk authentication
npm run enable-ai-chat     # AI SDK UI chat interface
npm run enable-queues      # Async message processing
npm run enable-vectorize   # Vector search & RAG
```

### Deploy

```bash
npm run build && bunx wrangler deploy
bunx wrangler d1 execute my-app-db --remote --file=schema.sql
bunx wrangler secret put CLERK_SECRET_KEY  # Repeat for other secrets
```

**Detailed setup walkthrough**: Load `references/quick-start-guide.md`

## Customization

Common patterns: remove unused services, add API routes, switch AI providers, customize theme, add pages

**Complete step-by-step guides**: Load `references/customization-guide.md`

## Critical Architecture Patterns

**Frontend-Backend Connection**: Vite plugin runs Worker on SAME port → use relative URLs (`fetch('/api/data')`)
**Environment Variables**: `.env` (VITE_ prefix, frontend) vs `.dev.vars` (no prefix, backend secrets)
**CORS**: Apply middleware BEFORE routes (`app.use('/api/*', corsMiddleware)` must come first)
**Auth**: Check `isLoaded` before API calls to prevent race conditions

**Detailed troubleshooting & examples**: Load `references/architecture-patterns.md` when debugging connection/CORS/auth issues

## Dependencies Included

**Frontend**: React 19, Vite, Tailwind v4, shadcn/ui (Radix UI), React Router, React Hook Form, Zod, TanStack Query
**Backend**: Hono, Cloudflare Workers, Wrangler
**AI**: AI SDK v5 (OpenAI, Anthropic, Google providers), Workers AI Provider
**Auth**: Clerk (optional, commented)

All packages current as of 2025-11. **Full list with versions**: See `references/supporting-libraries-guide.md`

## Token Efficiency

| Scenario | Without Scaffold | With Scaffold | Savings |
|----------|------------------|---------------|---------|
| Initial setup | ~18-22k tokens | ~3-5k tokens | ~80% |
| Service configuration | ~8-10k tokens | 0 tokens (done) | 100% |
| Frontend-backend connection | ~5-7k tokens | 0 tokens (done) | 100% |
| AI SDK setup | ~4-6k tokens | 0 tokens (done) | 100% |
| Auth integration | ~6-8k tokens | ~500 tokens | ~90% |
| Planning docs | ~3-5k tokens | 0 tokens (included) | 100% |
| **Total** | **~44-58k tokens** | **~3-6k tokens** | **~90%** |

**Time Savings**: 3-4 hours → 5-10 minutes (~95% faster)

## Common Issues Prevented

| Issue | How Scaffold Prevents It |
|-------|-------------------------|
| **Service binding errors** | All bindings pre-configured and tested |
| **CORS errors** | Middleware in correct order |
| **Auth race conditions** | Proper loading state patterns |
| **Frontend-backend connection** | Vite plugin correctly configured |
| **AI SDK setup confusion** | Multiple working examples |
| **Missing planning docs** | Complete docs/ structure included |
| **Environment variable mix-ups** | Clear .dev.vars.example with comments |
| **Missing migrations** | migrations/ directory with examples |
| **Inconsistent file structure** | Standard, tested structure |
| **Database type errors** | Typed query helpers included |
| **Theme configuration** | Tailwind v4 theming pre-configured |
| **Build errors** | Working build config (vite + wrangler) |

**Total Errors Prevented**: 12+ common setup and integration errors

## When NOT to Use This Scaffold

- ❌ Building a static site (no backend needed)
- ❌ Using Next.js, Remix, or other meta-framework
- ❌ Need SSR (use framework-specific Cloudflare adapter)
- ❌ Building backend-only API (no frontend needed)
- ❌ Extremely simple single-page app

**For these cases**: Use minimal templates or official framework starters.

## Production Evidence

**Based on**:
- Cloudflare's official agents-starter template (AI SDK patterns)
- cloudflare-full-stack-integration skill (tested frontend-backend patterns)
- session-handoff-protocol skill (planning docs + SCRATCHPAD.md)
- tailwind-v4-shadcn skill (UI component patterns)
- Multiple production projects

**Package versions verified**: 2025-10-23

**Works with**:
- Cloudflare Workers (production environment)
- Wrangler 4.0+
- Node.js 18+
- npm/pnpm/yarn

## Quick Reference

**Setup new project**:
```bash
cp -r scaffold/ my-app/
cd my-app/
bun install
# Follow quick-start-guide.md
```

**Enable auth**:
```bash
./scripts/enable-auth.sh
```

**Enable AI chat**:
```bash
./scripts/enable-ai-chat.sh
```

**Deploy**:
```bash
npm run build
bunx wrangler deploy
```

**Key Files**:
- `wrangler.jsonc` - Service configuration
- `vite.config.ts` - Build configuration
- `.dev.vars.example` - Environment variables template
- `docs/ARCHITECTURE.md` - System design
- `SCRATCHPAD.md` - Session handoff protocol

---

**Remember**: This scaffold is a **starting point**, not a constraint. Customize everything to match your needs. The value is in having a working foundation with all the integration patterns already figured out, saving hours of setup and debugging time.
