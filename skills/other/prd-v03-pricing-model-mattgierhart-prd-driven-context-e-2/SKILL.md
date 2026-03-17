---
name: prd-v03-pricing-model
description: Select and validate pricing model for PRD v0.3 Commercial Model. Triggers on requests to set pricing, choose monetization model, design pricing tiers, validate willingness to pay, or when user asks "how much should we charge?", "what pricing model?", "freemium vs paid?", "how to structure tiers?", "price point?". Consumes Competitive Landscape (CFD-) and Product Type (BR-) from v0.2. Outputs BR- entries for pricing rules, tier boundaries, and competitive positioning.
---

# Pricing Model Selection

Position in HORIZON workflow: v0.2 Product Type Classification → **v0.3 Pricing Model Selection** → v0.3 Moat Articulation

## Core Principle

**Pricing follows value timing**: When and how customers receive value determines the pricing model. Don't copy competitors without understanding their value delivery pattern.

## Pricing Model × Product Type Matrix

| Product Type | Typical Model | Why It Fits | Anti-Model (Avoid) |
|--------------|---------------|-------------|-------------------|
| **Fast Follow** | Match market structure | Users expect familiar pricing | Premium positioning (no differentiation) |
| **Undercut** | Flat rate, aggressive discount | Price IS the value prop | Per-user (negates savings) |
| **Clone** | Parity or slight discount | Must compete on terms users know | Innovation pricing (confuses buyers) |
| **Slice** | Usage-based or ecosystem-tied | Value tied to platform activity | Flat fee (misaligned with usage) |
| **Wrapper** | Per-integration or usage | Value = connections made | Per-seat (value isn't user count) |
| **Innovation** | Value-based, potentially premium | Funds education, signals quality | Race to bottom (devalues category) |

## Value Timing → Model Selection

Ask: **When does the customer get value?**

| Value Pattern | Recommended Model | Examples |
|---------------|-------------------|----------|
| Continuous recurring | Subscription (monthly/annual) | SaaS tools used daily |
| Per-transaction | Usage-based | API calls, exports, generations |
| One-time outcome | One-time fee or lifetime | Logo design, course completion |
| Milestone-based | Tiered + upsell triggers | Features unlock as needs grow |

## Competitive Anchoring Decision Tree

```
1. Do competitors use per-user pricing?
   ├─ YES → Calculate "SMB penalty" (5-user annual cost)
   │   └─ Flat pricing at 50%+ savings = strong positioning
   └─ NO → Match model, differentiate on value/features

2. Is competitor pricing transparent?
   ├─ YES (Tier 1) → Use as direct anchor
   └─ NO ("Contact sales") → Find proxy or G2/Capterra estimates

3. Should we undercut, match, or go premium?
   ├─ Undercut: When we're simpler/niche and can sustain margins
   ├─ Match: When competing on features, not price
   └─ Premium: Only with clear, provable differentiation
```

## SMB Penalty Calculation

Per-user pricing penalizes SMBs with larger teams. Calculate the arbitrage:

```
Competitor: $30/user/mo
SMB with 5 users: $30 × 5 × 12 = $1,800/year

Our flat rate: $99/year
Savings: ($1,800 - $99) / $1,800 = 94%
Headline: "94% less than [Competitor] for teams of 5"
```

**Rule**: If savings exceed 70%, lead with price in positioning.

## WTP Validation Hierarchy

| Tier | Method | Confidence | When to Use |
|------|--------|------------|-------------|
| **1 (Highest)** | Actual purchase, payment collected | 95%+ | Post-MVP, real customers |
| **2** | Pre-order, payment intent, trial→paid | 70-85% | Landing page tests |
| **3** | Email signup at stated price | 50-65% | Smoke tests |
| **4** | Survey, interview ("would you pay X?") | 25-40% | Early exploration only |
| **5 (Lowest)** | Assumption, gut feel | <20% | Never use alone |

**Gate rule**: Tier 1-2 evidence required before locking pricing. Tier 4-5 only for hypothesis generation.

## Free Tier Design Rules

Only include a free tier if it serves a strategic purpose:

| Purpose | Free Tier Design | Example |
|---------|------------------|---------|
| **Viral acquisition** | Generous + sharing incentive | Dropbox referral |
| **Product-led growth** | Useful enough to hook, limited enough to upgrade | Notion personal |
| **Market education** | Demo the category value | New category tools |
| **Usage seeding** | Get data/content, charge for output | Canva designs |

**Anti-patterns**:
- Free tier that satisfies most users (no upgrade trigger)
- Free tier that requires support (costs without revenue)
- "Free forever" for unlimited users (cannibalizes paid)

**Rule**: Every free tier needs a clear upgrade trigger tied to value moment.

## Tier Design Framework

Structure tiers around value events, not feature count:

| Tier | Purpose | Design Principle |
|------|---------|------------------|
| **Free/Trial** | Hook and demonstrate value | First win in <5 minutes |
| **Entry/Starter** | Convert to paying | Lowest price that sustains business |
| **Pro/Growth** | Capture value from power users | Features that scale with success |
| **Enterprise** | Custom needs, high touch | SLAs, SSO, dedicated support |

**Tier boundary rules**:
- Entry price = CAC payback in ≤3 months
- Pro upgrade trigger = clear usage milestone (not feature gate)
- Enterprise = only if you can support it (don't fake it)

## BR- Output Format

Create pricing BR- entries using this structure:

```
BR-PRC-XXX: [Rule Name]
Rule: [Imperative statement — what MUST happen]
Rationale: [Business driver — why this rule exists]
Enforcement: [Where enforced — code, contract, process]
Evidence: [WTP validation, competitor anchor, cost structure]
Exception: [Override conditions and approver]
```

### BR- Categories

| Prefix | Category | Example Rules |
|--------|----------|---------------|
| `BR-PRC-` | Price constraints | Price floor, ceiling, discount cap |
| `BR-PKG-` | Packaging rules | Tier boundaries, feature gates |
| `BR-CMP-` | Competitive positioning | Anchor target, undercut threshold |

### Example BR- Entries

```
BR-PRC-001: Entry Price Floor
Rule: Entry tier never below $15/mo (annual) or $19/mo (monthly)
Rationale: Below $15/mo, CAC payback exceeds 6 months
Enforcement: Stripe product configuration, pricing page
Evidence: CAC estimate $45, need 3-month payback
Exception: Founding customer 50% discount (Matt approval)

BR-PKG-002: Free Tier Upgrade Trigger
Rule: Free tier limited to 50 [units]; show upgrade at 40 (80%)
Rationale: Create natural upgrade moment without frustration
Enforcement: Usage tracking + UI prompt at threshold
Evidence: CFD-XXX shows competitors gate at 25-100 units
Exception: None — critical for conversion funnel

BR-CMP-003: Competitive Price Anchor
Rule: Maintain ≥50% savings vs [Competitor] at 5-user level
Rationale: Price advantage is core differentiator for SMB segment
Enforcement: Quarterly competitive price review
Evidence: CFD-XXX (competitor pricing); BR-001 (product type: Undercut)
Exception: If competitor drops price, floor takes precedence
```

## Anti-Patterns to Avoid

| Don't | Do Instead |
|-------|------------|
| Copy competitor pricing blindly | Understand their value timing and cost structure |
| Innovation product at Fast Follow price | Price for value, not market incumbents |
| Free tier without upgrade trigger | Define clear conversion moment |
| Discount to win deals | Maintain price integrity, add value |
| Change pricing weekly | Set, validate, iterate quarterly |
| Gut-feel price points | WTP validation (Tier 1-2 evidence) |

## Validation Workflow

Before locking pricing:

1. **Calculate cost floor**: What's minimum price for positive unit economics?
2. **Identify anchor**: What do customers pay today? (competitor or workaround)
3. **Design tiers**: Entry + Pro minimum; free only if strategic
4. **Test WTP**: Landing page with price, measure signup conversion
5. **Lock BR- entries**: Document as enforceable rules

## Output Requirements

Before advancing to Moat Articulation:

- [ ] Pricing model selected with rationale (ties to product type)
- [ ] Price anchor identified (CFD- reference)
- [ ] Entry price point defined with unit economics check
- [ ] Tier boundaries defined (or "no tiers" justified)
- [ ] Free tier decision documented (yes + trigger, or no + why)
- [ ] WTP validation plan created (even if not yet executed)
- [ ] ≥3 BR-PRC/PKG/CMP entries created

## Downstream Connections

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v0.3 Moat Articulation** | Price as moat element | "Price leadership" defense |
| **v0.5 Red Team** | Pricing risk assessment | "What if competitor undercuts?" |
| **v0.9 Unit Economics** | Price inputs to CAC/LTV | Revenue per customer calculation |
| **GTM Strategy** | Pricing messaging | "91% less than [Competitor]" |

## Detailed References

- **Good/bad examples**: See `references/examples.md`
- **BR- template worksheet**: See `assets/br-pricing.md`
