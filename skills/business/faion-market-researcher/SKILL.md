---
name: faion-market-researcher
description: "Market research: TAM/SAM/SOM sizing, competitor analysis, pricing research, trend analysis."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, Task, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Market Research Domain Skill

**Communication: User's language. Docs: English.**

## Purpose

Market research and business analysis for product/startup development. Handles market sizing, competitor intelligence, pricing benchmarking, trend analysis, niche evaluation, and business model planning.

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| `.aidocs/product_docs/` | Market research docs, competitor analysis | Research artifacts |
| Business plan | TAM/SAM/SOM calculations | Market sizing done |
| Competitor docs | Competitor profiles, SWOT | Competitive intel |
| Pricing sheets | Pricing models, benchmarks | Pricing research |
| Trend reports | Market trends, forecasts | Trend analysis |

### Discovery Questions

```yaml
questions:
  - question: "What research do you need?"
    options:
      - label: "Market size (TAM/SAM/SOM)"
        description: "Use market-research-tam-sam-som"
      - label: "Competitor analysis"
        description: "Use competitor-analysis, competitive-intelligence-methods"
      - label: "Pricing research"
        description: "Use pricing-research"
      - label: "Trend analysis"
        description: "Use trend-analysis"

  - question: "What's your business stage?"
    options:
      - label: "Idea validation"
        description: "Use market-research-tam-sam-som, niche-evaluation"
      - label: "Pre-launch planning"
        description: "Use competitor-analysis, pricing-research"
      - label: "Growth stage"
        description: "Use trend-analysis, competitive-intelligence"

  - question: "Do you have existing market data?"
    options:
      - label: "Yes, need to update"
        description: "Update existing research docs"
      - label: "Partial data"
        description: "Fill gaps with targeted research"
      - label: "No data yet"
        description: "Start with market-research-tam-sam-som"
```

---

## Quick Reference

| Research Area | Key Files |
|---------------|-----------|
| **Market Sizing** | market-research-tam-sam-som.md, market-sizing-with-ai.md, market-analysis.md |
| **Competitors** | competitor-analysis.md, competitive-intelligence-methods.md, competitive-intelligence.md |
| **Pricing** | pricing-research.md, business-model-planning.md |
| **Trends** | trend-analysis.md, product-development-trends-2026.md |
| **Niche** | niche-evaluation.md, business-model-research.md |
| **Ideas** | idea-generation.md, idea-generation-methods.md |
| **Tools** | ai-research-tools.md, perplexity-ai-research.md |

---

## Decision Tree

| If you need... | Use |
|---------------|-----|
| Market size (TAM/SAM/SOM) | market-research-tam-sam-som.md |
| Competitor landscape | competitor-analysis.md, competitive-intelligence-methods.md |
| Pricing benchmarks | pricing-research.md |
| Market trends | trend-analysis.md |
| Niche viability | niche-evaluation.md |
| Business model options | business-model-planning.md, business-model-research.md |
| Generate ideas | idea-generation.md, idea-generation-methods.md |
| Distribution strategy | distribution-channel-research.md |
| Risk assessment | risk-assessment.md |
| Project naming | naming-and-domains.md |

---

## Research Modes

| Mode | Output | Files Used |
|------|--------|------------|
| market | market-research.md | market-research-tam-sam-som.md, market-analysis.md |
| competitors | competitive-analysis.md | competitor-analysis.md, competitive-intelligence-methods.md |
| pricing | pricing-research.md | pricing-research.md, business-model-planning.md |
| niche | niche-evaluation.md | niche-evaluation.md, business-model-research.md |
| trends | trend-analysis.md | trend-analysis.md, product-development-trends-2026.md |
| ideas | idea-candidates.md | idea-generation.md, idea-generation-methods.md |

---

## Methodologies (22)

### Market Analysis (5)
- TAM/SAM/SOM framework
- Market sizing with AI
- Market opportunity assessment
- Trend analysis
- Continuous discovery

### Competitive Intelligence (3)
- Competitor analysis
- Competitive intelligence gathering
- Competitive intelligence methods

### Business Planning (5)
- Business model research
- Business model planning
- Niche evaluation
- Risk assessment
- Distribution channel research

### Pricing Strategy (1)
- Pricing research & benchmarking

### Idea Generation (3)
- Idea generation (7 Ps framework)
- Idea generation methods
- Product development trends

### Tools & Methods (5)
- AI research tools
- AI research tool categories
- Perplexity AI research
- Naming & domains
- Product development trends 2026

---

## Key Frameworks

| Framework | Purpose | File |
|-----------|---------|------|
| **TAM/SAM/SOM** | Market sizing (top-down/bottom-up) | market-research-tam-sam-som.md |
| **Porter's Five Forces** | Competitive dynamics | competitive-intelligence-methods.md |
| **7 Ps** | Idea generation | idea-generation-methods.md |
| **Niche Scoring** | Viability assessment (5 criteria) | niche-evaluation.md |
| **Business Model Canvas** | Model planning | business-model-planning.md |

---

## Output Files

All outputs go to `.aidocs/product_docs/`:

| Module | Output File |
|--------|-------------|
| Market Research | market-research.md |
| Competitors | competitive-analysis.md |
| Pricing | pricing-research.md |
| Niche | niche-evaluation.md |
| Ideas | idea-candidates.md |
| Trends | trend-analysis.md |

---

## Integration

### Parent Skill
Orchestrated by `faion-researcher` skill.

### Related Sub-Skills
- **faion-user-researcher** - User personas, interviews, validation

### Next Steps
After market research complete:
- User research → `faion-user-researcher`
- GTM planning → `faion-marketing-manager`
- Product spec → `faion-sdd`

---

*faion-market-researcher v1.0*
*Sub-skill of faion-researcher*
*22 methodologies | Market & Business Intelligence*
