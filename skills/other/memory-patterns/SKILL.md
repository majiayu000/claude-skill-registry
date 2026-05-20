---
name: memory-patterns
description: >
  Patterns for structuring MEMORY.md and topic-based memory files for Claude Code
  persistent memory. Use when the user asks about remembering things across sessions,
  wants to organize project knowledge, or needs guidance on what to save vs not save.
---

# Memory Patterns

Claude Code's auto memory system persists knowledge across sessions via files in the memory directory. MEMORY.md is always loaded into context; topic files store detailed notes referenced from MEMORY.md.

## When to Use
- User asks "remember this" or "always do X"
- User corrects a mistake that came from memory — update the source
- You discover stable project patterns worth persisting
- User asks about organizing cross-session knowledge
- You need to structure MEMORY.md or create topic files

## Core Patterns

### MEMORY.md Structure

MEMORY.md is the index file — always loaded, so it must stay concise (under 200 lines). Use it as a table of contents pointing to detailed topic files:

```markdown
# Project Memory

## Project Overview
- Name: acme-api
- Stack: Node.js, Express, PostgreSQL, TypeScript
- Test framework: Vitest
- Package manager: pnpm

## Key Conventions
- Use Zod for all input validation
- Repository pattern for database access
- All API responses follow ApiResponse<T> interface
- Feature branches: feat/description, fix/description

## Architecture
- See [architecture.md](./architecture.md) for service layout
- See [database.md](./database.md) for schema notes

## User Preferences
- Prefers functional style over classes
- Always use named exports (no default exports)
- Run tests before committing

## Known Issues
- See [debugging.md](./debugging.md) for recurring problems
```

### Topic File Organization

Create separate files for detailed knowledge. Link them from MEMORY.md:

```
memory/
  MEMORY.md              # Index (always loaded, < 200 lines)
  architecture.md        # Service layout, module boundaries
  database.md            # Schema notes, migration patterns
  debugging.md           # Recurring issues and solutions
  patterns.md            # Code patterns specific to this project
  api-conventions.md     # API design decisions
```

Each topic file should be self-contained:

```markdown
# Architecture Notes

## Service Layout
- src/services/ — Business logic, one file per domain
- src/routes/ — Express route handlers, thin layer
- src/db/ — Database access via repository pattern
- src/middleware/ — Auth, validation, error handling

## Module Boundaries
- Services never import from routes
- Routes call services, never DB directly
- Middleware is stateless

## Key Dependencies
- src/services/auth.ts depends on src/db/users.ts
- src/services/billing.ts depends on external Stripe SDK
```

### When to Save

Save to memory when:
- A pattern is confirmed across multiple interactions (not just one file)
- The user explicitly asks to remember something
- An architectural decision affects future work
- A debugging solution applies to a recurring problem
- User preferences are stated ("always use X", "never do Y")

### When NOT to Save

Do not save:
- Session-specific context (current task details, in-progress work)
- Information from a single file read that might be incomplete
- Speculative conclusions not verified against project docs
- Anything that duplicates CLAUDE.md instructions
- Temporary state or one-off fixes

### Update vs Create

Before creating a new memory entry, check if an existing one covers the topic:

```markdown
# WRONG: Creating duplicates
## Database Notes (added 2024-01-15)
Uses PostgreSQL with Prisma ORM.

## Database Info (added 2024-02-03)
Database is PostgreSQL. Uses Prisma for ORM.

# RIGHT: Update the existing entry
## Database
- PostgreSQL with Prisma ORM
- Migrations in prisma/migrations/
- Seed data in prisma/seed.ts
```

### Handling Corrections

When the user corrects something you stated from memory, update the source immediately:

```
User: "No, we switched from Prisma to Drizzle last month"

# IMMEDIATELY update MEMORY.md or the relevant topic file:
# Old: "Database: PostgreSQL with Prisma ORM"
# New: "Database: PostgreSQL with Drizzle ORM"
```

Never continue with incorrect memory. Fix the source first, then proceed.

### Semantic Organization

Group memories by topic, not by time:

```markdown
# WRONG: Chronological
## January 15
Learned that project uses TypeScript.
## January 16
Found out tests use Vitest.

# RIGHT: Semantic
## Tech Stack
- Language: TypeScript
- Test framework: Vitest
```

## Anti-Patterns

- **Bloated MEMORY.md**: Exceeding 200 lines means important information gets truncated. Move details to topic files and keep MEMORY.md as an index.
- **Saving speculative information**: Reading one file and concluding "the project uses pattern X" without verification leads to incorrect memories. Verify against multiple sources.
- **Duplicating CLAUDE.md**: If project instructions already exist in CLAUDE.md, do not repeat them in memory. Memory is for learned knowledge, not static configuration.
- **Never updating**: Memories rot. When you discover information is outdated, update or remove it immediately.
- **Saving session state**: "Currently working on the auth refactor" does not belong in memory. It is true now but meaningless next session.

## Quick Reference

| File | Purpose | Size Limit |
|------|---------|------------|
| MEMORY.md | Index, always loaded | < 200 lines |
| Topic files | Detailed knowledge | Unlimited |

**Save**: Stable patterns, user preferences, architecture decisions, recurring solutions
**Skip**: Session state, unverified guesses, CLAUDE.md duplicates
**Update**: When corrected, when information changes, when patterns evolve
**Organize**: By topic (semantic), not by date (chronological)
