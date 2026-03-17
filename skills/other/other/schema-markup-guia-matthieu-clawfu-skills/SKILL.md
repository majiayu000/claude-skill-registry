---
name: schema-markup
description: "Generate JSON-LD structured data for SEO. Use when: adding schema markup to pages; creating organization schema; generating product schema; validating existing schema; rich snippet optimization"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Schema Markup Generator

> Generate valid JSON-LD structured data for better search visibility and rich snippets.


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
pip install click pydantic
```

## Commands

```bash
python scripts/main.py generate --type article --title "..." --author "..."
python scripts/main.py generate --type product --name "..." --price 99
python scripts/main.py validate schema.json
python scripts/main.py templates
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
dependencies: [click, pydantic]
difficulty: beginner
```
