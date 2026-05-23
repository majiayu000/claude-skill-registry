---
name: story-type-analyzer
description: Analyze story genre types, extract creative elements and story features. Suitable for identifying genre positioning, extracting creativity, analyzing market audience
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
  - version: 2.2.0
    date: 2026-01-11
    changes:
      - type: improved
        content: Added references/guide.md reference, improved detailed documentation section
  - version: 2.1.0
    date: 2026-01-11
    changes:
      - type: improved
        content: Optimized description field to be more concise and comply with imperative language specifications
      - type: added
        content: Added allowed-tools (Read) and model (opus) fields
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
  - version: 1.0.0
    date: 2026-01-10
    changes:
      - type: added
        content: Initial version
---

# Genre Type and Creative Element Extraction Expert

## Functionality

Analyze story genre types, extract creative elements, identify story features and style characteristics.

## Use Cases

- Identify story's core genre and type positioning, clarify market direction.
- Extract unique creative elements of stories, enhance work attractiveness.
- Analyze story's market positioning and audience groups, guide promotion strategy.
- Provide deep reference basis for story adaptation and commercialization.

## Core Steps

1. **Genre Identification**: Analyze story's main genre types and secondary genre elements.
2. **Creative Extraction**: Identify and extract core creative elements and innovation points in stories.
3. **Feature Analysis**: Analyze story's uniqueness, innovation points, and style characteristics.
4. **Style Interpretation**: Interpret story's narrative style and artistic features, grasp work tone.
5. **Value Evaluation**: Comprehensively evaluate commercial and artistic value of genres.

## Input Requirements

- **Story Text/Outline/Summary**: Complete original story text, outline, or summary.
- **Recommended Text Length**: 500+ words.

## Output Format

```
[Genre Type Analysis]
- Dominant Genre: [Genre Type]
- Auxiliary Genres: [Genre Type 1, Genre Type 2]
- Genre Integration: [High/Medium/Low]

[Creative Element Extraction]
1. Core Creativity: [Describe the most core creative elements]
2. Innovation Point 1: [Specific description]
3. Innovation Point 2: [Specific description]

[Story Features]
- Setting Features: [Describe story setting characteristics]
- Narrative Features: [Describe narrative technique characteristics]

[Genre Value]
- Commercial Value: [Evaluate commercial potential]
- Artistic Value: [Evaluate artistic characteristics]
```

## Constraints

- Analysis results must be faithful to original story text, no subjective conjecture.
- Genre classification must be accurate, creative extraction refined.
- Value evaluation must be objective, give specific reasons.

## Examples

Please refer to `{baseDir}/references/examples.md` for detailed analysis examples.

## Detailed Documentation

See `{baseDir}/references/` directory for more documentation:
- `guide.md` - Complete analysis guide and definition explanations
- `examples.md` - More scenario examples

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field to be more concise and comply with imperative language specifications; added allowed-tools (Read) and model (opus) fields; optimized descriptions of functionality, use cases, core steps, input requirements, and output format to comply with imperative language specifications; added constraints, examples, and detailed documentation sections. |
| 2.0.0 | 2026-01-11 | Refactored according to official specifications |
| 1.0.0 | 2026-01-10 | Initial version |
