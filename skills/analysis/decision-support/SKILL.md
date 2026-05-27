---
name: decision-support
description: Facilitate data-driven technical decisions using embedded decision matrices and trade-off analysis. Use when relevant to the task.
---

# decision-support

Facilitate data-driven technical decisions using embedded decision matrices and trade-off analysis.

## Triggers

- "help me decide"
- "compare options"
- "trade-off analysis"
- "decision matrix"
- "which approach should we use"
- "evaluate alternatives"

## Purpose

This skill facilitates structured decision-making for technical and architectural choices by:
- Building weighted decision matrices
- Analyzing trade-offs across multiple dimensions
- Documenting decision rationale
- Generating Architecture Decision Records (ADRs)
- Tracking decision outcomes

## Behavior

When triggered, this skill:

1. **Identifies decision context**:
   - Parse the decision question
   - Identify stakeholders and constraints
   - Determine decision type (architectural, technical, process)

2. **Gathers alternatives**:
   - List candidate options
   - Research each alternative
   - Document key characteristics

3. **Defines evaluation criteria**:
   - Identify relevant factors
   - Assign weights based on priorities
   - Define scoring rubrics

4. **Builds decision matrix**:
   - Score each option per criterion
   - Calculate weighted totals
   - Visualize comparisons

5. **Analyzes trade-offs**:
   - Identify strengths/weaknesses
   - Document risks per option
   - Consider long-term implications

6. **Generates recommendation**:
   - Provide data-backed recommendation
   - Document minority positions
   - Create ADR for record

## Decision Types

### Architectural Decisions

```yaml
architectural:
  examples:
    - database_selection
    - api_design_pattern
    - microservices_vs_monolith
    - authentication_approach
    - caching_strategy

  typical_criteria:
    - scalability
    - maintainability
    - performance
    - security
    - team_expertise
    - cost
    - time_to_implement
```

### Technical Decisions

```yaml
technical:
  examples:
    - library_selection
    - framework_choice
    - language_selection
    - testing_approach
    - ci_cd_tooling

  typical_criteria:
    - maturity
    - community_support
    - documentation
    - learning_curve
    - integration_ease
    - license_compatibility
```

### Process Decisions

```yaml
process:
  examples:
    - branching_strategy
    - release_cadence
    - review_process
    - documentation_approach
    - communication_tools

  typical_criteria:
    - team_fit
    - efficiency
    - quality_impact
    - adoption_effort
    - tooling_support
```

## Decision Matrix Template

```markdown
# Decision Matrix: [Decision Title]

**Decision ID**: DEC-2025-001
**Date**: 2025-12-08
**Status**: Under Evaluation
**Decision Owner**: [Name]
**Stakeholders**: [List]

## Context

[Description of the problem or opportunity requiring a decision]

## Constraints

- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

## Options Under Consideration

### Option A: [Name]
- **Description**: [Brief description]
- **Pros**: [Key advantages]
- **Cons**: [Key disadvantages]
- **Risk Level**: Low/Medium/High

### Option B: [Name]
- **Description**: [Brief description]
- **Pros**: [Key advantages]
- **Cons**: [Key disadvantages]
- **Risk Level**: Low/Medium/High

### Option C: [Name]
- **Description**: [Brief description]
- **Pros**: [Key advantages]
- **Cons**: [Key disadvantages]
- **Risk Level**: Low/Medium/High

## Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Scalability | 25% | Ability to handle growth |
| Maintainability | 20% | Ease of ongoing maintenance |
| Performance | 20% | Speed and efficiency |
| Security | 15% | Security posture |
| Team Expertise | 10% | Team familiarity |
| Cost | 10% | Total cost of ownership |

## Scoring Rubric

| Score | Meaning |
|-------|---------|
| 5 | Excellent - Exceeds requirements |
| 4 | Good - Meets all requirements |
| 3 | Adequate - Meets most requirements |
| 2 | Poor - Meets some requirements |
| 1 | Unacceptable - Does not meet requirements |

## Decision Matrix

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Scalability | 25% | 4 (1.00) | 5 (1.25) | 3 (0.75) |
| Maintainability | 20% | 5 (1.00) | 3 (0.60) | 4 (0.80) |
| Performance | 20% | 4 (0.80) | 5 (1.00) | 3 (0.60) |
| Security | 15% | 4 (0.60) | 4 (0.60) | 5 (0.75) |
| Team Expertise | 10% | 5 (0.50) | 2 (0.20) | 4 (0.40) |
| Cost | 10% | 3 (0.30) | 4 (0.40) | 3 (0.30) |
| **Total** | 100% | **4.20** | **4.05** | **3.60** |

## Trade-off Analysis

### Option A vs Option B
- **A wins on**: Maintainability (+2), Team Expertise (+3)
- **B wins on**: Scalability (+1), Performance (+1), Cost (+1)
- **Key trade-off**: Immediate productivity vs long-term scale

### Option A vs Option C
- **A wins on**: Scalability (+1), Maintainability (+1), Performance (+1)
- **C wins on**: Security (+1)
- **Key trade-off**: Overall capability vs security focus

## Risk Assessment

| Option | Key Risks | Mitigation |
|--------|-----------|------------|
| A | May hit scale limits in 2 years | Plan migration path |
| B | Learning curve may slow initial dev | Training budget |
| C | Performance concerns at scale | Performance testing |

## Recommendation

**Recommended Option**: Option A

**Rationale**:
1. Highest weighted score (4.20)
2. Strong team expertise reduces implementation risk
3. Best maintainability for long-term ownership
4. Acceptable scalability with documented migration path

**Dissenting Views**:
- [Stakeholder X] prefers Option B for scalability headroom
- Noted for future re-evaluation if growth exceeds projections

## Decision Record

**Decision**: Adopt Option A
**Decided By**: [Decision Owner]
**Date**: 2025-12-08
**Review Date**: 2026-06-08 (6 months)

## Action Items

- [ ] Document implementation approach
- [ ] Create ADR
- [ ] Communicate decision to team
- [ ] Set up review milestone
```

