---
name: content-gap-analysis
description: Identifies content opportunities by finding topics and keywords your competitors cover that you don't. Reveals untapped content potential and strategic gaps in your content strategy.
---

# Content Gap Analysis

This skill identifies content opportunities by analyzing gaps between your content and competitors'. Find topics you're missing, keywords you could target, and content formats you should create.

## When to Use This Skill

- Planning content strategy and editorial calendar
- Finding quick-win content opportunities
- Understanding where competitors outperform you
- Identifying underserved topics in your niche
- Expanding into adjacent topic areas
- Prioritizing content creation efforts
- Finding GEO opportunities competitors miss

## What This Skill Does

1. **Keyword Gap Analysis**: Finds keywords competitors rank for that you don't
2. **Topic Coverage Mapping**: Identifies topic areas needing more content
3. **Content Format Gaps**: Reveals missing content types (videos, tools, guides)
4. **Audience Need Mapping**: Matches gaps to audience journey stages
5. **GEO Opportunity Detection**: Finds AI-answerable topics you're missing
6. **Priority Scoring**: Ranks gaps by impact and effort
7. **Content Calendar Creation**: Plans gap-filling content schedule

## How to Use

### Basic Gap Analysis

```
Find content gaps between my site [URL] and [competitor URLs]
```

```
What content am I missing compared to my top 3 competitors?
```

### Topic-Specific Analysis

```
Find content gaps in [topic area] compared to industry leaders
```

```
What [content type] do competitors have that I don't?
```

### Audience-Focused

