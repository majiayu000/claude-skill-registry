---
name: aget-generate-requirement
description: Generate EARS-compliant requirements
archetype: spec-engineer
allowed-tools:
  - Read
  - Glob
---

# aget-generate-requirement

Generate EARS-compliant requirements from stakeholder input or analysis. Ensures testability and proper formatting.

## Instructions

When this skill is invoked:

1. **Understand the Need**
   - What capability is needed
   - Who needs it
   - Why it's needed

2. **Classify Requirement**
   - Functional: What system does
   - Non-Functional: How well it does it
   - Constraint: Limitation on solution

3. **Select EARS Template**
   - Ubiquitous: Always true
   - Event-Driven: Response to event
   - State-Driven: While in state
   - Conditional: If condition

4. **Assign ID**
   - Follow R-XXX-NNN convention
   - Check for conflicts
   - Maintain sequence

5. **Verify Testability**
   - Can it be verified?
   - What evidence needed?
   - How to test?

## EARS Templates

```
Ubiquitous:
  The [system] SHALL [action].

Event-Driven:
  WHEN [event], the [system] SHALL [action].

State-Driven:
  WHILE [state], the [system] SHALL [action].

Conditional:
  IF [condition], the [system] SHALL [action].

Combined:
  WHEN [event] WHILE [state], IF [condition],
  the [system] SHALL [action].
```

## Output Format

```markdown
## Generated Requirement

### Input

**Need**: [Original description]
**Source**: [Who/What identified this need]

### Classification

| Attribute | Value |
|-----------|-------|
| Type | [Functional/NFR/Constraint] |
| Pattern | [Ubiquitous/Event/State/Conditional] |
| Priority | [Must/Should/May] |

### Requirement

**ID**: R-[XXX]-[NNN]

**Statement**:
> [EARS-formatted requirement]

### Testability

**Verifiable**: Yes

**Test Approach**: [How to verify]

**Acceptance Criteria**:
- [Criterion 1]
- [Criterion 2]

### Traceability

| Link | Reference |
|------|-----------|
| Source | [Need/User story] |
| Related | [Other requirements] |

---

### Clarifying Questions (if ambiguous)

1. [Question about unclear aspect]
```

## ID Convention

```
R-[Domain]-[Number]

Examples:
- R-CLI-001 (CLI domain)
- R-SESSION-002 (Session domain)
- R-SKILL-003 (Skill domain)
```

## Constraints

- **C1**: NEVER generate requirements without EARS format — format consistency required
- **C2**: NEVER accept untestable requirements — requirements must be verifiable
- **C3**: NEVER generate duplicate requirement IDs — IDs must be unique

## Related

- SKILL-034: aget-generate-requirement specification
- ONTOLOGY_spec-engineer.yaml: Requirement, Functional_Requirement concepts
- CAP-SPE-002: Requirement Generation capability
