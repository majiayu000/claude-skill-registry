---
name: ralph-prompt-single-task
description: Generate Ralph-compatible prompts for single implementation tasks. Creates prompts with clear completion criteria, automatic verification, and TDD approach. Use when creating prompts for bug fixes, single features, refactoring tasks, or any focused implementation that can be completed in one session.
---

# Ralph Prompt Generator: Single Task

## Overview

Generates well-structured prompts optimized for the Ralph Wiggum technique for single, focused tasks. These prompts include clear completion criteria, automatic verification (tests), self-correction loops, and proper `<promise>` completion tags.

**Best For:**
- Bug fixes with clear success criteria
- Single feature implementations
- Refactoring tasks
- Adding tests for existing code
- Documentation for specific modules
- Performance optimizations with measurable targets

**Ralph Philosophy**: This generator embraces the principle that failures are deterministic and fixable. Each iteration learns from the previous one. Don't fear failures—they're expected and provide data for improvement through prompt tuning.

## Quick Start

**Input Required:**
1. Task description (what needs to be done)
2. Success criteria (how to verify completion)
3. Completion promise text (the phrase that signals done)

**Generate prompt with:**
```
Generate a Ralph prompt for: [task description]
Success criteria: [how to verify]
Promise: [completion phrase]
```

## Prompt Generation Workflow

### Step 1: Analyze the Task

Identify these elements:
- **Action**: What specific work needs to be done?
- **Scope**: What files/modules are affected?
- **Verification**: How can success be automatically verified?
- **Edge cases**: What could go wrong?

### Step 2: Define Completion Criteria

**Good completion criteria are:**
- Measurable (tests pass, no errors, specific output)
- Verifiable automatically (not subjective)
- Binary (clearly done or not done)

**Examples:**
| Task Type | Good Criteria | Bad Criteria |
|-----------|---------------|--------------|
| Bug fix | "Tests pass, bug no longer reproducible" | "Bug is fixed" |
| Feature | "All CRUD endpoints return 200, tests pass" | "Feature works" |
| Refactor | "All tests pass, code uses new pattern" | "Code is cleaner" |

### Step 3: Structure the Prompt

Use this template:

```markdown
# Task: [Clear Task Title]

## Objective
[1-2 sentence clear description of what needs to be accomplished]

## Context
[Brief background - what exists, why this is needed]

## Requirements
1. [Specific requirement 1]
2. [Specific requirement 2]
3. [Specific requirement 3]

## Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

## Verification Steps
1. [How to verify criterion 1]
2. [How to verify criterion 2]
3. [How to verify criterion 3]

## TDD Approach
1. Write/identify failing tests for the requirement
2. Implement the solution
3. Run tests: `[test command]`
4. If tests fail, analyze output and fix
5. Repeat until all tests pass

## Completion
When ALL of the following are true:
- All success criteria met (checklist above)
- All tests passing
- No regressions introduced

Output: <promise>[COMPLETION_PHRASE]</promise>

## If Stuck
After multiple iterations without progress:
- Document what's blocking progress
- List approaches attempted
- Identify specific error or issue
- Do NOT output false promise - continue iterating or wait for max-iterations
```

### Step 4: Add Verification Commands

Include specific commands to verify success:

```markdown
## Verification Commands
```bash
# Run tests
npm test
# or
pytest tests/

# Check for errors
npm run lint
# or
ruff check .

# Verify specific functionality
curl -X GET http://localhost:3000/api/endpoint
```
```

## Example Prompts

### Example 1: Bug Fix

**Input:**
- Task: Fix authentication token refresh race condition
- Verification: Auth tests pass, no 401 errors in logs
- Promise: AUTH_FIX_COMPLETE

**Generated Prompt:**

```markdown
# Task: Fix Authentication Token Refresh Race Condition

## Objective
Fix the race condition in token refresh that causes intermittent 401 errors when multiple requests trigger refresh simultaneously.

## Context
The auth module in `src/auth/` handles JWT token refresh. When a token expires, multiple concurrent requests may all attempt to refresh, causing a race condition where some requests fail with 401.

## Requirements
1. Implement token refresh locking/queuing mechanism
2. Ensure concurrent requests wait for single refresh
3. Maintain backward compatibility with existing auth flow
4. Add tests covering concurrent refresh scenario

## Success Criteria
- [ ] All existing auth tests pass
- [ ] New concurrent refresh test passes
- [ ] No 401 errors in integration test logs
- [ ] Token refresh happens only once per expiration

## Verification Steps
1. Run auth tests: `npm test -- --grep "auth"`
2. Run concurrent refresh test: `npm test -- --grep "concurrent"`
3. Check logs for 401 after integration test
4. Verify single refresh in logs during concurrent requests

## TDD Approach
1. Write test for concurrent token refresh scenario
2. Verify test fails with current implementation
3. Implement locking mechanism
4. Run tests: `npm test`
5. If tests fail, analyze and fix
6. Repeat until all pass

## Completion
When ALL of the following are true:
- All auth tests passing (including new concurrent test)
- Integration tests show no 401 errors
- Single refresh verified in logs

Output: <promise>AUTH_FIX_COMPLETE</promise>

## If Stuck
After multiple iterations:
- Document the specific race condition behavior
- List locking approaches tried
- Identify where locks are failing
- Do NOT output false promise
```

