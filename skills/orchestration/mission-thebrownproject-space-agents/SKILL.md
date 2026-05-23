---
name: mission
description: "Select feature, select mode, delegate to execution skill."
---

# /mission - Execution Mode Router

Route to the appropriate execution mode for a feature.

## The Process

1. **Select feature** - Run `bd list -t feature --status open`, ask user with AskUserQuestion
2. **Select mode** - Ask user with AskUserQuestion
3. **Delegate** - Invoke skill with feature ID

## Modes

| Mode | Skill | Best For |
|------|-------|----------|
| Solo | `mission-solo` | Small (1-3 tasks) |
| Orchestrated | `mission-orchestrated` | Medium (4-10 tasks) |
| Ralph | `mission-ralph` | Large (10+ tasks) |

Invoke with: `Skill: mission-solo, args: "FEATURE_ID"` (or `mission-orchestrated`, `mission-ralph`)

## If No Features

```
HOUSTON: No features ready. Use /exploration to plan a feature first.
```
