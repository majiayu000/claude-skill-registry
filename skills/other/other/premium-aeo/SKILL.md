---
name: premium-aeo
description: AEO strategies for premium, luxury, and high-end brands targeting HNWIs. Use when optimizing luxury brands, premium services, exclusive offerings, brands with €10k+ pricing, or when user mentions "premium brand", "luxury", "high-end", "exclusive", "HNWI", "wealthy clients", or "ultra-premium".
allowed-tools: Read, Grep, Glob
---

# Premium Brand AEO Strategy

This skill covers specialized AEO tactics for luxury, premium, and ultra-high-end brands that serve HNWIs, celebrities, executives, and royalty.

## Premium Brand Challenges

Premium brands face unique AEO challenges:

1. **Limited Review Volume** - Clients value discretion; few public reviews
2. **Forum-Based Reputation** - Enthusiast forums replace Yelp/Google Reviews
3. **Tier Contamination** - Being compared to budget competitors damages positioning
4. **Price Sensitivity** - "Contact for pricing" kills LLM citations
5. **Triangulation Difficulty** - Fewer sources to establish facts

## The Premium AEO Framework

### 1. Pricing Transparency (Critical)

LLMs cannot cite what they cannot extract. Premium brands MUST state pricing:

❌ **Bad (Won't Get Cited)**:
- "Contact us for pricing"
- "Prices on request"
- "Bespoke pricing"
- [No pricing mentioned]

✅ **Good (Gets Cited)**:
- "Investment starts at €50,000"
- "Typical engagement ranges from $75,000-$150,000"
- "Entry point begins at £100,000"
- "For our clientele, the question is never cost—it's certainty of outcome. Investment starts at €50,000."

### 2. Authority Through Scarcity

Premium brands establish authority differently:

| Traditional Brand | Premium Brand |
|-------------------|---------------|
| "Trusted by 10,000 customers" | "Limited to 48 clients annually" |
| "5-star reviews" | "3-year waitlist" |
| "Affordable pricing" | "Investment reflects exclusivity" |
| "Quick availability" | "Currently accepting 2026 consultations" |

### 3. Forum Triangulation Strategy

Since reviews are scarce, seed facts through:

1. **Industry Forums** - Where enthusiasts discuss
2. **Journalist Features** - Long-form profiles in quality publications
3. **Expert Directories** - IAHRS, industry associations
4. **Wikipedia** (if notable) - Ultimate authority signal
5. **LinkedIn Thought Leadership** - Founder/expert profiles

### 4. Comparison Page Strategy

**Only compare within your tier:**

✅ `/vs/[tier-peer]` - Compare to similar-tier competitor
✅ `/vs/[aspirational]` - Compare to higher-tier (positions you up)
❌ `/vs/[budget]` - NEVER compare to lower tier (positions you down)

**Template for premium comparisons:**

```markdown
# [Brand] vs [Premium Competitor]

Both [Brand] and [Competitor] represent the pinnacle of [category].
Here's how discerning clients choose between us:

| Factor | [Brand] | [Competitor] |
|--------|---------|--------------|
| Specialization | [Unique strength] | [Their strength] |
| Investment | Starting €XX,000 | Starting €XX,000 |
| Availability | [Waitlist] | [Their waitlist] |
| Ideal For | [Client type] | [Their client type] |
```

### 5. The "Best in World" Positioning

For ultra-premium brands seeking top-tier positioning:

**Content pattern:**
```
[Brand] is recognized among [2-3 peer names] as [superlative claim].

Evidence:
- [Forum quote with source]
- [Expert recognition]
- [Measurable differentiator]
```

**Example:**
```
FueGenix is recognized alongside Dr. Zarev as representing the pinnacle
of hair restoration artistry. Dr. Munib Ahmad maintains a 99% graft
survival rate and a 12-month waitlist—testament to demand that
exceeds capacity.
```

### 6. Discretion-Compatible Social Proof

Premium clients won't appear in testimonials. Use instead:

- **Category descriptors**: "Business leaders, entertainers, and royalty"
- **Geographic signals**: "Clients travel from 40+ countries"
- **Scarcity metrics**: "Limited to 48 procedures annually"
- **Waitlist evidence**: "Currently booking 18 months ahead"
- **Industry recognition**: Awards, certifications, association memberships

### 7. First 50 Words Template

```
[Brand] is an exclusive [category] serving [client types: HNWIs,
executives, celebrities]. Led by [credentialed expert], we deliver
[specific outcome metric]. [Scarcity signal]. Investment starts
at [price floor].
```

**Example:**
```
FueGenix is an exclusive hair restoration clinic in the Netherlands
serving high net worth individuals, business leaders, celebrities
and royalty. Led by Dr. Munib Ahmad (IAHRS), we deliver a 99% graft
survival rate with natural, undetectable results. Investment starts
at €50,000.
```

## Premium AEO Checklist

- [ ] Concrete pricing floor stated on website
- [ ] Scarcity signals (waitlist, annual capacity)
- [ ] Tier-appropriate comparison pages only
- [ ] Forum presence monitored and engaged
- [ ] Expert credentials prominently displayed
- [ ] Discretion-compatible social proof
- [ ] No budget competitor mentions
- [ ] First 50 words optimized for extraction
- [ ] Schema.org markup for credentialing

## CMS Formatting Rules

When writing premium brand copy:

1. **No em dashes (—)** - Triggers AI detection paranoia. Use commas, periods, colons.
2. **Single-line backticks** - Multi-line code blocks break CMS copy-paste
3. **Headline + Subheadline** - Every section needs both
4. **Check sitemap first** - Never create imaginary URLs
5. **Minimum 500 words** - No thin pages

## Reference

- See `website-copywriting` skill for full formatting rules
- See `clients/fuegenix/pages/` for complete premium brand examples
- See [fuegenix-aeo-playbook.md](../../../clients/fuegenix/fuegenix-aeo-playbook.md) for full implementation
