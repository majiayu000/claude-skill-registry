---
name: seo-strategist
description: Strategic SEO planning and analysis toolkit for site-wide optimization,
  keyword research, technical SEO audits, and competitive positioning. Complements
  content-creator's on-page SEO with strategic pl
---

---

# === CORE IDENTITY ===
name: seo-strategist
title: SEO Strategist Skill Package
description: Strategic SEO planning and analysis toolkit for site-wide optimization, keyword research, technical SEO audits, and competitive positioning. Complements content-creator's on-page SEO with strategic planning, topic cluster architecture, and SEO roadmap generation. Use for keyword strategy, technical SEO audits, SERP analysis, site architecture planning, or when user mentions SEO strategy, keyword research, technical SEO, or search rankings.
domain: marketing
subdomain: search-marketing

# === WEBSITE DISPLAY ===
difficulty: intermediate
time-saved: "60%+ faster SEO strategy development"
frequency: Weekly/Monthly for strategy, daily for monitoring
use-cases:
  - Developing comprehensive keyword strategies and topic clusters
  - Performing technical SEO audits and site health analysis
  - Analyzing competitor SERP positioning and opportunities
  - Creating SEO roadmaps with prioritized action items
  - Planning site architecture for optimal crawlability
  - Generating internal linking strategy recommendations

# === RELATIONSHIPS ===
related-agents:
  - cs-seo-strategist
  - cs-content-creator
  - cs-demand-gen-specialist
related-skills:
  - marketing-team/content-creator
  - marketing-team/marketing-demand-acquisition
related-commands: []
orchestrated-by:
  - cs-seo-strategist

# === TECHNICAL ===
dependencies:
  scripts:
    - keyword_researcher.py
    - technical_seo_auditor.py
    - seo_roadmap_generator.py
  references:
    - seo_strategy_framework.md
    - technical_seo_guide.md
    - competitive_seo_analysis.md
  assets:
    - keyword_research_template.md
    - seo_audit_checklist.md
    - seo_roadmap_template.md
compatibility:
  python-version: 3.8+
  platforms: [macos, linux, windows]
tech-stack:
  - Python 3.8+
  - JSON/CSV data processing
  - HTML parsing
  - SEO frameworks
  python-tools:
    - keyword_researcher.py
    - technical_seo_auditor.py
    - seo_roadmap_generator.py

# === EXAMPLES ===
examples:
  - title: Keyword Research & Clustering
    input: "python scripts/keyword_researcher.py keywords.csv --cluster --output json"
    output: "Topic clusters with priority scores and content recommendations"
  - title: Technical SEO Audit
    input: "python scripts/technical_seo_auditor.py https://example.com --depth 3"
    output: "Technical SEO score, crawlability issues, and recommendations"
  - title: SEO Roadmap Generation
    input: "python scripts/seo_roadmap_generator.py audit-results.json --quarters 4"
    output: "Prioritized quarterly SEO roadmap with KPIs"

# === ANALYTICS ===
stats:
  downloads: 0
  stars: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-12-16
updated: 2025-12-16
license: MIT

# === DISCOVERABILITY ===
tags: [seo, strategy, keywords, technical-seo, search-marketing]
featured: false
verified: true
---

# SEO Strategist

Strategic SEO planning toolkit for site-wide optimization, keyword research, technical audits, and competitive analysis. Complements content-creator's on-page SEO with strategic, site-level planning.

## Overview

This skill provides automated tools and expert frameworks for developing comprehensive SEO strategies that go beyond individual content optimization. While content-creator focuses on optimizing individual pieces of content, seo-strategist handles the strategic layer: keyword research, topic clusters, technical SEO audits, competitive analysis, and roadmap planning.

**Core Value:** Save 60%+ time on SEO strategy development while improving search visibility by 40% through systematic, data-driven planning.

**Relationship to content-creator:**
- **content-creator** = On-page SEO (single article optimization, keyword density, meta tags)
- **seo-strategist** = Strategic SEO (site-wide strategy, keyword research, technical audits, roadmaps)

## Core Capabilities

- **Keyword Research & Clustering** - Analyze keyword lists, create topic clusters, map to content pillars
- **Technical SEO Audits** - Crawlability, indexation, site structure, Core Web Vitals assessment
- **Competitive Analysis** - SERP position tracking, content gap analysis, competitor benchmarking
- **SEO Roadmap Planning** - Prioritized action items, quarterly planning, resource estimation
- **Site Architecture** - Internal linking strategy, URL structure, information architecture
- **Performance Monitoring** - KPI tracking, ranking reports, progress dashboards

