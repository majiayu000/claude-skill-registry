---
name: narratological-algorithms
description: Distill artist/theorist narrative principles into formal, implementable algorithmic frameworks. Use when asked to extract, formalize, or systematize narrative techniques from any storytelling source—filmmakers, writers, theorists, game designers, showrunners. Triggers on requests involving narrative principle extraction, story structure analysis, craft methodology formalization, or creating implementable storytelling protocols.
license: MIT
---

# Narratological Algorithm Distillation

Transform narrative principles from artists, theorists, and practitioners into formal, implementable algorithmic frameworks.

## Workflow

### 1. Source Classification

Identify source type to calibrate extraction approach:

| Type | Characteristics | Extraction Focus |
|------|-----------------|------------------|
| **Theorist** | Prescriptive texts (McKee, Aristotle) | Direct principle extraction |
| **Practitioner** | Interviews, commentary, production docs | Reverse-engineering from stated methods |
| **Classical** | Ancient/foundational texts (Poetics, Natyasastra) | Translation of archaic terminology |
| **Analyst** | Secondary analysis of creator's work | Validation against primary sources |

### 2. Primary Source Prioritization

Always prioritize **primary sources** over secondary analysis:
- Direct quotes from the creator
- Production documents, interviews, lectures
- The creator's own articulated methodology
- Documented working processes

When using secondary sources, validate principles against primary evidence. Flag where principles are inferred vs. directly stated.

### 3. Principle Extraction Protocol

For each identified principle:

```
EXTRACT:
  1. Locate source statement (direct quote when available)
  2. Identify underlying mechanism (why it works)
  3. Formulate as rule or constraint
  4. Determine scope (universal vs. context-specific)
  5. Map to existing narrative theory where applicable
```

### 4. Document Structure

Generate output following the canonical structure. See [references/output-template.md](references/output-template.md) for the full template.

**Required sections:**
1. Meta-Principles (Axioms)
2. Structural Hierarchy
3. Core Algorithms/Protocols
4. Diagnostic Questions/Tests
5. Quick Reference Card

**Optional sections (as warranted):**
- Episode/Scene Templates
- Theoretical Correspondence Tables
- Source Cross-Reference Appendix

### 5. Formalization Patterns

Convert principles to implementable forms:

| Source Form | Target Form |
|-------------|-------------|
| Conceptual statement | Constraint rule |
| Process description | Pseudocode function |
| Best practice | Validity test |
| Comparison | Decision table |
| Taxonomy | Classification tree |

See [references/formalization-patterns.md](references/formalization-patterns.md) for detailed examples.

### 6. Axiom Identification

Identify 3-7 meta-principles that underpin the creator's entire approach:

```
AXIOM_CRITERIA:
  - Foundational (other principles derive from it)
  - Non-negotiable in the creator's worldview
  - Distinguishes this approach from alternatives
  - Stated explicitly or demonstrated consistently
```

Format axioms with unique identifiers: `[CREATOR_INITIALS]-A[N]`

### 7. Validation Checks

Before finalizing, verify:

- [ ] All principles traceable to source material
- [ ] Pseudocode is syntactically coherent
- [ ] Decision tables have complete coverage
- [ ] Quick reference captures essential operations
- [ ] Diagnostic questions are answerable yes/no
- [ ] Theoretical correspondences are accurate

### 8. Cross-Medium Adaptation Notes

When source material is medium-specific, include adaptation guidance for:
- Film → Television (serialization, episode structure)
- Literature → Interactive (agency, branching)
- Single creator → Collaborative (writers' room dynamics)
- Western → Non-Western theoretical traditions

## Reference Files

- **[references/output-template.md](references/output-template.md)** — Full document structure template
- **[references/formalization-patterns.md](references/formalization-patterns.md)** — Examples of converting prose to algorithms
- **[references/theoretical-correspondences.md](references/theoretical-correspondences.md)** — Mapping table across narrative traditions
