---
name: yandex-competitive-analysis
description: Analyze competitors and search landscape in Russian/CIS markets using Yandex tools. Finds who ranks for keywords, identifies content gaps, and discovers ranking opportunities. Use when user asks about competitors, who ranks for something, content gaps, or SERP analysis in Russia/CIS.
---

# Yandex Competitive Analysis

Analyze competitors and find opportunities in Russian and CIS search markets.

## Available Tools

- `mcp__yandex-search__search` - Find who currently ranks for target keywords
- `mcp__yandex-wordstat__top-requests` - Understand search volume and related queries
- `mcp__yandex-wordstat__dynamics` - Track if competition is increasing over time
- `mcp__yandex-wordstat__regions` - Find underserved regional markets
- `mcp__yandex-webmaster__get-popular-queries` - Compare user's site performance (requires Webmaster)
- `mcp__yandex-webmaster__get-summary` - Get user's site health metrics (requires Webmaster)

## Workflow

1. **Search landscape**: Use `search` to find top 10-20 results for target keywords
2. **Volume analysis**: Use `top-requests` to understand search demand
3. **Trend analysis**: Use `dynamics` to see if market is growing
4. **Regional opportunities**: Use `regions` to find high-affinity, underserved regions
5. **Own position** (if Webmaster): Compare user's ranking vs competitors

## Analysis Framework

When analyzing competitors:
- **Domain authority signals**: Identify recurring domains in top positions
- **Content patterns**: Note content types that rank (articles, products, forums)
- **Gap opportunities**: Keywords with high volume but weak competition
- **Regional gaps**: Regions with high affinity but low competition

## Output Guidelines

- Adapt output language to match the user's language
- Present competitor domains with their ranking positions
- Highlight content gaps and opportunities clearly
- Provide actionable recommendations
- Include regional opportunities if relevant

## Example Queries That Trigger This Skill

- "Who ranks for [keyword] in Yandex?"
- "Analyze competitors for [topic] in Russia"
- "What content gaps exist for [topic]?"
- "SERP analysis for [keyword]"
- "Find ranking opportunities for [topic]"
