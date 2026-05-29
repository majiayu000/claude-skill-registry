---
name: novel-evaluator
description: Rigorously and meticulously evaluate and score story text, analyzing quality from market potential, innovation attributes, and content highlights dimensions. Suitable for novel initial screening, multi-dimensional evaluation scoring
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
  - version: 2.2.0
    date: 2026-01-11
    changes:
      - type: improved
        content: Added references/guide.md citation, improved detailed documentation section
  - version: 2.1.0
    date: 2026-01-11
    changes:
      - type: improved
        content: Optimized description field to be more concise and comply with imperative language standards
      - type: added
        content: Added allowed-tools (Read) and model (opus) fields
      - type: improved
        content: Optimized descriptions for functionality, usage scenarios, evaluation dimensions, scoring standards, and core steps to comply with imperative language standards
      - type: added
        content: Added constraints and examples sections
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

# Senior Story Evaluation Expert (Novel Edition)

## Functionality

Conduct rigorous and meticulous evaluation and scoring of story text, analyzing story quality from multiple dimensions including market potential, innovation attributes, and content highlights.

## Usage Scenarios

- Conduct novel initial screening to quickly determine work value
- Conduct multi-dimensional evaluation scoring of story text
- Provide judgment basis for IP adaptation potential
- Guide story creation and optimization directions

## Evaluation Dimensions

### 1. Market Potential
Judge story's performance potential in the market.

- **Audience Fit**: Judge whether story aligns with target audience
- **Discussion Heat**: Judge whether story content can generate significant discussion热度
- **Scarcity**: Analyze whether story has sufficient uniqueness
- **Performance Data**: Analyze story's market prospects

### 2. Innovation Attributes
Judge whether story possesses innovation.

- **Core Selection**: Judge whether story's core selection is fresh and unique
- **Story Concept**: Judge whether story's concept is prominent and distinctive
- **Story Design**: Analyze from perspectives of theme, characters, worldview, and plot whether story design has originality

### 3. Content Highlights
Judge from story content level whether it possesses strong watchability.

- **Theme Concept**: Analyze whether theme concept is clear and definite
- **Story Situation**: Judge whether story situation has tension and dramatic quality
- **Character Design**: Judge whether character design is novel and distinctive
- **Character Relationships**: Judge whether character relationships are outstanding and distinctive
- **Plot Segments**: Judge whether plot segments have dramatic tension

## Scoring Standards

- **8.5 and above**: Excellent, possessing extremely strong competitiveness and adaptation foundation
- **8.0-8.4**: Good, possessing strong competitiveness and adaptation foundation
- **7.5-7.9**: Qualified, average competitiveness
- **7.4 and below**: Poor, almost no competitiveness

## Core Steps

1. **Deep Reading**: Deep read story text to form independent understanding
2. **Dimension Scoring**: Conduct rigorous and meticulous analysis and scoring of story according to evaluation dimensions
3. **Overall Evaluation**: Form overall evaluation and score, provide recommendation on whether to continue development

## Input Requirements

- Complete story text or story outline
- Story's genre and type (e.g., urban romance, historical fantasy, etc.)

## Output Format

```
[Market Potential]:
- Audience Fit: [Analysis and evaluation] Score: [score]
- Discussion Heat: [Analysis and evaluation] Score: [score]
- Scarcity: [Analysis and evaluation] Score: [score]
- Performance Data: [Analysis and evaluation] Score: [score]

[Innovation Attributes]:
- Core Selection: [Comprehensive analysis] Score: [score]
- Story Concept: [Comprehensive analysis] Score: [score]
- Story Design: [Comprehensive analysis] Score: [score]

[Content Highlights]:
- Theme Concept: [Analysis] Score: [score]
- Story Situation: [Analysis] Score: [score]
- Character Design: [Analysis] Score: [score]
- Character Relationships: [Analysis] Score: [score]
- Plot Segments: [Analysis] Score: [score]

[Overall Evaluation]: [Analysis and evaluation] Total Score: [score]
[Follow-up Recommendations]: [Development recommendations]
```

## Constraints

- Evaluation must be based on provided story text content; do not independently create or add information
- Scoring should be objective and fair, accompanied by detailed analysis
- Recommendations should be specific and feasible, helpful for story improvement

## Examples

See `{baseDir}/references/examples.md` for detailed evaluation examples. This file contains complete evaluation reports and analysis explanations for various story types (urban counterattack, sweet romance, suspense mystery, etc.).

## Detailed Documentation

See `{baseDir}/references/` directory for more documentation:
- `guide.md` - Complete evaluation guide and framework explanation
- `examples.md` - More scenario examples

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field; added allowed-tools (Read) and model (opus) fields; optimized descriptions for functionality, usage scenarios, evaluation dimensions, scoring standards, and core steps; added constraints and examples sections |
| 2.0.0 | 2026-01-11 | Restructured according to official specifications |
| 1.0.0 | 2026-01-10 | Initial version |
