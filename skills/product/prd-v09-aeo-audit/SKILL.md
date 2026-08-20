---
name: prd-v09-aeo-audit
description: >
  Audit how AI search engines (ChatGPT, Perplexity, Google AI Overviews, Claude) describe and
  recommend your product, then propose fixes. Triggers on requests to audit AI search visibility,
  improve AEO/GEO, check ChatGPT/Perplexity coverage, or when user asks "do we show up in AI
  search?", "AEO audit", "generative engine optimization", "AI discoverability", "how does
  ChatGPT describe us?", "Perplexity ranking". Outputs GTM-AEO-* entries and a Coverage Matrix.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# AEO Audit (AI Search Discoverability)

Position in workflow: v0.9 Launch Channels (ORB) → **v0.9 AEO Audit** → v0.9 Alternatives Pages, Launch Metrics

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | 5 target queries × 2 AI surfaces (ChatGPT + Perplexity); top 3 gaps with fixes |
| **standard** | 10–15 queries × 3–4 AI surfaces; full Coverage Matrix; ranked fix backlog |
| **deep** | 20–30 queries × all major surfaces; per-surface citation analysis; structured-data audit; before/after re-test plan |

## What This Does

Tests whether AI search engines surface, recommend, and accurately describe the product when a target customer asks a relevant question. AEO (answer-engine optimization) and GEO (generative-engine optimization) are the post-SEO distribution layer — when ChatGPT/Perplexity/AI Overviews answer a buyer's question, the product either is in the answer or isn't.

This is a **diagnostic** skill. It produces a gap map and a ranked fix backlog. The fixes are executed by [prd-v09-alternatives-pages](../prd-v09-alternatives-pages/SKILL.md), content updates, and structured-data work — not by this skill.

## How It Works

1. **Build a query set** — From the Positioning best-fit characteristics (jobs to be done, triggers, search intent), generate target queries an actual best-fit buyer would type. Mix high-intent ("best X for Y"), comparison ("X vs Y"), and category ("what is X").
2. **Run each query against AI surfaces** — At minimum: ChatGPT (free tier — what the median buyer sees), Perplexity, Google AI Overviews. Deep mode adds Claude, Brave Search, Kagi. Save raw responses with timestamps.
3. **Score each result** on five dimensions:
   - **Mentioned?** (yes / no)
   - **Position** in recommendation list (1st, 2nd, not listed)
   - **Description accuracy** (matches positioning vs. miscategorized vs. wrong)
   - **Competitive frame** (which alternatives are listed alongside)
   - **Citation sources** (which URLs/domains the AI cited to build the answer)
4. **Identify the gap pattern**:
   - **Absence gaps** — product not mentioned at all
   - **Category gaps** — mentioned in the wrong category (positioning failure)
   - **Citation gaps** — answer is built from sources the product doesn't appear in (need to be on those sources)
   - **Comparison gaps** — competitor wins the comparison query because comparison content doesn't exist on your side
5. **Propose ranked fixes** — Each fix maps to a specific gap type:
   - Absence → content on best-fit query intent, JSON-LD structured data, citation-source targets
   - Category → positioning content (handoff to Positioning skill)
   - Citation → outreach/contribution to high-citation sources (G2, Reddit, blog posts on cited domains)
   - Comparison → handoff to [prd-v09-alternatives-pages](../prd-v09-alternatives-pages/SKILL.md)

## Example

A best-fit buyer types **"best CRO tool for early-stage SaaS founders"** into ChatGPT. Result:

| Surface | Mentioned? | Position | Accuracy | Citations |
|---------|-----------|----------|----------|-----------|
| ChatGPT | No | n/a | n/a | 5 sources, none ours |
| Perplexity | Yes | 4th of 5 | "an analytics tool" (wrong category) | Sources include our pricing page only |
| AI Overviews | No | n/a | n/a | G2, Reddit r/SaaS, two competitor blog posts |

Gaps identified:
- **Absence** in ChatGPT — no high-intent landing for this query
- **Category miscoding** in Perplexity — we're being summarized as "analytics", not "CRO"
- **Citation gap** — we don't appear in G2 or r/SaaS threads about CRO

Ranked fixes:
1. Publish CRO-anchored guide ([prd-v09-alternatives-pages](../prd-v09-alternatives-pages/SKILL.md) handles competitor variants)
2. Rewrite product schema (JSON-LD) with the Dunford category claim
3. Outreach to G2 (claim profile, request reviews) and post a substantive thread in r/SaaS

## What You Get Back

- **GTM-AEO-\* entries** — one per query × surface gap, with the proposed fix and ranking
- **Coverage Matrix** (single GTM-* with Type=Audit) — full query × surface × status table
- **Fix backlog** — ranked list with handoff target skills

## When to Use It

