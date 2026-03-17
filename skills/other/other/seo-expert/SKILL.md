---
name: seo-expert
description: Эксперт SEO. Используй для поисковой оптимизации, keyword research, technical SEO и link building.
---

# SEO Expert

Deep expertise in search engine optimization including technical, on-page, and off-page SEO.

## Core Competencies

```yaml
technical_seo:
  - "Site architecture"
  - "Crawlability and indexation"
  - "Core Web Vitals"
  - "Schema markup"
  - "Mobile optimization"
  - "Site speed"

on_page_seo:
  - "Keyword research"
  - "Content optimization"
  - "Meta tags"
  - "Header structure"
  - "Internal linking"
  - "Image optimization"

off_page_seo:
  - "Link building"
  - "Digital PR"
  - "Brand mentions"
  - "Guest posting"
  - "Partnership links"
  - "Competitor analysis"
```

## Keyword Research

```yaml
keyword_research_process:
  step_1_seed:
    action: "Identify core topics"
    tools: ["Brainstorming", "Competitor analysis"]
    output: "10-20 seed keywords"

  step_2_expansion:
    action: "Expand keyword list"
    sources:
      - "Google Autocomplete"
      - "People Also Ask"
      - "Related searches"
      - "Ahrefs/SEMrush suggestions"
    output: "200-500 keyword variations"

  step_3_analysis:
    metrics:
      volume: "Monthly search volume"
      difficulty: "Keyword difficulty score"
      intent: "Informational/Commercial/Transactional"
      trend: "Rising, stable, declining"

  step_4_mapping:
    action: "Assign keywords to pages"
    rules:
      - "One primary keyword per page"
      - "3-5 secondary keywords"
      - "Group by intent"

  step_5_prioritization:
    formula: |
      Score = (Volume × Intent Weight) / Difficulty
    priority:
      high: "High volume, low difficulty, high intent"
      medium: "Moderate on all factors"
      low: "Low volume or high difficulty"

search_intent:
  types:
    informational:
      signals: ["what", "how", "why", "guide", "tutorial"]
      content: "Blog posts, guides, tutorials"
      example: "what is SEO"

    navigational:
      signals: ["brand name", "login", "site name"]
      content: "Homepage, product pages"
      example: "ahrefs login"

    commercial:
      signals: ["best", "top", "review", "comparison", "vs"]
      content: "Comparison pages, reviews"
      example: "best SEO tools 2024"

    transactional:
      signals: ["buy", "price", "discount", "coupon"]
      content: "Product pages, pricing"
      example: "buy ahrefs subscription"
```

## On-Page Optimization

```yaml
on_page_checklist:
  title_tag:
    length: "50-60 characters"
    structure: "Primary Keyword | Secondary | Brand"
    tips:
      - "Front-load primary keyword"
      - "Include power words"
      - "Make it compelling"

  meta_description:
    length: "150-160 characters"
    tips:
      - "Include primary keyword"
      - "Add call-to-action"
      - "Highlight unique value"
      - "Match search intent"

  url_structure:
    format: "/category/keyword-slug"
    rules:
      - "Short and descriptive"
      - "Include target keyword"
      - "Use hyphens, not underscores"
      - "Lowercase only"
      - "No stop words"

  headings:
    h1:
      count: "One per page"
      content: "Primary keyword variation"
    h2_h3:
      usage: "Logical content structure"
      keywords: "Include secondary keywords"

  content:
    first_100_words: "Include primary keyword"
    density: "1-2% keyword density (natural)"
    length: "Match or exceed competitors"
    format:
      - "Short paragraphs"
      - "Bullet points"
      - "Tables where appropriate"
      - "Images every 300-500 words"

  internal_linking:
    anchor_text: "Descriptive, keyword-rich"
    quantity: "3-5 internal links per 1000 words"
    strategy: "Link to relevant, important pages"

  images:
    filename: "descriptive-keyword.jpg"
    alt_text: "Descriptive, include keyword"
    compression: "WebP format preferred"
    lazy_loading: "Enable for below-fold images"

  schema_markup:
    types:
      article: "Blog posts"
      product: "E-commerce pages"
      faq: "FAQ sections"
      how_to: "Tutorial content"
      local_business: "Location pages"
```

## Technical SEO

```yaml
technical_audit:
  crawlability:
    robots_txt:
      - "Allow important pages"
      - "Block admin, duplicates"
      - "Include sitemap reference"

    xml_sitemap:
      - "Include all indexable URLs"
      - "Update automatically"
      - "Submit to Search Console"
      - "Split if >50k URLs"

    canonicalization:
      - "Self-referencing canonicals"
      - "Handle duplicate content"
      - "Consistent URL format"

  indexation:
    checks:
      - "site: search coverage"
      - "Index coverage in GSC"
      - "No unintended noindex"

    issues:
      - "Thin content"
      - "Duplicate content"
      - "Orphan pages"
      - "Redirect chains"

  site_speed:
    core_web_vitals:
      lcp:
        metric: "Largest Contentful Paint"
        target: "<2.5s"
        fixes:
          - "Optimize images"
          - "Preload critical resources"
          - "Use CDN"

      fid:
        metric: "First Input Delay"
        target: "<100ms"
        fixes:
          - "Minimize JavaScript"
          - "Use web workers"
          - "Code splitting"

      cls:
        metric: "Cumulative Layout Shift"
        target: "<0.1"
        fixes:
          - "Set image dimensions"
          - "Reserve ad space"
          - "Avoid dynamic content insertion"

    optimization:
      - "Enable compression (Gzip/Brotli)"
      - "Minify CSS/JS"
      - "Leverage browser caching"
      - "Reduce server response time"
      - "Implement lazy loading"

  mobile:
    requirements:
      - "Mobile-first indexing ready"
      - "Responsive design"
      - "Touch-friendly elements"
      - "Readable font sizes"
      - "No horizontal scrolling"

  security:
    https:
      - "SSL certificate valid"
      - "Force HTTPS redirect"
      - "No mixed content"
```

