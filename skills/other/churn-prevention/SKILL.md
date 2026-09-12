---
name: churn-prevention
description: |
  Designs cancel flow UX, dunning email sequences, win-back campaigns, and retention triggers. Covers the full churn prevention lifecycle from early warning signals to 90-day win-back. Use when someone mentions 'churn', 'retention', 'cancel flow', 'dunning', 'win-back', 'users leaving', 'reducing churn', 'keep users', 'customers canceling', 'payment failed', 'failed payments', 'losing subscribers', 'customer retention', or wants to prevent customers from leaving. Even if they just say 'people keep canceling' or 'how do I keep users' — this is the skill. Handles both voluntary churn (unhappy users) and involuntary churn (failed payments). Use this whenever subscription retention is the goal.
allowed-tools: []
---

# Churn Prevention

## Purpose

Reduce churn across three stages: before they want to leave (health scoring + proactive outreach), while they're leaving (cancel flow + save offers), and after they've left (win-back campaigns). Plus dunning sequences for involuntary churn from failed payments.

## Reads

- `brand/audience.md` — Personas, pain points, what they value most
- `brand/positioning.md` — Value props for reinforcement in save offers and win-back copy
- `brand/voice-profile.md` — Brand voice for all cancel flow and email copy

## Brand Integration

- **audience.md** — Churn signals vary by persona. Power users churn from missing features; casual users churn from confusion. Tailor intervention messaging to the persona's primary motivation.
- **positioning.md** — Save offers and win-back copy should reinforce the brand's core value proposition, not just offer discounts. Remind users of the specific value they're losing.
- **voice-profile.md** — Cancel flow copy must match brand voice. A playful brand says 'We'll miss you! Here's what you'll lose...' A professional brand says 'Before you go, here's a summary of your account value.' Win-back emails must sound like the brand, not like a desperate ex.

## Workflow

### Step 1: Analyze Churn Triggers

Identify and categorize churn drivers:

**Voluntary Churn (they chose to leave):**

| Trigger | Signal | Intervention Window |
|---------|--------|-------------------|
| Not using core feature | <2 logins/week for 2 weeks | Early — usage prompt |
| Price sensitivity | Viewed pricing page after billing | Pre-renewal — value reinforcement |
| Missing feature | Feature request + competitor mention | Medium — roadmap update |
| Poor onboarding | Never completed setup | Immediate — guided help |
| Support frustration | Multiple tickets, low CSAT | Immediate — escalation |
| Outgrew the product | Hitting limits frequently | Pre-churn — upgrade path |
| Champion left | Key user deactivated | Immediate — new champion onboarding |

**Involuntary Churn (payment failed):**

| Trigger | Signal | Intervention |
|---------|--------|-------------|
| Card expired | Payment decline code | Dunning sequence |
| Insufficient funds | Soft decline | Retry schedule |
| Card replaced | Hard decline | Update payment prompt |
| Bank block | Fraud decline | Direct outreach |

### Step 2: Design Health Score

Define a customer health score (0-100) based on:

```
Health Score Components:
- Usage frequency (0-25): Logins, feature usage, API calls
- Feature adoption (0-25): % of key features used
- Engagement depth (0-20): Session duration, actions per session
- Support sentiment (0-15): Ticket volume (inverse), CSAT scores
- Account growth (0-15): Seats added, plan upgrades, expansion
```

Health score thresholds:
- **80-100:** Healthy — nurture and expand
- **60-79:** Monitor — proactive check-in
- **40-59:** At risk — intervention needed
- **0-39:** Critical — immediate outreach

### Step 3: Design Cancel Flow

The cancel flow is not a wall — it's a conversation. Goal: understand why and offer a genuine solution.

```
Screen 1: "Before you go..."
|- "What's the main reason you're canceling?"
|   |- Too expensive -> Screen 2A
|   |- Missing features I need -> Screen 2B
|   |- Not using it enough -> Screen 2C
|   |- Switching to another tool -> Screen 2D
|   |- Just need a break -> Screen 2E
|   |- Other -> Screen 2F

Screen 2A (Too expensive):
|- Show usage stats: "You've [achievement] with [Product] this month"
|- Offer: Downgrade to lower plan / Annual discount / Pause billing
|- CTA: "Switch to [cheaper plan] — keep [key features]"
|- Skip: "No thanks, continue canceling"

Screen 2B (Missing features):
|- "Which features would keep you?"
|- Show roadmap items if relevant: "[Feature] ships in [timeframe]"
|- Offer: "We'll notify you when [feature] launches"
|- Skip: "Continue canceling"

Screen 2C (Not using it enough):
|- Show quick wins: "Here are 3 things you haven't tried yet"
|- Offer: Pause for 1-3 months instead of canceling
|- Offer: Free onboarding call
|- Skip: "Continue canceling"

Screen 2D (Switching to competitor):
|- "Which tool are you switching to?" (optional)
|- Show comparison: "Here's how [Product] compares on [key features]"
|- Offer: Match competitor pricing / free migration assistance
|- Skip: "Continue canceling"

Screen 2E (Need a break):
|- "We get it. Pause your account instead?"
|- Options: Pause 1 month / 2 months / 3 months
|- "Your data and settings stay exactly as they are"
|- Skip: "Cancel instead"

Screen 2F (Other):
|- Open text feedback
|- "Thanks for sharing. Is there anything we can do?"
|- Skip: "Continue canceling"

Screen 3 (Final confirmation):
|- Summary of what they'll lose (specific to their usage)
|- "Your [X] projects and [Y] data will be deleted after 30 days"
|- Final CTA: "Keep my account" (primary) / "Cancel" (secondary, muted)
|- Post-cancel: "Account canceled. You have access until [date]."
```

### Step 4: Build Dunning Sequence

