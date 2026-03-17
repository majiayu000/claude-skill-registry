---
name: serp-analysis
description: SERP analysis techniques for intent classification, feature identification, and competitive intelligence. Use when analyzing search results for content strategy.
---

# SERP Analysis

## When to Use

- Analyzing search results for a keyword
- Classifying search intent
- Identifying SERP feature opportunities
- Competitive intelligence gathering

## Intent Classification

### Intent Types

| Intent | SERP Signals | User Goal | Content Format |
|--------|--------------|-----------|----------------|
| **Informational** | Wikipedia, knowledge panels, "what is" queries | Learn something | Guide, tutorial, explainer |
| **Commercial** | Reviews, comparisons, "best X" queries | Compare options | Comparison, listicle, review |
| **Transactional** | Product pages, shopping results, "buy X" | Purchase something | Product page, pricing |
| **Navigational** | Brand homepage, login pages | Find specific site | Homepage, login page |

### Classification Process

1. **Search the keyword** using WebSearch
2. **Analyze result types**:
   - All informational = Informational intent
   - Mix of reviews/comparisons = Commercial intent
   - Product pages dominant = Transactional intent
   - Single brand dominant = Navigational intent
3. **Check for mixed intent** (common for broad keywords)
4. **Note confidence level** (% of results supporting classification)

## SERP Features

### Feature Identification

| Feature | How to Identify | Optimization Strategy |
|---------|-----------------|----------------------|
| **Featured Snippet** | Box at top with answer | Direct answer in first 100 words |
| **People Also Ask** | Expandable question boxes | FAQ section, answer common questions |
| **Image Pack** | Row of images | High-quality images with alt text |
| **Video Results** | YouTube thumbnails | Create video content |
| **Local Pack** | Map with business listings | GMB optimization, location pages |
| **Knowledge Panel** | Right sidebar info box | Schema markup, Wikipedia presence |
| **Sitelinks** | Sub-links under main result | Clear site structure, internal linking |

### Featured Snippet Types

| Type | Format | How to Optimize |
|------|--------|-----------------|
| Paragraph | Text block | 40-60 word direct answer |
| List | Numbered/bulleted list | Use ordered/unordered lists |
| Table | Data table | Use HTML tables |
| Video | YouTube embed | Create relevant video content |

## Competitive Analysis

### Competitor Data to Collect

For each top 10 result, note:

1. **Domain authority** (relative, not exact)
2. **Content format** (guide, listicle, comparison, etc.)
3. **Word count** (approximate)
4. **Heading structure** (H2 topics covered)
5. **Unique angle** (what makes them different)
6. **Content gaps** (what they miss)

### Competitor Matrix Template

| Rank | Domain | Format | Words | Unique Angle | Gap |
|------|--------|--------|-------|--------------|-----|
| 1 | {domain} | {format} | {count} | {angle} | {gap} |
| 2 | {domain} | {format} | {count} | {angle} | {gap} |
| ... | | | | | |

## Output Format

```markdown
## SERP Analysis: {keyword}

### Search Intent
- **Primary Intent**: {Informational | Commercial | Transactional | Navigational}
- **Confidence**: {percentage}%
- **Secondary Intent**: {if mixed}

### SERP Features Present
- [ ] Featured Snippet ({type})
- [ ] People Also Ask
- [ ] Image Pack
- [ ] Video Results
- [ ] Local Pack
- [ ] Knowledge Panel
- [ ] Sitelinks

### Competitor Analysis
| Rank | Domain | Format | Words | Unique Angle |
|------|--------|--------|-------|--------------|
| 1 | {domain} | {format} | {count} | {angle} |
...

### Content Gaps Identified
1. {gap} - {which competitors miss this}
2. {gap} - {which competitors miss this}

### Recommendations
1. **Content Format**: {recommended format based on SERP}
2. **Word Count**: {recommended based on competitors + 20%}
3. **Featured Snippet**: {opportunity and how to capture}
4. **Differentiator**: {unique angle to stand out}
```
