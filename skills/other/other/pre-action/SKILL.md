---
name: pre-action
description: Mandatory decision framework - clarify goal, evaluate options, choose consciously before acting
category: Core Universal
---

# Skill: pre-action

## What I do

I produce a **PREFLIGHT** before any tool calls: clarify goal, identify constraints, plan steps, and mark which calls can run in parallel. This is the PLAN phase — execution comes after via `parallel-execution`.

## When to use me

- **Always** — produce PREFLIGHT before first tool call in any task
- Before irreversible actions (deployment, deletion, commits)
- When facing unclear requirements or multiple viable approaches

## PREFLIGHT Schema (by role)

**Orchestrators** (sisyphus, hephaestus, atlas, Tech-Lead):
```
PREFLIGHT:
  Goal: <one sentence>
  Constraints: <limits, policies, blockers>
  Plan: <≤5 numbered steps>
  Parallel: <which steps are independent>
  Stop: <conditions to halt or escalate>
```

**Workers** (Senior-Engineer, QA-Engineer, Writer, etc.):
```
PREFLIGHT:
  Assumptions: <what I believe to be true>
  Plan: <≤5 numbered steps>
  Parallel: <which steps are independent>
  Risks: <what could go wrong>
```

**Read-only** (explore, Researcher, Data-Analyst):
```
PREFLIGHT:
  Assumptions: <what I believe to be true>
  Plan: <≤3 numbered steps>
  Parallel: <which reads/searches can batch>
```

## After PREFLIGHT

Once PREFLIGHT is complete, use `parallel-execution` skill to batch all independent calls identified in the Parallel field.

## Mid-chain reflection (sequential tool use)

When executing a chain of sequential tool calls where each step depends on the
previous result, apply a reflection step between calls:

**After each significant tool result, ask:**
- Does this result change my plan?
- Am I still on the right path, or do I need to backtrack?
- Do I have all information needed for the next step?

**Before any irreversible action, verify:**
- What exactly will this change?
- Is this the right target (file, record, resource)?
- Can I undo this if wrong?

**When results are unexpected, stop and reassess:**
- Why did I get this result?
- Does my mental model need updating?
- Should I try a different approach?

This is distinct from upfront pre-action thinking — it is reactive, triggered by
new information from tool results. Most valuable in long tool chains, policy-heavy
environments, and sequential decisions where mistakes compound.

## Related skills

- `parallel-execution` — Execute phase: batch independent calls after PREFLIGHT
- `memory-keeper` — Capture decision reasoning
- `critical-thinking` — Rigorous analysis for complex decisions

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Core-Universal/Pre Action.md`
