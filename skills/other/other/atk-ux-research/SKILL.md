---
name: atk-ux-research
description: Conduct comprehensive UX research for America's Test Kitchen across any feature area (recipes, equipment, subscription, app experience, billing, etc.). Uses Exa Search, Firecrawl, Perplexity MCP, and Reddit JSON API to gather user feedback from app stores, Reddit, Trustpilot, BBB, and other review sources. Outputs structured research reports with quantitative metrics and qualitative themes.
---

# America's Test Kitchen UX Research

Modular skill for conducting UX research on any ATK feature or experience area.

## When to Use This Skill

Use this skill when:
- Researching user feedback for any ATK feature (equipment, recipes, subscription, app, etc.)
- Gathering app store reviews (iOS/Android)
- Scraping Reddit discussions about ATK
- Collecting BBB complaints and Trustpilot reviews
- Creating UX research reports with findings and recommendations
- Comparing ATK to competitors (NYT Cooking, Serious Eats, etc.)

## Quick Start

```bash
# Run research on a specific feature area
python3 ~/.claude/skills/atk-ux-research/scripts/atk_research.py --feature "recipes"
python3 ~/.claude/skills/atk-ux-research/scripts/atk_research.py --feature "subscription"
python3 ~/.claude/skills/atk-ux-research/scripts/atk_research.py --feature "app experience"
```

## Feature Areas

| Feature | Description | Key Sources |
|---------|-------------|-------------|
| `equipment` | Kitchen gear and product reviews | App stores, Reddit, BBB |
| `recipes` | Recipe content and usability | Reddit, App stores |
| `subscription` | Billing, pricing, cancellation | BBB, Trustpilot, Reddit |
| `app` | App stability, UX, navigation | App stores, Reddit |
| `video` | TV shows, streaming, video content | Reddit, social media |
| `cookbooks` | Physical book purchases and quality | Reddit, Trustpilot |

## Research Workflow

### Phase 1: Data Collection

#### 1.1 App Store Reviews

```bash
# iOS App Store
firecrawl https://apps.apple.com/us/app/americas-test-kitchen/id1365223384

# Google Play Store
firecrawl https://play.google.com/store/apps/details?id=com.americastestkitchen.groceryapp
```

#### 1.2 Review Sites

```bash
# Trustpilot
firecrawl https://www.trustpilot.com/review/www.americastestkitchen.com

# BBB Complaints
firecrawl https://www.bbb.org/us/ma/boston/profile/publishers-periodical/americas-test-kitchen-lp-0021-66446/complaints
```

#### 1.3 Reddit (JSON API)

Reddit blocks standard scrapers. Use the `.json` suffix:

```bash
# Get subreddit posts
curl -s "https://www.reddit.com/r/AmericasTestKitchen/top.json?t=year&limit=25" \
  -H "User-Agent: ux-research/1.0" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for post in data['data']['children']:
    p = post['data']
    print(f\"**{p['title']}** (score: {p['score']}, comments: {p['num_comments']})\")
    print(f\"  https://reddit.com{p['permalink']}\n\")"

# Get thread comments
curl -s "https://www.reddit.com/r/AmericasTestKitchen/comments/THREAD_ID.json?limit=50" \
  -H "User-Agent: ux-research/1.0" | python3 -c "
import sys, json
data = json.load(sys.stdin)
comments = data[1]['data']['children']
for c in comments[:20]:
    if c['kind'] == 't1':
        d = c['data']
        print(f\"**{d['author']}** (score: {d['score']}):\n{d['body'][:500]}\n---\")"

# Search for feature-specific discussions
curl -s "https://www.reddit.com/r/Cooking/search.json?q=america%27s+test+kitchen+FEATURE&restrict_sr=0&limit=20" \
  -H "User-Agent: ux-research/1.0"
```

**Key Subreddits:**
- r/AmericasTestKitchen - Dedicated ATK community
- r/Cooking - General cooking discussions
- r/Costco - Cookbook/product finds
- r/BuyItForLife - Equipment durability
- r/AskCulinary - Recipe questions

#### 1.4 Exa Search

```bash
# Neural search for user feedback
python3 ~/.claude/skills/exa-search/scripts/exa_search.py \
  "America's Test Kitchen FEATURE user feedback reviews" \
  --category news -n 15

# Research with citations
python3 ~/.claude/skills/exa-search/scripts/exa_research.py \
  "What do users say about America's Test Kitchen FEATURE?" \
  --sources --markdown
```

