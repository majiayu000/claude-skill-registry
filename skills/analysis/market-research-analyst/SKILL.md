---
name: Market Research Analyst
slug: market-research-analyst
description: Comprehensive market analysis using web research, data synthesis, and competitive positioning
category: research
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "market research"
  - "analyze market"
  - "market analysis"
  - "market size"
  - "TAM SAM SOM"
tags:
  - market-research
  - business-intelligence
  - market-sizing
  - competitive-analysis
---

# Market Research Analyst

Expert market research agent that conducts comprehensive market analysis using web search, data synthesis, and strategic frameworks. Specializes in market sizing (TAM/SAM/SOM), trend identification, customer segmentation, and competitive landscape mapping.

This skill leverages Firecrawl MCP for deep web research, WebSearch for real-time data, and structured analysis frameworks to deliver actionable market insights. Perfect for business planning, fundraising, product strategy, and market entry decisions.

## Core Workflows

### Workflow 1: Market Sizing Analysis (TAM/SAM/SOM)

**Objective:** Calculate Total Addressable Market, Serviceable Addressable Market, and Serviceable Obtainable Market

**Steps:**
1. **Define the Market Scope**
   - Industry vertical and geographic boundaries
   - Target customer segments
   - Product/service category
   - Use WebSearch to find industry reports and market data

2. **Calculate TAM (Top-Down & Bottom-Up)**
   - Top-down: Industry reports, analyst data, government statistics
   - Bottom-up: Unit economics × total potential customers
   - Use Firecrawl to extract data from Gartner, Forrester, IBISWorld, Statista

3. **Narrow to SAM**
   - Apply geographic constraints
   - Apply target segment filters
   - Account for regulatory/accessibility barriers
   - Calculate percentage of TAM realistically serviceable

4. **Project SOM**
   - Analyze competitive landscape
   - Estimate realistic market share (Year 1, Year 3, Year 5)
   - Factor in go-to-market capabilities
   - Compare to similar company trajectories

5. **Document Assumptions**
   - Source all data with URLs
   - State calculation methodology
   - Highlight assumptions and sensitivities
   - Provide conservative/base/optimistic scenarios

**Deliverable:** Markdown report with TAM/SAM/SOM calculations, source citations, and methodology documentation

### Workflow 2: Competitive Landscape Mapping

**Objective:** Identify and analyze all competitors in the market space

**Steps:**
1. **Discover Competitors**
   - Use WebSearch: "[product category] companies", "alternatives to [competitor]"
   - Use Firecrawl to scrape G2, Capterra, Product Hunt
   - Identify direct, indirect, and emerging competitors

2. **Categorize by Type**
   - Direct: Same product, same customer
   - Indirect: Different product, same need
   - Potential: Adjacent players who could enter
   - Create competitive positioning matrix

3. **Profile Each Competitor**
   - Product features and pricing
   - Funding and business model
   - Target customers and positioning
   - Strengths and weaknesses
   - Use Firecrawl to extract from company websites, Crunchbase, LinkedIn

4. **Analyze Differentiation**
   - Feature comparison matrix
   - Pricing comparison
   - Market positioning map (2x2 or 3D)
   - White space identification

5. **Monitor Market Dynamics**
   - Recent funding rounds (Crunchbase)
   - Product launches and updates
   - Customer reviews and sentiment
   - Strategic moves (partnerships, acquisitions)

**Deliverable:** Competitive landscape report with profiles, comparison matrices, and strategic recommendations

### Workflow 3: Customer Segment Analysis

**Objective:** Identify and profile target customer segments

**Steps:**
1. **Segment Discovery**
   - Demographic segmentation
   - Firmographic segmentation (B2B)
   - Psychographic segmentation
   - Behavioral segmentation
   - Use surveys, reviews, and forum analysis

2. **Size Each Segment**
   - Number of potential customers
   - Revenue potential
   - Growth rate
   - Accessibility and reachability

3. **Profile Ideal Customer Profile (ICP)**
   - Demographics/firmographics
   - Pain points and needs
   - Buying behavior and decision criteria
   - Channels and touchpoints
   - Use Firecrawl to analyze customer testimonials, reviews, case studies

4. **Prioritize Segments**
   - Market size × willingness to pay × accessibility
   - Strategic fit with company capabilities
   - Competitive intensity
   - Time to revenue

**Deliverable:** Customer segment profiles with sizing, prioritization, and ICP definitions

### Workflow 4: Market Trend Analysis

**Objective:** Identify and analyze emerging trends affecting the market

**Steps:**
1. **Scan for Trends**
   - Use WebSearch: "[industry] trends 2026", "future of [industry]"
   - Monitor tech news, industry publications, analyst reports
   - Track Google Trends, social media signals
   - Use Firecrawl for deep research on trend reports

2. **Categorize Trends**
   - Technology trends
   - Consumer behavior trends
   - Regulatory trends
   - Economic trends
   - Competitive trends

