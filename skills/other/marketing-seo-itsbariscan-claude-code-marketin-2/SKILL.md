---
name: marketing-seo
description: SEO keyword research, content planning, and competitor analysis with anti-hallucination gates
keywords: [seo, keywords, content, marketing, keyword research, content brief, competitor analysis]
---

# SEO Skills

Keyword research, content planning, and competitor analysis with reasoning-based analysis and optional MCP enhancement.

---

## The Iron Law

```
NO METRICS WITHOUT SOURCE DECLARATION
```

Always state whether analysis is reasoning-based or MCP-enhanced.
Violating the letter of this rule is violating the spirit.

---

## Data Source Detection

At the start of any SEO task, identify available data sources:

### Check for MCP Tools

**IF Ahrefs MCP available** (tools contain `ahrefs_`):
- Use for: Volume, Keyword Difficulty, Backlinks, Domain Rating
- Confidence: HIGH
- Label: "Analysis enhanced with Ahrefs data"

**IF SEMrush MCP available** (tools contain `semrush_`):
- Use for: Volume, Keyword Difficulty, Competitor keywords, Domain overview
- Confidence: HIGH
- Label: "Analysis enhanced with SEMrush data"

**IF GSC MCP available** (tools contain `gsc_` or `search_console`):
- Use for: Current rankings, Impressions, Clicks, CTR
- Confidence: HIGH
- Label: "Analysis enhanced with Search Console data"

**IF user pastes data**:
- Parse CSV/TSV format
- Confidence: MEDIUM
- Label: "Analysis based on provided data"

**IF no MCP and no paste**:
- Use reasoning based on SEO principles
- Confidence: MEDIUM
- Label: "Reasoning-based analysis"

---

## Keyword Research

### When to Use

- "find keywords for [topic]"
- "keyword research for [industry]"
- "what should I rank for"
- "analyze these keywords"

### Data Source Gate

BEFORE analyzing keywords:

1. **CHECK for MCP tools** (Ahrefs, SEMrush, GSC)
2. **CHECK for pasted data** from user
3. **DECLARE data source** in output header

### Analysis Framework

| Factor | With MCP/Data | Reasoning-Based |
|--------|---------------|-----------------|
| **Volume** | Exact number from API | "Likely [high/medium/low] based on term type" |
| **Difficulty** | KD score from API | "Likely [easy/medium/hard] based on keyword structure" |
| **Intent** | Same analysis method | Same analysis method |
| **Position** | From GSC if available | "Unknown - connect GSC for current rankings" |

### Output Format

**With MCP Enhancement:**
```
📊 KEYWORD ANALYSIS

**Data Source:** [Ahrefs/SEMrush] MCP + Reasoning
**Confidence:** High

| Priority | Keyword | Volume | KD | Intent | Reasoning |
|----------|---------|--------|----|---------| ----------|
| 🏆 Quick Win | "keyword" | 2,400 | 23 | Commercial | Low difficulty, good volume |

Analysis enhanced with live [tool] data.
```

**Reasoning-Based:**
```
📊 KEYWORD ANALYSIS

**Data Source:** Reasoning-based
**Confidence:** Medium

| Priority | Keyword | Volume | KD | Intent | Reasoning |
|----------|---------|--------|----|---------| ----------|
| 🏆 Quick Win | "keyword" | ~2-5K est. | Likely easy | Commercial | Long-tail, specific modifier |

Based on SEO principles and keyword structure.
```

---

## Content Planning

### When to Use

- "plan content for [topic]"
- "create content calendar"
- "content brief for [keyword]"
- "what should I write about"

### Prerequisites Gate

BEFORE creating content plans:

1. ✅ Keyword analysis done? (If not: do keyword research first)
2. ✅ Brand context loaded? (If not: `/brand switch [name]`)
3. ✅ Declare data sources in output

### Placeholder Prohibition

NEVER output placeholders like:
- "[Topic]"
- "[First Step]"
- "Main Point 1"

Either generate specific content or ask for the information.

### Content Brief Format

```
📝 CONTENT BRIEF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 **Title:** [Actual title]
🎯 **Target Keyword:** [keyword]
📊 **Word Count:** [range] words
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Search Intent
[What the searcher wants - be specific]

## Target Audience
[From brand context or ask]

## Outline

### H2: [Actual heading]
- Key point
- Key point

### H2: [Actual heading]
- Key point

## Key Points to Cover
- [ ] [Specific point]
- [ ] [Specific point]

## Call to Action
[Based on intent + brand model]

**Data Sources:** [List what informed this brief]
```

---

## Competitor Analysis

### When to Use

- "analyze [competitor]"
- "competitor analysis"
- "find competitor keywords"
- "SEO gap analysis"

### Data Source Options

**With Ahrefs/SEMrush MCP:**
- Pull competitor's top keywords
- Get backlink profile
- Domain authority/rating
- Traffic estimates

**Without MCP:**
- Analyze their visible content
- Review their site structure
- Infer target keywords from page titles/URLs
- Use web search to research competitor public content

---

## Red Flags - STOP

If you catch yourself:
- Stating specific numbers (5,000 searches) without MCP data or paste
- Claiming "difficulty is 45" without KD source
- Saying "this is a quick win" without ranking data
- Making competitor claims without evidence

**STOP. Declare it as reasoning-based or ask for data.**

---

## Verification Checklist

BEFORE presenting SEO analysis:

- [ ] Data source declared in header?
- [ ] Confidence level stated?
- [ ] Numbers sourced or marked as estimates?
- [ ] No unsupported "quick win" claims?

If any unchecked: Fix before presenting.
