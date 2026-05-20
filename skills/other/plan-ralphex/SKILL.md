---
name: plan-ralphex
description: Create comprehensive implementation plans for features using the ralphex format. Plans include research, documentation, tests, and step-by-step tasks.
---

# Plan Document Creator

You are creating a comprehensive implementation plan for a software feature. The plan will be executed by Claude Code agents via [ralphex](https://github.com/umputun/ralphex), so it must be detailed, unambiguous, and self-contained.

## Output Location

Write the plan to: `ai/tickets/`

Use descriptive filenames: `YYYY-MM-DD-feature-name.md` (e.g., `2026-01-26-user-authentication.md`)

## Plan Structure

```markdown
# Plan: [Feature Name]

## Overview
[2-4 sentences describing what will be implemented and why]

## Context
[Information gathered during codebase exploration]
- Files involved: [list key files that will be modified]
- Dependencies: [external libraries, APIs, services needed]
- Related code: [existing patterns to follow or extend]

## Development Approach
- **Testing approach**: TDD - write tests first
- Complete each task fully before moving to the next
- Make small, focused changes
- **CRITICAL: every task MUST include new/updated tests**
- **CRITICAL: all tests must pass before starting next task**
- **CRITICAL: update this plan file when scope changes**

## Validation Commands
- `[test command]`
- `[lint command]`
- `[build command]`

### Task 1: [Task Name]
- [ ] [Specific action item]
- [ ] [Another action item]
- [ ] Write/update tests for this task
- [ ] Run `[validation command]` - must pass before next task

### Task 2: [Task Name]
...

## Technical Details
[Code examples, data structures, API contracts, diagrams]

## Edge Cases and Error Handling
[Document corner cases and how they should be handled]

## Post-Completion Verification
[Manual verification steps after all tasks complete]
```

## Your Process

### Phase 1: Clarify Requirements (if needed)

Before exploring code, ensure you understand WHAT to build. If the user's request is already clear and specific, skip to Phase 2.

Ask only questions that affect what you'll search for:
- "Should this feature be accessible to all users or require authentication?"
- "What should happen when [core operation] fails - retry, error message, or silent fallback?"
- "Does this need to work with [external system] or be standalone?"

**Keep it minimal.** Don't ask abstract questions - ask only what genuinely blocks your ability to explore effectively. Many questions are better asked in Phase 3 when you have codebase context.

### Phase 2: Explore Codebase

Thoroughly explore the codebase to build context:

1. **Find related code**: Search for similar features, patterns, or modules
2. **Understand architecture**: How does data flow? What are the layers?
3. **Identify touch points**: Which files will need changes?
4. **Review existing tests**: What testing patterns are used?
5. **Check documentation**: What project conventions exist (CLAUDE.md, README)?
6. **Discover constraints**: What libraries are already used? What patterns are established?

Use the Explore agent for comprehensive codebase analysis. This exploration informs what questions to ask.

**Before asking questions**, briefly summarize your findings to the user:
- Key files and patterns discovered
- Existing approaches that could apply
- Constraints or limitations found
- Areas of uncertainty that need clarification

This gives the user context for your questions.

### Phase 3: Ask Implementation Questions

Now ask questions about HOW to build, grounded in what you discovered:

1. **Validate assumptions**: "I found X pattern in the codebase. Should we follow it for this feature?"
2. **Present options**: "Given the existing architecture, I see two approaches: A (pros/cons) or B (pros/cons). Which do you prefer?"
3. **Clarify ambiguities**: "The codebase uses Y for similar features, but the requirement mentions Z. Should we stick with Y or introduce Z?"
4. **Confirm scope**: "Based on my exploration, this will require changes to [files]. Is there anything I'm missing?"
5. **Edge cases**: "How should we handle [specific scenario discovered during exploration]?"
6. **Testing strategy**: "Tests in this area use [pattern]. Should we continue with this approach?"

Use the AskUserQuestion tool. Ask focused questions based on actual findings. Reference specific files, patterns, or constraints you discovered.

### Phase 4: Design Solution

Based on exploration and user answers:

1. **Choose approach**: Select implementation strategy with rationale
2. **Define data structures**: Specify types, interfaces, schemas
3. **Plan API contracts**: Define function signatures, endpoints, messages
4. **Identify risks**: What could go wrong? How to mitigate?
5. **Document decisions**: Record why this approach was chosen over alternatives

### Phase 5: Write the Plan

Create the plan document with:

1. **Clear tasks**: Each task is a coherent unit of work (2-10 checkboxes)
2. **Logical ordering**: Tasks build on each other; dependencies are clear
3. **Specific checkboxes**: Each checkbox is a concrete, verifiable action
4. **Embedded testing**: Every task includes test writing/updating
5. **Validation gates**: Each task ends with passing validation commands

## Task Writing Guidelines

### Good Task Structure
```markdown
### Task 3: Implement user validation middleware
- [ ] Create `src/middleware/validate-user.ts` with `validateUser()` function
- [ ] Validate JWT token from Authorization header
- [ ] Return 401 for missing/invalid tokens, 403 for expired tokens
- [ ] Add middleware to protected routes in `src/routes/index.ts`
- [ ] Write unit tests in `src/middleware/validate-user.test.ts`
- [ ] Write integration test for protected endpoint
- [ ] Run `bun test:all` and `bun run typecheck` - must pass before next task
```

### Bad Task Structure (avoid)
```markdown
### Task 3: Add auth
- [ ] Implement authentication
- [ ] Add tests
```

### Checkbox Guidelines

Each checkbox should be:
- **Specific**: Name exact files, functions, endpoints
- **Verifiable**: Clear success criteria
- **Atomic**: One logical action per checkbox
- **Ordered**: Later checkboxes may depend on earlier ones

Include checkboxes for:
- Implementation steps
- Test creation/updates
- Error handling
- Edge case coverage
- Documentation updates (inline comments for complex logic)

## Testing Requirements

Every task MUST include testing checkboxes:

```markdown
- [ ] Write unit tests for [specific function/module]
- [ ] Write integration tests for [specific flow]
- [ ] Add test cases for edge cases: [list them]
- [ ] Run `[test command]` - must pass before next task
```

Test coverage should include:
- Happy path scenarios
- Error conditions
- Edge cases (empty inputs, boundary values, concurrent access)
- Integration with adjacent components

## Documentation Requirements

The final task should always update documentation. Example:

```markdown
### Task N: [Final] Update documentation
- [ ] Update README.md with new feature description
- [ ] Update CLAUDE.md with new patterns/conventions
- [ ] Add inline documentation for complex functions
- [ ] Update API documentation
```

## Technical Details Section

Include concrete specifications. Example:

```markdown
## Technical Details

### Data Types
```typescript
interface UserSession {
  userId: string;
  token: string;
  expiresAt: Date;
  permissions: string[];
}
```

### API Endpoints
| Method | Path | Request | Response |
|--------|------|---------|----------|
| POST | /api/login | `{email, password}` | `{token, expiresAt}` |
| POST | /api/logout | - | `{success: true}` |

### Error Codes
| Code | Meaning | Action |
|------|---------|--------|
| 401 | Unauthorized | Redirect to login |
| 403 | Forbidden | Show access denied |


## Edge Cases Section

Explicitly document corner cases. Example:

```markdown
## Edge Cases and Error Handling

### Authentication Edge Cases
- **Expired token during request**: Return 401, client should refresh
- **Concurrent logout**: Invalidate all sessions, not just current
- **Invalid refresh token**: Clear all tokens, force re-login

### Data Validation Edge Cases
- **Empty string vs null**: Treat empty strings as missing values
- **Unicode in usernames**: Allow, but normalize for comparison
- **Extremely long inputs**: Truncate at 1000 chars with warning
```

## Validation Commands

Always include commands that verify correctness:

```markdown
## Validation Commands
- `bun test:all`                    # Run all tests
- `bun run typecheck`           # Type checking
- `bun run lint`                # Linting
- `bun run build`               # Verify build succeeds
```

## Final Checklist

Before presenting the plan to the user, verify:

- [ ] Overview clearly explains what and why
- [ ] Context lists all files that will be modified
- [ ] Validation commands are correct for this project
- [ ] Each task has 2-10 specific checkboxes
- [ ] Every task includes test checkboxes
- [ ] Every task ends with validation gate
- [ ] Technical details include code examples
- [ ] Edge cases are documented
- [ ] Final task updates documentation
- [ ] Post-completion verification steps defined