## Quick Start

### Keyword Research
```bash
# Analyze and cluster keywords
python scripts/keyword_researcher.py keywords.csv --cluster

# Generate topic clusters with priorities
python scripts/keyword_researcher.py keywords.csv --cluster --output json > clusters.json
```

### Technical SEO Audit
```bash
# Audit local site files
python scripts/technical_seo_auditor.py ./site-export/ --output text

# Analyze with specific checks
python scripts/technical_seo_auditor.py ./site-export/ --checks all --output json
```

### SEO Roadmap
```bash
# Generate quarterly roadmap from audit
python scripts/seo_roadmap_generator.py audit-results.json --quarters 4

# Quick wins focus
python scripts/seo_roadmap_generator.py audit-results.json --quick-wins --output md
```

### Access Frameworks
- SEO Strategy: `references/seo_strategy_framework.md`
- Technical SEO: `references/technical_seo_guide.md`
- Competitive Analysis: `references/competitive_seo_analysis.md`

## Key Workflows

### 1. Keyword Strategy Development

**Time:** 4-6 hours

1. **Gather seed keywords** - Compile initial keyword list from business goals, competitors, brainstorming
2. **Expand keyword list** - Add variations, long-tail keywords, question-based queries
3. **Cluster keywords** - Run keyword_researcher.py to group by topic
   ```bash
   python scripts/keyword_researcher.py keywords.csv --cluster --min-cluster-size 3
   ```
4. **Analyze clusters** - Review topic clusters, identify content pillars
5. **Map to content** - Assign clusters to existing or planned content
6. **Prioritize** - Score by search volume, competition, business value
7. **Document strategy** - Use keyword_research_template.md

See [seo_strategy_framework.md](references/seo_strategy_framework.md) for detailed methodology.

### 2. Technical SEO Audit

**Time:** 3-4 hours

1. **Export site data** - Download HTML files or use sitemap
2. **Run technical audit** - Execute technical_seo_auditor.py
   ```bash
   python scripts/technical_seo_auditor.py ./site-export/ --checks all --output json > audit.json
   ```
3. **Review findings** - Analyze crawlability, indexation, structure issues
4. **Prioritize fixes** - Categorize by impact and effort
5. **Create action plan** - Document fixes with owners and deadlines
6. **Validate fixes** - Re-run audit after implementations

See [technical_seo_guide.md](references/technical_seo_guide.md) for checklist.

### 3. Competitive SEO Analysis

**Time:** 4-5 hours

1. **Identify competitors** - List 5-10 SERP competitors for target keywords
2. **Gather competitor data** - Export competitor sitemaps, content lists
3. **Analyze keyword overlap** - Compare keyword targeting
4. **Identify content gaps** - Find topics competitors rank for that you don't
5. **Benchmark technical SEO** - Compare site structure, page speed
6. **Document opportunities** - Create competitive positioning report

See [competitive_seo_analysis.md](references/competitive_seo_analysis.md) for framework.

### 4. SEO Roadmap Creation

**Time:** 2-3 hours

1. **Compile audit findings** - Gather technical audit results, keyword research
2. **Score opportunities** - Use impact/effort matrix
3. **Generate roadmap** - Run seo_roadmap_generator.py
   ```bash
   python scripts/seo_roadmap_generator.py audit.json --quarters 4 --output md
   ```
4. **Define KPIs** - Set measurable targets for each quarter
5. **Assign resources** - Estimate hours and owners for each initiative
6. **Present plan** - Review with stakeholders, adjust priorities

## Python Tools

### keyword_researcher.py

Keyword research, clustering, and content mapping tool.

**Key Features:**
- Keyword clustering by semantic similarity
- Topic pillar identification
- Search intent classification
- Priority scoring (volume x competition x relevance)
- Content gap analysis
- Export to JSON, CSV, Markdown

**Common Usage:**
```bash
# Basic clustering
python scripts/keyword_researcher.py keywords.csv --cluster

# With priority scoring
python scripts/keyword_researcher.py keywords.csv --cluster --score --output json

# Content mapping
python scripts/keyword_researcher.py keywords.csv --map-content content-inventory.csv

# Help
python scripts/keyword_researcher.py --help
```

### technical_seo_auditor.py

Technical SEO site audit and health assessment.

