---
name: marketing-email-automation
description: Email marketing automation - workflow design, platform setup (HubSpot, Klaviyo, Mailchimp), nurture sequences, lifecycle emails, and deliverability.
---

# EMAIL AUTOMATION — WORKFLOW OS (OPERATIONAL)

Built as a **no-fluff execution skill** for email marketing automation across B2B and B2C.

**Structure**: Core email automation fundamentals first. Platform-specific setup in dedicated sections. AI personalization in clearly labeled "Optional: AI / Automation" sections.

---

## Modern Best Practices (January 2026)

- HubSpot Email: https://knowledge.hubspot.com/email/
- Klaviyo Help: https://help.klaviyo.com/
- Mailchimp Resources: https://mailchimp.com/resources/
- Google Sender Guidelines: https://support.google.com/mail/answer/81126

---

## When to Use This Skill

- **Workflow design**: Trigger-based sequences, nurture flows, lifecycle emails
- **Platform setup**: HubSpot, Klaviyo, Mailchimp, Braze configuration
- **Segmentation**: List management, behavioral segments, RFM models
- **Deliverability**: Authentication, warm-up, reputation management
- **Personalization**: Dynamic content, merge tags, conditional logic

---

## Core: Email Workflow Types

| Workflow Type | Trigger | Purpose | Timeline |
|---------------|---------|---------|----------|
| **Welcome** | New subscriber | Introduce brand, set expectations | Day 0-7 |
| **Onboarding** | New customer | Drive activation, reduce churn | Day 0-30 |
| **Nurture** | Lead capture | Educate, build trust, convert | Weeks 1-8 |
| **Abandoned Cart** | Cart created, no purchase | Recover revenue | Hours 1-72 |
| **Re-engagement** | Inactive subscriber | Win back or clean list | Day 30-90 |
| **Upsell/Cross-sell** | Purchase complete | Increase LTV | Day 7-30 post-purchase |
| **Renewal/Retention** | Subscription nearing end | Prevent churn | Day -30 to -1 |

---

## Core: Workflow Design Framework

### Workflow Blueprint Template

```text
WORKFLOW: [Name]
TRIGGER: [Event that starts flow]
GOAL: [Primary conversion action]
DURATION: [Total time span]

┌─────────────────────────────────────────────────────────────┐
│                      ENTRY CRITERIA                          │
│  Trigger: [Event]                                           │
│  Filters: [Conditions to enter]                             │
│  Exclusions: [Who NOT to include]                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  EMAIL 1: [Name]                                            │
│  Delay: Immediate / [X hours/days]                          │
│  Subject: [Subject line]                                    │
│  Goal: [Micro-conversion]                                   │
│  CTA: [Primary action]                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WAIT: [X days] or UNTIL [condition]                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  BRANCH: IF [condition]                                     │
│  ├─ YES → [Next step for engaged]                          │
│  └─ NO → [Next step for non-engaged]                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  EXIT CRITERIA                                              │
│  Goal met: [Conversion action]                              │
│  Unsubscribe: Remove from flow                              │
│  Time limit: [Max days in flow]                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Core: Standard Workflow Templates

### 1. Welcome Sequence (4 emails, 7 days)

```text
TRIGGER: New subscriber
GOAL: First purchase / demo booking

Email 1 (Immediate): Welcome + Value Prop
├─ Subject: "Welcome to [Brand] - here's what's next"
├─ Content: Brand story, what to expect, quick win
└─ CTA: [Primary action based on business]

WAIT: 2 days

Email 2 (Day 2): Problem Agitation
├─ Subject: "The [problem] most [audience] face"
├─ Content: Pain point, consequences, hint at solution
└─ CTA: Read guide / Watch video

WAIT: 2 days

Email 3 (Day 4): Social Proof
├─ Subject: "How [Customer] achieved [Result]"
├─ Content: Case study, testimonial, results
└─ CTA: See more stories / Book demo

WAIT: 3 days

