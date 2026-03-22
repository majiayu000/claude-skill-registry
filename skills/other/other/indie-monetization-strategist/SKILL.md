---
name: indie-monetization-strategist
description: Monetization strategies for indie developers, solopreneurs, and small teams. Covers freemium models, SaaS pricing, sponsorships, donations, email list building, and passive income for developer tools, content sites, and educational apps. Activate on 'monetization', 'make money', 'pricing', 'freemium', 'SaaS', 'sponsorship', 'donations', 'passive income', 'indie hacker'. NOT for enterprise sales, B2B outbound, VC fundraising, or large-scale advertising (use enterprise/marketing skills).
allowed-tools: Read,Write,Edit,Bash,Glob,Grep,WebFetch,WebSearch
category: Business & Monetization
tags:
  - monetization
  - pricing
  - saas
  - indie
  - passive-income
pairs-with:
  - skill: tech-entrepreneur-coach-adhd
    reason: ADHD-friendly founder guidance
  - skill: seo-visibility-expert
    reason: Get traffic for monetization
---

# Indie Monetization Strategist

Turn side projects into sustainable income. Battle-tested strategies for indie developers and solopreneurs.

## Quick Start

1. **Build audience first** - Email list is your foundation
2. **Start with validation** - If people won't use it free, they won't pay
3. **Stack revenue streams** - Multiple small wins beats one moonshot
4. **Price on value, not cost** - Premium pricing attracts premium customers
5. **Play the long game** - Most "overnight" successes took 3-5 years

## When to Use

**Use for:**
- Choosing monetization models for dev tools
- Setting up freemium/premium tiers
- Pricing strategy decisions
- Email list building for launches
- Sponsorship and donation systems

**NOT for:**
- Enterprise B2B sales (use sales skills)
- VC fundraising/pitch decks
- Large-scale advertising campaigns

## The Indie Monetization Stack

```
┌─────────────────────────────────────────────┐
│           PREMIUM PRODUCTS                  │
│  SaaS subscriptions, one-time purchases     │
│  → Highest revenue, requires product-market │
├─────────────────────────────────────────────┤
│           SERVICES & CONSULTING             │
│  Custom work, implementation, training      │
│  → Trade time for money, but validates      │
├─────────────────────────────────────────────┤
│           PASSIVE/SEMI-PASSIVE              │
│  Sponsorships, donations, affiliates        │
│  → Lower friction, good for content/tools   │
├─────────────────────────────────────────────┤
│           LIST BUILDING                     │
│  Email subscribers, community members       │
│  → Foundation for all monetization          │
└─────────────────────────────────────────────┘
```

## Monetization Decision Tree

```
Is your project...

A DEVELOPER TOOL?
├── Open source? → Sponsorships + Premium features/hosting
├── Closed source? → Freemium SaaS or one-time purchase
└── CLI tool? → Pay-what-you-want + Pro tier

AN EDUCATIONAL RESOURCE?
├── Course/tutorial? → One-time purchase or membership
├── Reference site? → Sponsorships + Premium content
└── Interactive app? → Freemium with advanced features

A CONTENT SITE?
├── Technical blog? → Sponsorships + Newsletter premium tier
├── Showcase/portfolio? → Consulting leads + Sponsorships
└── Community site? → Membership + Sponsorships
```

## Model Quick Reference

### Freemium SaaS (80/20 Rule)

| Tier | Price | What to Include |
|------|-------|-----------------|
| **Free** | $0 | Core functionality, usage limits, goal: get users hooked |
| **Pro** | $9-29/mo | Higher limits, no branding, priority support |
| **Team** | $49-199/mo | Admin controls, SSO, SLA guarantees |

**Gate these:** Usage volume, team features, white-labeling, advanced analytics
**Never gate:** Core functionality, security features, basics competitors offer free

### Sponsorship Pricing Formula

