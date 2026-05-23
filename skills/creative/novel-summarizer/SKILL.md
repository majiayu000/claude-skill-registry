---
name: novel-summarizer
description: Read and comprehend novel text, summarize into fluent story outline. Suitable for novel initial screening, generating 500-800 word story outlines
category: novel-screening
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
        content: Optimized description field to be more concise and comply with imperative language standards
      - type: added
        content: Added allowed-tools (Read) and model (opus) fields
      - type: improved
        content: Optimized descriptions for functionality, usage scenarios, core capabilities, workflow, constraints, and output format to comply with imperative language standards
      - type: added
        content: Added examples and detailed documentation sections
  - version: 2.0.0
    date: 2026-01-11
    changes:
      - type: breaking
        content: Restructured according to Agent Skills official specifications
      - type: improved
        content: Optimized description, used imperative language, streamlined main content
      - type: added
        content: Added license and compatibility optional fields
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: Initial version
---

# Story Outline Generation Expert (Novel Edition)

## Functionality

Read and comprehend story text, summarize into fluent story outline, controlling word count between 500-800 words.

## Usage Scenarios

- Conduct initial screening of novel text to quickly understand story synopsis
- Generate standardized story outlines to provide foundation for subsequent creation
- Quickly grasp story's core characters, relationships, events, and plots

## Core Capabilities

- **Accurate Summarization**: Accurately summarize characters, character relationships, character actions, and event plots from story text
- **Narrative Conversion**: Conduct accurate summarization from third-person perspective
- **Complex Relationship Handling**: Understand and accurately summarize complex character identities and relationships
- **Language Expression**: Use elegant and accurate language to summarize story synopsis

## Workflow

1. **Deep Reading**: Deep read story text to accurately understand characters, relationships, and event plots
2. **Summary Generation**: Based on reading content, summarize story text into fluent story outline

## Constraints

- **Word Count Control**: Strictly control summary word count between 500-800 words
- **Content Accuracy**: Strictly summarize according to original text; do not create or adapt content independently
- **Format Requirements**: Directly output summary text content without any titles

## Output Format

Directly output fluent text summary of story outline.

## Examples

See `{baseDir}/references/examples.md` for more detailed examples:
- `examples.md` - Detailed summarization examples (different types such as urban romance, historical romance, rebirth revenge, etc.)

## Detailed Documentation

See `{baseDir}/references/examples.md` for detailed guidance and cases on novel summarization.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field; added allowed-tools (Read) and model (opus) fields; optimized descriptions for functionality, usage scenarios, core capabilities, workflow, constraints, and output format; added examples and detailed documentation sections |
| 2.0.0 | 2026-01-11 | Restructured according to official specifications |
| 1.0.0 | 2026-01-10 | Initial version |
