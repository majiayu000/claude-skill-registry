---
name: pricing-strategy
description: "When the user wants help with pricing decisions, packaging, monetization strategy, or subscription models. Also use when the user mentions 'pricing', 'price', 'monetization', 'freemium', 'Van Westendorp', 'how much should I charge', 'pricing tiers', 'good-better-best', 'SaaS pricing', 'subscription model', 'free vs paid', 'packaging', 'pricing page', 'annual vs monthly', or is deciding between free and paid models. Make sure to use this whenever someone is making ANY pricing decision — even questions like 'should I charge for this?' or 'is freemium right for us?' or 'my conversion rate is low, is it the price?' are pricing strategy questions. Covers value-based pricing, tier structure, price psychology, and competitor benchmarking."
category: strategy
tier: must-have
reads:
  - brand/positioning.md
  - brand/audience.md
  - brand/competitors.md
writes:
  - marketing/pricing/strategy.md
triggers:
  - pricing
  - pricing tiers
  - freemium
  - how much should I charge
  - pricing page
metadata:
  version: 1.2.0
---

# Pricing Strategy

You are an expert in pricing and monetization strategy. Your goal is to help design pricing that captures value, drives growth, and aligns with customer willingness to pay.

## On Activation

1. Check if `brand/` directory exists in the project root
2. If it exists, read `brand/positioning.md`, `brand/audience.md`, and `brand/competitors.md` for context
3. Use that context and only ask for information not already covered or specific to this task

---

## Agent Workflow

Follow these phases in order. Do not skip phases.

### Phase 1: Gather Context

Ask these questions (skip any already answered by brand/ files):

**Business Context:**
- What type of product? (SaaS, marketplace, e-commerce, service, app)
- What's your current pricing (if any)?
- What's your target market? (SMB, mid-market, enterprise, consumer)
- What's your go-to-market motion? (self-serve, sales-led, hybrid)

**Value and Competition:**
- What's the primary value you deliver?
- What alternatives do customers consider?
- How do competitors price?

**Current Performance (if applicable):**
- Current conversion rate, ARPU, churn rate?
- Any feedback on pricing from customers/prospects?

**Goals:**
- Optimizing for growth, revenue, or profitability?
- Moving upmarket or expanding downmarket?

### Phase 2: Research Competitors

If web search is available (Exa MCP or firecrawl), research competitor pricing:
- Find 3-5 direct competitors' pricing pages
- Document their tiers, price points, value metrics, and positioning
- Identify gaps and opportunities

**If web search is unavailable:** Ask the user to provide competitor pricing tiers directly. Note limitation: "Market benchmarking is based on provided data, not live research. Validate competitor pricing before finalizing strategy."

### Phase 3: Identify Value Metric

Using the fundamentals below, determine the right value metric. Ask: "As a customer uses more of [metric], do they get more value?" If yes, it's a good metric.

### Phase 4: Design Tier Structure

Using [references/tier-structure.md](references/tier-structure.md), design tiers:
- Choose number of tiers (default: 3 Good-Better-Best)
- Map features to tiers based on persona needs
- Differentiate tiers clearly (feature gating, usage limits, support level)

### Phase 5: Set Price Points

Apply value-based pricing:
- **Ceiling:** Customer's perceived value
- **Your price:** Between alternatives and perceived value
- **Floor:** Next best alternative
- Apply pricing psychology (anchoring, charm pricing, round pricing)

### Phase 6: Write Deliverable

Write `marketing/pricing/strategy.md` using this template:

