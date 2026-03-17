---
name: no-deferred-work
description: Use during all development - no TODOs, no FIXMEs, no "we'll add this later"; do it now or get explicit deferral permission
---

# No Deferred Work

## Overview

No TODOs. No "later". Do it now or don't commit.

**Core principle:** Deferred work is forgotten work. Technical debt accumulates.

**The rule:** If work is needed, do it now. If it's out of scope, get explicit permission to defer.

## Forbidden Patterns

### TODO Comments

```typescript
// NEVER COMMIT THESE

// TODO: Add error handling
// TODO: Implement validation
// TODO: Write tests
// FIXME: This is a workaround
// HACK: Temporary solution
// XXX: Need to revisit
```

### Placeholder Implementations

```typescript
// NEVER COMMIT THESE

function validateEmail(email: string): boolean {
  // TODO: Implement proper validation
  return true;
}

async function fetchUserData(id: string): Promise<User> {
  // Placeholder - implement later
  return {} as User;
}

try {
  await riskyOperation();
} catch (error) {
  // TODO: Handle error properly
  console.log(error);
}
```

### Incomplete Features

```typescript
// NEVER COMMIT THESE

class UserService {
  async createUser(data: UserData): Promise<User> {
    // Basic implementation - need to add:
    // - Email verification
    // - Password hashing
    // - Notification
    return this.db.create(data);
  }
}
```

## The Decision Flow

```
Work needed during implementation
            │
            ▼
┌─────────────────────────────┐
│ Is this work in scope of   │
│ current issue?              │
└─────────────┬───────────────┘
              │
     ┌────────┴────────┐
     │                 │
    Yes                No
     │                 │
     ▼                 ▼
  DO IT NOW      ┌────────────────┐
     │           │ Can I complete │
     │           │ current work   │
     │           │ without it?    │
     │           └───────┬────────┘
     │                   │
     │          ┌────────┴────────┐
     │          │                 │
     │         Yes                No
     │          │                 │
     │          ▼                 ▼
     │    Create separate    DO IT NOW
     │    issue for it       (expand scope)
     │          │                 │
     └──────────┴─────────────────┘
                │
                ▼
           COMMIT
```

## What To Do Instead

### In-Scope Work: Do It

If the work is needed for the current feature:

```typescript
// Don't do this
function validateEmail(email: string): boolean {
  // TODO: Add format validation
  return email.length > 0;
}

// Do this
function validateEmail(email: string): boolean {
  if (!email || email.trim().length === 0) {
    return false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

### Out-of-Scope Work: Create Issue

If the work is genuinely separate:

```bash
# Create a new issue for the deferred work
gh issue create \
  --title "Add email verification flow" \
  --body "## Description
Discovered while implementing #123 (user registration).

Email verification is a separate feature that should:
- Send verification email on registration
- Handle verification link clicks
- Update user status on verification

## Acceptance Criteria
- [ ] Verification email sent on registration
- [ ] Verification link validates correctly
- [ ] User status updated after verification

## Related
Discovered during: #123"
```

Then continue with current work without the deferred piece.

### Error Handling: Complete It

```typescript
// Don't do this
try {
  await saveData(data);
} catch (error) {
  // TODO: Handle properly
  throw error;
}

// Do this
try {
  await saveData(data);
} catch (error) {
  if (error instanceof ValidationError) {
    throw new UserFacingError('Invalid data provided', { cause: error });
  }
  if (error instanceof DatabaseError) {
    logger.error('Database save failed', { error, data });
    throw new UserFacingError('Unable to save. Please try again.', { cause: error });
  }
  throw error; // Unknown error, rethrow
}
```

### Tests: Write Them

```typescript
// Don't do this
// TODO: Add tests for edge cases

// Do this - write the tests
test('handles empty input', () => {
  expect(validate('')).toBe(false);
});

test('handles whitespace-only input', () => {
  expect(validate('   ')).toBe(false);
});

test('handles maximum length input', () => {
  expect(validate('a'.repeat(MAX_LENGTH))).toBe(true);
});

test('rejects over-length input', () => {
  expect(validate('a'.repeat(MAX_LENGTH + 1))).toBe(false);
});
```

## Exception Process

If deferral is truly necessary (very rare):

### 1. Get Explicit Permission

Ask your human partner:

```markdown
I've identified work that seems out of scope:

**Current issue:** #123 - User Registration
**Discovered work:** Email verification flow

This is genuinely a separate feature. Can I:
1. Create a separate issue for it
2. Complete current work without it
3. Reference the new issue in the code

Or should I implement it now as part of #123?
```

### 2. If Approved, Create Proper Issue

Not a TODO comment. A real, tracked issue with:
- Full description
- Acceptance criteria
- Link to where it was discovered

### 3. Reference Issue in Code

```typescript
// Only if explicitly approved as out of scope
// See issue #456 for email verification implementation
const user = await createBasicUser(data);
// Note: Email verification handled separately per #456
```

This is NOT a TODO. It's a reference to tracked work.

## Detecting Violations

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for TODO comments
if git diff --cached | grep -iE '^\+.*\b(TODO|FIXME|HACK|XXX)\b'; then
  echo "ERROR: TODO/FIXME comments detected. Do the work or create an issue."
  exit 1
fi
```

### Code Review Check

Reviewers should reject PRs containing:
- TODO comments
- FIXME comments
- Placeholder implementations
- Incomplete error handling
- Missing tests for new code

## Common Excuses Rejected

| Excuse | Response |
|--------|----------|
| "It's just a small thing" | Small things accumulate. Do it now. |
| "I'll fix it in the next PR" | Create an issue if it's separate work. |
| "The feature works without it" | If it's needed, it's part of the feature. |
| "I'm running out of time" | Time pressure isn't a reason for debt. |
| "It's not critical" | If you're writing a TODO, it's needed. |

## Checklist

Before committing:

- [ ] No TODO comments
- [ ] No FIXME comments
- [ ] No HACK comments
- [ ] No placeholder implementations
- [ ] Error handling is complete
- [ ] Tests are complete
- [ ] Any out-of-scope work has an issue created

## Integration

This skill is applied by:
- `issue-driven-development` - Step 7
- `comprehensive-review` - Checks for deferred work

This skill prevents:
- Technical debt accumulation
- Forgotten work
- Incomplete features
- Production issues from deferred error handling
