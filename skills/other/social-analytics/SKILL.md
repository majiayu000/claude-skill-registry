---
name: social-analytics
description: "Analyze social media profiles and engagement. Use when: auditing competitor social presence; calculating engagement rates; identifying top-performing content; tracking profile growth; benchmarking social metrics"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Social Analytics

> Analyze social media profiles and calculate engagement metrics - understand what content works for competitors and your own accounts.

## When to Use This Skill

- **Competitor analysis** - Audit competitor social presence
- **Engagement benchmarking** - Calculate and compare engagement rates
- **Content analysis** - Identify top-performing post types
- **Profile audit** - Assess social media health
- **Reporting** - Generate social performance reports


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
pip install click pandas requests beautifulsoup4
# For authenticated API access:
pip install tweepy instaloader
```

## Commands

### Analyze Profile
```bash
python scripts/main.py analyze @competitor --platform twitter
python scripts/main.py analyze @brand --platform instagram
```

### Calculate Engagement
```bash
python scripts/main.py engagement @profile --platform twitter --days 30
python scripts/main.py engagement @profile --platform linkedin --posts 50
```

### Find Top Posts
```bash
python scripts/main.py top-posts @profile --platform twitter --count 10
python scripts/main.py top-posts @profile --metric likes
```

### Export Data
```bash
python scripts/main.py export @profile --platform twitter --format csv
python scripts/main.py export @profile --platform instagram --output report.json
```

### Compare Profiles
```bash
python scripts/main.py compare @brand1 @brand2 @brand3 --platform twitter
```

## Examples

### Example 1: Competitor Social Audit
```bash
# Analyze competitor profile
python scripts/main.py analyze @competitor_brand --platform twitter

# Output:
# Profile Analysis: @competitor_brand
# ─────────────────────────────────────
# Followers:      45,230
# Following:      1,234
# Total Posts:    2,456
# Avg Likes:      234
# Avg Retweets:   45
# Engagement:     2.3%
# Post Frequency: 3.2/day
# Top Hashtags:   #marketing, #growth, #startup
```

### Example 2: Benchmark Engagement Rates
```bash
# Compare engagement across competitors
python scripts/main.py compare @brand1 @brand2 @brand3 --platform twitter

# Output:
# Engagement Comparison
# ─────────────────────
# Profile         Followers   Eng.Rate   Posts/Day
# @brand1         45,230      2.3%       3.2
# @brand2         32,100      3.1%       2.1
# @brand3         89,500      1.8%       4.5

# Winner: @brand2 (highest engagement despite fewer followers)
```

### Example 3: Find Winning Content
```bash
# Identify top performing posts
python scripts/main.py top-posts @marketing_pro --platform twitter --count 10

# Output:
# Top 10 Posts by Engagement
# ──────────────────────────
# 1. "Here's what nobody tells you about..."
#    Likes: 2,345  RTs: 456  Eng: 6.2%
#    Type: Thread  Time: Tuesday 9am

# 2. "The biggest mistake I see founders make..."
#    Likes: 1,890  RTs: 312  Eng: 4.8%
#    Type: Single  Time: Wednesday 8am
```

## Engagement Rate Benchmarks

### Twitter/X
| Account Size | Good | Great | Excellent |
|--------------|------|-------|-----------|
| <10K | 1-3% | 3-6% | >6% |
| 10K-100K | 0.5-1% | 1-3% | >3% |
| 100K+ | 0.2-0.5% | 0.5-1% | >1% |

### Instagram
| Account Size | Good | Great | Excellent |
|--------------|------|-------|-----------|
| <10K | 3-6% | 6-10% | >10% |
| 10K-100K | 1-3% | 3-6% | >6% |
| 100K+ | 0.5-1% | 1-3% | >3% |

### LinkedIn
| Account Size | Good | Great | Excellent |
|--------------|------|-------|-----------|
| Personal | 2-4% | 4-8% | >8% |
| Company | 0.5-1% | 1-2% | >2% |

## Metrics Explained

| Metric | Formula | What It Measures |
|--------|---------|------------------|
| **Engagement Rate** | (likes + comments + shares) / followers | Overall content resonance |
| **Amplification** | shares / followers | Content virality |
| **Conversation** | comments / followers | Community engagement |
| **Applause** | likes / followers | Content appreciation |

## Output Formats

| Format | Best For |
|--------|----------|
| `text` | Quick terminal review |
| `csv` | Spreadsheet analysis |
| `json` | Programmatic use |
| `md` | Reports and docs |

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

## Related Skills

- [content-repurposer](../../automation/content-repurposer/) - Repurpose top-performing content
- [hashtag-analyzer](../hashtag-analyzer/) - Deep dive into hashtag performance

## Skill Metadata


- **Mode**: centaur
```yaml
category: social
subcategory: analytics
dependencies: [pandas, requests, beautifulsoup4]
difficulty: intermediate
time_saved: 4+ hours/week
```