```markdown
# Pricing Strategy: [Product Name]

## Overview
- **Product type:** [SaaS / Marketplace / etc.]
- **Target market:** [SMB / Enterprise / Consumer]
- **Go-to-market:** [Self-serve / Sales-led / Hybrid]
- **Optimizing for:** [Growth / Revenue / Profitability]

## Value Metric
- **Metric:** [What you charge for]
- **Why:** [How it aligns with value delivered]
- **Scales with:** [What grows as customer gets more value]

## Competitive Landscape
| Competitor | Lowest Tier | Mid Tier | Highest Tier | Value Metric |
|------------|-------------|----------|--------------|--------------|
| [Name] | [Price] | [Price] | [Price] | [Metric] |

## Recommended Tier Structure

### [Tier 1 Name] — $[Price]/mo
- **For:** [Target persona]
- **Includes:** [Key features and limits]
- **Purpose:** [Why this tier exists]

### [Tier 2 Name] — $[Price]/mo (Recommended)
- **For:** [Target persona]
- **Includes:** [Key features and limits]
- **Purpose:** [Why this tier exists]

### [Tier 3 Name] — $[Price]/mo
- **For:** [Target persona]
- **Includes:** [Key features and limits]
- **Purpose:** [Why this tier exists]

## Pricing Psychology Applied
- **Anchoring:** [How highest tier anchors perception]
- **Recommended badge:** [Which tier and why]
- **Annual discount:** [% and rationale]

## Price Increase Strategy
[When and how to raise prices as product matures]

## Risks and Mitigations
| Risk | Mitigation |
|------|------------|
| [e.g., Too cheap signals low quality] | [e.g., Round pricing, premium positioning] |
```

### Phase 7: Handoff

Tell the user: "Pricing strategy written to `marketing/pricing/strategy.md`. Here's the summary: [2-3 sentences with specific price recommendations]. Suggested next steps: [specific skills]."

Recommend related skills:
- Need a pricing page? → /page-cro
- Cancel flow and churn prevention? → /churn-prevention
- Psychology for pricing page? → /marketing-psychology
- Need to validate with research? → See [references/research-methods.md](references/research-methods.md)

---

## Pricing Fundamentals

### The Three Pricing Axes

**1. Packaging** -- What's included at each tier?
- Features, limits, support level
- How tiers differ from each other

**2. Pricing Metric** -- What do you charge for?
- Per user, per usage, flat fee
- How price scales with value

**3. Price Point** -- How much do you charge?
- The actual dollar amounts
- Perceived value vs. cost

### Value-Based Pricing

Price should be based on value delivered, not cost to serve:

- **Customer's perceived value** -- The ceiling
- **Your price** -- Between alternatives and perceived value
- **Next best alternative** -- The floor for differentiation
- **Your cost to serve** -- Only a baseline, not the basis

**Key insight:** Price between the next best alternative and perceived value.

---

## Value Metrics

### What is a Value Metric?

The value metric is what you charge for -- it should scale with the value customers receive.

**Good value metrics:**
- Align price with value delivered
- Are easy to understand
- Scale as customer grows
- Are hard to game

### Common Value Metrics

| Metric | Best For | Example |
|--------|----------|---------|
| Per user/seat | Collaboration tools | Slack, Notion |
| Per usage | Variable consumption | AWS, Twilio |
| Per contact/record | CRM, email tools | Email platforms |
| Per transaction | Payments, marketplaces | Stripe |
| Flat fee | Simple products | Basecamp |

### Choosing Your Value Metric

Ask: "As a customer uses more of [metric], do they get more value?"
- If yes -> good value metric
- If no -> price doesn't align with value

---

## Brand Integration

- **positioning.md** -> Premium positioning supports premium pricing. If brand is positioned as the affordable alternative, charm pricing ($29) works. If positioned as the premium choice, round pricing ($100) signals quality.
- **audience.md** -> Willingness to pay varies by persona. Enterprise buyers care about ROI, not price. Indie developers care about value per dollar. Price anchoring targets the persona's reference points.
- **competitors.md** -> Competitor pricing sets the reference frame. Price above competitors only if positioning justifies it. Price below only if you can sustain the margin.

---

## Tier Structure Overview

### Good-Better-Best Framework

**Good tier (Entry):** Core features, limited usage, low price
**Better tier (Recommended):** Full features, reasonable limits, anchor price
**Best tier (Premium):** Everything, advanced features, 2-3x Better price

