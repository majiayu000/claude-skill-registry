---
name: conversion-flow-cro
description: |
  Optimizes multi-step conversion flows including signup, onboarding, upgrade, and checkout. Maps each step, identifies friction and drop-off risks, then recommends specific copy/UX changes with A/B test plans. Use when someone says 'signup flow', 'onboarding optimization', 'checkout conversion', 'paywall optimization', 'activation rate', 'funnel analysis', 'why are users dropping off', 'registration flow', 'trial conversion', 'free to paid', 'upgrade flow', 'user journey', or wants to improve any multi-step user journey. If they mention steps, screens, or a sequence that leads to signup, payment, or activation, this is the skill. Even casual mentions like 'users aren't finishing signup' or 'our onboarding sucks' should trigger this. Use this instead of page-cro when the problem spans multiple screens rather than a single page.
allowed-tools: []
---

# Conversion Flow CRO

## Purpose

Audit and optimize any multi-step conversion flow — signup, onboarding, trial-to-paid, checkout, upgrade. Map every step, find where people drop off, and fix each screen with specific copy and UX changes.

## Reads

- `brand/audience.md` — Personas, pain points, motivation levels at each stage
- `brand/positioning.md` — Value props for reinforcement copy at each step
- `brand/voice-profile.md` — Brand voice for all copy suggestions

## Brand Integration

- **audience.md** — Persona determines friction tolerance. A developer persona accepts more setup steps; a non-technical buyer needs fewer. Pain points inform which value reminders to show at each step.
- **positioning.md** — Value proposition reinforcement copy at each step should echo the positioning angle. If the brand positions on "saves time," every motivation booster references time savings.
- **voice-profile.md** — All redesigned copy (headlines, CTAs, supporting text) must match brand voice. A casual brand writes "Almost there!" while a professional brand writes "One final step."

## Workflow

### Step 1: Map the Current Flow

Get the flow information. Try these in order:
1. **User provides screenshots or screen recordings** — Best source, map directly
2. **Read the codebase** — If accessible, find route files, page components, and form definitions
3. **User walks through the flow verbally** — Accept but flag that recommendations will be more accurate with actual screens
4. **Use browser tool on live URL** — Walk through the flow step by step

If the flow is partially provided (only some screens), audit what's available and note which steps need investigation.

Document every screen/step in the flow:

```
Flow: [Signup / Onboarding / Upgrade / Checkout]

Step 1: [Page/Screen name]
- URL/Route: [path]
- Fields/Actions: [what user must do]
- Copy: [headline, body, CTA]
- Friction points: [identified issues]

Step 2: [Next screen]
...

Total steps: [N]
Total required fields: [N]
Total decisions: [N]
Estimated completion time: [X minutes]
```

### Step 2: Identify Drop-Off Points

For each step, assess drop-off risk:

| Risk Factor | Score 1-5 | Notes |
|------------|-----------|-------|
| Too many fields | | More than 3 per step = high risk |
| Unclear value | | User doesn't know why this step matters |
| Unexpected ask | | Requesting info that feels premature |
| No progress signal | | User doesn't know how far along they are |
| Decision fatigue | | Too many choices without guidance |
| Trust gap | | Asking for sensitive info without context |
| Technical friction | | Slow load, validation errors, mobile issues |

### Step 3: Apply Friction Reduction

For each step, apply these principles:

#### Progressive Disclosure
- Ask for minimum info at each step
- Defer optional fields to later (post-signup settings)
- Start with the easiest, most natural question
- Example: Email only -> Name -> Company -> Role (not all at once)

#### Single-Field Starts
- First interaction should be ONE field or ONE click
- "Enter your email to get started" > 5-field signup form
- Google/GitHub OAuth as primary option, email form as secondary

#### Smart Defaults
- Pre-select the most common option
- Use detection (timezone, language, company size from email domain)
- Show recommended plan with visual emphasis

#### Motivation Maintenance
- Show progress (Step 2 of 4)
- Remind of value at each step ("You're 1 step away from [outcome]")
- Use micro-commitments (each step delivers a small win)
- Show social proof inline ("12,000 teams completed this step today")

#### Social Proof Injection Points
- Before payment: "Join [X] companies already using [Product]"
- During onboarding: "[Role] at [Company] set this up in 3 minutes"
- At upgrade prompt: "[X]% of free users upgrade within [Y] days"

#### Urgency Without Sleaze
- Real deadlines: "Trial ends in 7 days" (if true)
- Opportunity cost: "Teams using [feature] save [X] hours/week"
- Progress anchoring: "You've already set up [X] — unlock [Y] to get full value"
- Never: fake countdown timers, "only 2 left", manufactured scarcity

### Step 4: Redesign Each Step

For every step in the flow, output:

```markdown
### Step [N]: [Name]

**Current State:**
- Headline: "[current]"
- Fields: [list]
- CTA: "[current]"
- Issues: [specific problems]

**Redesigned:**
- Headline: "[new — ties to value]"
- Fields: [reduced/reordered list]
- CTA: "[new — action + outcome]"
- Supporting copy: "[anxiety reducer or motivation booster]"
- Social proof: "[inline proof element]"

**Changes Made:**
1. [Specific change + reasoning]
2. [Specific change + reasoning]

**Expected Impact:** [Drop-off reduction estimate]
```

