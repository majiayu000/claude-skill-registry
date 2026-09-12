---
name: marketing-psychology
description: |
  Knowledge skill that applies behavioral psychology and persuasion principles to any marketing asset. Covers Cialdini's 6 principles, cognitive biases, and ethical persuasion frameworks. This skill is invoked BY other skills to enhance their output. Use it whenever copy needs more psychological weight, when a landing page feels flat, when email sequences lack urgency, or when any marketing asset needs to be more persuasive. Also use when someone says 'make this more convincing', 'add urgency', 'psychological triggers', 'persuasion framework', 'behavioral psychology', 'conversion optimization', 'nudge', 'influence tactics', or 'why isn't this converting'. Make sure to use this whenever ANY marketing copy needs to be more persuasive, even if the user just says 'this feels weak' or 'how do I get more signups', psychology principles likely apply.
category: knowledge
layer: foundation
tier: nice-to-have
reads:
  - brand/positioning.md
  - brand/audience.md
  - brand/voice-profile.md
writes: []
depends-on: []
triggers:
  - marketing psychology
  - persuasion
  - Cialdini
  - scarcity
  - social proof
  - cognitive bias
  - psychological triggers
  - influence tactics
  - make this more convincing
  - add urgency
allowed-tools: []
---

# Marketing Psychology

## Purpose

This is a KNOWLEDGE skill. It does not produce standalone deliverables. Instead, it enhances any marketing asset — landing pages, emails, ads, CTAs, pricing pages, onboarding flows — by applying behavioral psychology principles that increase persuasion and conversion.

When another skill produces copy or UX, this skill provides the psychological layer: why certain framings work, which biases to apply, and specific before/after rewrites grounded in research.

## No Reads/Writes

This skill is pure reference. It reads no brand files and writes no outputs. It is applied ON TOP of other skills' work.

## Brand Context Enhancement

While this skill reads no files itself, the calling skill should provide brand context when available:

- **audience.md** -> Knowing the audience helps select the right social proof type (peer testimonials for B2B, user statistics for consumer), the right authority signals (industry certifications for enterprise, founder story for indie), and the right scarcity framing (launch pricing for startups, seat limits for teams).
- **voice-profile.md** -> Brand voice affects HOW principles are applied. A playful brand uses conversational loss aversion ("Don't miss out on..."). A professional brand uses data-driven framing ("Companies without X lose an average of...").
- **positioning.md** -> Premium positioning supports authority and anchoring. Challenger positioning supports liking and social proof from peers.

When calling this skill, pass relevant brand context so principles are applied in voice, not generically.

## Workflow

### Step 1: Identify the Asset Type

Determine what marketing asset is being optimized:

- Landing page (hero, body, CTA)
- Email (subject, body, CTA)
- Ad copy (headline, description, creative)
- Pricing page (tiers, anchoring, CTA)
- Onboarding flow (screens, copy, nudges)
- Social post (hook, body, CTA)
- Cancel flow (retention, objection handling)
- Sales page (long-form persuasion)

### Step 2: Select Applicable Principles

Not every principle applies to every asset. Match principles to context. Use the Application Matrix below for quick selection.

### Step 3: Consider B2B vs B2C Differences

| Principle | B2B Emphasis | B2C Emphasis |
|-----------|-------------|-------------|
| Social proof | Case studies, logos, ROI metrics | User counts, ratings, peer testimonials |
| Authority | Industry certifications, compliance | Celebrity endorsements, media features |
| Scarcity | Limited pilot spots, implementation slots | Limited stock, countdown timers |
| Loss aversion | Revenue at risk, competitive disadvantage | Missing out on experiences, wasted time |
| Anchoring | ROI comparison, cost of inaction | Was/now pricing, competitor comparison |

**For real-world case studies of each principle in action:** See [references/case-studies.md](references/case-studies.md) — 11 examples from companies like HubSpot, Netflix, Stripe, Duolingo, and Superhuman showing how principles translate to specific implementations.

## How to Use This Skill

This is a knowledge skill — it enhances other skills' output rather than producing standalone deliverables.

