---
name: story-outline-evaluator
description: Professionally evaluate story outlines, judge and score from dimensions of market potential, innovation attributes, and content highlights. Suitable for story outline quality assessment, IP adaptation potential judgment, project approval decision
category: evaluation
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

# Story Outline Evaluation Expert

## Functionality

Deeply evaluate story outlines, judge and score from multiple dimensions including market potential, innovation attributes, and content highlights.

## Use Cases

- Evaluate story outline quality.
- Judge IP adaptation potential.
- Serve as project approval decision reference.
- Guide story optimization direction.

## Evaluation Dimensions

### 1. Market Potential
Combine with market, judge story outline's market performance potential.

- **Audience Fit**: Judge whether story fits target audience.
- **Discussion Heat**: Judge whether story content can resonate with the public.
- **Scarcity**: Analyze whether story has sufficient uniqueness.
- **Performance Data**: Analyze story's market prospects.

### 2. Innovation Attributes
Judge whether story outline has innovation.

- **Core Selection**: Judge whether story's core selection is fresh and unique.
- **Story Concept**: Judge whether story's concept is outstanding and clear.
- **Story Design**: Analyze from perspectives of theme, characters, worldview, plot, etc.

### 3. Content Highlights
From story content level, judge whether it has strong watchability.

- **Theme Concept**: Analyze whether theme concept is clear and definite.
- **Story Situation**: Judge whether story situation has tension and drama.
- **Character Settings**: Judge whether main character settings are novel and distinctive.
- **Character Relationships**: Judge whether main character relationships are brilliant and clear.
- **Plot Devices**: Judge whether plot devices have dramatic tension.

## Scoring Standards

- **8.5 and above**: Excellent, has extremely strong competitiveness and adaptation foundation.
- **8.0-8.4**: Good, has strong competitiveness and adaptation foundation.
- **7.5-7.9**: Qualified, average competitiveness.
- **7.4 and below**: Poor, almost no competitiveness.

## Core Steps

1. **Deep Reading**: Deeply read story outline, form independent understanding.
2. **Dimension Analysis**: Analyze each dimension according to evaluation framework.
3. **Scoring Judgment**: Score each dimension and form overall evaluation.
4. **Provide Recommendations**: According to overall evaluation, provide recommendations on whether to continue development.

## Input Requirements

- Complete story outline.
- Story's genre and type (such as: urban emotion, ancient fantasy, etc.).

## Output Format

```
[Story Outline Evaluation Report]

[Market Potential]:
- Audience Fit: [Analysis and Evaluation] Score: [X.X]
- Discussion Heat: [Analysis and Evaluation] Score: [X.X]
- Scarcity: [Analysis and Evaluation] Score: [X.X]
- Performance Data: [Analysis and Evaluation] Score: [X.X]

[Innovation Attributes]:
- Core Selection: [Summary Analysis] Score: [X.X]
- Story Concept: [Summary Analysis] Score: [X.X]
- Story Design: [Summary Analysis] Score: [X.X]

[Content Highlights]:
- Theme Concept: [Summary Analysis] Score: [X.X]
- Story Situation: [Brief description and analysis] Score: [X.X]
- Character Settings: [Summary Analysis] Score: [X.X]
- Character Relationships: [Summary Analysis] Score: [X.X]
- Plot Devices: [Analysis of performance] Score: [X.X]

[Overall Evaluation]:
[Combine all dimensions for overall analysis and evaluation]
Total Score: [X.X]

[Follow-up Recommendations]: [Proceed recommendations or modification recommendations]
```

## Constraints

- Evaluation must be based on provided story outline content, do not create or add information on your own.
- Scoring should be objective and fair, accompanied by detailed analysis.
- Recommendations should be specific and feasible, helping story outline improvement.

## Examples

Please refer to `{baseDir}/references/examples.md` for detailed evaluation examples. This file contains complete evaluation reports and analysis instructions for various story types (such as urban romance, sci-fi, history, etc.).

## Detailed Documentation

See `{baseDir}/references/guide.md` for complete guide to story outline evaluation, including evaluation framework, scoring standards, evaluation process, and precautions.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field, added allowed-tools (Read) and model (opus) fields, adjusted main content language style, added constraints, and directed to references/examples.md |
| 2.0.0 | 2026-01-11 | Refactored according to official specifications |
| 1.0.0 | 2026-01-10 | Initial version |
