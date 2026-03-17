---
name: marketing-email-automation
description: Email marketing automation for HubSpot/Klaviyo/Mailchimp (and similar ESPs): design trigger-based lifecycle workflows (welcome, onboarding, nurture, win-back, cart abandonment), define segmentation + suppression/frequency policies, troubleshoot deliverability (SPF/DKIM/DMARC, one-click unsubscribe, list hygiene), and measure incrementality/ROI (holdouts, RPE, retention economics).
---

# EMAIL AUTOMATION — WORKFLOW OS (OPERATIONAL)

Built as a **no-fluff execution skill** for designing and operating revenue-safe, deliverability-safe email automation across B2B and B2C.

**Structure**: Core workflows and segmentation in SKILL.md. Platform setup in `references/`. Revenue economics in `references/email-economics.md`. Templates in `assets/`.

**Scope note**: For outbound/cold email, see [marketing-leads-generation](../marketing-leads-generation/SKILL.md). For email HTML/CSS implementation, use a coding-focused workflow (this skill is strategy + operations).

---

## Modern Best Practices (January 2026)

Operational reality in 2026:
- Authentication and alignment are enforced (SPF/DKIM/DMARC).
- One-click unsubscribe is required for bulk sending.
- Inbox placement is driven by multi-signal engagement and complaint rates.
- Inactive recipients degrade reputation; enforce suppression/sunset policies.
- Open rates are unreliable due to privacy features (e.g., Apple MPP); measure downstream actions.
- AI-powered personalization is common; ship with guardrails and measure incrementality.
- Interactive email is possible (e.g., AMP for Email in Gmail), but client support is limited; treat it as progressive enhancement.
- EU Accessibility Act (EAA) effective June 2025; WCAG 2.2 AA is the standard.

References:
- Sources: `data/sources.json`
- Deliverability checklist: `references/deliverability.md`
- Accessibility requirements: `references/accessibility.md`

---

## Expert: Automation vs Campaigns (Quick Calibration)

Use this to avoid "scheduled campaigns in disguise."

- **Email campaigns**: One-to-many broadcasts optimized for short-lived goals (announcement, promotion).
- **Email automation**: Trigger-based workflows optimized for reliability, restraint, and state transitions.
- **Lifecycle messaging**: The set of automations that move users through product and revenue states (activation → value → expansion → renewal) with consistent suppression and stop rules.
- **Revenue-driven communication system**: Cross-functional control system where email is one actuator among others (product UX, sales, support, paid) measured for incrementality, not attribution comfort.

Organizational failure mode when automation is treated as scheduled campaigns:
- Teams optimize local email metrics while silently degrading global outcomes (deliverability, qualified pipeline, retention, margin) because messaging is decoupled from real user state.

---

## Core: Lifecycle Architecture (Behavior, Not CRM Defaults)

### Define stages by user-state constraints

Lifecycle stages are not CRM labels. A lifecycle stage is a set of constraints that implies:
- What message can help right now
- What message will be noise or cause harm

Define stages by:
- **Intent** (is the user trying to solve the problem now?)
- **Ability** (do they have access, setup, permissions, budget?)
- **Value realization** (have they experienced the core value loop?)
- **Risk** (churn risk, buyer risk, compliance risk)
- **Route** (self-serve vs sales-assisted vs partner)

### What moves users between stages

Stage transitions should be driven by observable behavior and system events (product, billing, support, sales), not time.

Examples (event-level, platform-agnostic):
- **Activation**: first meaningful action completed (not "account created")
- **Value**: repeated value loop within a window (not "opened email 3 times")
- **Expansion readiness**: feature ceiling hit, invites attempted, usage saturation, admin intent signals
- **Churn risk**: value loop stops, negative support signals, failed payments, downgrade intent

Strategically wrong signal that looks correct:
- Using email engagement (opens/clicks) as a proxy for lifecycle movement; it confuses attention with progress.

---

## Core: Workflow Design (Expert Boundaries)