## ADR Generation

When a decision is finalized, generate an ADR:

```markdown
# ADR-XXX: [Decision Title]

## Status

Accepted

## Context

[Background and problem statement]

## Decision

We will use [Option A] because [rationale summary].

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Trade-off 1]
- [Trade-off 2]

### Neutral
- [Observation 1]

## Alternatives Considered

### Option B: [Name]
Rejected because: [reason]

### Option C: [Name]
Rejected because: [reason]

## References

- Decision Matrix: .aiwg/decisions/DEC-2025-001.md
- Related ADRs: ADR-XXX
```

## Usage Examples

### Full Decision Analysis

```
User: "Help me decide between PostgreSQL and MongoDB for our user service"

Skill executes:
1. Identify decision: Database selection for user service
2. Gather alternatives: PostgreSQL, MongoDB, (suggests DynamoDB)
3. Define criteria based on user service requirements
4. Build comparison matrix
5. Analyze trade-offs
6. Generate recommendation

Output:
"Decision Analysis: User Service Database

Options Evaluated:
1. PostgreSQL (Score: 4.35)
2. MongoDB (Score: 3.90)
3. DynamoDB (Score: 3.65)

Recommendation: PostgreSQL

Key Factors:
- Strong ACID compliance for user data
- Team has SQL expertise
- Proven scalability with proper indexing
- Better for relational user data patterns

Trade-off Accepted:
- Less flexibility for schema changes
- Mitigation: Use JSONB for extensible fields

Decision Matrix: .aiwg/decisions/database-selection.md
ADR: .aiwg/architecture/adr-015-user-db.md"
```

### Quick Comparison

```
User: "Compare options for API gateway"

Skill generates:
- Kong vs AWS API Gateway vs Nginx
- Weighted criteria comparison
- Quick recommendation

Output:
"API Gateway Comparison:

| Criteria | Kong | AWS GW | Nginx |
|----------|------|--------|-------|
| Features | 5 | 4 | 3 |
| Cost | 3 | 4 | 5 |
| Ops Effort | 3 | 5 | 2 |
| Flexibility | 5 | 3 | 5 |
| Weighted | 4.1 | 4.0 | 3.8 |

Recommendation: Kong (slight edge)
Key: Best feature set with acceptable ops overhead

Want full analysis? Say 'full decision matrix'"
```

### Trade-off Focus

```
User: "What are the trade-offs between microservices and monolith?"

Skill analyzes:
- Key dimensions
- Specific trade-offs
- When each is preferred

Output:
"Microservices vs Monolith Trade-offs:

Microservices Wins:
✓ Independent scaling
✓ Technology flexibility
✓ Team autonomy
✓ Fault isolation

Monolith Wins:
✓ Simpler operations
✓ Easier debugging
✓ Lower latency (no network)
✓ Faster initial development

Decision Factors:
- Team size: <10 devs → monolith
- Scale needs: 10x+ growth → microservices
- Domain complexity: Clear boundaries → microservices

Want me to build a decision matrix for your specific context?"
```

## Integration

This skill uses:
- `project-awareness`: Context for decision constraints
- `artifact-metadata`: Track decision lifecycle
- `template-engine`: Load ADR templates

## Agent Orchestration

```yaml
agents:
  research:
    agent: technical-researcher
    focus: Gather data on alternatives

  architecture:
    agent: architecture-designer
    focus: Architectural implications

  security:
    agent: security-architect
    focus: Security trade-offs
    condition: security_relevant == true

  cost:
    agent: business-process-analyst
    focus: Cost and resource implications
```

## Configuration

### Default Criteria Sets

```yaml
criteria_sets:
  architectural:
    - {name: scalability, weight: 20, default: true}
    - {name: maintainability, weight: 20, default: true}
    - {name: performance, weight: 15, default: true}
    - {name: security, weight: 15, default: true}
    - {name: team_expertise, weight: 10, default: true}
    - {name: cost, weight: 10, default: true}
    - {name: time_to_implement, weight: 10, default: true}

  library_selection:
    - {name: maturity, weight: 20}
    - {name: community_support, weight: 20}
    - {name: documentation, weight: 15}
    - {name: learning_curve, weight: 15}
    - {name: license, weight: 15}
    - {name: performance, weight: 15}
```

### Decision Thresholds

```yaml
thresholds:
  clear_winner: 0.5  # Score gap for clear recommendation
  close_call: 0.2    # Gap requiring stakeholder input
  tie: 0.1           # Effectively equal, other factors decide
```

## Output Locations

- Decision matrices: `.aiwg/decisions/`
- ADRs: `.aiwg/architecture/adr-*.md`
- Decision log: `.aiwg/decisions/decision-log.md`

## References

- ADR template: templates/analysis-design/adr-template.md
- Decision matrix template: templates/management/decision-matrix.md
- Trade-off catalog: docs/common-tradeoffs.md
