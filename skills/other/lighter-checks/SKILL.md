---
name: lighter-checks
description: 'Size verification to the change so results ship. Use when checking has started to loop, when a check is about to re-run against code nothing touched, when a second tool would prove what the first already proved, or when the user says stop over-checking, just ship, or this is taking too long to verify.'
---

# Lighter Checks

Verification proves the change; it is not the deliverable. `verification-before-completion` sets the evidence bar for a claim. This skill sets its size.

## Do this

1. Pick the one action that proves this change, run it, and deliver on green.
2. Scope the run to the surface you changed. A repo-wide suite is the fallback when nothing narrower covers the change, not the opening move.
3. Run a second tool only when it covers a different failure class. Three tools agreeing on one fact is still one fact.
4. Treat tool output as the verification. An applied edit is proven by what the run says, not by reading the diff again.
5. On red, fix and re-run that same check. On green, ship. Green is the stop condition, not a prompt to go looking for a stricter check.
6. Keep the repo gate whole: the project's own typecheck, lint, and test commands still run once for every language you touched. Cut the repetition, never the gate.

## Verify

- [ ] One proving action per claim, scoped to the changed surface.
- [ ] Nothing was re-run purely for reassurance.
- [ ] No second tool ran to confirm a fact the first already established.
- [ ] The repo's own typecheck, lint, and test gate ran once per touched language.
- [ ] Delivery happened on the first green.
