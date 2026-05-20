---
name: internal-linking-optimizer
description: Analyzes and optimizes internal link structure to improve site architecture, distribute page authority, and help search engines understand content relationships. Creates strategic internal linking plans.
---

# Internal Linking Optimizer

This skill analyzes your site's internal link structure and provides recommendations to improve SEO through strategic internal linking. It helps distribute authority, establish topical relevance, and improve crawlability.

## When to Use This Skill

- Improving site architecture for SEO
- Distributing authority to important pages
- Fixing orphan pages with no internal links
- Creating topic cluster internal link strategies
- Optimizing anchor text for SEO
- Recovering pages that have lost rankings
- Planning internal links for new content

## What This Skill Does

1. **Link Structure Analysis**: Maps current internal linking patterns
2. **Authority Flow Mapping**: Shows how PageRank flows through site
3. **Orphan Page Detection**: Finds pages with no internal links
4. **Anchor Text Optimization**: Improves anchor text diversity
5. **Topic Cluster Linking**: Creates pillar-cluster link strategies
6. **Link Opportunity Finding**: Identifies where to add links
7. **Navigation Optimization**: Improves site-wide link elements

## How to Use

### Analyze Current Structure

```
Analyze internal linking structure for [domain/sitemap]
```

```
Find internal linking opportunities for [URL]
```

### Create Linking Strategy

```
Create internal linking plan for topic cluster about [topic]
```

```
Suggest internal links for this new article: [content/URL]
```

### Fix Issues

```
Find orphan pages on [domain]
```

```
Optimize anchor text across the site
```

## Instructions

When a user requests internal linking optimization:

1. **Analyze Current Internal Link Structure**

   ```markdown
   ## Internal Link Structure Analysis
   
   ### Overview
   
   **Domain**: [domain]
   **Total Pages Analyzed**: [X]
   **Total Internal Links**: [X]
   **Average Links per Page**: [X]
   
   ### Link Distribution
   
   | Links per Page | Page Count | Percentage |
   |----------------|------------|------------|
   | 0 (Orphan) | [X] | [X]% |
   | 1-5 | [X] | [X]% |
   | 6-10 | [X] | [X]% |
   | 11-20 | [X] | [X]% |
   | 20+ | [X] | [X]% |
   
   ### Top Linked Pages
   
   | Page | Internal Links | Authority | Notes |
   |------|----------------|-----------|-------|
   | [URL 1] | [X] | High | [notes] |
   | [URL 2] | [X] | High | [notes] |
   | [URL 3] | [X] | Medium | [notes] |
   
   ### Under-Linked Important Pages
   
   | Page | Current Links | Traffic | Recommended Links |
   |------|---------------|---------|-------------------|
   | [URL 1] | [X] | [X]/mo | [X]+ |
   | [URL 2] | [X] | [X]/mo | [X]+ |
   
   **Structure Score**: [X]/10
   ```

2. **Identify Orphan Pages**

   ```markdown
   ## Orphan Page Analysis
   
   ### Definition
   Orphan pages have no internal links pointing to them, making them 
   hard for users and search engines to discover.
   
   ### Orphan Pages Found: [X]
   
   | Page | Traffic | Priority | Recommended Action |
   |------|---------|----------|-------------------|
   | [URL 1] | [X]/mo | High | Link from [pages] |
   | [URL 2] | [X]/mo | Medium | Add to navigation |
   | [URL 3] | 0 | Low | Consider deleting/redirecting |
   
   ### Fix Strategy
   
   **High Priority Orphans** (have traffic/rankings):
   1. [URL] - Add links from: [relevant pages]
   2. [URL] - Add links from: [relevant pages]
   
   **Medium Priority Orphans** (potentially valuable):
   1. [URL] - Add to category/tag page
   2. [URL] - Link from related content
   
   **Low Priority Orphans** (consider removing):
   1. [URL] - Redirect to [better page]
   2. [URL] - Delete or noindex
   ```

