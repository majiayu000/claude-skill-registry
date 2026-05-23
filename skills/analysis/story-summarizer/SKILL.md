---
name: story-summarizer
description: Extract main plots and key points based on story text, generate complete story summary. Suitable for quickly understanding story content, script adaptation, project promotion
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

# Story Summary Generation Expert

## Functionality

Extract main plots and key points based on story text content, generate complete story summary.

## Use Cases

- Quickly understand story main content and plot development.
- Provide story summary for script adaptation or film and TV development.
- Create story introduction for project promotion materials.
- Provide story overview for subsequent in-depth analysis.

## Core Steps

1. **Careful Reading**: Carefully read story text, understand overall content.
2. **Main Plot Identification**: Identify story's main plot lines.
3. **Key Point Extraction**: Extract key points of story.
4. **Development Organization**: Organize story development process.
5. **Summary Generation**: Generate complete story summary.

## Input Requirements

- **Story Text**: Complete original story text (novels, scripts, story outlines, etc.).
- **Recommended Text Length**: 300+ words.

## Output Format

```
[Story Summary]

[Story Background]
[Describe background, environmental settings, etc. where story takes place]

[Main Plot]
[Describe main plot development of story]

[Story Development]
[Describe story development process in chronological order]

[Key Turning Points]
[Describe key turning points and important changes in story]

[Story Ending]
[Describe story's ending and final state]
```

## Constraints

- Summary should be concise and complete, usually 200-500 words.
- Strictly summarize according to story original content, do not create on your own.
- Maintain accuracy and completeness of plot.
- Include core elements of story: characters, events, conflicts, endings.

## Examples

See `{baseDir}/references/examples.md` directory for more detailed examples:
- `examples.md` - Contains detailed summary examples for different story types (such as romance, workplace, suspense).

## Detailed Documentation

See `{baseDir}/references/examples.md` for detailed guidance and cases on story summary generation.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field to be more concise and comply with imperative language specifications; added allowed-tools (Read) and model (opus) fields; optimized descriptions of functionality, use cases, core steps, input requirements, output format, requirements, etc. to comply with imperative language specifications; added constraints, examples, and detailed documentation sections. |
| 2.0.0 | 2026-01-11 | Refactored according to official specifications |
| 1.0.0 | 2026-01-10 | Initial version |
