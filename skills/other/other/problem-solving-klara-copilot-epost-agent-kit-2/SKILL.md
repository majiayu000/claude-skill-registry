---
name: problem-solving
description: Use when stuck, facing a complex bug, or need root cause analysis — 5 whys, bisection, inversion techniques

metadata:
  agent-affinity: [epost-debugger, epost-implementer, epost-architect]
  keywords: [problem-solving, root-cause, analysis, debugging, 5-whys, bisection, crash, error, stuck]
  platforms: [all]
  triggers: ["stuck", "problem", "root cause", "why"]
  connections:
    enhances: [debugging]
---

# Problem Solving Skill

## Purpose
Root cause analysis and complex problem resolution.

## When Active
User reports bug, system is behaving unexpectedly, debugging feels stuck.

## Expertise

### Techniques

#### Root Cause Analysis (5 Whys)
Ask "why" 5 times to dig past symptoms to fundamental cause.

#### Inversion
Ask "what would make this fail?" then prevent those conditions.

#### Collision Zone Thinking
Find where multiple systems interact. Bugs live at boundaries.

#### State Machine Extraction
When a component behaves unexpectedly, extract its actual state machine from code. Compare actual vs expected transitions — the diff IS the bug. See `planning/references/state-machine-guide.md` for notation.

#### Simplification Cascades
Remove complexity until problem disappears. Add back until it returns.

### When Stuck
1. Change perspective (explain to rubber duck)
2. Bisect the problem (binary search for root cause)
3. Check assumptions (what are you taking for granted?)
4. Sleep on it (context switch resets mental model)
5. Zoom out (is this really the right problem?)

## Patterns

### Root Cause Analysis Format
```
Problem: [Observed behavior]
Why 1: [Immediate cause]
Why 2: [What caused that]
Why 3: [Layer deeper]
Why 4: [Systemic issue]
Why 5: [Fundamental cause]
Fix: [Address root, not symptom]
```

### Bisection Strategy
- Create minimal failing test
- Remove half the code
- Does it still fail? If yes, problem is in remaining half
- Repeat until isolated

## Best Practices
- Fix root causes, not symptoms
- Don't stop at first "why"
- Test your hypothesis before implementing
- Consider environmental factors
- Document the problem-solving path
- Share what you learned with team

### Related Skills
- `debugging` — Systematic debugging methodology
- `error-recovery` — Error handling and recovery patterns
- `knowledge-capture` — Persist root cause findings
- `sequential-thinking` — Structured step-by-step reasoning