## Link Building

```yaml
link_building_strategies:
  content_marketing:
    linkable_assets:
      - "Original research/data"
      - "Comprehensive guides"
      - "Free tools/calculators"
      - "Infographics"
      - "Expert roundups"

    promotion:
      - "Outreach to industry sites"
      - "Social amplification"
      - "PR distribution"

  digital_pr:
    tactics:
      - "News hijacking"
      - "Expert commentary"
      - "Data-driven stories"
      - "Brand mentions → links"

    targets:
      - "News sites"
      - "Industry publications"
      - "Podcasts"

  guest_posting:
    process:
      - "Find relevant sites"
      - "Check domain authority"
      - "Pitch unique topics"
      - "Write quality content"
      - "Include contextual links"

    quality_criteria:
      - "DA 30+"
      - "Real traffic"
      - "Relevant niche"
      - "Editorial standards"

  broken_link_building:
    process:
      - "Find broken links on relevant sites"
      - "Create replacement content"
      - "Outreach to webmasters"

  resource_page_links:
    process:
      - "Find resource pages in niche"
      - "Create worthy resource"
      - "Request inclusion"

  competitor_analysis:
    steps:
      - "Identify top competitors"
      - "Analyze their backlinks"
      - "Find replicable opportunities"
      - "Prioritize by difficulty/value"

link_quality_factors:
  positive:
    - "High domain authority"
    - "Relevant to your niche"
    - "Editorial (earned)"
    - "Contextual placement"
    - "Followed link"
    - "Traffic-driving"

  negative:
    - "Link farms"
    - "Paid links (unnatural)"
    - "Irrelevant sites"
    - "Footer/sidebar links"
    - "Same anchor text repeatedly"
```

## SEO Analytics

```yaml
key_metrics:
  organic_traffic:
    tool: "Google Analytics 4"
    tracking: "Sessions with source/medium = organic"

  keyword_rankings:
    tools: ["Ahrefs", "SEMrush", "GSC"]
    tracking:
      - "Position changes"
      - "SERP features"
      - "Click-through rate"

  domain_authority:
    tools: ["Moz DA", "Ahrefs DR"]
    tracking: "Monthly trend"

  core_web_vitals:
    tool: "Google Search Console"
    tracking: "Pass/fail status"

  backlinks:
    tool: "Ahrefs"
    tracking:
      - "New/lost links"
      - "Referring domains"
      - "Anchor text distribution"

  click_through_rate:
    tool: "Google Search Console"
    optimization:
      - "Improve title tags"
      - "Optimize meta descriptions"
      - "Win featured snippets"

reporting:
  weekly:
    - "Ranking changes"
    - "Traffic anomalies"
    - "New backlinks"

  monthly:
    - "Traffic growth"
    - "Keyword performance"
    - "Content performance"
    - "Technical health"

  quarterly:
    - "Goal progress"
    - "Competitor analysis"
    - "Strategy review"
    - "ROI assessment"
```

## Algorithm Factors

```yaml
ranking_factors:
  content:
    - "Quality and depth"
    - "Relevance to query"
    - "Freshness"
    - "E-E-A-T signals"
    - "User satisfaction"

  technical:
    - "Page speed"
    - "Mobile friendliness"
    - "Secure (HTTPS)"
    - "Core Web Vitals"
    - "Crawlability"

  authority:
    - "Backlink quality"
    - "Backlink quantity"
    - "Brand signals"
    - "Domain age/history"

  user_signals:
    - "Click-through rate"
    - "Dwell time"
    - "Bounce rate"
    - "Pogo-sticking"

e_e_a_t:
  experience:
    signals:
      - "First-hand experience"
      - "Personal stories"
      - "Original photos"

  expertise:
    signals:
      - "Author credentials"
      - "Depth of content"
      - "Accuracy"

  authoritativeness:
    signals:
      - "Backlinks from authorities"
      - "Brand mentions"
      - "Industry recognition"

  trustworthiness:
    signals:
      - "HTTPS"
      - "Clear contact info"
      - "Privacy policy"
      - "No deceptive practices"
```

## Tools Stack

```yaml
seo_tools:
  keyword_research:
    - "Ahrefs"
    - "SEMrush"
    - "Google Keyword Planner"
    - "Ubersuggest"

  rank_tracking:
    - "Ahrefs Rank Tracker"
    - "SEMrush Position Tracking"
    - "AccuRanker"

  technical:
    - "Screaming Frog"
    - "Sitebulb"
    - "Google Search Console"
    - "PageSpeed Insights"

  backlinks:
    - "Ahrefs"
    - "Majestic"
    - "Moz Link Explorer"

  content:
    - "Clearscope"
    - "Surfer SEO"
    - "MarketMuse"

  analytics:
    - "Google Analytics 4"
    - "Google Search Console"
```

## Лучшие практики

1. **User first** — оптимизируй для людей, не только для роботов
2. **Quality content** — уникальный, полезный контент
3. **Technical foundation** — быстрый, мобильный, доступный сайт
4. **Earn links** — качество важнее количества
5. **Track everything** — данные для решений
6. **Stay updated** — алгоритмы меняются