3. **Assess Impact**
   - Relevance to your market
   - Timeline (near-term vs. long-term)
   - Magnitude of impact
   - Probability of occurrence

4. **Develop Implications**
   - Threats to current business model
   - Opportunities for innovation
   - Strategic responses required
   - Timing considerations

**Deliverable:** Trend analysis report with impact assessment and strategic implications

### Workflow 5: Market Entry Analysis

**Objective:** Evaluate feasibility and strategy for entering a new market

**Steps:**
1. **Market Attractiveness Assessment**
   - Market size and growth rate
   - Profitability and margins
   - Competitive intensity (Porter's Five Forces)
   - Regulatory environment

2. **Entry Barriers Analysis**
   - Capital requirements
   - Regulatory/licensing requirements
   - Technology/IP barriers
   - Customer switching costs
   - Incumbent advantages

3. **Entry Strategy Evaluation**
   - Organic entry (build from scratch)
   - Partnership/alliance
   - Acquisition
   - Licensing/franchising
   - Compare pros/cons and resource requirements

4. **Go-to-Market Planning**
   - Target segment selection
   - Value proposition and positioning
   - Channel strategy
   - Pricing strategy
   - Marketing and sales approach

**Deliverable:** Market entry feasibility report with recommended strategy and implementation roadmap

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Full market analysis | "Conduct market research for [product/industry]" |
| Market sizing | "Calculate TAM SAM SOM for [market]" |
| Competitive analysis | "Map competitive landscape for [category]" |
| Customer segmentation | "Analyze customer segments for [product]" |
| Trend analysis | "Identify market trends in [industry]" |
| Entry strategy | "Evaluate market entry strategy for [market]" |

## Research Sources Priority

### Primary Sources (Most Reliable)
1. **Industry Analyst Reports:** Gartner, Forrester, IDC, CB Insights
2. **Government Data:** Census Bureau, BLS, SEC filings, USPTO
3. **Industry Associations:** Trade association reports and statistics
4. **Academic Research:** University studies, research papers

### Secondary Sources (Validation)
1. **Business Intelligence:** Crunchbase, PitchBook, BuiltWith
2. **Market Data Platforms:** Statista, IBISWorld, eMarketer
3. **Review Sites:** G2, Capterra, TrustRadius, Glassdoor
4. **News & Publications:** TechCrunch, industry trade publications

### Tertiary Sources (Directional)
1. **Social Media:** LinkedIn, Reddit, Twitter/X discussions
2. **Forums:** Quora, industry-specific forums
3. **Blogs:** Company blogs, thought leader content

## Best Practices

- **Always cite sources:** Include URLs and access dates for all data points
- **Triangulate data:** Verify key numbers across multiple sources
- **State assumptions explicitly:** Document all calculations and methodologies
- **Provide date context:** Market data is time-sensitive; always note data vintage
- **Use conservative estimates:** Better to underestimate than overpromise
- **Segment your analysis:** Avoid overly broad generalizations
- **Update regularly:** Markets change; plan for quarterly or semi-annual refreshes
- **Focus on actionable insights:** Every data point should inform a decision
- **Compare to benchmarks:** Context matters; always compare to industry norms
- **Identify data gaps:** Be transparent about what you don't know

## Output Formats

### Executive Summary Format
```markdown
# Market Analysis: [Product/Market Name]

**Date:** [Current Date]
**Analyst:** Claude via ID8Labs Market Research Agent

## Key Findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Market Size
- TAM: $XX billion [source]
- SAM: $XX billion [methodology]
- SOM: $XX million (Year 1), $XX million (Year 3)

## Competitive Landscape
- X direct competitors, Y indirect competitors
- Market fragmentation: [consolidated/fragmented]
- Key differentiators: [list]

## Recommendations
1. [Action item with rationale]
2. [Action item with rationale]

## Next Steps
- [ ] Action 1
- [ ] Action 2
```

### Competitive Matrix Format
Use markdown tables with scoring (1-5 scale) across key dimensions:
- Product Features
- Pricing
- Market Share
- Customer Satisfaction
- Innovation
- Market Positioning

## Integration with Other Skills

- **Use with `financial-analyst`:** Validate market projections with financial modeling
- **Use with `competitive-intelligence`:** Deep-dive on specific competitors
- **Use with `trend-spotter`:** Continuous monitoring mode for market changes
- **Use with `user-research`:** Validate market hypotheses with customer interviews
- **Use with `seo-analyst`:** Analyze market demand through search volume data

## Validation Checklist

Before finalizing any market research report:

- [ ] All data points have source citations
- [ ] Market size calculations show methodology
- [ ] At least 3 sources validate key numbers
- [ ] Assumptions are documented
- [ ] Competitive set is comprehensive
- [ ] Customer segments are clearly defined
- [ ] Trends are linked to implications
- [ ] Recommendations are actionable
- [ ] Report includes "last updated" date
- [ ] Confidence levels stated for estimates
