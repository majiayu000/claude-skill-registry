---
name: on-page-seo-auditor
version: "1.0"
description: Performs comprehensive on-page SEO audits to identify optimization opportunities including title tags, meta descriptions, headers, content quality, internal linking, and image optimization.
---

# On-Page SEO Auditor

This skill performs detailed on-page SEO audits to identify issues and optimization opportunities. It analyzes all on-page elements that affect search rankings and provides actionable recommendations.

## When to Use This Skill

- Auditing pages before or after publishing
- Identifying why a page isn't ranking well
- Optimizing existing content for better performance
- Creating pre-publish SEO checklists
- Comparing your on-page SEO to competitors
- Systematic site-wide SEO improvements
- Training team members on SEO best practices

## What This Skill Does

1. **Title Tag Analysis**: Evaluates title optimization and CTR potential
2. **Meta Description Review**: Checks description quality and length
3. **Header Structure Audit**: Analyzes H1-H6 hierarchy
4. **Content Quality Assessment**: Reviews content depth and optimization
5. **Keyword Usage Analysis**: Checks keyword placement and density
6. **Internal Link Review**: Evaluates internal linking structure
7. **Image Optimization Check**: Audits alt text and file optimization
8. **Technical On-Page Review**: Checks URL, canonical, and mobile factors

## How to Use

### Audit a Single Page

```
Audit the on-page SEO of [URL]
```

```
Check SEO issues on this page targeting [keyword]: [URL/content]
```

### Compare Against Competitors

```
Compare on-page SEO of [your URL] vs [competitor URL] for [keyword]
```

### Audit Content Before Publishing

