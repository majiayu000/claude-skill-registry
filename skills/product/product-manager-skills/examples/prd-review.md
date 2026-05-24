# Example: PRD Review And Pushback

## Scenario

You already have a PRD draft, but you want a strong PM peer review instead of grammar cleanup.

## Prompt

```text
Review this PRD for a notification preferences center. Flag solution smuggling, weak metrics, overscoping, and delivery risk. Be opinionated.
```

## Example Output Excerpt

```text
Findings
- The problem statement is solution-smuggled. "Users need a preferences dashboard" starts from UI, not from the user problem.
- Success metrics are incomplete. There is no baseline, no target, and no guardrail metric.
- Scope is too broad for one release: channel controls, digest preferences, quiet hours, admin policy, and migration are multiple slices.
- User stories are horizontal. API work, UI work, and notification service updates are separated instead of being cut by user value.

Suggested reframing
- Problem: users receive too many irrelevant notifications and lack confidence they can control frequency without missing critical updates.
- First release: account-level email preferences + unsubscribe rescue flow + instrumentation for preference changes and unsubscribe reduction.

Recommended next step
- Rewrite the problem statement and success metrics first. Do not expand solution detail until scope is sliced vertically.
```

## What Good Looks Like

The review should not stop at criticism. It should:

- name the anti-pattern directly
- explain the consequence
- propose a thinner, more testable slice