Branch only when the best next action materially changes due to:
- Different constraints (setup/permissions/budget)
- Different route (sales-assisted vs self-serve)
- Different risk profile (compliance, churn, payment failure)
- Different intent (decision support vs execution support)

Collapse logic when differences are cosmetic and can be handled by:
- Segmented entry rules (separate enrollment) instead of deep branching
- Shared core path + modular blocks (same workflow, different payload)
- Stop rules (exit on success) rather than "if/else forever"

Automation complexity is harming performance when:
- You cannot explain "why did this user get this message" without manual platform tracing
- Users qualify for multiple flows and experience frequency spikes
- Branches rely on stale or inconsistently populated fields
- Too many simultaneous changes prevent causal learning

Early warning sign of unmaintainable automation:
- The team cannot answer "who is in this flow and why" without opening the ESP and manually stepping through conditions.

---

## Core: Platform Literacy (Non-Tool-Centric)

Platform-agnostic decisions (must be stable even if you switch tools):
- Lifecycle stage model and transitions
- Event taxonomy and identity rules (user vs account vs contact; merge/split)
- Consent, suppression, and frequency policies (including global caps)
- Measurement strategy (incrementality, holdouts, decision criteria)
- Routing rules between product, sales, support, and email

Legitimately platform-dependent decisions:
- Data model constraints (profile vs event tables, custom objects)
- Segmentation expressiveness (real-time vs batch; lookback windows)
- Identity resolution behavior (dedupe rules, stitching)
- Deliverability tooling availability (sending pools, domain controls)
- Workflow evaluation semantics (how often conditions re-evaluate)

Common mistake from over-trusting platform "best practices":
- Treating default attribution windows and engagement filters as if they represent causality.

---

## Core: Automation Archetypes (What They Solve)

| Workflow Type | Trigger | Purpose | Timeline |
|---------------|---------|---------|----------|
| **New subscriber / opt-in** | Consent captured | Set expectations, route to intent path | Day 0-7 |
| **New customer / start** | First purchase / start | Drive first value loop | Day 0-30 |
| **Decision support** | Intent signal | Reduce decision risk, progress to commitment | Weeks 1-8 |
| **Abandoned Cart** | Cart created, no purchase | Recover revenue | Hours 1-72 |
| **Re-engagement** | Inactive subscriber | Win back or clean list | Day 30-90 |
| **Upsell/Cross-sell** | Purchase complete | Increase LTV | Day 7-30 post-purchase |
| **Renewal/Retention** | Subscription nearing end | Prevent churn | Day -30 to -1 |

---

## Core: Workflow Design Framework

```text
WORKFLOW: [Name]
TRIGGER: [Event that starts flow]
GOAL: [Primary conversion action]
DURATION: [Total time span]

ENTRY → STEP 1 → WAIT → BRANCH (state A/state B) → STEP 2 → ... → EXIT

Exit when: Goal met | Unsubscribe | Time limit reached
```

See [assets/workflow-blueprint.md](assets/workflow-blueprint.md) for full template.

---

## Core: Nurture Sequences (Reality Check)

What nurture is actually optimizing for:
- Reduce time-to-value and time-to-commitment by removing uncertainty
- Increase decision confidence (not "engagement") through clarity and risk reduction
- Detect route: self-serve users progress; sales-assisted users surface intent and constraints

Why most nurture fails even with good content:
- Wrong stage model: messages do not match the user's constraint (they cannot act yet, or already acted)
- No stop rules: users keep receiving messages after conversion, churn, or route change
- No cross-channel routing: email tries to replace product UX, sales, or support, so it becomes noise
- Optimization for clicks: high click-through can be "confusion," not progress

How nurture changes once product or sales signals exist:
- Shift from generic persuasion to contextual assistance (unblock setup, remove friction, coordinate handoffs)
- Use product and sales events as primary triggers; email becomes a reinforcement and routing layer
- Segment by next constraint (permissions, onboarding step, stakeholder, pricing fit), not by persona labels

Optional scaffolds (if you need examples, not copy guidance):
- [assets/welcome-sequence.md](assets/welcome-sequence.md)
- [assets/nurture-sequence.md](assets/nurture-sequence.md)
- [assets/cart-abandonment.md](assets/cart-abandonment.md)

