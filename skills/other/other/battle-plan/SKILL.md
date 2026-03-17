---
name: battle-plan
description: |
  Before ANY significant development task (new feature, refactor, integration,
  migration), run a complete planning ritual by orchestrating other skills in
  sequence: rubber-duck (clarify scope) -> pre-mortem (assess risks) -> eta
  (estimate time) -> final confirmation. Do not start coding until the battle
  plan is approved.
allowed-tools: |
  bash: find, grep, cat, head, ls, wc, python
  file: read
---

# Battle Plan

<purpose>
Claude Code's built-in plan mode is just "read-only mode + write a markdown file."
It doesn't assess risks, estimate time, define done, or check scope. This skill
orchestrates a complete planning ritual using composable skills before any
significant work begins.
</purpose>

## When To Activate

Trigger before:
- New feature implementation
- Refactors touching multiple files
- External service integrations
- Database migrations
- "Significant" or "important" tasks (user's words)
- Anything estimated >15 minutes

Do NOT trigger for:
- Typo fixes
- Single-line changes
- Questions/exploration
- Tasks user explicitly says are trivial

## Instructions

### Phase 1: Scope (uses [rubber-duck](../rubber-duck/SKILL.md) patterns)

Before anything, clarify what we're actually building:

```
Scope Check

What are we building?
-> [Clear description of the goal]

What's the definition of done?
-> [Specific, verifiable completion criteria]

What's explicitly OUT of scope?
-> [Things we're NOT doing, even if related]

Any ambiguity I should clarify before planning?
```

If scope is vague, ask clarifying questions. Do not proceed with vague scope.

### Phase 2: Recon

Map the terrain before planning the attack:

```
Recon

Files likely affected:
- [file1.py] - [why]
- [file2.py] - [why]

Existing patterns to follow:
- [Pattern observed in codebase]

Dependencies/callers to check:
- [What depends on code we're changing]

Tests that exist:
- [Relevant test files]
```

Use `find`, `grep`, `head` to actually explore. Don't guess.

### Phase 3: Risks (uses [pre-mortem](../pre-mortem/SKILL.md) patterns)

Imagine it's 2 weeks later and this failed. Why?

```
Pre-mortem

If this fails, it's probably because:

1. HIGH: [Specific risk]
   Mitigation: [How to prevent]

2. MED: [Specific risk]
   Mitigation: [How to prevent]

3. LOW: [Specific risk]
   Mitigation: [How to prevent]
```

Reorder plan to address HIGH risks first.

### Phase 4: Estimate (uses [eta](../eta/SKILL.md) patterns)

Provide realistic Claude-time estimate:

```
Estimate

Scope: [X files, Y estimated lines changed]
Complexity: [Simple / Medium / Complex]

Breakdown:
- Recon & setup: ~X min
- Implementation: ~Y min
- Testing: ~Z min
- Verification: ~W min

Total: ~[range] minutes

Checkpoint: [If >15 min, where's the halfway check-in?]
```

### Phase 5: The Plan

Now write the actual plan - structured, not prose:

```
Battle Plan: [Task Name]

SCOPE
  Goal: [One sentence]
  Done when: [Verifiable criteria]
  Not doing: [Explicit exclusions]

STEPS
  1. [ ] [Step] -> [Output/artifact]
       Confidence: HIGH/MED/LOW

  2. [ ] [Step] -> [Output/artifact]
       Confidence: HIGH/MED/LOW
       Depends on: Step 1

  3. [ ] [Step] -> [Output/artifact]
       Confidence: HIGH/MED/LOW

RISKS & MITIGATIONS
  [Risk 1] -> [Mitigation baked into steps]
  [Risk 2] -> [Mitigation baked into steps]

ROLLBACK
  If this goes wrong: [How to undo safely]

ESTIMATE
  ~[X-Y] minutes
  Checkpoint at: [Step N / halfway point]

Ready to execute?
```

### Phase 6: Confirmation (uses [you-sure](../you-sure/SKILL.md) patterns)

Do not proceed without explicit approval:

```
Type 'go' to execute this plan, or tell me what to adjust.
```

Accept only:
- "go" / "proceed" / "execute" -> Start work
- Feedback -> Adjust plan and re-present
- "abort" -> Cancel

## Confidence Levels

For each step, assess confidence:

**HIGH** - Done this before, clear path, low ambiguity
**MED** - Reasonable approach, some unknowns
**LOW** - Best guess, might need to pivot

If multiple steps are LOW confidence, flag it:
```
Several steps have LOW confidence. Consider spiking/prototyping first?
```

## Composability Note

This skill orchestrates patterns from:
- [rubber-duck](../rubber-duck/SKILL.md) - Scope clarification
- [pre-mortem](../pre-mortem/SKILL.md) - Risk assessment
- [eta](../eta/SKILL.md) - Time estimation
- [you-sure](../you-sure/SKILL.md) - Confirmation gate

If those skills are installed, their full capabilities enhance this ritual.
If not, this skill includes the core patterns inline.

## NEVER

- Start coding without presenting the battle plan
- Proceed without explicit confirmation
- Skip risk assessment for "simple" significant tasks
- Provide single-point estimates (always give ranges)
- Hide low confidence behind confident language

## ALWAYS

- Map actual files before planning (recon is real, not imagined)
- Include rollback strategy
- Set checkpoint for tasks >15 minutes
- Surface confidence levels honestly
- Respect scope boundaries during execution

## Example

```
User: "Add Stripe payment integration"

Scope Check

What are we building?
-> Accept one-time payments via Stripe Checkout

Definition of done:
-> User can click "Pay", complete Stripe Checkout, and see success confirmation
-> Payment recorded in our database
-> Works in test mode with test cards

Explicitly OUT of scope:
-> Subscriptions (future task)
-> Refunds (future task)
-> Multiple payment methods (just card for now)

Any ambiguity?
-> Should failed payments show inline error or redirect to error page?

[User answers: inline error]

Recon

Files likely affected:
- routes/payments.py - new endpoints
- models/order.py - add payment_status field
- templates/checkout.html - payment button
- tests/test_payments.py - new file

Existing patterns:
- Routes use Flask blueprints
- Models use SQLAlchemy with migrations
- Tests use pytest + fixtures

Dependencies:
- Order model used by 3 other routes
- Checkout template included in 2 places

Pre-mortem

If this fails in 2 weeks, it's probably because:

1. HIGH: Webhook signature validation wrong
   Mitigation: Set up Stripe CLI, test webhooks FIRST

2. HIGH: Test vs live key confusion
   Mitigation: Env validation on startup

3. MED: No idempotency on payment creation
   Mitigation: Add idempotency key from start

Estimate

Scope: 4 files, ~200 lines
Complexity: Medium

Breakdown:
- Stripe CLI + webhook setup: ~5 min
- Payment endpoints: ~10 min
- Database migration: ~5 min
- Frontend integration: ~8 min
- Testing: ~12 min

Total: ~35-45 minutes
Checkpoint: After webhook setup works (~15 min mark)

Battle Plan: Stripe Payment Integration

SCOPE
  Goal: One-time payments via Stripe Checkout
  Done when: Test payment completes end-to-end
  Not doing: Subscriptions, refunds, multi-method

STEPS
  1. [ ] Set up Stripe CLI + webhook endpoint -> Working signature validation
       Confidence: HIGH

  2. [ ] Add payment routes (create session, success, webhook) -> Endpoints responding
       Confidence: HIGH
       Depends on: Step 1

  3. [ ] Database migration for payment_status -> Migration applied
       Confidence: HIGH

  4. [ ] Frontend checkout button -> Redirects to Stripe
       Confidence: MED (need to check existing JS patterns)
       Depends on: Step 2

  5. [ ] Integration tests with Stripe test mode -> Tests passing
       Confidence: HIGH
       Depends on: Steps 1-4

RISKS & MITIGATIONS
  Webhook validation -> Addressed in Step 1 (before business logic)
  Key confusion -> Env check added in Step 2
  Idempotency -> Built into Step 2

ROLLBACK
  If broken: Revert migration, remove routes, disable checkout button
  Data safety: No production payments until explicitly switched to live keys

ESTIMATE
  ~35-45 minutes
  Checkpoint at: Step 1 complete (webhook working)

Ready to execute?
```
