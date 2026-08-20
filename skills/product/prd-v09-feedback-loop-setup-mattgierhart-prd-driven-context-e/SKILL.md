---
name: prd-v09-feedback-loop-setup
description: >
  Establish channels and processes for capturing and processing post-launch feedback during PRD v0.9 Go-to-Market.
  Triggers on requests to set up feedback systems, capture user input, or when user asks "how do we collect feedback?",
  "feedback loop", "user research", "post-launch feedback", "customer feedback", "NPS", "voice of customer".
  Outputs CFD- entries specialized for post-launch feedback capture.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# Feedback Loop Setup

Position in workflow: v0.9 Launch Metrics → **v0.9 Feedback Loop Setup** → v1.0 Market Adoption

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | 1–2 channels (in-app + support); basic triage workflow |
| **standard** | 3–4 channels; full processing workflow + sentiment tracking + SLAs |
| **deep** | All channels + closed-loop tracking + voice-of-customer synthesis + escalation rules |

## Consumes

This skill requires prior work from v0.9 Launch Metrics and v0.1-v0.8:

- **GTM-\* launch channels** (from v0.9 GTM Strategy) — Active launch channels (Product Hunt, email, paid ads, etc.) become feedback sources; GTM- messaging and channels inform where feedback will arrive
- **MON-\* monitoring dashboards and alerts** (from v0.8 Monitoring Setup) — MON- thresholds (latency, error rate, performance) define what qualifies as critical feedback; monitoring alerts can trigger deep-dive user research
- **KPI-\* launch targets and baselines** (from v0.9 Launch Metrics) — KPI- thresholds (Day 1/7/30/90 targets) inform feedback urgency and trigger investigation when below target; baseline performance metrics (p95 latency, error rate, conversion rate) provide context for performance feedback
- **CFD-\* baseline entries** (from v0.1-v0.4) — Baseline customer feedback hypotheses (user pain points, value propositions, competitive alternatives) become validation targets post-launch; feedback loop confirms or contradicts CFD- assumptions
- **PER-\* personas** (from v0.4 Persona Definition) — Persona segments (PER-001 Startup Founder, PER-002 Team Lead) enable feedback categorization by user type and prioritization by persona importance

This skill assumes v0.9 Launch Metrics is live with KPI- thresholds established, GTM- channels are active, and MON- dashboards are displaying baseline metrics.

## Produces

This skill creates/updates:

- **CFD-\* post-launch feedback entries** (feedback capture specifications, channel/type-based) — Every piece of user feedback becomes a CFD- entry with source, sentiment, impact, and action taken; traced to GTM- channels and user personas
- **Feedback processing workflow/matrix** — Triage → Categorization → Prioritization → Action mapping showing how feedback flows from capture to ID updates (CFD- → FEA-/BR-/RISK- → EPIC-)
- **CFD-\* update entries** — CFD- entries updated with resolution status, outcome, and follow-up evidence, enabling confidence progression (initial feedback → validated pattern → implemented action → confirmed outcome)

All CFD-* post-launch entries are **evidential feedback records**, not confidence-based themselves but supporting confidence scoring on OTHER IDs:
- **Timestamped** (when feedback was received, to track trends and velocity)
- **Sourced** (channel, user segment, user ID if available for follow-up)
- **Categorized** (UX | Performance | Feature Gap | Bug | Praise | Confusion for trend analysis)
- **Prioritized** (Critical/High/Medium/Low with impact justification)
- **Actionable** (every CFD- either triggers ID creation/update or documents "won't fix" decision)
- **Closed-loop** (user receives response and can verify resolution)