3. **Analyze Anchor Text Distribution**

   ```markdown
   ## Anchor Text Analysis
   
   ### Current Anchor Text Patterns
   
   **Most Used Anchors**:
   
   | Anchor Text | Count | Target Pages | Assessment |
   |-------------|-------|--------------|------------|
   | "click here" | [X] | [X] pages | ❌ Not descriptive |
   | "read more" | [X] | [X] pages | ❌ Not descriptive |
   | "[exact keyword]" | [X] | [page] | ⚠️ May be over-optimized |
   | "[descriptive phrase]" | [X] | [page] | ✅ Good |
   
   ### Anchor Text Distribution by Page
   
   **Page: [Important URL]**
   
   | Anchor Text | Source Page | Status |
   |-------------|-------------|--------|
   | "[anchor 1]" | [source URL] | ✅/⚠️/❌ |
   | "[anchor 2]" | [source URL] | ✅/⚠️/❌ |
   
   **Issues Found**:
   - Over-optimized anchors: [X] instances
   - Generic anchors: [X] instances
   - Same anchor to multiple pages: [X] instances
   
   ### Anchor Text Recommendations
   
   **For Page: [URL]**
   
   Current: "[current anchor]" used [X] times
   
   Recommended variety:
   - "[variation 1]" - Use from [page type]
   - "[variation 2]" - Use from [page type]
   - "[variation 3]" - Use from [page type]
   
   **Anchor Score**: [X]/10
   ```

4. **Create Topic Cluster Link Strategy**

   ```markdown
   ## Topic Cluster Internal Linking
   
   ### Cluster: [Main Topic]
   
   **Pillar Page**: [URL]
   **Cluster Articles**: [X]
   
   ### Current Link Map
   
   ```
   [Pillar Page]
      ├── [Cluster Article 1] ←→ [linked?]
      ├── [Cluster Article 2] ←→ [linked?]
      ├── [Cluster Article 3] ←→ [linked?]
      └── [Cluster Article 4] ←→ [linked?]
   ```
   
   ### Recommended Link Structure
   
   ```
   [Pillar Page]
      ├── Links TO all cluster articles ✅
      │
      ├── [Cluster Article 1]
      │   ├── Link TO pillar ✅
      │   └── Link TO related cluster articles
      │
      ├── [Cluster Article 2]
      │   ├── Link TO pillar ✅
      │   └── Link TO related cluster articles
      │
      └── [etc.]
   ```
   
   ### Links to Add
   
   | From Page | To Page | Anchor Text | Location |
   |-----------|---------|-------------|----------|
   | [URL 1] | [URL 2] | "[anchor]" | [paragraph/section] |
   | [URL 2] | [URL 3] | "[anchor]" | [paragraph/section] |
   | [Pillar] | [Cluster 1] | "[anchor]" | [section] |
   ```

5. **Find Contextual Link Opportunities**

   ```markdown
   ## Contextual Link Opportunities
   
   ### Link Opportunity Analysis
   
   For each page, find relevant pages to link to based on:
   - Topic relevance
   - Keyword overlap
   - User journey logic
   - Authority distribution needs
   
   ### Opportunities Found
   
   **Page: [URL 1]**
   **Topic**: [topic]
   **Current internal links**: [X]
   
   | Opportunity | Target Page | Anchor Text | Why Link |
   |-------------|-------------|-------------|----------|
   | Paragraph 2 mentions "[topic]" | [URL] | "[topic phrase]" | Topic match |
   | Section on "[subject]" | [URL] | "[anchor]" | Related guide |
   | CTA at end | [URL] | "[anchor]" | User journey |
   
   **Page: [URL 2]**
   [Continue for each page...]
   
   ### Priority Link Additions
   
   **High Impact Links** (add these first):
   
   1. **From**: [Source URL]
      **To**: [Target URL]
      **Anchor**: "[anchor text]"
      **Why**: [reason - e.g., "Target page needs authority boost"]
      **Where to add**: [specific location in content]
   
   2. **From**: [Source URL]
      **To**: [Target URL]
      [etc.]
   ```

6. **Optimize Navigation and Footer Links**

   ```markdown
   ## Site-Wide Link Optimization
   
   ### Current Navigation Analysis
   
   **Main Navigation**:
   - Links present: [list]
   - Missing important pages: [list]
   - Too many links: [Yes/No]
   
   **Footer Navigation**:
   - Links present: [list]
   - SEO value: [assessment]
   
   ### Navigation Recommendations
   
   | Element | Current | Recommended | Reason |
   |---------|---------|-------------|--------|
   | Main nav | [X] links | [Y] links | [reason] |
   | Footer | [X] links | [Y] links | [reason] |
   | Sidebar | [status] | [recommendation] | [reason] |
   | Breadcrumbs | [status] | [recommendation] | [reason] |
   
   ### Pages to Add to Navigation
   
   1. [Page] - Add to [location] because [reason]
   2. [Page] - Add to [location] because [reason]
   
   ### Pages to Remove from Navigation
   
   1. [Page] - Move to [footer/remove] because [reason]
   ```