Email 4 (Day 7): Soft Sell
├─ Subject: "Ready to [achieve outcome]?"
├─ Content: Offer summary, urgency, risk reversal
└─ CTA: Start trial / Book demo / Buy now
```

### 2. Abandoned Cart (3 emails, 72 hours)

```text
TRIGGER: Cart created, no purchase in 1 hour
GOAL: Complete purchase

Email 1 (1 hour): Reminder
├─ Subject: "You left something behind"
├─ Content: Cart contents, product images
└─ CTA: Complete order (direct to cart)

WAIT: 24 hours
IF: Still not purchased

Email 2 (Day 1): Urgency + Support
├─ Subject: "Your cart is waiting (questions?)"
├─ Content: Cart contents, FAQ, support link
└─ CTA: Complete order + Chat with us

WAIT: 48 hours
IF: Still not purchased

Email 3 (Day 3): Incentive (optional)
├─ Subject: "10% off to complete your order"
├─ Content: Discount code, expiration
└─ CTA: Use code [CODE] - Shop now

EXIT: Purchase complete or Day 7
```

### 3. Lead Nurture (6 emails, 4 weeks)

```text
TRIGGER: Lead captured (gated content, webinar, etc.)
GOAL: SQL / Demo booking

Email 1 (Immediate): Deliver value
├─ Subject: "Your [resource] is ready"
├─ Content: Download link, quick intro
└─ CTA: Download now

WAIT: 3 days

Email 2 (Day 3): Educational content
├─ Subject: "3 ways to [solve problem]"
├─ Content: Tips, how-to, best practices
└─ CTA: Read full guide

WAIT: 4 days

Email 3 (Day 7): Case study
├─ Subject: "How [Company] achieved [Result]"
├─ Content: Customer story, metrics
└─ CTA: Read case study

WAIT: 5 days

Email 4 (Day 12): Objection handling
├─ Subject: "Worried about [common objection]?"
├─ Content: Address concerns, proof points
└─ CTA: See how we handle [objection]

WAIT: 5 days

Email 5 (Day 17): Comparison/evaluation
├─ Subject: "How we compare to [alternative]"
├─ Content: Comparison, differentiators
└─ CTA: See comparison

WAIT: 7 days

Email 6 (Day 24): Soft close
├─ Subject: "Ready to talk?"
├─ Content: Recap value, offer conversation
└─ CTA: Book a call

BRANCH after each email:
├─ Engaged (opened/clicked) → Continue sequence
├─ Converted (booked demo) → Exit to sales
└─ Unengaged (no opens 3+ emails) → Move to re-engagement
```

### 4. Onboarding (5 emails, 14 days)

```text
TRIGGER: New customer / trial start
GOAL: Activation (key feature used)

Email 1 (Immediate): Getting started
├─ Subject: "Welcome! Let's get you set up"
├─ Content: Quick start steps, first action
└─ CTA: Complete setup

WAIT: 1 day
IF: Setup not complete

Email 2 (Day 1): Setup reminder
├─ Subject: "Need help getting started?"
├─ Content: Setup guide, support resources
└─ CTA: Complete setup / Chat with us

WAIT: 2 days

Email 3 (Day 3): Key feature intro
├─ Subject: "Unlock [key feature]"
├─ Content: Feature benefit, how-to
└─ CTA: Try [feature] now

WAIT: 4 days

Email 4 (Day 7): Progress check
├─ Subject: "You're making progress!"
├─ Content: What they've done, next steps
└─ CTA: [Next milestone action]

WAIT: 7 days

Email 5 (Day 14): Value realization
├─ Subject: "[Name], here's what you've achieved"
├─ Content: Usage stats, value delivered
└─ CTA: Upgrade / Continue / Share feedback

