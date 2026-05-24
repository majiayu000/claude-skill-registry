---
name: plot-points-analyzer
description: Analyze story plot points, identify key plots and turning points. Suitable for deep analysis of plot structure, evaluating plot development effectiveness
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

# Plot Point Analysis Expert

## Functionality

Analyze plot points in stories, identify key plots and turning points, describe plot development process.

## Use Cases

- Deeply analyze story plot structure, reveal internal logic.
- Identify key turning nodes in stories, evaluate their impact on plot.
- Evaluate effectiveness and rationality of plot development.
- Provide professional suggestions for plot optimization and script adaptation.

## Core Steps

1. **Identify**: Identify all important plot points in the story.
2. **Importance Evaluation**: Analyze importance level of plot points (core/important/supporting).
3. **Type Classification**: Classify plot points by plot function (opening/development/turning/climax/conclusion).
4. **Process Description**: Describe complete process of plot point development, including prerequisites, development and results.
5. **Turning Analysis**: Analyze nature, mechanism, and emotional impact of plot turning points.

## Input Requirements

- **Story Text or Plot Outline**: Complete original story text or detailed plot outline.
- **Specific Analysis Focus** (optional): Specify plot points or aspects needing focused analysis.

## Output Format

```
[Plot Point X]: Plot Point Name

1. Plot Point Type
   - Type: [Opening/Development/Turning/Climax/Conclusion]
   - Function: Specifically describe the function of this plot point

2. Plot Point Importance
   - Importance Level: [Core/Important/Supporting]
   - Impact Scope: Describe impact on overall story

3. Plot Development Process
   - Prerequisites: What conditions led to this plot point
   - Development Process: How the plot developed
   - Result Orientation: What results were produced

4. Turning Point Analysis
   - Turning Nature: [Positive/Negative/Neutral]
   - Turning Mechanism: How the turning was achieved
   - Emotional Impact: Impact on audience emotions

5. Plot's Impact on Story
   - Impact on character development
   - Driving role for main plot
   - Contribution to theme expression
```

## Constraints

- Analysis results must be faithful to original story text, no subjective conjecture.
- Ensure accurate plot point classification, clear function description.
- Suggestions should be actionable and guide plot optimization.

## Examples

See `{baseDir}/references/examples.md` directory for more detailed examples:
- `examples.md` - Contains key plot point analysis examples for different story types (such as urban romance, ancient fantasy, suspense mystery).

## Detailed Documentation

See `{baseDir}/references/examples.md` for detailed guidance and cases on plot point analysis.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01-11 | Optimized description field to be more concise and comply with imperative language specifications; added allowed-tools (Read) and model (opus) fields; optimized descriptions of functionality, use cases, core steps, input requirements, and output format to comply with imperative language specifications; added constraints, examples, and detailed documentation sections. |
| 2.0.0 | 2026-01-11 | Refactored according to official specifications |
| 1.0.0 | 2026-01-10 | Initial version |
