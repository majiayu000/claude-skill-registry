---
name: story-five-elements
description: Comprehensively analyze story five elements: genre type, story summary, character biographies, character relationships, major plot points. Suitable for deep story analysis, script adaptation preparation, story development documentation
category: story-analysis
version: 2.1.0
last_updated: 2026-01-11
license: MIT
compatibility: Claude Code 1.0+
maintainer: Gong Fan
allowed-tools: []
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
        content: Added references/ structure to store detailed examples
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: Initial version
---

# Story Five Elements Analysis Expert

## Functionality

Analyze five core elements of stories: genre type and creative element extraction, story summary, character biographies, character relationships, major plot points.

## Use Cases

- Comprehensively and deeply analyze story text
- Provide complete five elements analysis for script adaptation
- Create story development documentation
- Evaluate overall quality and market potential of stories

## Five Core Elements

1. **Genre Type and Creative Element Extraction**: Analyze story genres, extract creative elements
2. **Story Summary**: Generate complete story summary
3. **Character Biographies**: Generate detailed biographies for main characters
4. **Character Relationships**: Analyze relationship networks between characters
5. **Major Plot Points**: Organize and analyze main plot points

## Core Steps

1. **Text Preprocessing**: Intelligently truncate and split long text, ensure analysis quality and efficiency
2. **Parallel Analysis**: Efficiently process text segments, call professional analysis modules
3. **Five Elements Analysis**: Simultaneously conduct professional analysis in five dimensions: genre type, story summary, character biographies, character relationships, major plot points
4. **Result Integration**: Integrate all analysis results, generate structured comprehensive analysis report
5. **Mind Map Generation**: Optionally generate visualized mind map, intuitively display five elements relationships

## Input Requirements

- Complete story text (supports long text)
- Text length: No limit (system will automatically process long text)

## Output Format

```
[Story Five Elements Analysis Report]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. Genre Type and Creative Element Extraction
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Genre types, creative elements, story features, style characteristics]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
II. Story Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Complete story summary, 300-500 words]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
III. Character Biographies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Biographies generated for each main character]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IV. Character Relationships
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Character relationship types, relationship characteristics, relationship development process]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V. Major Plot Points
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Main plot points arranged by development stage]
```

## Detailed Documentation

See `{baseDir}/references/` directory for more documentation:
- `examples.md` - Detailed analysis examples (urban emotion, ancient court intrigue, suspense mystery, etc.)
- `guide.md` - Complete five elements analysis guide and techniques

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field to be more concise and comply with imperative language specifications; changed model to opus; optimized descriptions of functionality, use cases, core steps, input requirements, and output format to comply with imperative language specifications; added constraints, examples, and detailed documentation sections. |
| 2.0.0 | 2026-01-11 | Refactored according to official specifications, added references structure |
| 1.0.0 | 2026-01-10 | Initial version |
