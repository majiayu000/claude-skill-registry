# Example: PM Sprint From Idea To PRD

## Scenario

You have a raw feature idea and want the skill to run the full 6-phase sprint, then hand back a PRD-ready output instead of jumping straight to solution details.

## Prompt

```text
Take this from idea to PRD: users keep missing important billing alerts because our notification system is too blunt. Run the full 6-phase PM sprint and keep the output decision-oriented.
```

## Example Output Excerpt

```text
Sprint Summary

1. Discover
- Problem confirmed: users are using unsubscribe as a blunt escape hatch because they cannot tune notification frequency by type.
- Evidence needed next: unsubscribe rate by cohort, billing alert miss rate, and 3 user calls with recent unsubscribers.

2. Position
- Primary user: small team leads who own billing and receive both critical alerts and marketing mail.
- Product value: reduce notification fatigue without losing trust in critical billing messages.

3. Prioritize
- Best first slice: account-level email preferences plus critical-alert protection.
- Rejected for v1: quiet hours, digest builder, admin policy matrix, and multi-channel controls.

4. Specify
- PRD scope: account settings page, notification categories, billing-alert override, and analytics instrumentation.
- Out of scope: SMS, Slack, and organization-wide admin policy.

5. Validate
- Hypothesis: giving users fine-grained email control will reduce unsubscribes without increasing missed billing alerts.
- Probe: prototype test plus cohort tracking for unsubscribe reduction and billing-alert engagement.

6. Measure
- Primary metric: unsubscribe rate among billing-adjacent cohorts.
- Guardrail metric: missed billing alert rate.
- Leading indicator: preference-setting completion rate within the first week.
```

## What Good Looks Like

The sprint should not stop at a feature list. It should:

- force the idea through discovery before design
- name the first slice and the explicit exclusions
- produce a PRD-ready scope with success metrics and validation plan

