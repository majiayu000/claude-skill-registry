---
name: sequential-thinking
description: (ePost) Use when facing a complex problem that needs step-by-step breakdown, branching analysis, or iterative reasoning

metadata:
  agent-affinity: [epost-debugger, epost-planner, epost-fullstack-developer, epost-brainstormer]
  keywords: [sequential, thinking, analysis, step-by-step, reasoning, logic, stuck, complex, bug]
  platforms: [all]
  triggers: ["complex problem", "step by step", "analyze"]
  connections:
    enhances: [debug]
---

# Sequential Thinking Skill

## Purpose
Structured step-by-step analysis for complex problems.

## When Active
Use for debugging, test planning, architecture decisions, root cause analysis.

## Expertise

### Core Patterns

#### Linear Decomposition
Break problem into ordered steps. Each step builds on previous.

#### Branching Analysis
Explore multiple paths. Evaluate each independently.

#### Revision Loop
After reaching conclusion, revisit assumptions. Check for gaps.

### Thought Structure
1. State the problem clearly
2. List known facts
3. Identify unknowns
4. Form hypothesis
5. Test hypothesis with evidence
6. Revise if needed
7. State conclusion with confidence level

### When to Use
- **Debugging**: Trace execution flow step by step
- **Testing**: Identify all paths that need coverage
- **Architecture**: Evaluate trade-offs systematically
- **Root Cause**: Follow evidence chain to source
- **Design**: Think through all edge cases

## Patterns

### Hypothesis Testing
```
Hypothesis: [Your guess]
Evidence for: [Supporting facts]
Evidence against: [Contradicting facts]
Conclusion: [Accept/Reject/Uncertain]
```

## Best Practices
- Write your thinking, don't keep it mental
- Verify each step before moving to next
- Challenge assumptions explicitly
- Consider multiple root causes
- Document your reasoning trail

### Related Skills
- `debug` — Systematic debugging methodology
- `problem-solving` — Root cause analysis techniques
- `plan` — Implementation planning and task breakdown
