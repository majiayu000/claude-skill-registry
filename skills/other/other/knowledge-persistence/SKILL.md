---
name: knowledge-persistence
description: >
  Patterns for learning from corrections, capturing instincts, extracting stable patterns,
  and building cross-session knowledge. Use when the user corrects you, when you discover
  a recurring pattern, or when insights should persist beyond the current session.
---

# Knowledge Persistence

Knowledge persistence is about capturing what you learn during sessions so future sessions start smarter. This includes corrections, discovered patterns, user preferences, and debugging insights.

## When to Use
- User corrects a mistake originating from stored memory
- You discover a pattern that applies broadly to the project
- A debugging session reveals a non-obvious root cause
- User states a preference ("always do X", "never use Y")
- You solve a problem that is likely to recur

## Core Patterns

### Learning from Corrections

When the user corrects you, the correction invalidates stored knowledge. Fix the source immediately:

```
User: "We don't use Express anymore, we migrated to Fastify"

# WRONG: Just acknowledge and continue
"Got it, I'll use Fastify."

# RIGHT: Update memory, then continue
1. Edit memory/MEMORY.md:
   Old: "Framework: Express"
   New: "Framework: Fastify (migrated from Express)"

2. Check topic files for stale Express references:
   Edit memory/architecture.md if it mentions Express

3. Then continue with correct context
```

The correction means the stored memory is wrong. Fix it at the source before continuing, so the same mistake does not repeat.

### Instinct Capture

When you notice yourself repeatedly making the same decision, capture it:

```markdown
# memory/patterns.md

## Project-Specific Instincts

### Error Handling
- This project always wraps service calls in try/catch at the route level
- Errors are logged with structuredLogger.error(), not console.error()
- All error responses use the AppError class from src/errors.ts

### Naming
- Database functions: findX, createX, updateX, deleteX (not getX, setX)
- Route handlers: handleGetUser, handleCreateUser (not getUser, createUser)
- Test files: same name with .test.ts suffix, same directory
```

### Pattern Extraction

After seeing a pattern in 3+ locations, extract it to memory:

```
# Observation across multiple files:
# - src/routes/users.ts uses Zod schema + validate middleware
# - src/routes/posts.ts uses Zod schema + validate middleware
# - src/routes/comments.ts uses Zod schema + validate middleware

# Extract to memory/patterns.md:
## Input Validation Pattern
All route handlers use Zod schemas for request validation:
1. Schema defined in src/schemas/{resource}.ts
2. validate(schema) middleware applied to route
3. Handler receives typed, validated body via req.validated

Example:
  const schema = z.object({ title: z.string().min(1) })
  router.post('/', validate(schema), handleCreatePost)
```

### Cross-Session Knowledge Building

Structure knowledge to be useful across sessions:

```markdown
# memory/debugging.md

## Recurring Issues and Solutions

### "Cannot find module" after adding new file
- Cause: TypeScript path aliases not updated in tsconfig.json
- Fix: Add path to compilerOptions.paths in tsconfig.json
- Also check: jest.config.ts moduleNameMapper if tests fail

### Database connection timeout in tests
- Cause: Test database pool not closed after test suite
- Fix: Add afterAll(() => db.destroy()) in test setup
- File: src/test/setup.ts

### Build fails with "heap out of memory"
- Cause: TypeScript compiling node_modules due to missing exclude
- Fix: Ensure tsconfig.json has "exclude": ["node_modules", "dist"]
```

### Preference Capture

When a user states a preference, save it immediately:

```
User: "Always use bun instead of npm"

# Save to memory/MEMORY.md under User Preferences:
## User Preferences
- Package manager: bun (not npm or yarn)
- Always use named exports (no default exports)
- Prefers functional style over classes
- Run tests before committing
```

Preferences are explicit user requests — save them after a single interaction, no need to wait for repetition.

### Knowledge Confidence Levels

Not all learned information is equally reliable:

```markdown
# HIGH confidence (save immediately):
- User explicitly states a preference
- Pattern confirmed in 3+ files
- Architectural decision documented in code comments or README

# MEDIUM confidence (save with caveat):
- Pattern seen in 2 files (note: "observed in X and Y, may be broader")
- Behavior inferred from test expectations

# LOW confidence (do NOT save):
- Pattern seen in only 1 file
- Guess about project conventions from naming alone
- Inferred from a single error message
```

### Knowledge Lifecycle

Memory entries have a lifecycle:

```
Discovery -> Verification -> Recording -> Maintenance -> Retirement

1. Discovery: Notice a pattern or receive a correction
2. Verification: Confirm across multiple sources (unless explicit user request)
3. Recording: Save to appropriate memory file
4. Maintenance: Update when corrections arrive or project evolves
5. Retirement: Remove when no longer applicable (framework migration, etc.)
```

## Anti-Patterns

- **Saving everything**: Not every observation deserves persistence. A one-off fix for a typo is not worth saving. Focus on recurring patterns and explicit preferences.
- **Ignoring corrections**: When the user says "that is wrong", you must update memory. Acknowledging without updating means the error repeats next session.
- **Speculative memories**: "I think this project probably uses X" based on one file read is not reliable enough to save. Verify first.
- **Stale memories**: Never-updated memories become lies. When you notice information is outdated, fix it immediately.
- **Chronological dumps**: "On Tuesday I learned X, on Wednesday I learned Y" is useless. Organize by topic so information is findable.

## Quick Reference

| Trigger | Action | Confidence Required |
|---------|--------|-------------------|
| User says "remember X" | Save immediately | Explicit request |
| User corrects you | Update source immediately | Correction = verified |
| Pattern in 3+ files | Save as confirmed pattern | High |
| Pattern in 2 files | Save with caveat | Medium |
| Pattern in 1 file | Do not save | Too low |
| Debugging solution | Save if likely to recur | Medium-High |

**Corrections are urgent**: Fix the memory source before continuing.
**Preferences are immediate**: One explicit request is enough to save.
**Patterns need evidence**: Wait for 3+ occurrences before extracting.
**Organize by topic**: Semantic grouping, never chronological.
