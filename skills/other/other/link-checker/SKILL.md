---
name: link-checker
description: "Find broken links on websites. Use when: auditing website for broken links; checking internal link structure; finding 404 errors; validating external links; pre-launch QA"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Link Checker

> Crawl websites to find broken links and 404 errors - essential for SEO health and user experience.


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
pip install aiohttp beautifulsoup4 click
```

## Commands

```bash
python scripts/main.py check https://example.com --depth 2
python scripts/main.py report https://example.com --output broken-links.csv
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
dependencies: [aiohttp, beautifulsoup4]
difficulty: beginner
```