---

## Core: Segmentation Framework

### Behavioral Segments

| Segment | Definition | Use For |
|---------|------------|---------|
| **Engaged** | Clicked (or took downstream action) in last 30 days | Primary campaigns |
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

### Zero-Party Data Collection

Zero-party data = information users explicitly and voluntarily provide (preferences, intentions, feedback). Unlike behavioral data, this comes directly from the user's stated intent.

**Why it matters (2026)**:

- Third-party cookies deprecated; first-party and zero-party data are now primary
- 48% of consumers prefer brands that collect data transparently
- 93% of marketers view first-party data as critical for future-proofing

**Collection methods**:

| Method | Example | Best For |
| ------ | ------- | -------- |
| **Preference centers** | Content frequency, topic interests, channel preferences | List health, relevance |
| **Progressive profiling** | Ask 1-2 questions per touchpoint over time | Low friction, high completion |
| **Surveys/quizzes** | Gamified "find your style" or product match | Engagement + data capture |
| **Onboarding questions** | Role, company size, goals during signup | B2B segmentation |
| **Post-purchase feedback** | "How did you hear about us?" | Attribution clarity |

**Implementation principles**:

- Clear value exchange: explain why you're asking and what they get
- Progressive, not invasive: 1-2 questions per interaction, not 10-field forms
- Respect stated preferences: if they say "weekly," don't send daily
- Store with consent timestamp: GDPR/CCPA requires audit trail

**Dynamic content from zero-party data**:

- Product recommendations based on stated preferences (not just browsing)
- Content blocks that change based on declared interests
- Send frequency that respects explicit preferences
- Lifecycle stage based on stated goals, not inferred behavior

---

## Core: Message Design Principles (Non-Copy)

- Minimize mismatch: map each message to one user constraint and one next action
- Prefer stop rules over reminders: exit on success, suppress on route change
- Use frequency caps and suppression as first-class design surfaces, not afterthoughts
- Treat incentives as a last resort (they can train discounting and attract low-LTV behavior)
- Optimize for downstream outcomes (activation, retention, qualified pipeline), not surface engagement

---

## Deliverability as a System (Not a Checklist)

Deliverability is three coupled systems:
- **Technical system**: authentication (SPF/DKIM/DMARC), alignment, headers, infrastructure, bounces
- **Behavioral system**: whether recipients consistently signal "this is wanted" (read, reply, save, move) and avoid "this is spam"
- **Reputation system**: ISPs infer your sender quality from aggregate behavior, consistency, and list hygiene over time

One action that improves short-term performance but harms long-term deliverability:
- Increasing send volume by re-mailing unengaged users to "recover revenue" often creates a delayed reputation crash (complaints up, inbox placement down, future revenue down).

### AI-Powered Email Automation (2026)

AI capabilities are mainstream. Treat them as accelerators, not substitutes for measurement, consent, and deliverability hygiene.

**Production-ready AI capabilities**:

| Capability | What It Does | When to Use |
| ---------- | ------------ | ----------- |
| **Send time optimization** | Predicts best send time per recipient | High-volume campaigns, engagement optimization |
| **Subject line generation** | AI-generated variants for testing | A/B testing, creative scaling |
| **Content personalization** | Dynamic blocks based on behavior + preferences | Nurture sequences, product recommendations |
| **Predictive segmentation** | Identifies churn risk, purchase likelihood | Retention, upsell targeting |
| **Copy generation** | Full email drafts from prompts | Campaign scaling, first drafts |

**Guardrails (non-negotiable)**:

- AI suggestions must pass deliverability review (no spam triggers, no misleading claims)
- Human approval for anything customer-facing until confidence is established
- A/B test AI vs human copy; measure downstream outcomes, not just opens
- Stop rules: if AI-generated content underperforms, revert to human baseline

**Autonomous campaigns (emerging)**:

- Real-time systems can adapt timing, offer, and content based on behavior and context.
- Use only when measurement infrastructure is mature (incrementality, holdouts) and governance is explicit.

