---
name: self-review
description: Scale review effort to task complexity
user-invocable: false
model: sonnet
---

# Adaptive Review

Scale your effort to the task. Don't over-review trivial changes, don't under-review critical ones.

## Effort Levels

| Task Type | Review Depth |
|-----------|--------------|
| Typo, one-liner | Does it work? Ship it. |
| Feature, component | Build + types + looks right |
| Architecture, refactor | All above + system impact + docs |

## Quick Check

After any change:
1. `npm run typecheck && npm run build` - must pass
2. Does it solve the problem? (not just technically correct)
3. Would I approve this PR?

If yes to all, move on.

## When to Dig Deeper

**More review:** Money, security, user data, unfamiliar code
**Less review:** Isolated changes, low risk, well-understood code

→ For detailed verification workflow, use `verify` command.
