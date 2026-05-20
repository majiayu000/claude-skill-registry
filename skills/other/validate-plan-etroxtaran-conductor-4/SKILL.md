---
name: validate-plan
tags:
  technology: [python, typescript, javascript]
  feature: [workflow, testing]
  priority: high
summary: Validate implementation plans for completeness and feasibility
version: 1
---

# Validate Plan

## When to use

- After a plan has been created
- Before starting implementation
- When reviewing someone else's plan

## Instructions

1. Check for completeness:
   - All acceptance criteria covered
   - All files identified
   - All tests specified
   - Dependencies mapped

2. Check for feasibility:
   - Tasks are appropriately sized
   - No circular dependencies
   - Technical approach is sound

3. Identify risks and blockers:
   - Missing information
   - Unclear requirements
   - Technical challenges

## Validation Checklist

### Completeness
- [ ] All user stories map to tasks
- [ ] All tasks have file scope
- [ ] All tasks have test requirements
- [ ] Dependencies are explicit

### Feasibility
- [ ] Tasks can be completed independently (where possible)
- [ ] Technical approach is proven or documented
- [ ] No circular dependencies
- [ ] Estimated effort is reasonable

### Risk Assessment
- [ ] Known unknowns are documented
- [ ] Mitigation strategies exist for high risks
- [ ] Blockers have escalation paths

## Output Format

```json
{
  "approved": true|false,
  "score": 1-10,
  "blocking_issues": [],
  "suggestions": [],
  "risks": []
}
```