BRANCH by activation:
├─ Activated → Success path (upsell)
└─ Not activated → Risk path (support outreach)
```

---

## Core: Segmentation Framework

### Behavioral Segments

| Segment | Definition | Use For |
|---------|------------|---------|
| **Engaged** | Opened/clicked in last 30 days | Primary campaigns |
| **Active** | Logged in / used product recently | Onboarding, upsell |
| **At-risk** | No engagement 31-60 days | Re-engagement |
| **Dormant** | No engagement 61-90 days | Win-back |
| **Churned** | No engagement 90+ days | Sunset or remove |

### RFM Segmentation (E-commerce)

| Segment | Recency | Frequency | Monetary | Strategy |
|---------|---------|-----------|----------|----------|
| **Champions** | Recent | Often | High | Reward, refer |
| **Loyal** | Recent | Often | Medium | Upsell |
| **Potential** | Recent | Rare | Low | Nurture |
| **At Risk** | Old | Often | High | Win back |
| **Hibernating** | Old | Rare | Low | Re-engage or remove |

### Lifecycle Segments

| Stage | Definition | Primary Workflow |
|-------|------------|------------------|
| **Subscriber** | Email only | Welcome, nurture |
| **Lead** | Engaged, not converted | Nurture, sales |
| **Trial** | Active trial | Onboarding |
| **Customer** | Paying | Onboarding, upsell |
| **Churned** | Cancelled | Win-back |

---

## Core: Email Best Practices

### Subject Lines

**Do:**
- Keep under 50 characters
- Personalize when relevant (name, company)
- Use numbers and specifics
- Create curiosity or urgency
- A/B test consistently

**Avoid:**
- ALL CAPS
- Excessive punctuation!!!
- Spam trigger words (FREE, ACT NOW)
- Misleading subjects
- Generic subjects ("Newsletter #47")

### Email Copy

**Structure:**
```text
1. Hook (first line): Grab attention, reference pain/benefit
2. Body (2-3 short paragraphs): Value, proof, bridge to CTA
3. CTA (clear, single action): Button or linked text
4. P.S. (optional): Reinforce urgency or secondary offer
```

**Formatting:**
- Short paragraphs (2-3 sentences max)
- Plenty of white space
- Mobile-first design (single column)
- One primary CTA per email
- Plain text alternative

### Timing

| Email Type | Best Days | Best Times |
|------------|-----------|------------|
| B2B | Tue-Thu | 9-11am, 1-3pm |
| B2C | Tue-Thu, Sat | 10am, 8pm |
| Transactional | Immediate | N/A |
| Newsletter | Consistent day | Your data |

---

## Core: Deliverability Checklist

### Authentication (Required)

- [ ] **SPF** configured (RFC 7208)
- [ ] **DKIM** configured (RFC 6376)
- [ ] **DMARC** configured (RFC 7489)
- [ ] Custom sending domain (not @gmail.com)

### List Hygiene

- [ ] Double opt-in enabled (or single with clear consent)
- [ ] Unsubscribe link in every email
- [ ] Hard bounces removed immediately
- [ ] Soft bounces removed after 3 attempts
- [ ] Inactive subscribers suppressed (90 days no engagement)
- [ ] Spam complaints monitored (<0.1% rate)

### Sending Practices

- [ ] Consistent sending frequency
- [ ] Gradual volume increases (warm-up)
- [ ] No purchased lists (ever)
- [ ] Engagement-based sending (engaged first)
- [ ] Sunset policy for unengaged

### Monitoring

| Metric | Target | Action if Below |
|--------|--------|-----------------|
| Open rate | >20% | Check subject lines, sender reputation |
| Click rate | >2% | Check content, CTA, relevance |
| Bounce rate | <2% | Clean list, verify addresses |
| Spam rate | <0.1% | Review content, frequency, consent |
| Unsubscribe | <0.5% | Check frequency, relevance |

---

## Platform Setup Guides

### HubSpot

See [resources/hubspot-setup.md](resources/hubspot-setup.md)

### Klaviyo

See [resources/klaviyo-setup.md](resources/klaviyo-setup.md)

### Mailchimp

See [resources/mailchimp-setup.md](resources/mailchimp-setup.md)

---

## Quick Reference

| Task | Template | Location |
|------|----------|----------|
| Workflow design | Workflow blueprint | `templates/workflow-blueprint.md` |
| Welcome sequence | Welcome flow | `templates/welcome-sequence.md` |
| Nurture sequence | Nurture flow | `templates/nurture-sequence.md` |
| Cart abandonment | Cart recovery | `templates/cart-abandonment.md` |
| Email audit | Health check | `templates/email-audit.md` |

---

## Decision Tree (Email Triage)

```text
Open rates low (<15%)?
├─ Check sender reputation (Google Postmaster, MXToolbox)
├─ Check subject lines (A/B test)
├─ Check send time (test different times)
└─ Check list quality (remove inactive)

