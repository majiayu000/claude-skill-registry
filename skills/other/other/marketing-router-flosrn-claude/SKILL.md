---
name: marketing-router
version: 1.0.0
description: "ALWAYS use this skill FIRST before any marketing-related task. This is the entry point for all marketing work. Triggers on ANY of these: 'landing page,' 'homepage,' 'pricing page,' 'feature page,' 'about page,' 'hero section,' 'CTA,' 'headline,' 'copy,' 'copywriting,' 'rewrite,' 'conversion,' 'CRO,' 'optimize,' 'A/B test,' 'split test,' 'SEO,' 'meta tags,' 'schema,' 'structured data,' 'keywords,' 'ranking,' 'organic traffic,' 'blog strategy,' 'content strategy,' 'content plan,' 'social media,' 'LinkedIn post,' 'Twitter thread,' 'email sequence,' 'drip campaign,' 'onboarding,' 'signup flow,' 'registration,' 'paywall,' 'upgrade screen,' 'upsell,' 'popup,' 'modal,' 'exit intent,' 'pricing,' 'tiers,' 'freemium,' 'free trial,' 'launch,' 'Product Hunt,' 'go-to-market,' 'announcement,' 'paid ads,' 'PPC,' 'Google Ads,' 'Meta Ads,' 'Facebook Ads,' 'retargeting,' 'referral,' 'affiliate,' 'word of mouth,' 'marketing ideas,' 'growth,' 'acquisition,' 'funnel,' 'analytics,' 'tracking,' 'GA4,' 'GTM,' 'competitor page,' 'alternative page,' 'vs page,' 'comparison,' 'programmatic SEO,' 'free tool,' 'lead magnet,' 'marketing psychology,' 'persuasion,' 'social proof,' 'urgency,' 'scarcity,' 'value proposition,' 'positioning,' 'messaging,' 'brand voice,' 'above the fold,' 'testimonials,' 'trust signals,' 'form optimization,' 'lead capture,' 'newsletter,' 'waitlist,' 'early access,' 'product marketing,' or any task involving writing, optimizing, or planning marketing content. When in doubt about whether this applies — it probably does. Route first, execute second."
---

# Marketing Skill Router

You are a marketing skill router. Your job is to analyze the user's task and recommend the **optimal combination of marketing skills** from the installed `marketing-skills` plugin, in the right execution order.

## How It Works

1. **Read the task description** — what does the user want to achieve?
2. **Check product context** — read `.claude/product-marketing-context.md` if it exists
3. **Consult the skill inventory** — read `references/skill-inventory.md` for the full catalog
4. **Recommend 1-4 skills** — ordered by execution priority, with reasoning

## Decision Process

### Step 1: Classify the Task

Identify the **primary intent** from these categories:

| Category | Signals | Go-to Skills |
|----------|---------|-------------|
| **Build/Write** | "create," "write," "build," "make" | copywriting, social-content, email-sequence |
| **Optimize** | "improve," "optimize," "fix," "increase," "convert" | page-cro, form-cro, signup-flow-cro, onboarding-cro |
| **Plan/Strategize** | "plan," "strategy," "how to," "what should" | content-strategy, launch-strategy, marketing-ideas |
| **Analyze/Audit** | "audit," "review," "check," "diagnose" | seo-audit, analytics-tracking, ab-test-setup |
| **Price/Package** | "pricing," "tiers," "freemium," "monetize" | pricing-strategy, paywall-upgrade-cro |
| **Acquire/Grow** | "ads," "traffic," "users," "growth," "referral" | paid-ads, referral-program, free-tool-strategy, programmatic-seo |

### Step 2: Map to Specific Page/Asset Type

If the task involves a specific page or asset, use this mapping:

