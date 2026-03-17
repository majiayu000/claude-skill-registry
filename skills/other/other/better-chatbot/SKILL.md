---
name: better-chatbot
description: better-chatbot project conventions and standards. Use for contributing code, following three-tier tool system (MCP/Workflow/Default), or encountering server action validators, repository patterns, component design errors.

  Keywords: better-chatbot, chatbot contribution, better-chatbot standards, chatbot development, AI chatbot patterns, API architecture, three-tier tool system, repository pattern, progressive enhancement, defensive programming, streaming-first, compound component pattern, Next.js chatbot, Vercel AI SDK chatbot, MCP tools, workflow builder, server action validators, tool abstraction, DAG workflows, shared business logic, safe() wrapper, tool lifecycle
license: MIT
metadata:
  version: 3.0.0
  author: Claude Skills Maintainers
  upstream: https://github.com/cgoinglove/better-chatbot
  last_verified: 2025-12-17
  tech_stack: Next.js 15, Vercel AI SDK 5, Better Auth, Drizzle ORM, PostgreSQL, Playwright
  token_savings: ~75%
  errors_prevented: 8
  optimization_date: 2025-12-17
---

# better-chatbot Contribution & Standards Skill

**Status**: Production Ready
**Version**: 3.0.0 (Optimized with progressive disclosure)
**Last Updated**: 2025-12-17
**Dependencies**: None (references better-chatbot project)
**Latest Versions**: Next.js 16.0.3, Vercel AI SDK 5.0.98, Better Auth 1.3.34, Drizzle ORM 0.41.0

---

## Overview

**better-chatbot** is an open-source AI chatbot platform for individuals and teams, built with Next.js 15 and Vercel AI SDK v5. It combines multi-model AI support (OpenAI, Anthropic, Google, xAI, Ollama, OpenRouter) with advanced features like MCP (Model Context Protocol) tool integration, visual workflow builder, realtime voice assistant, and team collaboration.

**This skill teaches Claude the project-specific conventions and patterns** used in better-chatbot to ensure contributions follow established standards and avoid common pitfalls.

---

## Quick Start

### Setup Development Environment

```bash
# Clone and install
git clone https://github.com/cgoinglove/better-chatbot.git
cd better-chatbot
pnpm install

# Configure environment
cp .env.example .env
# Add your API keys: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.
# Add database URL: DATABASE_URL="postgresql://..."
# Add auth secret: BETTER_AUTH_SECRET="your-secret"

# Run development server
pnpm dev
```

### Core Commands

- `pnpm dev` - Start development server
- `pnpm build` - Production build
- `pnpm test` - Run unit tests
- `pnpm test:e2e` - Run E2E tests (requires DB + API keys)
- `pnpm check` - Lint + type check + tests (run before PR)

### Repository Structure

```
better-chatbot/
├── src/
│   ├── app/                # Next.js routes + API
│   ├── components/         # UI components by domain
│   ├── lib/               # Core logic (ai, db, validations)
│   ├── hooks/             # React hooks
│   └── types/             # TypeScript types
├── tests/                 # E2E Playwright tests
└── drizzle/              # Database migrations
```

---

## Core Architecture

### Three-Tier Tool System

Better-chatbot uses a three-tier tool architecture for AI capabilities:

1. **MCP Tools** - External tools via Model Context Protocol
2. **Workflow Tools** - Visual DAG-based workflows
3. **Default Tools** - Built-in app tools (web search, image generation, etc.)

**For details**: Load `references/tool-system.md` when implementing tools or understanding tool execution.

### API Patterns

Routes follow RESTful conventions with streaming-first architecture and defensive programming using `safe()` wrapper.

**For details**: Load `references/api-architecture.md` when building API routes or implementing streaming.

### Component Philosophy

Components organized by feature using compound component pattern. Tools execution separated from rendering.

**For details**: Load `references/component-patterns.md` when building UI components.

### Database & Repository Pattern

All database access abstracted through repository classes using Drizzle ORM.

**For details**: Load `references/database-patterns.md` when implementing database queries.

---

## Top 5 Errors (Must Know)

