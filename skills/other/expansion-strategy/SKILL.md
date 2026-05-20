---
name: expansion-strategy
description: Upsell, cross-sell, and account growth tactics. Framework for revenue expansion.
disable-model-invocation: false
user-invocable: true
---

# Expansion Strategy: Upsell, Cross-sell, and Account Growth

## Quick Start

```
/expansion-strategy
```
Then provide:
1. **Current pricing tiers** and plans (or I'll pull from business-info)
2. **NRR and expansion rate** (if known -- or I'll query your analytics MCP)
3. **Which expansion lever** to focus on: upsell, cross-sell, or seat expansion

I'll decompose your NRR, identify the biggest expansion gap, assess
pricing sensitivity, design in-product triggers, and build a playbook.

**Output:** Saved to `outputs/analyses/expansion-strategy-[date].md`
**Time:** ~15 min for focused lever, ~30 min for full strategy

**When to use:** When optimizing monetization, planning pricing tiers, or building expansion features

**Framework source:** Aakash Gupta's expansion and monetization frameworks

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Business Info | `context-library/business-info-template.md` | pricing, tiers, plans, ACV, revenue model, monetization | Current pricing, tiers, customer segments, revenue targets |
| Metrics/Analytics | `context-library/metrics/*.md` | NRR, "net revenue retention", expansion rate, upsell, churn, MRR | Existing expansion metrics, NRR benchmarks, churn by segment |
| PRDs | `context-library/prds/*.md` | pricing, tier, feature gate, monetization | Feature decisions tied to monetization, pricing rationale |
| Strategy | `context-library/strategy/*.md` | "growth", "expansion", "pricing", "positioning" | Strategic approach, customer segmentation, market positioning |
| Meeting Notes | `context-library/meetings/*.md` | pricing, customer expansion, upsell, enterprise, segment, revenue | Sales conversations, customer upgrade opportunities, pricing feedback |

**Context Priority:**
1. Internal context FIRST (business info, existing metrics, PRDs)
2. Analytics MCP SECOND (if connected - query expansion rates, NRR)
3. Framework guidance LAST (generic expansion tactics)

**Cross-Skill Links:**
- If activation concerns mentioned → Link to `activation-analysis`
- If retention impacts mentioned → Link to `retention-analysis`
- If pricing model unclear → Link to `write-prod-strategy`

---

## Step 0: Understanding Current Monetization State

Before diving into expansion tactics, let me check what you already know about your business...

**Checking:**
- `context-library/business-info-template.md` for current pricing and segments
- `context-library/metrics/` for existing expansion metrics and NRR
- `context-library/prds/` for monetization-related decisions
- `context-library/strategy/` for revenue growth strategy
- `context-library/meetings/` for sales conversations about expansion

**[If analytics MCP connected]:** "Let me also query [Amplitude/Mixpanel] for current expansion rates, NRR, and customer segment growth patterns."

**Based on what I find, I'll show you:**

### Internal Intelligence Summary

**From Business Info:**
- [Current pricing tiers and plans]
- [Customer segments and ACV by segment]
- [Revenue targets and goals]
- Example: "Free → Pro → Enterprise with annual discounts"

**From Metrics/Analytics:**
- [Current expansion rate and NRR]
- [Churn by customer segment]
- [Average time to first expansion]
- Example: "Current NRR is 105%, expansion rate 12% MoM"

**From PRDs:**
- [Feature gating decisions and their rationale]
- [Past pricing experiments or changes]
- Example: "PRD-2024-05 added feature X to drive tier upgrades"

**From Sales/CS Meetings:**
- [Common upgrade objections and customer requests]
- [Segments ready to expand]
- Example: "Enterprise segment asking for 5+ more features before upgrade"

**From Strategy Docs:**
- [Revenue growth targets and expansion approach]
- [Customer segmentation strategy]
- Example: "Strategy targets 120% NRR through seat expansion in 2024"

### Gaps in Knowledge

Based on internal context, we **don't yet know:**
- [Gap 1]: Specific usage patterns triggering expansion readiness
- [Gap 2]: Competitor pricing and tier comparison
- [Gap 3]: Customer willingness to pay for specific features

**Should I dive into expansion strategy, or would you like to provide additional context first?**

---

## Step 1: Expansion Diagnostic Questions

Instead of generic "what's your revenue model," I'll ask:

### Question 1: Current Expansion Reality
**"What percentage of your customers expand each month, and how much revenue do they bring?"**

This tells me your baseline expansion rate and whether expansion is already happening.

### Question 2: Stuck Segment
**"Which customer segment should be expanding but isn't?"**

Examples:
- "Free users who should upgrade to Paid"
- "Starter tier customers ready for Professional"
- "Single-seat accounts needing multi-seat licenses"

### Question 3: Expansion Blocker
**"What's preventing expansion right now—is it product gaps, unclear value, pricing confusion, or customer awareness?"**

This helps prioritize what to fix first.

### Question 4: Low-Hanging Fruit
**"Which expansion lever—upsell, cross-sell, or seat expansion—is closest to ready?"**

Some need product changes, some just need sales motion.

### Question 5: Revenue Impact
**"What would expanding by 10% do to your NRR and annual revenue?"**

Anchors expansion work to business impact.

---

## Three Types of Expansion

### 1. Upsell (Vertical Expansion)

**What it is:** Move customers to higher-priced tiers

**Examples:**
- Free → Paid
- Starter → Professional → Enterprise
- Individual → Team → Business

**When it works:**
- Clear value differentiation between tiers
- Usage-based triggers (hitting limits)
- Feature gating that makes sense

---

### 2. Cross-sell (Horizontal Expansion)

**What it is:** Sell additional products/modules

**Examples:**
- Salesforce: CRM → Marketing Cloud → Service Cloud
- HubSpot: Marketing → Sales → Service
- Adobe: Photoshop → Illustrator → Premiere

**When it works:**
- Products have natural workflow adjacency
- Bundled value > sum of parts
- Integration reduces friction

---

### 3. Account Expansion (Seat Expansion)

**What it is:** Grow usage within existing accounts

**Examples:**
- More seats (Slack, Notion, Figma)
- More usage volume (Stripe, Twilio, AWS)
- More locations/teams (multi-location SaaS)

**When it works:**
- Viral/collaborative products
- Network effects within organization
- Department-by-department rollout

---

## The Expansion Funnel

**Track these stages:**

```
Active Users (100%)
    ↓
Engaged Users (60%) - using product regularly
    ↓
Power Users (30%) - hitting limits or wanting more
    ↓
Expansion Trigger (15%) - ready to upgrade
    ↓
Upgraded (10%) - completed expansion
```

**Key metrics:**
- Expansion rate: % of accounts that expand MoM
- Time to expansion: Days from signup to upgrade
- Expansion ARR: Revenue from upsells/cross-sells

---

## How to Build an Expansion Strategy

### Step 1: Identify Your Expansion Levers

**Use this prompt:**
```
Use /expansion-strategy and reference context-library/business-info-template.md

Help me identify expansion opportunities:
- Product: [describe your product]
- Current pricing: [tiers/plans]
- Usage patterns: [how customers use it]

What are our top 3 expansion levers?
```

**Common levers:**
- **Usage limits** (storage, API calls, seats)
- **Feature gating** (advanced features locked)
- **Service tiers** (self-serve → managed service)
- **Add-ons** (integrations, premium support)
- **New products** (complementary offerings)

---

### Step 2: Segment Your Customers

**Three expansion segments:**

**1. Ready to Expand (Hot)**
- Hitting usage limits
- High engagement
- Team growing
- **Action:** Proactive outreach + in-app prompts

**2. Could Expand (Warm)**
- Moderate usage
- Some friction points
- Growing organization
- **Action:** Nurture campaigns, show value

**3. Not Ready (Cold)**
- Low usage
- Just started
- Small team
- **Action:** Focus on activation first

---

### Step 3: Design Expansion Triggers

**In-product triggers:**

**1. Limit-based triggers**
```
Example: "You've used 90% of your storage. Upgrade for unlimited?"
```

**2. Feature-access triggers**
```
Example: "Unlock advanced analytics with Professional plan"
```

**3. Team-growth triggers**
```
Example: "Invite 5+ teammates? Team plan is 30% cheaper per seat"
```

**4. Success-based triggers**
```
Example: "You've completed 100 projects! You're ready for Pro features"
```

**Timing matters:** Show upgrade prompts at moments of success, not frustration

---

### Step 4: Build Value Ladders

**Value ladder = clear progression of benefits**

**Example: Notion's tiers**
- **Free:** Personal use, unlimited pages
- **Plus:** Unlimited file uploads, version history
- **Business:** Advanced permissions, analytics, priority support
- **Enterprise:** SAML SSO, advanced security, dedicated manager

**Each tier unlocks new capabilities aligned with growing needs**

---

## Expansion Pricing Models

### Usage-Based Pricing

**What it is:** Pay for what you use (seats, volume, API calls)

**Examples:**
- Slack: Per active user
- Stripe: % of transaction volume
- AWS: Computing hours used

**Pros:**
- Natural expansion as usage grows
- Fair to customers
- Aligns incentives

**Cons:**
- Unpredictable revenue
- Complex to communicate

**Best for:** Products with clear usage metrics

---

### Feature-Based Pricing

**What it is:** Tiers unlock features

**Examples:**
- Superhuman: Basic → Pro (access to premium features)
- Figma: Starter → Professional (plugins, version history)
- Canva: Free → Pro (premium templates, brand kit)

**Pros:**
- Predictable revenue
- Clear differentiation
- Easy to understand

**Cons:**
- Risk of over-gating features
- Can feel restrictive

**Best for:** Products with distinct feature sets

---

### Hybrid Pricing

**What it is:** Combination of seats + features + usage

**Example: HubSpot**
- Base price: per seat
- Tier pricing: feature access
- Usage charges: email send volume

**Best for:** Complex products with multiple value dimensions

---

## Expansion Playbooks

### Playbook 1: Free to Paid Conversion

**Goal:** Convert free users to first paid plan

**Tactics:**
1. **Time-limited trial** (14-30 days of premium features)
2. **Feature teasing** (show locked features, explain value)
3. **Success milestones** ("You've created 50 docs! Upgrade for unlimited")
4. **Team triggers** ("Invite teammates? Paid plans include collaboration")

**Example: Notion**
- Free tier is generous (works for individuals)
- Team features require paid plan
- Conversion happens when users need collaboration

---

### Playbook 2: Tier Jumping

**Goal:** Move paid users to higher tiers

**Tactics:**
1. **Limit notifications** ("Approaching storage limit")
2. **Feature discovery** (surface higher-tier features)
3. **Cohort messaging** ("Companies like yours use Enterprise")
4. **ROI calculator** ("Save 10 hours/week with automation")

**Example: Salesforce**
- Start with Sales Cloud
- Show integrations with Marketing Cloud
- Upsell to bundles

---

### Playbook 3: Seat Expansion

**Goal:** Grow seats within accounts

**Tactics:**
1. **Viral loops** (collaborative features require invites)
2. **Admin dashboard** (show adoption metrics)
3. **Department expansion** (start with one team, spread to others)
4. **Volume discounts** (cheaper per-seat at scale)

**Example: Slack**
- Free tier allows team trial
- Paid plan unlocks full history
- Virality spreads to whole company

---

## Measuring Expansion Success

**Key metrics to track:**

### Net Revenue Retention (NRR)

```
NRR = (Starting ARR + Expansion - Churn) / Starting ARR × 100%

Example:
- Starting ARR: $1M
- Expansion: $300K (upsells + cross-sells)
- Churn: -$100K
- NRR = ($1M + $300K - $100K) / $1M = 120%
```

**Benchmarks:**
- 100%+ = Good (expansion offsets churn)
- 110%+ = Great (growth from existing customers)
- 120%+ = Exceptional (best-in-class SaaS)

---

### Expansion Rate

```
Monthly Expansion Rate = (Accounts that expanded this month) / (Total accounts) × 100%
```

**Target:** 10-15% monthly expansion rate

---

### Time to Expansion

```
Median days from signup to first upgrade
```

**Target varies by product:**
- B2B SaaS: 30-90 days
- Consumer apps: 7-30 days

---

## Common Mistakes

❌ **Pushing expansion before activation**
- Problem: Users churn because they haven't found value yet
- Fix: Activation first, expansion second

❌ **Over-gating features**
- Problem: Free tier is useless, no one converts
- Fix: Make free tier valuable, gate advanced features

❌ **Ignoring usage patterns**
- Problem: Upgrade prompts at wrong time
- Fix: Trigger based on behavior, not time

❌ **No clear value differentiation**
- Problem: Users don't understand why to upgrade
- Fix: Articulate clear benefits per tier

❌ **Treating expansion as sales-led only**
- Problem: Misses self-serve expansion opportunity
- Fix: Build in-product expansion flows

---

## Real-World Examples

### Example 1: Dropbox

**Strategy:** Storage-based upsell
- Free: 2GB storage
- Plus: 2TB storage
- Family: 2TB + 6 accounts

**Trigger:** File storage nearing limit

**Result:** Simple, usage-based expansion

---

### Example 2: Zoom

**Strategy:** Usage limits + features
- Free: 40-minute meetings
- Pro: Unlimited meeting duration + cloud recording
- Business: Admin controls + SSO

**Trigger:** 40-minute limit hit during meetings

**Result:** Natural friction point drives upgrades

---

### Example 3: Figma

**Strategy:** Seat expansion + feature gating
- Free: 3 files, 1 team
- Professional: Unlimited files, version history, plugins
- Organization: Advanced security, libraries

**Trigger:** Team collaboration needs

**Result:** 150%+ NRR, seat expansion drives growth

---

## Expansion Strategy Worksheet

### 1. Current State
- Average contract value (ACV): $_____
- Monthly expansion rate: ____%
- Net Revenue Retention (NRR): ____%
- Time to first expansion: _____ days

### 2. Expansion Levers
**Identify your top 3:**
1. ___________ (upsell/cross-sell/seats)
2. ___________ (upsell/cross-sell/seats)
3. ___________ (upsell/cross-sell/seats)

### 3. Triggers to Build
**What signals indicate expansion readiness?**
- Usage trigger: ___________
- Feature trigger: ___________
- Team trigger: ___________

### 4. Value Ladder
**List your pricing tiers and key differentiators:**
- Tier 1: ___________ (features: _______)
- Tier 2: ___________ (features: _______)
- Tier 3: ___________ (features: _______)

### 5. Hypothesis to Test
- If we ___________, expansion rate will improve by ___% because ___________

---

## Output Integration

### Where to Save Your Expansion Strategy

**Strategy Documents:**
- Save to: `outputs/analyses/expansion-strategy-[quarter].md`
- When finalized: Move to `context-library/strategy/expansion-strategy-[quarter].md` for reference

**Pricing Changes & Experiments:**
- Create PRD in `context-library/prds/` for any tier changes or feature gating
- Link to this expansion strategy as context

**Sales Playbooks:**
- For go-to-market: Use `/slack-message` to draft sales team battlecards
- For playbook docs: Reference expansion-strategy findings

### Cross-Skill Integration

**Feeds into:**
- `/prd-draft` - New tier/feature gating decisions reference expansion strategy
- `/retention-analysis` - Expansion cohort performance data informs retention strategy
- `/activation-analysis` - Activation rate by segment informs expansion readiness
- `/write-prod-strategy` - Revenue model and pricing strategy
- `/metrics-framework` - NRR, expansion rate as leading indicators of business health

**Pulls from:**
- `/retention-analysis` - Which segments retain best (expansion potential)
- `/activation-analysis` - When users are ready to expand (post-activation)
- `/define-north-star` - Ensure expansion metrics align with North Star
- `/competitive-analysis` - Competitor pricing and tier positioning

### Key Questions to Revisit

After defining your expansion strategy, ask:
- Does every tier have clear value differentiation?
- When should we show upgrade prompts (moment of success, not friction)?
- What's our win-back strategy for customers who churn instead of expand?
- How do we measure expansion impact on overall unit economics?

---

## NRR Decomposition

Break NRR into its components to diagnose where growth is coming from:

```
NRR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR
```

| Component | Current | Target | Gap | Primary Driver |
|-----------|---------|--------|-----|---------------|
| Starting MRR | $_____ | - | - | Baseline |
| Expansion MRR | $_____ | $_____ | $_____ | Seat growth / tier upgrades / add-ons |
| Contraction MRR | $_____ | $_____ | $_____ | Downgrades / seat removals |
| Churn MRR | $_____ | $_____ | $_____ | Full cancellations |
| **NRR** | **___%** | **___%** | **___%** | [Biggest gap component] |

**Focus your strategy on the component with the biggest gap.**

### Diagnosis by NRR Range

| NRR Range | Diagnosis | Priority |
|-----------|-----------|----------|
| <90% | Churn is killing you. Fix retention before expansion. | Retention first |
| 90-100% | Churn and contraction offset expansion. Reduce downgrades. | Balance churn reduction + expansion |
| 100-110% | Healthy but room to grow. Focus on expansion levers. | Expansion optimization |
| 110-120% | Strong. Optimize expansion efficiency and reduce CAC. | Efficiency + new expansion vectors |
| 120%+ | Exceptional. Protect what's working, experiment with new vectors. | Protect + innovate |

---

## Pricing Sensitivity Assessment

Before recommending tier upgrades, assess pricing sensitivity:

### Key Questions

1. **What % of customers are at >80% of their tier limits?**
   - High % = natural expansion pressure (good)
   - Low % = tier limits may be too generous or customers don't grow into them

2. **What's the price gap between tiers?**
   - 2-3x jumps work well for SMB
   - Enterprise tiers can have larger gaps if value justifies it
   - If gap is too large, customers stay on lower tier even when they need more

3. **Is there a "dead zone" where customers outgrow one tier but the next tier is too expensive?**
   - Identify the % of customers who hit limits but DON'T upgrade
   - Survey them: "Why didn't you upgrade?"
   - Common answers: "Too expensive," "Don't need all those features," "Only need one thing from the next tier"

4. **What's the upgrade conversion rate at each tier boundary?**
   - Free -> Paid: Benchmark 2-5% for freemium, 15-25% for free trial
   - Tier 1 -> Tier 2: Benchmark 10-20%
   - Tier 2 -> Tier 3: Benchmark 5-15%

### Dead Zone Solutions

If a dead zone exists between tiers, consider:
- **Intermediate tier** - Bridge the gap with a mid-priced option
- **Usage-based pricing** - Charge per unit instead of per tier
- **A la carte add-ons** - Let customers buy specific features without full tier upgrade
- **Annual discount** - Make the next tier affordable when paid annually

### Competitive Pricing Comparison

When analyzing expansion opportunities, map your pricing against competitors:

| Tier | Your Price | Competitor A | Competitor B | Positioning |
|------|-----------|-------------|-------------|-------------|
| Free/Starter | [$/user/mo] | [$/user/mo] | [$/user/mo] | [Cheaper/Parity/Premium] |
| Mid-Tier | [$/user/mo] | [$/user/mo] | [$/user/mo] | [Cheaper/Parity/Premium] |
| Enterprise | [$/user/mo] | [$/user/mo] | [$/user/mo] | [Cheaper/Parity/Premium] |

**Key questions:**
1. Where are your upgrade price jumps vs competitors? (If your Team-to-Business is a 2.6x jump but competitors are 1.5x, you may have a dead zone)
2. What features do competitors gate at each tier? (If a key feature is free at Competitor A but gated at your Business tier, that's churn risk)
3. Is there a tier gap? (Price point where no option exists -- e.g., between $25 and $65/user, there's a $40 gap where users might feel stuck)

Pull competitor pricing from `context-library/research/competitive-*.md` or `context-library/business-info-template.md` competitor sections.

---

## Expansion Trigger Design

Design in-product triggers that naturally lead to expansion. Each trigger should surface a contextual upgrade prompt, not a generic paywall.

### Trigger Types

| Trigger | When It Fires | Message Pattern | Conversion Rate Benchmark |
|---------|--------------|-----------------|--------------------------|
| **Usage limit approaching** | 80% of seats/storage/API calls used | "You're at 80% of your [limit]. Upgrade to avoid hitting your cap." | 5-15% |
| **Team growth detected** | New team member invited | "Welcome [name]! Your team is growing. Team plan saves 30% per seat." | 8-12% |
| **Advanced feature attempted** | User clicks on a locked feature | "This feature is available on [tier]. Here's what it does: [value]." | 3-8% |
| **Success milestone reached** | User hits a usage milestone | "You've shipped 10 PRDs! Power users like you get more from Pro." | 2-5% |
| **Competitor feature gap** | User tries to do something they can't | "Looking for [capability]? It's available on [tier]." | 4-10% |

### Trigger Design Principles

1. **Show at moments of success, not frustration.** An upgrade prompt after a win ("Great job completing your 50th task!") converts better than one after hitting a wall.
2. **Be specific about what they get.** Not "Upgrade to Pro" but "Upgrade to get unlimited projects, advanced analytics, and priority support."
3. **Include social proof.** "Teams your size typically use the Business plan."
4. **Make it easy to dismiss.** Aggressive paywalls drive churn, not upgrades.
5. **Track trigger-to-upgrade attribution.** Know which triggers actually convert.

### Expansion Trigger Attribution

Not all triggers convert. Some just annoy. Track these per trigger:

| Trigger | Impressions | Clicks | Conversions | Conversion Rate | Dismiss Rate | Annoyance Signal |
|---------|------------|--------|-------------|-----------------|--------------|-----------------|
| [Trigger 1] | [N] | [N] | [N] | [%] | [%] | [NPS delta or support tickets] |

**Metrics to track per trigger:**
- **Conversion rate:** % of users who saw the trigger and upgraded within 7 days
- **Dismiss rate:** % of users who closed/ignored the trigger (>80% dismiss = reconsider the trigger)
- **NPS impact:** Did users who saw the trigger report lower NPS? If so, the trigger is damaging brand perception.
- **Time-to-upgrade:** How long between trigger exposure and upgrade? (Same session = strong trigger; 7+ days = weak signal)
- **Repeat exposure threshold:** After how many exposures does the trigger start hurting? (Usually 3-5 times before fatigue)

**Decision framework:**
- Conversion >5% + Dismiss <60% → Keep and optimize
- Conversion 2-5% + Dismiss 60-80% → Redesign the trigger message/timing
- Conversion <2% + Dismiss >80% → Kill the trigger, it's net negative
- Any trigger with negative NPS impact → Kill immediately regardless of conversion

---

## Output Quality Self-Check

Before delivering the expansion strategy, verify:

- [ ] **NRR is decomposed** into expansion, contraction, and churn components with gaps identified
- [ ] **Biggest expansion lever** is identified (upsell, cross-sell, or seat expansion) with rationale
- [ ] **Customer segments** are categorized as Hot/Warm/Cold with specific actions for each
- [ ] **Pricing sensitivity** is assessed -- are there dead zones between tiers?
- [ ] **Expansion triggers** are designed with specific timing, messaging, and expected conversion
- [ ] **Value ladder** is clear -- each tier has differentiated value that customers understand
- [ ] **Metrics** include NRR target, expansion rate target, and time-to-expansion
- [ ] **Competitor pricing** is referenced for positioning context
- [ ] **Connected to retention** -- expansion strategy doesn't sacrifice retention
- [ ] **Connected to activation** -- only expanding activated, engaged users
- [ ] **Hypothesis format** is used: If we [action], expansion will improve by [amount] because [reason]
- [ ] **Expansion trigger attribution measurement** included
- [ ] **Competitive pricing comparison** referenced
- [ ] **No generic advice** -- all recommendations reference this specific product's pricing and segments

---

## Related Skills

- `retention-analysis` - Retention enables expansion (retained users more likely to expand)
- `activation-analysis` - Activation precedes expansion (activate before offering tiers)
- `experiment-decision` - Test expansion features and pricing changes
- `define-north-star` - Align expansion to metrics (ensure NRR supports growth)
- `metrics-framework` - Track expansion rate and NRR as leading indicators
- `competitor-analysis` - Understand competitive pricing and positioning
- `write-prod-strategy` - Align expansion to broader strategy

---

**Framework credit:** Adapted from Aakash Gupta's expansion and monetization frameworks. Read: https://www.news.aakashg.com/p/ultimate-guide-expansion
