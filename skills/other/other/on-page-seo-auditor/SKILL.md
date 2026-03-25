---
name: on-page-seo-auditor
version: "4.0.0"
description: 'Audit on-page HTML elements including title tags, headers, image alt text, and internal links with a scored SEO report. Use when the user asks to "audit page SEO", "on-page SEO check", "SEO score", "page optimization", "what SEO issues does this page have", "score my page", "why is this page not ranking", or "check my page". For server, speed, and crawl issues, see technical-seo-checker. For full EEAT content quality scoring, see content-quality-auditor.'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
allowed-tools: WebFetch
metadata:
  author: aaron-he-zhu
  version: "4.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - on-page audit
    - page optimization
    - seo audit
    - content optimization
    - header tags
    - image optimization
    - seo score
    - page-audit
    - seo-score
    - on-page-optimization
    - optimization-checklist
    - seo-checklist
    - page-score
    - h1-optimization
    - meta-audit
    - content-audit
  triggers:
    - "audit page SEO"
    - "on-page SEO check"
    - "SEO score"
    - "page optimization"
    - "what SEO issues"
    - "check my page"
    - "on-page audit"
    - "what's wrong with this page's SEO"
    - "score my page"
    - "why isn't this page ranking"
---

# On-Page SEO Auditor


> **[SEO & GEO Skills Library](https://github.com/aaron-he-zhu/seo-geo-claude-skills)** · 20 skills for SEO + GEO · [ClawHub](https://clawhub.ai/u/aaron-he-zhu) · [skills.sh](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)

<details>
<summary>Browse all 20 skills</summary>

**Research** · [keyword-research](../../research/keyword-research/) · [competitor-analysis](../../research/competitor-analysis/) · [serp-analysis](../../research/serp-analysis/) · [content-gap-analysis](../../research/content-gap-analysis/)

**Build** · [seo-content-writer](../../build/seo-content-writer/) · [geo-content-optimizer](../../build/geo-content-optimizer/) · [meta-tags-optimizer](../../build/meta-tags-optimizer/) · [schema-markup-generator](../../build/schema-markup-generator/)

**Optimize** · **on-page-seo-auditor** · [technical-seo-checker](../technical-seo-checker/) · [internal-linking-optimizer](../internal-linking-optimizer/) · [content-refresher](../content-refresher/)

**Monitor** · [rank-tracker](../../monitor/rank-tracker/) · [backlink-analyzer](../../monitor/backlink-analyzer/) · [performance-reporter](../../monitor/performance-reporter/) · [alert-manager](../../monitor/alert-manager/)

**Cross-cutting** · [content-quality-auditor](../../cross-cutting/content-quality-auditor/) · [domain-authority-auditor](../../cross-cutting/domain-authority-auditor/) · [entity-optimizer](../../cross-cutting/entity-optimizer/) · [memory-management](../../cross-cutting/memory-management/)

</details>

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

5. **Audit Content Quality** — Word count, reading level, comprehensiveness, formatting, E-E-A-T signals, content elements checklist, gap identification

   > **Reference**: See [references/audit-templates.md](./references/audit-templates.md) for the content quality template (Step 5).

6. **Audit Keyword Usage** — Primary/secondary keyword placement across all page elements, LSI/related terms, density analysis

   > **Reference**: See [references/audit-templates.md](./references/audit-templates.md) for the keyword optimization template (Step 6).

7. **Audit Internal Links** — Link count, anchor text relevance, broken links, recommended additions

   > **Reference**: See [references/audit-templates.md](./references/audit-templates.md) for the internal linking template (Step 7).

8. **Audit Images** — Alt text, file names, sizes, formats, lazy loading

   > **Reference**: See [references/audit-templates.md](./references/audit-templates.md) for the image optimization template (Step 8).

9. **Audit Technical On-Page Elements** — URL, canonical, mobile, speed, HTTPS, schema

   > **Reference**: See [references/audit-templates.md](./references/audit-templates.md) for the technical on-page template (Step 9).

10. **CORE-EEAT Content Quality Quick Scan** — 17 on-page-relevant items from the 80-item CORE-EEAT benchmark

    > **Reference**: See [references/audit-templates.md](./references/audit-templates.md) for the CORE-EEAT quick scan template (Step 10). Full benchmark: [CORE-EEAT Benchmark](../../references/core-eeat-benchmark.md).

11. **Generate Audit Summary** — Overall score with visual breakdown, priority issues (critical/important/minor), quick wins, detailed recommendations, competitor comparison, action checklist, expected results

    > **Reference**: See [references/audit-templates.md](./references/audit-templates.md) for the full audit summary template (Step 11).

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

> **Reference**: See [references/audit-example.md](./references/audit-example.md) for a full worked example (noise-cancelling headphones audit) and page-type checklists (blog post, product page, landing page).

## Tips for Success

1. **Prioritize issues by impact** - Fix critical issues first
2. **Compare to competitors** - See what's working for top rankings
3. **Balance optimization and readability** - Don't over-optimize
4. **Audit regularly** - Content degrades over time
5. **Test changes** - Track ranking changes after updates

> **Scoring details**: For the complete weight distribution, scoring scale, issue resolution playbook, and industry benchmarks, see [references/scoring-rubric.md](./references/scoring-rubric.md).

## Reference Materials

- [Scoring Rubric](./references/scoring-rubric.md) — Detailed scoring criteria, weight distribution, and grade boundaries for on-page audits
- [Audit Templates](./references/audit-templates.md) — Detailed output templates for steps 5-11 (content quality, keywords, links, images, technical, CORE-EEAT scan, audit summary)
- [Audit Example & Checklists](./references/audit-example.md) — Full worked example and page-type checklists (blog, product, landing page)

## Related Skills

- [seo-content-writer](../../build/seo-content-writer/) — Create optimized content
- [technical-seo-checker](../technical-seo-checker/) — Technical SEO audit
- [meta-tags-optimizer](../../build/meta-tags-optimizer/) — Optimize meta tags
- [serp-analysis](../../research/serp-analysis/) — SERP context for audit findings
- [content-refresher](../content-refresher/) — Update existing content
- [content-quality-auditor](../../cross-cutting/content-quality-auditor/) — Full 80-item CORE-EEAT audit
- [internal-linking-optimizer](../internal-linking-optimizer/) — Optimize internal link structure
- [schema-markup-generator](../../build/schema-markup-generator/) — Validate and generate schema markup

