---
name: aeo-audit
description: Answer Engine Optimization (AEO) audit methodology for LLM visibility. Use when auditing brands for ChatGPT/Gemini mentions, checking LLM citations, analyzing AI search visibility, or when user mentions "AEO", "LLM visibility", "ChatGPT mentions", "Gemini citations", or "AI search optimization".
allowed-tools: Read, Grep, Glob
---

# AEO Audit Methodology

This skill provides the complete Answer Engine Optimization protocol for auditing and optimizing brand visibility in LLM-powered search (ChatGPT, Gemini, Perplexity, etc.).

## CRITICAL: Read Protocol First

**BEFORE running ANY audit, you MUST read the AEO Protocol SOP:**

```
Read aeo-protocol-sop.md (key sections):
- Lines 1-200: Core methodology
- Lines 850-900: First 50 Words Audit (CRITICAL)
- Lines 1200-1300: Content gap analysis
- Lines 2800-2900: Audit checklist
- Lines 3400-3500: Final checklist
```

**Do NOT skip this step.** The protocol is the source of truth.

## Core Concepts

### What is AEO?
Answer Engine Optimization ensures brands appear in LLM-generated answers, not just traditional search results. LLMs cite sources differently than Google - they need:
- Facts repeated across 3+ authoritative sources (triangulation)
- Structured, extractable content
- Clear entity establishment
- Technical accessibility (SSR, proper robots.txt)

### The Three Search Backends

| Engine | Backend | How It Works |
|--------|---------|--------------|
| ChatGPT | Bing + Memory | 3-layer cache (parametric → memory → live search) |
| Gemini | Google Grounding | Real-time Google Search verification |
| Google AI Overview | Google SERP | Aggregates top organic results |

## Audit Process

### Step 1: Run Brand Audit
Use `run_brand_audit` MCP tool with:
- Brand name
- Product category (be specific: "hair transplant clinic" not "medical")
- Primary competitor (optional)

### Step 2: Discovery Query Testing
Test queries people use BEFORE knowing the brand:
- "Best [category] in [location]"
- "Best [category] for [use case]"
- "Top [category] [year]"
- "[problem] solution"

### Step 2.5: CRITICAL - Run Key Queries 10 Times Each

**LLM responses are non-deterministic.** Single tests are unreliable.

For top 2-3 discovery queries, run each **10 times** per LLM and calculate consistency:

| Score | Interpretation |
|-------|----------------|
| 9-10/10 | Strong (locked in) |
| 7-8/10 | Good (consistent) |
| 5-6/10 | Weak (inconsistent) |
| 1-4/10 | Poor (rarely mentioned) |
| 0/10 | Invisible (critical) |

**A brand at 60% consistency is NOT reliably visible.**

### Step 2.6: Custom Client Queries

Beyond standard queries, test client-specific "dream queries":

| Query Type | Example |
|------------|---------|
| Outcome-focused | "[category] if money doesn't matter" |
| Problem-aware | "fix bad [category]" |
| Fear-based | "safest [category]" |
| Lifestyle | "[category] for executives" |
| Attribute-specific | "[category] no scars" |

**Ask during intake:** "What 3-5 queries do you WANT to own?"

For 0% visibility queries → create dedicated landing page.

### Step 3: Competitive Analysis
- Check which competitors appear in LLM responses
- Identify citation sources (what sites are LLMs pulling from?)
- Map competitive tier (don't compare premium to budget)

### Step 4: Gap Analysis
For each query where brand is missing:
1. What sources ARE being cited?
2. Is brand mentioned on those sources?
3. What facts are LLMs extracting?
4. What content needs to be created?

### Step 5: First 50 Words Audit (CRITICAL)
For every key page:
1. Fetch page content
2. Extract first 50 words of visible body text
3. Check for presence of:
   - **WHO**: Brand/entity name, credentials
   - **WHAT**: Core offering/service
   - **WHERE**: Location
   - **PRICE**: Pricing tier or specific numbers
4. Score: Pass (3-4) / Partial (2) / Fail (0-1)
5. Document specific rewrites needed

**Why this matters:** LLMs weight early content heavily. Facts not in first 50 words often aren't extracted.

## Scoring Framework

| Metric | Weight | Measurement |
|--------|--------|-------------|
| ChatGPT Mentions | 30% | Brand appears in X/8 queries |
| Gemini Mentions | 30% | Brand appears in X/8 queries |
| Google AI Overview | 20% | Brand in AI Overview snippets |
| Citation Quality | 20% | Authoritative sources citing brand |

## Key Audit Queries (Template)

1. `What is [brand]?` - Basic recognition
2. `Best [category] in [location]` - Discovery
3. `[Brand] vs [competitor]` - Comparison
4. `[Brand] reviews` - Reputation
5. `[Brand] pricing` - Commercial intent
6. `Best [category] for [use case]` - Use-case discovery
7. `[Problem] specialist [location]` - Problem-aware discovery
8. `Top [category] [year]` - List inclusion

## Red Flags in Audits

- ❌ Brand not mentioned in discovery queries (acquisition problem)
- ❌ Competitor mentioned but brand isn't (content gap)
- ❌ Incorrect facts in LLM responses (reputation risk)
- ❌ No citations to brand's own website (authority problem)
- ❌ Only mentioned with competitor comparisons (positioning issue)

## Quick Reference

For detailed methodology, see:
- [aeo-protocol-sop.md](../../../aeo-protocol-sop.md) - Full protocol
- [fuegenix-aeo-audit.md](../../../clients/fuegenix/fuegenix-aeo-audit.md) - Example audit
