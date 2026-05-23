---
name: meta-methodology-anti-over-engineering
description: Anti-over-engineering principles - surgical implementation, not architectural innovation. Use existing utilities, minimal changes, follow established conventions. No new abstractions.
---

# Anti-Over-Engineering Principles

> **Quick Guide:** Your job is surgical implementation, not architectural innovation. Use existing utilities, make minimal changes, follow established conventions.

---

<critical_requirements>

## CRITICAL: Your Job is Surgical Implementation

**(Use existing utilities - search the codebase before creating anything new)**

**(Make minimal changes - only what the spec explicitly requires)**

**(Follow established conventions - match naming, formatting, organization)**

**(Never create new abstractions, helpers, or "for future flexibility" code)**

</critical_requirements>

---

<anti_over_engineering>

**Your job is surgical implementation, not architectural innovation.**

Analyze thoroughly and examine similar areas of the codebase to ensure your proposed approach fits seamlessly with the established patterns and architecture. Aim to make only minimal and necessary changes, avoiding any disruption to the existing design.

### What to NEVER Do (Unless Explicitly Requested)

**Don't create new abstractions:**

- No new base classes, factories, or helper utilities
- No "for future flexibility" code
- Use what exists - don't build new infrastructure
- Never create new utility functions when existing ones work

**Don't add unrequested features:**

- Stick to the exact requirements
- "While I'm here" syndrome is forbidden
- Every line must be justified by the spec

**Don't refactor existing code:**

- Leave working code alone
- Only touch what the spec says to change
- Refactoring is a separate task, not your job

**Don't optimize prematurely:**

- Don't add caching unless asked
- Don't rewrite algorithms unless broken
- Existing performance is acceptable

**Don't introduce new patterns:**

- Follow what's already there
- Consistency > "better" ways
- If the codebase uses pattern X, use pattern X

**Don't create complex state management:**

- For simple features, use simple solutions
- Match the complexity level of similar features

### What TO Do

**Use existing utilities:**

- Search the codebase for existing solutions
- Check utility functions in `/lib` or `/utils`
- Check helper functions in similar components
- Check shared services and modules
- Reuse components, functions, types
- Ask before creating anything new

**Make minimal changes:**

- Change only what's broken or missing
- Ask yourself: What's the smallest change that solves this?
- Am I modifying more files than necessary?
- Could I use an existing pattern instead?
- Preserve existing structure and style
- Leave the rest untouched

**Use as few lines of code as possible:**

- While maintaining clarity and following existing patterns

**Follow established conventions:**

- Match naming, formatting, organization
- Use the same libraries and approaches
- When in doubt, copy nearby code

**Follow patterns in referenced example files exactly:**

- When spec says "follow auth.py", match its structure precisely

**Question complexity:**

- If your solution feels complex, it probably is
- Simpler is almost always better
- Ask for clarification if unclear

**Focus on solving the stated problem only:**

- **(Do not change anything not explicitly mentioned in the specification)**
- This prevents 70%+ of unwanted refactoring

</anti_over_engineering>

---

<decision_framework>

## Decision Framework

Before writing code, ask yourself:

```xml
<complexity_check>
1. Does an existing utility do this? -> Use it
2. Is this explicitly in the spec? -> If no, don't add it
3. Does this change existing working code? -> Minimize it
4. Am I introducing a new pattern? -> Stop, use existing patterns
5. Could this be simpler? -> Make it simpler
</complexity_check>
```

### When in Doubt

**Ask yourself:** "Am I solving the problem or improving the codebase?"

- Solving the problem = good
- Improving the codebase = only if explicitly asked

**Remember: Every line of code is a liability.** Less code = less to maintain = better.

**Remember: Code that doesn't exist can't break.**

</decision_framework>

---

<proven_phrases>

## Proven Effective Phrases

Include these in your responses when applicable:

- "I found an existing utility in [file] that handles this"
- "The simplest solution matching our patterns is..."
- "To make minimal changes, I'll modify only [specific files]"
- "This matches the approach used in [existing feature]"

</proven_phrases>

---

<critical_reminders>

## CRITICAL REMINDERS

**(Your job is surgical implementation, not architectural innovation)**

**(Use existing utilities - search before creating)**

**(Make minimal changes - only what the spec requires)**

**(Follow established conventions - match existing code)**

**(Never create new abstractions unless explicitly requested)**

**(Every line must be justified by the spec)**

</critical_reminders>
