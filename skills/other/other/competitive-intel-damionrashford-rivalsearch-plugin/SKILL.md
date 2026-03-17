---
name: competitive-intel
description: Competitive intelligence for companies, products, markets, or websites. Maps sites, analyzes products and pricing, tracks news and sentiment, profiles the competitive landscape, and produces SWOT analysis. Use when analyzing competitors, evaluating markets, or auditing web presence.
argument-hint: "[company name, product, market segment, or URL]"
allowed-tools: mcp__RivalSearchMCP__web_search, mcp__RivalSearchMCP__social_search, mcp__RivalSearchMCP__news_aggregation, mcp__RivalSearchMCP__scientific_research, mcp__RivalSearchMCP__github_search, mcp__RivalSearchMCP__content_operations, mcp__RivalSearchMCP__map_website, mcp__RivalSearchMCP__document_analysis, mcp__RivalSearchMCP__research_topic, mcp__RivalSearchMCP__research_agent, Read, Grep, Glob, WebFetch, WebSearch
---

# Competitive Intelligence

Conduct competitive intelligence on: **$ARGUMENTS**

The argument may be a company name, product name, market segment, or URL. Follow these steps precisely using RivalSearchMCP tools. Report progress after each step.

## Step 1: Target Identification

Use `web_search`:
- query: "$ARGUMENTS official website", num_results: 10, extract_content: true

Establish the target's identity, website, and determine if this is a single entity or a market segment.

## Step 2: Website & Product Audit

Use `map_website` to explore the target's web presence:
1. url: <target_website>, mode: "map", max_pages: 15, max_depth: 2
2. url: <target_website>, mode: "research", max_pages: 10, max_depth: 2

If they have documentation:
3. url: <target_website>, mode: "docs", max_pages: 10

Record page hierarchy, navigation patterns, technology signals, and content volume.

## Step 3: Key Page Analysis

Use `content_operations` to retrieve and analyze critical pages:
- operation: "retrieve" for homepage, pricing, product, about, and team pages
- operation: "analyze", content: <retrieved>, analysis_type: "business", extract_key_points: true, summarize: true

Extract ecosystem links:
- operation: "extract", url: <target_website>, link_type: "internal", max_links: 100
- operation: "extract", url: <target_website>, link_type: "external", max_links: 50

## Step 4: Market Landscape

Use `web_search` three times:
1. query: "$ARGUMENTS market landscape overview", num_results: 15, extract_content: true
2. query: "$ARGUMENTS market size growth trends", num_results: 10
3. query: "$ARGUMENTS competitors alternatives market share", num_results: 10

Identify the broader market context, key players, and competitive positioning.

## Step 5: News & Investment Activity

Use `news_aggregation` twice:
1. query: "$ARGUMENTS", max_results: 15, time_range: "month"
2. query: "$ARGUMENTS funding OR acquisition OR partnership", max_results: 10, time_range: "month"

Use `web_search`:
- query: "$ARGUMENTS funding raised investment valuation", num_results: 10

## Step 6: Community Perception

Use `social_search` twice:
1. query: "$ARGUMENTS", platforms: ["reddit", "hackernews", "devto", "producthunt", "medium"], max_results_per_platform: 10, time_filter: "year"
2. query: "$ARGUMENTS vs OR alternative OR comparison OR best", platforms: ["reddit", "hackernews"], max_results_per_platform: 10

What do users praise? Complain about? What alternatives do they mention?

## Step 7: Technical & GitHub Assessment

Use `github_search` twice:
1. query: "$ARGUMENTS", sort: "stars", max_results: 15, include_readme: true
2. query: "$ARGUMENTS", sort: "updated", max_results: 10

Use `web_search`:
- query: "$ARGUMENTS tech stack OR technology OR engineering OR architecture", num_results: 10

Use `scientific_research`:
- operation: "academic_search", query: "$ARGUMENTS", max_results: 5

## Step 8: Compile Report

1. **Executive Summary** — Key findings and market position assessment
2. **Company/Market Overview** — Identity, product, market context
3. **Website Assessment** — Site structure, content quality, technical observations
4. **Product & Pricing** — Offerings, pricing model, features, target audience
5. **Market Landscape** — Market size, growth, key players with comparison table
6. **SWOT Analysis**
   - **Strengths** — Competitive advantages and moats
   - **Weaknesses** — Vulnerabilities and pain points
   - **Opportunities** — Where they (or you) can gain ground
   - **Threats** — Competitive dangers and headwinds
7. **News & Investment** — Funding, partnerships, growth trajectory
8. **Community Perception** — Practitioner sentiment with evidence
9. **Technical Assessment** — Stack, GitHub presence, engineering quality
10. **Ecosystem & Partnerships** — Integrations, partner network, link analysis
11. **Sources** — All URLs consulted

Use tables for player comparisons. Format as clean markdown with inline citations [Source Name](URL).
