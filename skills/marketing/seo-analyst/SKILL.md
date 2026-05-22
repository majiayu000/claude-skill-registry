---
name: SEO Analyst
slug: seo-analyst
description: Analyze SEO performance, conduct keyword research, audit technical SEO, and develop data-driven optimization strategies
category: research
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "seo analysis"
  - "keyword research"
  - "seo audit"
  - "search optimization"
tags:
  - seo
  - search-optimization
  - keyword-research
  - technical-seo
  - content-optimization
---

# SEO Analyst

Expert SEO analysis agent that conducts comprehensive search optimization research, analyzes performance, identifies opportunities, and develops data-driven strategies. Specializes in keyword research, technical SEO audits, content optimization, competitor analysis, and ranking strategies.

This skill applies rigorous SEO methodologies, search algorithms understanding, and data analysis to improve organic search visibility and traffic. Perfect for content strategy, website optimization, competitive positioning, and organic growth.

## Core Workflows

### Workflow 1: Comprehensive SEO Audit

**Objective:** Evaluate overall SEO health and identify improvement opportunities

**Steps:**
1. **Technical SEO Audit**
   - **Crawlability & Indexability:**
     - robots.txt configuration
     - XML sitemap presence and quality
     - Canonical tags implementation
     - Noindex/nofollow usage
     - Crawl errors and blocked resources
     - Use WebSearch to check Google Search Console data patterns

   - **Site Architecture:**
     - URL structure (clean, descriptive, hierarchical)
     - Internal linking structure
     - Site depth (pages <3 clicks from homepage)
     - Orphan pages (no internal links)
     - Redirect chains and loops

   - **Page Speed & Performance:**
     - Core Web Vitals (LCP, FID, CLS)
     - Page load time
     - Mobile performance
     - Image optimization
     - Code minification and compression
     - Server response time

   - **Mobile Optimization:**
     - Mobile-friendly test results
     - Responsive design implementation
     - Mobile usability issues
     - Touch targets and spacing

   - **Security:**
     - HTTPS implementation
     - Mixed content issues
     - Security headers

2. **On-Page SEO Audit**
   - **Title Tags:**
     - Presence on all pages
     - Unique and descriptive
     - Target keyword inclusion
     - Optimal length (50-60 characters)

   - **Meta Descriptions:**
     - Presence and quality
     - Compelling and accurate
     - Optimal length (150-160 characters)

   - **Header Tags (H1, H2, H3):**
     - Proper hierarchy
     - Keyword inclusion
     - One H1 per page

   - **Content Quality:**
     - Uniqueness (no duplicate content)
     - Depth and comprehensiveness
     - Keyword optimization (not over-optimization)
     - Readability and formatting
     - Content freshness

   - **Image Optimization:**
     - Alt text presence and quality
     - File names (descriptive)
     - File size optimization
     - Image formats (WebP, etc.)

   - **Schema Markup:**
     - Structured data implementation
     - Types used (Article, Product, FAQ, etc.)
     - Validation (no errors)

3. **Off-Page SEO Audit**
   - **Backlink Profile:**
     - Total backlinks and referring domains
     - Domain authority of linking sites
     - Anchor text distribution
     - Link quality vs. spammy links
     - Toxic backlinks to disavow
     - Link velocity (growth rate)

   - **Brand Mentions:**
     - Unlinked brand mentions
     - Sentiment of mentions
     - Opportunity for link reclamation

4. **Content Audit**
   - Inventory all pages
   - Traffic by page (Google Analytics data)
   - Rankings by page
   - Content gaps (missing topics)
   - Thin content (pages with little value)
   - Outdated content
   - Cannibalization issues (multiple pages competing for same keyword)

5. **Competitive Analysis**
   - Identify top-ranking competitors
   - Compare domain authority
   - Backlink gap analysis
   - Content gap analysis
   - Keyword gap analysis

6. **Audit Summary & Prioritization**
   - Categorize issues by severity (critical, high, medium, low)
   - Estimate impact and effort
   - Prioritize quick wins vs. strategic improvements
   - Create action roadmap

**Deliverable:** Comprehensive SEO audit report with prioritized recommendations

### Workflow 2: Keyword Research & Strategy

**Objective:** Identify high-value keyword opportunities aligned with business goals

**Steps:**
1. **Seed Keyword Generation**
   - Core products/services
   - Industry terms
   - Customer language (from support, sales, reviews)
   - Competitor keywords
   - Brand and branded variations

2. **Keyword Expansion**
   - **Use Google-based research:**
     - Google Autocomplete suggestions
     - "People Also Ask" questions
     - Related searches at bottom of SERP
     - Google Trends for trending topics
   - **Topic clustering:**
     - Group keywords by theme/intent
     - Identify topic pillars

