---
name: yandex-keyword-research
description: Research keywords for Russian/CIS markets using Yandex Wordstat data. Analyzes search volumes, trends over time, and regional distribution. Use when user asks about keyword research, search volumes, trending topics, or what people are searching for in Russia/CIS.
---

# Yandex Keyword Research

Research keywords and search trends for Russian and CIS markets using Yandex tools.

## Available Tools

- `mcp__yandex-wordstat__top-requests` - Find popular queries containing a keyword (costs 1 quota unit)
- `mcp__yandex-wordstat__dynamics` - Analyze search volume trends over time (costs 2 quota units)
- `mcp__yandex-wordstat__regions` - See regional distribution of search interest (costs 2 quota units)
- `mcp__yandex-wordstat__get-regions-tree` - Get region hierarchy for filtering (free)
- `mcp__yandex-search__search` - See what currently ranks in Yandex for the keyword
- `mcp__yandex-webmaster__get-popular-queries` - Check if user's site ranks for terms (requires Webmaster access)

## Workflow

1. **Get popular queries**: Start with `top-requests` to find related searches and volumes
2. **Analyze trends**: Use `dynamics` to see if interest is growing or declining
3. **Regional breakdown**: Use `regions` to find which areas have highest interest
4. **SERP analysis** (optional): Use `search` to see current ranking content
5. **Own site check** (if Webmaster configured): Check user's site performance for these terms

## Output Guidelines

- Adapt output language to match the user's language
- Present search volumes with context (high/medium/low for the market)
- Highlight trend direction (growing, stable, declining) with percentage change
- Show top 5-10 regions by volume and by affinity index
- Include actionable insights based on the data

## Example Queries That Trigger This Skill

- "What are people searching for related to [topic] in Russia?"
- "Research keywords for [topic] in Russian market"
- "What's the search volume for [keyword] in Yandex?"
- "Is [topic] trending in Russia?"
- "Keyword analysis for [topic]"
