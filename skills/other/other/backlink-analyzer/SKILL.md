---
name: backlink-analyzer
description: 'Use when analyzing backlink profiles, link authority, toxic links, link-building opportunities, or competitor link gaps. 外链分析/反向链接'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when analyzing backlink profiles, link quality, toxic links, referring domains, or anchor text distribution."
argument-hint: "<domain or URL>"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
  geo-relevance: "low"
  tags:
    - seo
    - backlinks
    - link-building
    - link-profile
    - toxic-links
    - off-page-seo
    - link-audit
    - referring-domains
    - disavow
    - ahrefs-alternative
    - 外链分析
    - 被リンク
    - 백링크
    - backlinks-seo
  triggers:
    - "analyze backlinks"
    - "check link profile"
    - "find toxic links"
    - "link building opportunities"
    - "backlink audit"
    - "who links to me"
    - "I have spammy links"
    - "how do I get more backlinks"
    - "disavow links"
    - "how to build backlinks"
    - "外链分析"
    - "反向链接"
    - "有毒链接"
    - "链接建设"
    - "外链怎么做"
    - "有垃圾外链"
    - "谁链接到我"
    - "友链"
    - "互换友链"
    - "外链建设"
    - "被リンク分析"
    - "バックリンク"
    - "リンク構築"
    - "백링크 분석"
    - "링크 빌딩"
    - "누가 내 사이트 링크해?"
    - "백링크 어떻게 늘려?"
    - "análisis de backlinks"
    - "enlaces entrantes"
    - "análise de backlinks"
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

- **Reads**: current metrics, baselines, alert thresholds, and reporting context from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing monitoring deliverable and reusable summary.
- **Promotes**: significant changes, confirmed anomalies, and follow-up actions to `memory/open-loops.md` and `memory/decisions.md`.
- **Primary next skill**: [domain-authority-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/domain-authority-auditor/SKILL.md) when toxicity or authority concerns need formal scoring.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

All integrations optional (see [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md)). With tools, pull backlink profiles from ~~link database and competitor data from ~~SEO tool. Without tools, ask for backlink CSVs, referring domains, competitor domains, and link changes. Respect `robots.txt` and TOS per [SECURITY.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/SECURITY.md).

## Instructions

When a user requests backlink analysis:

1. **Generate Profile Overview** — key metrics, link velocity, authority distribution, and profile health score.
2. **Analyze Link Quality** — top backlinks, link type mix, anchor text distribution, and geography.
3. **Identify Toxic Links** — risk indicators, links to review, and disavow recommendations.
4. **Compare Against Competitors** — profile comparison, link intersection, and top linked competitor content.
5. **Find Link Building Opportunities** — intersection prospects, broken links, unlinked mentions, resource pages, guest posts, and effort-vs-impact priorities.
6. **Track Link Changes** — new and lost links, net change, and recovery priorities.
7. **Generate Backlink Report** — executive summary, strengths, concerns, opportunities, competitive position, recommended actions, and KPIs.

> **Reference**: See [references/analysis-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/backlink-analyzer/references/analysis-templates.md) for the compact output templates used in all seven steps.

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

Sample outcome: a link-intersection table, top immediate opportunities, and an estimated impact model. Keep the full structure in [references/analysis-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/backlink-analyzer/references/analysis-templates.md).

## Tips for Success

Prioritize quality, monitor regularly, diversify anchors and link types, and disavow cautiously.

## Link Quality and Strategy Reference

> **Reference**: See [references/link-quality-rubric.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/backlink-analyzer/references/link-quality-rubric.md) for the scoring matrix, toxic-link criteria, benchmarks, and disavow guidance.

> **Reference**: See [references/outreach-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/backlink-analyzer/references/outreach-templates.md) for outreach frameworks, subject lines, response benchmarks, follow-up sequences, and templates.

### Save Results

Ask "Save these results?" If yes, write `memory/monitoring/YYYY-MM-DD-<topic>.md` with headline finding, actions, and open loops. If toxic ratio exceeds 15%, recommend `domain-authority-auditor`.

## Reference Materials

- [Link Quality Rubric](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/backlink-analyzer/references/link-quality-rubric.md) — Quality and toxicity rubric
- [Outreach Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/backlink-analyzer/references/outreach-templates.md) — Outreach frameworks and examples

## Next Best Skill

Toxic ratio > 15% → [domain-authority-auditor](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/domain-authority-auditor/SKILL.md). Otherwise → Terminal. Visited-set rule applies per [skill-contract.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).
