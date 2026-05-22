---
name: effective-prompting
description: Master effective prompting techniques for Claude Code. Use when learning prompt patterns, improving task descriptions, optimizing Claude interactions, or troubleshooting why Claude misunderstood a request. Covers @ mentions, thinking keywords, task framing, and iterative refinement.
allowed-tools: ["Read"]
---

# Effective Prompting for Claude Code

Write prompts that Claude Code understands and executes correctly the first time.

## Quick Reference

| Technique | When to Use | Example |
|-----------|-------------|---------|
| @ mentions | Include specific context | `@src/api/users.ts` |
| ultrathink | Complex reasoning tasks | "ultrathink about the architecture" |
| Success criteria | Clear deliverables | "Done when tests pass" |
| Task decomposition | Multi-step work | "First X, then Y, finally Z" |
| /compact | Long sessions | Summarize and continue |

## @ Mentions (Context Injection)

@ mentions pull specific context into your prompt. Use them liberally.

### Types

| Mention | Purpose | Example |
|---------|---------|---------|
| `@file` | Single file | `@src/utils/auth.ts` |
| `@folder` | Directory contents | `@src/api/` |
| `@url` | Web content | `@https://docs.example.com/api` |
| `@git` | Git context | `@git:diff`, `@git:log` |

### File Patterns

```
@src/api/*.ts           # All TS files in api folder
@src/**/*.test.ts       # All test files recursively
@package.json           # Specific file
@src/components/        # Entire folder
```

### Best Practices

- **Be specific**: `@src/api/users.ts` > `@src/`
- **Include tests**: `@src/auth.ts @src/auth.test.ts`
- **Add related files**: `@types/user.ts @src/api/users.ts`
- **Limit scope**: 3-5 relevant files > entire codebase

## Thinking Keywords

Trigger deeper reasoning with specific keywords.

| Keyword | Depth | Use Case |
|---------|-------|----------|
| `think` | Standard | General problem-solving |
| `think harder` | Extended | Complex bugs, edge cases |
| `ultrathink` | Deep | Architecture, security, optimization |
| `megathink` | Maximum | Critical decisions, complex refactors |

### When to Use Extended Thinking

- Architecture decisions
- Security-sensitive code
- Performance optimization
- Complex debugging
- Multi-system integration
- Breaking changes analysis

### Example

```
ultrathink about how to refactor the authentication system
to support OAuth2 while maintaining backward compatibility
with our existing session-based auth @src/auth/
```

## Task Framing

Structure prompts for clarity and precision.

### The WHAT-WHY-HOW Pattern

```
WHAT: [Specific task]
WHY: [Context/motivation]
HOW: [Constraints/approach]
```

**Example:**
```
WHAT: Add rate limiting to the /api/upload endpoint
WHY: Users are uploading large files too frequently, causing server strain
HOW: Use a sliding window approach, 10 requests per minute per user
```

### Success Criteria

Always define "done":

```
Add user search to the dashboard.

Done when:
- Search input filters users in real-time
- Debounced to 300ms
- Shows "No results" for empty matches
- Tests cover happy path and edge cases
```

### Constraints Pattern

Specify boundaries:

```
Implement caching for API responses.

Constraints:
- Use Redis (already configured in docker-compose)
- TTL of 5 minutes for user data
- No caching for POST/PUT/DELETE
- Must work with existing middleware
```

## Multi-Step Tasks

For complex work, structure as steps.

### Sequential Steps

```
Implement user authentication:

1. First, add the User model with email/password fields
2. Then, create login/register API endpoints
3. Next, add JWT token generation and validation
4. Finally, protect routes with auth middleware

Run tests after each step.
```

### Parallel Work Indicators

```
These can be done in parallel:
- Add UserCard component
- Add UserList component
- Add UserSearch component

Then combine them in the UserDashboard page.
```

### Checkpoints

```
Refactor the payment module.

Checkpoint 1: Extract PaymentService class
- Run tests, commit if green

Checkpoint 2: Add Stripe integration
- Run tests, commit if green

Checkpoint 3: Add webhook handling
- Run tests, commit if green
```

## Iterative Refinement

Build complex features incrementally.

### Start Simple

```
# Round 1
Add a basic todo list component with hardcoded items.

# Round 2
Now add the ability to add new todos.

# Round 3
Add delete functionality and persist to localStorage.
```

### Feedback Loop

```
# Initial
Add pagination to the user list.

# After seeing result
Good, but the page buttons are too small on mobile.
Make them at least 44px tap targets.

# After fix
Perfect. Now add keyboard navigation (arrow keys).
```

## Session Management

### Using /compact

When context grows large:

```
/compact

Continue with: We're implementing user auth.
Done: User model, login endpoint.
Next: JWT middleware.
```

### Context Reset

```
Let's start fresh on the auth system.
Ignore previous attempts.
Here's the new approach: [approach]
```

## Common Prompt Patterns

| Pattern | Template |
|---------|----------|
| Bug fix | "Fix [bug]. Reproduce: [steps]. Expected: [X]. Actual: [Y]." |
| Feature | "Add [feature]. Requirements: [list]. Done when: [criteria]." |
| Refactor | "Refactor [code] to [goal]. Keep: [constraints]. Test: [how]." |
| Review | "Review @file for [concerns]. Focus on: [areas]." |
| Debug | "Debug why [symptom]. Context: @logs @code. Checked: [attempts]." |

## Reference Files

| File | Contents |
|------|----------|
| [PATTERNS.md](./PATTERNS.md) | Detailed prompt patterns for specific tasks |
| [EXAMPLES.md](./EXAMPLES.md) | Real-world prompt examples |
| [ANTI-PATTERNS.md](./ANTI-PATTERNS.md) | Common mistakes and how to avoid them |

## Validation Checklist

Before sending a complex prompt:

- [ ] Included relevant context with @ mentions
- [ ] Stated the goal clearly
- [ ] Defined success criteria
- [ ] Specified constraints
- [ ] Used thinking keywords if needed
- [ ] Broke down multi-step tasks
- [ ] Provided examples if pattern is unclear
