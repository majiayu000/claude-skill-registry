---
name: optimizing-blog-posts-for-seo
description: Analyzes and enhances existing blog posts for better search rankings. Use when the user asks about SEO optimization, blog post improvements, content refreshing, ranking improvements, or competitor content gaps.
---

# SEO Blog Post Optimizer

## When to use this skill

- User wants to improve existing blog posts
- User asks about SEO content optimization
- User mentions ranking improvements
- User needs competitor content analysis
- User wants to refresh outdated content

## Workflow

- [ ] Analyze current content
- [ ] Research top-ranking competitors
- [ ] Identify content gaps
- [ ] Optimize on-page elements
- [ ] Enhance content structure
- [ ] Add supporting elements
- [ ] Validate improvements

## Instructions

### Step 1: Current Content Audit

Evaluate the existing post:

| Element          | Check                         | Notes |
| ---------------- | ----------------------------- | ----- |
| Word count       | Current vs. competitor avg    |       |
| Headings         | H1, H2, H3 structure          |       |
| Target keyword   | Primary and secondary         |       |
| Keyword density  | 1-2% optimal                  |       |
| Meta title       | 50-60 chars, keyword included |       |
| Meta description | 150-160 chars, compelling     |       |
| URL slug         | Short, keyword-rich           |       |
| Images           | Alt text, optimization        |       |
| Internal links   | Relevant connections          |       |
| External links   | Authoritative sources         |       |
| Publish date     | Freshness signal              |       |

### Step 2: Competitor Analysis

Analyze top 5 ranking pages for target keyword:

```markdown
## Competitor Analysis: "[Target Keyword]"

### Top Ranking Pages

| Rank | URL   | Word Count | Headings | Key Sections     |
| ---- | ----- | ---------- | -------- | ---------------- |
| 1    | [URL] | [#]        | [#]      | [Topics covered] |
| 2    | [URL] | [#]        | [#]      | [Topics covered] |
| 3    | [URL] | [#]        | [#]      | [Topics covered] |

### Common Elements (Present in 3+ competitors)

- [ ] [Section/topic 1]
- [ ] [Section/topic 2]
- [ ] [FAQ section]
- [ ] [Data/statistics]
- [ ] [Visual content]

### Differentiators (Unique angles to explore)

- [Gap 1]
- [Gap 2]
```

### Step 3: Content Gap Analysis

Identify missing elements:

**Structural gaps:**

- Missing H2/H3 sections competitors cover
- No FAQ section when SERP shows "People Also Ask"
- Missing table of contents for long content
- No conclusion or summary section

**Topic gaps:**

- Subtopics competitors address
- Questions not answered
- Use cases not covered
- Examples not provided

**Technical gaps:**

- Missing schema markup
- No featured snippet optimization
- Poor mobile formatting
- Slow-loading elements

### Step 4: On-Page Optimization

#### Title Tag Optimization

```
Format: [Primary Keyword] - [Benefit/Modifier] | [Brand]
Example: "SEO Blog Writing: 15 Tips to Rank Higher in 2026 | ContentPro"
```

**Title formulas:**

- How to [Keyword]: [Number] [Adjective] Ways
- [Keyword]: The Complete Guide for [Year]
- [Number] [Keyword] Tips That [Benefit]
- [Keyword] vs [Alternative]: Which Is Better?

#### Meta Description Optimization

```
Format: [Hook with keyword] + [Value proposition] + [CTA]
Example: "Learn proven SEO blog writing techniques that boost rankings. Discover 15 actionable tips used by top content marketers. Start ranking today."
```

#### URL Optimization

- Keep under 60 characters
- Include primary keyword
- Remove stop words (a, the, and, or)
- Use hyphens, not underscores

### Step 5: Content Structure Enhancement

#### Heading Hierarchy

```markdown
# H1: Main Title (1 only, contains primary keyword)

## H2: Major Section (contains secondary keywords)

### H3: Subsection (supports H2 topic)

#### H4: Detail point (rarely needed)
```

#### Recommended Structure

1. **Hook intro** (50-100 words) - Problem + promise
2. **Quick answer** - Featured snippet target
3. **Table of contents** - For posts 1,500+ words
4. **Main sections** - Comprehensive coverage
5. **FAQ section** - "People Also Ask" answers
6. **Conclusion** - Summary + CTA

#### Featured Snippet Optimization

| Snippet Type | Format                              | Target                     |
| ------------ | ----------------------------------- | -------------------------- |
| Paragraph    | 40-60 word answer after H2 question | Definition queries         |
| List         | Numbered/bulleted under H2          | "How to" queries           |
| Table        | Comparison data                     | "vs" or comparison queries |

