---
name: forum-research
description: Research real competitors and market positioning via Reddit, forums, and community discussions. Use when finding actual competitors (not assumed ones), researching brand reputation, discovering how users compare brands, or when user mentions "forum research", "Reddit comparisons", "real competitors", or "what do people say about".
allowed-tools: Read, Grep, Glob
---

# Forum Research Methodology

This skill teaches how to discover REAL competitors and market positioning through forum research, rather than relying on category assumptions.

## Why Forum Research Matters

- Category competitors ≠ actual competitors
- Users compare within tiers, not across tiers
- Forums reveal authentic competitive landscape
- Premium brands often have unexpected peer groups
- Budget comparisons can damage premium positioning

## The Forum Research Process

### Step 1: Reddit Search Queries

```
site:reddit.com "[Brand]" vs
site:reddit.com "[Brand]" comparison
site:reddit.com "[Brand]" or "[Competitor]"
site:reddit.com "best [category]" recommendations
site:reddit.com "[Brand]" review
site:reddit.com "[Brand]" worth it
```

### Step 2: Industry Forum Search

Find industry-specific forums:
```
"[category] forum" site:*.com
"[category] community" discussions
```

Then search within:
```
site:[industry-forum].com "[Brand]"
site:[industry-forum].com "best [category]"
site:[industry-forum].com "[Brand]" vs
```

### Step 3: Comparison Mining

Look for natural language patterns:
- "X and Y are the best"
- "X is comparable to Y"
- "If you can't get X, try Y"
- "X is the [category] equivalent of Y"
- "X vs Y - which is better?"

### Step 4: Tier Mapping

Categorize competitors by tier based on forum discussions:

| Tier | Indicators |
|------|------------|
| Ultra-Premium | Multi-year waitlists, prices rarely discussed, "if you have to ask..." |
| Premium | High prices openly discussed, quality focus, limited availability |
| Mid-Tier | Price/quality balance, accessible, mainstream |
| Budget | Price-focused, volume, accessibility emphasized |

## Critical Rules

### DO:
- ✅ Compare within the same tier
- ✅ Use exact quotes from forums as evidence
- ✅ Note the date of forum discussions
- ✅ Cross-reference multiple forums
- ✅ Identify tier-appropriate competitors only

### DON'T:
- ❌ Assume category = competition (Elithair ≠ competitor to FueGenix)
- ❌ Compare premium to budget (damages positioning)
- ❌ Trust single sources (triangulate)
- ❌ Ignore price as a tier indicator
- ❌ Use competitor data from different tiers in content

## Evidence Template

When reporting findings, use this format:

```markdown
### Competitor: [Name]
**Source**: [Forum Name] - [Date]
**Quote**: "[Exact quote from forum]"
**Tier**: [Ultra-Premium/Premium/Mid/Budget]
**Why Competitor**: [Explanation]
**Price Comparison**: [If available]
```

## Example: FueGenix Case Study

### Wrong Approach (Category-Based)
"FueGenix competes with Elithair because both do hair transplants"
→ WRONG: Elithair is budget Turkish clinic (~€3k), FueGenix is ultra-premium (~€50k+)

### Right Approach (Forum-Based)
```
Search: site:reddit.com "FueGenix" vs
Found: "Imo current best in the world are Dr. Munib from FUEGENIX and Dr. Zarev"
Tier: Ultra-Premium (both have long waitlists, €50k+ pricing)
```

**Real competitors discovered:**
- Dr. Zarev (Bulgaria) - €50k-100k+, 3-5 year waitlist
- Dr. Konior (USA) - ~$35k, similar quality tier
- Hasson & Wong (Canada) - Premium tier

**NOT competitors:**
- Elithair - Budget tier, €3k
- Turkish mill clinics - Volume-based

## Output Format

After research, produce:

1. **Tier Map** - Visual of where brand sits
2. **Real Competitors** - Forum-verified peer group
3. **Key Quotes** - Evidence from forums
4. **NOT Competitors** - Who to avoid comparing against
5. **Content Implications** - What comparison pages to create

## Reference

See [fuegenix-aeo-audit.md](../../../clients/fuegenix/fuegenix-aeo-audit.md) Section "Real Competitive Landscape" for full example.
