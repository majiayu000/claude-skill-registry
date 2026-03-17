---
name: implement-and-test
description: Implement feature with interleaved testing
user-invocable: true
---

# Implement Feature with Interleaved Testing

Implement the current feature by following the spec, with interleaved testing after each user story.

**User arguments:** $ARGUMENTS

## Instructions for Claude

You MUST follow these steps:

1. **Get current feature number** from branch:

   ```bash
   BRANCH=$(git rev-parse --abbrev-ref HEAD)
   NUM=$(echo "$BRANCH" | grep -oE 'alg-([0-9]+)' | grep -oE '[0-9]+')
   ```

2. **Read context files**:
   - Read `specs/alg-${NUM}-*/spec.md` - User stories, requirements, acceptance criteria (REQUIRED)
   - Check if `specs/alg-${NUM}-*/research.md` exists - Implementation patterns, files to modify (OPTIONAL)

3. **Create a todo list** with all user stories from the spec (P1 first, then P2, P3)

4. **For each user story**, follow this interleaved pattern:
   - Mark the todo as in_progress
   - Implement the functionality (follow research.md patterns if present, otherwise existing codebase patterns)
   - Commit implementation: `git commit -m "feat(scope): description ALG-${NUM}"`
   - Write unit tests for the implemented functionality
   - Write integration tests if needed (multi-component, database, API, or e2e)
   - Run tests: `npm test --workspaces --if-present`
   - Fix any failing tests before proceeding
   - Commit tests: `git commit -m "test(scope): description ALG-${NUM}"`
   - Mark the todo as completed

5. **Final verification**:
   - Run: `npm run type-check --workspaces --if-present`
   - Run: `npm test --workspaces --if-present`
   - Ensure all checks pass

**CRITICAL:** Do NOT batch all implementation then all tests. Interleave them - implement one story, test it, commit, then move to the next.

---

## Commit Conventions

Follow [Conventional Commits](https://www.conventionalcommits.org/):

**Types:** `feat`, `fix`, `test`, `refactor`, `perf`, `docs`, `chore`, `ci`, `build`

**Examples:**

```bash
git commit -m "feat(search): add semantic search service ALG-27"
git commit -m "test(search): add semantic search tests ALG-27"
git commit -m "fix(api): handle null response from Tidal ALG-27"
```

## When to Write Integration Tests

Write integration tests when the user story involves:

- Database operations (TypeORM entities, queries)
- External API calls (Tidal, Qdrant, etc.)
- Multi-service coordination
- GraphQL resolver chains
- End-to-end user flows