Example CFD- post-launch entries:
```markdown
CFD-101: "Can't figure out how to export my data"
Type: Support Ticket
Source: Intercom (GTM-002 email → user support request)
Date: 2025-01-15
User Segment: PER-001 (Startup Founder)

Verbatim: "I've been using the tool for a week and I can't find any way to export my work."

Processed:
  Category: Feature Gap
  Sentiment: Frustrated
  Priority: High
  Frequency: Repeated (3rd request this week)

Impact Assessment:
  Users Affected: ~50 (based on support volume)
  KPI Impact: KPI-104 (D7 Retention) — export needed for team use case
  Revenue Risk: High — multiple users mentioned "dealbreaker"

Action:
  Response: "Thanks for reaching out! Export is on our roadmap."
  Internal Action: Escalated to product team, added to backlog
  Linked IDs: FEA-025 (Export Feature) created, EPIC-05 updated
  Status: In Progress

Resolution:
  Outcome: FEA-025 shipped in v1.2
  Date: 2025-02-01
  Follow-up: Emailed user with release notes

Linked IDs: GTM-002 (email channel source), PER-001 (persona), KPI-104 (affected metric), FEA-025 (action taken), EPIC-05 (implementation)

---

CFD-102: NPS Detractor Response
Type: NPS Response
Source: In-App Survey (MON-005 trigger)
Date: 2025-01-18
User Segment: PER-002 (Team Lead)

Verbatim: "Score: 4. Too slow. Takes forever to load projects and I give up waiting."

Processed:
  Category: Performance
  Sentiment: Negative
  Priority: Critical
  Frequency: Trending (NPS dropped 10 points this week)

Impact Assessment:
  Users Affected: ~200 (20% of NPS responses mention speed)
  KPI Impact: KPI-103 (Activation), KPI-104 (Retention) — both trending down
  Revenue Risk: High — performance is activation blocker

Action:
  Response: N/A (anonymous survey)
  Internal Action: Performance spike investigation started (MON-001 latency breach detected)
  Linked IDs: RISK-012 (Performance Degradation) escalated, EPIC-06 prioritized for optimization
  Status: In Progress

Resolution:
  Outcome: Database query optimization deployed, latency restored to baseline
  Date: 2025-01-22
  Follow-up: Next NPS cycle (Day 30) will measure improvement

Linked IDs: MON-005 (dashboard source), PER-002, KPI-103, KPI-104, MON-001 (latency baseline), RISK-012, EPIC-06

---

CFD-103: Community Feature Request (Dark Mode)
Type: Community Post
Source: Discord #feature-requests (GTM-005 community channel)
Date: 2025-01-20
User Segment: Power Users (multiple PER-)

Verbatim: "Thread: 47 messages discussing dark mode. Summary: 15 unique users requesting."

Processed:
  Category: Feature Gap
  Sentiment: Neutral (constructive)
  Priority: Medium
  Frequency: Repeated (ongoing, 15 users vocal)

Impact Assessment:
  Users Affected: 15+ vocal, likely more silent
  KPI Impact: Minor — nice-to-have, not activation blocker; may reduce churn for night users
  Revenue Risk: Low

Action:
  Response: Community manager acknowledged, added to public roadmap
  Internal Action: Added to backlog as P2 feature
  Linked IDs: FEA-030 (Dark Mode) created, posted on public roadmap
  Status: Acknowledged

Resolution:
  Outcome: Pending — scheduled for Q2 release
  Date: N/A
  Follow-up: Posted on public roadmap

Linked IDs: GTM-005 (community channel), PER-* (multiple personas), FEA-030, public roadmap
```

## Feedback → ID Flow

Each CFD- post-launch entry triggers cascading updates:

| Feedback Type | Creates/Updates | Confidence Impact | Example |
|---------------|-----------------|-------------------|---------|
| **Feature Request** | FEA-, BR-FEA- | Increases FEA- confidence (user interview → beta validation) | CFD-101 (export request, 3rd this week) → FEA-025 (confidence: 2→3, source: support-requests-2025-01) |
| **Performance Complaint** | MON- threshold, RISK- escalation | Triggers MON- investigation; may update RISK- severity | CFD-102 (slow, 20% mention) → MON-001 threshold validation → RISK-012 escalation |
| **UX Confusion** | SCR-, UJ- refinement | Informs screen redesign without changing foundational journey | "Can't find export" → SCR-005 (export button placement) update |
| **Bug Report** | RISK- or direct fix | RISK- frequency increases → triggers prioritization | Critical bugs → P0 RISK- entry |
| **Praise/Testimonial** | CFD- (evidence), GTM- (social proof) | Confirms CFD- hypothesis; can become GTM- case study | "Love this feature!" → CFD- entry → GTM-015 (testimonial) |

