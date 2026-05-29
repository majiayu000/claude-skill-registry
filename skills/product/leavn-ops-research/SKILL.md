---
name: Leavn Ops: Research & Competitive Analysis Skill
description: Use this skill when conducting competitor analysis, sentiment monitoring, or user research for Leavn.
allowed-tools: Grep
---

# Leavn Ops: Research & Competitive Analysis Skill

Use this skill when conducting competitor analysis, sentiment monitoring, or user research for Leavn.

## CLI Commands Available

```bash
# Competitor teardown
leavn-ops research competitors "YouVersion,Hallow,Pray.com"

# Sentiment monitoring
leavn-ops research sentiment --topic "bible app" --days 7

# Interview synthesis
leavn-ops research interviews ~/interviews/
```

## Competitor Analysis Framework

### Primary Competitors
1. **YouVersion (Bible App)** - Market leader, massive community
2. **Hallow** - Premium prayer/meditation, Catholic focus
3. **Pray.com** - Audio content, celebrity prayers
4. **Glorify** - Modern design, devotional focus
5. **Abide** - Sleep/meditation focused

### Teardown Template

For each competitor, analyze:

#### Product
- Core features
- Unique differentiators
- UX/UI quality
- Performance

#### Business Model
- Pricing strategy
- Free vs premium split
- Subscription tiers
- Trial offers

#### Marketing
- App Store presence (ASO)
- Social media strategy
- Content marketing
- Paid acquisition

#### Community
- User reviews sentiment
- Social media engagement
- Community features
- Retention strategies

### Competitive Matrix

| Feature | Leavn | YouVersion | Hallow | Pray.com |
|---------|-------|------------|--------|----------|
| Bible | Y | Y | N | N |
| AI Devotionals | Y | N | N | N |
| On-Device AI | Y | N | N | N |
| Prayer Wall | Y | Y | N | Y |
| Audio TTS | Y | Y | Y | Y |
| Offline | Y | Y | Y | N |
| Privacy-First | Y | N | N | N |

### Leavn's Differentiators
1. **On-Device AI**: Privacy-first, no cloud dependency
2. **SwiftUI Native**: True iOS-native experience
3. **Unified Experience**: Bible + Devotional + Prayer in one
4. **Modern Design**: Clean, contemporary aesthetic

## Sentiment Analysis Framework

### Data Sources
1. **Reddit**
   - r/Christianity
   - r/Bible
   - r/Prayer
   - r/TrueChristian
   - r/Reformed

2. **Twitter/X**
   - #BibleApp
   - #ChristianApp
   - #DailyDevotional
   - Competitor mentions

3. **App Store Reviews**
   - Leavn reviews (all ratings)
   - Competitor reviews (1-2 stars = pain points)

### Sentiment Categories
- **Positive**: Praise, recommendations, gratitude
- **Neutral**: Questions, comparisons, information
- **Negative**: Complaints, frustrations, feature requests

### Key Insights to Extract
1. What do users love about existing apps?
2. What frustrates users most?
3. What features are frequently requested?
4. What language do users use to describe their needs?

## User Interview Protocol

### Interview Structure (30-45 min)
1. **Warm-up** (5 min)
   - Background, faith journey

2. **Current Behavior** (10 min)
   - How do they engage with faith daily?
   - What apps/tools do they use?

3. **Pain Points** (10 min)
   - What's frustrating about current solutions?
   - What's missing?

4. **Ideal Solution** (10 min)
   - Magic wand: what would perfect look like?
   - Feature priorities

5. **Wrap-up** (5 min)
   - Any other thoughts
   - Thank you

### Synthesis Framework

After interviews, identify:
1. **Patterns**: What themes appear 3+ times?
2. **Pain Points**: What problems are universal?
3. **Desires**: What features are most wanted?
4. **Personas**: What user types emerge?
5. **Opportunities**: Where can Leavn win?

## Research Best Practices

### Data Collection
- Use web search for recent discussions
- Use Puppeteer for JS-rendered content
- Screenshot/quote notable findings
- Date-stamp all research

### Synthesis
- Look for patterns, not outliers
- Quote users directly when possible
- Quantify findings (X of Y mentioned...)
- Separate facts from interpretation

### Action Items
- Translate insights to product decisions
- Prioritize based on frequency and impact
- Validate with additional research
- Track implementation

## Using Research Outputs

After running research commands:
1. Review templates in `~/.local/share/leavn-ops/outputs/`
2. Fill in actual data from web research
3. Use Claude Code's WebSearch for live data
4. Store insights in Memory MCP for future reference

## Memory Integration

Store key insights:
```
mcp__memory__create_entities({
  entities: [{
    name: "Competitor:Hallow",
    entityType: "competitor",
    observations: ["Premium pricing ($70/yr)", "Catholic focus"]
  }]
})
```

## Output Location
All research saved to: `~/.local/share/leavn-ops/outputs/`