3. **Keyword Metrics Analysis**
   - **Search Volume:**
     - Monthly search volume estimates
     - Seasonality and trends
     - Growing vs. declining keywords

   - **Keyword Difficulty:**
     - Competition level (low, medium, high)
     - Domain authority of top-ranking pages
     - Number of backlinks needed to rank

   - **Search Intent:**
     - Informational (learning)
     - Navigational (finding specific site)
     - Transactional (ready to buy)
     - Commercial (researching before buying)

   - **Business Value:**
     - Alignment with offerings
     - Conversion potential
     - Customer value (high-value vs. low-value searches)

4. **Competitive Keyword Analysis**
   - Keywords competitors rank for that you don't
   - Your ranking position vs. competitors
   - Opportunities to outrank (lower difficulty, high value)
   - Gaps in competitor content

5. **Keyword Prioritization**
   - **Opportunity Score:** Search Volume × Business Value / Keyword Difficulty
   - **Quick Wins:** Medium volume, low difficulty, high relevance
   - **Strategic Targets:** High volume, medium difficulty, high relevance
   - **Long-tail Opportunities:** Low volume, low difficulty, high intent
   - **Avoid:** High difficulty with low return or irrelevant

6. **Keyword Mapping**
   - Assign primary keyword to each page
   - Assign secondary/supporting keywords
   - Identify content gaps (keywords with no target page)
   - Plan new content for gaps
   - Optimize existing pages for mapped keywords

**Deliverable:** Keyword research report with prioritized keywords and content plan

### Workflow 3: Content Optimization

**Objective:** Optimize existing content to improve rankings and traffic

**Steps:**
1. **Select Content to Optimize**
   - **High Priority Pages:**
     - Ranking 4-20 (easy to push to page 1)
     - High impressions, low CTR (improve title/description)
     - Declining traffic (refresh needed)
     - Important business pages (product, service)

2. **Analyze Top-Ranking Competitors**
   - Review top 10 results for target keyword
   - Note patterns:
     - Content length (word count)
     - Content structure (headers, sections)
     - Content depth (topics covered)
     - Media usage (images, videos)
     - Page speed and UX
     - Backlinks and authority

3. **Content Gap Analysis**
   - What do competitors cover that you don't?
   - What questions do they answer?
   - What subtopics do they include?
   - What media do they use?

