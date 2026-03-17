---
name: prd-v09-gtm-strategy
description: >
  Define go-to-market strategy including launch plan, messaging, channels, and timing during PRD v0.9 Go-to-Market.
  Triggers on requests to plan launch, define GTM strategy, or when user asks "how do we launch?",
  "go-to-market", "launch plan", "marketing strategy", "messaging", "launch channels", "GTM".
  Outputs GTM- entries with launch plan components.
---

# GTM Strategy

Position in workflow: v0.8 Monitoring Setup → **v0.9 GTM Strategy** → v0.9 Launch Metrics

## Purpose

Define how the product reaches its target users—the channels, messaging, timing, and coordination required for a successful launch.

## Core Concept: Launch as Campaign

> A launch is not "making the product available." It is a **coordinated campaign** that creates awareness, drives activation, and captures feedback. Every touchpoint should move users toward value.

## GTM Components

| Component | Purpose | Output |
|-----------|---------|--------|
| **Messaging** | What we say | GTM- (value props, headlines) |
| **Channels** | Where we say it | GTM- (channel strategy) |
| **Timing** | When we launch | GTM- (timeline, phases) |
| **Coordination** | Who does what | GTM- (RACI, tasks) |

## Execution

1. **Review target personas**
   - Pull PER- from v0.4
   - Understand where they spend time
   - Know what messages resonate

2. **Define core messaging**
   - Value proposition (from CFD- value hypotheses)
   - Positioning (from BR- product type)
   - Key differentiators (from v0.2 competitive landscape)

3. **Select launch channels**
   - Match channels to personas
   - Prioritize by reach and conversion potential
   - Consider owned, earned, and paid media

4. **Plan launch timeline**
   - Pre-launch: Build anticipation
   - Launch day: Maximum impact
   - Post-launch: Sustain momentum

5. **Assign ownership**
   - Who creates content?
   - Who monitors channels?
   - Who handles support surge?

6. **Create GTM- entries** with full traceability

## GTM- Output Template

```
GTM-XXX: [GTM Item Title]
Type: [Messaging | Channel | Timeline | Task | Asset]
Owner: [Person or team responsible]
Status: [Planned | In Progress | Ready | Live]

For Messaging Type:
  Audience: [PER-XXX targeted]
  Format: [Headline | Value Prop | Tagline | Elevator Pitch]
  Message: [The actual copy]
  Supporting Evidence: [CFD-XXX value hypothesis it's based on]
  Where Used: [GTM-YYY channels, assets]

For Channel Type:
  Channel: [Specific platform or medium]
  Audience Fit: [Why this channel reaches PER-XXX]
  Strategy: [How we'll use this channel]
  Content Plan: [What content goes here]
  Success Metric: [How we measure effectiveness]
  Linked Assets: [GTM-YYY assets for this channel]

For Timeline Type:
  Phase: [Pre-launch | Launch Day | Week 1 | Month 1]
  Date: [Specific date or relative timing]
  Activities: [What happens in this phase]
  Dependencies: [What must be ready]
  Milestones: [Key checkpoints]

For Task Type:
  Task: [What needs to be done]
  Owner: [Who is responsible]
  Due: [When it's due]
  Dependency: [What it depends on]
  Deliverable: [What's produced]

For Asset Type:
  Asset: [What this is — landing page, email, video]
  Purpose: [What it accomplishes]
  Channel: [GTM-YYY where it's used]
  Copy: [GTM-YYY messaging used]
  Status: [Draft | Review | Approved | Live]

Linked IDs: [PER-XXX, CFD-XXX, KPI-XXX related]
```

**Example GTM- entries:**

```
GTM-001: Primary Value Proposition
Type: Messaging
Owner: Product Marketing
Status: Ready

Audience: PER-001 (Startup Founder)
Format: Value Prop
Message: "Ship faster with AI that understands your codebase.
         Context-aware coding assistance that reduces debugging
         time by 40%."
Supporting Evidence: CFD-010 (time savings validated in interviews)
Where Used: GTM-005 (Landing Page), GTM-010 (Product Hunt)

Linked IDs: PER-001, CFD-010, KPI-001
```

```
GTM-002: Product Hunt Launch
Type: Channel
Owner: Growth Team
Status: Planned

Channel: Product Hunt
Audience Fit: PER-001 (Startup Founder) frequents PH for tools
Strategy:
  - Launch on Tuesday 12:01 AM PT
  - Engage with comments first 24 hours
  - Share maker story
  - Prepare demo video
Content Plan:
  - Tagline: GTM-001 (Primary Value Prop)
  - Maker comment: GTM-003 (Founder Story)
  - Demo video: GTM-006 (Product Demo)
Success Metric: Top 5 product of the day, 500+ upvotes

Linked IDs: PER-001, GTM-001, GTM-003, GTM-006, KPI-005
```

