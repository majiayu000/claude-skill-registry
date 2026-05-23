---
name: comment-guidelines
description: "Code comment guidelines. Remove redundant comments, add strategic ones explaining WHY not WHAT. Applied automatically when modifying code."
user-invocable: false
---

# Comment Guidelines

These guidelines should be automatically applied whenever writing or modifying code.

## Core Principles

1. **Self-documenting code first** - Use clear naming and structure; comments are last resort
2. **WHY over WHAT** - Comments explain intent and reasoning, not mechanics
3. **Reduce cognitive load** - Make non-obvious knowledge explicit
4. **Zero redundancy** - Never duplicate what code already expresses

## When to Add Comments

**DO comment:**
- Design decisions and trade-offs
- Non-obvious behavior or edge cases
- Interface contracts (public APIs, function signatures)
- Important context that isn't evident from code
- Gotchas and subtle behaviors
- Cross-module dependencies

**DON'T comment:**
- What the code literally does (self-evident)
- Well-named variables/functions
- Standard patterns and idioms
- Implementation details visible in code

## Application Rules

When modifying code:

1. **Remove** any comments that restate what code does
2. **Keep** comments that explain WHY something is done
3. **Add** comments only for non-obvious behavior or design decisions
4. **Update** existing comments if code changes make them stale
5. **Never** add comments just to fill space or appear thorough

## Examples

```typescript
// BAD: Restates the obvious
// Set user name to the input value
user.name = input.value;

// GOOD: Explains non-obvious behavior
// Normalize to lowercase for case-insensitive matching in search
user.searchKey = user.name.toLowerCase();

// BAD: Documents what is self-evident
// Loop through all items
for (const item of items) { ... }

// GOOD: Explains WHY this approach
// Process in reverse to allow safe removal during iteration
for (let i = items.length - 1; i >= 0; i--) { ... }
```

## Automatic Application

This skill does NOT need to be explicitly invoked. Claude should:
- Apply these principles whenever editing code
- Proactively clean up redundant comments encountered
- Add strategic comments only where they reduce cognitive load
