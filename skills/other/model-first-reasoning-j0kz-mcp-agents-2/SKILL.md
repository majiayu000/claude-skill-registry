---
name: model-first-reasoning
description: "Two-phase reasoning paradigm that reduces hallucinations and constraint violations in complex planning tasks. Use when tasks involve multi-step planning, constraint satisfaction, resource allocatio..."
---

# Model-First Reasoning (MFR)

Paradigm that separates **problem representation** from **problem solving**. Before reasoning, explicitly construct a model of the problem space. All subsequent reasoning operates strictly within this model.

## When to Use This Skill

- Multi-step planning with dependencies
- Resource allocation problems
- Scheduling with constraints
- Any task where "it depends on previous steps"
- Problems with explicit rules/invariants
- Tasks with keywords: "plan", "schedule", "allocate", "optimize", "solve", "coordinate"

**Skip for:**
- Single-step factual queries
- Creative tasks without hard constraints
- Simple transformations

## Core Principle

Most planning failures are **representational, not inferential**. When constraints and state are implicit, reasoning appears locally coherent but becomes globally inconsistent. MFR fixes this by making structure explicit and verifiable.

## Two-Phase Process

### Phase 1: Model Construction

Before ANY solution attempt, define:

1. **ENTITIES**: Objects/agents involved (name, type, initial state)
2. **STATE VARIABLES**: Properties that change (variable -> possible values)
3. **ACTIONS**: Operations allowed (action_name | preconditions -> effects)
4. **CONSTRAINTS**: Invariants that must ALWAYS hold

See [references/phase1-model-construction.md](references/phase1-model-construction.md) for template and examples.

**Critical**: Do NOT propose solutions during this phase. Complete the model first.

### Phase 2: Reasoning Over Model

Generate solution using ONLY the constructed model:

- Each action must satisfy its preconditions (reference model explicitly)
- Apply effects to update state variables
- Verify no constraints are violated after each step
- If any step would violate the model: STOP and explain the conflict

See [references/phase2-reasoning.md](references/phase2-reasoning.md) for execution template.

## Domain-Specific References

Load the relevant domain file for pre-defined entity types, common actions, and typical constraints:

- **Ecommerce/inventory**: [references/domains/ecommerce.md](references/domains/ecommerce.md)
- **Scheduling/calendar**: [references/domains/scheduling.md](references/domains/scheduling.md)
- **Resource allocation**: [references/domains/resource-allocation.md](references/domains/resource-allocation.md)

## Model Validation

Before Phase 2, verify:
1. All entities referenced in actions are defined
2. All state variables in preconditions/effects exist
3. Constraints are testable (not vague)
4. Initial state is complete

Optional: Run `scripts/validate_model.py` on XML/JSON model output.

## Output Format

Present the model in structured format (XML or markdown table), then show reasoning as numbered steps with explicit state transitions:

```
Step N: [action_name]
  Preconditions: [list satisfied preconditions]
  Effects: [state variable] := [new value]
  Constraints: [list constraints still valid]
  State after: [updated state summary]
```

## Common Failure Patterns to Avoid

1. **Skipping Phase 1**: Jumping to solutions without explicit model
2. **Implicit constraints**: Assuming rules without stating them
3. **State drift**: Losing track of current state mid-plan
4. **Assumed observations**: Acting on information not in the model

## Quick Reference

| Phase | Goal | Output |
|-------|------|--------|
| **Phase 1** | Build model | Entities, State vars, Actions, Constraints |
| **Phase 2** | Execute plan | Step-by-step with state verification |

## Related Skills

- **Scheduling**: Use `references/domains/scheduling.md` for time-based problems
- **Ecommerce**: Use `references/domains/ecommerce.md` for inventory/pricing
- **Resource Allocation**: Use `references/domains/resource-allocation.md` for capacity planning
