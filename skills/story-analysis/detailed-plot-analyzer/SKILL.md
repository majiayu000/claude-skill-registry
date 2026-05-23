---
name: detailed-plot-analyzer
description: Based on major plot points, deeply analyze and generate detailed plot point descriptions and plot development explanations. Suitable for refining story outlines, guiding script writing, analyzing plot internal logic
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
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: Initial version
---

# Detailed Plot Point Analysis Expert

## Functionality

Based on major plot points, deeply analyze and expand, generating detailed plot point descriptions and plot development explanations.

## Use Cases

- Refine and expand story outlines.
- Provide detailed plot guidance for script writing.
- Analyze internal logic of plot development.
- Discover problems and optimization opportunities in plot design.

## Core Steps

1. **Understand Core Elements**: Carefully analyze major plot point content, understand core elements of each plot point.
2. **Deep Expansion**: Deeply analyze each plot point, generating detailed plot descriptions.
3. **Logic Analysis**: Analyze logical relationships and development脉络 between plot points.
4. **Provide Suggestions**: Provide detailed explanations and optimization suggestions for plot development.

## Input Requirements

- Extracted list of major plot points
- Original story text (optional, for reference)
- Specific analysis requirements (optional)

## Output Format

```
[Detailed Plot Point Analysis]

[Plot Point 1]: Major plot description
- Core Elements: Key element analysis
- Character Behavior: Character behavior analysis
- Plot Development: Plot development explanation
- Logical Relationship: Relationship with other plot points

[Plot Point 2]: Major plot description
- Core Elements: Key element analysis
- Character Behavior: Character behavior analysis
- Plot Development: Plot development explanation
- Logical Relationship: Relationship with other plot points
...

[Plot Development Summary]
Summary and suggestions for overall plot development
```

## Constraints

- Each detailed plot point description controlled between 200-300 words.
- Strictly analyze according to major plot point content, do not create on your own.
- Maintain logic and coherence of plot development.
- Avoid repetitive and redundant descriptions.

## Examples

Please refer to `{baseDir}/references/examples.md` for more detailed examples.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field, added allowed-tools and model fields, adjusted main content language style, and directed to references/examples.md |
| 2.0.0 | 2026-01-11 | Refactored according to official specifications |
| 1.0.0 | 2026-01-10 | Initial version |