Click rates low (<1%)?
├─ Check content relevance (segmentation)
├─ Check CTA clarity (single, prominent)
├─ Check mobile rendering (responsive design)
└─ Check email length (shorter often better)

High unsubscribes (>0.5%)?
├─ Check frequency (too often?)
├─ Check relevance (right content to right segment?)
├─ Check expectations (did they know what they signed up for?)
└─ Add preference center (let them choose frequency/topics)

Deliverability issues?
├─ Check authentication (SPF, DKIM, DMARC)
├─ Check blacklists (MXToolbox)
├─ Check content (spam words, link ratio)
└─ Check sending patterns (consistent volume)
```

---

## Metrics & KPIs

### Primary Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| **Open rate** | Opens / Delivered | >20% |
| **Click rate** | Clicks / Delivered | >2% |
| **Conversion rate** | Conversions / Clicks | Varies |
| **Revenue per email** | Revenue / Emails sent | Track trend |

### Workflow Metrics

| Metric | Definition | Purpose |
|--------|------------|---------|
| **Flow conversion** | Goal completions / Flow entries | Workflow effectiveness |
| **Drop-off rate** | Exits at each step | Find weak points |
| **Time to convert** | Days from entry to goal | Optimize timing |
| **Re-entry rate** | Multiple entries | Check exclusions |

---

## Templates

| Template | Purpose |
|----------|---------|
| [workflow-blueprint.md](templates/workflow-blueprint.md) | Design any workflow |
| [welcome-sequence.md](templates/welcome-sequence.md) | New subscriber welcome |
| [nurture-sequence.md](templates/nurture-sequence.md) | Lead nurturing |
| [cart-abandonment.md](templates/cart-abandonment.md) | E-commerce recovery |
| [email-audit.md](templates/email-audit.md) | Health check template |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Batch-and-blast** | Low relevance, high unsubscribes | Segment and trigger |
| **No segmentation** | One size fits none | Behavioral segments |
| **Too many CTAs** | Decision paralysis | One CTA per email |
| **Ignoring mobile** | 60%+ read on mobile | Mobile-first design |
| **No testing** | Assumptions vs data | A/B test everything |
| **Buying lists** | Spam complaints, reputation damage | Build organically |
| **No sunset policy** | Sending to dead addresses | Remove unengaged |

---

## Optional: AI / Automation

> **Note**: Core email automation fundamentals above work without AI. This section covers optional AI capabilities.

### AI Personalization

| Feature | Use Case | Tools |
|---------|----------|-------|
| **Subject line generation** | A/B test variants | Claude, GPT, platform built-in |
| **Dynamic content** | Personalized blocks | Klaviyo, HubSpot, Braze |
| **Send time optimization** | Per-recipient timing | Seventh Sense, platform AI |
| **Predictive segments** | Churn risk, purchase propensity | Klaviyo, HubSpot predictive |

### AI Best Practices

- Always A/B test AI-generated vs human-written
- Review AI content for brand voice consistency
- Use AI for variants, not strategy
- Monitor performance vs control

---

## Related Skills

- [marketing-leads-generation](../marketing-leads-generation/SKILL.md) — Lead capture and sequences
- [marketing-content-strategy](../marketing-content-strategy/SKILL.md) — Content for emails
- [marketing-cro](../marketing-cro/SKILL.md) — Landing page optimization
- [startup-go-to-market](../startup-go-to-market/SKILL.md) — Channel strategy

---

## Usage Notes (Claude)

- Stay operational: return workflow diagrams, email copy templates, setup steps
- Include timing recommendations and branching logic
- Always include deliverability requirements (authentication, hygiene)
- Reference platform-specific features when applicable
- Do not invent benchmark data; use ranges or state "varies by industry"