```
GTM-003: Launch Week Timeline
Type: Timeline
Owner: Launch Coordinator
Status: Planned

Phase: Launch Week

Day -7 (Pre-launch):
  - [ ] Email list teaser
  - [ ] Social media hints
  - [ ] Press outreach

Day -1:
  - [ ] Final staging verification
  - [ ] Launch assets approved
  - [ ] Team roles confirmed

Day 0 (Launch):
  - [ ] Product Hunt live at 12:01 AM PT
  - [ ] Social media posts scheduled
  - [ ] Email to waitlist
  - [ ] Monitor and engage

Day 1-3:
  - [ ] Respond to all feedback
  - [ ] Fix any critical issues
  - [ ] Share early wins

Day 4-7:
  - [ ] Publish case study
  - [ ] Analyze metrics
  - [ ] Plan iteration

Dependencies: DEP- release criteria met, MON- monitoring active
Milestones: 1000 signups (Day 3), First paying customer (Day 7)

Linked IDs: DEP-002, MON-005, KPI-001
```

```
GTM-004: Landing Page Hero Section
Type: Asset
Owner: Design + Marketing
Status: In Progress

Asset: Landing page hero section
Purpose: Convert visitors to signups
Channel: GTM-007 (Website), GTM-002 (Product Hunt referrals)
Copy: GTM-001 (Primary Value Prop)
Status: Review

Components:
  - Headline: "Ship faster with AI that understands your codebase"
  - Subhead: "Context-aware coding assistance that reduces
              debugging time by 40%"
  - CTA: "Start Free Trial" → /signup
  - Social proof: "Trusted by 500+ developers"
  - Demo video thumbnail: GTM-006

Linked IDs: GTM-001, GTM-006, SCR-001
```

## Channel Selection Framework

Match channels to product type (from v0.2 BR-):

| Product Type | Primary Channels | Strategy |
|--------------|------------------|----------|
| **Fast Follow** | SEO, Paid, Aggregators | "We're the better [competitor]" |
| **Slice** | Community, Integrations, Partnerships | "Best [thing] for [ecosystem]" |
| **Innovation** | Content, PR, Events | "Here's why this matters" |

## Channel Categories

| Category | Examples | Best For |
|----------|----------|----------|
| **Owned** | Website, Blog, Email, Product | Control message, build audience |
| **Earned** | PR, Reviews, Word-of-mouth | Credibility, reach |
| **Paid** | Ads, Sponsorships, Influencers | Scale, targeting |
| **Community** | Forums, Discord, Twitter | Engagement, feedback |

## Messaging Hierarchy

| Level | Purpose | Example |
|-------|---------|---------|
| **Mission** | Why we exist | "Make developers 10x more productive" |
| **Value Prop** | What we offer | "AI that understands your codebase" |
| **Differentiator** | Why us vs others | "Context-aware, not just autocomplete" |
| **Proof Point** | Why believe us | "40% reduction in debugging time" |
| **CTA** | What to do next | "Start your free trial" |

## Launch Phases

| Phase | Duration | Focus | Success Metric |
|-------|----------|-------|----------------|
| **Teaser** | 2 weeks pre | Build anticipation | Waitlist signups |
| **Launch** | Day 0-3 | Maximum impact | Traffic, signups |
| **Momentum** | Week 1-4 | Sustain interest | Activation, feedback |
| **Steady State** | Month 2+ | Optimize funnel | Conversion, retention |

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Launch and leave** | Big launch day, then silence | Plan 30 days of post-launch activity |
| **Everything everywhere** | All channels, no focus | Pick 2-3 channels, do them well |
| **Features not benefits** | "We have X, Y, Z" | "You can achieve X, Y, Z" |
| **No measurement** | "The launch went well (I think)" | Define KPI- before launch |
| **Ignoring personas** | Generic messaging for everyone | Tailor by PER- |
| **Over-promising** | "Revolutionary AI" without proof | Ground in CFD- evidence |

## Quality Gates

Before proceeding to Launch Metrics:

- [ ] Core messaging defined (GTM- Messaging type)
- [ ] Primary channels selected (GTM- Channel type)
- [ ] Launch timeline created (GTM- Timeline type)
- [ ] All tasks assigned owners (GTM- Task type)
- [ ] Key assets identified (GTM- Asset type)
- [ ] Messaging traces to CFD- evidence
- [ ] Channel selection matches PER- personas

## Downstream Connections

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **Launch Metrics** | GTM- channels inform tracking | GTM-002 (PH) → KPI-005 (PH upvotes) |
| **Feedback Loop Setup** | GTM- channels become feedback sources | GTM-002 comments → CFD-100 |
| **Content Creation** | GTM- messaging guides content | GTM-001 → blog post theme |
| **Sales** | GTM- messaging for outreach | GTM-001 → sales email template |

## Detailed References

- **Messaging framework examples**: See `references/messaging-examples.md`
- **GTM- entry template**: See `assets/gtm-template.md`
- **Channel evaluation guide**: See `references/channel-guide.md`
- **Launch timeline template**: See `references/timeline-template.md`
