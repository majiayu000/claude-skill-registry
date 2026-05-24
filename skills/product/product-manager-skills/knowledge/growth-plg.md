# Growth & Product-Led Growth

Compressed reference for product-led growth: PLG readiness assessment, activation funnel design, viral mechanics, freemium conversion strategy, self-serve onboarding, and growth experimentation frameworks.

## PLG Readiness & Positioning

### PLG vs SLG Decision Framework

Not every product should be product-led. Assess fit before committing.

| Dimension | PLG Fit (strong) | SLG Fit (strong) |
|-----------|-----------------|------------------|
| **Buyer** | End user can evaluate alone | Committee decision, multi-stakeholder |
| **Price point** | <$500/mo starting tier | >$50K ACV |
| **Time-to-value** | Minutes to hours | Weeks (requires integration, training) |
| **Complexity** | Low config, self-explanatory | Custom implementation, professional services |
| **Data sensitivity** | Low-medium (user can sign up freely) | High (security review, procurement) |
| **Network effects** | Strong (value grows with users) | Weak (value is per-seat) |

**Hybrid PLG+SLG:** Most B2B SaaS is hybrid. PLG generates pipeline, sales closes enterprise deals. The question is which motion leads.

**Decision rule:** If a user can reach the "aha moment" without talking to a human, PLG is viable. If the aha moment requires integration, data migration, or team adoption, start SLG with a PLG layer for expansion.

### PLG Maturity Levels

| Level | Description | Signals |
|-------|-------------|---------|
| **0: No PLG** | Sales-only, no self-serve | No free tier, no public pricing, demo required |
| **1: PLG-Assisted** | Free trial or freemium exists, but sales drives conversion | <10% of revenue from self-serve, most users convert via sales touch |
| **2: PLG-Primary** | Self-serve drives majority of new revenue | >50% self-serve conversion, sales handles expansion only |
| **3: PLG-Native** | Product is the growth engine | Viral loops active, >70% self-serve, negative churn from expansion |

## Activation & Onboarding

### Activation Framework

Activation = the moment a user experiences enough value to form a habit. Not signup. Not login. The specific action that predicts retention.

**Finding your activation metric:**
1. Identify users who retained at 30 days (or your retention period)
2. Compare their first-session behavior vs. churned users
3. Find the action with highest correlation to retention
4. That action is your activation event

**Examples:**
- Slack: send 2,000 messages as a team (not "create a workspace")
- Dropbox: put a file in one folder on one device (not "sign up")
- Zoom: complete one meeting (not "download the app")

**Activation rate formula:** `Users who hit activation event / Total signups x 100`

**Benchmarks by model:**
| Model | Good | Great | Best-in-class |
|-------|------|-------|---------------|
| Free trial (14-day) | 15-25% | 25-40% | >40% |
| Freemium | 5-15% | 15-30% | >30% |
| Reverse trial | 20-35% | 35-50% | >50% |

### Onboarding Design Principles

1. **Time-to-value, not time-to-feature.** Measure how fast users reach the activation event, not how fast they see the settings page.
2. **Progressive disclosure.** Show only what's needed for the next step. Hide advanced features until the user needs them.
3. **Contextual, not front-loaded.** Tooltips and guidance at the moment of need beat a 10-step setup wizard.
4. **Empty states are product.** Every empty state is a chance to show value. "No data yet" is a dead end. "Import your first X to see Y" is a pathway.
5. **Reduce time-to-first-value (TTFV).** If TTFV > 5 minutes for consumer, > 30 minutes for prosumer, or > 1 day for B2B, you have a friction problem.

### Onboarding Diagnostic

When activation rate is below benchmark, diagnose with this funnel:

| Stage | Drop-off signal | Common fix |
|-------|----------------|------------|
| Signup → First action | >60% drop-off | Reduce signup friction (fewer fields, SSO, defer profile) |
| First action → Activation event | >70% drop-off | Shorten path to aha moment (pre-fill data, templates, sample content) |
| Activation → Day 7 return | >50% drop-off | Add engagement hooks (email, notification, incomplete task reminder) |
| Day 7 → Day 30 habit | >40% drop-off | Build habit loops (regular value delivery, streaks, team features) |

