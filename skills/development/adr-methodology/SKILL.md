---
name: adr-methodology
description: This skill should be used when the user asks to "create an ADR", "document an architecture decision", "compare architectural options", "generate assessment criteria", "analyze trade-offs", or mentions Architecture Decision Records, MADR templates, or decision matrices.
---

# ADR Methodology

Structured frameworks for documenting architectural decisions with human-in-the-loop AI assistance.

## Core Principle

AI handles drafting, formatting, and enumeration. Humans provide project-specific context, stakeholder awareness, and final decision accountability.

**AI assists with:**

- Research and enumeration of options
- Consistent formatting
- Risk/trade-off summarization
- Matrix generation

**Humans provide:**

- Project-specific context and constraints
- Stakeholder empathy and political nuance
- Final decision accountability

## Workflow Stages

### Stage 1: Context to Criteria (`/adr-assistant:new`)

Gather decision context and generate assessment criteria.

1. Ask for problem description, constraints, stakeholders, initial options
2. Select appropriate framework (Salesforce Well-Architected or Technical Trade-off)
3. Generate criteria grouped by framework pillars
4. For each criterion: name, rationale for this decision, definition of "good"
5. Write criteria to `.claude/adr-session.yaml`
6. Prompt user to refine criteria before analysis

### Stage 2: Options Matrix (`/adr-assistant:analyze`)

Evaluate options against criteria with risk ratings.

1. Read criteria from `.claude/adr-session.yaml`
2. For each option, rate against each criterion (Low/Medium/High risk)
3. Include rationale for each rating
4. Generate comparison matrix table
5. Write analysis to state file
6. Prompt user to refine ratings before generation

### Stage 3: ADR Generation (`/adr-assistant:generate`)

Output final ADR document using MADR template.

1. Read criteria and analysis from state file
2. Ask user which option they're choosing and why
3. Generate ADR with AI disclosure
4. Auto-detect next ADR number from `docs/adr/`
5. Write ADR file
6. Clear state file

## Assessment Frameworks

### Salesforce Well-Architected (Trusted/Easy/Adaptable)

Use for enterprise decisions with security, UX, and scale concerns.

**Trusted**: Data security, compliance, access control, audit/governance
**Easy**: User experience, deployment complexity, integration effort, maintenance
**Adaptable**: Scalability, future flexibility, cost trajectory, team skill alignment

### Technical Trade-off Framework

Use for infrastructure and tooling decisions.

**Operational**: Setup complexity, maintenance burden, monitoring, failure modes
**Development**: Learning curve, velocity, testing approach, documentation quality
**Integration**: Ecosystem compatibility, migration path, dependency management, lock-in risk

### Custom Framework

When neither standard framework fits:

1. Extract 3-5 key decision drivers from context
2. Create criteria that directly measure those drivers
3. Ensure criteria are evaluatable (not vague)
4. Include at least one "reversibility" criterion

## Risk Ratings

| Rating | Definition | Governance |
|--------|------------|------------|
| **Low** | Minimal risk to requirements, performance, or scale | Standard review |
| **Medium** | Manageable risk with proper governance | Documented mitigation |
| **High** | Significant risk without active mitigation | Explicit acceptance |

**Assign Low when**: Option aligns naturally, no significant trade-offs, team has experience, reversible
**Assign Medium when**: Trade-offs exist but manageable, requires discipline, some learning curve, partially reversible
**Assign High when**: Conflicts with requirement, requires significant mitigation, team lacks experience, hard to reverse

**Consistency rule**: At least one option should be Low or Medium for each criterion. If all options are High, the criterion may be a blocker rather than a trade-off.

## State File Format

State persists to `.claude/adr-session.yaml`:

```yaml
topic: "Database selection for user service"
status: "analyzed"  # new | criteria_defined | analyzed
framework: "technical"  # salesforce | technical | custom
criteria:
  - name: "Data consistency"
    pillar: "Operational"
    rationale: "ACID compliance needed for financial data"
    good_looks_like: "Full transaction support with rollback"
options:
  - name: "PostgreSQL"
    ratings:
      "Data consistency":
        risk: "Low"
        rationale: "Full ACID support, mature transaction handling"
```

## ADR Output Format

Use MADR template. Include AI disclosure section:

```markdown
## AI Disclosure

This ADR was drafted with AI assistance (Claude). Assessment criteria and
rationale were reviewed by decision-makers listed above. Final decision
made by humans.
```

## Additional Resources

### Reference Files

For detailed templates and frameworks, consult:

- **`references/templates.md`** - Complete ADR templates (MADR, Nygard, Y-statement)
- **`references/criteria-frameworks.md`** - Detailed assessment criteria by framework
- **`references/risk-ratings.md`** - Comprehensive risk rating guidelines
