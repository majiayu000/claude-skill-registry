---
name: aico-pm-competitor-analysis
description: |
  Research and analyze competitors with STRUCTURED output: feature comparison matrix, strengths/weaknesses analysis, and actionable recommendations.

  UNIQUE VALUE: Creates standardized competitor analysis document with feature matrix and strategic recommendations.

  Use this skill when:
  - User asks "what do competitors do?", "who are our competitors?"
  - User mentions competitor names or asks for product comparison
  - User asks for "competitor analysis", "market research", "competitive landscape"
  - Entering new market, feature area, or evaluating product direction
  - Need to understand competitive landscape before making product decisions
  - Writing PRD and need market context or differentiation strategy

  Output format: Feature comparison matrix + Strengths/Weaknesses + Actionable recommendations
---

# Competitor Analysis

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Identify competitors**: Direct and indirect
2. **Create feature matrix**: Compare capabilities
3. **Analyze each competitor**: Strengths, weaknesses, positioning
4. **Identify market gaps**: Opportunities for differentiation
5. **Develop recommendations**: Actionable strategies

## Analysis Document Template

```markdown
# Competitor Analysis: [Product Area]

## Executive Summary

[2-3 sentence overview of findings]

## Competitors Overview

| Competitor | Type     | Target Users | Key Strength |
| ---------- | -------- | ------------ | ------------ |
| [Name]     | Direct   | [Users]      | [Strength]   |
| [Name]     | Indirect | [Users]      | [Strength]   |

## Feature Comparison

| Feature     | Us    | Competitor A | Competitor B |
| ----------- | ----- | ------------ | ------------ |
| [Feature 1] | ✓/✗/- | ✓/✗/-        | ✓/✗/-        |

Legend: ✓ Has / ✗ Doesn't have / - Partial

## Detailed Analysis

### [Competitor Name]

- **Strengths**: [What they do well]
- **Weaknesses**: [Where they fall short]
- **Positioning**: [How they position themselves]

## Opportunities

### Gaps in Market

- [Gap 1]: [How we can address]

### Differentiation Strategies

- [Strategy 1]

## Recommendations

- [Actionable recommendation based on analysis]
```

## Research Sources

- Product websites and documentation
- User reviews (G2, Capterra, etc.)
- Social media and community feedback
- Direct product trials

## Key Rules

- ALWAYS include both direct and indirect competitors
- MUST create feature comparison matrix
- ALWAYS end with actionable recommendations
- Include positioning and strategy, not just features

## Common Mistakes

- ❌ Only direct competitors → ✅ Include indirect/adjacent
- ❌ Feature-only focus → ✅ Include positioning/strategy
- ❌ No recommendations → ✅ Always end with actions