This feedback loop enables **evidence-driven iteration**: feedback patterns → ID updates → implementation → launch validation → next iteration.

## Downstream Connections

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v1.0 Market Adoption Planning** | CFD- feedback patterns inform roadmap | 10× CFD- export requests → FEA-025 move to P1 |
| **Product Development** | CFD- → FEA-, BR- updates feed next EPIC | CFD-102 performance complaints → EPIC-06 optimization prioritized |
| **Sales/Marketing** | CFD- testimonials become GTM assets | CFD-103 community enthusiasm → GTM-015 case study |
| **Support Team** | CFD- patterns become FAQ and onboarding | Repeated "can't export" → FAQ article |
| **Risk Management** | CFD- negative trends escalate RISK- | NPS dropping → RISK-012 escalation |
| **KPI Accountability** | CFD- confirms KPI- achievement | KPI-104 (D7 Retention) gaps trigger CFD- investigation |

## Purpose

Establish systematic channels for capturing, processing, and acting on post-launch user feedback—closing the loop between user experience and product iteration.

## Core Concept: Feedback as Fuel

> Feedback is not a task to complete—it is **fuel for iteration**. Every piece of feedback should flow into the ID graph, informing future CFD-, BR-, FEA-, or RISK- entries. If feedback sits in a spreadsheet, it's not feedback—it's noise.

## Feedback Channels

| Channel | Type | Best For | Response Time |
|---------|------|----------|---------------|
| **In-App** | Prompted | Contextual reactions | Real-time |
| **Support** | Reactive | Issues, requests | <24h |
| **Community** | Proactive | Discussion, ideas | Ongoing |
| **Surveys** | Scheduled | Structured data | Periodic |
| **Analytics** | Passive | Behavior signals | Continuous |

## Execution

1. **Map feedback touchpoints**
   - Where do users already reach out?
   - Where should we actively prompt?
   - What channels from GTM- are active?

2. **Design feedback capture**
   - In-app widgets (NPS, CSAT, feature requests)
   - Support ticket taxonomy
   - Community moderation workflow
   - Survey schedule and instruments

3. **Define processing workflow**
   - Who triages incoming feedback?
   - How does it become CFD- entries?
   - What triggers action?

4. **Establish feedback → ID flow**
   - Feedback → CFD-
   - CFD- → BR-, FEA-, RISK- updates
   - Updates → EPIC- for implementation

5. **Set up monitoring**
   - Volume metrics
   - Sentiment tracking
   - Response time SLAs

6. **Create CFD- entries** for post-launch feedback

## CFD- Output Template (Post-Launch Feedback)

```
CFD-XXX: [Feedback Title]
Type: [Support Ticket | Feature Request | Bug Report | NPS Response | Community Post | Survey Response]
Source: [Intercom | Zendesk | Discord | In-App | Email | Twitter]
Date: [When received]
User Segment: [PER-XXX if identifiable]

Verbatim: "[Exact user quote or description]"

Processed:
  Category: [UX | Performance | Feature Gap | Bug | Praise | Confusion]
  Sentiment: [Positive | Neutral | Negative | Frustrated]
  Priority: [Critical | High | Medium | Low]
  Frequency: [One-off | Repeated | Trending]

Impact Assessment:
  Users Affected: [Count or estimate]
  KPI Impact: [KPI-XXX affected if applicable]
  Revenue Risk: [High | Medium | Low | None]

Action:
  Response: [How we responded to user]
  Internal Action: [What we're doing about it]
  Linked IDs: [BR-XXX, FEA-XXX, RISK-XXX created/updated]
  Status: [New | Acknowledged | In Progress | Resolved | Won't Fix]

Resolution:
  Outcome: [What happened]
  Date: [When resolved]
  Follow-up: [Did we close the loop with user?]
```

