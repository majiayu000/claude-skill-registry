---
name: prd-v09-feedback-loop-setup
description: >
  Establish channels and processes for capturing and processing post-launch feedback during PRD v0.9 Go-to-Market.
  Triggers on requests to set up feedback systems, capture user input, or when user asks "how do we collect feedback?",
  "feedback loop", "user research", "post-launch feedback", "customer feedback", "NPS", "voice of customer".
  Outputs CFD- entries specialized for post-launch feedback capture.
---

# Feedback Loop Setup

Position in workflow: v0.9 Launch Metrics → **v0.9 Feedback Loop Setup** → v1.0 Market Adoption

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

**Example CFD- entries:**

```
CFD-101: "Can't figure out how to export my data"
Type: Support Ticket
Source: Intercom
Date: 2025-01-15
User Segment: PER-001 (Startup Founder)

Verbatim: "I've been using the tool for a week and I can't find
          any way to export my work. I need to share results with
          my team. Is this possible? If not, this is a dealbreaker."

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
  Response: "Thanks for reaching out! Export is on our roadmap.
             We're prioritizing this for our next release."
  Internal Action: Escalated to product team, added to backlog
  Linked IDs: FEA-025 (Export Feature) created, EPIC-05 updated
  Status: In Progress

Resolution:
  Outcome: FEA-025 shipped in v1.2
  Date: 2025-02-01
  Follow-up: Emailed user with release notes
```

```
CFD-102: NPS Detractor Response
Type: NPS Response
Source: In-App Survey
Date: 2025-01-18
User Segment: PER-002 (Team Lead)

Verbatim: "Score: 4. Too slow. Takes forever to load projects
          and I give up waiting half the time."

Processed:
  Category: Performance
  Sentiment: Negative
  Priority: Critical
  Frequency: Trending (NPS dropped 10 points this week)

Impact Assessment:
  Users Affected: ~200 (20% of NPS responses mention speed)
  KPI Impact: KPI-103 (Activation), KPI-104 (Retention)
  Revenue Risk: High — performance is activation blocker

Action:
  Response: N/A (anonymous survey)
  Internal Action: Performance spike investigation started
  Linked IDs: RISK-012 (Performance Degradation) escalated
  Status: In Progress

Resolution:
  Outcome: Database query optimization deployed
  Date: 2025-01-22
  Follow-up: Next NPS cycle will measure improvement
```

```
CFD-103: Community Feature Discussion
Type: Community Post
Source: Discord #feature-requests
Date: 2025-01-20
User Segment: Power Users (multiple PER-)

Verbatim: "Thread: 47 messages discussing dark mode.
          Summary: 15 unique users requesting dark mode.
          Top comment: 'I work at night and this is eye-strain city.'"

Processed:
  Category: Feature Gap
  Sentiment: Neutral (constructive)
  Priority: Medium
  Frequency: Repeated (ongoing thread)

Impact Assessment:
  Users Affected: 15+ vocal, likely more silent
  KPI Impact: Minor — nice-to-have, not activation blocker
  Revenue Risk: Low

Action:
  Response: Community manager acknowledged, added to public roadmap
  Internal Action: Added to backlog as P2
  Linked IDs: FEA-030 (Dark Mode) created
  Status: Acknowledged

Resolution:
  Outcome: Pending — scheduled for Q2
  Date: N/A
  Follow-up: Posted on public roadmap
```

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

## Feedback → ID Flow

| Feedback Type | Creates/Updates | Example |
|---------------|-----------------|---------|
| **Feature Request** | FEA-, BR-FEA- | CFD-101 → FEA-025 |
| **Bug Report** | RISK- (or direct fix) | CFD-102 → RISK-012 |
| **UX Confusion** | SCR-, UJ- refinement | "Can't find X" → SCR-005 update |
| **Performance** | MON-, RISK- | "Too slow" → MON-010 threshold |
| **Praise** | CFD- (testimonial), GTM- | "Love this!" → GTM-015 (social proof) |

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

## Downstream Connections

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v1.0 Planning** | CFD- feedback informs roadmap | CFD-101 frequency → FEA-025 priority |
| **Product Development** | CFD- → FEA-, BR- updates | "Users need X" → FEA-030 |
| **Support Team** | CFD- patterns for FAQ | Repeated CFD-102 → knowledge base |
| **Marketing** | CFD- testimonials for GTM- | Positive CFD- → case study |
| **Risk Management** | CFD- negative trends → RISK- | Sentiment drop → RISK-015 |

## Detailed References

- **Feedback channel setup**: See `references/channel-setup.md`
- **CFD- post-launch template**: See `assets/cfd-feedback-template.md`
- **Survey question bank**: See `references/survey-questions.md`
- **Sentiment analysis guide**: See `references/sentiment-guide.md`