```
Pre-publish SEO audit for this content targeting [keyword]: [content]
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~SEO tool + ~~web crawler connected:**
Claude can automatically pull page HTML via ~~web crawler, fetch keyword search volume and difficulty from ~~SEO tool, retrieve click-through rate data from ~~search console, and download competitor pages for comparison. This enables fully automated audits with live data.

**With manual data only:**
Ask the user to provide:
1. Page URL or complete HTML content
2. Target primary and secondary keywords
3. Competitor page URLs for comparison (optional)

Proceed with the full audit using provided data. Note in the output which findings are from automated crawl vs. manual review.

## Instructions

When a user requests an on-page SEO audit:

1. **Gather Page Information**

   ```markdown
   ### Audit Setup
   
   **Page URL**: [URL]
   **Target Keyword**: [primary keyword]
   **Secondary Keywords**: [additional keywords]
   **Page Type**: [blog/product/landing/service]
   **Business Goal**: [traffic/conversions/authority]
   ```

2. **Audit Title Tag**

   ```markdown
   ## Title Tag Analysis
   
   **Current Title**: [title]
   **Character Count**: [X] characters
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Length (50-60 chars) | ✅/⚠️/❌ | [notes] |
   | Keyword included | ✅/⚠️/❌ | Position: [front/middle/end] |
   | Keyword at front | ✅/⚠️/❌ | [notes] |
   | Unique across site | ✅/⚠️/❌ | [notes] |
   | Compelling/clickable | ✅/⚠️/❌ | [notes] |
   | Matches intent | ✅/⚠️/❌ | [notes] |
   
   **Title Score**: [X]/10
   
   **Issues Found**:
   - [Issue 1]
   - [Issue 2]
   
   **Recommended Title**:
   "[Optimized title suggestion]"
   
   **Why**: [Explanation of improvements]
   ```

3. **Audit Meta Description**

   ```markdown
   ## Meta Description Analysis
   
   **Current Description**: [description]
   **Character Count**: [X] characters
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Length (150-160 chars) | ✅/⚠️/❌ | [notes] |
   | Keyword included | ✅/⚠️/❌ | [notes] |
   | Call-to-action present | ✅/⚠️/❌ | [notes] |
   | Unique across site | ✅/⚠️/❌ | [notes] |
   | Accurately describes page | ✅/⚠️/❌ | [notes] |
   | Compelling copy | ✅/⚠️/❌ | [notes] |
   
   **Description Score**: [X]/10
   
   **Issues Found**:
   - [Issue 1]
   
   **Recommended Description**:
   "[Optimized description suggestion]" ([X] chars)
   ```

4. **Audit Header Structure**

   ```markdown
   ## Header Structure Analysis
   
   ### Current Header Hierarchy
   
   ```
   H1: [H1 text]
     H2: [H2 text]
       H3: [H3 text]
       H3: [H3 text]
     H2: [H2 text]
       H3: [H3 text]
     H2: [H2 text]
   ```
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Single H1 | ✅/⚠️/❌ | Found: [X] H1s |
   | H1 includes keyword | ✅/⚠️/❌ | [notes] |
   | Logical hierarchy | ✅/⚠️/❌ | [notes] |
   | H2s include keywords | ✅/⚠️/❌ | [X]/[Y] contain keywords |
   | No skipped levels | ✅/⚠️/❌ | [notes] |
   | Descriptive headers | ✅/⚠️/❌ | [notes] |
   
   **Header Score**: [X]/10
   
   **Issues Found**:
   - [Issue 1]
   - [Issue 2]
   
   **Recommended Changes**:
   - H1: [suggestion]
   - H2s: [suggestions]
   ```

5. **Audit Content Quality**

   ```markdown
   ## Content Quality Analysis
   
   **Word Count**: [X] words
   **Reading Level**: [Grade level]
   **Estimated Read Time**: [X] minutes
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Sufficient length | ✅/⚠️/❌ | [comparison to ranking content] |
   | Comprehensive coverage | ✅/⚠️/❌ | [notes] |
   | Unique value/insights | ✅/⚠️/❌ | [notes] |
   | Up-to-date information | ✅/⚠️/❌ | [notes] |
   | Proper formatting | ✅/⚠️/❌ | [notes] |
   | Readability | ✅/⚠️/❌ | [notes] |
   | E-E-A-T signals | ✅/⚠️/❌ | [notes] |
   
   **Content Elements Present**:
   - [ ] Introduction with keyword
   - [ ] Clear sections/structure
   - [ ] Bullet points/lists
   - [ ] Tables where appropriate
   - [ ] Images/visuals
   - [ ] Examples/case studies
   - [ ] Statistics with sources
   - [ ] Expert quotes
   - [ ] FAQ section
   - [ ] Conclusion with CTA
   
   **Content Score**: [X]/10
   
   **Gaps Identified**:
   - [Missing topic/section 1]
   - [Missing topic/section 2]
   
   **Recommendations**:
   1. [Specific improvement]
   2. [Specific improvement]
   ```

6. **Audit Keyword Usage**

   ```markdown
   ## Keyword Optimization Analysis
   
   **Primary Keyword**: "[keyword]"
   **Keyword Density**: [X]%
   
   ### Keyword Placement
   
   | Location | Present | Notes |
   |----------|---------|-------|
   | Title tag | ✅/❌ | Position: [X] |
   | Meta description | ✅/❌ | [notes] |
   | H1 | ✅/❌ | [notes] |
   | First 100 words | ✅/❌ | Word position: [X] |
   | H2 headings | ✅/❌ | In [X]/[Y] H2s |
   | Body content | ✅/❌ | [X] occurrences |
   | URL slug | ✅/❌ | [notes] |
   | Image alt text | ✅/❌ | In [X]/[Y] images |
   | Conclusion | ✅/❌ | [notes] |
   
   ### Secondary Keywords
   
   | Keyword | Occurrences | Status |
   |---------|-------------|--------|
   | [keyword 1] | [X] | ✅/⚠️/❌ |
   | [keyword 2] | [X] | ✅/⚠️/❌ |
   
   ### LSI/Related Terms
   
   **Present**: [list of related terms found]
   **Missing**: [important related terms not found]
   
   **Keyword Score**: [X]/10
   
   **Issues**:
   - [Issue 1]
   
   **Recommendations**:
   - [Suggestion 1]
   ```

7. **Audit Internal Links**

   ```markdown
   ## Internal Linking Analysis
   
   **Total Internal Links**: [X]
   **Unique Internal Links**: [X]
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Number of internal links | ✅/⚠️/❌ | [X] (recommend 3-5+) |
   | Relevant anchor text | ✅/⚠️/❌ | [notes] |
   | Links to related content | ✅/⚠️/❌ | [notes] |
   | Links to important pages | ✅/⚠️/❌ | [notes] |
   | No broken links | ✅/⚠️/❌ | [X] broken found |
   | Natural placement | ✅/⚠️/❌ | [notes] |
   
   **Current Internal Links**:
   1. "[Anchor text]" → [URL]
   2. "[Anchor text]" → [URL]
   3. "[Anchor text]" → [URL]
   
   **Internal Linking Score**: [X]/10
   
   **Recommended Additional Links**:
   1. Add link to "[Related page]" with anchor "[suggested anchor]"
   2. Add link to "[Related page]" with anchor "[suggested anchor]"
   
   **Anchor Text Improvements**:
   - Change "[current anchor]" to "[improved anchor]"
   ```

8. **Audit Images**

   ```markdown
   ## Image Optimization Analysis
   
   **Total Images**: [X]
   
   ### Image Audit Table
   
   | Image | Alt Text | File Name | Size | Status |
   |-------|----------|-----------|------|--------|
   | [img1] | [alt or "missing"] | [filename] | [KB] | ✅/⚠️/❌ |
   | [img2] | [alt or "missing"] | [filename] | [KB] | ✅/⚠️/❌ |
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | All images have alt text | ✅/⚠️/❌ | [X]/[Y] have alt |
   | Alt text includes keywords | ✅/⚠️/❌ | [notes] |
   | Descriptive file names | ✅/⚠️/❌ | [notes] |
   | Appropriate file sizes | ✅/⚠️/❌ | [notes] |
   | Modern formats (WebP) | ✅/⚠️/❌ | [notes] |
   | Lazy loading enabled | ✅/⚠️/❌ | [notes] |
   
   **Image Score**: [X]/10
   
   **Recommendations**:
   1. Add alt text to image [X]: "[suggested alt text]"
   2. Compress image [Y]: Currently [X]KB, should be under [Y]KB
   3. Rename [filename] to [better-filename]
   ```

9. **Audit Technical On-Page Elements**

   ```markdown
   ## Technical On-Page Analysis
   
   | Element | Current Value | Status | Recommendation |
   |---------|---------------|--------|----------------|
   | URL | [URL] | ✅/⚠️/❌ | [notes] |
   | URL length | [X] chars | ✅/⚠️/❌ | [notes] |
   | URL keywords | [present/absent] | ✅/⚠️/❌ | [notes] |
   | Canonical tag | [URL or "missing"] | ✅/⚠️/❌ | [notes] |
   | Mobile-friendly | [yes/no] | ✅/⚠️/❌ | [notes] |
   | Page speed | [X]s | ✅/⚠️/❌ | [notes] |
   | HTTPS | [yes/no] | ✅/⚠️/❌ | [notes] |
   | Schema markup | [types or "none"] | ✅/⚠️/❌ | [notes] |
   
   **Technical Score**: [X]/10
   ```

10. **CORE-EEAT Content Quality Quick Scan**

    Run a quick scan of on-page-relevant CORE-EEAT items. Reference: [CORE-EEAT Benchmark](../../references/core-eeat-benchmark.md)

    ```markdown
    ## CORE-EEAT Quick Scan

    Content-relevant items from the 80-item benchmark:

    | ID | Check Item | Status | Notes |
    |----|-----------|--------|-------|
    | C01 | Intent Alignment | ✅/⚠️/❌ | Title promise = content delivery |
    | C02 | Direct Answer | ✅/⚠️/❌ | Core answer in first 150 words |
    | C09 | FAQ Coverage | ✅/⚠️/❌ | Structured FAQ present |
    | C10 | Semantic Closure | ✅/⚠️/❌ | Conclusion answers opening |
    | O01 | Heading Hierarchy | ✅/⚠️/❌ | H1→H2→H3, no skipping |
    | O02 | Summary Box | ✅/⚠️/❌ | TL;DR or Key Takeaways |
    | O03 | Data Tables | ✅/⚠️/❌ | Comparisons in tables |
    | O05 | Schema Markup | ✅/⚠️/❌ | Appropriate JSON-LD |
    | O06 | Section Chunking | ✅/⚠️/❌ | Single topic per section |
    | R01 | Data Precision | ✅/⚠️/❌ | ≥5 precise numbers |
    | R02 | Citation Density | ✅/⚠️/❌ | ≥1 per 500 words |
    | R06 | Timestamp | ✅/⚠️/❌ | Updated <1 year |
    | R08 | Internal Link Graph | ✅/⚠️/❌ | Descriptive anchors |
    | R10 | Content Consistency | ✅/⚠️/❌ | No contradictions |
    | Exp01 | First-Person Narrative | ✅/⚠️/❌ | "I tested" or "We found" |
    | Ept01 | Author Identity | ✅/⚠️/❌ | Byline + bio present |
    | T04 | Disclosure Statements | ✅/⚠️/❌ | Affiliate links disclosed |

    **CORE-EEAT Quick Score**: [X]/17 items passing

    > For a complete 80-item audit with weighted scoring, use [content-quality-auditor](../../cross-cutting/content-quality-auditor/).
    ```

11. **Generate Audit Summary**

    ```markdown
    # On-Page SEO Audit Report
    
    **Page**: [URL]
    **Target Keyword**: [keyword]
    **Audit Date**: [date]
    
    ## Overall Score: [X]/100
    
    ```
    Score Breakdown:
    ████████░░ Title Tag: 8/10
    ██████░░░░ Meta Description: 6/10
    █████████░ Headers: 9/10
    ███████░░░ Content: 7/10
    ██████░░░░ Keywords: 6/10
    █████░░░░░ Internal Links: 5/10
    ████░░░░░░ Images: 4/10
    ████████░░ Technical: 8/10
    ```
    
    ## Priority Issues
    
    ### 🔴 Critical (Fix Immediately)
    1. [Critical issue 1]
    2. [Critical issue 2]
    
    ### 🟡 Important (Fix Soon)
    1. [Important issue 1]
    2. [Important issue 2]
    
    ### 🟢 Minor (Nice to Have)
    1. [Minor issue 1]
    2. [Minor issue 2]
    
    ## Quick Wins
    
    These changes will have immediate impact:
    
    1. **[Change 1]**: [Why and how]
    2. **[Change 2]**: [Why and how]
    3. **[Change 3]**: [Why and how]
    
    ## Detailed Recommendations
    
    ### Title Tag
    - **Current**: [current title]
    - **Recommended**: [new title]
    - **Impact**: [expected improvement]
    
    ### Meta Description
    - **Current**: [current description]
    - **Recommended**: [new description]
    - **Impact**: [expected improvement]
    
    ### Content Improvements
    1. [Specific content change with location]
    2. [Specific content change with location]
    
    ### Internal Linking
    1. Add link: "[anchor]" → [destination]
    2. Add link: "[anchor]" → [destination]
    
    ### Image Optimization
    1. [Image 1]: [change needed]
    2. [Image 2]: [change needed]
    
    ## Competitor Comparison
    
    | Element | Your Page | Top Competitor | Gap |
    |---------|-----------|----------------|-----|
    | Word count | [X] | [Y] | [+/-Z] |
    | Internal links | [X] | [Y] | [+/-Z] |
    | Images | [X] | [Y] | [+/-Z] |
    | H2 headings | [X] | [Y] | [+/-Z] |
    
    ## Action Checklist
    
    - [ ] Update title tag
    - [ ] Rewrite meta description
    - [ ] Add keyword to H1
    - [ ] Add [X] more internal links
    - [ ] Add alt text to [X] images
    - [ ] Add [X] more content sections
    - [ ] Implement FAQ schema
    - [ ] [Additional action items]
    
    ## Expected Results

    After implementing these changes:
    - Estimated ranking improvement: [X] positions
    - Estimated CTR improvement: [X]%
    - Estimated traffic increase: [X]%
    ```

## Validation Checkpoints

### Input Validation
- [ ] Target keyword(s) clearly specified by user
- [ ] Page content accessible (either via URL or provided HTML)
- [ ] If competitor comparison requested, competitor URL provided

### Output Validation
- [ ] Every recommendation cites specific data points (not generic advice)
- [ ] Scores based on measurable criteria, not subjective opinion
- [ ] All suggested changes include specific locations (title tag, H2 #3, paragraph 5, etc.)
- [ ] Source of each data point clearly stated (~~SEO tool data, user-provided, ~~web crawler, or manual review)

## Example

**User**: "Audit the on-page SEO of my blog post about 'email marketing tips'"

**Output**: [Comprehensive audit following the structure above with specific findings and recommendations]

## Audit Checklists by Page Type

### Blog Post Checklist

```markdown
- [ ] Title includes keyword and is compelling
- [ ] Meta description has keyword and CTA
- [ ] Single H1 with keyword
- [ ] H2s cover main topics
- [ ] Keyword in first 100 words
- [ ] 1,500+ words for competitive topics
- [ ] 3+ internal links with varied anchors
- [ ] Images with descriptive alt text
- [ ] FAQ section with schema
- [ ] Author bio with credentials
```

### Product Page Checklist

```markdown
- [ ] Product name in title
- [ ] Price and availability in description
- [ ] H1 is product name
- [ ] Product features in H2s
- [ ] Multiple product images with alt text
- [ ] Customer reviews visible
- [ ] Product schema implemented
- [ ] Related products linked
- [ ] Clear CTA button
```

### Landing Page Checklist

```markdown
- [ ] Keyword-optimized title
- [ ] Benefit-focused meta description
- [ ] Clear H1 value proposition
- [ ] Supporting H2 sections
- [ ] Trust signals (testimonials, logos)
- [ ] Single clear CTA
- [ ] Fast page load speed
- [ ] Mobile-optimized layout
```

## Tips for Success

1. **Prioritize issues by impact** - Fix critical issues first
2. **Compare to competitors** - See what's working for top rankings
3. **Balance optimization and readability** - Don't over-optimize
4. **Audit regularly** - Content degrades over time
5. **Test changes** - Track ranking changes after updates

## Related Skills

- [seo-content-writer](../../build/seo-content-writer/) - Create optimized content
- [technical-seo-checker](../technical-seo-checker/) - Technical SEO audit
- [meta-tags-optimizer](../../build/meta-tags-optimizer/) - Optimize meta tags
- [serp-analysis](../../research/serp-analysis/) - SERP context for audit findings
- [content-refresher](../content-refresher/) - Update existing content
- [content-quality-auditor](../../cross-cutting/content-quality-auditor/) - Full 80-item CORE-EEAT audit

