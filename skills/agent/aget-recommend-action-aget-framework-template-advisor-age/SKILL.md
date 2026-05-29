---
name: aget-recommend-action
description: Provide recommendations with rationale and alternatives
archetype: advisor
allowed-tools:
  - Read
  - Glob
  - Grep
---

# aget-recommend-action

Provide structured recommendations with clear rationale, alternatives considered, and risk assessment. Advisory role — informs decisions, does not make them.

## Instructions

When this skill is invoked:

1. **Understand the Context**
   - Clarify the decision or question requiring recommendation
   - Identify constraints, goals, and success criteria
   - Note stakeholder perspectives

2. **Analyze Options**
   - Identify at least 2-3 viable alternatives
   - Evaluate each against criteria
   - Document pros and cons

3. **Form Recommendation**
   - Select primary recommendation
   - Articulate clear rationale (why this option)
   - Assign confidence level (High, Medium, Low)

4. **Document Uncertainties**
   - List assumptions made
   - Note information gaps
   - Identify conditions that would change recommendation

## Output Format

```markdown
## Recommendation: [Topic]

### Primary Recommendation

**Action**: [Clear, actionable recommendation]

**Rationale**: [Why this option over alternatives]

**Confidence**: [High/Medium/Low] — [Brief justification]

### Alternatives Considered

| Option | Pros | Cons | Why Not Primary |
|--------|------|------|-----------------|
| [Alt 1] | [+] | [-] | [Reason] |
| [Alt 2] | [+] | [-] | [Reason] |

### Risk Assessment

- **If adopted**: [Key risks]
- **If not adopted**: [Opportunity cost]

### Assumptions

1. [Assumption that, if wrong, changes recommendation]

### Conditions for Revisiting

- Revisit if: [Condition 1]
- Revisit if: [Condition 2]
```

## Constraints

- **C1**: NEVER present recommendations as commands — advisory role is advisory
- **C2**: NEVER hide alternatives that conflict with primary recommendation
- **C3**: NEVER claim certainty when assumptions exist — intellectual honesty required

## Related

- SKILL-015: aget-recommend-action specification
- ONTOLOGY_advisor.yaml: Recommendation, Strategy, Option concepts
- CAP-ADV-002: Recommendation capability
