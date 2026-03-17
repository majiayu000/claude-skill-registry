---
name: research
description: Comprehensive multi-source research with academic depth. Searches web, social platforms, news, academic databases, and GitHub. Discovers papers, datasets, and open source implementations. Use when conducting research, literature reviews, or investigating any topic.
argument-hint: "[topic, research question, or academic query]"
allowed-tools: mcp__RivalSearchMCP__web_search, mcp__RivalSearchMCP__social_search, mcp__RivalSearchMCP__news_aggregation, mcp__RivalSearchMCP__scientific_research, mcp__RivalSearchMCP__github_search, mcp__RivalSearchMCP__content_operations, mcp__RivalSearchMCP__map_website, mcp__RivalSearchMCP__document_analysis, mcp__RivalSearchMCP__research_topic, mcp__RivalSearchMCP__research_agent, Read, Grep, Glob, WebFetch, WebSearch
---

# Research

Conduct comprehensive research on: **$ARGUMENTS**

Follow these steps precisely using RivalSearchMCP tools. Report progress after each step.

## Step 1: Web Discovery

Use `web_search` for broad discovery:
- query: "$ARGUMENTS", num_results: 15, extract_content: true, follow_links: true, max_depth: 2

Identify the top 3-5 most relevant URLs. Note key themes and recurring sources.

## Step 2: Social & Community Pulse

Use `social_search` to gauge community discussions:
- query: "$ARGUMENTS", platforms: ["reddit", "hackernews", "devto", "producthunt", "medium"], max_results_per_platform: 10, time_filter: "year"

Analyze what practitioners are saying. Note consensus, debate, and emerging opinions.

## Step 3: News Coverage

Use `news_aggregation` for recent developments:
- query: "$ARGUMENTS", max_results: 15, time_range: "month"

Identify breaking news, announcements, and trend shifts.

## Step 4: Academic Literature

Use `scientific_research` twice for peer-reviewed sources:
1. operation: "academic_search", query: "$ARGUMENTS", max_results: 15, sources: ["semantic_scholar", "arxiv"]
2. operation: "academic_search", query: "$ARGUMENTS survey OR review OR overview", max_results: 5

Identify the most cited papers, recent publications, key authors, and methodologies. Look for surveys that summarize the field.

## Step 5: Datasets & Implementations

Use `scientific_research` for datasets:
- operation: "dataset_discovery", query: "$ARGUMENTS", max_results: 10

Use `github_search` for open source implementations:
- query: "$ARGUMENTS", sort: "stars", max_results: 10, include_readme: true

## Step 6: Deep Content Retrieval

For the 3-5 most important sources from previous steps:

Use `content_operations`:
- operation: "retrieve", url: <selected_url>, extraction_method: "markdown"

For any key papers with accessible PDFs, use `document_analysis`:
- url: <paper_pdf_url>, max_pages: 10, extract_metadata: true, summary_length: 1000

Then analyze the most critical content:
- operation: "analyze", content: <retrieved>, analysis_type: "general", extract_key_points: true, summarize: true

## Step 7: Compile Report

1. **Executive Summary** — 2-3 paragraph overview of key takeaways
2. **Key Findings** — Numbered list of the most important discoveries
3. **Web Intelligence** — What mainstream sources reveal
4. **Community Sentiment** — Practitioner discussions and opinions
5. **Recent Developments** — News, announcements, trend shifts
6. **Academic Foundation** — Key papers, methodologies, research threads, and key authors
7. **Datasets & Tools** — Available datasets and open source implementations
8. **Deep Dive Insights** — Detailed analysis from primary sources
9. **Contradictions & Gaps** — Where sources disagree or information is missing
10. **Sources** — Complete list of all URLs consulted

Use clean markdown. Cite sources inline with [Source Name](URL) format.