#### 1.5 Perplexity MCP

```
mcp__perplexity__search: "America's Test Kitchen FEATURE user complaints feedback"
mcp__perplexity__get_documentation: "ATK app store reviews analysis"
```

### Phase 2: Analysis

#### 2.1 Quantitative Metrics

| Metric | Source | How to Get |
|--------|--------|------------|
| iOS Rating | App Store | Firecrawl scrape |
| Android Rating | Google Play | Firecrawl scrape |
| BBB Complaints | BBB | Count from scrape |
| Trustpilot Score | Trustpilot | Firecrawl scrape |
| Reddit Engagement | Reddit JSON | Sum scores/comments |

#### 2.2 Qualitative Themes

Code feedback into themes:
- **Discoverability** - Can users find the feature?
- **Usability** - Is it easy to use?
- **Reliability** - Does it work consistently?
- **Value** - Is it worth the price?
- **Support** - How are issues resolved?

#### 2.3 Severity Classification

| Severity | Criteria |
|----------|----------|
| Critical | Prevents core functionality, multiple sources confirm |
| High | Significant friction, frequent complaints |
| Medium | Annoyance, moderate complaint frequency |
| Low | Nice-to-have improvements |

### Phase 3: Report Generation

Use template at: `~/.claude/skills/atk-ux-research/templates/report-template.md`

#### Report Sections

1. **Executive Summary** - Key findings, severity table
2. **Methodology** - Sources, sample sizes, limitations
3. **Quantitative Overview** - Ratings, complaint distribution
4. **Feature Analysis** - Deep dive on researched feature
5. **User Pain Points** - Themed complaints with evidence
6. **Positive Feedback** - What users appreciate
7. **Recommendations** - Prioritized improvements
8. **Appendix** - Source URLs, raw data references

## Output Locations

```
~/Desktop/ATK-UX-Research/
├── reports/                    # Generated reports
│   └── FEATURE-YYYY-MM-DD.md
├── scraped-data/              # Raw scraped content
│   ├── app-store/
│   ├── reddit/
│   └── review-sites/
└── research-plan.md           # Active research plan
```

## Competitor Comparison

When benchmarking, compare against:

| Competitor | Focus | URL |
|------------|-------|-----|
| NYT Cooking | Recipes, no equipment | cooking.nytimes.com |
| Serious Eats | Recipes + equipment | seriouseats.com |
| Wirecutter | Equipment only | nytimes.com/wirecutter |
| Consumer Reports | Equipment reviews | consumerreports.org |
| King Arthur | Baking focus | kingarthurbaking.com |

## Known Limitations

- **Facebook Groups**: Not accessible via API, requires manual research
- **App Store Historical Data**: Need AppFollow/Sensor Tower for trends
- **Reddit Rate Limits**: Use 2-second delays between requests
- **Trustpilot**: Limited ATK reviews (only 4 as of Jan 2026)

## Environment Variables

```bash
# Required for full functionality
export EXA_API_KEY="your-key"
export FIRECRAWL_API_KEY="your-key"
```

## Example Usage

### Research Equipment Feature

```bash
# 1. Gather data
firecrawl https://apps.apple.com/us/app/americas-test-kitchen/id1365223384
firecrawl https://www.trustpilot.com/review/www.americastestkitchen.com

# 2. Search Reddit
curl -s "https://www.reddit.com/r/AmericasTestKitchen/search.json?q=equipment&limit=20" \
  -H "User-Agent: ux-research/1.0"

# 3. Exa research
python3 ~/.claude/skills/exa-search/scripts/exa_research.py \
  "America's Test Kitchen equipment reviews user experience" --sources

# 4. Generate report
# Use report template and synthesize findings
```

### Research Subscription/Billing

```bash
# Focus on BBB and cancellation complaints
firecrawl https://www.bbb.org/us/ma/boston/profile/publishers-periodical/americas-test-kitchen-lp-0021-66446/complaints

curl -s "https://www.reddit.com/r/AmericasTestKitchen/search.json?q=cancel+subscription&limit=20" \
  -H "User-Agent: ux-research/1.0"

python3 ~/.claude/skills/exa-search/scripts/exa_research.py \
  "America's Test Kitchen subscription billing complaints auto-renewal" --sources
```

## Integration with Project

This skill outputs to the ATK-UX-Research git repository:
- `/Users/tomdimino/Desktop/ATK-UX-Research/`

Commit findings after each research session.
