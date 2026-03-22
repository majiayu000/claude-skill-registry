---
name: receiving-code-review
description: "Use when receiving code review feedback, processing reviewer comments, or responding to suggested changes from human or automated reviewers."
user-invokable: false

metadata:
  agent-affinity: [epost-implementer, epost-debugger, epost-tester]
  keywords: [feedback, review-comment, suggestion, change-request, reviewer, nit, fix-this]
  platforms: [all]
  connections:
    enhances: [code-review]
---

# Receiving Code Review

## Response Protocol

When receiving review feedback, follow this sequence exactly:

1. **READ** — Read the full feedback without responding
2. **UNDERSTAND** — Identify the reviewer's intent (what problem are they pointing at?)
3. **VERIFY** — Check if the feedback is technically correct for this codebase/stack/version
4. **EVALUATE** — Determine if the suggestion applies to this specific context
5. **RESPOND** — State factual assessment (not gratitude)
6. **IMPLEMENT** — Apply valid changes; push back on invalid ones with evidence

## Forbidden Responses

Do NOT use these phrases when receiving feedback:

- "You're absolutely right!"
- "Great point!"
- "Thanks for catching that!"
- "Good catch!"
- "That's a great suggestion!"

Replace with technical verification statements:
- "Confirmed: X causes Y. Updated to Z."
- "Verified the issue. Changed `methodA` to use `patternB` because [reason]."
- "This doesn't apply here because [technical reason]."

## Source-Specific Handling

### Human Reviewer
- Trusted context — they know the project
- Still verify technical accuracy before implementing
- If unclear, ask for clarification BEFORE implementing

### Automated Reviewer (Linter, CI, Bot)
- Check if the rule applies to this stack/version
- False positives are common — verify against actual behavior
- Do not blindly suppress warnings without understanding them

## Before Implementing Any Suggestion

Run the YAGNI check:

1. Is the code being discussed actually used in production paths?
2. Does the suggestion address a real problem or a hypothetical one?
3. Will implementing it introduce more complexity than it removes?
4. Does it conflict with existing architectural decisions?

If any answer raises doubt → push back with evidence.

## Implementation Order

When processing multiple review comments:

1. **Clarify** — Ask about unclear items FIRST (batch questions)
2. **Blocking** — Fix issues that prevent merge
3. **Simple** — Apply straightforward fixes
4. **Complex** — Address items requiring significant changes

Do NOT implement in the order comments were written. Prioritize by impact.

## When to Push Back

Push back (with evidence) when a suggestion:

- **Breaks functionality** — "This change would break X because [test/behavior]"
- **Lacks context** — "The reviewer may not have seen [related code/decision]"
- **Violates YAGNI** — "This adds complexity for a scenario that doesn't occur"
- **Is technically incorrect** — "In [framework version], this pattern is [correct/deprecated]"
- **Conflicts with architecture** — "This contradicts [ADR/decision] because [reason]"

## Acknowledgment Format

State WHAT changed, not gratitude:

- "Updated `validateInput` to check boundary conditions. Added test for empty array case."
- "Reverted to original approach. The suggested pattern doesn't support [requirement]."
- "Clarification needed: the reviewer's suggestion assumes X, but current behavior requires Y."

NOT: "Thanks for the great review! I've made all the suggested changes."

### Related Skills
- `code-review` — Giving code reviews (complementary skill)
- `verification-before-completion` — Verify fixes before claiming done
