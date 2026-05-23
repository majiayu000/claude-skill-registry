---
name: aget-assess-risk
description: Assess risks with likelihood, impact, and mitigation options
archetype: advisor
allowed-tools:
  - Read
  - Glob
  - Grep
---

# aget-assess-risk

Assess risks associated with decisions, actions, or situations. Produces structured risk analysis with likelihood, impact, and mitigation recommendations.

## Instructions

When this skill is invoked:

1. **Gather Context**
   - Understand the decision, action, or situation being assessed
   - Identify stakeholders and scope boundaries
   - Note any constraints or assumptions

2. **Identify Risks**
   - Enumerate potential risks using standard categories:
     - Operational (process, execution)
     - Strategic (direction, positioning)
     - Financial (cost, revenue)
     - Compliance (regulatory, policy)
     - Technical (implementation, integration)

3. **Assess Each Risk**
   - **Likelihood**: Low, Medium, High, Critical
   - **Impact**: Low, Medium, High, Critical
   - Calculate risk score (Likelihood × Impact)

4. **Propose Mitigations**
   - For High/Critical risks, propose mitigation strategies
   - Categorize as: Avoid, Mitigate, Transfer, Accept

## Output Format

```markdown
## Risk Assessment: [Topic]

### Identified Risks

| Risk | Category | Likelihood | Impact | Score | Mitigation |
|------|----------|------------|--------|-------|------------|
| [Description] | [Cat] | [L/M/H/C] | [L/M/H/C] | [1-16] | [Strategy] |

### Risk Matrix

|          | Low Impact | Medium | High | Critical |
|----------|:----------:|:------:|:----:|:--------:|
| Critical |     ⚠️     |   🔴   |  🔴  |    🔴    |
| High     |     ⚠️     |   ⚠️   |  🔴  |    🔴    |
| Medium   |     ✅     |   ⚠️   |  ⚠️  |    🔴    |
| Low      |     ✅     |   ✅   |  ⚠️  |    ⚠️    |

### High-Priority Mitigations

1. [Risk]: [Mitigation strategy]

### Assumptions & Limitations

- [Assumption 1]
```

## Constraints

- **C1**: NEVER make decisions on behalf of the user — provide assessment, not directives
- **C2**: NEVER present speculation as fact — distinguish known facts from assumptions
- **C3**: NEVER omit identified risks due to perceived sensitivity — complete picture essential

## Related

- SKILL-014: aget-assess-risk specification
- ONTOLOGY_advisor.yaml: Risk, Mitigation concepts
- CAP-ADV-001: Risk Assessment capability
