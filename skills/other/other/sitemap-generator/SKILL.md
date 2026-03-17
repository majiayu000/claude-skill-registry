---
name: sitemap-generator
description: "Generate XML sitemaps for SEO. Use when: creating sitemap for new site; updating sitemap after changes; generating sitemap from URLs list; validating existing sitemap"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Sitemap Generator

> Generate valid XML sitemaps for search engine indexing and submission.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures analysis frameworks | Metric definitions |
| Identifies patterns in data | Business interpretation |
| Creates visualization templates | Dashboard design |
| Suggests optimization areas | Action priorities |
| Calculates statistical measures | Decision thresholds |

## Dependencies

```bash
pip install click lxml requests
```

## Commands

```bash
python scripts/main.py generate https://example.com --depth 3
python scripts/main.py from-urls urls.txt --output sitemap.xml
python scripts/main.py validate sitemap.xml
```

## Skill Boundaries

### What This Skill Does Well
- Structuring data analysis
- Identifying patterns and trends
- Creating visualization frameworks
- Calculating statistical measures

### What This Skill Cannot Do
- Access your actual data
- Replace statistical expertise
- Make business decisions
- Guarantee prediction accuracy

## Skill Metadata


- **Mode**: centaur
```yaml
category: seo-tools
dependencies: [click, lxml, requests]
difficulty: beginner
```