### Step 6: Content Enrichment

#### Add Missing Elements

**Statistics and data:**

- Find recent statistics (within 2 years)
- Link to primary sources
- Format as callout boxes or tables

**Visual content:**

- Add 1 image per 300-500 words
- Include infographics for data
- Add screenshots for tutorials
- Consider embedded video

**Examples and case studies:**

- Real-world applications
- Before/after comparisons
- Step-by-step walkthroughs

**Expert quotes:**

- Industry authority opinions
- Customer testimonials
- Research citations

#### Internal Linking Strategy

| Link Type         | Purpose                | Anchor Text               |
| ----------------- | ---------------------- | ------------------------- |
| Pillar to cluster | Authority distribution | Descriptive, keyword-rich |
| Cluster to pillar | Support main topic     | Exact or partial match    |
| Related posts     | User journey           | Natural, contextual       |
| CTA links         | Conversion             | Action-oriented           |

Target 3-5 internal links per 1,000 words.

#### External Linking

- Link to authoritative sources (.edu, .gov, industry leaders)
- Open in new tab
- 2-5 external links per post
- Avoid linking to competitors

### Step 7: Technical SEO Checks

```markdown
## Technical SEO Checklist

### Schema Markup

- [ ] Article schema implemented
- [ ] FAQ schema (if FAQ section exists)
- [ ] HowTo schema (if tutorial)
- [ ] Breadcrumb schema

### Page Speed

- [ ] Images compressed (WebP format)
- [ ] Lazy loading enabled
- [ ] Core Web Vitals passing

### Mobile Optimization

- [ ] Responsive layout
- [ ] Tap targets sized correctly
- [ ] Text readable without zoom
- [ ] No horizontal scrolling

### Indexing

- [ ] Page is indexable (no noindex)
- [ ] Canonical URL correct
- [ ] XML sitemap includes page
- [ ] No orphan page (internal links exist)
```

### Step 8: Content Freshness

**Update signals:**

- Change publish date to current date
- Add "Updated: [Date]" notice
- Update statistics with recent data
- Add new sections for current trends
- Replace outdated screenshots/examples

**Historical optimization:**

- Keep original publish date visible
- Add "Originally published: [Date]"
- Note major updates in content

## Output Format

```markdown
# SEO Optimization Report: [Post Title]

## Current Performance

- **URL:** [URL]
- **Target keyword:** [Keyword]
- **Current word count:** [#]
- **Publish date:** [Date]

---

## Competitor Benchmark

| Metric         | Your Post | Competitor Avg | Gap    |
| -------------- | --------- | -------------- | ------ |
| Word count     | [#]       | [#]            | [+/-#] |
| Headings       | [#]       | [#]            | [+/-#] |
| Images         | [#]       | [#]            | [+/-#] |
| Internal links | [#]       | [#]            | [+/-#] |

---

## Recommended Improvements

### High Priority

1. [Action item with specific guidance]
2. [Action item with specific guidance]

### Medium Priority

1. [Action item]
2. [Action item]

### Low Priority

1. [Action item]

---

## Content Additions

### New Sections to Add

- **[H2 heading]**: [Brief description of what to cover]
- **[H2 heading]**: [Brief description]

### FAQ Section

**Q: [Question from PAA]**
A: [40-60 word answer]

**Q: [Question]**
A: [Answer]

---

## On-Page Optimizations

**Recommended title tag:**
[New title - 60 chars max]

**Recommended meta description:**
[New description - 160 chars max]

**Internal links to add:**

- [Anchor text] → [Target URL]
- [Anchor text] → [Target URL]

---

## Technical Fixes

- [ ] [Fix needed]
- [ ] [Fix needed]

---

## Expected Impact

[Brief statement on potential ranking improvement]
```

## Validation

Before completing:

- [ ] All competitor pages analyzed
- [ ] Content gaps identified
- [ ] On-page elements optimized
- [ ] Structure improvements recommended
- [ ] Internal linking strategy included
- [ ] Technical SEO checked
- [ ] Actionable recommendations provided

## Error Handling

- **No target keyword provided**: Ask user to specify primary keyword.
- **Post not found**: Request URL or content to analyze.
- **No competitors ranking**: Broaden keyword scope or check search volume.
- **Content too thin**: Recommend expanding or combining with related posts.

## Resources

- [Google Search Console](https://search.google.com/search-console) - Performance data
- [Ahrefs](https://ahrefs.com/) - Competitor analysis
- [Semrush](https://www.semrush.com/) - Keyword research
- [Schema.org](https://schema.org/) - Structured data reference
- [PageSpeed Insights](https://pagespeed.web.dev/) - Performance testing
