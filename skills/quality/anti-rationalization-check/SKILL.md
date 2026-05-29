---
name: vibe-anti-rationalization-check
description: Detects and prevents shortcut rationalization — when the agent is about to skip a step, simplify a requirement, or optimize away a constraint. Triggers proactively when rationalization patterns are noticed.
user-invocable: true
---

# vibe-anti-rationalization-check

LLMs systematically rationalize shortcuts. This skill catches it happening.

## When to Use This Skill

- You catch yourself thinking "this is simple enough to skip testing"
- You're about to reduce scope without the user asking
- You notice you're explaining why something "doesn't really need" to be done
- A constraint feels "too strict" and you want to relax it
- You're about to say "in the interest of time..."

## When NOT to Use This Skill

- The user explicitly asked to skip something
- You're genuinely unsure if something is needed (ask the user instead)
- The simplification is the user's explicit request

## Known Rationalization Patterns

Watch for these thoughts — they're red flags:

| Rationalization | Reality |
|----------------|---------|
| "This is too simple to need tests" | Simple code in complex systems causes the hardest bugs |
| "The user probably doesn't care about this edge case" | Production users will find every edge case |
| "We don't need error handling here" | Internal code fails too, especially during refactors |
| "I'll add that later" | "Later" never comes. Do it now or create a tracked task |
| "This is just boilerplate" | Boilerplate often contains critical correctness constraints |
| "The happy path is enough for now" | The sad path is where real users spend most of their time |
| "It works, so it must be correct" | "Works" and "correct" are different things |
| "This test is redundant" | Redundant tests catch redundant bugs |
| "Let me simplify this requirement" | Simplifying without asking = silently dropping scope |
| "This doesn't need documentation" | If you thought about it for >2 minutes, document why |

## Steps

When you detect a rationalization:

1. **Name it** — "I notice I'm rationalizing skipping [X]"
2. **State the constraint** — "The requirement says [specific requirement]"
3. **Evaluate honestly** — Is there a legitimate reason to skip this, or is it laziness?
4. **Choose**:
   - If legitimate: Ask the user "Should we skip X because Y?"
   - If rationalization: Do the work. Don't mention the temptation.
5. **If you skipped something without asking**: Go back and do it

## Output

This skill doesn't produce output — it's a mental discipline check. When triggered, it modifies behavior, not output.

If invoked explicitly by the user, report:
- What rationalizations were detected in recent work
- What was skipped and why
- What should be revisited
