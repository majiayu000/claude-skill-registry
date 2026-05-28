---
name: communication-style
description: This skill should be used when generating spec artifacts (research.md, requirements.md, design.md, tasks.md), formatting agent output, structuring phase results, or when any Ralph agent needs guidance on concise, scannable output formatting. Applies to all Ralph spec phase agents.
version: 0.2.0
user-invocable: false
---

# Communication Style

Be extremely concise. Sacrifice grammar for concision.

## Rationale

- Plans should not be novels
- Terminal reads bottom-up
- Scanning beats reading
- Fewer tokens = faster, cheaper

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

```
1. Brief overview (2-3 sentences MAX)
2. Main content (tables, bullets, diagrams)
3. Unresolved questions (if any)
4. Numbered action steps (ALWAYS LAST)
```

### 3. End with Action Steps

Action steps appear last because terminal output is read bottom-up -- the most important content occupies the most visible position.

```markdown
## Next Steps

1. Create auth module at src/auth/
2. Add JWT dependency
3. Implement login endpoint
4. Add tests
```

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

## References

- **`references/examples.md`** -- Bad vs good output examples for each spec phase (research, requirements, design, tasks)
