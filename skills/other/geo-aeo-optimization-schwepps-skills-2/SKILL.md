---
name: geo-aeo-optimization
description: Optimize content for AI search engines (ChatGPT, Perplexity, Claude, Gemini) and featured snippets. Covers Generative Engine Optimization (GEO), Answer Engine Optimization (AEO), E-E-A-T signals, and content structuring for maximum AI citation probability. Use when optimizing content for AI visibility or auditing AI search readiness.
license: MIT
metadata:
  author: Schwepps
  version: "1.0.0"
  category: marketing
  tags: geo, aeo, ai-search, chatgpt, perplexity, featured-snippets
---

# GEO & AEO Optimization Framework

Professional methodology for visibility in AI-powered search engines and generative AI responses.

## Understanding GEO vs AEO vs SEO

```
SEO  → Rank in traditional search results (blue links)
AEO  → Appear in featured snippets, AI Overviews, voice answers
GEO  → Get cited in generative AI responses (ChatGPT, Claude, Perplexity)
```

**2025 Reality:**
- 58% of queries are conversational
- AI Overviews appear in ~47% of Google searches
- Traditional CTR dropped 34.5% for top results due to AI answers
- These strategies are complementary, not competing

## When to Use This Skill

- Optimizing content for AI search engines
- Improving featured snippet capture rate
- Auditing AI citation readiness
- Restructuring content for AI extractability
- Implementing E-E-A-T signals
- Preparing for voice search

## The Triple-Threat Framework

### 1. E-E-A-T Foundation (Required for All)

AI systems prioritize trusted, authoritative sources:

```
Experience   → First-hand knowledge, case studies, original research
Expertise    → Credentials, depth of knowledge, technical accuracy
Authority    → Citations, backlinks, mentions, brand recognition
Trustworthiness → Accuracy, transparency, clear sourcing
```

**Implementation Checklist:**
```
□ Author bio with credentials on every article
□ Link to authoritative sources
□ Include original data/research
□ Show methodology and sources
□ Update content regularly with visible dates
□ Display contact information
□ Include editorial guidelines
```

### 2. AEO: Featured Snippets & AI Overviews

**Lead with the Answer:**
- First 40-60 words should directly answer the query
- Use question-format H2 headers
- Provide concise, extractable definitions

**Content Structure for AEO:**
```markdown
## What is [Topic]?

[Direct answer in 1-2 sentences that can be extracted as a snippet]

[Supporting details and context follow]
```

**Snippet-Optimized Formats:**
| Query Type | Best Format |
|------------|-------------|
| "What is X?" | Definition paragraph (40-60 words) |
| "How to X" | Numbered steps (5-8 steps) |
| "Best X" | Bulleted list with brief descriptions |
| "X vs Y" | Comparison table |
| "Why X?" | Direct answer + explanation |

### 3. GEO: AI Citation Optimization

**The CRASP Framework:**
```
C - Clarity    → Unambiguous statements AI can quote
R - Relevance  → Match conversational query intent
A - Authority  → Cited sources, expert credentials
S - Structure  → Scannable, extractable format
P - Precision  → Specific facts, numbers, dates
```

**High-Citation Content Elements:**
1. **TL;DR blocks** at the top
2. **Statistics with sources** ("According to [Source], X increased by Y%")
3. **Expert quotes with attribution**
4. **Definition lists** for key terms
5. **Comparison tables** with clear data
6. **FAQ sections** with complete answers

## Content Structure Template

```markdown
# [H1: Primary Question or Topic]

**TL;DR:** [2-3 sentence summary with key facts]

## What is [Topic]? {#definition}

[Direct definition in 40-60 words - optimized for extraction]

[Expanded explanation with context]

## How [Topic] Works {#how-it-works}

[Step-by-step explanation]

1. **Step One**: [Description]
2. **Step Two**: [Description]
3. **Step Three**: [Description]

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| [Stat 1] | [Value] | [Source, Year] |
| [Stat 2] | [Value] | [Source, Year] |

## [Topic] vs [Alternative]

| Factor | [Topic] | [Alternative] |
|--------|---------|---------------|
| [Factor 1] | [Value] | [Value] |
| [Factor 2] | [Value] | [Value] |

## Frequently Asked Questions

### [Question 1]?

[Complete, standalone answer - 50-100 words]

### [Question 2]?

[Complete, standalone answer - 50-100 words]

## Expert Insights

> "[Quotable statement with specific insight]"
> — [Expert Name], [Title], [Organization]

---
*Last updated: [Date] | Author: [Name], [Credentials]*
```

## Fact-Density Checklist

```
Extractability:
□ TL;DR or summary present at top
□ Paragraphs <120 words each
□ Clear topic sentences (first sentence = main point)
□ Bullet lists for features/benefits
□ Tables for comparisons
□ FAQ section with schema

Fact-Density:
□ Statistics with sources cited
□ Specific numbers and dates
□ Verifiable data points
□ Expert quotes with attribution
□ Original research/data
□ Named entities (people, companies, places)

Structure for AI:
□ Question-based H2 headers
□ Direct answers in first 40-60 words
□ Logical information hierarchy
□ Schema markup (FAQPage, HowTo, Article)
```

## AI Crawler Configuration

**robots.txt for AI Search Visibility:**
```
# ALLOW search/chat features
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

# OPTIONAL: Block training (keeps search)
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /
```

**Critical:** Ensure server-side rendering. AI crawlers often don't execute JavaScript well.

## Schema Markup for AI

**Priority Schema Types:**
1. **FAQPage** - Highest AI citation impact
2. **HowTo** - Step-by-step visibility
3. **Article + Author** - E-E-A-T signals
4. **Organization** - Brand authority

**FAQPage Example:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is [topic]?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "[Complete answer that can be extracted]"
    }
  }]
}
```

## Output Format

```markdown
# GEO/AEO Audit Report

**Page:** [URL]
**Date:** [Date]
**Overall Score:** X/100

## Executive Summary
[2-3 sentence AI search readiness assessment]

## Scores by Category

| Category | Score | Status |
|----------|-------|--------|
| E-E-A-T Signals | X/25 | [Good/Needs Work/Critical] |
| Content Structure | X/20 | [Good/Needs Work/Critical] |
| Fact-Density | X/20 | [Good/Needs Work/Critical] |
| Extractability | X/20 | [Good/Needs Work/Critical] |
| AI Technical Readiness | X/15 | [Good/Needs Work/Critical] |

## Priority Issues
1. **[Issue]** - [Impact] - [Fix]
2. **[Issue]** - [Impact] - [Fix]
3. **[Issue]** - [Impact] - [Fix]

## AI Visibility Assessment
[Current citation probability and gaps]

## Action Plan

**Immediate:**
- [ ] Add TL;DR to top articles
- [ ] Implement FAQ schema

**Short-term:**
- [ ] Restructure headers as questions
- [ ] Add author credentials

**Ongoing:**
- [ ] Monitor AI platform citations
- [ ] Update content freshness
```

## Quick Audit (5-Point Check)

1. **TL;DR** - Summary present at top?
2. **Structure** - Question-based headers?
3. **Facts** - Statistics with sources?
4. **E-E-A-T** - Author credentials visible?
5. **Schema** - FAQPage/HowTo markup?

## Scoring Guide

- **90-100:** Excellent - High AI citation probability
- **70-89:** Good - Likely cited with minor improvements
- **50-69:** Needs Work - Significant optimization needed
- **Below 50:** Critical - Major restructuring required