```
Monthly visitors × $0.01-0.05 = Base sponsorship rate

Multipliers:
+ Developer audience (2-3x)
+ Niche focus (1.5-2x)
+ High engagement (1.5x)
```

### Donation Platforms

| Platform | Best For | Notes |
|----------|----------|-------|
| GitHub Sponsors | Developers | Best for OSS |
| Buy Me a Coffee | Low friction | Quick setup |
| Ko-fi | Creators | No platform cut |
| Stripe Links | Direct | Lowest fees |

## Pricing Psychology Essentials

**The Decoy Effect:**
```
BASIC: $9    PRO: $29 (target)    ENTERPRISE: $99 (decoy)
```

**Price Anchoring:**
```
❌ "Only $29/month!"
✅ "$49/month → $29/month (save 40%)"
```

**Annual vs Monthly:**
```
Monthly: $29/month | Annual: $19/month (billed $228/year)
Annual subscribers have 5x lower churn.
```

## Anti-Patterns (10 Critical Mistakes)

### 1. Premature Monetization
**Symptom:** Adding payments before product-market fit
**Fix:** Validate with free users first

### 2. Race to the Bottom Pricing
**Symptom:** Pricing way below competitors
**Fix:** Price on value delivered, not competitor copying

### 3. Feature Bloat to Justify Price
**Symptom:** Adding features nobody asked for
**Fix:** Charge more for LESS but BETTER

### 4. Ignoring Existing Monetization
**Symptom:** Building new revenue streams instead of optimizing existing
**Fix:** 2x conversion rate before adding new streams

### 5. Crippled Free Tier
**Symptom:** Free tier so limited it's useless
**Fix:** Users who never experience value never convert

### 6. No Email List
**Symptom:** Relying only on organic traffic
**Fix:** Build list before you need it - foundation for everything

### 7. One-Size-Fits-All Pricing
**Symptom:** Same price for hobbyists and enterprises
**Fix:** Segment pricing by use case and value

### 8. Hidden Costs
**Symptom:** Surprise fees after signup
**Fix:** Transparent pricing builds trust

### 9. Ignoring Churn
**Symptom:** Focus on acquisition, not retention
**Fix:** Reducing churn 5% can increase profits 25-95%

### 10. Pricing Too Low
**Symptom:** Undervaluing your work
**Fix:** Higher prices = better customers, higher expectations

## Revenue Benchmarks (Indie Scale)

| Stage | Monthly Revenue | Meaning |
|-------|-----------------|---------|
| Ramen Profitable | $2-5k | Can quit day job (barely) |
| Comfortable | $10-20k | Good indie income |
| Scaling | $50k+ | Time to consider hiring |

**Reality check:** Most indie projects earn $0-500/month. $2k/month = top 10%.

## Quick Implementation

### Add Payments (5 min with Stripe)

```typescript
// See references/stripe-integration.md for complete guide
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  line_items: [{ price: 'price_xxx', quantity: 1 }],
  success_url: 'https://yoursite.com/success',
});
```

### Add Sponsorship Button

```html
<a href="https://github.com/sponsors/yourusername">
  <img src="https://img.shields.io/badge/Sponsor-💖-ea4aaa">
</a>
```

### Launch Email Sequence

```
Day 0: Deliver lead magnet + welcome
Day 3: Best content piece
Day 7: Your story/why you built this
Day 14: Soft pitch
Day 21: Social proof
Day 30: Direct pitch with deadline
```

## Reference Files

| File | Contents |
|------|----------|
| `references/pricing-templates.md` | HTML/CSS pricing page templates |
| `references/email-sequences.md` | Complete email sequence examples |
| `references/stripe-integration.md` | Full Stripe implementation guide |

---

**Covers:** Monetization Strategy | Pricing Psychology | Freemium | Sponsorships | Email Marketing

**Use with:** content-marketer (distribution) | web-design-expert (pricing pages) | product-strategist (positioning)