## Viral & Network Effects

### Viral Loop Design

A viral loop has 4 components:

1. **Trigger:** User encounters a reason to invite others (collaboration, sharing, showing off)
2. **Action:** User sends an invitation or creates shareable content
3. **Conversion:** Recipient signs up and becomes active
4. **Value delivery:** New user gets enough value to trigger their own loop

**Viral coefficient (K-factor):** `K = invitations sent per user x conversion rate per invitation`
- K < 1: not viral (most products). Paid acquisition required.
- K = 1: sustainable but not growing. Each user replaces themselves.
- K > 1: exponential growth. Rare and usually temporary.

**Practical target:** K = 0.3-0.7 (viral-assisted, not viral-dependent). Reduces CAC by 30-70% even without exponential growth.

### Types of Virality

| Type | Mechanism | Example | Strength |
|------|-----------|---------|----------|
| **Inherent** | Product requires others to function | Slack, Zoom, Figma | Strongest, built into core value |
| **Collaborative** | Product improves with more users | Google Docs, Notion | Strong, tied to use case |
| **Word-of-mouth** | Users tell others because it's good | Linear, Arc | Medium, hard to engineer |
| **Incentivized** | Rewards for referrals | Dropbox (+500MB), PayPal ($10) | Weak long-term, good for launch |
| **Content** | User-generated content attracts new users | Substack, YouTube | Strong if content is public |

### Network Effects Assessment

| Question | If Yes | If No |
|----------|--------|-------|
| Does the product get more valuable as more people use it? | Direct network effect present | Single-player value only |
| Do users create content that attracts new users? | Content network effect | No organic discovery |
| Does usage data improve the product for everyone? | Data network effect | No compounding advantage |
| Can users build on top of the product? | Platform network effect | Closed ecosystem |

**Network effects ≠ virality.** Network effects increase value for existing users. Virality increases distribution to new users. Both can exist independently.

## Freemium & Conversion

### Freemium Model Types

| Model | Free tier | Conversion trigger | Best for |
|-------|-----------|-------------------|----------|
| **Feature-limited** | Core features free, advanced paid | User hits feature ceiling | Tools with clear feature tiers (Slack, Zoom) |
| **Usage-limited** | All features, limited volume | User exceeds usage quota | Storage, API, compute products (Dropbox, Vercel) |
| **Seat-limited** | Full product, limited team size | Team grows beyond free limit | Collaboration tools (Notion, Linear) |
| **Time-limited (reverse trial)** | Full product for 14-30 days, then drops to free | Trial ends, user downgrades or converts | Complex products where free tier is hard to define |

### Free-to-Paid Conversion Diagnostic

**Conversion rate formula:** `Paid users / Total free users x 100`

**Benchmarks:**
| Model | Low | Healthy | Strong |
|-------|-----|---------|--------|
| Freemium (feature) | 1-2% | 3-5% | >5% |
| Freemium (usage) | 2-4% | 5-8% | >8% |
| Free trial | 10-15% | 15-25% | >25% |
| Reverse trial | 15-25% | 25-40% | >40% |

**Common conversion failures:**
- **Free tier too generous:** Users never hit the ceiling. Fix: audit feature usage in free tier, move sticky features to paid.
- **Free tier too restrictive:** Users can't experience value. Fix: ensure the activation event is achievable on the free tier.
- **No upgrade trigger:** User hits ceiling but sees no prompt. Fix: contextual upgrade prompts at the moment of friction.
- **Price shock:** Free to $99/mo with nothing in between. Fix: add a low entry-point tier ($9-29/mo).

## Growth Experimentation

### Growth Experiment Framework

Every growth experiment needs 5 things before running:

1. **Hypothesis:** "If we [change], then [metric] will [direction] by [amount] because [reason]."
2. **Primary metric:** One number that decides success or failure.
3. **Guardrail metric:** One number that must not degrade (e.g., test activation rate but guardrail retention).
4. **Sample size:** Minimum users needed for statistical significance. Use a sample size calculator.
5. **Duration:** Minimum time to capture full effect (at least 1 full user lifecycle).

