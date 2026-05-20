---
name: hashtag-analyzer
description: "Analyze hashtag performance and discover trending tags. Use when: researching hashtags for posts; finding related hashtags; analyzing hashtag reach; planning hashtag strategy; competitor hashtag research"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Hashtag Analyzer

> Analyze and discover effective hashtags for social media marketing campaigns.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures analysis frameworks | Strategic priorities |
| Synthesizes market data | Competitive positioning |
| Identifies opportunities | Resource allocation |
| Creates strategic options | Final strategy selection |
| Suggests implementation approaches | Execution decisions |

## Dependencies

```bash
pip install click requests
```

## Commands

```bash
python scripts/main.py analyze "#marketing" --platform instagram
python scripts/main.py related "#startup" --count 20
python scripts/main.py strategy "@competitor" --platform twitter
```

## Skill Boundaries

### What This Skill Does Well
- Structuring strategic analysis
- Identifying market opportunities
- Creating strategic frameworks
- Synthesizing competitive data

### What This Skill Cannot Do
- Replace market research
- Guarantee strategic success
- Know proprietary competitor info
- Make executive decisions

## Skill Metadata


- **Mode**: centaur
```yaml
category: social
dependencies: [click, requests]
difficulty: beginner
```