### Error #1: Forgetting Auth Checks in Server Actions

**Error**: Unauthorized users accessing protected actions
**Why**: Manual auth implementation is inconsistent
**Prevention**: Use `validatedActionWithUser` or `validatedActionWithAdminPermission`

```typescript
// ❌ BAD: Manual auth check
export async function updateProfile(data: ProfileData) {
  const session = await getSession()
  if (!session) throw new Error("Unauthorized")
  // ... rest of logic
}

// ✅ GOOD: Use validator
export const updateProfile = validatedActionWithUser(
  profileSchema,
  async (data, formData, user) => {
    // user is guaranteed to exist, auto-error handling
  }
)
```

### Error #2: Tool Type Mismatches

**Error**: Runtime type errors when executing tools
**Why**: Not checking tool type before execution
**Prevention**: Use branded type tags for runtime narrowing

```typescript
// ❌ BAD: Assuming tool type
const result = await executeMcpTool(tool)

// ✅ GOOD: Check tool type
if (VercelAIMcpToolTag.isMaybe(tool)) {
  const result = await executeMcpTool(tool)
} else if (VercelAIWorkflowToolTag.isMaybe(tool)) {
  const result = await executeWorkflowTool(tool)
}
```

### Error #3: FormData Parsing Errors

**Error**: Inconsistent error handling for form submissions
**Why**: Manual FormData parsing with ad-hoc validation
**Prevention**: Validators handle parsing automatically

```typescript
// ❌ BAD: Manual parsing
const name = formData.get("name") as string
if (!name) throw new Error("Name required")

// ✅ GOOD: Validator with Zod
const schema = z.object({ name: z.string().min(1) })
export const action = validatedAction(schema, async (data) => {
  // data.name is validated and typed
})
```

### Error #4: Cross-Field Validation Issues

**Error**: Password mismatch validation not working
**Why**: Separate validation for related fields
**Prevention**: Use Zod `superRefine`

```typescript
// ❌ BAD: Separate checks
if (data.password !== data.confirmPassword) { /* error */ }

// ✅ GOOD: Zod superRefine
const schema = z.object({
  password: z.string(),
  confirmPassword: z.string()
}).superRefine((data, ctx) => {
  if (data.password !== data.confirmPassword) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Passwords don't match",
      path: ["confirmPassword"]
    })
  }
})
```

### Error #5: Zustand State Mutation

**Error**: State updates not triggering re-renders
**Why**: Mutating state directly instead of creating new objects
**Prevention**: Use shallow updates with spread operator

```typescript
// ❌ BAD: Direct mutation
set((state) => {
  state.user.name = "New Name" // Mutation!
})

// ✅ GOOD: Shallow update
set((state) => ({
  user: { ...state.user, name: "New Name" }
}))
```

**For all errors**: Load `references/common-errors.md` when debugging issues beyond the top 5.

---

## Critical Rules

### Always Do

✅ Use `validatedActionWithUser` or `validatedActionWithAdminPermission` for server actions
✅ Check tool types with branded type tags before execution
✅ Use Zod `superRefine` for cross-field validation
✅ Add unit tests (happy path + one failure mode)
✅ Run `pnpm check` before PR submission
✅ Include visual documentation for UI changes
✅ Use Conventional Commit format for PR titles
✅ Run E2E tests when touching critical flows

### Never Do

❌ Implement server actions without auth validators
❌ Assume tool type without runtime check
❌ Parse FormData manually (use validators)
❌ Mutate Zustand state directly (use shallow updates)
❌ Skip first-user tests on clean database
❌ Commit without running `pnpm check`
❌ Submit PR without visual docs (if UI change)
❌ Use non-conventional commit format

---

## When to Load References

Load reference files when working on specific aspects of better-chatbot:

### API Architecture (`references/api-architecture.md`)
Load when:
- Implementing new API routes or endpoints
- Understanding route handler patterns
- Working with streaming responses
- Implementing defensive programming with safe()
- Troubleshooting API-related issues
- Building shared business logic

