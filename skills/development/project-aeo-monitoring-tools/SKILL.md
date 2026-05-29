---
name: project-aeo-monitoring-tools
description: Build custom AI search monitoring tools for competitive AEO analysis. Covers API access, scraping architecture, legal compliance, and cost estimation.
version: 1.0.0
tags: [aeo, monitoring, scraping, api, competitive-analysis, engineering]
---

# AEO Monitoring Tools

Build custom infrastructure for monitoring AI search engine visibility and competitive citation analysis.

**Audience**: Engineers building custom AEO monitoring systems
**Related**: For AEO strategy and optimization guidance, see `marketing-ai-search-optimization`

## When to Use This Skill

- Building custom AEO monitoring infrastructure
- Evaluating build vs. buy decisions for AI search tracking
- Understanding API vs. scraping trade-offs per platform
- Designing data pipelines for citation analysis
- Estimating costs for multi-platform monitoring

## Decision Framework: Build vs. Buy

Before building custom tools, evaluate whether commercial solutions fit your needs.

| Factor | Use Commercial Tools | Build Custom |
| ------ | -------------------- | ------------ |
| Budget | <$500/mo | >$2,000/mo in tool costs OR need custom queries |
| Query volume | <500 queries/week | >2,000 queries/week |
| Platform coverage | Standard 5-6 engines | Need niche engines or custom prompts |
| Integration needs | Standard exports (CSV, API) | Deep CRM/analytics integration |
| Engineering capacity | No dedicated engineer | 1+ FTE available |
| Customization | Standard metrics sufficient | Custom scoring, proprietary analysis |

**Commercial tools to evaluate first:**

| Tool | Price | Strengths |
| ---- | ----- | --------- |
| Profound | $499/mo | Full AEO tracking, competitor analysis |
| Semrush One | $199+/mo | Integrated with SEO suite |
| Goodie AI | $495+/mo | Enterprise features |
| Otterly.AI | Contact | ChatGPT/Perplexity focus |
| LLMrefs | Free | Basic citation tracking |

## Platform Access Overview

Each AI platform requires different access approaches.

| Platform | Recommended Approach | API Available | Monthly Cost | Citation Support |
| -------- | -------------------- | ------------- | ------------ | ---------------- |
| Perplexity | Sonar API | Yes (citations native) | $15-30 | Native |
| Gemini | Free API tier | Yes (1,500/day free) | $0 | Extract from response |
| Claude | Claude API | Yes | $75-150 | Extract from response |
| ChatGPT / OpenAI | Official API (use web search tools if available) OR commercial vendor | Yes (varies) | $60-500+ | Varies (official tools or vendor) |
| Google AI Overviews | Commercial tools only | No (typically) | N/A | Commercial tools only |

**Key insight**: Perplexity Sonar API is the most AEO-friendly - it returns citations natively in the response.

See: [references/platform-access-methods.md](references/platform-access-methods.md)

## Architecture Tiers

### Tier 1: API-First (Recommended)

Use official APIs where available. Lowest risk, most maintainable.

```
Query Bank -> API Orchestrator -> Response Store -> Analysis Layer
   (250-500     (rate limiting,    (PostgreSQL/    (citation extraction,
    queries)     retry logic)       BigQuery)       brand detection)
```

**Platforms covered**: Perplexity, Gemini, Claude, OpenAI (baseline; use official web-search tooling if available)
**Cost**: $15-300/mo depending on volume
**Risk**: Low

### Tier 2: Hybrid (API + Commercial Scraping)

Add commercial scraping services for platforms without good APIs.

**Additional coverage**: ChatGPT web interface, Google AI Overviews
**Cost**: $500-1,500/mo (adds commercial scraper fees)
**Risk**: Medium (dependent on scraper provider)

### Tier 3: Full Custom Scraping (Not Recommended)

DIY web scraping of AI platforms.

**Why to avoid**:

- High ToS violation risk
- Aggressive bot detection (especially Google, ChatGPT)
- Maintenance burden (UI changes break scrapers)
- Potential legal liability

See: [assets/technical/architecture-diagrams.md](assets/technical/architecture-diagrams.md)

## Risk Assessment Matrix

