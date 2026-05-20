---
name: ugc-collector
description: "Collect and organize user-generated content. Use when: gathering customer testimonials; collecting product photos; organizing social mentions; building UGC campaigns; managing brand mentions"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# UGC Collector

> Collect and organize user-generated content for marketing campaigns and social proof.


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
pip install click requests beautifulsoup4
```

## Commands

```bash
python scripts/main.py search "#brandname" --platform instagram
python scripts/main.py mentions @brand --platform twitter
python scripts/main.py organize ./ugc/ --by-type
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
category: social
dependencies: [click, requests, beautifulsoup4]
difficulty: intermediate
```
