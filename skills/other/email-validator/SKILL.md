---
name: email-validator
description: "Validate and clean email lists. Use when: cleaning email lists before campaigns; validating signup emails; removing invalid addresses; checking for disposable emails; improving deliverability"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Email Validator

> Validate email addresses and clean lists to improve deliverability and reduce bounces.


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
pip install email-validator dnspython click
```

## Commands

```bash
python scripts/main.py validate email@example.com
python scripts/main.py batch emails.csv --column email --output clean.csv
python scripts/main.py clean emails.txt --remove-disposable
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
category: email-tools
dependencies: [email-validator, dnspython]
difficulty: beginner
```
