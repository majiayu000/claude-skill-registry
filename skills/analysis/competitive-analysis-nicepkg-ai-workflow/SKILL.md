---
name: competitive-analysis
version: "2.0.0"
description: Competitive intelligence, market analysis, and strategic positioning for product differentiation.
sasmp_version: "1.3.0"
bonded_agent: 01-strategy-vision
bond_type: PRIMARY_BOND
parameters:
  - name: analysis_type
    type: string
    enum: [market_sizing, competitor_research, positioning, battlecard]
    required: true
  - name: competitor_count
    type: number
    default: 5
retry_logic:
  max_attempts: 3
  backoff: exponential
logging:
  level: info
  hooks: [start, complete, error]
---

# Competitive Analysis Skill

Analyze competitors and market dynamics to inform product strategy. Master competitive intelligence and strategic positioning.

## Market Analysis

### TAM/SAM/SOM Calculation

```
TAM (Total Addressable Market):
= Total customers × Average deal size
= 10M companies × $10K = $100B

SAM (Serviceable Addressable Market):
= TAM × Segment % you can reach
= $100B × 10% = $10B

SOM (Serviceable Obtainable Market):
= SAM × Realistic market share (3-5 years)
= $10B × 5% = $500M
```

### Market Dynamics

| Factor | Analysis | Impact |
|--------|----------|--------|
| Growth | CAGR % | High/Med/Low |
| Competition | # players | Fragmented/Consolidated |
| Barriers | Entry difficulty | High/Med/Low |
| Regulation | Compliance needs | Increasing/Stable |

## Competitor Research

### Competitor Matrix

| Feature | You | Comp A | Comp B | Comp C |
|---------|-----|--------|--------|--------|
| Feature 1 | ✓ | ✓ | ✗ | ✓ |
| Feature 2 | ✓ | ✗ | ✓ | ✗ |
| Pricing | $99 | $149 | $79 | $199 |
| Target | SMB | Enterprise | Startup | Mid |

### Competitive Intelligence Sources

- **Public**: Website, pricing, blog, press
- **Product**: Free trial, demo, screenshots
- **Customers**: Win/loss interviews
- **Community**: G2, Capterra, Reddit
- **Industry**: Analyst reports, conferences

## Strategic Frameworks

### Porter's Five Forces

```
Supplier Power: [Low/Med/High]
Buyer Power: [Low/Med/High]
Competitive Rivalry: [Low/Med/High]
Threat of Substitutes: [Low/Med/High]
Threat of New Entrants: [Low/Med/High]
```

### SWOT Analysis

```
STRENGTHS          | WEAKNESSES
- [Internal +]     | - [Internal -]
- [Internal +]     | - [Internal -]
-------------------+-------------------
OPPORTUNITIES      | THREATS
- [External +]     | - [External -]
- [External +]     | - [External -]
```

## Battlecards

### Sales Battlecard Template

```
COMPETITOR: [Name]

POSITIONING:
"[Competitor] is [category] focused on [segment].
We are [differentiator]."

WIN THEMES:
1. [Your advantage 1]
2. [Your advantage 2]
3. [Your advantage 3]

OBJECTION HANDLING:
Q: "Why not [Competitor]?"
A: "[Competitor] is great for [X], but [your advantage]"

GOTCHAS (Their weaknesses):
- [Weakness 1]
- [Weakness 2]
```

## Troubleshooting

### Yaygın Hatalar & Çözümler

| Hata | Olası Sebep | Çözüm |
|------|-------------|-------|
| Outdated intel | No refresh cycle | Quarterly updates |
| Missing competitors | Narrow view | Expand search |
| Feature parity | No differentiation | Find unique angle |
| Lost deals | Weak positioning | Win/loss analysis |

### Debug Checklist

```
[ ] TAM/SAM/SOM assumptions documented mi?
[ ] Competitor list complete mi?
[ ] Feature matrix current mi?
[ ] Battlecards distributed mi?
[ ] Win/loss tracked mi?
```

### Recovery Procedures

1. **Lost Deal** → Win/loss interview, update battlecard
2. **New Competitor** → Rapid assessment, positioning review
3. **Feature Gap** → Prioritize, or reposition

## Learning Outcomes

- Conduct competitive research
- Build competitive matrices
- Create effective battlecards
- Identify market opportunities
- Position against competitors