4. **Optimize Content Elements**
   - **Title Tag:**
     - Include primary keyword (preferably near beginning)
     - Compelling and click-worthy
     - 50-60 characters

   - **Meta Description:**
     - Include primary keyword
     - Clear value proposition
     - Call-to-action
     - 150-160 characters

   - **URL:**
     - Short, descriptive, includes keyword
     - Avoid changing if page already indexed (redirects needed)

   - **H1:**
     - Include primary keyword
     - Compelling and descriptive
     - Only one H1 per page

   - **Headers (H2, H3):**
     - Clear structure
     - Include semantic keywords
     - Organize content logically

   - **Body Content:**
     - Include primary keyword naturally (don't overstuff)
     - Include semantic/related keywords (LSI)
     - Add missing subtopics from gap analysis
     - Improve depth and comprehensiveness
     - Enhance readability (short paragraphs, bullet points)
     - Add visuals (images, diagrams, videos)
     - Update outdated information
     - Target 1500-2500+ words for competitive topics

   - **Internal Links:**
     - Link to related content
     - Use descriptive anchor text
     - 3-5 contextual internal links

   - **Images:**
     - Optimize alt text with keywords
     - Compress file size
     - Use descriptive file names

   - **Schema Markup:**
     - Add relevant structured data
     - Article, FAQ, How-To, Product, Review, etc.

5. **Content Freshness**
   - Update publish date (if significantly refreshed)
   - Add recent examples and data
   - Note "Updated [Date]" if appropriate

6. **Post-Optimization Monitoring**
   - Track rankings for target keywords
   - Monitor traffic changes
   - Track engagement metrics (time on page, bounce rate)
   - Re-optimize if no improvement after 4-8 weeks

**Deliverable:** Content optimization plan with before/after analysis

### Workflow 4: Competitor SEO Analysis

**Objective:** Understand competitor strategies and identify opportunities

**Steps:**
1. **Identify SEO Competitors**
   - Top-ranking sites for your target keywords
   - May differ from business competitors
   - Focus on 3-5 main competitors

2. **Domain Metrics Comparison**
   - Domain Authority / Domain Rating
   - Organic traffic estimates
   - Ranking keywords count
   - Backlink profile (quantity and quality)
   - Content volume (indexed pages)

3. **Keyword Gap Analysis**
   - Keywords competitors rank for that you don't
   - Filter by:
     - Search volume (medium to high)
     - Relevance to your business
     - Keyword difficulty (achievable)
   - Prioritize opportunities

4. **Content Gap Analysis**
   - Topics and content types competitors have
   - High-traffic pages you're missing
   - Content formats (guides, tools, calculators, etc.)
   - Content depth and quality

5. **Backlink Gap Analysis**
   - Domains linking to competitors but not you
   - Link-worthy content competitors have
   - Link building strategies competitors use
   - Opportunities for outreach

6. **On-Page Strategy Analysis**
   - How competitors structure content
   - Title and description strategies
   - Internal linking patterns
   - Use of media and visuals
   - Schema markup usage

7. **Content Strategy Patterns**
   - Publishing frequency
   - Content types and formats
   - Topic themes
   - Target audience

8. **Technical SEO Comparison**
   - Site speed comparison
   - Mobile optimization
   - Security (HTTPS)
   - Structured data usage

9. **Strategic Insights**
   - What are they doing well? (learn from)
   - What are their weaknesses? (opportunities)
   - Where can you differentiate?
   - What's achievable vs. aspirational?

**Deliverable:** Competitive SEO analysis with gap analysis and opportunities

### Workflow 5: Local SEO Optimization

**Objective:** Improve local search visibility for location-based businesses

**Steps:**
1. **Google Business Profile Optimization**
   - Claim and verify listing
   - Complete all profile fields
   - Accurate NAP (Name, Address, Phone)
   - Business hours (including special hours)
   - Business categories (primary + secondary)
   - Business description with keywords
   - High-quality photos (exterior, interior, products, team)
   - Regular posts and updates
   - Respond to reviews promptly

2. **Local Citation Building**
   - NAP consistency across all directories
   - Core citations: Yelp, Facebook, Apple Maps, Bing Places
   - Industry-specific directories
   - Local directories and chambers
   - Audit existing citations for accuracy

3. **Review Management**
   - Encourage customer reviews
   - Respond to all reviews (positive and negative)
   - Address negative reviews professionally
   - Highlight positive reviews on website
   - Track review sentiment and themes

4. **Local Content Optimization**
   - Location pages for each location
   - Local keywords (city, neighborhood names)
   - Location-specific content (events, news, community)
   - Embed Google Map on contact page
   - Local schema markup (LocalBusiness)

5. **Local Link Building**
   - Local news and blogs
   - Chamber of commerce and associations
   - Local sponsorships and partnerships
   - Community involvement (events, charities)
   - Local resource pages

6. **Mobile Optimization**
   - Mobile-friendly design
   - Click-to-call buttons
   - Easy-to-find address and hours
   - Fast mobile page speed
   - Mobile-specific local schema

**Deliverable:** Local SEO optimization plan with citation and review strategy

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Full SEO audit | "Conduct comprehensive SEO audit for [website]" |
| Keyword research | "Find keyword opportunities for [topic/industry]" |
| Optimize content | "How should I optimize [page] for SEO?" |
| Competitor analysis | "Analyze SEO strategy of [competitor]" |
| Technical audit | "Audit technical SEO for [website]" |
| Local SEO plan | "Create local SEO strategy for [business]" |

## SEO Best Practices

### Content Creation
- **Quality over quantity:** 10 great pages > 100 mediocre pages
- **Target user intent:** Match content to what searchers want
- **Comprehensive coverage:** Be the best result for the query
- **Original insights:** Don't just rehash what others say
- **Regular updates:** Keep content fresh and accurate
- **Natural keyword use:** Write for humans first, search engines second

### Technical SEO
- **Fast page speed:** Core Web Vitals matter
- **Mobile-first:** Google uses mobile version for indexing
- **Clean URLs:** Descriptive, short, keyword-rich
- **Logical site structure:** Easy to navigate and crawl
- **HTTPS:** Security is a ranking factor
- **Fix errors promptly:** Monitor Search Console regularly

### Link Building
- **Quality over quantity:** One great link > 10 spammy links
- **Relevant sources:** Links from topically related sites
- **Natural anchor text:** Vary anchor text, avoid over-optimization
- **Earn links:** Create link-worthy content
- **Avoid schemes:** No buying links, link exchanges, or PBNs

### Avoid These Pitfalls
- **Keyword stuffing:** Unnatural overuse of keywords
- **Duplicate content:** Same content on multiple pages
- **Thin content:** Pages with little value
- **Cloaking:** Showing different content to search engines vs. users
- **Hidden text:** White text on white background, etc.
- **Paid links without nofollow:** Violates Google guidelines
- **Auto-generated content:** Low-quality, spun content
- **Doorway pages:** Pages created only for search engines

## SEO Metrics to Track

### Organic Traffic Metrics
- **Organic Sessions:** Total visits from search
- **Organic Users:** Unique visitors from search
- **Landing Pages:** Which pages receive traffic
- **Traffic by Device:** Desktop, mobile, tablet
- **Traffic by Location:** Geographic distribution

### Ranking Metrics
- **Keyword Rankings:** Position for target keywords
- **Ranking Distribution:** How many keywords in top 3, top 10, etc.
- **SERP Features:** Featured snippets, People Also Ask, etc.
- **Visibility Score:** Overall search visibility

### Engagement Metrics
- **Bounce Rate:** % of single-page sessions
- **Pages per Session:** Depth of engagement
- **Average Session Duration:** Time on site
- **Pageviews:** Total pages viewed

### Conversion Metrics
- **Organic Conversions:** Goals completed from search traffic
- **Conversion Rate:** % of organic visitors who convert
- **Assisted Conversions:** Organic's role in multi-touch conversions
- **Revenue from Organic:** Direct attribution

### Technical Metrics
- **Core Web Vitals:** LCP, FID, CLS scores
- **Page Speed:** Load time, Time to Interactive
- **Crawl Errors:** Issues Googlebot encountered
- **Index Coverage:** Pages indexed vs. excluded

### Authority Metrics
- **Backlinks:** Total number of backlinks
- **Referring Domains:** Number of unique linking domains
- **Domain Authority:** Third-party authority score
- **Anchor Text Distribution:** Diversity of link anchor text

## SEO Audit Report Template

```markdown
# SEO Audit Report: [Website]

**Date:** [Audit Date]
**Analyst:** Claude SEO Analyst
**Scope:** [Pages audited, depth of audit]

## Executive Summary
- **Overall Health:** [Good/Fair/Poor]
- **Critical Issues:** X
- **High Priority:** X
- **Quick Wins:** X
- **Estimated Impact:** [Description]

## Current Performance
- **Organic Traffic:** [Monthly sessions]
- **Ranking Keywords:** [Count]
- **Domain Authority:** [Score]
- **Top Ranking Pages:** [List]

## Technical SEO

### Critical Issues
1. **[Issue]**
   - Impact: [High/Medium/Low]
   - Pages Affected: X
   - Fix: [Specific action]

### Site Architecture
- [Finding]

### Page Speed
- **Desktop Score:** [X/100]
- **Mobile Score:** [X/100]
- **Issues:** [List]

### Mobile Optimization
- [Finding]

## On-Page SEO

### Title Tags
- **Missing:** X pages
- **Duplicate:** X pages
- **Too Long/Short:** X pages

### Meta Descriptions
- **Missing:** X pages
- **Duplicate:** X pages

### Content Issues
- **Thin Content:** X pages (<300 words)
- **Duplicate Content:** X instances
- **Missing H1:** X pages

## Off-Page SEO

### Backlink Profile
- **Total Backlinks:** X
- **Referring Domains:** X
- **Domain Authority:** X
- **Toxic Links:** X (need disavow)

### Top Linking Domains
1. [Domain] - [DR score]
2. [Domain] - [DR score]

## Competitive Analysis
- **Competitor 1:** [Strengths vs. you]
- **Competitor 2:** [Strengths vs. you]

## Keyword Opportunities
1. **[Keyword]** - Volume: X | Difficulty: X | Opportunity: [High/Med/Low]
2. **[Keyword]** - Volume: X | Difficulty: X | Opportunity: [High/Med/Low]

## Priority Recommendations

### Quick Wins (0-2 weeks)
1. [Action] - Impact: [High/Med/Low]
2. [Action] - Impact: [High/Med/Low]

### Short-term (1-3 months)
1. [Action] - Impact: [High/Med/Low]
2. [Action] - Impact: [High/Med/Low]

### Long-term (3-6 months)
1. [Action] - Impact: [High/Med/Low]
2. [Action] - Impact: [High/Med/Low]

## Appendix
- Detailed issue list
- Affected URLs
- Technical specifications
```

## Integration with Other Skills

- **Use with `competitive-intelligence`:** Deep competitive SEO analysis
- **Use with `market-research-analyst`:** Keyword research for market validation
- **Use with `content-publishing`:** SEO-optimized content creation
- **Use with `data-analyzer`:** Advanced analytics on SEO data
- **Use with `trend-spotter`:** Identify emerging search trends

## Tools & Data Sources

- **Google Search Console:** Performance data, index coverage, issues
- **Google Analytics:** Traffic, engagement, conversions
- **Google PageSpeed Insights:** Core Web Vitals, performance
- **Google Trends:** Search volume trends, seasonality
- **Manual SERP analysis:** Review top-ranking pages directly
