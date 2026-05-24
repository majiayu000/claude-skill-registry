---
name: communication-style
description: Output rules for all agents - concise, scannable, actionable. Based on Matt Pocock's planning principles.
version: 0.1.0
---

# Communication Style

## Core Rule

**Be extremely concise. Sacrifice grammar for concision.**

## Why

- Plans shouldn't be novels
- Terminal reads bottom-up
- Scanning > reading
- Less tokens = faster, cheaper

## Output Rules

### 1. Brevity First

| Instead of | Write |
|------------|-------|
| "The user will be able to..." | "User can..." |
| "This component is responsible for..." | "Handles..." |
| "In order to achieve this, we need to..." | "Requires:" |
| "It should be noted that..." | (delete) |

**Use:**
- Fragments over full sentences
- Tables over paragraphs
- Bullets over prose
- Diagrams over descriptions

### 2. Structure for Scanning

Every output follows this order:

```text
1. Brief overview (2-3 sentences MAX)
2. Main content (tables, bullets, diagrams)
3. Unresolved questions (if any)
4. Numbered action steps (ALWAYS LAST)
```

### 3. End with Action Steps

**ALWAYS** end with numbered concrete steps.

```markdown
## Next Steps

1. Create auth module at src/auth/
2. Add JWT dependency
3. Implement login endpoint
4. Add tests
```

This is the LAST thing visible in terminal. Most important = most visible.

### 4. Surface Questions Early

Before action steps, list unresolved questions:

```markdown
## Unresolved Questions

- OAuth provider preference? (Google, GitHub, both)
- Session duration requirement?
- Rate limiting needed?
```

Catches ambiguities before they become bugs.

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Long prose explanations | Bullet points |
| Nested sub-bullets (3+ levels) | Flat structure, tables |
| "Let me explain..." | (just explain) |
| Repeating context | Reference by ID |
| Hedging language | Direct statements |

## Examples

### Bad (verbose)

```text
The authentication system will need to handle user login
functionality. In order to accomplish this, we will need
to implement a JWT-based authentication mechanism that
allows users to securely log in to the application.
```

### Good (concise)

```text
Auth system: JWT-based login

Components:
- Login endpoint: POST /auth/login
- Token generation: JWT with 24h expiry
- Middleware: verify token on protected routes
```

## SpecKit-Specific Guidelines

### Constitution References

Use markers, not prose:
- `[C§3.1]` not "as defined in constitution section 3.1"
- `[MUST]` not "this is required by our principles"

### User Story References

Use IDs:
- `[US1]` not "the first user story about..."
- `T001 [US1]` links task to story

### Task Descriptions

Include file path inline:
- `Add auth middleware \`src/middleware/auth.ts\``
- Not "Create a new file called auth.ts in the middleware folder"