### Example 2: Feature Implementation

**Input:**
- Task: Add pagination to /api/users endpoint
- Verification: Pagination params work, tests pass
- Promise: PAGINATION_DONE

**Generated Prompt:**

```markdown
# Task: Add Pagination to Users Endpoint

## Objective
Implement offset-based pagination for GET /api/users endpoint with page, limit, and total count.

## Context
The users endpoint in `src/routes/users.ts` currently returns all users. As the user base grows, this needs pagination for performance.

## Requirements
1. Accept `page` (default 1) and `limit` (default 20, max 100) query params
2. Return paginated response with metadata: { data: [], page, limit, total, totalPages }
3. Handle edge cases: invalid params, page beyond data, empty results
4. Add comprehensive tests for pagination

## Success Criteria
- [ ] GET /api/users returns paginated response
- [ ] `page` and `limit` query params work correctly
- [ ] Response includes correct metadata (total, totalPages)
- [ ] Edge cases handled gracefully
- [ ] All new pagination tests pass
- [ ] Existing user tests still pass

## Verification Steps
1. Run tests: `npm test -- --grep "users"`
2. Manual verification:
   - `curl localhost:3000/api/users?page=1&limit=10`
   - `curl localhost:3000/api/users?page=999&limit=10`
   - `curl localhost:3000/api/users?limit=200`

## TDD Approach
1. Write tests for pagination behavior
2. Verify tests fail
3. Implement pagination logic
4. Run tests: `npm test`
5. If failures, fix and retry
6. Test edge cases manually

## Completion
When ALL of the following are true:
- All pagination tests pass
- All existing user tests pass
- Manual verification shows correct behavior
- Edge cases handled (returns empty for page beyond data)

Output: <promise>PAGINATION_DONE</promise>

## If Stuck
Document:
- Which tests are failing and why
- What pagination approach was tried
- Specific error messages
- Do NOT output false promise
```

### Example 3: Refactoring Task

**Input:**
- Task: Convert callbacks to async/await in database module
- Verification: All DB tests pass, no callback patterns remain
- Promise: ASYNC_REFACTOR_COMPLETE

**Generated Prompt:**

```markdown
# Task: Convert Database Module to Async/Await

## Objective
Refactor all callback-based database operations in `src/db/` to use async/await pattern for improved readability and error handling.

## Context
The database module uses callback patterns from legacy code. Modern async/await improves code clarity and makes error handling more consistent.

## Requirements
1. Convert all callback-based functions to async/await
2. Replace callback error handling with try/catch
3. Update all callers to use await
4. Maintain identical external API behavior
5. No callback patterns remaining in db module

## Success Criteria
- [ ] All database functions use async/await
- [ ] No callback patterns in src/db/*.ts files
- [ ] All existing database tests pass
- [ ] All integration tests pass
- [ ] No TypeScript errors

## Verification Steps
1. Run tests: `npm test -- --grep "database"`
2. Search for callbacks: `grep -r "callback\|cb)" src/db/`
3. TypeScript check: `npm run typecheck`
4. Integration tests: `npm run test:integration`

## TDD Approach
1. Run all tests - ensure baseline passes
2. Convert one function at a time
3. Run tests after each conversion
4. If failures, fix before continuing
5. After all conversions, verify no callbacks remain

## Completion
When ALL of the following are true:
- All database tests passing
- grep for callbacks returns empty
- TypeScript compilation succeeds
- Integration tests pass

Output: <promise>ASYNC_REFACTOR_COMPLETE</promise>

## If Stuck
Document:
- Which function is causing issues
- The specific error or test failure
- What conversion approach was tried
- Do NOT output false promise
```

## Best Practices

### DO:
- Use specific, measurable success criteria
- Include actual test commands
- Add verification steps for each criterion
- Include TDD approach for self-correction
- Set clear completion conditions
- Provide "If Stuck" guidance

### DON'T:
- Use vague criteria ("make it work")
- Skip verification commands
- Forget edge cases
- Make subjective success criteria
- Allow escape without genuine completion

## Integration with Ralph Loop

**Run your generated prompt:**
```bash
/ralph-wiggum:ralph-loop "[paste generated prompt]" --completion-promise "YOUR_PROMISE" --max-iterations 30
```

**Recommended settings:**
- Bug fixes: `--max-iterations 15-20`
- Features: `--max-iterations 25-35`
- Refactoring: `--max-iterations 20-30`

## Validation Checklist

Before using a generated prompt, verify:
- [ ] Task has single, focused objective
- [ ] Success criteria are measurable
- [ ] Verification commands are specific and runnable
- [ ] TDD approach is defined
- [ ] Completion promise is clear and specific
- [ ] "If Stuck" section provides guidance

---

For multi-task prompts, see `ralph-prompt-multi-task`.
For project-level prompts, see `ralph-prompt-project`.
For research/analysis prompts, see `ralph-prompt-research`.
