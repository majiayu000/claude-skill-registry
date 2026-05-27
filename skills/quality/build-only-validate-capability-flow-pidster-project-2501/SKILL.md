---
name: build-only-validate-capability-flow
description: Validate a capability flow specification against schema constraints. Use after designing a process to ensure it conforms to framework rules. Triggers on "validate capability flow", "check process spec", "verify schema compliance".
allowed-tools: Bash, Read
---

# Build-Only: Validate Capability Flow

Validate a capability flow specification against the framework's schema constraints.

**Note**: This skill is prefixed `build-only-` because it is used during framework development, not as part of the framework itself.

## When to Use

Use this skill after designing a capability flow specification to verify:
- Schema constraint compliance (C1-C4)
- Structural completeness
- Consistency between patterns and roles

## Schema Constraints

The capability flow schema defines four core constraints:

| ID | Constraint | Rule |
|----|------------|------|
| **C1** | Human-Only pattern consistency | If Pattern = "Human-Only" then AI Role MUST = "None" |
| **C2** | AI-Only pattern consistency | If Pattern = "AI-Only" then Human Role MUST = "None" |
| **C3** | AI participation implies non-Human-Only | If AI Role ≠ "None" then Pattern MUST ≠ "Human-Only" |
| **C4** | Human participation implies non-AI-Only | If Human Role ≠ "None" then Pattern MUST ≠ "AI-Only" |

## Additional Validation Rules

Beyond C1-C4, check:

| Rule | Description |
|------|-------------|
| **Single capability** | Each step uses exactly one capability from the eight |
| **Escalation defined** | All AI-participating steps have escalation triggers |
| **Completion criteria** | Each step has testable completion criteria |
| **Valid capability** | Capability is one of: Elicit, Analyse, Synthesise, Transform, Validate, Decide, Generate, Preserve |
| **Valid pattern** | Pattern is one of: Human-Only, Human-Led, Partnership, AI-Led, AI-Only |

## How to Validate

### Manual Validation Checklist

For each capability instance in the specification:

```
□ Capability is one of the eight valid capabilities
□ Pattern is one of the five valid patterns
□ C1: If Human-Only, AI Role = "None"
□ C2: If AI-Only, Human Role = "None"
□ C3: If AI Role ≠ "None", Pattern ≠ Human-Only
□ C4: If Human Role ≠ "None", Pattern ≠ AI-Only
□ Escalation triggers defined (if AI participates)
□ Completion criteria are testable
```

### Validation Script

Execute the validation script:

```bash
.claude/skills/build-only-validate-capability-flow/scripts/validate-capability-flow.sh <spec-file>
```

The script reads a YAML capability flow specification and reports:
- Constraint violations
- Missing required fields
- Recommendations for fixes

## Validation Output

The validator returns:
- **PASS** if all constraints satisfied
- **FAIL** with list of violations if any constraint broken

Example output:
```
Validating: process-spec.yaml
Step PA-3: FAIL - C1 violated: Pattern is Human-Only but AI Role is "Proposes decomposition"
Step PA-7: PASS
Step PA-8: PASS
Overall: FAIL (1 violation)
```

## Handling Failures

When validation fails:
1. Identify the specific constraint violated
2. Determine which field is incorrect (Pattern or Role)
3. Either change the pattern to match the roles, or change the roles to match the pattern
4. Re-validate after correction

---

*Part of the AI-Augmented SDLC Framework build tooling*
