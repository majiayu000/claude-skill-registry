---
name: backlink-analyzer
description: 'Use when the user asks to "analyze backlinks" or "外链分析"; profiles external referring domains, anchor-text distribution, toxic links, and competitor link gaps. Not for internal links — use internal-linking-optimizer. 外链分析/反向链接'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when analyzing backlink profiles, link quality, toxic links, referring domains, or anchor text distribution."
argument-hint: "<domain or URL>"
allowed-tools: WebFetch
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  geo-relevance: "low"
---

# Backlink Analyzer

Analyzes backlink profiles for quality, risk, competitive gaps, and link-building opportunities.

## Quick Start

```
Analyze backlink profile for [domain]
```

```
Find link building opportunities by analyzing [competitor domains]
```

## Skill Contract

**Expected output**: a backlink report or delta summary plus the standard handoff summary for `memory/monitoring/`.

- **Reads**: target domain, backlink/referring-domain exports, competitor domains, anchor data, and any user-provided or tool metrics.
- **Writes**: a user-facing monitoring deliverable and reusable summary.
- **Promotes**: significant changes, confirmed anomalies, follow-up actions, and pending decisions to `memory/open-loops.md`.
- **Done when**: referring domains, anchor mix, and toxic-link share are reported with each metric source-tagged (or N/A); toxic ratio is computed; and at least 3 link-building or disavow actions are named.
- **Primary next skill**: [domain-authority-auditor](../../cross-cutting/domain-authority-auditor/SKILL.md) when toxicity or authority concerns need formal scoring.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

All integrations optional (see [CONNECTORS.md](../../CONNECTORS.md)). With tools, pull backlink profiles from ~~link database and competitor data from ~~SEO tool. Without tools, ask for backlink CSVs, referring domains, competitor domains, and link changes. Respect `robots.txt` and TOS per [SECURITY.md](../../SECURITY.md).

## Decision Gates

**Stop and ask the user when:**
- No backlink data is provided and no ~~link database is connected — link counts cannot be measured. Offer: (1) paste a backlink/referring-domain export, (2) connect a tool, (3) cancel. Do not estimate referring-domain volume from the domain alone.

**Continue silently (never stop for):**
- Which of several competitors to deep-dive — analyze the top 3 by overlap and note the rest.
- Missing optional fields (geography, link velocity) — mark N/A and proceed.

## Instructions

When a user requests backlink analysis:

1. **Generate Profile Overview** — output key metrics, link velocity, authority distribution, and profile health score, with each metric carrying its source tag (tool export / user-provided / estimated).
2. **Analyze Link Quality** — top backlinks, link type mix, anchor text distribution, and geography.
3. **Identify Toxic Links** — risk indicators, links to review, and disavow recommendations; report the toxic ratio as a labeled figure.
4. **Compare Against Competitors** — profile comparison, link intersection, and top linked competitor content.
5. **Find Link Building Opportunities** — intersection prospects, broken links, unlinked mentions, resource pages, guest posts, and effort-vs-impact priorities.
6. **Track Link Changes** — new and lost links, net change, and recovery priorities, each delta labeled against its baseline.
7. **Generate Backlink Report** — executive summary, strengths, concerns, opportunities, competitive position, recommended actions, and KPIs, with every figure source-tagged.

Label every metric **Measured** (tool/export), **User-provided**, or **Estimated** (model inference); never present an estimate as measured; if a required metric is unavailable, mark it N/A — do not invent it.

> **Reference**: See [Analysis Templates](references/analysis-templates.md) for the compact output templates used in all seven steps.

### CITE Item Mapping

When running `domain-authority-auditor` after this analysis, the following data feeds directly into CITE scoring:

| Backlink Metric | CITE Item | Dimension |
|----------------|-----------|-----------|
| Referring domains count | C01 (Referring Domain Volume) | Citation |
| Authority distribution (DA breakdown) | C02 (Referring Domains Quality) | Citation |
| Link velocity | C04 (Link Velocity) | Citation |
| Geographic distribution | C10 (Link Source Diversity) | Citation |
| Dofollow/Nofollow ratio | T02 (Dofollow Ratio Normality) | Trust |
| Toxic link analysis | T01 (Link Profile Naturalness), T03 (Link-Traffic Coherence) | Trust |
| Competitive link intersection | T05 (Profile Uniqueness) | Trust |

## Example

See [Analysis Templates](references/analysis-templates.md) for the full output structure (link-intersection table, opportunities, and impact model).

## Link Quality and Strategy Reference

> **Reference**: See [Link Quality Rubric](references/link-quality-rubric.md) for the scoring matrix, toxic-link criteria, benchmarks, and disavow guidance.

> **Reference**: See [Outreach Templates](references/outreach-templates.md) for outreach frameworks, subject lines, response benchmarks, follow-up sequences, and templates.

### Save Results

Ask "Save these results?" If yes, write to `memory/monitoring/` — see [Skill Contract](../../references/skill-contract.md) §Save Results Template. If toxic ratio exceeds 15%, recommend `domain-authority-auditor`.

## Reference Materials

- [Link Quality Rubric](references/link-quality-rubric.md) — Quality and toxicity rubric
- [Outreach Templates](references/outreach-templates.md) — Outreach frameworks and examples

## Next Best Skill

Toxic ratio > 15% → [domain-authority-auditor](../../cross-cutting/domain-authority-auditor/SKILL.md). Otherwise → Terminal. Visited-set rule applies per [skill-contract.md](../../references/skill-contract.md).
