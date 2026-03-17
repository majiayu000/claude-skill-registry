---
name: due-diligence
description: Comprehensive due diligence on companies or individuals. Investigates background, product, financials, leadership, technology, risks, competitive position, and public reputation. Use when evaluating companies for investment, researching people, or making partnership decisions.
argument-hint: "[company name, person's name, product, or URL]"
allowed-tools: mcp__RivalSearchMCP__web_search, mcp__RivalSearchMCP__social_search, mcp__RivalSearchMCP__news_aggregation, mcp__RivalSearchMCP__scientific_research, mcp__RivalSearchMCP__github_search, mcp__RivalSearchMCP__content_operations, mcp__RivalSearchMCP__map_website, mcp__RivalSearchMCP__document_analysis, mcp__RivalSearchMCP__research_topic, mcp__RivalSearchMCP__research_agent, Read, Grep, Glob, WebFetch, WebSearch
---

# Due Diligence

Conduct due diligence research on: **$ARGUMENTS**

The argument may be a company name, person's name, product name, or URL. Follow these steps precisely using RivalSearchMCP tools. Report progress after each step.

## Step 1: Entity Identification

Use `web_search` twice:
1. query: "$ARGUMENTS", num_results: 15, extract_content: true
2. query: "$ARGUMENTS bio OR background OR career OR founder OR company OR about", num_results: 10

Determine if the subject is a **company** or an **individual**. Establish: full name, current role/mission, website, and key facts. Adapt subsequent steps accordingly.

## Step 2: Digital Presence

Use `map_website`:
- url: <primary_website>, mode: "research", max_pages: 10, max_depth: 2

Use `content_operations` to retrieve key pages:
- operation: "retrieve" for homepage/profile, about, product/work, team/bio pages
- operation: "analyze", content: <retrieved>, analysis_type: "business", extract_key_points: true, summarize: true

## Step 3: Financial & Growth Signals

*For companies:*

Use `web_search` three times:
1. query: "$ARGUMENTS funding raised investment", num_results: 10
2. query: "$ARGUMENTS revenue growth customers", num_results: 10
3. query: "$ARGUMENTS layoffs OR downsizing OR restructuring OR controversy", num_results: 10

*For individuals:*

Use `web_search`:
- query: "$ARGUMENTS investments OR portfolio OR companies OR ventures", num_results: 10

Use `news_aggregation`:
- query: "$ARGUMENTS", max_results: 15, time_range: "month"

## Step 4: Leadership & People

Use `web_search`:
- query: "$ARGUMENTS founder CEO leadership team", num_results: 10, extract_content: true

Use `social_search`:
- query: "$ARGUMENTS CEO OR founder", platforms: ["reddit", "hackernews"], max_results_per_platform: 5

Use `web_search`:
- query: "$ARGUMENTS glassdoor OR employee review OR culture", num_results: 5

*For individuals — also search for:*
- query: "$ARGUMENTS interview OR podcast OR keynote OR conference", num_results: 10

## Step 5: Technical Assessment

Use `github_search`:
- query: "$ARGUMENTS", sort: "stars", max_results: 10, include_readme: true

Use `web_search`:
- query: "$ARGUMENTS tech stack OR engineering OR architecture", num_results: 10

Use `scientific_research`:
- operation: "academic_search", query: "$ARGUMENTS", max_results: 5

## Step 6: Market & Competitive Position

Use `web_search`:
- query: "$ARGUMENTS competitors alternatives market share", num_results: 10

Use `social_search`:
- query: "$ARGUMENTS vs OR alternative OR comparison", platforms: ["reddit", "hackernews", "producthunt"], max_results_per_platform: 10

## Step 7: Reputation & Risk Assessment

Use `social_search`:
- query: "$ARGUMENTS", platforms: ["reddit", "hackernews", "producthunt", "medium"], max_results_per_platform: 10, time_filter: "year"

Use `web_search`:
- query: "$ARGUMENTS review OR complaint OR problem OR issue OR controversy", num_results: 10

Use `content_operations` on any regulatory filings or key reports found:
- operation: "retrieve", url: <document_url>, extraction_method: "markdown"

## Step 8: Deep Content Analysis

For the 2-3 most informative pages found, use `content_operations`:
- operation: "retrieve", url: <page_url>, extraction_method: "markdown"
- operation: "analyze", content: <retrieved>, analysis_type: "general", extract_key_points: true, summarize: true

## Step 9: Compile Report

**For companies:**

1. **Executive Summary** — 2-3 paragraph overview with key findings
2. **Company Profile** — Founded, mission, HQ, size, key facts
3. **Product & Market** — Offerings, pricing, target market, customer evidence
4. **Financial Signals** — Funding history, growth indicators, burn rate signals
5. **Leadership & Team** — Key executives, backgrounds, culture signals
6. **Technical Assessment** — Stack, open source, IP, engineering quality
7. **Competitive Position** — Landscape, differentiation, market share signals
8. **Risk Assessment** — Table format:
   | Risk Category | Level | Evidence |
   |--------------|-------|----------|
   | Financial | Low/Medium/High | ... |
   | Technical | Low/Medium/High | ... |
   | Market | Low/Medium/High | ... |
   | Legal/Regulatory | Low/Medium/High | ... |
   | Reputational | Low/Medium/High | ... |
9. **Red Flags** — Concerning signals discovered
10. **Green Flags** — Positive indicators and strengths
11. **Information Gaps** — What couldn't be determined
12. **Sources** — All URLs consulted with brief context

**For individuals:**

1. **Profile Summary** — 2-3 paragraph overview of who this person is
2. **Key Facts** — Current role, company, location, notable achievements
3. **Career Timeline** — Professional history in reverse chronological order
4. **Public Presence** — Websites, writing, speaking, media appearances
5. **Community Reputation** — What others say (with sources)
6. **Technical Contributions** — Open source, papers, patents
7. **Media Coverage** — Recent press and interviews
8. **Notable Connections** — Companies, investors, co-founders, collaborators
9. **Red Flags** — Any concerning signals
10. **Green Flags** — Positive indicators
11. **Information Gaps** — What couldn't be determined
12. **Sources** — All URLs consulted

Use clean markdown. Cite every claim with [Source Name](URL) format. Only include publicly available information.