### Step 5: A/B Test Suggestions

For each high-impact change, define a test:

```markdown
## A/B Test: [Test Name]

**Hypothesis:** Changing [element] from [A] to [B] will increase [metric] by [X]% because [reasoning].

**Control:** [Current version]
**Variant:** [New version]
**Primary metric:** [Conversion rate at this step]
**Secondary metric:** [Overall flow completion rate]
**Sample size needed:** [Estimate based on current traffic]
**Duration:** [Minimum 2 weeks or X conversions]
```

## Flow-Specific Patterns

### Signup Flow
- Goal: Minimize time-to-value
- Ideal: 1-2 steps max before product access
- Pattern: Email -> Magic link -> Product (skip password creation)
- Anti-pattern: Email -> Password -> Verify email -> Profile -> Team -> Product

### Onboarding Flow
- Goal: Reach "aha moment" fast
- Ideal: 3-5 steps, each delivering visible value
- Pattern: Welcome -> Import data OR use template -> See first result -> Invite team
- Anti-pattern: Long feature tour -> Settings configuration -> Empty state

### Trial-to-Paid Flow
- Goal: Demonstrate value before asking for money
- Ideal: Usage triggers upgrade prompt, not calendar
- Pattern: Hit feature limit -> See what you'd unlock -> One-click upgrade
- Anti-pattern: Day 13 email -> Pricing page -> Checkout -> Success

### Checkout Flow
- Goal: Reduce payment anxiety
- Ideal: 1-2 steps with full transparency
- Pattern: Plan summary -> Payment (with guarantees visible) -> Confirmation
- Anti-pattern: Plan -> Billing info -> Review -> Confirm -> Upsell -> Success

## Worked Example

**Before:** 8-step signup requiring name, email, password, company, role, team size, use case, phone
**After:** 3-step progressive flow:
1. Email only → instant access to limited features
2. After first value moment → ask name + role (contextualized: 'Help us personalize your experience')
3. After 3 sessions → ask company + team size (gated behind upgrade)

**Expected impact:** 40-60% improvement in signup completion rate. Progressive disclosure works because each ask feels justified by the value already delivered.

## Copy Templates Per Step

### First Touch (Signup)
- "Get started free — no credit card required"
- "Create your [product] in 60 seconds"
- "Join [X] [role]s already using [Product]"

### Mid-Flow (Onboarding Step)
- "Nice — you're [X]% set up"
- "Most [role]s complete this in under 2 minutes"
- "This step unlocks [specific feature/outcome]"

### Commitment Point (Payment/Upgrade)
- "You've already [achievement] — unlock [next level]"
- "Plans start at $[X]/mo. Cancel anytime."
- "[X]-day money-back guarantee. No questions asked."

### Completion
- "You're all set. Here's what to do first:"
- "[Product] is ready. Your first [outcome] is [X] away."

See `references/flow-benchmarks.md` for completion rate benchmarks by flow type, step-by-step drop-off patterns, mobile-specific data, and A/B test priorities. Use these to ground recommendations in real numbers.

## Output

Each flow audit produces:
- Visual flow map (current state with step count, fields, decisions)
- Drop-off risk assessment per step
- Redesigned copy and UX for each step
- Prioritized A/B test suggestions
- Before/after comparison of total flow friction score
- Implementation checklist ordered by impact

## Anti-Patterns

- Don't remove security steps (2FA, email verification) — flag them as necessary friction and suggest making them smoother, not removing them
- Don't skip legally required fields (KYC, age verification, GDPR consent) — these stay; optimize their placement and copy instead
- Don't simplify past compliance requirements — if a step exists for legal reasons, note it and move on
- Don't suggest removing steps without understanding the business logic behind them — ask first
- Don't use fake urgency (countdown timers, "only 2 left") — the "Urgency Without Sleaze" principles apply
- Don't optimize for signup completion at the expense of user quality — vanity signups that never activate are worse than fewer, engaged signups

## Edge Cases

- **Partial flow information:** Audit available steps, clearly flag gaps, and ask the user for the missing screens before finalizing recommendations.
- **Mobile vs. desktop divergence:** If the flow differs by platform, audit both. Mobile-specific issues: tap targets, keyboard types for input fields, thumb-zone CTA placement.
- **Legally required steps:** Mark as "required — optimize, don't remove." Focus copy and UX improvements within the constraint.
- **Enterprise/B2B flows:** Longer flows are acceptable when the buyer expects a consultative process. Don't force a consumer-style 2-step signup on an enterprise product.

## Quality Checks

- [ ] Total steps reduced or justified
- [ ] Every field has a clear reason to exist at that step
- [ ] Progress indicator present throughout
- [ ] Value reminder at each step
- [ ] Social proof placed at high-anxiety moments
- [ ] CTA copy is action + outcome, not generic
- [ ] Mobile experience considered for every step
- [ ] Error states are helpful, not punishing
- [ ] Security and compliance steps preserved (not removed)
- [ ] Copy rewrites match brand voice (if voice-profile.md exists)
