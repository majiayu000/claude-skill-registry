---
name: plot-keypoints
description: Organize story main line, extract and arrange major plot points by development stage. Suitable for quickly grasping story structure, creating outlines, and script adaptation structure organization
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
      - type: changed
        content: Changed model to opus
      - type: improved
        content: Optimized descriptions of functionality, use cases, core steps, input requirements, and output format to comply with imperative language specifications
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
      - type: added
        content: Added allowed-tools (Read) and model fields
      - type: added
        content: Added references/ structure to store detailed examples
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: Initial version
---

# Major Plot Point Analysis Expert

## Functionality

Organize story main line, extract and arrange major plot points by story development stage.

## Use Cases

- Quickly grasp overall story structure and plot development.
- Provide basic framework for detailed plot analysis.
- Create story outlines or summaries.
- Organize structure before script adaptation.

## Core Steps

1. **Reading Comprehension**: Fully read and understand story text, grasp overall structure and theme.
2. **脉络 Organization**: Organize story accurate and complete脉络, identify key turning points.
3. **Plot Point Extraction**: According to plot point definitions, accurately summarize major plot points, ensuring completeness and accuracy.
4. **Stage Division**: Divide and arrange by story development stage (such as three-act structure).
5. **Structured Output**: Output according to specified format, ensuring clarity and readability.

## Input Requirements

- Complete story text (novels, scripts, story outlines, etc.)
- Recommended text length: 1000+ words for more complete analysis

## Output Format

```
[Stage One: Plot Theme]:
- Sub-plot point 1
- Sub-plot point 2
- Sub-plot point 3

[Stage Two: Plot Theme]:
- Sub-plot point 1
- Sub-plot point 2
- Sub-plot point 3

[Stage Three: Plot Theme]:
...
```

## Constraints

- Each plot point description does not exceed 150 words.
- Strictly summarize according to story text original meaning, do not create or adapt on your own.
- Ensure summary of major plot points is complete, accurate, and detailed.
- Do not use Arabic numerals to number plot points.

## Examples

Please refer to `{baseDir}/references/examples.md` for detailed examples. This file contains complete input and output examples and analysis instructions for various story structures (such as three-act, five-act, vertical short drama, multi-line narrative, etc.), as well as plot point extraction techniques.

## Detailed Documentation

See `{baseDir}/references/` directory for more documentation:
- `examples.md` - Detailed analysis examples (different structure types like three-act, five-act, multi-line narrative, etc.)
- `guide.md` - Complete analysis guide and best practices

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field, added allowed-tools and model fields, adjusted main content language style, deleted best practices, and directed to references/examples.md |
| 2.0.0 | 2026-01-11 | Refactored according to official specifications, added references structure |
| 1.0.0 | 2026-01-10 | Initial version |
