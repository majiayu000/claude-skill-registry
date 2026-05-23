---
name: seo-optimizer
description: SEO optimization with keyword analysis, readability assessment, technical validation, content quality. Use for search rankings, blog posts, content audits, or encountering keyword density, readability scores, meta tags, schema markup errors.
---

# SEO Optimizer

## Overview

Perform comprehensive SEO analysis and optimization covering keyword placement, readability metrics, technical elements, and content quality to improve search engine rankings and user experience.

## When to Use

- Optimizing blog posts or articles for search rankings
- Conducting content audits
- Improving existing content performance
- Planning new content with SEO in mind
- Analyzing competitor content strategies
- Preparing content for publication

## Core Analysis Areas

### 1. Target Keywords Analysis

- Identify primary and secondary keywords
- Check placement in title, H1, first 100 words, subheadings
- Calculate keyword density (target: 1-2%)
- Identify LSI keywords and semantic variations
- Flag keyword stuffing issues

### 2. Content Structure

- Verify heading hierarchy (H1 → H2 → H3)
- Check keyword usage in headings
- Evaluate paragraph length (target: <150 words)
- Assess overall scannability
- Review content organization

### 3. Readability Metrics

```javascript
// Readability scoring example
const readabilityMetrics = {
  fleschScore: 65,           // Target: 60-70
  gradeLevel: 8,             // Target: 7-9
  avgSentenceLength: 18,     // Target: <20 words
  passiveVoice: 5,           // Target: <10%
  transitionWords: 30        // Target: >30%
};
```

**Key Metrics:**
- Flesch Reading Ease score (60-70 ideal)
- Grade level estimation
- Average sentence length (<20 words)
- Passive voice percentage (minimize)
- Transition word usage

### 4. Technical SEO Elements

| Element | Recommendation |
|---------|----------------|
| Meta Title | 50-60 characters with primary keyword |
| Meta Description | 150-160 characters, compelling with keyword |
| URL Slug | Short, keyword-rich, hyphen-separated |
| Image Alt Text | Descriptive with natural keyword usage |
| Internal Links | Link to related content with keyword anchors |
| External Links | Quality outbound links to authoritative sources |

### 5. Content Quality Assessment

- Word count adequacy (1500+ for competitive topics)
- Content depth and topic coverage
- Unique value proposition
- E-A-T signals (Expertise, Authority, Trustworthiness)
- Content freshness (current examples, recent data)
- Clear answer to user intent

### 6. Provide Actionable Recommendations

Organize findings into prioritized action items based on impact and implementation effort.

## Priority Levels

### Critical (Fix Immediately) 🚨
- Missing or poor meta description
- No keyword in title or H1
- Broken internal links
- Keyword density too high (stuffing) or too low

### High Priority ⚠️
- Poor readability score
- Weak heading structure
- Missing alt text on images
- Content too thin for topic

### Medium Priority 📋
- Could add related keywords
- Featured snippet opportunities
- Additional internal linking
- Schema markup opportunities

## Analysis Report Structure

```markdown
# SEO Analysis Report

## Overall Score: X/100

### Quick Wins 🚀
1. [Specific action with exact change]
2. [Specific action with exact change]

## Keyword Analysis
- Primary keyword density
- Placement verification
- LSI keyword coverage

## Readability Metrics
- Flesch Reading Ease: XX/100
- Grade Level: X
- Sentence length assessment

## Technical SEO
- Meta tags analysis
- URL optimization
- Image optimization

## Content Gaps
- Missing subtopics
- Coverage recommendations
- Topic expansion opportunities

## Competitor Insights
- Top ranking pages analysis
- Word count comparison
- Unique angles they cover
- Our competitive advantage

## Implementation Checklist
- [ ] Action item 1
- [ ] Action item 2

## Estimated Impact
- **Time to Implement**: X hours
- **Expected Improvement**: [Moderate/Significant] ranking boost
- **Priority**: [High/Medium/Low]
- **Timeframe**: [Weeks until results]
```

## Best Practices

- **User experience first**: Prioritize readability and value over keyword density
- **Write for humans**: Optimize for search engines second
- **Be specific**: Provide exact changes, not vague suggestions
- **Consider intent**: Match content to search intent (informational, commercial, transactional)
- **E-A-T signals**: Include author credentials, sources, and expertise indicators
- **Featured snippets**: Format content for definition boxes, lists, tables
- **Schema markup**: Suggest structured data (FAQ, How-To, Review) where relevant

## Example Analysis Flow

1. **Identify keywords** → Extract from user input or content
2. **Check placement** → Verify in title, H1, first 100 words
3. **Calculate density** → Ensure 1-2% keyword density
4. **Assess readability** → Calculate Flesch score and sentence length
5. **Review structure** → Check heading hierarchy and paragraph length
6. **Analyze technical** → Validate meta tags, URLs, alt text
7. **Find gaps** → Identify missing topics and internal links
8. **Prioritize fixes** → Sort by impact (critical > high > medium)
9. **Generate checklist** → Create actionable implementation steps

## Output Guidelines

- Provide **specific recommendations** with exact text changes
- Show **before/after examples** for clarity
- Include **keyword variations** naturally in suggestions
- Estimate **time to implement** and **expected impact**
- Format for **easy scanning** with headings and lists
- Add **context** explaining why changes matter

## Additional Resources

See [references/analysis-framework.md](references/analysis-framework.md) for:
- Detailed analysis instructions for each area
- Technical specifications and formulas
- Competitor analysis guidelines
- E-A-T evaluation criteria

See [references/output-templates.md](references/output-templates.md) for:
- Complete SEO report template
- Implementation checklist format
- Example workflow with sample content
- Featured snippet optimization templates

## Core Philosophy

> "SEO is about creating valuable, well-optimized content that serves user intent better than competitors."

Focus on genuine value creation, not manipulation tactics. Quality content that helps users naturally attracts engagement signals that improve rankings.
