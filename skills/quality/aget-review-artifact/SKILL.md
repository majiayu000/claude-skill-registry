---
name: aget-review-artifact
description: Review artifacts against criteria
archetype: reviewer
allowed-tools:
  - Read
  - Glob
  - Grep
---

# aget-review-artifact

Review artifacts against defined criteria and produce structured feedback. Supports code, documentation, designs, and plans.

## Instructions

When this skill is invoked:

1. **Identify Artifact**
   - Type (code, doc, design, plan)
   - Location
   - Context

2. **Determine Criteria**
   - Use provided criteria
   - Or apply standard criteria for artifact type
   - Document criteria used

3. **Evaluate**
   - Assess against each criterion
   - Note strengths and issues
   - Classify findings

4. **Form Recommendation**
   - Approve: Ready as-is
   - Approve with fixes: Minor issues
   - Revise: Significant issues
   - Reject: Fundamental problems

## Standard Criteria by Type

**Code**:
- Correctness, Readability, Test coverage, Standards

**Documentation**:
- Accuracy, Completeness, Clarity, Currency

**Design**:
- Requirements coverage, Feasibility, Quality attributes

**Plan**:
- Scope clarity, Feasibility, Risk coverage, V-tests

## Output Format

```markdown
## Artifact Review: [Name/Path]

### Artifact Info

| Field | Value |
|-------|-------|
| Type | [Code/Doc/Design/Plan] |
| Location | [Path] |
| Reviewer | [Agent] |
| Date | [YYYY-MM-DD] |

---

### Criteria Applied

| Criterion | Weight |
|-----------|--------|
| [Criterion 1] | [High/Med/Low] |
| [Criterion 2] | [High/Med/Low] |

---

### Evaluation

| Criterion | Rating | Notes |
|-----------|--------|-------|
| [Criterion 1] | [Pass/Partial/Fail] | [Details] |
| [Criterion 2] | [Pass/Partial/Fail] | [Details] |

---

### Findings

#### Issues
| Severity | Location | Issue | Suggestion |
|----------|----------|-------|------------|
| Blocking | [Where] | [What] | [How to fix] |
| Suggestion | [Where] | [What] | [Consider] |

#### Strengths
- [Positive observation 1]
- [Positive observation 2]

---

### Recommendation

**Decision**: [Approve / Approve with Fixes / Revise / Reject]

**Rationale**: [Why this decision]

**Required Actions**: (if not Approve)
1. [Action 1]
2. [Action 2]
```

## Constraints

- **C1**: NEVER review without clear criteria — reviews need objective basis
- **C2**: NEVER provide only negative feedback — balanced feedback more effective
- **C3**: NEVER approve artifacts with blocking issues — quality gates must be respected

## Related

- SKILL-031: aget-review-artifact specification
- ONTOLOGY_reviewer.yaml: Review, Artifact, Criteria concepts
- CAP-REV-001: Artifact Review capability
