---
name: effective-tasks
description: Best practices for writing SIMBL tasks that Claude can execute with zero context. Use when creating or refining tasks for maximum clarity.
allowed-tools: Read, Bash, Grep, Glob
---

# Writing Effective SIMBL Tasks

Write tasks that Claude Code can execute with ZERO context - even in a fresh session.

## Goal

A well-written task contains everything needed to complete it without searching the codebase for context. Future sessions shouldn't need to ask "what did we mean by this?"

## Title Formula

**Action verb + specific noun + context**

### Good Titles
- "Add email validation to signup form"
- "Fix null pointer in UserService.getProfile()"
- "Refactor auth middleware to use JWT"
- "Update error messages in checkout flow"
- "Remove deprecated analytics calls"

### Bad Titles
- "Fix the bug" (what bug?)
- "Update user stuff" (too vague)
- "Auth" (not actionable)
- "Investigate issue" (no clear outcome)
- "Improvements" (not specific)

## Description Structure

### 1. Context (What Exists Now)

Provide concrete references:
- File paths: `src/services/auth.ts`
- Function names: `validateToken()`
- Current behavior: "Returns 500 when token expired"
- Error messages: "TypeError: Cannot read property 'id' of null"

```markdown
### Context
- File: `src/services/UserService.ts:45`
- Function: `getProfile(userId)`
- Current: Returns 500 on missing user
- Stack trace shows null dereference at line 52
```

### 2. Requirement (What Should Change)

Be explicit about:
- Expected behavior: "Return 401 with error message"
- Constraints: "Must be backwards compatible"
- Edge cases to handle: "Null user, expired token, missing permissions"

```markdown
### Requirement
- Return 404 with `{ error: "user_not_found" }` for missing users
- Keep existing behavior for valid users
- Add null check before accessing user.id
```

### 3. Relevant Code Snippets

Paste the specific code that needs changing - don't make Claude search for it:

```markdown
### Current Code
\`\`\`typescript
// src/services/UserService.ts:45-55
async getProfile(userId: string) {
  const user = await this.repo.findById(userId);
  return {
    id: user.id,  // <-- crashes here when user is null
    name: user.name
  };
}
\`\`\`
```

## Acceptance Criteria

Concrete, testable conditions with checkboxes:

```markdown
### Acceptance Criteria
- [ ] `getProfile()` returns 404 for non-existent users
- [ ] Response includes `{ error: "user_not_found" }`
- [ ] Existing tests pass
- [ ] New test covers null user case
- [ ] No console errors in browser
```

### Good Criteria
- Specific and verifiable
- Binary (done or not done)
- Testable by running code

### Bad Criteria
- "Works correctly" (vague)
- "Handles errors well" (subjective)
- "Is performant" (no metric)

## Context Embedding Tips

### Paste Error Messages Directly
```markdown
Error: TypeError: Cannot read property 'id' of null
    at UserService.getProfile (src/services/UserService.ts:52:15)
    at async ProfileController.show (src/controllers/profile.ts:18:22)
```

### Reference Related Work
```markdown
Related: task-12 (same service), task-8 (similar null handling)
See also: PR #234 where we fixed the same pattern in OrderService
```

### Include External References
```markdown
Per RFC 7519 section 4.1 - JWT claims must include 'exp'
Following pattern from: https://docs.example.com/auth#tokens
```

### Add File Paths Even If Obvious
```markdown
Files to modify:
- src/services/UserService.ts (main fix)
- src/services/__tests__/UserService.test.ts (add test)
- src/types/errors.ts (add UserNotFoundError if needed)
```

## Priority Guidelines

Match priority to actual urgency:

| Priority | Use For |
|----------|---------|
| p1 | Production broken, data loss, security issue |
| p2 | Important feature, significant bug |
| p3 | Normal development work |
| p4 | Nice to have, polish |
| p5-p9 | Backlog items, someday/maybe |

## Complete Task Example

```markdown
## task-42 Fix null user crash in getProfile

[p2] [backend] [bug]

### Context
- File: `src/services/UserService.ts:45-55`
- Current: `getProfile()` crashes when user not found
- Error: `TypeError: Cannot read property 'id' of null`
- Reproduces: Call `/api/users/nonexistent-id`

### Current Code
\`\`\`typescript
async getProfile(userId: string) {
  const user = await this.repo.findById(userId);
  return {
    id: user.id,  // crashes when user is null
    name: user.name
  };
}
\`\`\`

### Requirement
Return 404 response instead of crashing. Use existing NotFoundError pattern from OrderService.

### Acceptance Criteria
- [ ] GET /api/users/:id returns 404 for non-existent user
- [ ] Response body: `{ error: "user_not_found", userId: "<id>" }`
- [ ] Existing user tests still pass
- [ ] New test: "returns 404 for missing user"

### Notes
See OrderService.getOrder() for similar pattern.
Related: task-38 (added NotFoundError class)
```
