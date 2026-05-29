---
name: perplexity-routing
description: Routing guide for selecting the correct Perplexity tool. Reference before spawning any Perplexity agent.
---

# Perplexity Tool Selection

## Fundamental Distinction

**Search API** (perplexity-search) = Raw results, NO LLM processing
**Sonar Models** (ask/reason/research/sec) = LLM-synthesized answers with citations

## Tool Overview

| Tool | Model | Output | Key Strength |
|------|-------|--------|--------------|
| search | Search API | Raw JSON: {title, URL, snippet, date} | See actual sources, no interpretation |
| ask | sonar-pro (200K ctx, F=0.858) | Synthesized answer + citations | Best factuality for single facts |
| reason | sonar-reasoning-pro (DeepSeek-R1) | Step-by-step analysis + citations | Chain-of-thought for "why" |
| research | sonar-deep-research | Structured report + citations | 10-20+ sources synthesized |
| sec | Python + search_mode='sec' | Synthesized answer from filings | SEC EDGAR only |

## Decision Tree

```
├─ Need raw URLs/sources to process yourself?
│  └─ search (ONLY tool with no LLM - see actual articles)
│
├─ Need official SEC filing content?
│  └─ sec (ONLY tool limited to EDGAR: 10-K, 10-Q, 8-K, S-1)
│
├─ Simple fact? "What is...", "When is...", "How much..."
│  Examples: consensus EPS, stock price, earnings date, revenue guidance
│  └─ ask (fastest synthesized, best factuality)
│
├─ Reasoning? "Why did...", "Compare...", "What caused..."
│  Examples: why stock fell despite beat, AAPL vs MSFT, margin compression cause
│  └─ reason (chain-of-thought, explains logic)
│
└─ Comprehensive analysis? "Full report on...", "Everything about..."
   Examples: earnings attribution, company deep dive, sector analysis
   └─ research (slowest but most thorough)
```

## Cross-References

| Instead of... | Use... | When... |
|---------------|--------|---------|
| research | ask | Single fact (overkill otherwise) |
| research | reason | Single "why" question (faster) |
| ask | reason | Question starts with "why" |
| ask/reason | search | Want to see/filter sources yourself |
| search/ask | sec | Need official regulatory language |
| any | sec | Looking for 10-K, 10-Q, 8-K, S-1 content |

## Speed/Cost

| Tool | Speed | Cost | Use When |
|------|-------|------|----------|
| search | Fastest | Lowest | Building source lists |
| ask | Fast | Low | Quick facts with citation |
| sec | Fast | Low | Official filings |
| reason | Medium | Medium | Causal analysis |
| research | 30+ sec | Highest | Thoroughness > speed |

## Workflows

**Earnings Analysis:**
sec (8-K/10-Q actuals) → ask (consensus estimates) → reason (why stock moved)

**Stock Move Investigation:**
search (news from that day) → reason (causal factors) → research (full attribution if needed)

**Company Research:**
ask (market cap, sector, price) → sec (risk factors, MD&A) → research (comprehensive)

**Finding Analyst Commentary:**
search (get article list) → ask (specific question about coverage)
