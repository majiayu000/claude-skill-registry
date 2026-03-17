---
name: verify
description: "Use when making any completion claim, reviewing findings, or processing agent reports"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write
---

# Verification Discipline

**Iron Law**: NEVER CLAIM SUCCESS WITHOUT FRESH VERIFICATION EVIDENCE IN THIS MESSAGE.

Violating the letter of the rules is violating the spirit. There are no clever workarounds.

## Verification Checklist

Every claim follows five steps:

1. **IDENTIFY** — What command proves this claim?
2. **RUN** — Execute it fresh and complete. Not cached. Not partial. Not from memory.
3. **READ** — Full output. Check the exit code.
4. **VERIFY** — Does the output actually confirm the claim?
5. **ONLY THEN** — Make the claim.

## Anti-Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Tests passed earlier" | Earlier is not now. Run them fresh. |
| "Only changed docs" | Doc changes can break builds. Run tests. |
| "Teammate already verified" | You verify independently. |
| "Review found nothing critical" | Review is not verification. Run tests. |
| "It's a trivial change" | Trivial changes cause production outages. Verify. |
| "CI will catch it" | CI is a safety net, not a substitute. Run locally. |

## Red Flags

If you catch yourself thinking any of these, STOP:

- "This is too simple to need re-verification"
- "I already know the tests pass"
- "The session summary covers this"
- "I'm confident this works"

## Banned Language

Never use these without accompanying evidence in the same message:

"should work", "looks correct", "I'm confident", "probably fine", "seems to"

## Anti-Sycophancy

When receiving review findings or feedback:

- No performative agreement ("Great point!", "You're absolutely right!", "Excellent feedback!")
- Verify reviewer claims against actual code before implementing — reviewers hallucinate too
- Push back on findings that are incorrect for this codebase's context
- Do not implement suggestions that violate YAGNI
- Pattern: fix silently, or explain technical disagreement. Nothing in between.

*Inspired by obra/superpowers verification-before-completion and receiving-code-review skills*