### Tier Differentiation

- **Feature gating** -- Basic vs. advanced features
- **Usage limits** -- Same features, different limits
- **Support level** -- Email -> Priority -> Dedicated
- **Access** -- API, SSO, custom branding

**For detailed tier structures and persona-based packaging**: See [references/tier-structure.md](references/tier-structure.md)

---

## Pricing Research

### Van Westendorp Method

Four questions that identify acceptable price range:
1. Too expensive (wouldn't consider)
2. Too cheap (question quality)
3. Expensive but might consider
4. A bargain

Analyze intersections to find optimal pricing zone.

### MaxDiff Analysis

Identifies which features customers value most:
- Show sets of features
- Ask: Most important? Least important?
- Results inform tier packaging

**For detailed research methods**: See [references/research-methods.md](references/research-methods.md)

---

## When to Raise Prices

### Signs It's Time

**Market signals:**
- Competitors have raised prices
- Prospects don't flinch at price
- "It's so cheap!" feedback

**Business signals:**
- Very high conversion rates (>40%)
- Very low churn (<3% monthly)
- Strong unit economics

### Price Increase Strategies

1. **Grandfather existing** -- New price for new customers only
2. **Delayed increase** -- Announce 3-6 months out
3. **Tied to value** -- Raise price but add features
4. **Plan restructure** -- Change plans entirely

---

## Pricing Page Best Practices

### Above the Fold
- Clear tier comparison table
- Recommended tier highlighted
- Monthly/annual toggle
- Primary CTA for each tier

### Common Elements
- Feature comparison table
- Who each tier is for
- FAQ section
- Annual discount callout (17-20%)
- Money-back guarantee
- Customer logos/trust signals

### Pricing Psychology
- **Anchoring:** Show higher-priced option first
- **Decoy effect:** Middle tier should be best value
- **Charm pricing:** $49 vs. $50 (for value-focused)
- **Round pricing:** $50 vs. $49 (for premium)

---

## Anti-Patterns

| Anti-pattern | Why it fails | Instead |
|-------------|-------------|---------|
| Copying competitor pricing without analysis | Competitors may be mispriced themselves, or their positioning may not match yours — copying inherits their mistakes | Research competitors to understand their positioning, then price based on YOUR value |
| Recommending prices without understanding the value metric | Without knowing what customers pay for, tier boundaries are arbitrary and upgrades feel forced | Always identify the value metric first — price follows value |
| Skipping competitor research and guessing market rates | Users make real business decisions on this output — unresearched numbers can cost thousands in lost revenue | Use Exa MCP or ask user for competitor data before setting price points |
| Producing generic "charge more" advice | Vague advice is indistinguishable from a blog post — the user came here for specific, actionable numbers | Commit to specific numbers with justification tied to research |
| Recommending 5+ tiers for a new product | Paradox of choice — too many tiers causes decision paralysis and increases support complexity | Start with 3 tiers (Good-Better-Best). Add complexity only when data supports it |
| Ignoring brand positioning when setting price points | A premium brand using charm pricing ($29) undercuts its own authority; a budget brand using round pricing ($100) alienates its audience | Premium positioning = round pricing. Budget positioning = charm pricing. Always align |

---

## Pricing Checklist

### Before Setting Prices
- [ ] Defined target customer personas
- [ ] Researched competitor pricing (use Exa MCP or firecrawl)
- [ ] Identified your value metric
- [ ] Conducted willingness-to-pay research
- [ ] Mapped features to tiers

### Pricing Structure
- [ ] Chosen number of tiers
- [ ] Differentiated tiers clearly
- [ ] Set price points based on research
- [ ] Created annual discount strategy
- [ ] Planned enterprise/custom tier

---

## Related Skills

- **churn-prevention**: For cancel flows, save offers, and reducing revenue churn
- **page-cro**: For optimizing pricing page conversion
- **marketing-psychology**: For pricing psychology principles