| Trigger | Mode |
|---------|------|
| Pre-launch sanity check (before paid channels activate) | quick |
| Standard launch wave audit | standard |
| Quarterly retention/competitive intelligence review | deep |
| After major positioning change (re-test) | standard |
| When organic signups stall and paid CAC rises | deep |

Do **not** run before Positioning is complete — without a sharpened category claim, every "miscategorized" result is unfixable.

## Consumes

- **GTM-\* positioning statement + category claim** (from v0.9 Positioning) — Defines what "accurate description" looks like; without this, scoring is opinion
- **CFD-\* competitive alternatives** (from v0.2) — Source for comparison-intent queries
- **PER-\* best-fit characteristics** (sharpened by Positioning) — Source for query intent
- **GTM-\* channel mix** (from v0.9 Launch Channels) — AEO is a channel; surfaces tested should match best-fit channel use

## Produces

- **GTM-AEO-\* entries** with `Type=AEO-Recommendation`, one per gap-fix pair
- **GTM-\* with `Type=Audit`** — the Coverage Matrix
- **Fix backlog** — handoff list referencing [prd-v09-alternatives-pages](../prd-v09-alternatives-pages/SKILL.md), Positioning re-run, content production tickets

Confidence guidance (P4): AEO scoring is **3/5 minimum** because it's based on observed AI responses, not opinion. Quick mode may produce 2/5 outputs (limited sampling) and must tag them.

## Output Template

```
GTM-AEO-XXX: [Gap Title]
Type: AEO-Recommendation
Status: Open
Priority: [High | Medium | Low]
Owner: [Person / role]

Query: "[the exact query]"
Surface: [ChatGPT | Perplexity | AI Overviews | Claude | Brave | Kagi]
Date observed: [YYYY-MM-DD]

Result summary:
  Mentioned? [yes | no]
  Position: [#]
  Accuracy: [matches positioning | miscategorized | wrong]
  Competitive frame: [list of alternatives shown]
  Citation sources: [URLs/domains used]

Gap type: [Absence | Category | Citation | Comparison]

Proposed fix:
  - [Specific action 1]
  - [Specific action 2]

Handoff: [Target skill or owner — e.g., prd-v09-alternatives-pages, content team]

Re-test: [Date to verify fix]

Linked IDs: GTM-YYY (positioning), CFD-ZZZ (competitor), PER-AAA (best-fit)
```

```
GTM-XXX: AEO Coverage Matrix
Type: Audit
Status: Snapshot — [YYYY-MM-DD]

| Query | ChatGPT | Perplexity | AI Overviews | Gap Type |
|-------|---------|------------|--------------|----------|
| ... | ✓ #2 | ✗ | ✗ | Absence (2 surfaces) |
| ... | ✗ | ✓ #4 (miscat) | ✗ | Category + Absence |

Total queries: X
Coverage rate: Y% (mentioned in any surface)
Accurate-description rate: Z% (mentioned AND correctly described)

Linked IDs: All GTM-AEO-* entries above
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Vanity queries** | Auditing "best [exact product name]" — you'll always win that one | Use buyer-intent queries the buyer would actually type |
| **No timestamp / no re-test** | Results saved but never re-tested | AI surfaces change; re-test every fix within 2 weeks |
| **Surface monoculture** | Only testing ChatGPT | Each surface has different model/data; minimum 3 surfaces |
| **Fix all gaps equally** | 20 gaps, parallel work, no ranking | Rank by query buyer-intent strength × surface adoption |
| **Treating absence as failure** | "We're not in any results — game over" | Absence is often the easiest fix (publish high-intent content); category miscoding is the harder one |
| **Skipping citation analysis** | Knowing you're absent but not why | Citation sources reveal *where* you need to appear |

## Quality Gates

Before proceeding to fix execution:

- [ ] At least 5 queries tested (quick) / 10–15 (standard) / 20+ (deep)
- [ ] At least 3 AI surfaces sampled (standard+)
- [ ] Every gap has a typed classification (Absence / Category / Citation / Comparison)
- [ ] Every gap has a proposed fix with a handoff target
- [ ] Coverage Matrix exists and is dated
- [ ] Fix backlog is ranked

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Alternatives Pages** | Comparison-gap fixes become alternatives-page targets | "X vs us" comparison gap → SCR-ALT- page |
| **Positioning (re-run)** | Category-coding gaps signal positioning weakness | Recurring miscategorization → re-run prd-v09-positioning-dunford |
| **Launch Metrics** | Coverage Matrix becomes a KPI baseline | KPI-AEO-coverage% |
| **v1.0 Continuous Discovery** | Recurring gap patterns inform discovery questions | "Users keep finding competitor X — why?" |

## Detailed References

- Sanity team's `seo-aeo-best-practices` skill (VoltAgent index)
- Princeton AI Search benchmark studies
- (No bundled `references/` — AI surfaces change too quickly to canonize)
