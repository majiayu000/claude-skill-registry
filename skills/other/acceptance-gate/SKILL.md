---
name: vibe-acceptance-gate
description: Validates completed work against defined acceptance criteria. Use after completing a task that has specific success criteria defined in issues, specs, or task descriptions.
user-invocable: true
---

# vibe-acceptance-gate

Don't claim "done" until you've checked against the criteria that define "done."

## When to Use This Skill

- After completing a task that has acceptance criteria
- Before marking an issue/ticket as resolved
- When the user asks "is this done?"
- After implementing a spec with defined requirements

## When NOT to Use This Skill

- Exploratory work with no defined criteria
- Research tasks (use `vibe-reflect-and-compound` instead)
- When criteria haven't been defined yet (define them first)

## Steps

1. **Find the criteria** — Look in:
   - Issue/ticket description (MUST/SHOULD requirements)
   - Spec document (acceptance criteria section)
   - Task description (success conditions)
   - User's original request (implicit criteria)

2. **Validate each criterion** — For each one:
   - Run the relevant test, command, or check
   - Record PASS (met), FAIL (not met), or PARTIAL (partially met)
   - Capture evidence (test output, code reference)

3. **Report results**:

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | [criterion text] | PASS/FAIL/PARTIAL | [evidence] |

4. **Gate decision**:
   - All PASS → Task complete
   - Any FAIL on MUST criteria → Task NOT complete, list remaining work
   - PARTIAL only → Report what's missing, ask user if acceptable

## Output Format

### Acceptance Gate: [Task Name]

**Result**: PASS / FAIL / PARTIAL
**Criteria Met**: X/Y (Z%)

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | ... | ✓/✗/◐ | ... |

### Remaining Work (if FAIL)
1. [What needs to be done]
