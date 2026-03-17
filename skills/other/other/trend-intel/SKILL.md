---
name: trend-intel
description: Track and analyze trends, breaking news, and market shifts. Measures velocity across web, social, news, GitHub, and academic signals. Produces news digests and trend trajectory reports. Use when tracking news, identifying trends, or monitoring developments.
argument-hint: "[topic, technology, market, or trend to track]"
allowed-tools: mcp__RivalSearchMCP__web_search, mcp__RivalSearchMCP__social_search, mcp__RivalSearchMCP__news_aggregation, mcp__RivalSearchMCP__scientific_research, mcp__RivalSearchMCP__github_search, mcp__RivalSearchMCP__content_operations, mcp__RivalSearchMCP__map_website, mcp__RivalSearchMCP__document_analysis, Read, Grep, Glob, WebFetch, WebSearch
---

# Trend Intelligence

Analyze trends and news for: **$ARGUMENTS**

Follow these steps precisely using RivalSearchMCP tools. Report progress after each step.

## Step 1: Breaking News Scan

Use `news_aggregation` twice to establish recency and trajectory:
1. query: "$ARGUMENTS", max_results: 15, time_range: "week"
2. query: "$ARGUMENTS", max_results: 15, time_range: "month"

Compare weekly to monthly volume. Is coverage accelerating, steady, or declining?

## Step 2: Web Context

Use `web_search` twice for broader context:
1. query: "$ARGUMENTS trends 2025 2026", num_results: 15, extract_content: true
2. query: "$ARGUMENTS emerging growth adoption", num_results: 10, extract_content: true

Capture analysis from non-news sources (blogs, industry sites, company announcements).

## Step 3: Social Signal Measurement

Use `social_search` twice to measure community momentum:
1. query: "$ARGUMENTS", platforms: ["reddit", "hackernews", "producthunt", "devto", "medium"], max_results_per_platform: 15, time_filter: "month"
2. query: "$ARGUMENTS", platforms: ["reddit", "hackernews"], max_results_per_platform: 15, time_filter: "year"

Compare recent (month) vs historical (year) volume. Note sentiment shifts, new voices, and debate intensity.

## Step 4: Developer Adoption Signals

Use `github_search` twice:
1. query: "$ARGUMENTS", sort: "stars", max_results: 15, include_readme: true
2. query: "$ARGUMENTS", sort: "updated", max_results: 15

Compare established projects (stars) vs active development (updated). Note star counts, contributor numbers, and issue activity.

## Step 5: Academic Foundation

Use `scientific_research`:
- operation: "academic_search", query: "$ARGUMENTS", max_results: 10, sources: ["semantic_scholar", "arxiv"]

Is there peer-reviewed research driving this trend? How recent are the publications?

## Step 6: Deep Dives

For the 3 most insightful articles or reports found, use `content_operations`:
- operation: "retrieve", url: <article_url>, extraction_method: "markdown"
- operation: "analyze", content: <retrieved>, analysis_type: "general", extract_key_points: true, summarize: true

For the top 2-3 companies or projects driving this trend:
- Use `map_website` with url: <player_url>, mode: "research", max_pages: 5, max_depth: 1

## Step 7: Compile Trend Report

1. **Headlines** — Top 3-5 stories in bullet form with one-line summaries
2. **Key Developments** — Expanded coverage of the most significant stories (2-3 paragraphs each)
3. **Velocity Indicators** — Table with metrics:
   | Signal | Measurement | Direction |
   |--------|------------|-----------|
   | News frequency | X articles/week | Accelerating/Steady/Declining |
   | Social mentions | X threads/month | ... |
   | GitHub stars | Top repo: X stars | ... |
   | Academic papers | X papers in last year | ... |
4. **Community Pulse** — What practitioners and the public are saying
5. **Maturity Assessment** — Nascent / Emerging / Growing / Mainstream / Mature / Declining
6. **Key Players & Catalysts** — Who and what is driving adoption
7. **Trajectory Projection** — Bull case vs bear case with evidence
8. **What to Watch** — Upcoming events, expected announcements, early signals to track
9. **Sources** — All URLs consulted

Keep it concise but data-rich. Use clean markdown with inline citations [Source Name](URL).
