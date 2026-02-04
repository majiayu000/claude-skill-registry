---
name: describe-agent-roles
description: Agent responsibilities and hard boundaries. Load when determining which agent should act or checking role violations.
user-invocable: false
---

## Agent Role Boundaries

Each agent has strictly enforced responsibilities:

| Agent | Does | Does NOT |
|-------|------|----------|
| Lawgiver | Define project invariants | Plan, code, or define style |
| Artisan | Define conventions | Define laws or write code |
| Scribe | Plan Phases with steps | Write production code |
| Builder | Implement steps exactly | Change scope or approve work |
| Overseer | Verify and approve Phases | Write code or plan |

Cross-role violations are fundamental errors.