---
name: aget-document-finding
description: Document research findings with evidence
archetype: researcher
allowed-tools:
  - Read
  - Glob
  - Write
---

# aget-document-finding

Document research findings with evidence, methodology, and implications. Creates structured finding documents for knowledge capture.

## Instructions

When this skill is invoked:

1. **Formulate Finding**
   - Clear, specific statement
   - Falsifiable where possible
   - Scoped appropriately

2. **Document Evidence**
   - Primary sources
   - Data/observations
   - Chain of reasoning

3. **Describe Methodology**
   - How finding was reached
   - Tools/techniques used
   - Reproducibility notes

4. **Articulate Implications**
   - What this means
   - Recommended actions
   - Future research directions

5. **Note Limitations**
   - Scope boundaries
   - Confidence level
   - Known gaps

## Output Format

```markdown
# Research Finding: [Title]

**Date**: [YYYY-MM-DD]
**Researcher**: [Agent Name]
**Status**: [Draft/Reviewed/Accepted]
**Confidence**: [High/Medium/Low]

---

## Finding Statement

[Clear, specific, falsifiable statement of what was discovered]

---

## Evidence

### Primary Sources
1. [Source 1]: [What it shows]
2. [Source 2]: [What it shows]

### Data/Observations
- [Observation 1]
- [Observation 2]

### Reasoning Chain
1. [Premise 1]
2. [Premise 2]
3. Therefore: [Conclusion]

---

## Methodology

**Approach**: [Description of method]

**Tools Used**:
- [Tool 1]
- [Tool 2]

**Reproducibility**: [How to reproduce this finding]

---

## Implications

### Immediate
- [Implication 1]

### Strategic
- [Longer-term implication]

### Recommended Actions
1. [Action 1]
2. [Action 2]

---

## Limitations

1. [Limitation 1]: [How it affects conclusions]
2. [Limitation 2]: [How it affects conclusions]

---

## Future Research

- [Question raised by this finding]

---

## References

1. [Citation 1]
```

## Constraints

- **C1**: NEVER document findings without evidence — findings must be supported
- **C2**: NEVER overstate confidence level — epistemic humility required
- **C3**: NEVER omit contradictory evidence — complete picture enables sound judgment

## Related

- SKILL-030: aget-document-finding specification
- ONTOLOGY_researcher.yaml: Finding, Evidence, Hypothesis concepts
- CAP-RES-002: Finding Documentation capability