For involuntary churn (failed payments):

**Day 0 — Payment Failed (Immediate)**
```
Subject: Action needed — your payment didn't go through

Your latest payment for [Product] didn't process.
This usually happens when a card expires or has insufficient funds.

[Update Payment Method] <- primary CTA

Your account is still active. We'll retry in 3 days.
```

**Day 3 — First Retry Failed**
```
Subject: Your [Product] payment still needs attention

We tried charging your card again but it didn't work.

Quick fixes:
- Update your card: [link]
- Try a different payment method: [link]

Your account stays active for now, but features will be
limited on [date + 7 days] if we can't process payment.
```

**Day 7 — Warning**
```
Subject: Your [Product] account will be limited tomorrow

We haven't been able to process your payment.

Tomorrow your account will switch to limited mode:
- [Feature 1] will be paused
- [Feature 2] will be read-only
- Your data is safe — nothing is deleted

Takes 30 seconds to fix: [Update Payment]
```

**Day 10 — Last Chance**
```
Subject: Last call — update your payment to keep [Product]

Your account is now in limited mode.

You've built [specific: X projects / Y workflows / Z data points]
in [Product]. Update your payment to pick up where you left off.

[Reactivate Now]

If we don't hear from you by [date + 14], your account
will be suspended. Your data is preserved for 60 days.
```

**Day 14 — Account Suspended**
```
Subject: Your [Product] account has been suspended

Your account is suspended due to non-payment.
Your data is safe and preserved for 60 days.

Ready to come back? [Reactivate — takes 30 seconds]

If you meant to cancel, no action needed.
We'll delete your data after [date + 60] for privacy.
```

### Step 5: Create Win-Back Campaign

For users who completed cancellation:

**Day 7 Post-Cancel — Soft Check-In**
```
Subject: How's it going without [Product]?

No pitch — just curious how things are going.

If you switched to something else, we'd genuinely love
to know what they do better. Reply to this email anytime.

— [Founder name]
```

**Day 30 Post-Cancel — Value Reminder**
```
Subject: Here's what shipped since you left

A few things we've built since you canceled:
- [Feature 1]: [one-line benefit]
- [Feature 2]: [one-line benefit]
- [Improvement]: [one-line benefit]

[See what's new] — your data is still here if you want to come back.
```

**Day 60 Post-Cancel — Win-Back Offer**
```
Subject: Come back to [Product] — [X]% off for 3 months

We'd love to have you back.

Here's a [X]% discount for your first 3 months back.
Your previous [projects/data/settings] are still saved.

[Reactivate with [X]% off]

Offer expires [date + 14 days].
```

**Day 90 Post-Cancel — Final Reach**
```
Subject: Your [Product] data will be deleted on [date]

Per our privacy policy, we delete account data 90 days
after cancellation.

Want to keep your data? [Reactivate] or [Download your data]

After [date], it's permanently removed.
```

## Retention Metric Frameworks

Track these to measure churn prevention effectiveness:

| Metric | Formula | Target |
|--------|---------|--------|
| Gross churn rate | Lost MRR / Starting MRR | <5% monthly |
| Net churn rate | (Lost MRR - Expansion MRR) / Starting MRR | <0% (net negative) |
| Save rate | Saved cancellations / Total cancel attempts | 15-30% |
| Dunning recovery rate | Recovered payments / Failed payments | 50-70% |
| Win-back rate | Reactivated / Total churned | 5-15% |
| Time to churn | Days from first risk signal to cancellation | Track trend |

## Output

Each churn prevention build produces:
- Health score model with component weights
- Cancel flow wireframe with copy for every screen and branch
- Dunning email sequence (5 emails with timing)
- Win-back campaign (4 emails with timing)
- Retention metrics dashboard spec
- Proactive intervention playbook per risk signal

## Anti-Patterns

- Never hide the cancel button or make it hard to find — this is a dark pattern and may violate FTC rules
- Never guilt-trip users ("You'll lose EVERYTHING!") — state facts about what changes, not emotional manipulation
- Never use threatening language in dunning emails ("Your account will be TERMINATED") — keep the tone helpful
- Never offer discounts to every canceller — this trains users to cancel for discounts; segment by reason and value
- Never skip the cancel confirmation — users must see what they'll lose and confirm intentionally
- Never send win-back emails more than 4 times in 90 days — respect the user's decision

## Edge Cases

- **Freemium products:** No payment to fail, so dunning doesn't apply. Focus on voluntary churn: cancel flow becomes "downgrade to free" flow. Lead with what they keep on free tier.
- **Annual billing:** Cancel flow should show prorated refund options. Longer save window since they've already paid. Route to customer success more aggressively (higher LTV at stake).
- **Regulated industries:** Healthcare and finance may have specific data retention and notification requirements. Flag for legal review before implementing data deletion timelines.
- **Team/enterprise accounts:** Show team impact ("Your 8 team members will lose access"). Require admin role to cancel. Route high-MRR accounts to customer success.

See `references/cancel-flow-patterns.md` for business-type segmentation and compliance details. See `references/dunning-playbook.md` for provider-specific setup and smart retry strategies.

## Quality Checks

- [ ] Cancel flow offers genuine alternatives, not guilt trips
- [ ] Dunning emails are helpful, not threatening
- [ ] Win-back offers have real value, not desperation discounts
- [ ] Health score covers usage, engagement, sentiment, and growth
- [ ] All emails have clear single CTA
- [ ] Data deletion timeline is clearly communicated
- [ ] Pause option available as cancel alternative
- [ ] Cancel path is always completable — no dead ends or hidden buttons
- [ ] Copy matches brand voice (if voice-profile.md exists)
- [ ] Compliance considerations noted (FTC click-to-cancel, GDPR data retention)
