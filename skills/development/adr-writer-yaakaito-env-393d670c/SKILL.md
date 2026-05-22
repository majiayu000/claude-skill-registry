---
name: adr-writer
description: Skill for creating and editing Architecture Decision Records (ADRs). Use when requests involve "create ADR", "record architecture decision", or "document design decisions". Supports creating new ADRs, updating existing ADRs, and reviewing ADR format.
---

# ADR Writer

A skill for creating Architecture Decision Records (ADRs). Generates ADRs following project-specific format conventions.

## ADR Format

### File Naming Convention

```
adr-NNN-short-description-in-english-with-hyphens.md
```

Example: `adr-002-new-feature.md`

### Storage Location

```
docs/adr/
```

### Structure

````markdown
# Title (in English)

## Status

Approved

## Context

Describe the background, challenges, and current issues. Follow the flow: facts → challenges → what you want to solve.
Use lists to enumerate facts and issues. Avoid adding sub-headers; prefer prose and lists within this section.

## Decision

Start with a brief summary of the overall decision (1-2 paragraphs). Then, if there are multiple decisions, create a sub-section for each (e.g., ### Decision 1).
However, avoid creating too many sub-sections unnecessarily. Use tables or Mermaid diagrams as needed.

**Important**: Do NOT include implementation-specific code. Use pseudocode only to illustrate concepts.

## Consequences

### Positive

- Positive outcomes and benefits

### Negative

- Negative outcomes, drawbacks, and trade-offs

### Neutral

- Neutral impacts and side effects

## Notes

### Alternatives Considered

- **Alternative A**: Reason for not adopting
- **Alternative B**: Reason for not adopting

### References

- Related ADRs and external resources
````

## Creation Steps

1. **Determine next ADR number**: Check existing files in `docs/adr/` to determine the next number
2. **Use example**: Refer to `assets/adr-example.md`
3. **Fill in each section**:
   - Title should be concise and in English
   - Context/Decision/Consequences/Notes should be detailed and in Japanese
   - Add code blocks, tables, and Mermaid diagrams as needed
4. **Save file**: Save as `docs/adr/adr-NNN-description.md`

## Examples

- [assets/adr-example.md](assets/adr-example.md) - Structure template with explanations
- Before writing, read the two most recent ADRs in `docs/adr/` to understand the current format and writing style

## Writing Guidelines

- **Status**: Always set to "Approved"
- **Strict structure adherence**: Follow the defined ADR format strictly. Before adding any new headers or sections, carefully consider whether it is truly necessary. Prefer using lists or prose within existing sections
- **Context**: Clearly explain "why this decision is needed now"
- **Decision**: Be specific and implementation-ready. Avoid vague expressions
- **Code examples**: Never include implementation-specific code from the actual codebase. Use pseudocode only to illustrate concepts and help readers understand the design. Pseudocode should be language-agnostic and focus on the "what" rather than the "how"
- **Consequences**: Honestly describe both benefits and drawbacks. No solution is perfect
- **Alternatives Considered**: Document alternatives that were considered and explain why they were not adopted