**Invocation pattern:** When another skill produces copy or UX, ask: "Apply marketing psychology principles to this asset." This skill audits the output and suggests principle-specific rewrites.

**Example:** After /direct-response-copy produces a landing page, apply this skill to audit the hero for anchoring, the CTA for scarcity, and the testimonials for social proof.

## Cialdini's 6 Principles of Persuasion

### 1. Reciprocity

People feel obligated to return favors. Give value first, ask second.

**Application:**
- Free tools, templates, guides before asking for signup
- Free trial with no credit card (gift, not trap)
- Personalized recommendations or audit before pitching

**Before:** "Sign up for our product"
**After:** "Here's a free audit of your [X]. Want to fix these issues automatically? [Start free trial]"

**Why this works:** Giving value before asking creates an obligation loop — the free checklist makes the paid product feel like a natural next step, not a cold ask.

**Where it works best:** Lead magnets, free tools, onboarding emails, content marketing

### 2. Commitment and Consistency

People who take small steps continue in the same direction. Micro-commitments build toward conversion.

**Application:**
- "Yes ladder" — series of small agreements before the big ask
- Interactive tools that invest the user's time (endowment effect crossover)
- Public commitments: sharing goals, publishing results
- Progressive profiling: ask for email first, details later

**Before:** "Buy our annual plan for $299/year"
**After:** "Start your free project -> See your first results -> Upgrade when you're ready"

**Why this works:** Each small yes builds psychological momentum — once someone has invested time and seen results, saying yes to payment feels consistent with their prior actions.

**Where it works best:** Signup flows, onboarding, pricing pages, email sequences

### 3. Social Proof

People follow the actions of others, especially similar others.

**Types of social proof (ordered by persuasion strength):**

| Type | Example | Strength |
|------|---------|----------|
| Expert endorsement | "[Industry expert] recommends [Product]" | Highest |
| Celebrity/Influencer | "[Known figure] uses [Product]" | High |
| User statistics | "12,847 teams use [Product]" | High |
| Peer testimonial | "[Same role/industry] saw [specific result]" | High |
| Certification/Award | "G2 Leader, 4.8/5 stars" | Medium |
| Wisdom of crowds | "Most popular plan" badge | Medium |
| Friend referral | "[Name] invited you" | Highest (context-dependent) |

**Before:** "Our product is great"
**After:** "12,847 marketing teams use [Product] to save 10+ hours/week. Here's what [Similar Company] achieved in 30 days."

**Why this works:** Humans use others' behavior as a decision shortcut — specific numbers and named peers eliminate the need to evaluate the product independently.

**Where it works best:** Every asset. No exceptions. Always include social proof.

### 4. Authority

People defer to experts and credible sources.

**Authority signals:**
- Founder credentials and expertise
- Media logos ("As seen in TechCrunch, Forbes")
- Data and research citations
- Industry certifications and compliance badges
- Published content demonstrating expertise
- Years in business, customers served

**Before:** "We help with email marketing"
**After:** "Built by the team that scaled [Company]'s email list from 0 to 500K subscribers"

**Why this works:** Concrete credentials transfer trust instantly — the reader borrows confidence from the known achievement rather than evaluating your claim from scratch.

**Where it works best:** Landing pages, about pages, sales emails, B2B proposals

### 5. Liking

People buy from people (and brands) they like. Similarity, compliments, and cooperation build liking.

**Application:**
- Use customer's language, not corporate jargon
- Show the team (real photos, real names)
- Mirror the audience's values and frustrations
- Conversational tone > formal tone
- "We built this because we had this problem too"

**Before:** "Our enterprise-grade solution leverages AI-powered analytics"
**After:** "We were tired of staring at spreadsheets too. So we built [Product]."

**Why this works:** Mirroring the audience's frustration signals "we're one of you" — people trust and buy from those who understand their lived experience.

**Where it works best:** Brand voice, about pages, founder stories, email tone

### 6. Scarcity

People value what's limited. Real scarcity drives action; manufactured scarcity destroys trust.

**Legitimate scarcity patterns:**
- Limited beta access (real capacity constraint)
- Expiring discounts tied to events (launch pricing, annual sale)
- Feature limits on free tier (natural product boundary)
- Seats or usage limits (infrastructure reality)