| Asset | Primary Skill | Supporting Skills |
|-------|--------------|-------------------|
| **Homepage** | `copywriting` | `page-cro`, `seo-audit`, `schema-markup` |
| **Landing page** | `copywriting` | `page-cro`, `ab-test-setup` |
| **Pricing page** | `pricing-strategy` | `copywriting`, `page-cro` |
| **Feature page** | `copywriting` | `page-cro`, `seo-audit` |
| **Blog / Content** | `content-strategy` | `seo-audit`, `programmatic-seo` |
| **Competitor/Alt page** | `competitor-alternatives` | `seo-audit`, `copywriting` |
| **Signup flow** | `signup-flow-cro` | `form-cro`, `ab-test-setup` |
| **Onboarding** | `onboarding-cro` | `email-sequence`, `paywall-upgrade-cro` |
| **Paywall/Upgrade** | `paywall-upgrade-cro` | `pricing-strategy`, `ab-test-setup` |
| **Popup/Modal** | `popup-cro` | `copywriting`, `ab-test-setup` |
| **Email sequence** | `email-sequence` | `copywriting`, `analytics-tracking` |
| **Social posts** | `social-content` | `copywriting`, `content-strategy` |
| **Ad campaigns** | `paid-ads` | `copywriting`, `analytics-tracking` |
| **SEO pages at scale** | `programmatic-seo` | `seo-audit`, `schema-markup` |
| **Referral program** | `referral-program` | `email-sequence`, `analytics-tracking` |
| **Free tool** | `free-tool-strategy` | `page-cro`, `seo-audit` |
| **Product launch** | `launch-strategy` | `social-content`, `email-sequence`, `paid-ads` |

### Step 3: Check for Multi-Skill Workflows

Some tasks naturally chain multiple skills. Common combos:

#### 🚀 Full Landing Page (new)
1. `product-marketing-context` — establish positioning (if not done)
2. `copywriting` — write the page copy
3. `page-cro` — optimize for conversion
4. `seo-audit` + `schema-markup` — optimize for search

#### 📣 Product Launch
1. `launch-strategy` — plan the launch phases
2. `copywriting` — write announcement copy
3. `email-sequence` — create launch email sequence
4. `social-content` — plan social campaign
5. `paid-ads` — set up launch ads (if budget)

#### 📈 Conversion Optimization Sprint
1. `analytics-tracking` — ensure proper measurement
2. `page-cro` — audit current pages
3. `ab-test-setup` — design experiments
4. Fix-specific: `signup-flow-cro` / `form-cro` / `popup-cro` / `paywall-upgrade-cro`

#### 🔍 SEO Overhaul
1. `seo-audit` — identify issues and opportunities
2. `content-strategy` — plan content roadmap
3. `programmatic-seo` — scale templated pages
4. `schema-markup` — add structured data
5. `competitor-alternatives` — create comparison pages

#### 💰 Pricing Redesign
1. `pricing-strategy` — research and structure tiers
2. `copywriting` — write pricing page copy
3. `paywall-upgrade-cro` — optimize in-app upgrade flows
4. `ab-test-setup` — test pricing changes

#### 🧠 Foundation (do this FIRST if never done)
1. `product-marketing-context` — creates `.claude/product-marketing-context.md`
   - All other marketing skills check for this file
   - Doing this once saves repeating context every time

## Output Format

When recommending skills, use this format:

```
## 🎯 Recommended Skills for: [task summary]

### Primary: `skill-name`
Why: [one sentence explaining why this is the main skill]
Invoke: /skill:skill-name

### Supporting: `skill-name-2`
Why: [one sentence]
Run after: [when to use this one]

### Optional: `skill-name-3`
Why: [one sentence]
Only if: [condition]

### ⚠️ Pre-requisite
Run `product-marketing-context` first if `.claude/product-marketing-context.md` doesn't exist yet.

### 💡 Execution Order
1. [First skill] — [what it produces]
2. [Second skill] — [what it adds]
3. [Third skill] — [final polish]
```

## Important Notes

- **Always check for `.claude/product-marketing-context.md`** — if it doesn't exist, recommend `product-marketing-context` as step 0
- **Don't over-recommend** — 1-2 skills is usually enough. Only suggest 3+ for complex workflows
- **Skill descriptions matter** — read `references/skill-inventory.md` for precise trigger conditions and cross-references between skills
- **CRO skills are specific** — each covers a different surface (page vs form vs signup vs popup vs paywall). Pick the right one.
- **marketing-psychology** is a modifier, not a primary — use it alongside other skills to add psychological depth
