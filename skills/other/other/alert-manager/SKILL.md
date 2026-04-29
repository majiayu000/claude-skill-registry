---
name: alert-manager
description: 'Configure SEO alerts for ranking drops, traffic changes, technical issues, competitor movements. SEO预警/排名监控'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when setting up monitoring alerts for rankings, traffic, backlinks, technical issues, or AI visibility changes."
argument-hint: "<domain> [metric]"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
  geo-relevance: "low"
  tags:
    - seo
    - geo
    - seo-alerts
    - ranking-alerts
    - traffic-monitoring
    - competitor-alerts
    - automated-monitoring
    - anomaly-detection
    - SEO预警
    - SEOアラート
    - SEO알림
    - alertas-seo
  triggers:
    - "set up SEO alerts"
    - "monitor rankings"
    - "traffic alerts"
    - "competitor alerts"
    - "alert me if rankings drop"
    - "notify me of traffic changes"
    - "watch my keywords for changes"
    - "how to monitor my rankings"
    - "how to set up SEO alerts"
    - "SEO预警"
    - "排名监控"
    - "流量报警"
    - "竞品变动提醒"
    - "排名掉了提醒我"
    - "流量异常"
    - "有变化通知我"
    - "SEOアラート"
    - "ランキング監視"
    - "SEO 알림"
    - "순위 모니터링"
    - "alertas SEO"
    - "monitoreo de rankings"
    - "alertas de SEO"
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

- **Reads**: current metrics, baselines, alert thresholds, and reporting context from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing monitoring deliverable and reusable summary.
- **Promotes**: significant anomalies, durable thresholds, and follow-up actions to `memory/open-loops.md` and `memory/decisions.md`.
- **Primary next skill**: [performance-reporter](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/performance-reporter/SKILL.md) when alert output needs a reporting cadence.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

All integrations optional (see [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md)). With tools, monitor real-time feeds from ~~SEO tool, ~~search console, and ~~web crawler. Without tools, ask for baselines, critical keywords, preferences, and historical data.

## Instructions

When a user requests alert setup:

1. **Define Alert Categories** — choose from rankings, traffic, technical, backlinks, competitors, GEO / AI, and brand alerts.
2. **Configure Alert Rules by Category** — define trigger condition, threshold, alert name, and priority for each relevant rule.
3. **Define Alert Response Plans** — map Critical / High / Medium / Low to response time and next actions.
4. **Set Up Alert Delivery** — configure channels, routing, cooldowns, maintenance windows, and escalation paths.
5. **Create Alert Summary** — deliver category counts, critical playbook, and weekly review checklist.

> **Reference**: See [references/alert-configuration-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/alert-manager/references/alert-configuration-templates.md) for the full category tables, thresholds, and response-plan templates.

## Example

Sample outcome: a keyword alert matrix with Critical vs High thresholds, a response plan for drops, and notification routing to email + Slack.

## Tips for Success

Start simple, tune thresholds to normal volatility, avoid alert fatigue, and review the system regularly.

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

> **Reference**: See [references/alert-threshold-guide.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/alert-manager/references/alert-threshold-guide.md) for threshold setting, fatigue prevention, escalation paths, and response playbooks.

### Save Results

Ask "Save these results?" If yes, write `memory/monitoring/YYYY-MM-DD-<topic>.md` with headline finding, actions, and open loops.

## Reference Materials

- [Alert Threshold Guide](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/alert-manager/references/alert-threshold-guide.md) — Thresholds, fatigue prevention, and escalation templates

## Next Best Skill

Reporting cadence requested → [performance-reporter](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/performance-reporter/SKILL.md). Standalone setup → Terminal. Visited-set rule applies per [skill-contract.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).
