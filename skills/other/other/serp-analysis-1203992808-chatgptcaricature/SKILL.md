---
name: serp-analysis
description: Analyzes search engine results pages (SERPs) to understand ranking factors, SERP features, user intent patterns, and AI overview triggers. Essential for understanding what it takes to rank.
---

# SERP Analysis

This skill analyzes Search Engine Results Pages to reveal what's working for ranking content, which SERP features appear, and what triggers AI-generated answers. Understand the battlefield before creating content.

## When to Use This Skill

- Before creating content for a target keyword
- Understanding why certain pages rank #1
- Identifying SERP feature opportunities (featured snippets, PAA)
- Analyzing AI Overview/SGE patterns
- Evaluating keyword difficulty more accurately
- Planning content format based on what ranks
- Identifying ranking factors for specific queries

## What This Skill Does

1. **SERP Composition Analysis**: Maps what appears on the results page
2. **Ranking Factor Identification**: Reveals why top results rank
3. **SERP Feature Mapping**: Identifies featured snippets, PAA, knowledge panels
4. **AI Overview Analysis**: Examines when and how AI answers appear
5. **Intent Signal Detection**: Confirms user intent from SERP composition
6. **Content Format Recommendations**: Suggests optimal format based on SERP
7. **Difficulty Assessment**: Evaluates realistic ranking potential

## How to Use

### Basic SERP Analysis

```
Analyze the SERP for [keyword]
```

```
What does it take to rank for [keyword]?
```

### Feature-Specific Analysis

```
Analyze featured snippet opportunities for [keyword list]
```

```
Which of these keywords trigger AI Overviews? [keyword list]
```

### Competitive SERP Analysis

```
Why does [URL] rank #1 for [keyword]?
```

## Instructions

When a user requests SERP analysis:

1. **Understand the Query**

   Clarify if needed:
   - Target keyword(s) to analyze
   - Search location/language
   - Device type (mobile/desktop)
   - Specific questions about the SERP

