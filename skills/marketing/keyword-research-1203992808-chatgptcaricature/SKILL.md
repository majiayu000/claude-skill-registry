---
name: keyword-research
description: Discovers high-value keywords with search intent analysis, difficulty assessment, and content opportunity mapping. Essential for starting any SEO or GEO content strategy.
---

# Keyword Research

This skill helps you discover, analyze, and prioritize keywords for SEO and GEO content strategies. It identifies high-value opportunities based on search volume, competition, intent, and business relevance.

## ⚠️ Language Scope: English Only

> **This skill is designed for English keyword research.**

### For Non-English Keywords

**DO NOT use this skill for locale-specific keyword research.**

Instead:
1. **Read validated keywords**: `.claude/skills/i18n-seo-localizer/data/keywords-{locale}.json`
2. **If keyword not found**: Use cumulative SERP analysis (see `i18n-seo-localizer/references/00-keyword-research.md`)
3. **Add to data file**: Store validated keywords for future use

### Why Separate Skills?

| Language | Problem with Direct Translation | Solution |
|----------|--------------------------------|----------|
| Chinese | "AI image generator" → "AI图像生成器" (low volume) | Use "AI绘画" (validated) |
| Russian | "AI" → "ИИ" (less common) | Use "Нейросеть" (validated) |
| German | "AI" → "AI" (wrong) | Use "KI" (validated) |

**Always read keyword data files first for non-English content.**

---

## When to Use This Skill

- Starting a new content strategy or campaign (English)
- Expanding into new topics or markets (English)
- Finding keywords for a specific product or service (English)
- Identifying long-tail keyword opportunities (English)
- Understanding search intent for your industry (English)
- Planning content calendars (English)
- Researching keywords for GEO optimization (English)

## What This Skill Does

1. **Keyword Discovery**: Generates comprehensive keyword lists from seed terms
2. **Intent Classification**: Categorizes keywords by user intent (informational, navigational, commercial, transactional)
3. **Difficulty Assessment**: Evaluates competition level and ranking difficulty
4. **Opportunity Scoring**: Prioritizes keywords by potential ROI
5. **Clustering**: Groups related keywords into topic clusters
6. **GEO Relevance**: Identifies keywords likely to trigger AI responses

## How to Use

### Basic Keyword Research

```
Research keywords for [topic/product/service]
```

```
Find keyword opportunities for a [industry] business targeting [audience]
```

### With Specific Goals

```
Find low-competition keywords for [topic] with commercial intent
```

```
Identify question-based keywords for [topic] that AI systems might answer
```

### Competitive Research

```
What keywords is [competitor URL] ranking for that I should target?
```

## Instructions

When a user requests keyword research:

1. **Understand the Context**

   Ask clarifying questions if not provided:
   - What is your product/service/topic?
   - Who is your target audience?
   - What is your business goal? (traffic, leads, sales)
   - What is your current domain authority? (new site, established, etc.)
   - Any specific geographic targeting?
   - Preferred language?

2. **Generate Seed Keywords**

   Start with:
   - Core product/service terms
   - Problem-focused keywords (what issues do you solve?)
   - Solution-focused keywords (how do you help?)
   - Audience-specific terms
   - Industry terminology

3. **Expand Keyword List**

   For each seed keyword, generate variations:
   
   ```markdown
   ## Keyword Expansion Patterns
   
   ### Modifiers
   - Best [keyword]
   - Top [keyword]
   - [keyword] for [audience]
   - [keyword] near me
   - [keyword] [year]
   - How to [keyword]
   - What is [keyword]
   - [keyword] vs [alternative]
   - [keyword] examples
   - [keyword] tools
   
   ### Long-tail Variations
   - [keyword] for beginners
   - [keyword] for small business
   - Free [keyword]
   - [keyword] software/tool/service
   - [keyword] template
   - [keyword] checklist
   - [keyword] guide
   ```

4. **Classify Search Intent**

   Categorize each keyword:

   | Intent | Signals | Example | Content Type |
   |--------|---------|---------|--------------|
   | Informational | what, how, why, guide, learn | "what is SEO" | Blog posts, guides |
   | Navigational | brand names, specific sites | "google analytics login" | Homepage, product pages |
   | Commercial | best, review, vs, compare | "best SEO tools 2024" | Comparison posts, reviews |
   | Transactional | buy, price, discount, order | "buy SEO software" | Product pages, pricing |

