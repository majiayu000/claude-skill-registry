---
name: pm-assumption-mapping
description: Assumption mapping and product hypothesis testing frameworks for validating product ideas.
triggers:
  - assumption mapping
  - product hypothesis
  - hypothesis testing
  - riskiest assumption
  - validate assumption
---

# Assumption Mapping & Hypothesis Testing

Frameworks for identifying, prioritizing, and testing product assumptions.

## Riskiest Assumption Test (RAT)

```markdown
## Assumption Map

### Desirability (Will they want it?)
| Assumption | Evidence For | Evidence Against | Risk Level |
|------------|--------------|------------------|------------|
| [Users want X] | [data] | [data] | High/Med/Low |

### Viability (Will it work for the business?)
| Assumption | Evidence For | Evidence Against | Risk Level |
|------------|--------------|------------------|------------|
| [Users will pay $X] | [data] | [data] | High/Med/Low |

### Feasibility (Can we build it?)
| Assumption | Evidence For | Evidence Against | Risk Level |
|------------|--------------|------------------|------------|
| [We can integrate with X] | [data] | [data] | High/Med/Low |

### Riskiest Assumption to Test Next
**Assumption:** [The one with highest risk + least evidence]
**Test:** [Cheapest way to validate/invalidate]
**Success Criteria:** [Specific threshold]
**Timeline:** [Days/weeks]
```

## Product Hypothesis Format

```markdown
## Hypothesis: [Short name]

**We believe that** [building this feature/making this change]
**For** [target user segment]
**Will result in** [expected outcome/behavior change]
**We will know we're right when** [measurable success criteria]

### Riskiest Assumption
[The assumption that if wrong, invalidates the hypothesis]

### Minimum Test
[Cheapest/fastest way to validate]
- Type: [Prototype/Fake door/Concierge/etc]
- Duration: [X days/weeks]
- Sample size: [N users]

### Decision Criteria
- **Ship if:** [specific threshold met]
- **Iterate if:** [mixed signals, specify]
- **Kill if:** [specific threshold not met]
```

## Test Types by Assumption

| Assumption Type | Test Method | Timeline |
|-----------------|-------------|----------|
| Desirability | Fake door, landing page | Days |
| Usability | Prototype testing | Days |
| Value | Concierge MVP | Weeks |
| Feasibility | Technical spike | Days |
| Viability | Pre-sales, LOIs | Weeks |

## Assumption Prioritization

```
Priority = Risk Level × Impact if Wrong × Cost to Test (inverse)
```

Test assumptions that are:
1. High risk (least evidence)
2. High impact (invalidates entire concept)
3. Low cost to test (quick experiments)
