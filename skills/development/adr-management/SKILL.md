---
name: adr-management
description: Create and manage Architecture Decision Records (ADRs). Use when documenting technology choices, design decisions, or architectural changes that need to be tracked over time.
allowed-tools: Read, Write, Glob, Grep, Skill
---

# ADR Management

## When to Use This Skill

Use this skill when you need to:

- Document a technology choice or design decision
- Record why a particular approach was selected over alternatives
- Track the history of architectural decisions
- Create a searchable record of decisions for team onboarding

**Keywords:** adr, architecture decision record, decision log, why we chose, alternatives considered, design decision, technology choice

## ADR Workflow

### Creating a New ADR

1. **Determine the next ADR number**
   - Check existing ADRs in `/architecture/adr/`
   - Use sequential numbering: 0001, 0002, 0003, etc.

2. **Create the ADR file**
   - Location: `/architecture/adr/NNNN-title-in-kebab-case.md`
   - Use the template from `references/adr-template.md`

3. **Fill in required sections**
   - Status: Start with "Proposed"
   - Date: Current date in YYYY-MM-DD format
   - Context: Describe the problem and constraints
   - Decision: State the decision clearly
   - Consequences: List positive, negative, and neutral outcomes

4. **Document alternatives**
   - List each alternative considered
   - Include pros, cons, and why it was rejected

5. **Optional: Generate context diagram**
   - If visualization plugin is available, generate a diagram showing the decision's context
   - Use: `visualization:diagram-generator` for C4 or component diagrams

### ADR Status Lifecycle

| Status | Meaning |
| --- | --- |
| Proposed | Decision is under discussion |
| Accepted | Decision has been approved and implemented |
| Deprecated | Decision is no longer relevant but kept for history |
| Superseded | Decision has been replaced by a newer ADR |

When superseding an ADR:

1. Update the old ADR's status to "Superseded by ADR-XXXX"
2. Reference the old ADR in the new ADR's "Related Decisions" section

### Searching Existing ADRs

Before creating a new ADR, search for existing relevant decisions:

```bash
# Search ADR titles
ls /architecture/adr/

# Search ADR content for keywords
grep -r "keyword" /architecture/adr/
```

## Integration with Architecture Principles

Link ADRs to architecture principles when the decision:

- Implements a principle
- Makes a trade-off against a principle
- Establishes a new principle

Reference format: "This decision implements Principle P1: [Principle Name]"

## Template Reference

The ADR template is available at `references/adr-template.md`. Key sections:

- **Status**: Current state of the decision
- **Date**: When the decision was made
- **Deciders**: Who was involved
- **Context**: Problem and constraints
- **Decision**: What was decided
- **Consequences**: Outcomes (positive, negative, neutral)
- **Alternatives Considered**: What else was evaluated
- **Related Decisions**: Links to related ADRs
- **References**: Supporting documentation

## Best Practices

1. **One decision per ADR** - Keep ADRs focused
2. **Immutable history** - Never delete ADRs, only supersede
3. **Link decisions** - Reference related ADRs
4. **Include context** - Future readers need to understand the constraints
5. **Be honest about trade-offs** - Document negative consequences too

## Related: Specification-Driven ADRs

If you're extracting decisions FROM specifications, consider using the `spec-driven-development` plugin's `/spec:adr:create` which links ADRs directly to specification IDs (SPEC-xxx). Those ADRs are stored in `docs/adr/` (linked to specification IDs).

Both approaches use MADR format and can coexist in the same project.

## Repository Structure

Ensure your project has the standard architecture directory:

```text
/architecture/
  /adr/
    0001-record-template.md
    0002-first-decision.md
    ...
```

If the directory doesn't exist, create it before adding ADRs.

## Version History

- **v1.0.0** (2025-12-05): Initial release
  - ADR creation and management workflow
  - Status lifecycle documentation
  - Integration with architecture principles
  - Template reference and best practices

---

## Last Updated

**Date:** 2025-12-05
**Model:** claude-opus-4-5-20251101