5. **Assess Keyword Difficulty**

   Score each keyword (1-100 scale):

   ```markdown
   ### Difficulty Factors
   
   **High Difficulty (70-100)**
   - Major brands ranking
   - High domain authority competitors
   - Established content (1000+ backlinks)
   - Paid ads dominating SERP
   
   **Medium Difficulty (40-69)**
   - Mix of authority and niche sites
   - Some opportunities for quality content
   - Moderate backlink requirements
   
   **Low Difficulty (1-39)**
   - Few authoritative competitors
   - Thin or outdated content ranking
   - Long-tail variations
   - New or emerging topics
   ```

6. **Calculate Opportunity Score**

   Formula: `Opportunity = (Volume × Intent Value) / Difficulty`

   ```markdown
   ### Opportunity Matrix
   
   | Scenario | Volume | Difficulty | Intent | Priority |
   |----------|--------|------------|--------|----------|
   | Quick Win | Low-Med | Low | High | ⭐⭐⭐⭐⭐ |
   | Growth | High | Medium | High | ⭐⭐⭐⭐ |
   | Long-term | High | High | High | ⭐⭐⭐ |
   | Research | Low | Low | Low | ⭐⭐ |
   ```

7. **Identify GEO Opportunities**

   Keywords likely to trigger AI responses:
   
   ```markdown
   ### GEO-Relevant Keywords
   
   **High GEO Potential**
   - Question formats: "What is...", "How does...", "Why is..."
   - Definition queries: "[term] meaning", "[term] definition"
   - Comparison queries: "[A] vs [B]", "difference between..."
   - List queries: "best [category]", "top [number] [items]"
   - How-to queries: "how to [action]", "steps to [goal]"
   
   **AI Answer Indicators**
   - Query is factual/definitional
   - Answer can be summarized concisely
   - Topic is well-documented online
   - Low commercial intent
   ```

8. **Create Topic Clusters**

   Group keywords into content clusters:

   ```markdown
   ## Topic Cluster: [Main Topic]
   
   **Pillar Content**: [Primary keyword]
   - Search volume: [X]
   - Difficulty: [X]
   - Content type: Comprehensive guide
   
   **Cluster Content**:
   
   ### Sub-topic 1: [Secondary keyword]
   - Volume: [X]
   - Difficulty: [X]
   - Links to: Pillar
   - Content type: [Blog post/Tutorial/etc.]
   
   ### Sub-topic 2: [Secondary keyword]
   - Volume: [X]
   - Difficulty: [X]
   - Links to: Pillar + Sub-topic 1
   - Content type: [Blog post/Tutorial/etc.]
   
   [Continue for all cluster keywords...]
   ```

9. **Generate Output Report**

   ```markdown
   # Keyword Research Report: [Topic]
   
   **Generated**: [Date]
   **Target Audience**: [Audience]
   **Business Goal**: [Goal]
   
   ## Executive Summary
   
   - Total keywords analyzed: [X]
   - High-priority opportunities: [X]
   - Estimated traffic potential: [X]/month
   - Recommended focus areas: [List]
   
   ## Top Keyword Opportunities
   
   ### Quick Wins (Low difficulty, High value)
   
   | Keyword | Volume | Difficulty | Intent | Score |
   |---------|--------|------------|--------|-------|
   | [keyword 1] | [X] | [X] | [type] | [X] |
   | [keyword 2] | [X] | [X] | [type] | [X] |
   
   ### Growth Keywords (Medium difficulty, High volume)
   
   | Keyword | Volume | Difficulty | Intent | Score |
   |---------|--------|------------|--------|-------|
   | [keyword 1] | [X] | [X] | [type] | [X] |
   
   ### GEO Opportunities (AI-citation potential)
   
   | Keyword | Type | AI Potential | Recommended Format |
   |---------|------|--------------|-------------------|
   | [keyword 1] | Question | High | Q&A section |
   | [keyword 2] | Definition | High | Clear definition |
   
   ## Topic Clusters
   
   [Include cluster maps]
   
   ## Content Calendar Recommendations
   
   | Month | Content | Target Keyword | Type |
   |-------|---------|----------------|------|
   | [Month] | [Title] | [Keyword] | [Type] |
   
   ## Next Steps
   
   1. [Action item 1]
   2. [Action item 2]
   3. [Action item 3]
   ```

## Example

**User**: "Research keywords for a project management software company targeting small businesses"

**Output**:

```markdown
# Keyword Research Report: Project Management Software

**Generated**: December 2024
**Target Audience**: Small business owners and teams
**Business Goal**: Software signups and trials

## Executive Summary

- Total keywords analyzed: 150+
- High-priority opportunities: 23
- Estimated traffic potential: 45,000/month
- Recommended focus areas: 
  - Task management workflows
  - Team collaboration
  - Small business productivity

## Top Keyword Opportunities

### Quick Wins (Priority: Immediate)

| Keyword | Volume | Difficulty | Intent | Score |
|---------|--------|------------|--------|-------|
| project management for small teams | 1,200 | 28 | Commercial | 92 |
| simple task management software | 890 | 25 | Commercial | 89 |
| best free project management tool | 2,400 | 35 | Commercial | 85 |
| how to manage remote team projects | 720 | 22 | Informational | 82 |
| project tracking spreadsheet alternative | 480 | 18 | Commercial | 80 |

### Growth Keywords (Priority: 3-6 months)

| Keyword | Volume | Difficulty | Intent | Score |
|---------|--------|------------|--------|-------|
| project management software | 18,000 | 72 | Commercial | 65 |
| best project management tools 2024 | 8,500 | 65 | Commercial | 62 |
| project management app | 12,000 | 68 | Commercial | 58 |

### GEO Opportunities (AI-citation potential)

| Keyword | Type | AI Potential | Recommended Format |
|---------|------|--------------|-------------------|
| what is project management | Definition | ⭐⭐⭐⭐⭐ | Clear definition + methodology |
| agile vs waterfall | Comparison | ⭐⭐⭐⭐⭐ | Side-by-side comparison table |
| project management methodologies | List | ⭐⭐⭐⭐ | Comprehensive list with pros/cons |
| how to create a project plan | How-to | ⭐⭐⭐⭐ | Step-by-step guide |
| project management best practices | List | ⭐⭐⭐⭐ | Numbered best practices |

## Topic Clusters

### Cluster 1: Project Management Fundamentals

**Pillar**: "Complete Guide to Project Management" (8,500 volume)

Cluster articles:
1. What is project management? (2,200 volume)
2. Project management methodologies explained (1,800 volume)
3. How to create a project plan (1,400 volume)
4. Project management best practices (1,200 volume)
5. Project management roles and responsibilities (890 volume)

### Cluster 2: Team Collaboration

**Pillar**: "Team Collaboration Tools Guide" (4,200 volume)

Cluster articles:
1. How to improve team communication (1,600 volume)
2. Remote team management tips (1,400 volume)
3. Best practices for distributed teams (920 volume)
4. Team productivity tools comparison (780 volume)

## Content Calendar Recommendations

| Month | Content | Target Keyword | Type |
|-------|---------|----------------|------|
| Week 1 | Simple Task Management Guide | simple task management software | Blog + Demo |
| Week 2 | Project Management for Small Teams | project management for small teams | Pillar Page |
| Week 3 | Agile vs Waterfall: Complete Comparison | agile vs waterfall | Comparison |
| Week 4 | Free PM Tools Roundup | best free project management tool | Listicle |

## Next Steps

1. **Immediate**: Create landing pages for top 5 quick-win keywords
2. **Week 1-2**: Write pillar content for "Project Management Fundamentals"
3. **Week 3-4**: Build out cluster content with internal linking
4. **Ongoing**: Track rankings and adjust strategy based on performance
```

## Advanced Features

### Intent Mapping

```
Map all keywords for [topic] by search intent and funnel stage
```

### Seasonal Analysis

```
Identify seasonal keyword trends for [industry]
```

### Competitor Gap

```
What keywords do [competitor 1], [competitor 2], [competitor 3] rank for 
that I'm missing?
```

### Local Keywords

```
Research local keywords for [business type] in [city/region]
```

## Tips for Success

1. **Start with seed keywords** that describe your core offering
2. **Don't ignore long-tail** - they often have highest conversion rates
3. **Match content to intent** - informational queries need guides, not sales pages
4. **Group into clusters** for topical authority
5. **Prioritize quick wins** to build momentum and credibility
6. **Include GEO keywords** in your strategy for AI visibility
7. **Review quarterly** - keyword dynamics change over time

## Related Skills

- [competitor-analysis](../competitor-analysis/) - See what keywords competitors rank for
- [content-gap-analysis](../content-gap-analysis/) - Find missing keyword opportunities
- [seo-content-writer](../../build/seo-content-writer/) - Create content for target keywords
- [geo-content-optimizer](../../build/geo-content-optimizer/) - Optimize for AI citations