2. **Map SERP Composition**

   Document all elements appearing:

   ```markdown
   ## SERP Analysis: "[keyword]"
   
   **Search Details**
   - Keyword: [keyword]
   - Location: [location]
   - Device: [mobile/desktop]
   - Date: [date]
   
   ### SERP Layout Overview
   
   ```
   ┌─────────────────────────────────────────┐
   │ [AI Overview / SGE] (if present)        │
   ├─────────────────────────────────────────┤
   │ [Ads] - [X] ads above fold              │
   ├─────────────────────────────────────────┤
   │ [Featured Snippet] (if present)         │
   ├─────────────────────────────────────────┤
   │ [Organic Result #1]                     │
   │ [Organic Result #2]                     │
   │ [People Also Ask] (if present)          │
   │ [Organic Result #3]                     │
   │ ...                                     │
   ├─────────────────────────────────────────┤
   │ [Related Searches]                      │
   └─────────────────────────────────────────┘
   ```
   
   ### SERP Features Present
   
   | Feature | Present | Position | Opportunity |
   |---------|---------|----------|-------------|
   | AI Overview | Yes/No | Top | [analysis] |
   | Featured Snippet | Yes/No | [pos] | [analysis] |
   | People Also Ask | Yes/No | [pos] | [analysis] |
   | Knowledge Panel | Yes/No | Right | [analysis] |
   | Image Pack | Yes/No | [pos] | [analysis] |
   | Video Results | Yes/No | [pos] | [analysis] |
   | Local Pack | Yes/No | [pos] | [analysis] |
   | Shopping Results | Yes/No | [pos] | [analysis] |
   | News Results | Yes/No | [pos] | [analysis] |
   | Sitelinks | Yes/No | [pos] | [analysis] |
   ```

3. **Analyze Top Ranking Pages**

   For top 10 results:

   ```markdown
   ### Top 10 Organic Results Analysis
   
   #### Position #1: [Title]
   
   **URL**: [url]
   **Domain**: [domain]
   **Domain Authority**: [DA]
   
   **Content Analysis**:
   - Type: [Blog/Product/Guide/etc.]
   - Word Count: [X] words
   - Publish Date: [date]
   - Last Updated: [date]
   
   **On-Page Factors**:
   - Title: [exact title]
   - Title contains keyword: Yes/No
   - Meta description: [description]
   - H1: [heading]
   - URL structure: [clean/keyword-rich/etc.]
   
   **Content Structure**:
   - Headings (H2s): [list key sections]
   - Media: [X] images, [X] videos
   - Tables/Lists: Yes/No
   - FAQ section: Yes/No
   
   **Estimated Metrics**:
   - Page backlinks: [X]
   - Referring domains: [X]
   - Social shares: [X]
   
   **Why It Ranks #1**:
   1. [Factor 1]
   2. [Factor 2]
   3. [Factor 3]
   
   [Repeat for positions #2-10]
   ```

4. **Identify Ranking Patterns**

   ```markdown
   ### Ranking Patterns Analysis
   
   **Common Characteristics of Top 5 Results**:
   
   | Factor | Avg/Common Value | Importance |
   |--------|-----------------|------------|
   | Word Count | [X] words | High/Med/Low |
   | Domain Authority | [X] | High/Med/Low |
   | Page Backlinks | [X] | High/Med/Low |
   | Content Freshness | [timeframe] | High/Med/Low |
   | HTTPS | [X]% | High/Med/Low |
   | Mobile Optimized | [X]% | High/Med/Low |
   
   **Content Format Distribution**:
   - How-to guides: [X]/10
   - Listicles: [X]/10
   - In-depth articles: [X]/10
   - Product pages: [X]/10
   - Other: [X]/10
   
   **Domain Type Distribution**:
   - Brand/Company sites: [X]/10
   - Media/News sites: [X]/10
   - Niche blogs: [X]/10
   - Aggregators: [X]/10
   
   **Key Success Factors Identified**:
   
   1. **[Factor 1]**: [Explanation + evidence]
   2. **[Factor 2]**: [Explanation + evidence]
   3. **[Factor 3]**: [Explanation + evidence]
   ```

5. **Analyze SERP Features**

   ```markdown
   ### Featured Snippet Analysis
   
   **Current Snippet Holder**: [URL]
   **Snippet Type**: [Paragraph/List/Table/Video]
   **Snippet Content**: 
   > [Exact text/description of snippet]
   
   **How to Win This Snippet**:
   1. [Strategy based on current snippet]
   2. [Content format recommendation]
   3. [Structure recommendation]
   
   ---
   
   ### People Also Ask (PAA) Analysis
   
   **Questions Appearing**:
   1. [Question 1] → Currently answered by: [URL]
   2. [Question 2] → Currently answered by: [URL]
   3. [Question 3] → Currently answered by: [URL]
   4. [Question 4] → Currently answered by: [URL]
   
   **PAA Optimization Strategy**:
   - Include these questions as H2/H3 headings
   - Provide direct, concise answers (40-60 words)
   - Use FAQ schema markup
   
   ---
   
   ### AI Overview Analysis
   
   **AI Overview Present**: Yes/No
   **AI Overview Type**: [Summary/List/Comparison/etc.]
   
   **Sources Cited in AI Overview**:
   1. [Source 1] - [Why cited]
   2. [Source 2] - [Why cited]
   3. [Source 3] - [Why cited]
   
   **AI Overview Content Patterns**:
   - Pulls definitions from: [source type]
   - Lists information as: [format]
   - Cites statistics from: [source type]
   
   **How to Get Cited in AI Overview**:
   1. [Specific recommendation]
   2. [Specific recommendation]
   3. [Specific recommendation]
   ```

6. **Determine Search Intent**

   ```markdown
   ### Search Intent Analysis
   
   **Primary Intent**: [Informational/Commercial/Transactional/Navigational]
   
   **Evidence**:
   - SERP features suggest: [analysis]
   - Top results are: [content types]
   - User likely wants: [description]
   
   **Intent Breakdown**:
   - Informational signals: [X]%
   - Commercial signals: [X]%
   - Transactional signals: [X]%
   
   **Content Format Implication**:
   Based on intent, your content should:
   - Format: [recommendation]
   - Tone: [recommendation]
   - CTA: [recommendation]
   ```

7. **Calculate True Difficulty**

   ```markdown
   ### Difficulty Assessment
   
   **Overall Difficulty Score**: [X]/100
   
   **Difficulty Factors**:
   
   | Factor | Score | Weight | Impact |
   |--------|-------|--------|--------|
   | Top 10 Domain Authority | [avg] | 25% | [High/Med/Low] |
   | Top 10 Page Authority | [avg] | 20% | [High/Med/Low] |
   | Backlinks Required | [est.] | 20% | [High/Med/Low] |
   | Content Quality Bar | [rating] | 20% | [High/Med/Low] |
   | SERP Stability | [rating] | 15% | [High/Med/Low] |
   
   **Realistic Assessment**:
   
   - **New site (DA <20)**: [Can rank?] [Timeframe]
   - **Growing site (DA 20-40)**: [Can rank?] [Timeframe]
   - **Established site (DA 40+)**: [Can rank?] [Timeframe]
   
   **Easier Alternatives**:
   If too difficult, consider:
   - [Alternative keyword 1] - Difficulty: [X]
   - [Alternative keyword 2] - Difficulty: [X]
   ```

8. **Generate Recommendations**

   ```markdown
   ## SERP Analysis Summary & Recommendations
   
   ### Key Findings
   
   1. [Most important finding]
   2. [Second important finding]
   3. [Third important finding]
   
   ### Content Requirements to Rank
   
   To compete for "[keyword]", you need:
   
   **Minimum Requirements**:
   - [ ] Word count: [X]+ words
   - [ ] Backlinks: [X]+ referring domains
   - [ ] Domain Authority: [X]+
   - [ ] Content format: [type]
   - [ ] Include: [specific elements]
   
   **Differentiators to Win**:
   - [ ] [Unique angle from analysis]
   - [ ] [Missing element in current results]
   - [ ] [SERP feature opportunity]
   
   ### SERP Feature Strategy
   
   | Feature | Winnable? | Strategy |
   |---------|-----------|----------|
   | Featured Snippet | Yes/No | [strategy] |
   | PAA | Yes/No | [strategy] |
   | AI Overview | Yes/No | [strategy] |
   
   ### Recommended Content Outline
   
   Based on SERP analysis:
   
   ```
   Title: [Optimized title]
   
   H1: [Main heading]
   
   [Introduction - address intent immediately]
   
   H2: [Section based on PAA/top results]
   H2: [Section based on PAA/top results]
   H2: [Section based on PAA/top results]
   
   [FAQ section for PAA optimization]
   
   [Conclusion with CTA]
   ```
   
   ### Next Steps
   
   1. [Immediate action]
   2. [Content creation action]
   3. [Optimization action]
   ```

## Example

**User**: "Analyze the SERP for 'how to start a podcast'"

**Output**:

```markdown
# SERP Analysis: "how to start a podcast"

## SERP Overview

**Intent**: Informational (100%)
**Difficulty**: 72/100 (High)
**AI Overview**: Yes - comprehensive guide format

### SERP Features Present

| Feature | Present | Analysis |
|---------|---------|----------|
| AI Overview | ✅ | Lists steps, cites 3 sources |
| Featured Snippet | ✅ | Step-by-step list from Buzzsprout |
| People Also Ask | ✅ | 4 questions visible, expandable |
| Video Results | ✅ | 3 YouTube videos mid-page |
| Image Pack | ❌ | |

### Top 5 Results Analysis

| Pos | Domain | DA | Word Count | Format | Backlinks |
|-----|--------|-----|------------|--------|-----------|
| 1 | Buzzsprout | 71 | 8,500 | Ultimate Guide | 2,400 |
| 2 | Spotify | 93 | 3,200 | How-to Guide | 890 |
| 3 | Podcastinsights | 58 | 12,000 | Mega Guide | 1,800 |
| 4 | Transistor | 62 | 5,500 | Tutorial | 720 |
| 5 | HubSpot | 91 | 6,200 | Complete Guide | 1,100 |

### Why #1 Ranks First

Buzzsprout's guide succeeds because:
1. **Comprehensive** - Covers every step in detail
2. **Updated** - "2024" in title, recent updates
3. **Structured** - Clear numbered steps (owns featured snippet)
4. **Authoritative** - Podcast hosting company (topical authority)
5. **Supporting content** - Links to detailed sub-guides

### Featured Snippet Opportunity

**Current format**: Ordered list (steps)
**Current holder**: Buzzsprout

**To win snippet**:
- Create cleaner, more scannable list format
- Keep steps to 8-10 items max
- Start each step with action verb
- Include "how to start a podcast" in H2

### AI Overview Analysis

**Sources cited**:
1. Buzzsprout - "Choose your podcast topic"
2. Spotify for Podcasters - "Record and edit"
3. Wikipedia - Definition of podcasting

**Pattern**: AI pulls step-by-step instructions from guides with clear structure

### Content Requirements

To rank on page 1:
- **Word count**: 5,000+ words minimum
- **Format**: Step-by-step ultimate guide
- **Backlinks**: 500+ from relevant domains
- **Updates**: Must show current year
- **Unique angle**: Equipment comparisons, cost breakdowns, or specific niche focus

### Recommended Strategy

Given high difficulty, consider:
1. Target long-tail: "how to start a podcast for free" (Difficulty: 45)
2. Target niche: "how to start a podcast about [topic]" (Difficulty: 30)
3. Create supporting video content for video carousel
4. Focus on PAA optimization for quick wins
```

## Advanced Analysis

### Multi-Keyword SERP Comparison

```
Compare SERPs for [keyword 1], [keyword 2], [keyword 3]
```

### Historical SERP Changes

```
How has the SERP for [keyword] changed over time?
```

### Local SERP Variations

```
Compare SERP for [keyword] in [location 1] vs [location 2]
```

### Mobile vs Desktop SERP

```
Analyze mobile vs desktop SERP differences for [keyword]
```

## Tips for Success

1. **Always check SERP before writing** - Don't assume, verify
2. **Match content format to SERP** - If lists rank, write lists
3. **Identify SERP feature opportunities** - Lower competition than #1
4. **Note SERP volatility** - Stable SERPs are harder to break into
5. **Study the outliers** - Why does a weaker site rank? Opportunity!
6. **Consider AI Overview optimization** - Growing importance

## Related Skills

- [keyword-research](../keyword-research/) - Find keywords to analyze
- [competitor-analysis](../competitor-analysis/) - Deep dive on ranking competitors
- [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) - Optimize based on findings
- [geo-content-optimizer](../../build/geo-content-optimizer/) - Optimize for AI citations

