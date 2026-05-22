---
name: agent-ops-impl-details
description: "Extract, plan, or propose implementation details at configurable depth levels (low/normal/extensive). Outputs to reference files for team discussion and handoff."
category: utility
invokes: [agent-ops-state]
invoked_by: [agent-ops-planning, agent-ops-implementation]
state_files:
  read: [focus.md, issues/*.md, issues/references/*]
  write: [focus.md, issues/references/*]
reference: [REFERENCE.md]
---

# Implementation Details

Generate detailed implementation specifications at varying depths.

**Reference**: See [REFERENCE.md](REFERENCE.md) for templates, examples, and output formats.

---

## Depth Levels

| Level | Name | Includes | Use Case |
|-------|------|----------|----------|
| 1 | `low` | Files, approach, dependencies, risks | Quick alignment |
| 2 | `normal` | + Signatures, pseudo-code, data structures | Technical review |
| 3 | `extensive` | + **Actual executable code**, edge cases, tests | Formal spec |

### Auto-Selection by Confidence

| Confidence | Level | Override |
|------------|-------|----------|
| LOW | **extensive** (mandatory) | No |
| NORMAL | normal | Yes |
| HIGH | low | Yes |

**LOW confidence requires extensive details with actual executable code.**

---

## Modes

### Extract Mode
Document existing code to understand how it works.

**Input**: File path or symbol name

**Procedure**:
1. Identify target (file or symbol)
2. Analyze at requested level
3. Generate reference file: `.agent/issues/references/{context}-impl-extract.md`

### Plan Mode
Generate implementation details for planned changes.

**Input**: Issue ID (e.g., `FEAT-0083@c5f3e7`)

**Procedure**:
1. Read issue requirements and acceptance criteria
2. Analyze affected code
3. Generate details at requested level
4. Create reference file: `.agent/issues/references/{ISSUE-ID}-impl-plan.md`
5. Link from issue's `spec_file` field

### Propose Mode
Suggest implementation approach for a conceptual change.

**Input**: Description of desired change

**Procedure**:
1. Identify affected areas
2. Generate approach options
3. Create proposal file: `.agent/issues/references/{context}-impl-proposal.md`

---

## Output Sections

All levels include:
- **Summary**: One-paragraph overview
- **Files Affected**: Table of files and actions
- **Approach**: Technical rationale

Normal adds:
- **Detailed Changes**: Function signatures, code locations
- **Dependencies**: What this requires/enables
- **Risks**: Potential issues with mitigations

Extensive adds:
- **Complete Implementation**: Full executable code
- **Edge Cases**: Table of cases and handling
- **Test Cases**: Complete test functions

---

## Invocation

```bash
# Extract existing code
/agent-impl-details extract src/services/auth.ts --level normal

# Plan for issue
/agent-impl-details plan FEAT-0083@c5f3e7 --level extensive

# Propose approach
/agent-impl-details propose "Add rate limiting to API" --level low
```

---

## Confidence Indicators

Output should include:

```markdown
## Confidence Indicators

### ✅ High Confidence
- All files identified
- Clear API contracts

### ⚠️ Uncertainty
- {Area}: {Why}

### ❓ Blockers
- {Question needing answer}
```