7. **Generate Link Implementation Plan**

   ```markdown
   # Internal Linking Optimization Plan
   
   **Site**: [domain]
   **Analysis Date**: [date]
   
   ## Executive Summary
   
   - Total link opportunities found: [X]
   - Orphan pages to fix: [X]
   - Estimated traffic impact: [+X%]
   - Priority actions: [X]
   
   ## Current State
   
   | Metric | Current | Target | Gap |
   |--------|---------|--------|-----|
   | Avg links per page | [X] | [X] | [X] |
   | Orphan pages | [X] | 0 | [X] |
   | Over-optimized anchors | [X]% | <10% | [X]% |
   | Topic cluster coverage | [X]% | 100% | [X]% |
   
   ## Priority Actions
   
   ### Phase 1: Critical Fixes (Week 1)
   
   **Fix Orphan Pages**:
   - [ ] [URL] - Add links from [X] pages
   - [ ] [URL] - Add links from [X] pages
   
   **High-Value Link Additions**:
   - [ ] Link [Page A] to [Page B] with "[anchor]"
   - [ ] Link [Page A] to [Page C] with "[anchor]"
   
   ### Phase 2: Topic Clusters (Week 2-3)
   
   **Cluster 1: [Topic]**
   - [ ] Ensure pillar links to all [X] cluster articles
   - [ ] Add [X] cross-links between cluster articles
   
   **Cluster 2: [Topic]**
   - [ ] [Tasks]
   
   ### Phase 3: Optimization (Week 4+)
   
   **Anchor Text Diversity**:
   - [ ] Vary anchors for [Page] - currently [X]% exact match
   - [ ] [Additional tasks]
   
   **Navigation Updates**:
   - [ ] Add [Page] to main navigation
   - [ ] Update footer links
   
   ## Implementation Guide
   
   ### Adding Internal Links
   
   Best practices:
   1. Add links contextually within content
   2. Use descriptive anchor text (not "click here")
   3. Link to relevant, helpful pages
   4. Aim for 3-10 internal links per 1,000 words
   5. Vary anchor text for the same target
   
   ### Anchor Text Guidelines
   
   | Type | Example | Usage |
   |------|---------|-------|
   | Exact match | "keyword research" | 10-20% |
   | Partial match | "tips for keyword research" | 30-40% |
   | Branded | "Brand's guide to..." | 10-20% |
   | Natural | "this article", "learn more" | 20-30% |
   
   ## Tracking Success
   
   Monitor these metrics weekly:
   - [ ] Rankings for target keywords
   - [ ] Traffic to previously orphan pages
   - [ ] Crawl stats in Search Console
   - [ ] Internal link distribution changes
   ```

## Example

**User**: "Find internal linking opportunities for my blog post about 'email marketing best practices'"

**Output**:

```markdown
## Internal Linking Opportunities

**Page**: /blog/email-marketing-best-practices/
**Current Internal Links**: 2

### Recommended Links to Add

| Section | Text to Link | Target Page | Anchor |
|---------|--------------|-------------|--------|
| Para 2 | "building your email list" | /blog/grow-email-list/ | "building your email list" |
| Para 5 | "subject lines" | /blog/email-subject-lines/ | "write compelling subject lines" |
| Section on segmentation | "audience segments" | /blog/email-segmentation-guide/ | "segment your audience" |
| CTA section | "marketing automation" | /services/email-automation/ | "email automation services" |
| Conclusion | "email marketing tools" | /blog/best-email-tools/ | "top email marketing tools" |

### Pages That Should Link TO This Article

| Source Page | Location | Anchor Text |
|-------------|----------|-------------|
| /blog/digital-marketing-guide/ | Email section | "email marketing best practices" |
| /services/marketing-services/ | Related content | "email marketing strategies" |
| /blog/lead-generation-tips/ | Email mention | "email marketing techniques" |

### Priority Actions

1. Add 5 outbound internal links (listed above)
2. Request 3 inbound links from related pages
3. Add to "Marketing" category page
```

## Tips for Success

1. **Quality over quantity** - Add relevant links, not random ones
2. **User-first thinking** - Links should help users navigate
3. **Vary anchor text** - Avoid over-optimization
4. **Link to important pages** - Distribute authority strategically
5. **Regular audits** - Internal links need maintenance as content grows

## Related Skills

- [content-gap-analysis](../../research/content-gap-analysis/) - Find content to link to
- [seo-content-writer](../../build/seo-content-writer/) - Create linkable content
- [on-page-seo-auditor](../on-page-seo-auditor/) - Audit overall on-page SEO
- [technical-seo-checker](../technical-seo-checker/) - Check crawlability

