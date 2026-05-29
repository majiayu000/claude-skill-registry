---
name: ralph-loop-guide
description: Ralph Loop Best Practices - Guidelines for effective autonomous iteration. Based on Anthropic's official ralph-loop plugin. Helps design prompts for iterative AI development with clear completion signals.
allowed-tools: Read
---

# Ralph Loop Best Practices Guide

This skill provides guidelines for effective autonomous iteration using the Ralph Wiggum pattern, based on Anthropic's official ralph-loop plugin.

## How Ralph Loop Works

The Ralph Loop is a methodology for iterative AI development through self-referential feedback loops:

1. **The prompt never changes between iterations**
2. **Claude's previous work persists in files**
3. **Each cycle, the AI sees modified files and git history**
4. **Enables autonomous refinement without manual re-prompting**

## Effective Ralph Prompt Design

### Required Elements

1. **Clear Completion Signal**
   ```markdown
   ## Completion Criteria
   - [ ] All unit tests pass (npm test)
   - [ ] Build succeeds (npm run build)
   - [ ] Coverage ≥80% (npm run coverage)
   - [ ] No TypeScript errors (npx tsc --noEmit)

   When ALL criteria are met, output: "RALPH_COMPLETE: All tasks done"
   ```

2. **Incremental Phases**
   ```markdown
   ## Implementation Phases

   ### Phase 1: Foundation
   - Create database schema
   - Set up repository layer
   - Write unit tests for repository

   ### Phase 2: Business Logic
   - Implement service layer
   - Add validation
   - Write service tests

   ### Phase 3: API Layer
   - Create endpoints
   - Add input validation
   - Write API tests
   - Run full test suite
   ```

3. **Self-Correction Cycles**
   ```markdown
   ## On Each Iteration

   1. Run tests: `npm test`
   2. If tests fail:
      - Read error messages
      - Fix the failing code
      - Run tests again
   3. If tests pass:
      - Check coverage: `npm run coverage`
      - If coverage < 80%, add more tests
      - If coverage ≥ 80%, proceed to next phase
   ```

4. **Safety Limits**
   ```markdown
   ## Safety Rules

   - Maximum 100 iterations per phase
   - If stuck for 5 iterations on same error, ask for help
   - Never delete test files
   - Always commit working state before major changes
   ```

## Good Ralph Prompts

### Example 1: API Development
```markdown
# Task: Build User Authentication API

## Context
- Node.js + Express + TypeScript
- PostgreSQL with Prisma
- JWT authentication

## Phases

### Phase 1: Database (iterations 1-10)
Create Prisma schema for User model with:
- id, email (unique), passwordHash, createdAt, updatedAt

Run: `npx prisma migrate dev`
Test: Schema validates with `npx prisma validate`

### Phase 2: Repository (iterations 11-25)
Create UserRepository with:
- create(email, password) → User
- findByEmail(email) → User | null
- findById(id) → User | null

Tests: All repository tests pass

### Phase 3: Service (iterations 26-45)
Create AuthService with:
- register(email, password) → { user, token }
- login(email, password) → { user, token }
- validateToken(token) → User

Tests: All service tests pass

### Phase 4: Routes (iterations 46-70)
Create routes:
- POST /auth/register
- POST /auth/login
- GET /auth/me (protected)

Tests: All API tests pass with supertest

### Phase 5: Integration (iterations 71-100)
- Full E2E flow works
- Error handling for all edge cases
- Rate limiting on auth endpoints

## Completion
When `npm test` passes with 0 failures AND coverage ≥80%,
output: "RALPH_COMPLETE"
```

### Example 2: Refactoring Task
```markdown
# Task: Refactor Legacy Auth Module

## Current State
- Monolithic auth.js with 500 lines
- No tests
- Mixed concerns

## Target State
- Separate files: auth-service.ts, user-repository.ts, token-utils.ts
- 100% backward compatible
- 80%+ test coverage

## Iteration Loop

1. Read current auth.js
2. Identify one function to extract
3. Create new file with extracted function
4. Update imports in auth.js
5. Run existing integration tests
6. If tests fail, fix and retry
7. If tests pass, proceed to next function

## Completion Criteria
- [ ] auth.js < 100 lines
- [ ] All functions have dedicated files
- [ ] All tests pass
- [ ] No breaking changes to API

Output "RALPH_COMPLETE" when done.
```

## When Ralph Works

| Task Type | Suitability | Reason |
|-----------|------------|--------|
| API development | ✅ Excellent | Clear test-driven feedback |
| Refactoring | ✅ Excellent | Tests verify each step |
| Bug fixing | ✅ Good | Reproduce → fix → verify cycle |
| Test writing | ✅ Good | Coverage metrics as feedback |
| Documentation | ⚠️ Limited | No automated verification |
| UI development | ⚠️ Limited | Visual verification hard |
| Design decisions | ❌ Poor | Requires human judgment |
| One-time scripts | ❌ Poor | No iteration benefit |

## When NOT to Use Ralph

1. **Subjective decisions** - No objective completion signal
2. **One-time operations** - No benefit from iteration
3. **Ambiguous requirements** - Will spin without progress
4. **Security-critical code** - Needs human review
5. **Production deployments** - Too risky for autonomous action

## Anti-Patterns to Avoid

### 1. Vague Completion Criteria
```markdown
# BAD
Complete when the code looks good.

# GOOD
Complete when:
- npm test exits with code 0
- npm run build succeeds
- No TypeScript errors (npx tsc --noEmit)
```

### 2. No Phase Boundaries
```markdown
# BAD
Build the entire application.

# GOOD
Phase 1: Database schema (test: migrations apply)
Phase 2: Repository layer (test: unit tests pass)
Phase 3: Service layer (test: integration tests pass)
```

### 3. Missing Error Recovery
```markdown
# BAD
If something fails, figure it out.

# GOOD
If tests fail:
1. Read the error message
2. Identify the failing file:line
3. Fix the specific issue
4. Run tests again
5. If same error after 3 attempts, try alternative approach
```

### 4. No Safety Limits
```markdown
# BAD
Keep going until done.

# GOOD
- Max 100 iterations total
- Max 10 retries per failing test
- Checkpoint every 25 iterations
```

## Integration with SpecWeave

SpecWeave's `/sw:auto` command implements Ralph Loop with:

1. **Tasks.md as Completion Checklist**
   - Each `[ ] pending` task is a completion criterion
   - Auto mode continues until all `[x] completed`

2. **Built-in Quality Gates**
   - `--build` - Build must pass
   - `--tests` - Tests must pass
   - `--e2e` - E2E tests must pass
   - `--cov N` - Coverage threshold

3. **Automatic Phase Management**
   - Tasks grouped by User Story
   - Progress tracked in metadata.json
   - External sync keeps stakeholders informed

## Real-World Success Stories

From Anthropic's documentation:
- "6 repositories overnight"
- "$50k contract for $297 in API costs"
- "259 PRs, 497 commits, 40,000 lines in one month without opening IDE"

The key to success: **Well-defined tasks with automated verification**.
