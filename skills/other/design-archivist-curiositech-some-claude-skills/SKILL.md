---
name: design-archivist
description: Long-running design anthropologist that builds comprehensive visual databases from 500-1000 real-world examples, extracting color palettes, typography patterns, layout systems, and interaction design across any domain (portfolios, e-commerce, SaaS, adult content, technical showcases). This skill should be used when users need exhaustive design research, pattern recognition across large example sets, or systematic visual analysis for competitive positioning.
allowed-tools: Read,Write,WebSearch,WebFetch
category: Research & Analysis
tags:
  - design-research
  - patterns
  - analysis
  - visual-database
  - trends
pairs-with:
  - skill: web-design-expert
    reason: Apply researched patterns to designs
  - skill: competitive-cartographer
    reason: Design-focused competitive analysis
---

# Design Archivist

A design anthropologist that systematically builds visual databases through large-scale analysis of real-world examples. **This is a long-running skill** designed for multi-day research (2-7 days for 500-1000 examples).

## Quick Start

```
User: "Research design patterns for fintech apps targeting Gen Z"

Archivist:
1. Define scope: "fintech landing pages, Gen Z audience (18-27)"
2. Set target: 500 examples over 2-3 days
3. Identify seeds: Venmo, Cash App, Robinhood, plus competitors
4. Begin systematic crawl with checkpoints every 10 examples
5. After 48 hours: Deliver pattern database with:
   - Color trends
   - Typography patterns
   - Layout systems
   - White space opportunities
```

## When to Use

**Use for:**
- Exhaustive design research (300-1000 examples)
- Pattern recognition across large example sets
- Competitive visual analysis
- Trend identification with data backing
- Domain-specific design language extraction

**NOT for:**
- Quick design inspiration (use Dribbble/Awwwards directly)
- Single example analysis
- Small samples (&lt;50 examples)
- Real-time trend spotting (this takes days)

## Core Process

### 1. Domain Initialization
- Define target domain and audience
- Set target count (300-1000 based on specificity)
- Identify seed URLs or search queries
- Establish focus areas

### 2. Systematic Crawling
For each example:
1. Capture visual snapshot
2. Record metadata (URL, timestamp, context)
3. Extract Visual DNA (colors, typography, layout, interactions)
4. Analyze contextual signals (audience, positioning, success indicators)
5. Apply categorical tags
6. **Save checkpoint every 10 examples**

### 3. Pattern Extraction
After accumulating examples, identify:
- **Dominant patterns** - The "norm" (most common approaches)
- **Emerging patterns** - The "future" (gaining traction)
- **Deprecated patterns** - The "past" (avoid these)
- **Outlier patterns** - The "experimental" (unique approaches)

## Visual DNA Extraction

For each example, extract:

| Category | What to Extract |
|----------|-----------------|
| **Colors** | Palette, primary/secondary/accent, dominance percentages |
| **Typography** | Font families, weights, sizes, hierarchy |
| **Layout** | Grid system, spacing base, structure, whitespace |
| **Interactions** | Hover effects, transitions, scroll behaviors |
| **Animation** | Presence level, types, timing |

See `references/data_structures.md` for full TypeScript interfaces.

## Domain Quick Reference

| Domain | Focus Areas | Seed Sources |
|--------|-------------|--------------|
| **Portfolios** | Clarity, credibility, storytelling | Awwwards, Dribbble, Behance |
| **SaaS Landing** | Conversion, trust signals, pricing | Product Hunt, SaaS directories |
| **E-Commerce** | Product photos, checkout, mobile | Shopify stores, major retailers |
| **Adult Content** | Premium positioning, discretion | Adult ad networks, VR platforms |
| **Technical Demos** | Visual drama, performance, interactivity | Shadertoy, Codrops, ArtStation |

See `references/domain_guides.md` for detailed domain strategies.

## Long-Running Infrastructure

### Checkpointing Strategy
- Save checkpoint every 10 examples
- Include job ID, progress count, queue state, timestamp
- Keep last 3 checkpoints as backup

### Progress Reporting
Report at intervals:
- "Analyzed 250/1000 examples (25% complete)"
- "Current rate: 100 examples/day"
- "Estimated completion: 7 days"
- "Top emerging pattern: glassmorphic cards (15% of recent examples)"

### Rate Limiting
- Max 1 request per second per domain
- Respect robots.txt
- Implement exponential backoff on errors

## Anti-Patterns

### 1. Scraping Too Aggressively
**Symptom:** Requests every 100ms, same domain hammered repeatedly
**Fix:** 1 request/second max, respect robots.txt, exponential backoff

### 2. No Checkpointing
**Symptom:** Running 24 hours straight without saving
**Fix:** Save every 10 examples with timestamp and queue state

### 3. Ignoring Domain Context
**Symptom:** Applying e-commerce patterns to portfolio sites
**Fix:** Research domain-specific best practices first

### 4. Analysis Paralysis
**Symptom:** 30 minutes per example across 1000 examples
**Fix:** Batch process in groups of 10, deep-dive only on outliers

### 5. Insufficient Diversity
**Symptom:** Only analyzing top-tier examples
**Fix:** Include leaders, mid-tier, and independents; geographic diversity

### 6. Ignoring Historical Context
**Symptom:** Treating all patterns as current
**Fix:** Use Wayback Machine, note when patterns emerged, track evolution

## Output Format

Generate comprehensive research packages with:
- **Meta**: Domain, count, date range, depth
- **Examples**: Full visual database
- **Patterns**: Dominant, emerging, deprecated, outlier
- **Insights**: Color/typography/layout/interaction trends
- **Recommendations**: Safe choices, differentiators, patterns to avoid

## Cost and Scale

For 1000-example analysis:
| Item | Cost |
|------|------|
| Screenshots | ~$20 (Playwright cloud @ $0.02/each) |
| LLM Analysis | ~$15 (100 batches × $0.15) |
| Storage | ~$0.01 (200MB) |
| **Total** | **~$35** |
| **Runtime** | 48-72 hours |

Inform users of scope and cost before beginning.

## Reference Files

| File | Contents |
|------|----------|
| `references/data_structures.md` | TypeScript interfaces for VisualDNA, ContextAnalysis, Checkpoint |
| `references/domain_guides.md` | Detailed domain-specific strategies and focus areas |

---

**Covers:** Design Research | Pattern Recognition | Visual Analysis | Competitive Intelligence

**Use with:** web-design-expert (apply findings) | competitive-cartographer (market context)