**Illegitimate scarcity (never use):**
- Fake countdown timers that reset
- "Only 2 left!" when there's unlimited supply
- Artificial waitlists for available products
- Urgency language with no actual deadline

**Before:** "Sign up anytime"
**After:** "Launch pricing: $29/mo for the first 500 customers (347 claimed)" — only if real

**Why this works:** Real scarcity activates fear of missing out on a genuine opportunity — the specific count (347/500) makes the constraint feel tangible and urgent without feeling manufactured.

**Where it works best:** Pricing pages, launch campaigns, limited offers (when genuine)

## Cognitive Biases for Marketing

### Loss Aversion

People feel losses 2x more intensely than equivalent gains. Frame around what they'll lose, not just what they'll gain.

**Before:** "Save 10 hours per week with [Product]"
**After:** "You're losing 10 hours every week to [manual task]. [Product] gives them back."

**Why this works:** The pain of losing 10 hours hits harder than the pleasure of saving them — reframing a gain as a recovered loss doubles the emotional weight.

**Application:** Cancel flows, upgrade prompts, trial expiration emails, feature comparison

### Anchoring

The first number people see becomes the reference point. Control the anchor.

**Application:**
- Show highest-priced plan first on pricing page
- Compare your price to the cost of the problem: "Losing $5K/month to [problem]? Fix it for $49/month."
- Show original price crossed out next to sale price
- "Teams spend 20 hours/week on [task]. [Product] reduces it to 2."

**Pricing page pattern:**
```
Enterprise: $299/mo  <-  Anchor
Pro: $99/mo          <-  Looks reasonable now
Starter: $29/mo      <-  Feels like a steal
```

### Endowment Effect

People value things more once they feel ownership. Let them invest before asking to pay.

**Application:**
- Free trials that let users create real work (not sandboxed demos)
- "Your dashboard", "Your projects" language from day one
- Showing what they'll lose at trial end: "You have 3 active projects and 47 contacts"
- Data import during onboarding (invested effort = harder to leave)

### IKEA Effect

People value things they helped build. Involvement increases attachment.

**Application:**
- Onboarding that involves customization (pick your theme, set your goals)
- Interactive tools that require user input
- Templates users modify rather than pre-built outputs
- "Built by you" framing for created assets

### Paradox of Choice

Too many options -> decision paralysis -> no action. Reduce choices, add recommendations.

**Application:**
- 3 pricing tiers maximum, one highlighted as "Most Popular"
- "Recommended for you" based on signup answers
- Default selections for settings and preferences
- "Start here" guidance instead of feature overwhelm

**Before:** 5 plan tiers with 40 feature comparison rows
**After:** 3 plans, "Most Popular" badge on middle tier, "Not sure? Start with Pro" CTA

**Why this works:** Reducing options from 5 to 3 eliminates decision paralysis, and the "Most Popular" badge gives permission to stop comparing — the crowd already chose for you.

### Zero-Risk Bias

People strongly prefer eliminating a risk entirely over reducing it. Money-back guarantees outperform discount offers.

**Application:**
- "30-day money-back guarantee. No questions asked."
- "Cancel anytime. No contracts, no penalties."
- "Free tier available forever" (eliminates downgrade anxiety)
- "We'll migrate your data for free" (eliminates switching risk)

### Framing Effect

The same information presented differently changes decisions. Frame to match your goal.

**Application:**
- "95% uptime" vs "Only 5% downtime" — same fact, different feeling
- "Join 10,000 happy customers" vs "Don't be one of the few who miss out"
- "Save $120/year" vs "Save $10/month" — annual framing feels bigger for savings
- Positive frame for gains ("Get X"), negative frame for preventing losses ("Stop losing X")

**Before:** "Our tool has 99.9% accuracy"
**After:** "Our tool catches 999 out of every 1,000 errors — so nothing slips through"

**Why this works:** Concrete framing (999/1000) is more vivid than abstract percentages. The reader can picture the result.

### Status Quo Bias

