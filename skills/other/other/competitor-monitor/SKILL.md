---
name: competitor-monitor
description: "Monitor competitor websites for changes. Use when: tracking competitor pricing changes; monitoring new features; watching for content updates; alerting on website changes; competitive intelligence"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Competitor Monitor

> Track competitor websites for changes and get alerts - stay informed about pricing, features, and content updates.

## When to Use This Skill

- **Pricing intelligence** - Track competitor price changes
- **Feature tracking** - Monitor new feature announcements
- **Content watch** - Track new blog posts or pages
- **Change alerts** - Get notified of website updates
- **Competitive analysis** - Regular competitor audits


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
pip install beautifulsoup4 requests click
# For diff comparison:
pip install diff-match-patch
```

## Commands

### Watch URL
```bash
python scripts/main.py watch https://competitor.com/pricing
python scripts/main.py watch https://competitor.com/pricing --selector ".price"
```

### Check Changes
```bash
python scripts/main.py diff https://competitor.com/pricing --baseline cache.html
```

### Monitor Pricing
```bash
python scripts/main.py pricing https://competitor.com/pricing
```

### Batch Monitor
```bash
python scripts/main.py batch competitors.txt --output changes/
```

## Examples

### Example 1: Track Pricing Changes
```bash
# First, capture baseline
python scripts/main.py watch https://competitor.com/pricing --save baseline.html

# Later, check for changes
python scripts/main.py diff https://competitor.com/pricing --baseline baseline.html

# Output:
# Changes Detected!
# ─────────────────────
# - Starter: $29/mo → $39/mo (+34%)
# - Pro: $99/mo (unchanged)
# + New: Enterprise tier added
```

### Example 2: Monitor Multiple Competitors
```bash
# Create competitor list
cat > competitors.txt << EOF
https://competitor1.com/pricing
https://competitor2.com/pricing
https://competitor3.com/features
EOF

# Run batch monitor
python scripts/main.py batch competitors.txt --output ./snapshots/

# Output: Creates timestamped snapshots for each URL
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

## Related Skills

- [web-scraper](../web-scraper/) - Extract detailed data
- [lighthouse-audit](../../seo-tools/lighthouse-audit/) - Audit competitor performance

## Skill Metadata


- **Mode**: centaur
```yaml
category: automation
subcategory: competitive-intelligence
dependencies: [beautifulsoup4, requests]
difficulty: intermediate
time_saved: 4+ hours/week
```