**Key Features:**
- Crawlability analysis (robots.txt, sitemap.xml)
- Indexation checks (canonical tags, noindex)
- Site structure evaluation (heading hierarchy, internal links)
- Performance indicators (page size, resource count)
- Structured data validation
- SEO score (0-100)

**Common Usage:**
```bash
# Full audit
python scripts/technical_seo_auditor.py ./site-export/ --checks all

# Specific checks
python scripts/technical_seo_auditor.py ./site-export/ --checks crawlability,structure

# JSON output for roadmap
python scripts/technical_seo_auditor.py ./site-export/ --output json > audit.json

# Help
python scripts/technical_seo_auditor.py --help
```

### seo_roadmap_generator.py

SEO roadmap and prioritization tool.

**Key Features:**
- Impact/effort prioritization matrix
- Quick wins identification
- Quarterly planning
- Resource estimation
- KPI target setting
- Markdown and JSON output

**Common Usage:**
```bash
# Generate quarterly roadmap
python scripts/seo_roadmap_generator.py audit.json --quarters 4

# Focus on quick wins
python scripts/seo_roadmap_generator.py audit.json --quick-wins

# Markdown report
python scripts/seo_roadmap_generator.py audit.json --output md > roadmap.md

# Help
python scripts/seo_roadmap_generator.py --help
```

## Reference Guides

### When to Use Each Reference

**[seo_strategy_framework.md](references/seo_strategy_framework.md)** - Strategic planning
- Pillar-Cluster content model
- Keyword research methodology (seed → expand → cluster → prioritize)
- SEO maturity assessment framework
- Search intent classification (informational, navigational, transactional, commercial)
- SERP feature targeting strategies

**[technical_seo_guide.md](references/technical_seo_guide.md)** - Technical implementation
- Crawlability checklist (robots.txt, XML sitemaps, crawl budget)
- Indexation management (canonical tags, noindex, pagination)
- Core Web Vitals optimization (LCP, FID, CLS)
- Structured data/schema markup guide
- Mobile-first indexing requirements
- Site architecture best practices

**[competitive_seo_analysis.md](references/competitive_seo_analysis.md)** - Competitive intelligence
- Competitor identification framework
- SERP analysis methodology
- Content gap analysis process
- Backlink profile comparison
- Keyword overlap analysis
- Competitive positioning strategies

## Best Practices

### Quality Standards
- Technical SEO score: 80+ (good), 90+ (excellent)
- Keyword cluster size: 5-15 keywords per cluster
- Content coverage: 80%+ of priority keywords mapped
- Roadmap timeline: Quarterly with monthly milestones
- Quick wins: 3-5 items completable within 2 weeks

### Common Pitfalls to Avoid
- Targeting keywords without search intent analysis
- Ignoring technical SEO in favor of content-only focus
- Creating content without cluster/pillar strategy
- Not tracking competitor movements
- Focusing on vanity metrics instead of business impact
- Over-optimizing for search engines at expense of users

## Performance Metrics

**Organic Search Metrics:**
- Organic traffic growth (target: 15-25% quarterly)
- Keyword rankings (track top 10, top 3 positions)
- Click-through rate from SERPs (target: 3-5% average)
- Impressions growth (leading indicator)

**Technical SEO Metrics:**
- Core Web Vitals scores (all green)
- Crawl errors (target: 0 critical)
- Index coverage ratio (target: 95%+)
- Mobile usability score (target: 100)

**Business Metrics:**
- Organic conversion rate (target: 2-5%)
- Organic revenue/leads
- Cost per organic acquisition
- SEO ROI (organic value vs. investment)

## Integration with content-creator

This skill works alongside content-creator in a complementary workflow:

1. **seo-strategist**: Keyword research → Topic clusters → Content priorities
2. **content-creator**: Write content → On-page SEO → Brand voice
3. **seo-strategist**: Technical audit → Site structure → Internal linking
4. **content-creator**: Content optimization → Meta tags → Readability

**Handoff Points:**
- seo-strategist provides keyword targets → content-creator optimizes content
- content-creator identifies content gaps → seo-strategist validates with data
- seo-strategist audits site → content-creator updates existing content

## Additional Resources

- **Templates** - See `assets/` directory
- **Strategy framework** - See [seo_strategy_framework.md](references/seo_strategy_framework.md)
- **Technical checklist** - See [technical_seo_guide.md](references/technical_seo_guide.md)
- **Competitive analysis** - See [competitive_seo_analysis.md](references/competitive_seo_analysis.md)