**Warning**: AI can optimize for surface metrics (opens, clicks) while degrading system outcomes (deliverability, retention, margin). Always validate with downstream outcomes.

AVOID **Over-automation without controls**: Complex flows without monitoring and suppression eventually damage reputation. Review automation performance monthly and retire stale logic.

---

## Core: Deliverability Controls (Operational)

Use `references/deliverability.md` for the full compliance checklist (including BIMI and enforcement status). Use `assets/email-audit.md` for audits.

---

## Revenue Attribution (Hard Part)

Why last-touch attribution fails for automation:
- Automation participates across a long decision journey; last-touch over-credits the final nudge and under-credits earlier state changes.
- It rewards late-stage "harvesting intent" patterns that may not be incremental.
- It breaks when routes mix (product-led + sales-led) and when offline touches exist.

How experts estimate email contribution without overclaiming:
- Treat attribution dashboards as accounting, not truth.
- Prefer incrementality: holdouts, randomized suppression, geo splits, or step-wedge rollouts.
- Evaluate system outcomes: activation rate, time-to-value, retention cohorts, pipeline velocity, margin protection.

Attribution signal to trust more than dashboards:
- Lift measured via a properly designed holdout/suppression test on the automation (conversion/retention difference between eligible users who were and were not emailed).

---

## Economics & Retention (Use Subfiles)

Use `references/email-economics.md` for attribution models, RPE framework, segment economics, churn reduction ROI, and channel mix decisions.

How automation contributes:
- **Retention**: reinforces the value loop, removes friction, and routes users to help before they stall
- **Expansion**: drives feature adoption and account-level enablement when usage ceilings or admin intent appear
- **Churn reduction**: detects risk states (usage drop, failed payments, negative support signals) and triggers corrective paths with tight suppression

---

## Metrics & KPIs

Use metrics to detect system health, not to "win the dashboard":
- Open rate: trend only (MPP).
- Click/action rate: engagement signal; prefer downstream action.
- Revenue per email: accounting signal; validate with incrementality.
- Conversion and retention cohorts: primary outcomes.

Retention-related email metric that can look positive while the business degrades:
- Rising "re-engagement" click rate driven by incentives while retention cohorts and gross margin deteriorate (you are buying activity, not improving value).

See `references/email-economics.md` for definitions and calculations.

## Platform Setup Guides

- [references/hubspot-setup.md](references/hubspot-setup.md)
- [references/klaviyo-setup.md](references/klaviyo-setup.md)
- [references/mailchimp-setup.md](references/mailchimp-setup.md)
- [references/accessibility.md](references/accessibility.md) — WCAG 2.2, EAA compliance, dark mode

---

## Templates

| Template | Purpose |
|----------|---------|
| [workflow-blueprint.md](assets/workflow-blueprint.md) | Design any workflow |
| [welcome-sequence.md](assets/welcome-sequence.md) | New subscriber welcome |
| [nurture-sequence.md](assets/nurture-sequence.md) | Lead nurturing |
| [cart-abandonment.md](assets/cart-abandonment.md) | E-commerce recovery |
| [email-audit.md](assets/email-audit.md) | Health check template |
| [email-roi-calculator.md](assets/email-roi-calculator.md) | ROI calculation |

---

## Interactive Email (AMP for Email)

AMP for Email enables in-email actions without leaving the inbox. Users can complete forms, browse carousels, submit reviews, and update preferences directly in the message.

**Adoption status (2026)**:

- Support is limited and uneven across clients; treat AMP as progressive enhancement, not a default UX.
- You must ship a full HTML fallback that preserves intent (not just a broken placeholder).

**Interactive elements and use cases**:

| Element | Use Case |
| ------- | -------- |
| **Forms** | Surveys, reviews, preference updates |
| **Carousels** | Product browsing, feature highlights |
| **Accordions** | FAQ, detailed specs, terms |
| **Live data** | Inventory counts, pricing, appointment slots |
| **Checkout** | One-click purchase, cart updates |

**Implementation requirements**:

