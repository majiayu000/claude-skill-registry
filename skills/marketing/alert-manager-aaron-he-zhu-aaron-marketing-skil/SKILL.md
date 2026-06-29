---
name: alert-manager
description: 'Use when the user asks to "set SEO alerts" or "排名掉了提醒我"; configures threshold notifications for FUTURE ranking, traffic, technical, and competitor changes. Not for one-time measurement or reporting — use rank-tracker or performance-reporter. SEO预警/排名监控'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when setting up monitoring alerts for rankings, traffic, backlinks, technical issues, or AI visibility changes."
argument-hint: "<domain> [metric]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  geo-relevance: "low"
---

# Alert Manager

Sets up proactive monitoring alerts for ranking, traffic, technical, backlink, competitor, and GEO changes.

## Quick Start

```
Set up SEO monitoring alerts for [domain]
```

```
Create ranking drop alerts for my top 20 keywords
```

## Skill Contract

**Expected output**: an alert configuration summary plus the standard handoff summary for `memory/monitoring/`.

- **Reads**: baselines, critical keywords/metrics to watch, normal volatility, delivery preferences, and any user-provided or tool data.
- **Writes**: a user-facing monitoring deliverable and reusable summary.
- **Promotes**: significant anomalies, durable thresholds, follow-up actions, and pending decisions to `memory/open-loops.md`.
- **Done when**: each chosen alert category has a named trigger condition, threshold, and priority; a Critical/High/Medium/Low response plan and delivery routing are defined; and thresholds are tuned to the metric's stated normal volatility.
- **Primary next skill**: [performance-reporter](../performance-reporter/SKILL.md) when alert output needs a reporting cadence.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

All integrations optional (see [CONNECTORS.md](../../CONNECTORS.md)). With tools, monitor real-time feeds from ~~SEO tool, ~~search console, and ~~web crawler. Without tools, ask for baselines, critical keywords, preferences, and historical data.

## Decision Gates

**Stop and ask the user when:**
- No baseline or normal-volatility reference exists for the metrics to be watched — thresholds would be arbitrary. Offer: (1) supply recent baseline data, (2) use the Quick Reference defaults below and label them Estimated, (3) cancel.

**Continue silently (never stop for):**
- Which delivery channel to use — default to the channel already in context (or email) and note it.
- A category the user did not mention — leave it unconfigured; do not add alerts they did not request.

## Instructions

When a user requests alert setup:

1. **Define Alert Categories** — choose from rankings, traffic, technical, backlinks, competitors, GEO / AI, and brand alerts.
2. **Configure Alert Rules by Category** — define trigger condition, threshold, alert name, and priority for each relevant rule; tie each threshold to a stated baseline and label that baseline Measured / User-provided / Estimated.
3. **Define Alert Response Plans** — map Critical / High / Medium / Low to response time and next actions.
4. **Set Up Alert Delivery** — configure channels, routing, cooldowns, maintenance windows, and escalation paths.
5. **Create Alert Summary** — output category counts, the critical playbook, and a weekly review checklist as the deliverable.

Label every metric **Measured** (tool/export), **User-provided**, or **Estimated** (model inference); never present an estimate as measured; if a required metric is unavailable, mark it N/A — do not invent it.

> **Reference**: See [Alert Configuration Templates](references/alert-configuration-templates.md) for the full category tables, thresholds, and response-plan templates.

## Example

Sample outcome: a keyword alert matrix with Critical vs High thresholds, a response plan for drops, and notification routing to email + Slack.

## Alert Threshold Quick Reference

| Metric | Warning | Critical | Frequency |
|--------|---------|----------|-----------|
| Organic traffic | -15% WoW | -30% WoW | Daily |
| Keyword positions | >3 position drop | >5 position drop | Daily |
| Pages indexed | -5% change | -20% change | Weekly |
| Crawl errors | >10 new/day | >50 new/day | Daily |
| Core Web Vitals | "Needs Improvement" | "Poor" | Weekly |
| Backlinks lost | >5% in 1 week | >15% in 1 week | Weekly |
| AI citation loss | Any key query | >20% queries | Weekly |
| Security issues | Any detected | Any detected | Daily |

> **Reference**: See [Alert Threshold Guide](references/alert-threshold-guide.md) for threshold setting, fatigue prevention, escalation paths, and response playbooks.

### Save Results

Ask "Save these results?" If yes, write to `memory/monitoring/` — see [Skill Contract](../../references/skill-contract.md) §Save Results Template.

## Reference Materials

- [Alert Threshold Guide](references/alert-threshold-guide.md) — Thresholds, fatigue prevention, and escalation templates

## Next Best Skill

Reporting cadence requested → [performance-reporter](../performance-reporter/SKILL.md). Standalone setup → Terminal. Visited-set rule applies per [skill-contract.md](../../references/skill-contract.md).
