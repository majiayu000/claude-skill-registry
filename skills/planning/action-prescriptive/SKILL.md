---
name: prescriptive-actions
description: Use when the user asks for recommendations, next steps, best approaches, or “what should I do” guidance to achieve a goal or fix a problem.
version: 1.0
---

# Prescriptive Actions Skill

## Purpose
Provide actionable guidance: recommended approaches, prioritized steps, options, and tradeoffs.

## When to use
Use this skill when the user request is primarily:
- Recommend / advise / propose
- “What should I do?”
- Suggest next steps or an approach
- Diagnose + prescribe direction (but not a full plan)

Do NOT use if the user explicitly asks for:
- a roadmap or timeline (use planning-action)
- a runbook or checklist (use procedural-action)
- success criteria or tests (use validation-action)

## Operating rules
1. Restate the goal in one line.
2. Recommend a primary approach.
3. Provide alternatives when meaningful (A/B).
4. Make tradeoffs explicit (cost, time, risk, complexity).
5. Keep steps high-level and directional, not exhaustive.
6. List assumptions clearly.
7. Follow safety and legality constraints.

## Outputs
Use this structure unless the user specifies otherwise:

### Goal
- One sentence.

### Recommended approach
- 3–6 high-level steps or principles (directional, not detailed).

### Alternatives
- Option A: when to use it
- Option B: when to use it

### Tradeoffs
- Cost / speed / risk / complexity notes

### Key risks
- Major risks to watch (no mitigation plans unless asked)

### Immediate next actions
- 2–5 concrete starting actions (not a full checklist)