### Experiment Prioritization (ICE for Growth)

| Factor | Score 1-10 | Question |
|--------|-----------|----------|
| **Impact** | How much will this move the target metric? | 1 = marginal, 10 = step change |
| **Confidence** | How sure are you it will work? | 1 = pure guess, 10 = strong evidence |
| **Ease** | How fast can you ship and measure? | 1 = months of eng, 10 = same-day deploy |

**ICE Score = (I + C + E) / 3.** Run the highest-scoring experiment first.

**Anti-patterns in experimentation:**
- Running 10 experiments with no prioritization
- Declaring results in 3 days (too short for user behavior to stabilize)
- Testing copy changes and expecting 10x improvement
- Ignoring guardrail metrics ("activation went up but retention dropped")
- Not logging experiment results (losing institutional knowledge)

### Growth Metrics Dashboard

Track these 6 metrics weekly for a PLG product:

| Metric | Formula | Why it matters |
|--------|---------|----------------|
| **Signup → Activation rate** | Activated users / Signups | Core health indicator |
| **Activation → Paid conversion** | Paid / Activated | Monetization efficiency |
| **Time-to-value (TTFV)** | Median time from signup to activation event | Onboarding friction indicator |
| **Viral coefficient (K)** | Invites sent per user x invite conversion rate | Organic growth potential |
| **Expansion rate** | Expansion MRR / Starting MRR | Revenue growth from existing users |
| **Logo retention (monthly)** | 1 - (churned users / starting users) | Base health, see `finance-metrics.md` for full churn framework |

**Cross-reference with finance-metrics.md** for detailed formulas on NRR, LTV, CAC, and churn analysis. This module focuses on the top-of-funnel and activation metrics. Bottom-of-funnel retention and unit economics live in `knowledge/finance-metrics.md`.

## Quality Gates

### PLG Anti-Patterns

- **PLG theater:** Adding a free tier without instrumenting activation. You have a free plan, not PLG.
- **Premature PLG:** Launching self-serve before the product can deliver value without human help. Result: low activation, high support cost.
- **Viral delusion:** Assuming K > 1 in your financial model. Almost no product sustains K > 1. Plan for K = 0.3-0.5.
- **Conversion theater:** Optimizing free-to-paid conversion rate while ignoring absolute numbers. 50% conversion of 10 users is worse than 5% conversion of 10,000.
- **Feature gating without data:** Deciding what's free vs. paid based on opinion instead of usage data. Audit first, gate second.
- **Onboarding as afterthought:** Treating onboarding as a one-time project, not a continuous product surface.
- **Vanity activation:** Defining activation as "completed onboarding wizard" instead of the action that actually predicts retention.

### Growth Experiment Anti-Patterns

- Testing without a hypothesis
- Stopping experiments early because results "look good"
- Blaming users for low activation instead of diagnosing the funnel
- Optimizing a step in the funnel without understanding the full funnel
- Copying another company's growth tactic without understanding their context

## Interaction Rules (Coaching Mode)

When coaching is active for growth and PLG topics, use these rules.

| Trigger | Action | Stop When |
|---------|--------|-----------|
| User says "we need PLG" without articulating why | Push: "What's the specific user behavior that would change if you added a free tier? What does the user do today instead?" | User names specific activation event and current alternative |
| Activation metric is vague ("users engage with the product") | Challenge: "What single action, done in the first session, best predicts a user will still be active at day 30?" | User names a specific, measurable action |
| Viral loop is assumed but not designed | Push: "Walk me through the loop: what triggers a user to invite someone, what does the invitee see, and why would they sign up?" | User describes all 4 loop components |
| Freemium tier designed without usage data | Challenge: "Which features do free users actually use weekly? Which do they never touch? Show me the data before gating." | User provides usage data or acknowledges the gap |
| Growth experiment has no guardrail metric | Push: "If this experiment increases activation but tanks retention, would you still call it a win? What's your guardrail?" | User names a guardrail metric |
| User has answered 2 follow-ups on the same point | Stop pushing. Summarize what's still weak and give best-guess output. | -- |
