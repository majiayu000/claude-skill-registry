---
name: text-analyzer
description: Comprehensive text analysis coordinator. Execute Python script for multi-aspect text analysis. Use when you need grammar, sentiment, readability, and SEO analysis combined.
---

# Text Analyzer (Parent Skill)

I coordinate comprehensive text analysis by delegating to specialized child skills.

## How to Use This Skill

For comprehensive text analysis, execute the coordinator script:

```bash
python /home/ywatanabe/dev/agent-patterns/.claude/skills/text-analyzer/run.py "text to analyze"
```

The script invokes all child skills and returns:
- Grammar analysis (critical issues, minor issues, style suggestions)
- Sentiment analysis (polarity, tone, emotional impact)
- Readability analysis (grade level, audience fit, complexity)
- SEO analysis (keywords, optimization score, recommendations)
- Synthesized executive summary with prioritized action items

## Child Skills I Use

1. **grammar-checker**: Grammar, spelling, punctuation analysis
2. **sentiment-analyzer**: Emotional tone and sentiment detection
3. **readability-scorer**: Readability metrics and audience appropriateness
4. **seo-optimizer**: SEO recommendations and keyword optimization

## When This Skill Activates

Activate when user requests:
- "Analyze this text/document/article/post"
- "Review this content for publication"
- "Check this writing quality"
- "Evaluate this document comprehensively"
- Any request combining multiple text analysis aspects

## How I Coordinate

For comprehensive analysis, I:
1. Determine which child skills are needed based on request
2. Invoke relevant child skills in appropriate order
3. Synthesize results into coherent report
4. Provide prioritized recommendations

## Typical Workflows

**Full Analysis** (all aspects):
1. grammar-checker → identify language issues
2. sentiment-analyzer → understand emotional tone
3. readability-scorer → assess audience fit
4. seo-optimizer → suggest improvements
5. Synthesize comprehensive report

**Quick Review** (grammar + readability):
1. grammar-checker → language correctness
2. readability-scorer → audience appropriateness
3. Provide concise feedback

**Marketing Focus** (sentiment + SEO):
1. sentiment-analyzer → emotional impact
2. seo-optimizer → search optimization
3. Marketing-focused recommendations

## Output Format

Provide structured analysis report:
- **Executive Summary**: Key findings and priority actions
- **Grammar & Language**: Issues and corrections
- **Sentiment**: Emotional tone analysis
- **Readability**: Scores and audience fit
- **SEO**: Optimization opportunities
- **Recommendations**: Prioritized action items

## Example Requests

✅ "Analyze this blog post before publishing"
✅ "Review this marketing email comprehensively"
✅ "Check this article for grammar and readability"
✅ "Evaluate this content for SEO and sentiment"
