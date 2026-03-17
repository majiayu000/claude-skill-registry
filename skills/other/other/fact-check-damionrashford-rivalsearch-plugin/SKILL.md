---
name: fact-check
description: Verify claims, statements, or assertions by cross-referencing web, news, academic, and social sources. Produces a confidence-scored verdict with full evidence chain. Use when verifying claims, checking facts, or validating statements.
argument-hint: "[claim or statement to verify]"
allowed-tools: mcp__RivalSearchMCP__web_search, mcp__RivalSearchMCP__social_search, mcp__RivalSearchMCP__news_aggregation, mcp__RivalSearchMCP__scientific_research, mcp__RivalSearchMCP__github_search, mcp__RivalSearchMCP__content_operations, mcp__RivalSearchMCP__document_analysis, mcp__RivalSearchMCP__research_topic, Read, Grep, Glob, WebFetch, WebSearch
---

# Fact Check

Verify the following claim: **$ARGUMENTS**

Follow these steps precisely using RivalSearchMCP tools. Report progress after each step.

## Step 1: Claim Decomposition

Parse the claim into individually verifiable components. List each sub-claim and what evidence would confirm or refute it.

## Step 2: Primary Source Search

Use `web_search` to find the origin of the claim:
- query: "$ARGUMENTS"
- num_results: 15
- extract_content: true

Identify where this claim first appeared. Use `content_operations` to retrieve the original source:
- operation: "retrieve", url: <source_url>, extraction_method: "markdown"

## Step 3: Corroboration Search

Search for independent confirmation:
- `web_search` with query: "$ARGUMENTS", num_results: 10
- `web_search` with alternative phrasing of the claim, num_results: 10
- `news_aggregation` with query: "$ARGUMENTS", max_results: 10, time_range: "month"

Count how many independent sources confirm the claim.

## Step 4: Counter-Evidence Search

Actively search for contradicting evidence:
- `web_search` with query: "$ARGUMENTS false OR debunked OR incorrect OR misleading", num_results: 10
- `social_search` with query: "$ARGUMENTS", platforms: ["reddit", "hackernews"], max_results_per_platform: 10

Look for rebuttals, corrections, retractions, or alternative explanations.

## Step 5: Academic Verification

If the claim involves data, statistics, or technical facts:
- `scientific_research` with operation: "academic_search", query: "$ARGUMENTS", max_results: 5, sources: ["semantic_scholar", "arxiv"]

Check if peer-reviewed research supports or contradicts the claim.

## Step 6: Deep Source Analysis

For the 2-3 most authoritative sources (for and against), use `content_operations`:
- operation: "retrieve", url: <source_url>, extraction_method: "markdown"
- operation: "analyze", content: <retrieved>, analysis_type: "general", extract_key_points: true

Read and assess the quality of each source.

## Step 7: Compile Verdict

1. **Claim Under Review** — Quote the exact claim
2. **Verdict** — One of: Verified / Likely True / Unverified / Disputed / Likely False / False
3. **Confidence Score** — High / Medium-High / Medium / Medium-Low / Low
4. **Evidence For** — Sources supporting the claim with inline citations
5. **Evidence Against** — Sources contradicting the claim with inline citations
6. **Primary Source Analysis** — What the original source actually says
7. **Context & Nuance** — Important context that affects interpretation
8. **Component Verdicts** — If multiple sub-claims, verdict on each
9. **Sources** — Complete list of all URLs consulted

Use clean markdown. Every factual statement must cite its source with [Source Name](URL) format.