### Tool System (`references/tool-system.md`)
Load when:
- Adding new MCP tools
- Creating workflow tools
- Understanding tool lifecycle
- Debugging tool execution
- Implementing tool filtering or mentions
- Working with the three-tier tool architecture

### Component Patterns (`references/component-patterns.md`)
Load when:
- Building new UI components
- Understanding compound component pattern
- Implementing state management
- Working with Zustand stores
- Designing component APIs
- Separating tool execution from rendering

### Database Patterns (`references/database-patterns.md`)
Load when:
- Creating new repository classes
- Writing complex database queries
- Implementing transactions
- Understanding the repository pattern
- Troubleshooting database issues
- Working with Drizzle ORM

### Architectural Principles (`references/architectural-principles.md`)
Load when:
- Making architectural decisions
- Understanding design philosophy
- Implementing progressive enhancement
- Following streaming-first patterns
- Ensuring defensive programming
- Understanding DRY principle application

### Extension Points (`references/extension-points.md`)
Load when:
- Extending the chatbot with custom features
- Adding new tool types
- Customizing existing behavior
- Understanding plugin architecture
- Integrating external services

### UX Patterns (`references/ux-patterns.md`)
Load when:
- Implementing @mention functionality
- Understanding UX patterns
- Working with multi-model support
- Designing interaction flows
- Building chat UI components

### Templates (`references/templates.md`)
Load when:
- Adding new routes, tools, or components
- Following code templates
- Understanding complete implementation examples
- Starting new features from scratch
- Implementing standard patterns

### Server Actions (`references/server-actions.md`)
Load when:
- Implementing server actions
- Understanding action validators
- Following server-side validation patterns
- Troubleshooting server action issues
- Working with FormData

### Common Errors (`references/common-errors.md`)
Load when:
- Debugging issues beyond the top 5 errors
- Encountering specific error messages
- Understanding error patterns
- Looking for solutions to common problems
- Preventing known issues

### Repository Guidelines (`references/AGENTS.md`)
Load when:
- Understanding project structure
- Following coding conventions
- Setting up development environment
- Running tests or builds
- Understanding commit/PR guidelines

### Contributing (`references/CONTRIBUTING.md`)
Load when:
- Preparing to contribute
- Understanding PR process
- Following commit message conventions
- Submitting pull requests
- Adding visual documentation

---

## Using Bundled Resources

This skill includes 12 reference files:

**Technical References** (10 files):
- `api-architecture.md` - API patterns and route handlers
- `tool-system.md` - Three-tier tool architecture
- `component-patterns.md` - UI component design
- `database-patterns.md` - Repository pattern and Drizzle ORM
- `architectural-principles.md` - Design philosophy
- `extension-points.md` - How to extend the system
- `ux-patterns.md` - UX patterns and @mentions
- `templates.md` - Code templates for routes/tools/components
- `server-actions.md` - Server action validators
- `common-errors.md` - Complete error catalog

**Repository References** (2 files):
- `AGENTS.md` - Repository structure and development commands
- `CONTRIBUTING.md` - Contribution workflow and PR guidelines

Load references on-demand when specific knowledge is needed. See "When to Load References" section for triggers.

---

## Dependencies

**Core**:
- Next.js 15+ (App Router)
- Vercel AI SDK 5+
- Better Auth 1.3+
- Drizzle ORM 0.40+
- PostgreSQL

**Testing**:
- Vitest (unit tests)
- Playwright (E2E tests)

**Tools**:
- TypeScript 5+
- Biome (formatting + linting)
- pnpm 8+

---

## Official Documentation

- **Repository**: https://github.com/cgoinglove/better-chatbot
- **Vercel AI SDK**: https://sdk.vercel.ai/docs
- **Better Auth**: https://www.better-auth.com/docs
- **Drizzle ORM**: https://orm.drizzle.team/docs/overview
- **MCP Spec**: https://modelcontextprotocol.io/introduction

---

## Production Example

This skill is based on the production better-chatbot repository with 48 E2E tests covering core functionality, active development, and growing community contributions.

---

**Last verified**: 2025-12-17 | **Version**: 3.0.0
