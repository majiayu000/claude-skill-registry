---
name: aget-validate-spec
description: Validate specifications for completeness and consistency
archetype: spec-engineer
allowed-tools:
  - Read
  - Glob
  - Grep
---

# aget-validate-spec

Validate specifications for completeness, consistency, and testability. Ensures EARS format compliance.

## Instructions

When this skill is invoked:

1. **Check Completeness**
   - Required sections present
   - All requirements have IDs
   - Traceability links exist

2. **Check Consistency**
   - No contradictions
   - Terminology consistent
   - IDs unique

3. **Check Testability**
   - Requirements are verifiable
   - Acceptance criteria clear
   - No vague language

4. **Check Format**
   - EARS templates applied
   - Correct SHALL/SHOULD usage
   - Proper structure

## Required Sections

- Scope
- Requirements (functional)
- Constraints (non-functional)
- Traceability
- Test cases or V-tests

## EARS Patterns

| Pattern | Template |
|---------|----------|
| Ubiquitous | The [system] SHALL [action] |
| Event-Driven | WHEN [event], the [system] SHALL [action] |
| State-Driven | WHILE [state], the [system] SHALL [action] |
| Conditional | IF [condition], the [system] SHALL [action] |

## Output Format

```markdown
## Specification Validation: [Spec Name]

### Overview

| Attribute | Value |
|-----------|-------|
| Spec | [Name] |
| Version | [X.Y.Z] |
| Validator | [Agent] |
| Date | [YYYY-MM-DD] |

---

### Completeness Check

| Section | Status | Notes |
|---------|--------|-------|
| Scope | [Present/Missing] | |
| Requirements | [Present/Missing] | [N] requirements |
| Constraints | [Present/Missing] | [N] constraints |
| Traceability | [Present/Missing] | |
| Tests | [Present/Missing] | [N] tests |

---

### Consistency Check

| Check | Status | Issues |
|-------|--------|--------|
| No contradictions | [Pass/Fail] | [Details] |
| Terminology | [Pass/Fail] | [Details] |
| Unique IDs | [Pass/Fail] | [Details] |

---

### Testability Check

| Requirement | Testable | Issue |
|-------------|----------|-------|
| R-XXX-001 | [Yes/No] | [Why not testable] |

---

### EARS Format Check

| Requirement | Pattern | Compliant | Issue |
|-------------|---------|-----------|-------|
| R-XXX-001 | [Pattern] | [Yes/No] | [Issue] |

---

### Summary

**Status**: [Valid / Issues Found]

**Blocking Issues**: [N]
**Warnings**: [N]

**Required Actions**:
1. [Action 1]
```

## Constraints

- **C1**: NEVER pass specifications with EARS violations — format consistency essential
- **C2**: NEVER modify the specification during validation — validation is read-only
- **C3**: NEVER skip testability assessment — untestable requirements are not requirements

## Related

- SKILL-033: aget-validate-spec specification
- ONTOLOGY_spec-engineer.yaml: Specification, Validation, Traceability concepts
- CAP-SPE-001: Specification Validation capability