```
What content gaps exist for [audience segment] in my niche?
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~SEO tool + ~~search console + ~~analytics + ~~AI monitor connected:**
Automatically pull your site's content inventory from ~~search console and ~~analytics (indexed pages, traffic per page, keywords ranking), competitor content data from ~~SEO tool (ranking keywords, top pages, backlink counts), and AI citation patterns from ~~AI monitor. Keyword overlap analysis and gap identification can be automated.

**With manual data only:**
Ask the user to provide:
1. Your site URL and content inventory (list of published content with topics)
2. Competitor URLs (3-5 sites)
3. Your current traffic and keyword performance (if available)
4. Known content strengths and weaknesses
5. Industry context and business goals

Proceed with the full analysis using provided data. Note in the output which metrics are from automated collection vs. user-provided data.

## Instructions

When a user requests content gap analysis:

1. **Define Analysis Scope**

   Clarify parameters:
   
   ```markdown
   ### Analysis Parameters
   
   **Your Site**: [URL]
   **Competitors to Analyze**: [URLs or "identify for me"]
   **Topic Focus**: [specific area or "all"]
   **Content Types**: [blogs, guides, tools, videos, or "all"]
   **Audience**: [target audience]
   **Business Goals**: [traffic, leads, authority, etc.]
   ```

2. **Audit Your Existing Content**

   ```markdown
   ## Your Content Inventory
   
   **Total Indexed Pages**: [X]
   **Content by Type**:
   - Blog posts: [X]
   - Landing pages: [X]
   - Resource pages: [X]
   - Tools/calculators: [X]
   - Case studies: [X]
   
   **Content by Topic Cluster**:
   
   | Topic | Articles | Keywords Ranking | Traffic |
   |-------|----------|------------------|---------|
   | [topic 1] | [X] | [X] | [X] |
   | [topic 2] | [X] | [X] | [X] |
   | [topic 3] | [X] | [X] | [X] |
   
   **Top Performing Content**:
   1. [Title] - [traffic] visits - [keywords] keywords
   2. [Title] - [traffic] visits - [keywords] keywords
   3. [Title] - [traffic] visits - [keywords] keywords
   
   **Content Strengths**:
   - [Strength 1]
   - [Strength 2]
   
   **Content Weaknesses**:
   - [Weakness 1]
   - [Weakness 2]
   ```

3. **Analyze Competitor Content**

   ```markdown
   ## Competitor Content Analysis
   
   ### Competitor 1: [Name/URL]
   
   **Content Volume**: [X] pages
   **Monthly Traffic**: [X] visits
   
   **Content Distribution**:
   | Type | Count | Est. Traffic |
   |------|-------|--------------|
   | Blog posts | [X] | [X] |
   | Guides | [X] | [X] |
   | Tools | [X] | [X] |
   | Videos | [X] | [X] |
   
   **Topic Coverage**:
   | Topic | Articles | Your Coverage |
   |-------|----------|---------------|
   | [topic] | [X] | [X or "None"] |
   
   **Unique Content They Have**:
   1. [Content piece] - [traffic] - [why it works]
   2. [Content piece] - [traffic] - [why it works]
   
   [Repeat for each competitor]
   ```

4. **Identify Keyword Gaps**

   ```markdown
   ## Keyword Gap Analysis
   
   ### Keywords Competitors Rank For (You Don't)
   
   **High Priority Gaps** (High volume, achievable difficulty)
   
   | Keyword | Volume | Difficulty | Competitor | Their Position |
   |---------|--------|------------|------------|----------------|
   | [kw 1] | [vol] | [diff] | [comp] | [pos] |
   | [kw 2] | [vol] | [diff] | [comp] | [pos] |
   | [kw 3] | [vol] | [diff] | [comp] | [pos] |
   
   **Quick Win Gaps** (Lower volume, low difficulty)
   
   | Keyword | Volume | Difficulty | Competitor | Their Position |
   |---------|--------|------------|------------|----------------|
   | [kw 1] | [vol] | [diff] | [comp] | [pos] |
   
   **Long-term Gaps** (High volume, high difficulty)
   
   | Keyword | Volume | Difficulty | Competitor | Their Position |
   |---------|--------|------------|------------|----------------|
   | [kw 1] | [vol] | [diff] | [comp] | [pos] |
   
   ### Keyword Overlap Analysis
   
   ```
   Venn Diagram Representation:
   
        You          Competitor 1
         ○               ○
        / \             / \
       /   \           /   \
      /  A  \ B       / C   \
     /       \       /       \
    ○─────────○─────○─────────○
              Competitor 2
   
   A: Keywords only you rank for: [X]
   B: Overlap with Comp 1: [X]
   C: Keywords all competitors share: [X]
   Gap: Keywords they all have, you don't: [X]
   ```
   
   **Unique Keywords (Your Advantage)**:
   | Keyword | Your Position | Volume |
   |---------|---------------|--------|
   | [kw] | [pos] | [vol] |
   ```

5. **Map Topic Gaps**

   ```markdown
   ## Topic Gap Analysis
   
   ### Topic Coverage Comparison
   
   | Topic Area | You | Comp 1 | Comp 2 | Comp 3 | Gap? |
   |------------|-----|--------|--------|--------|------|
   | [Topic 1] | ✅ [X] | ✅ [X] | ✅ [X] | ✅ [X] | No |
   | [Topic 2] | ❌ 0 | ✅ [X] | ✅ [X] | ✅ [X] | **Yes** |
   | [Topic 3] | ✅ [X] | ✅ [X] | ❌ 0 | ✅ [X] | Partial |
   | [Topic 4] | ❌ 0 | ✅ [X] | ✅ [X] | ❌ 0 | **Yes** |
   
   ### Missing Topic Clusters
   
   #### Gap 1: [Topic Area]
   
   **Why it matters**: [Business relevance]
   **Competitor coverage**: [Who covers it and how]
   **Opportunity size**: [Traffic/keyword potential]
   
   **Sub-topics to cover**:
   1. [Sub-topic] - [X] search volume
   2. [Sub-topic] - [X] search volume
   3. [Sub-topic] - [X] search volume
   
   **Recommended approach**:
   - Pillar content: [topic]
   - Cluster articles: [list]
   - Supporting content: [list]
   ```

6. **Identify Content Format Gaps**

   ```markdown
   ## Content Format Gap Analysis
   
   ### Format Distribution Comparison
   
   | Format | You | Comp 1 | Comp 2 | Industry Avg |
   |--------|-----|--------|--------|--------------|
   | Long-form guides | [X] | [X] | [X] | [X] |
   | Tutorials | [X] | [X] | [X] | [X] |
   | Comparison posts | [X] | [X] | [X] | [X] |
   | Case studies | [X] | [X] | [X] | [X] |
   | Tools/calculators | [X] | [X] | [X] | [X] |
   | Templates | [X] | [X] | [X] | [X] |
   | Video content | [X] | [X] | [X] | [X] |
   | Infographics | [X] | [X] | [X] | [X] |
   | Original research | [X] | [X] | [X] | [X] |
   
   ### Format Gaps to Fill
   
   #### Gap: [Format Type]
   
   **Current state**: You have [X], competitors average [Y]
   **Best examples**: [Competitor content examples]
   **Opportunity**: [Description]
   **Effort to create**: [Low/Medium/High]
   **Expected impact**: [Low/Medium/High]
   
   **Recommended first project**:
   [Specific content idea]
   ```

7. **Analyze GEO/AI Gaps**

   ```markdown
   ## GEO Content Gap Analysis
   
   ### AI-Answerable Topics Assessment
   
   **Topics where competitors get AI citations (you don't)**:
   
   | Topic | AI Cites | Why They're Cited | Your Gap |
   |-------|----------|-------------------|----------|
   | [topic 1] | [Comp] | [reason] | [what you need] |
   | [topic 2] | [Comp] | [reason] | [what you need] |
   
   ### GEO-Optimized Content Gaps
   
   **Missing Q&A Content**:
   | Question | Search Volume | Currently Answered By |
   |----------|---------------|----------------------|
   | [question] | [vol] | [competitor] |
   
   **Missing Definition/Explanation Content**:
   | Term | Search Volume | Best Current Source |
   |------|---------------|---------------------|
   | [term] | [vol] | [source] |
   
   **Missing Comparison Content**:
   | Comparison | Search Volume | Best Current Source |
   |------------|---------------|---------------------|
   | [A vs B] | [vol] | [source] |
   
   ### GEO Opportunity Score
   
   | Topic | Traditional SEO Value | GEO Value | Combined Priority |
   |-------|----------------------|-----------|-------------------|
   | [topic] | [score] | [score] | [priority] |
   ```

8. **Map to Audience Journey**

   ```markdown
   ## Audience Journey Gap Analysis
   
   ### Funnel Stage Coverage
   
   | Stage | Your Content | Competitor Avg | Gap |
   |-------|--------------|----------------|-----|
   | Awareness | [X] articles | [X] articles | [+/-X] |
   | Consideration | [X] articles | [X] articles | [+/-X] |
   | Decision | [X] articles | [X] articles | [+/-X] |
   | Retention | [X] articles | [X] articles | [+/-X] |
   
   ### Journey Gap Details
   
   #### Awareness Stage Gaps
   - Missing: [topics/content]
   - Opportunity: [description]
   
   #### Consideration Stage Gaps
   - Missing: [topics/content]
   - Opportunity: [description]
   
   #### Decision Stage Gaps
   - Missing: [topics/content]
   - Opportunity: [description]
   ```

9. **Prioritize and Create Action Plan**

   ```markdown
   # Content Gap Analysis Report
   
   ## Executive Summary
   
   **Analysis Date**: [Date]
   **Sites Analyzed**: [Your site] vs [Competitors]
   
   **Key Findings**:
   1. [Most significant gap]
   2. [Second significant gap]
   3. [Third significant gap]
   
   **Total Opportunity**:
   - Keywords gaps identified: [X]
   - Estimated traffic opportunity: [X]/month
   - Quick wins available: [X] pieces
   
   ---
   
   ## Prioritized Gap List
   
   ### Tier 1: Quick Wins (Do Now)
   
   | Content to Create | Target Keyword | Volume | Difficulty | Impact |
   |-------------------|----------------|--------|------------|--------|
   | [Title idea] | [keyword] | [vol] | [diff] | High |
   | [Title idea] | [keyword] | [vol] | [diff] | High |
   
   **Why prioritize**: Low effort, immediate ranking potential
   
   ### Tier 2: Strategic Builds (This Quarter)
   
   | Content to Create | Target Keyword | Volume | Difficulty | Impact |
   |-------------------|----------------|--------|------------|--------|
   | [Title idea] | [keyword] | [vol] | [diff] | High |
   
   **Why prioritize**: High value, requires more resources
   
   ### Tier 3: Long-term Investments (This Year)
   
   | Content to Create | Target Keyword | Volume | Difficulty | Impact |
   |-------------------|----------------|--------|------------|--------|
   | [Title idea] | [keyword] | [vol] | [diff] | High |
   
   **Why prioritize**: Builds authority, competitive differentiator
   
   ---
   
   ## Content Calendar Recommendation
   
   ### Month 1
   | Week | Content | Type | Target Keyword | Status |
   |------|---------|------|----------------|--------|
   | 1 | [Title] | [Type] | [Keyword] | Planned |
   | 2 | [Title] | [Type] | [Keyword] | Planned |
   | 3 | [Title] | [Type] | [Keyword] | Planned |
   | 4 | [Title] | [Type] | [Keyword] | Planned |
   
   ### Month 2
   [Continue...]
   
   ### Month 3
   [Continue...]
   
   ---
   
   ## Success Metrics
   
   Track these to measure gap-filling success:
   
   | Metric | Current | 3-Month Target | 6-Month Target |
   |--------|---------|----------------|----------------|
   | Keyword coverage | [X] | [X] | [X] |
   | Topic clusters complete | [X] | [X] | [X] |
   | Traffic from new content | [X] | [X] | [X] |
   | AI citations | [X] | [X] | [X] |
   ```

## Validation Checkpoints

### Input Validation
- [ ] Your content inventory is complete or representative sample provided
- [ ] Competitor URLs identified (minimum 2-3 competitors)
- [ ] Analysis scope defined (specific topics or comprehensive)
- [ ] Business goals and priorities clarified

### Output Validation
- [ ] Every recommendation cites specific data points (not generic advice)
- [ ] Gap analysis compares like-to-like content (topic clusters to topic clusters)
- [ ] Priority scoring based on measurable criteria (volume, difficulty, business fit)
- [ ] Content calendar maps gaps to realistic timeframes
- [ ] Source of each data point clearly stated (~~SEO tool data, ~~analytics data, ~~AI monitor data, user-provided, or estimated)

## Example

**User**: "Find content gaps for my SaaS marketing blog compared to HubSpot and Drift"

**Output**:

```markdown
# Content Gap Analysis: SaaS Marketing Blog

## Executive Summary

Compared to HubSpot and Drift, your blog has significant gaps in:
1. **Interactive tools** - They have 15+, you have 0
2. **Comparison content** - Missing "[Your Tool] vs [Competitor]" pages
3. **GEO-optimized definitions** - No glossary or term definitions

Total opportunity: ~25,000 monthly visits from 45 keyword gaps

## Top Keyword Gaps

### Quick Wins (Difficulty <40)

| Keyword | Volume | Difficulty | Who Ranks |
|---------|--------|------------|-----------|
| saas marketing metrics | 1,200 | 32 | HubSpot #3 |
| b2b email sequences | 890 | 28 | Drift #5 |
| saas onboarding emails | 720 | 25 | Neither! |
| marketing qualified lead definition | 1,800 | 35 | HubSpot #1 |

### Content Format Gaps

**You're missing**:
- [ ] Interactive ROI calculator (HubSpot gets 15k visits/mo from theirs)
- [ ] Email template library (Drift's gets 8k visits/mo)
- [ ] Marketing glossary (HubSpot's definition pages rank for 500+ keywords)

## Recommended Content Calendar

**Week 1**: "SaaS Marketing Metrics: Complete Guide" (Quick win)
**Week 2**: "What is a Marketing Qualified Lead?" (GEO opportunity)
**Week 3**: "B2B Email Sequence Templates" (Format gap)
**Week 4**: "[Your Tool] vs HubSpot" (Comparison gap)
```

## Advanced Analysis

### Competitive Cluster Comparison

```
Compare our topic cluster coverage for [topic] vs top 5 competitors
```

### Temporal Gap Analysis

```
What content have competitors published in the last 6 months that we haven't covered?
```

### Intent-Based Gaps

```
Find gaps in our [commercial/informational] intent content
```

## Tips for Success

1. **Focus on actionable gaps** - Not all gaps are worth filling
2. **Consider your resources** - Prioritize based on ability to execute
3. **Quality over quantity** - Better to fill 5 gaps well than 20 poorly
4. **Track what works** - Measure gap-filling success
5. **Update regularly** - Gaps change as competitors publish
6. **Include GEO opportunities** - Don't just optimize for traditional search

## Related Skills

- [keyword-research](../keyword-research/) - Deep-dive on gap keywords
- [competitor-analysis](../competitor-analysis/) - Understand competitor strategies
- [seo-content-writer](../../build/seo-content-writer/) - Create gap-filling content
- [content-refresher](../../optimize/content-refresher/) - Improve existing content

