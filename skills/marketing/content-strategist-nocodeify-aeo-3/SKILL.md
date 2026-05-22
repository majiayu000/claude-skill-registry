---
name: content-strategist
description: Strategic content planning for AEO dominance. Use when planning what content to create, identifying data study opportunities, finding terms to own, discovering zero-volume keywords, or auditing content lifecycle. Triggers on "content strategy", "what content", "content plan", "data study", "keyword research", "terms to own", "content audit".
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, mcp__aeo-audit__query_chatgpt, mcp__aeo-audit__query_gemini, mcp__aeo-audit__query_google
---

# Content Strategist Skill

This skill plans **what content to create** (strategic), not **how to write it** (tactical). It implements Section 3.5 of the AEO Protocol: The Content Supply Chain Protocol.

## Core Principle

> "LLMs don't cite generic advice. They cite original data."

The goal is to identify content opportunities that will FORCE LLMs to cite you because you're the only source.

## Four Strategic Pillars

### 1. Source of Truth Assets (Data Studies)

Identify opportunities to become THE source for a statistic.

**Discovery Questions:**
- What data do you have that no one else has?
- What could you analyze that would produce citable numbers?
- What questions do people ask that have no authoritative answer?

**Minimum Viable Study Framework:**
| Element | Requirement |
|---------|-------------|
| Sample Size | 50-100 minimum |
| Format | One key finding + data table |
| Length | 1,500-2,500 words |
| Update Cadence | Annually |

**Output:** List of 3-5 potential data studies with:
- Study title
- Key question answered
- Data source/methodology
- Target URL: `/research/[study-name]`

### 2. Dictionary Definition Heist (Terms to Own)

Identify concepts without authoritative definitions that the brand can claim.

**Discovery Process:**
1. List common problems in the industry
2. Check if each has a named term
3. Query ChatGPT/Gemini: "What is [problem]?"
4. If vague or no direct answer = opportunity to coin

**Criteria for Good Terms:**
- Describes a real, recognized problem
- No existing authoritative definition
- Memorable, capitalized name
- Can be explained in one sentence

**Output:** List of 5-10 terms to coin with:
- Proposed term name
- One-sentence definition
- Target URL: `/glossary/[term-name]`

### 3. Zero-Volume Keyword Discovery

Find 10-search/month queries that convert at 100%.

**Discovery Methods:**

```bash
# Forum mining (manual search patterns)
site:reddit.com "[industry] problem"
site:reddit.com "[brand] vs"
site:[industry-forum].com "help with"
```

**Questions to Surface Keywords:**
- "What did you search before finding us?" (customer interviews)
- What specific issues appear in support tickets?
- What do competitors NOT cover?

**Qualification Criteria:**
| Factor | Requirement |
|--------|-------------|
| Monthly Volume | <100 (ideally <50) |
| Competition | None or minimal |
| Intent | High (specific problem) |
| Commercial Value | High (ready to buy/convert) |

**Output:** List of 20-30 zero-volume keywords with:
- Keyword
- Estimated intent level (high/medium)
- Content type to create (FAQ, dedicated page, blog)

### 4. Content Lifecycle Audit

Identify what exists and what needs attention.

**Audit Framework:**

```
┌─────────────────────────────────────────────────────────────┐
│  CONTENT INVENTORY                                          │
│                                                             │
│  1. PILLAR CONTENT (Core pages)                             │
│     └── Exists? Updated? Performing?                        │
│                                                             │
│  2. COMPARISON CONTENT (/vs/ pages)                         │
│     └── Top 5 competitors covered?                          │
│     └── Top 10-20 covered?                                  │
│                                                             │
│  3. FEATURE/USE CASE CONTENT                                │
│     └── Each feature has a page?                            │
│     └── Each use case/vertical covered?                     │
│                                                             │
│  4. DATA ASSETS                                             │
│     └── Any original research?                              │
│     └── Statistics pages?                                   │
│                                                             │
│  5. GLOSSARY                                                │
│     └── Key terms defined?                                  │
│     └── Proprietary terms coined?                           │
└─────────────────────────────────────────────────────────────┘
```

**Decay Detection:**
- Last updated >6 months ago = needs review
- Last updated >12 months ago = urgent refresh
- Outdated statistics = immediate fix
- Broken links/images = immediate fix

**Output:** Content audit report with:
- Inventory by category
- Gaps identified
- Decay alerts
- Priority ranking

## Workflow

### Step 1: Gather Context

```
1. Read client playbook if exists: clients/[client]/[client]-aeo-playbook.md
2. Fetch current sitemap: curl -s [domain]/sitemap.xml
3. Review existing content inventory
4. Check current LLM visibility: query_chatgpt, query_gemini
```

### Step 2: Run Four-Pillar Analysis

For each pillar, produce specific, actionable recommendations.

### Step 3: Prioritize by Impact

| Priority | Content Type | Why |
|----------|--------------|-----|
| P0 | Missing core pages | Foundation |
| P1 | Data studies | Unique citation opportunity |
| P1 | Terms to coin | Definition ownership |
| P2 | Zero-volume content | High-intent capture |
| P2 | Content refresh | Decay prevention |
| P3 | Horizontal expansion | Growth after saturation |

### Step 4: Deliver Strategy Document

Output format:

```markdown
# Content Strategy: [Brand]

## Executive Summary
[2-3 sentences on current state and biggest opportunities]

## Data Study Opportunities
1. [Study 1] - /research/[url]
2. [Study 2] - /research/[url]

## Terms to Own
1. [Term 1] - /glossary/[url]
2. [Term 2] - /glossary/[url]

## Zero-Volume Keywords
| Keyword | Intent | Content Type |
|---------|--------|--------------|
| ... | ... | ... |

## Content Lifecycle Status
| Page | Last Updated | Status | Action |
|------|--------------|--------|--------|
| ... | ... | ... | ... |

## Priority Roadmap
### Immediate (This Month)
- ...

### Short-term (Next 90 Days)
- ...

### Long-term (6-12 Months)
- ...
```

## Integration with Other Skills

| Task | Use This Skill |
|------|----------------|
| Plan what to create | `content-strategist` (this skill) |
| Write the content | `website-copywriting` |
| Optimize existing content | `content-optimizer` agent |
| Premium brand strategy | `premium-aeo` skill |
| Competitor research | `forum-research` skill |

## Reference

- See `aeo-protocol-sop.md` Section 3.5 for methodology
- See `aeo-protocol-sop.md` Section 0 for SEO fundamentals
- See `aeo-protocol-sop.md` Section 3.2.5-3.2.6 for page templates