**Note:** See Produces section above for detailed CFD- examples with full traceability links.

## Feedback Collection Methods

### In-App Feedback

| Method | When to Use | Question |
|--------|-------------|----------|
| **NPS** | After activation, monthly | "How likely to recommend?" (0-10) |
| **CSAT** | After support interaction | "How satisfied?" (1-5) |
| **CES** | After key action | "How easy was this?" (1-7) |
| **Feature Request** | Persistent widget | "What's missing?" |
| **Bug Report** | Error states | "What went wrong?" |

### Survey Cadence

| Survey | Frequency | Purpose |
|--------|-----------|---------|
| **NPS** | Monthly | Overall sentiment tracking |
| **Onboarding Exit** | After churn signal | Why didn't they activate? |
| **Feature Satisfaction** | Post-release | Did this solve the problem? |
| **Annual Deep Dive** | Yearly | Strategic feedback |

### Passive Signals

| Signal | What It Indicates | Action Trigger |
|--------|-------------------|----------------|
| **Rage clicks** | Frustration | UX investigation |
| **Drop-off** | Confusion or friction | Funnel analysis |
| **Feature abandonment** | Poor value delivery | User interview |
| **Error rates** | Technical issues | Bug investigation |

## Feedback Processing Workflow

```
CAPTURE → TRIAGE → CATEGORIZE → PRIORITIZE → ACTION → CLOSE LOOP

1. CAPTURE
   - All channels → central inbox

2. TRIAGE (Daily)
   - Critical: <4h response
   - High: <24h response
   - Medium/Low: Weekly review

3. CATEGORIZE
   - Apply CFD- template
   - Link to existing IDs

4. PRIORITIZE
   - Frequency × Impact × Revenue Risk
   - Weekly prioritization meeting

5. ACTION
   - Create/update IDs (BR-, FEA-, RISK-)
   - Add to EPIC- backlog
   - Communicate internally

6. CLOSE LOOP
   - Respond to user
   - Update CFD- status
   - Verify resolution
```

## Sentiment Monitoring

Track aggregate sentiment over time:

| Metric | Calculation | Target |
|--------|-------------|--------|
| **NPS** | % Promoters - % Detractors | >30 |
| **CSAT** | % Satisfied (4-5) | >80% |
| **Support Volume** | Tickets per 100 users | <5 |
| **Response Time** | Median first response | <4h |
| **Resolution Rate** | % resolved within SLA | >90% |

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Feedback graveyard** | Collect but never act | Mandate weekly triage meeting |
| **Only negative** | No positive feedback captured | Celebrate wins, capture praise |
| **No closing loop** | Users never hear back | Require follow-up on High+ priority |
| **Volume without insight** | "We got 500 tickets" | Categorize and trend analysis |
| **Building in silence** | Ship features, don't validate | Post-release surveys |
| **Anecdote-driven** | "One user said..." | Require frequency data |

## Quality Gates

Before proceeding to v1.0 Market Adoption:

- [ ] All feedback channels identified and configured
- [ ] In-app feedback widgets deployed
- [ ] Support ticket taxonomy defined
- [ ] Community monitoring active
- [ ] Processing workflow documented and assigned
- [ ] Feedback → ID flow established
- [ ] Sentiment metrics baselined

## Detailed References

- **Feedback channel setup**: See `references/channel-setup.md`
- **CFD- post-launch template**: See `assets/cfd-feedback-template.md`
- **Survey question bank**: See `references/survey-questions.md`
- **Sentiment analysis guide**: See `references/sentiment-guide.md`
