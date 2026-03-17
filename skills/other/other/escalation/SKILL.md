---
name: escalation
description: "Confidence-based model tier escalation for agent tasks. Defines when to escalate from Haiku to Sonnet to Opus, escalation signals, and the never-skip-tiers rule. Use when an agent fails or underperforms."
---

# Model Escalation

## Escalation Tiers

```
Haiku (junior-coder, docs, explainer, optimizer)
  ↓ on failure
Sonnet (coder, tech-lead, reviewer, qa, architect, explorer)
  ↓ on failure
Opus (senior-coder, planner, red-teamer)
```

## Never Skip Tiers

- ALWAYS try the next tier first before jumping to Opus
- Haiku → Sonnet → Opus (never Haiku → Opus directly)
- Each tier gets ONE attempt before escalation
- Exception: if the task is known to require Opus (architecture, cross-cutting), start there

## Escalation Signals

Escalate to the next tier when:

- **Test failures**: Agent's code fails tests and agent can't fix in one retry
- **Clippy warnings**: Agent introduces warnings it can't resolve
- **Wrong output schema**: Agent produces output that doesn't match expected format
- **Tech-lead BLOCKED twice**: Tech-lead rejects the same agent's work twice on the same task
- **Task timeout**: Agent exceeds expected completion time by 2x
- **Repeated hook blocks**: Agent triggers enforcement hooks 3+ times on the same operation

## Do NOT Escalate When

- Task is simply large (break it down instead)
- Agent needs more context (add skills/instructions instead)
- Infrastructure error (retry, don't escalate)
- First-time failure on a reasonable task (retry once at same tier)

## Escalation Protocol

1. Diagnose the failure (see `capability-diagnostic` skill)
2. Determine if it's a model capability issue (Step 3 of diagnostic)
3. If yes: re-assign task to next tier agent with original prompt + "Previous attempt failed because: [reason]"
4. If no: fix the actual issue (context, tools, spec) and retry at same tier

## Tracking

- Log escalations to claude-mem: "Escalated [task type] from [tier] to [tier] because [reason]"
- After 3+ escalations of the same task type → update agent-routing defaults
- The optimizer agent reviews escalation patterns periodically
