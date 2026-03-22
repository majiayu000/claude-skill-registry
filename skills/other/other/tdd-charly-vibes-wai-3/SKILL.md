---
name: tdd
description: Implement features following Test-Driven Development methodology. Red-Green-Refactor cycle with phased approach and verification at each step.
---

# Implement with TDD Workflow

Implement the requested feature following Test-Driven Development and a phased approach.

## Core Principle: Red, Green, Refactor

**Red:** Write a failing test that describes desired behavior
**Green:** Write minimal code to make the test pass
**Refactor:** Clean up code while keeping tests green

## Process

### Phase 0: Plan (If needed)

**For complex features, create a plan first:**

1. Read relevant code to understand current state
2. Identify what needs to change
3. Break work into logical phases
4. Define success criteria (automated and manual)
5. Get user approval of plan before implementing

**Plan structure:**
```markdown
# [Feature Name] Implementation Plan

## Current State
[What exists now]

## Desired End State
[What will exist, how to verify]

## Out of Scope
[What we're NOT doing]

## Phase 1: [Name]

### Changes Required
- File: `path/to/file.ext`
- Changes: [Description]
- Tests: [What tests to write]

### Success Criteria

#### Automated:
- [ ] New tests pass
- [ ] Existing tests still pass
- [ ] Type checking passes (if applicable)

#### Manual:
- [ ] [Specific manual verification]

## Phase 2: [Name]
[Continue...]
```

**Get plan approved before proceeding.**

### Phase 1: Implement First Component

**For each phase:**

#### Step 1: Write Failing Test

```typescript
// RED: Test describes what should happen
describe('UserAuthentication', () => {
  it('should validate JWT tokens', async () => {
    const token = 'valid.jwt.token'
    const result = await validateToken(token)
    expect(result).toEqual({ userId: '123', valid: true })
  })
})
```

Run test: **Confirm it fails** (and fails for the right reason)

#### Step 2: Implement Minimal Code

```typescript
// GREEN: Minimal implementation to pass test
async function validateToken(token: string) {
  // Simplest thing that could work
  const decoded = jwt.verify(token, SECRET)
  return {
    userId: decoded.sub,
    valid: true
  }
}
```

Run test: **Confirm it passes**

#### Step 3: Refactor If Needed

```typescript
// REFACTOR: Clean up while keeping tests green
async function validateToken(token: string): Promise<TokenResult> {
  try {
    const decoded = jwt.verify(token, getSecret()) as JWTPayload
    return {
      userId: decoded.sub,
      valid: true
    }
  } catch (error) {
    return { userId: null, valid: false, error: error.message }
  }
}
```

Run tests: **Confirm they still pass**

#### Step 4: Verify Phase Completion

**Automated verification:**
```bash
# Run all tests
npm test

# Run type checking (if applicable)
npm run type-check

# Run linting (if applicable)
npm run lint
```

**Manual verification:**
- [ ] [Specific manual tests from plan]

#### Step 5: Inform User

```
Phase 1 Complete - Ready for Verification

Automated verification:
- [x] Tests pass (12 new tests, all existing tests still passing)
- [x] Type checking passes
- [x] Linting passes

Manual verification needed:
- [ ] [Manual verification step 1]
- [ ] [Manual verification step 2]

Changes made:
- src/auth/validate.ts: Added validateToken function
- tests/auth/validate.test.ts: Added 12 tests covering valid/invalid tokens

Let me know when verified so I can proceed to Phase 2.
```

**Wait for user confirmation before proceeding.**

### Phase 2, 3, etc.: Repeat

Continue with each phase following the same Red-Green-Refactor cycle.

## Key Guidelines

1. **Tests first, always** - Write the test before the implementation
2. **Minimal implementation** - Write just enough code to pass the test
3. **One phase at a time** - Complete and verify before moving on
4. **Keep tests green** - Never commit with failing tests
5. **Refactor with green tests** - Only clean up when tests pass
6. **Verify at each phase** - Automated and manual checks
7. **Update plan** - Check off completed items as you go

## When Things Don't Match

If reality doesn't match the plan:

```
Issue in Phase [N]:

Expected: [What the plan says]
Found: [Actual situation]
Why this matters: [Explanation]

Options:
1. Adapt implementation to reality
2. Update plan to reflect new understanding
3. Discuss with user

How should I proceed?
```

**Don't blindly follow an outdated plan.**

## Resuming Work

If resuming from an existing plan:

1. Read the plan completely
2. Check for items already checked off
3. Start from first unchecked item
4. Verify previous work if something seems off
5. Continue with Red-Green-Refactor cycle
