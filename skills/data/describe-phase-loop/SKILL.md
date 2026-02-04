---
name: describe-phase-loop
description: Plan-Build-Review cycle and agent handoffs. Load when transitioning between agents or understanding workflow progression.
user-invocable: false
---

## The Phase Loop

```
Plan (Scribe) → Build (Builder) → Review (Overseer)
                      ↑                    ↓
                      └───── refine ───────┘
```

- **Planning** produces a Phase folder on disk
- **Building** modifies code and updates progress
- **Review** either declares the Phase complete OR adds follow-up steps and sends back to Build

No Phase is complete without Overseer approval.