| Approach | ToS Risk | Legal Risk | Detection Risk | Recommendation |
| -------- | -------- | ---------- | -------------- | -------------- |
| Official APIs | None | None | None | RECOMMENDED |
| Commercial scraping services | Transferred to provider | Provider's liability | Low | Acceptable with due diligence |
| DIY web scraping | High | Medium-High | High | NOT RECOMMENDED |
| Violating robots.txt | Very High | High | Very High | NEVER |

**Legal developments to monitor**:

- Publisher lawsuits and data sourcing disputes (example: Reddit v. Perplexity AI (2024))
- Platform ToS enforcement and liquidated damages policies (example: X ToS changes)
- Rising use of crawler blocks and WAF rules (GPTBot, ClaudeBot, etc.)

See: [references/legal-compliance.md](references/legal-compliance.md)

## Cost Estimation

| Tier | Components | Monthly Cost |
| ---- | ---------- | ------------ |
| Minimal | Gemini free + Perplexity Sonar + Supabase | $15-50 |
| Standard | Multi-platform APIs + PostgreSQL | $150-300 |
| Comprehensive | APIs + commercial scraping + analytics | $500-1,500 |
| Enterprise | Full coverage + dedicated infrastructure | $2,000+ |

See: [references/cost-estimation.md](references/cost-estimation.md)

## Implementation Timeline

| Week | Focus | Deliverables |
| ---- | ----- | ------------ |
| 1 | Foundation | Query bank (250-500), API accounts, database schema |
| 2 | Core pipeline | API orchestrator, response storage, citation extraction |
| 3 | Analysis | Brand detection, competitor tracking, Share of Model calc |
| 4 | Reporting | Dashboard, alerts, maintenance procedures |

See: [assets/setup/minimal-setup-guide.md](assets/setup/minimal-setup-guide.md)

## What to Load (Progressive Disclosure)

Load additional references based on your needs:

| Reference | When to Load |
| --------- | ------------ |
| [references/platform-access-methods.md](references/platform-access-methods.md) | API setup, rate limits, authentication per platform |
| [references/legal-compliance.md](references/legal-compliance.md) | ToS analysis, compliance checklist, disclaimer language |
| [references/cost-estimation.md](references/cost-estimation.md) | Detailed pricing breakdown, ROI calculation |
| [assets/technical/architecture-diagrams.md](assets/technical/architecture-diagrams.md) | System architecture, data flow diagrams |
| [assets/technical/code-templates.md](assets/technical/code-templates.md) | Python orchestrator, SQL schema, extraction functions |
| [assets/setup/minimal-setup-guide.md](assets/setup/minimal-setup-guide.md) | Step-by-step 4-week implementation guide |

## Quick Start Checklist

```
[ ] Define query bank (250-500 queries by intent)
[ ] Choose platforms to monitor (prioritize by ICP usage)
[ ] Evaluate build vs. buy decision
[ ] If building: Set up API accounts (Perplexity, Gemini, Claude/OpenAI)
[ ] Create database schema (PostgreSQL recommended)
[ ] Build API orchestrator with rate limiting
[ ] Implement citation extraction
[ ] Set up scheduled runs (daily/weekly)
[ ] Create Share of Model dashboard
[ ] Document maintenance procedures
```

## Key Metrics

**Primary metric**: Share of Model (SoM)

```
SoM = (Your brand mentions / Total responses) * 100
```

Track SoM:

- Per platform (ChatGPT, Perplexity, Gemini, Claude)
- Per query intent (informational, commercial, transactional)
- Over time (weekly/monthly trends)
- vs. competitors

**Secondary metrics**:

- Citation rate (% of responses with your URL)
- Position in citations (1st, 2nd, 3rd mention)
- Sentiment of brand mentions
- Query coverage (% of target queries where you appear)

## Related Skills

- `marketing-ai-search-optimization` - AEO strategy, content optimization, measurement methodology
- `software-api-design` - API integration patterns
- `qa-observability` - Monitoring and alerting setup

## Disclaimer

This guidance is for educational purposes. Users must:

- Conduct their own legal review
- Ensure compliance with applicable terms of service
- Respect robots.txt directives
- Follow laws and regulations in their jurisdiction

Building monitoring tools that violate platform ToS may result in account termination, legal action, or both.