People prefer the current state of affairs. Reducing friction to switch is more effective than amplifying benefits.

**Application:**
- "Import your data in one click" (reduces switching cost)
- "Works with tools you already use" (no workflow change)
- "Keep your existing setup — we just plug in"
- Free migration services eliminate the biggest barrier

**Where it works best:** Competitor displacement, upgrade prompts, onboarding

### Mere Exposure Effect

Familiarity breeds preference. People like what they've seen before.

**Application:**
- Retargeting ads that keep your brand visible
- Consistent visual branding across all touchpoints
- Content marketing that puts your name in front of prospects repeatedly
- Email nurture sequences that build familiarity before asking for the sale

**Where it works best:** Top-of-funnel content, retargeting, email sequences, social media presence

## Framework Application Matrix

Quick reference — which principles apply to which assets:

| Principle | Landing Page | Email | Pricing | Onboarding | Ads |
|-----------|-------------|-------|---------|------------|-----|
| Reciprocity | Medium | High | Low | High | Low |
| Commitment | Low | High | Medium | High | Low |
| Social Proof | High | Medium | High | Medium | High |
| Authority | High | Medium | Medium | Low | High |
| Liking | Medium | High | Low | High | Medium |
| Scarcity | Medium | High | High | Low | High |
| Loss Aversion | Medium | High | High | High | Medium |
| Anchoring | Medium | Low | High | Low | Medium |
| Endowment | Low | Medium | Low | High | Low |
| Framing | High | High | Medium | Medium | High |
| Status Quo | Medium | Low | Low | High | Medium |

## How to Apply This Skill

When reviewing any marketing asset:

1. **Identify** the asset type and primary conversion goal
2. **Select** 2-4 most relevant principles (don't force all of them)
3. **Consider** B2B vs B2C context — application differs significantly
4. **Audit** current copy/UX for existing psychology use (intentional or accidental)
5. **Suggest** specific changes with before/after examples
6. **Prioritize** by expected impact: social proof and loss aversion almost always win
7. **Warn** about dark patterns: if a suggestion feels manipulative, flag it and offer an ethical alternative

## Anti-Patterns

| Mistake | Why it fails | Instead |
|---------|-------------|---------|
| Applying all principles to every asset | Stacking 10 principles on one page creates a manipulative wall of tricks that readers feel viscerally — less is more persuasive | Select 2-4 most relevant using the Application Matrix |
| Forcing scarcity where none exists | Users share notes about fake urgency on social media — one "fake countdown timer" screenshot can destroy brand trust permanently | Only use scarcity with real constraints. Fake urgency destroys trust |
| Generic "add social proof" without specifics | "Add social proof" gives the agent nothing to work with — peer testimonials work differently than user counts, and the wrong type falls flat | Specify the TYPE of social proof (peer testimonial, user count, expert endorsement) based on audience |
| Applying principles without considering brand voice | A corporate brand writing "Don't miss out!!" and a playful brand writing "Enterprise-grade urgency metrics" both sound absurd | A playful brand and a corporate brand apply the same principle very differently |
| Suggesting dark patterns as psychological techniques | Dark patterns generate short-term conversions but long-term refunds, chargebacks, and reputation damage | Always apply the transparency test: would you be comfortable if the user knew? |
| Ignoring that the asset might already be effective | Over-optimizing working copy risks breaking what already converts — psychology should enhance, not overhaul | Audit first — if conversion is strong, don't add psychology for the sake of it |

## Ethical Boundaries

Use psychology to help people make better decisions, not to trick them:

- **Use:** Helping users understand value they're already getting (loss aversion in cancel flow)
- **Don't use:** Manufacturing fake urgency to pressure purchases
- **Use:** Social proof showing real users with real results
- **Don't use:** Fake testimonials or inflated numbers
- **Use:** Anchoring to help frame fair pricing in context
- **Don't use:** Hiding fees or making comparison deliberately confusing
- **Use:** Commitment/consistency to help users follow through on goals they set
- **Don't use:** Dark patterns that make cancellation impossible

The test: Would you be comfortable if the user knew exactly what psychological principle you were applying? If yes, proceed. If no, find another approach.
