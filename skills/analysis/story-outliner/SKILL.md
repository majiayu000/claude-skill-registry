---
name: story-outliner
description: Read and comprehend story text, summarize characters, relationships, plots, organize into fluent outline. Suitable for quickly understanding story core, providing outline foundation for script creation
category: story-analysis
version: 2.1.0
last_updated: 2026-01-11
license: MIT
compatibility: Claude Code 1.0+
maintainer: Gong Fan
allowed-tools:
  - Read
model: opus
changelog:
  - version: 2.1.0
    date: 2026-01-11
    changes:
      - type: improved
        content: Optimized description field to be more concise and comply with imperative language specifications
      - type: added
        content: Added allowed-tools (Read) and model (opus) fields
      - type: improved
        content: Optimized descriptions of functionality, use cases, core steps, input requirements, output format, requirements, etc. to comply with imperative language specifications
      - type: added
        content: Added constraints, examples, and detailed documentation sections
  - version: 2.0.0
    date: 2026-01-11
    changes:
      - type: breaking
        content: Refactored according to Agent Skills official specifications
      - type: improved
        content: Optimized description, using imperative language, simplified main content
      - type: added
        content: Added license and compatibility optional fields
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: Initial version
---

# Story Outline Generation Expert

## Functionality

Deeply read and comprehend story text, summarize characters, character relationships, plots, organize into fluent story outline.

## Use Cases

- Quickly understand story's core content and structure.
- Provide story outline foundation for script creation.
- Create project application or promotion materials.
- Provide overview for story evaluation and adaptation.

## Core Steps

1. **Deep Reading**: Deeply read story text, accurately understand characters, character relationships, and event plots in story.
2. **Information Extraction**: Extract main characters, character relationships, and key plots.
3. **Structure Organization**: Organize information according to story development logic, build outline framework.
4. **Outline Writing**: Summarize story into a fluent story outline.

## Input Requirements

- **Story Text**: Complete original story text (supports first-person or third-person narrative).
- **Recommended Text Length**: 300+ words.

## Output Format

Directly output fluent text summarizing story outline, without any titles.

## Constraints

- **Word Count Control**: Strictly control summary word count between 300-500 Chinese characters.
- **Content Accuracy**: Strictly summarize according to text original, do not create or adapt on your own.
- **Unified Person**: Use third person for summary (even if original is first person).
- **Format Requirements**: Directly output body text, without any titles.
- **Avoid Commentary**: Do not make summary or commentary overview of text content.

## Examples

See `{baseDir}/references/examples.md` directory for more detailed examples:
- `examples.md` - Contains story outline examples for different narrative perspectives (first-person, third-person) and complex character relationships.

## Detailed Documentation

See `{baseDir}/references/examples.md` for detailed guidance and cases on story outline generation.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field to be more concise and comply with imperative language specifications; added allowed-tools (Read) and model (opus) fields; optimized descriptions of functionality, use cases, core steps, input requirements, output format, requirements, etc. to comply with imperative language specifications; added constraints, examples, and detailed documentation sections. |
| 2.0.0 | 2026-01-11 | Refactored according to official specifications |
| 1.0.0 | 2026-01-10 | Initial version |
