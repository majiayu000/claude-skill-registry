---
name: aget-assess-tradeoffs
description: Analyze trade-offs between competing architectural concerns
archetype: architect
allowed-tools:
  - Read
  - Glob
  - Grep
---

# aget-assess-tradeoffs

Analyze trade-offs between competing concerns and quality attributes. Provides structured decision support for architectural choices.

## Instructions

When this skill is invoked:

1. **Identify Competing Concerns**
   - List quality attributes in tension
   - Document the options being considered
   - Note constraints and context

2. **Evaluate Options**
   - Rate each option against each quality attribute
   - Use consistent scale (1-5 or Low/Med/High)
   - Consider both immediate and long-term effects

3. **Assess Reversibility**
   - Classify decisions: One-way door vs. Two-way door
   - Note cost of changing later
   - Identify lock-in risks

4. **Formulate Recommendation**
   - Provide clear recommendation
   - Explain trade-off resolution rationale
   - Document rejected alternatives

## Output Format

```markdown
## Trade-off Analysis: [Decision Topic]

### Context

[What decision needs to be made and why]

### Competing Concerns

| Quality Attribute | Option A | Option B | Option C |
|-------------------|:--------:|:--------:|:--------:|
| Performance | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Maintainability | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| Cost | ⭐⭐ | ⭐ | ⭐⭐⭐ |
| Time to Market | ⭐ | ⭐⭐ | ⭐⭐⭐ |

### Reversibility Assessment

| Option | Reversibility | Cost to Change | Lock-in Risk |
|--------|---------------|----------------|--------------|
| A | Low | High | Significant |
| B | High | Low | Minimal |
| C | Medium | Medium | Moderate |

### Recommendation

**Choose**: [Option X]

**Rationale**: [Why this trade-off resolution is appropriate given context]

**What We're Trading**: [Quality we're deprioritizing] for [Quality we're prioritizing]

### Rejected Alternatives

| Option | Why Rejected |
|--------|--------------|
| [Option Y] | [Specific reason] |

### Conditions for Revisiting

- Revisit if: [Condition that would change the analysis]
```

## Constraints

- **C1**: NEVER pretend trade-offs don't exist — architectural honesty requires acknowledging costs
- **C2**: NEVER recommend without explaining trade-off resolution — recommendations need justification
- **C3**: NEVER treat all quality attributes as equally important — context determines priority

## Related

- SKILL-019: aget-assess-tradeoffs specification
- ONTOLOGY_architect.yaml: Trade_off, Quality_Attribute, Decision concepts
- CAP-ARC-002: Trade-off Assessment capability
