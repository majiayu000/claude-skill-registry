---
name: hr-network-analyst
description: Professional network graph analyst identifying Gladwellian superconnectors, mavens, and influence brokers using betweenness centrality, structural holes theory, and multi-source network reconstruction. Activate on 'superconnectors', 'network analysis', 'who knows who', 'professional network', 'influence mapping', 'betweenness centrality'. NOT for surveillance, discrimination, stalking, privacy violation, or speculation without data.
allowed-tools: Read,Write,Edit,WebSearch,WebFetch,mcp__firecrawl__firecrawl_search,mcp__firecrawl__firecrawl_scrape,mcp__brave-search__brave_web_search,mcp__SequentialThinking__sequentialthinking
category: Research & Analysis
tags:
  - network
  - superconnectors
  - influence
  - graph-theory
  - hr
pairs-with:
  - skill: career-biographer
    reason: Understand network in career context
  - skill: competitive-cartographer
    reason: Map competitive professional landscape
---

# HR Network Analyst

Applies graph theory and network science to professional relationship mapping. Identifies hidden superconnectors, influence brokers, and knowledge mavens that drive professional ecosystems.

## Integrations

Works with: career-biographer, competitive-cartographer, research-analyst, cv-creator

## Core Questions Answered

- **Who should I know?** (optimal networking targets)
- **Who knows everyone?** (superconnectors for referrals)
- **Who bridges worlds?** (cross-domain brokers)
- **How does influence flow?** (information/opportunity pathways)
- **Where are structural holes?** (untapped connection opportunities)

## Quick Start

```
User: "Who are the key connectors in AI safety research?"

Process:
1. Define boundary: AI safety researchers, 2020-2024
2. Identify sources: arXiv, NeurIPS workshops, Twitter clusters
3. Compute centrality: betweenness (bridges), eigenvector (influence)
4. Classify by archetype: Connector, Maven, Broker
5. Output: Ranked list with network position rationale
```

**Key principle**: Most valuable people aren't always most famous—they connect otherwise disconnected worlds.

## Gladwellian Archetypes (Quick Reference)

| Type | Network Signature | HR Value |
|------|-------------------|----------|
| **Connector** | High betweenness + degree, bridges clusters | Best for cross-domain referrals |
| **Maven** | High in-degree, authoritative, creates content | Know who's good at what |
| **Salesman** | High influence propagation, deal networks | Close candidates, navigate negotiation |

**Full theory**: See `references/network-theory.md`

## Centrality Metrics (Quick Reference)

| Metric | Meaning | When to Use |
|--------|---------|-------------|
| **Betweenness** | Controls information flow | Finding gatekeepers, brokers |
| **Degree** | Raw connection count | Maximizing referral reach |
| **Eigenvector** | Quality over quantity | Access to power, rising stars |
| **PageRank** | Endorsed by important others | Thought leaders |
| **Closeness** | Can reach anyone quickly | Information spreading |

## Analysis Workflows

### 1. Find Superconnectors for Referrals
- Define target domain → Seed network → Expand → Compute betweenness + degree → Rank

### 2. Map Domain Influence
- Define boundaries → Multi-source construction → Community detection → Identify brokers

### 3. Optimize Personal Networking
- Map current network → Map target domain → Find shortest paths → Identify structural holes

### 4. Organizational Network Analysis (ONA)
- Collect data (surveys, Slack metadata) → Construct graph → Find informal vs formal structure

**Detailed workflows**: See `references/data-sources-implementation.md`

## Data Sources

| Source | Signal Strength | What to Extract |
|--------|-----------------|-----------------|
| Co-authorship | Very strong | Publication collaborations |
| Conference co-panel | Strong | Speaking relationships |
| GitHub co-repo | Medium-strong | Code collaboration |
| LinkedIn connection | Medium | Professional links |
| Twitter mutual | Weak | Social association |

**Multi-source fusion**: Weight and combine signals for robust network

## When NOT to Use

- **Surveillance**: Tracking individuals without consent
- **Discrimination**: Using network position to exclude
- **Manipulation**: Engineering social influence for harm
- **Privacy violation**: Accessing non-public data
- **Speculation without data**: Guessing network structure

## Anti-Patterns

### Anti-Pattern: Degree Obsession
**What it looks like**: Only looking at who has most connections
**Why wrong**: High degree often = noise; connectors differ from popular
**Instead**: Use betweenness for bridging, eigenvector for influence quality

### Anti-Pattern: Static Network Assumption
**What it looks like**: Treating 5-year-old connections as current
**Why wrong**: Networks evolve; old edges may be dead
**Instead**: Recency-weight edges, verify currency

### Anti-Pattern: Single-Source Reliance
**What it looks like**: Using only LinkedIn data
**Why wrong**: Missing relationships not on LinkedIn
**Instead**: Multi-source fusion with source-appropriate weighting

### Anti-Pattern: Ignoring Context
**What it looks like**: High betweenness = valuable, regardless of domain
**Why wrong**: Bridging irrelevant communities isn't useful
**Instead**: Constrain analysis to relevant domain boundaries

## Ethical Guidelines

**Acceptable**:
- Analyzing public data (conference speakers, publications)
- Aggregate pattern analysis
- Opt-in organizational analysis
- Academic research with proper IRB

**NOT Acceptable**:
- Scraping private profiles without consent
- Building surveillance systems
- Selling individual data
- Discrimination based on network position

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Can't find data | Domain small/private | Snowball sampling, surveys, adjacent communities |
| False edges | Over-weighting weak signals | Require multiple signals, threshold weights |
| Too large | Unconstrained boundary | K-core filtering, high-weight only |
| Entity resolution | Same person, different names | Unique IDs (ORCID), manual verification |

## Reference Files

- `references/algorithms.md` - NetworkX code patterns, centrality formulas, Gladwell classification
- `references/graph-databases.md` - Neo4j, Neptune, TigerGraph, ArangoDB query examples
- `references/data-sources.md` - LinkedIn network data acquisition strategies, APIs, scraping, legal considerations

---

**Core insight**: Advantage comes from bridging otherwise disconnected groups, not from connections within dense clusters. — Ron Burt, Structural Holes Theory
