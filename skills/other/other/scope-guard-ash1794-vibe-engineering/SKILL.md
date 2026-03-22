---
name: vibe-scope-guard
description: Detects and redirects scope creep during implementation. Catches unrequested features, unnecessary refactoring, and over-engineering.
user-invocable: true
---

# vibe-scope-guard

The best code is the code you don't write. Stay focused on what was asked.

## When to Use This Skill

- During any implementation task
- When you notice you're "improving" code that wasn't in the request
- When implementation is taking longer than expected
- When you're about to create an abstraction "for later"

## When NOT to Use This Skill

- During brainstorming (ideas should be unconstrained)
- When the user explicitly asks for broad improvements
- When scope expansion is necessary for correctness

## Scope Creep Signals

Watch for these patterns:

| Signal | Example | Response |
|--------|---------|----------|
| Unrequested features | "While I'm here, let me add caching" | Stop. Was caching requested? |
| Premature abstraction | "Let me create a generic helper for this" | Is it used more than once? |
| Gold plating | "Let me add comprehensive error messages for every case" | Only at system boundaries |
| Refactoring drive-by | "This function could be cleaner" | Was refactoring requested? |
| Over-engineering | "Let me make this configurable" | Does anyone need configuration? |
| Documentation creep | "Let me add docstrings to all these functions" | Only to functions you changed |
| Test over-expansion | "Let me test every possible input" | Test the boundaries, not every input |

## The Rule

**Three similar lines of code is better than a premature abstraction.**

Before adding anything not explicitly requested, ask:
1. Was this requested? → No → Don't do it
2. Is it necessary for correctness? → No → Don't do it
3. Will it break without this? → No → Don't do it
4. Is the user watching time/cost? → Yes → Definitely don't do it

## Steps

When you detect scope creep:
1. **Stop** — Don't commit the extra work
2. **Acknowledge** — "I notice I'm adding [X] which wasn't requested"
3. **Offer** — "Would you like me to also [X], or should I stay focused on [original task]?"
4. **If declined** — Revert the extra work, continue with original scope
5. **If accepted** — Proceed, but track it separately

## Output

This skill doesn't produce formal output. It modifies behavior. When triggered explicitly:

### Scope Audit
**Original request**: [what was asked]
**Current work**: [what's being done]
**Scope additions detected**: X

| Addition | Requested? | Necessary? | Recommendation |
|----------|-----------|------------|----------------|
| [extra work] | No | No | Remove |
