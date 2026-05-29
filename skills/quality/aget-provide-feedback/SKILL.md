---
name: aget-provide-feedback
description: Provide structured feedback with severity classification
archetype: reviewer
allowed-tools:
  - Read
  - Glob
---

# aget-provide-feedback

Provide structured feedback with severity classification. Balances constructive criticism with positive observations.

## Instructions

When this skill is invoked:

1. **Review Work Product**
   - Understand context and goals
   - Identify what was attempted
   - Note constraints author faced

2. **Classify Feedback**
   - **Blocking**: Must fix, prevents acceptance
   - **Suggestion**: Should consider, improves quality
   - **Nitpick**: Minor, stylistic
   - **Praise**: Positive, worth acknowledging

3. **Make Actionable**
   - Specific location
   - Clear description
   - Suggested resolution

4. **Balance**
   - Include positive observations
   - Constructive tone
   - Proportionate to significance

## Output Format

```markdown
## Feedback: [Work Product]

### Summary

| Severity | Count |
|----------|-------|
| Blocking | [N] |
| Suggestion | [N] |
| Nitpick | [N] |
| Praise | [N] |

---

### Blocking Issues

1. **[Location]**
   - Issue: [Description]
   - Impact: [Why this blocks]
   - Suggestion: [How to resolve]

---

### Suggestions

1. **[Location]**
   - Observation: [What could be better]
   - Rationale: [Why it matters]
   - Suggestion: [Specific improvement]

---

### Nitpicks

1. **[Location]**: [Minor observation]

---

### Positive Observations

1. **[Location]**: [What was done well]
2. **General**: [Overall strength]

---

### Overall Assessment

[Brief summary of quality level and key points]
```

## Severity Guidelines

| Severity | Criteria | Examples |
|----------|----------|----------|
| Blocking | Prevents functionality, correctness, or compliance | Bug, security issue, spec violation |
| Suggestion | Improves quality, maintainability, clarity | Refactoring opportunity, better naming |
| Nitpick | Style, preference, minor | Formatting, comment wording |
| Praise | Notable positive | Elegant solution, thorough testing |

## Constraints

- **C1**: NEVER classify all feedback as blocking — severity inflation reduces effectiveness
- **C2**: NEVER provide vague feedback — specific feedback enables action
- **C3**: NEVER use harsh or personal language — constructive tone maintains collaboration

## Related

- SKILL-032: aget-provide-feedback specification
- ONTOLOGY_reviewer.yaml: Feedback, Issue, Approval concepts
- CAP-REV-002: Feedback Delivery capability
