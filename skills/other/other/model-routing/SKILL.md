---
name: model-routing
description: Model selection strategy for subagents — haiku for exploration, sonnet for implementation, opus for architecture/security
disable-model-invocation: true
---

# Model Routing Strategy

Route subagents to the cheapest sufficient model. The `model` parameter on Task tool calls controls this.

## When to Run

- Before dispatching Task subagents (which model to use?)
- When a subagent fails quality review (escalate to next tier?)
- When reviewing Ralph epic configuration

## Routing Table

| Task Type | Model | Rationale |
|-----------|-------|-----------|
| Exploration/search (Explore agents) | haiku | Fast, cheap, sufficient for find/read |
| Simple edits, single-file changes | haiku | Clear instructions, low complexity |
| Documentation writing | haiku | Structure is straightforward |
| Multi-file implementation | sonnet | Best balance for coding tasks |
| PR/code review | sonnet | Understands context, catches nuance |
| Test writing | sonnet | Needs pattern matching, not deep reasoning |
| Complex architecture, planning | opus | Deep reasoning required |
| Security analysis | opus | Can't afford to miss vulnerabilities |
| Debugging complex bugs | opus | Needs to hold entire system in mind |
| Ralph subagent tasks | sonnet | Default for autonomous execution, escalate on failure |

## Fallback Escalation

When a subagent fails quality review, retry with the next tier:
1. **haiku fails** → retry with sonnet
2. **sonnet fails** → retry with opus
3. **opus fails** → record failure (circuit breaker)

Do NOT escalate for:
- Syntax errors (fix in same tier)
- Missing imports (fix in same tier)
- Test-only failures with obvious fix (fix in same tier)

Only escalate when the failure indicates insufficient reasoning capability.

## Examples

```
# Explore agent — use haiku
Task(subagent_type="Explore", model="haiku", ...)

# Implementation subagent — use sonnet
Task(subagent_type="general-purpose", model="sonnet", ...)

# Architecture/security review — use sonnet (or opus for security-critical)
Task(subagent_type="code-reviewer", model="sonnet", ...)
```

## Cost Reference

| Model | Input/MTok | Output/MTok | Relative Cost |
|-------|-----------|-------------|---------------|
| Haiku | $0.80 | $4.00 | 1x |
| Sonnet | $3.00 | $15.00 | ~4x |
| Opus | $15.00 | $75.00 | ~19x |
