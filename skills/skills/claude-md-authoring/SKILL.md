---
name: claude-md-authoring
description: Creating and maintaining CLAUDE.md project memory files that provide non-obvious codebase context. Use when (1) creating a new CLAUDE.md for a project, (2) adding architectural patterns or design decisions to existing CLAUDE.md, (3) capturing project-specific conventions that aren't obvious from code inspection.
model# allowedTools: Read,Write,Edit,Grep,Glob
---

# CLAUDE.md Authoring

Create effective CLAUDE.md files that serve as project-specific memory for AI coding agents.

## Purpose

CLAUDE.md files provide AI agents with:
- Non-obvious conventions, architectural patterns and gotchas
- Confirmed solutions to recurring issues
- Project-specific context not found in standard documentation

**Not for**: Obvious patterns, duplicating documentation, or generic coding advice.

## Core Principles

**Signal over noise**: Every sentence must add non-obvious value. If an AI agent could infer it from reading the codebase, omit it.

**Actionable context**: Focus on "what to do" and "why it matters", not descriptions of what exists.

**Solve real friction, not theoretical concerns**: Add to CLAUDE.md based on actual problems encountered, not hypothetical scenarios. If you repeatedly explain the same thing to Claude, document it. If you haven't hit the problem yet, don't pre-emptively solve it.

## Structure

Use XML-style tags for organisation. Common sections:

```xml
<ARCHITECTURE>  System design, key patterns, data flow
<CONVENTIONS>   Project-specific patterns, naming
<GOTCHAS>       Non-obvious issues and solutions to recurring problems
<TESTING>       Test organisation, special requirements
```

Use 2-4 sections. Only include what adds value.

## What to Include

**Architectural decisions**: Why microservices over monolith, event-driven patterns, state management

**Non-obvious conventions**:
- "Use `_internal` suffix for private APIs not caught by linter"
- "Date fields always UTC, formatting happens client-side"
- "Avoid ORM for reports, use raw SQL in `/queries`"

**Recurring issues**:
- "TypeError in auth: ensure `verify()` uses Buffer.from(secret, 'base64')"
- "Cache race condition: acquire lock before checking status"

**Project patterns**: Error handling, logging, API versioning, migrations

## What to Exclude

- **Line numbers**: Files change, references break. Use descriptive paths: "in `src/auth/middleware.ts`" not "line 42"
- **Obvious information**: "We use React" (visible in package.json)
- **Setup steps**: Belongs in README unless highly non-standard
- **Generic advice**: "Write good tests" adds no project-specific value
- **Temporary notes**: "TODO: refactor this" belongs in code comments
- **Duplicate content**: If it's in README, don't repeat it

## Anti-Patterns

**Code style guidelines**: Don't document formatting rules, naming conventions, or code patterns that linters enforce. Use ESLint, Prettier, Black, golangci-lint, or similar tools. LLMs are in-context learners and will pick up patterns from codebase exploration. Configure Claude Code Hooks to run formatters if needed.

**Task-specific minutiae**: Database schemas, API specifications, deployment procedures belong in their own documentation. Link to them from CLAUDE.md rather than duplicating content.

**Kitchen sink approach**: Not every gotcha needs CLAUDE.md. Ask: "Is this relevant across most coding sessions?" If no, it belongs in code comments or specific documentation files.

## Linking to Existing Documentation

Point to existing docs rather than duplicating content. Provide context about when to read them:

**Good**:
```xml
<ARCHITECTURE>
Event-driven architecture using AWS EventBridge.

- For database schema: see src/database/SCHEMA.md when working with data models
- For auth flows: see src/auth/README.md when working with authentication
</ARCHITECTURE>
```

**Bad**: Copying schema tables, pasting deployment steps, or duplicating API flows into CLAUDE.md

Use `file:line` references for specific code: "See error handling in src/utils/errors.ts:45-67"

## Writing Style

**Be specific**:
- ❌ "Use caution with the authentication system"
- ✅ "Auth tokens expire after 1 hour. Background jobs must refresh tokens using `refreshToken()` in `src/auth/refresh.ts`"

**Be concise**:
- ❌ "It's important to note that when working with our database layer, you should be aware that..."
- ✅ "Database queries: Use Prisma for CRUD, raw SQL for complex reports in `/queries`"

**Use active voice**:
- ❌ "Migrations should be run before deployment"
- ✅ "Run migrations before deployment: `npm run migrate:prod`"

## When to Update

Add to CLAUDE.md when:
- Discovering a non-obvious pattern discovered after codebase exploration
- Solving an issue that took significant investigation that will be encountered again by other agents
- Finding a gotcha that's not immediately clear from code

Don't add:
- One-off fixes for specific bugs
- Information easily found in existing docs
- Temporary workarounds (these belong in code comments)
- Verbose descriptions or explanations

## Spelling Conventions

Always use Australian English spelling

## Example Structure

```xml
<ARCHITECTURE>
Event-driven architecture using AWS EventBridge. Services communicate via events, not direct calls.

Auth: JWT tokens with refresh mechanism. See src/auth/README.md for detailed flows when working on authentication.
Database schema and relationships: see src/database/SCHEMA.md when working with data models.
</ARCHITECTURE>

<CONVENTIONS>
- API routes: Plural nouns (`/users`, `/orders`), no verbs in paths
- Error codes: 4-digit format `ERRR-1001`, defined in src/errors/codes.ts
- Feature flags: Check in middleware, not in business logic
- Dates: Always UTC in database, format client-side via src/utils/dates.ts
</CONVENTIONS>

<GOTCHAS>
**Cache race conditions**: Always acquire lock before checking cache status

**Background job authentication**: Tokens expire after 1 hour. Refresh using
`refreshToken()` in src/auth/refresh.ts before making API calls.
</GOTCHAS>

<TESTING>
Run `make test` before committing. Integration tests require Docker.
</TESTING>
```

## Token Budget

Aim for 1k-4k tokens for CLAUDE.md. Most projects fit in 100-300 lines. If exceeding:
1. Reword to be more concise
2. Remove generic advice
3. Ensure there's no duplicated content

Check token count: `ingest CLAUDE.md` (if available)

## Review Checklist

Before finalising:
- [ ] Wording is concise and not duplicated
- [ ] Sections only add non-obvious value
- [ ] No code style guidelines (use linters instead)
- [ ] Links to existing docs rather than duplicating them
- [ ] No vague or overly verbose guidance
- [ ] No temporary notes or TODOs (unless requested by the user)
- [ ] No line numbers in file references
- [ ] Focused on stable, long-term patterns