- Sender must be registered with Google (AMP for Email sender registration)
- DKIM/SPF/DMARC must pass
- AMP MIME part required alongside HTML fallback
- Content must be dynamic (server-rendered, not static)

**When to use AMP**:

- High-intent moments: abandoned cart, booking confirmation, review request
- Data collection: NPS surveys, preference updates, feedback forms
- Real-time content: inventory, pricing, appointment availability

**When NOT to use AMP**:

- Simple announcements (overhead not justified)
- Audiences primarily on Apple Mail (no AMP support)
- When HTML fallback would be significantly different experience

**Fallback requirement**: Always provide HTML fallback. AMP is progressive enhancement, not replacement.

**Testing**: Use Litmus, Email on Acid, or Gmail's AMP Playground to validate rendering across clients.

---

## CRO vs Email Automation Boundary

Email automation supports CRO when it:
- Routes the right users back into the funnel at the right stage (intent match)
- Reduces friction and uncertainty around the next commitment (activation, checkout, demo)

Email automation conflicts with CRO when it:
- Trains the market to wait for discounts or bypasses qualification gates
- Drives low-intent traffic back to conversion pages (inflates visits, lowers close quality)

Optimization mistake that improves email metrics but reduces funnel efficiency:
- Maximizing click-through by broadening eligibility and adding incentives, which increases page traffic while lowering qualified conversion rate and harming deliverability.

---

## Red Flags (Subtle, Practitioner-Level)

Three statements that signal non-expert operation:
1. "We just need more emails in the flow to increase conversions."
2. "If the email gets clicks, the automation is working."
3. "Our platform attribution shows email drove X%, so we should scale volume."

---

## Decision Tree (Email Triage)

```text
Complaints rising (or inbox placement dropping)?
├─ Suppress unengaged; tighten eligibility
├─ Reduce frequency; add global caps
└─ Audit list sources + consent + auth alignment

Bounces rising?
├─ Remove hard bounces immediately
├─ Fix list acquisition hygiene (double opt-in where appropriate)
└─ Verify infrastructure and authentication

Clicks/actions down but deliverability stable?
├─ Stage mismatch: rebuild lifecycle entry/exit rules
├─ Route mismatch: coordinate with product/sales/support signals
└─ Validate impact with holdouts; do not "add more emails" first

Revenue up but retention/margin down?
└─ Incentive training or low-LTV acquisition: tighten segmentation and protect pricing integrity
```

---

## Anti-Patterns

| Anti-Pattern | Instead |
|--------------|---------|
| Batch-and-blast | Segment and trigger |
| No segmentation | Behavioral segments |
| Multiple competing goals | One primary outcome per message |
| Ignoring mobile constraints | Mobile constraints first (tap targets, load, readability) |
| Buying lists | Build organically |
| Set-and-forget automations | Monthly performance reviews |
| Relying on open rates | Use click rate, conversions, revenue |

---

## International Markets

This skill uses US/UK market defaults. For international email marketing:

| Need | See Skill |
|------|-----------|
| Regional compliance (CASL, LGPD, PIPL) | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| Regional send time optimization | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| Cultural messaging adaptation | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| Alternative channels (WhatsApp, LINE, WeChat) | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |

**Auto-triggers**: When your query mentions a specific country, region, or compliance framework, both skills load automatically.

---

## Related Skills

- [marketing-geo-localization](../marketing-geo-localization/SKILL.md) — International marketing, regional compliance
- [marketing-leads-generation](../marketing-leads-generation/SKILL.md) — Lead capture
- [marketing-content-strategy](../marketing-content-strategy/SKILL.md) — Content for emails
- [marketing-cro](../marketing-cro/SKILL.md) — Landing page optimization
- [startup-go-to-market](../startup-go-to-market/SKILL.md) — Channel strategy

---

## Usage Notes (Claude)

- Stay operational: return lifecycle stage model, trigger rules, suppression/frequency policy, and workflow diagrams
- For revenue/ROI questions, reference `references/email-economics.md`
- Always include deliverability requirements (authentication, hygiene)
- Do not invent benchmark data; use ranges or state "varies by industry"
