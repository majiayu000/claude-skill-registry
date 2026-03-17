---
name: mteb-leaderboard
description: This skill provides guidance for retrieving and verifying information from dynamic ML leaderboards (MTEB, Scandinavian Embedding Benchmark, HuggingFace leaderboards, etc.) with specific temporal requirements. It should be used when tasks involve finding top-performing models, rankings, or benchmark results as of a specific date, especially when the data source is frequently updated.
---

# MTEB Leaderboard

## Overview

This skill guides the retrieval of accurate information from machine learning benchmark leaderboards, particularly the Massive Text Embedding Benchmark (MTEB) and related embedding model leaderboards. The core challenge is obtaining temporally-accurate data from dynamic sources that update frequently.

## Key Challenges

1. **Temporal accuracy**: Leaderboards change over time; a paper or cached result from one date may not reflect the state at another date
2. **Data source identification**: Leaderboards may have multiple interfaces (web UI, API, GitHub data files, papers)
3. **Format interpretation**: Model naming conventions vary (API models vs. open-source, organization/model format)
4. **Historical data access**: Finding leaderboard state at a specific past date requires different strategies than current data

## Approach

### Step 1: Clarify Requirements Before Searching

Before starting any search, explicitly identify:

- **Target date**: Is it current data or historical (specific date in the past)?
- **Leaderboard scope**: Which specific benchmark or subset (e.g., MTEB overall, Scandinavian subset, specific language)?
- **Model format constraints**: Are API-only models acceptable, or only downloadable/open-source models?
- **Metric of interest**: Overall score, specific task performance, or particular metric?

If any requirements are ambiguous, seek clarification rather than making assumptions.

### Step 2: Identify Primary Data Sources

For MTEB and embedding leaderboards, potential data sources include:

1. **Official leaderboard UI**: HuggingFace Spaces hosting the leaderboard
2. **GitHub repositories**: Often contain raw data files (JSON, CSV) with historical commits
3. **Academic papers**: Provide snapshot data but become outdated quickly
4. **API endpoints**: Some leaderboards have programmatic access

Prioritize sources based on temporal requirements:
- **Current data**: Live leaderboard UI or API
- **Historical data**: GitHub commit history, archived web pages, or versioned data files

### Step 3: Access Underlying Data Files

When web interfaces fail or historical data is needed:

1. Search for the leaderboard's GitHub repository
2. Look for data directories containing JSON, CSV, or JSONL files
3. For historical queries, examine git commit history around the target date
4. Check for cached or archived versions of the leaderboard

### Step 4: Handle Temporal Discrepancies

When data sources don't match the requested time period:

- **Never assume** old data represents a more recent date
- **Acknowledge gaps** explicitly if the exact temporal data cannot be found
- **Provide context** about when the available data was captured
- **Search for updates** using date-restricted queries (e.g., "MTEB leaderboard August 2025")

### Step 5: Verify and Cross-Reference

Before providing a final answer:

1. Confirm the data source's timestamp matches the requested period
2. Cross-reference with multiple sources when possible
3. Note any assumptions or limitations in the response
4. Specify the exact source and retrieval date

## Common Pitfalls

### Using Outdated Papers as Current Truth
Academic papers provide point-in-time snapshots. A paper from June 2024 cannot be used to answer questions about August 2025 leaderboard state without explicit acknowledgment of this limitation.

### Making Format Assumptions
When asked for "organization/model_name format," do not assume this excludes API models. Clarify whether the user wants:
- Only models downloadable from HuggingFace
- Any model that can be expressed in that format
- A specific category (open-source, commercial, etc.)

### Dismissing System Context
If the system indicates a specific date context, treat temporal references relative to that date. "As of August 2025" from a November 2025 context means historical data retrieval, not future prediction.

### Premature Conclusions
Exhaust available data sources before concluding. If the primary leaderboard UI is inaccessible:
- Try alternative URLs
- Search for GitHub data repositories
- Look for API endpoints
- Check web archives

### Ignoring Data Freshness
Always report when data was captured, not just what it shows. "According to the June 2024 paper" is different from "As of August 2025."

## Verification Strategies

1. **Source timestamp verification**: Confirm when the data was published or last updated
2. **Cross-source validation**: Check if multiple sources agree on rankings
3. **Recency check**: For current queries, verify the leaderboard shows recent submissions
4. **Format compliance**: Ensure the model name matches the requested format exactly
5. **Scope confirmation**: Verify the result is for the correct benchmark subset

## Output Guidelines

When providing leaderboard information:

1. State the exact source of the information
2. Include the date/version of the data
3. Note any temporal limitations or assumptions
4. Provide the answer in the exact format requested
5. If unable to find data for the specific time period, explicitly state this limitation
