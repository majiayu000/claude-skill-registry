---
name: commerce-subscriptions
description: Manage subscription plans, billing cycles, and subscriptions. Use when running `stateset-subscriptions` or updating subscription state.
---

# Commerce Subscriptions

Handle recurring billing plans and customer subscriptions.

## How It Works

1. Create or update subscription plans.
2. Enroll customers and manage subscription status.
3. Pause, resume, cancel, or skip billing cycles.
4. Review billing history and events.

## Usage

- CLI: `stateset-subscriptions ...`
- Writes require `--apply`.
- MCP tools: `create_subscription_plan`, `create_subscription`, `pause_subscription`, `resume_subscription`, `cancel_subscription`, `list_billing_cycles`.

## Output

```json
{"status":"active","subscription_id":"sub_123","plan":"monthly"}
```

## Present Results to User

- Plan and subscription identifiers.
- Billing interval and next charge date.
- Any proration or cancellation details.

## Troubleshooting

- Plan archived: select an active plan.
- Past due: review billing cycles and payment status.

## References
- references/subscriptions-flow.md
- /home/dom/stateset-icommerce/cli/.claude/agents/subscriptions.md
