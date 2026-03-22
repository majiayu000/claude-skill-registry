---
name: implement-plan
description: Execute implementation plans phase by phase
disable-model-invocation: true
---

# Implement Plan

Implement an approved plan following Test-Driven Development methodology.

## Getting Started

When given a plan path:
1. Read the plan completely (no limit/offset)
2. Check for existing checkmarks (✓ or [x]) indicating completed work
3. Read related specs/documentation referenced in the plan
4. Create a todo list to track progress through phases
5. Start implementing from the first unchecked phase

If no plan path provided, ask the user which plan to implement or list available plans.

## Implementation Philosophy

Follow the **Red, Green, Refactor** cycle:

1. **Red**: Write a failing test for the desired behavior
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Clean up code while keeping tests green

**Never skip the Red phase** - watching tests fail confirms they actually test something.

## Workflow

### For Each Phase:

#### Step 1: Read Phase Requirements

1. Read the phase section completely
2. Understand files to change and what changes are needed
3. Note the success criteria (automated and manual)
4. Check for any dependencies or prerequisites

#### Step 2: Write Tests First (TDD - RED)

1. Write test(s) that describe the desired behavior
2. Make tests as specific as possible
3. Run the tests - **confirm they fail** (and fail for the right reason)
4. If test doesn't fail, the test is wrong or code already works

```typescript
// Example: Write failing test first
describe('validateToken', () => {
  it('should accept valid JWT tokens', async () => {
    const token = 'valid.jwt.token'
    const result = await validateToken(token)
    expect(result.valid).toBe(true)
  })
})

// Run test: npm test
// ❌ FAILED: validateToken is not defined
// Good - fails for the right reason
```

#### Step 3: Implement Minimal Code (GREEN)

1. Write just enough code to make the test pass
2. Don't add features not tested yet
3. Resist the urge to "make it perfect" now
4. Run tests - **confirm they pass**

```typescript
// Minimal implementation to pass test
export async function validateToken(token: string) {
  const decoded = jwt.verify(token, SECRET)
  return { valid: true, userId: decoded.sub }
}

// Run test: npm test
// ✓ PASSED
```

#### Step 4: Refactor (if needed)

1. Clean up the code while tests stay green
2. Extract functions, improve names, remove duplication
3. Run tests after each refactor - **keep them green**
4. Stop when code is clean enough

```typescript
// Refactored with better error handling
export async function validateToken(token: string): Promise<TokenResult> {
  try {
    const decoded = jwt.verify(token, getSecret()) as JWTPayload
    return {
      valid: true,
      userId: decoded.sub
    }
  } catch (error) {
    return {
      valid: false,
      userId: null,
      error: error.message
    }
  }
}

// Run test: npm test
// ✓ Still passing after refactor
```

#### Step 5: Run Success Criteria Checks

**Automated verification:**
```bash
# Run all tests (not just the new ones)
npm test

# Type checking (if applicable)
npm run type-check  # or tsc --noEmit

# Linting (if applicable)
npm run lint

# Build (if applicable)
npm run build
```

**Manual verification:**
- Follow manual verification steps from the plan
- Actually perform the verification, don't skip it
- Note any issues or unexpected behaviors

#### Step 6: Mark Phase Complete

1. Check off completed items in the plan file
2. Update the plan with any learnings or deviations
3. Commit the changes for this phase (if appropriate)

#### Step 7: Inform User

```
Phase [N] Complete - Ready for Verification

Automated verification:
- [x] All tests pass (15 tests, 3 new)
- [x] Type checking passes
- [x] Build succeeds

Manual verification needed:
- [ ] [Manual step 1 from plan]
- [ ] [Manual step 2 from plan]

Changes made:
- src/auth/validate.ts:25-45 - Added validateToken function
- tests/auth/validate.test.ts:12-28 - Added 3 tests for token validation

Let me know when verified so I can proceed to Phase [N+1].
```

**Wait for user confirmation before proceeding to next phase.**

### Moving Between Phases

- Complete one phase before starting the next
- Don't work on multiple phases in parallel
- Each phase should leave the codebase in a working state
- If a phase is blocked, inform the user immediately

## When Things Don't Match Reality

If the plan doesn't match what you find:

```
Issue in Phase [N]:

Expected (from plan): [What the plan says]
Found (in codebase): [Actual situation]
Why this matters: [Impact explanation]

Options:
1. Adapt implementation to current reality
2. Update the plan to reflect new understanding
3. Ask user for guidance

How should I proceed?
```

**Important:** Don't blindly follow an outdated or incorrect plan. Reality wins.

## Resuming Work

If the plan has checkmarks indicating completed work:

1. **Trust completed work** - assume it's done correctly
2. **Start from first unchecked item** - don't redo completed work
3. **Verify previous work ONLY if**:
   - Something seems obviously broken
   - Tests are failing
   - Current phase depends on previous phase and seems incompatible
4. **Continue with Red-Green-Refactor** cycle from current phase

## Key Reminders

1. **Tests first, always** - Write test before implementation (TDD)
2. **Watch it fail** - Confirm test fails before implementing
3. **Minimal code** - Write just enough to pass the test
4. **Keep tests green** - All tests should pass after each change
5. **Refactor safely** - Only refactor when tests are green
6. **One phase at a time** - Complete and verify before moving on
7. **Mark progress** - Check off items as you complete them
8. **Verify thoroughly** - Actually run the verification steps

## Handling Common Situations

### Tests are already passing (someone implemented it):
```
Phase [N]: The tests I was about to write already pass. It appears this work was already completed.

Verification:
- [x] Tests exist and pass
- [x] Implementation matches plan requirements

Marking phase complete and moving to next phase.
```

### Can't make tests pass:
```
Phase [N]: Issue encountered

I wrote tests for [feature] but after [X] attempts, can't make them pass due to [specific reason].

Options:
1. Revise the approach (suggest alternative)
2. Update the plan (if requirements changed)
3. Need more research/context

How should we proceed?
```

### Found a better approach mid-implementation:
```
Phase [N]: Alternative approach discovered

While implementing [feature], I discovered [better pattern/approach].

Current plan: [Approach from plan]
Alternative: [New approach]
Tradeoffs: [Pros/cons]

Should I:
1. Continue with plan as written
2. Update plan and use new approach
3. Discuss further
```

### External dependency is broken/unavailable:
```
Phase [N]: Blocked by external dependency

Cannot proceed because [dependency] is [unavailable/broken/different than expected].

Impact: [What this blocks]
Workaround options: [If any]

Need guidance on how to proceed.
```

## Working with Issue Trackers

If using an issue tracker (GitHub Issues, Jira, etc.):

**Before starting:**
```bash
# Note the issue ID in commits
# Reference the plan in issue comments
```

**After completing a phase:**
```bash
# Update issue with progress
# Link commits to issue
# Add "Completed Phase N" comment
```

**After completing all phases:**
```bash
# Close or mark issue as ready for review
# Link to relevant commits/PRs
```

## Integration with Other Workflows

**After implementation:**
- Use `prompt-workflow-deliberate-commits.md` to commit changes thoughtfully
- Use `prompt-task-describe-pr.md` to create comprehensive PR descriptions
- Use `prompt-task-iterative-code-review.md` to self-review before committing

**If need to pause:**
- Use `prompt-workflow-create-handoff.md` to document progress
- Mark current phase status in todo list
- Note what's complete vs in-progress
