---
name: kai-surround-sound
description: LLM brand manipulation — build a consensus web so ChatGPT, Claude, Perplexity, and Google AI Overviews mention your brand when people ask about your category. Uses surround sound methodology, entity SEO, and LLM citation science. Use when "get mentioned in AI", "LLM brand presence", "surround sound", "AI search visibility", "Perplexity ranking", "ChatGPT mentions", "AI Overview inclusion", "entity authority", "brand mentions in AI", or any request to influence how AI systems perceive and recommend your brand.
---

Build a consensus web that makes LLMs mention your brand. The bleeding edge of marketing.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Entity Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Brand/product** — what should AI mention?
2. **Category** — when someone asks "[what's the best X]", what's X?
3. **Current AI presence** — test: ask ChatGPT/Perplexity "what's the best [category]?" — are you mentioned?
4. **Competitors mentioned** — who IS being mentioned by AI when you're not?
5. **Existing content assets** — blog, social, press, directories, forums?

## Phase 2: Consensus Audit

Load these before starting:
- `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\surround-sound-llm-manipulation.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\llm-citation-tracking.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\entity-seo-knowledge-graph-deep-dive.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\perplexity-ranking-reverse-engineered.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\geo-academic-research-synthesis.md`

### Audit the Current Consensus Web

Map where your brand appears (and doesn't) across LLM training/retrieval sources:

| Source Type | Examples | Your Presence | Competitor Presence |
|------------|---------|---------------|-------------------|
| **Your domain** | Blog, landing pages, docs | [Y/N] | N/A |
| **Third-party articles** | Review sites, "best of" lists, comparisons | [Y/N] | [who?] |
| **Forums** | Reddit, Quora, HN, industry forums | [Y/N] | [who?] |
| **Directories** | G2, Capterra, Product Hunt, industry directories | [Y/N] | [who?] |
| **Social platforms** | LinkedIn, X, YouTube | [Y/N] | [who?] |
| **Wikipedia/reference** | Wikipedia, Crunchbase, knowledge bases | [Y/N] | [who?] |
| **Academic/research** | Papers, case studies, whitepapers cited | [Y/N] | [who?] |
| **Press/media** | News articles, press releases, interviews | [Y/N] | [who?] |

### Own-Domain Agent-Readiness Audit

Before you can surround-sound from third parties, your own site has to be legible to the agents routing back. If ChatGPT can't parse your homepage, every pulse you build elsewhere dead-ends.

Load: `E:\Dev2\kai-cmo-harness-work\knowledge\checklists\agent-readiness-checklist.md`

Run the checklist against the user's primary domain. Report:

| Check | Status | Evidence |
|-------|--------|----------|
| `/robots.txt` explicit AI bot rules | [Pass/Partial/Fail] | [what's there] |
| `/llms.txt` entrypoint exists and valid | [Pass/Partial/Fail] | [url or missing] |
| Markdown mirrors of core docs | [Pass/Partial/Fail] | [sample url] |
| Content not JS-gated (`curl` test) | [Pass/Partial/Fail] | [what renders] |
| Capability signaling in plain text | [Pass/Partial/Fail] | [missing fields] |
| `Organization` + product JSON-LD | [Pass/Partial/Fail] | [what's present] |

**Auto-run the linter if available:**
```bash
python scripts/quality_gates/agent_readiness_lint.py https://<their-domain>
```

Any P0 failure blocks the rest of the plan until fixed — surround-sound spend on a site that agents can't read is wasted.

### Prestige Pulse Score

Each mention type generates a "pulse" of authority:
- Forum post mentioning brand → 1 pulse
- Third-party review → 3 pulses
- "Best of" list inclusion → 5 pulses
- Wikipedia mention → 10 pulses
- Academic citation → 10 pulses

Estimate your total pulse score vs top 3 competitors.

## Phase 3: Consensus Building Plan

Generate a 90-day plan to build your consensus web:

### Month 0: Fix Own-Domain Agent-Readiness (P0 only)

Remediate every P0 failure from the agent-readiness audit before spending on outbound surround sound.

| Action | Platform | Goal |
|--------|----------|------|
| Ship `/robots.txt` with explicit AI bot rules | Your site | Deliberate allow/block per bot |
| Ship `/llms.txt` entrypoint pointing at core docs + API + auth model | Your site | One-fetch map for agents |
| Add markdown mirrors for top 10 doc pages | Your site | Agents can read without JS |
| Move capability signaling (what, who-for, API, auth, pricing) into plain text above the fold | Your site | Research agents get the summary right |
| Add `Organization` + product JSON-LD | Your site | Knowledge graph reconciliation |

Skip to Month 1 only if the linter reports Pass on P0.

### Month 1: Foundation (Entity Establishment)

| Action | Platform | Goal |
|--------|----------|------|
| Claim/optimize all directory listings | G2, Capterra, Product Hunt, Crunchbase | Establish entity across platforms |
| Publish 3-5 definitive content pieces on your domain | Your blog | Create authoritative source material |
| Create comparison pages | Your site | "[Your Brand] vs [Competitor]" pages |
| Ensure structured data / schema markup | Your site | Help search engines understand your entity |

### Month 2: Amplification (Third-Party Presence)

| Action | Platform | Goal |
|--------|----------|------|
| Get included in "best of" / "top X" listicles | Review sites, industry blogs | Third-party validation |
| Participate in relevant forum discussions | Reddit, Quora, HN | Natural brand mentions in context |
| Publish guest articles / contributed content | Industry publications | Expand entity footprint |
| Create linkable assets (research, data, tools) | Your site | Earn organic citations |

### Month 3: Dominance (Surround Sound)

| Action | Platform | Goal |
|--------|----------|------|
| Control multiple domains ranking for category queries | Owned properties, guest posts | "Surround" search results |
| Build author/founder expertise signals | LinkedIn, speaking, bylines | E-E-A-T signals |
| Strategic PR for AI citation | Press, media | Get mentioned in sources LLMs index |
| Monitor and respond to AI mentions | ChatGPT, Perplexity, Google AIO | Track progress, fix gaps |

## Phase 4: Content Production for AI Visibility

### AEO-Optimized Content Rules

Load: `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\aeo-ai-search\aeo-ai-search-playbook-2026.md`

For every content piece in the plan:
- **Atomic facts** — one verifiable claim per sentence
- **Entity-first** — name your brand explicitly, don't use pronouns early
- **Structured for extraction** — tables, lists, Q&A format that LLMs can parse
- **Citation-worthy** — include original data, research, or unique insights
- **Information Gain** — say something NOT already in the consensus (novelty signals)

### Priority Content Types for AI Visibility

1. **Comparison pages**: "[Brand] vs [Competitor]" — LLMs love structured comparisons
2. **Definition pages**: "What is [your category]?" — entity establishment
3. **How-to guides**: "How to [solve problem your product solves]" — with your brand as the tool
4. **Data/research**: Original stats, surveys, benchmarks — citation magnets
5. **FAQ pages**: Structured Q&A that matches how people ask AI

## Phase 5: Monitoring

### Weekly AI Check

Test these queries in ChatGPT, Claude, and Perplexity:
- "What's the best [your category]?"
- "Compare [your brand] vs [competitor]"
- "[Your category] for [your ICP]"
- "How to [problem you solve]"

Track: Are you mentioned? What position? What's said about you? Is it accurate?

## Phase 6: Output

```
workspace/surround-sound/
├── _consensus-audit.md          # Current state of your AI presence
├── _90-day-plan.md              # Month-by-month action plan
├── _content-production-queue.md # Content pieces to produce (feed to /kai-content-calendar)
├── _directory-checklist.md      # All directories to claim/optimize
├── _monitoring-queries.md       # Weekly AI check queries
└── _competitor-ai-presence.md   # What competitors look like in AI answers
```
