---
name: prd-v05-risk-discovery-interview
description: Surface risks through guided questioning, helping users consider pivots, constraints, and prioritization during PRD v0.5 Red Team Review. Triggers on requests to identify risks, stress-test the idea, perform red team review, or when user asks "what could go wrong?", "identify risks", "red team", "risk assessment", "challenge assumptions", "stress test the idea". Consumes all prior IDs (CFD-, BR-, FEA-, PER-, UJ-, SCR-) as interview context. Outputs RISK- entries with owner decisions and mitigations. Feeds v0.5 Technical Stack Selection.
---

# Risk Discovery Interview

Position in workflow: v0.4 Screen Flow Definition → **v0.5 Risk Discovery Interview** → v0.5 Technical Stack Selection

This is an **interactive interview skill**. The AI asks questions, the user reflects and decides. The goal is to surface risks so the user can mitigate or accept them—not to kill ideas.

## Design Principles

1. **Interview, not inquisition** — Facilitate discovery, don't interrogate
2. **Inform, not kill** — Surface risks so user can mitigate, not abandon
3. **User owns decisions** — AI facilitates, user assigns severity and response
4. **Actionable outputs** — Every risk has a mitigation path or explicit "accept"

## Risk Categories

### Discovery Categories (Interview Prompts)

| Category | Focus Area | Example Questions |
|----------|------------|-------------------|
| **Market** | Competitors, timing, demand | "What if [competitor] launches this feature next month?" |
| **Technical** | Complexity, unknowns, dependencies | "Which feature has the most technical uncertainty?" |
| **Adoption** | User behavior, activation, retention | "What's the biggest friction point in onboarding?" |
| **Resource** | Team, budget, time | "If you had to cut scope by 50%, what stays?" |
| **Dependency** | External factors, integrations, partners | "What external factor could block launch?" |
| **Timing** | Deadlines, market windows, seasonality | "Is there a deadline we must hit? Why?" |

### Scoring Categories (README Scorecard)

Each RISK- entry maps to one of 3 scoring categories for the README Risk Scorecard:

| Scoring Category | Discovery Categories | Measures |
|---|---|---|
| **Market** | Market, Timing | Will anyone buy this? |
| **User** | Adoption, Dependency | Will users succeed with this? |
| **Technical** | Technical, Resource | Can we build and run this? |

## Interview Flow

### Phase 1: Context Review
Before asking questions, AI reviews:
- CFD- evidence from v0.1-v0.2
- FEA- features and their priorities
- UJ- journeys and their complexity
- BR- business rules and constraints

### Phase 2: Guided Questions
Ask questions from each category, adapting based on product context:

**Market Risks:**
- "What happens if [competitor] launches something similar in 60 days?"
- "What market assumption are you least confident about?"
- "What would cause users to choose a competitor instead?"

**Technical Risks:**
- "Which feature has the most technical uncertainty?"
- "What technology choice are you least confident about?"
- "Is there anything you've never built before?"

**Adoption Risks:**
- "What's the biggest friction point in [UJ-001 onboarding journey]?"
- "What behavior change are you asking users to make?"
- "What would cause a user to churn in the first week?"

**Resource Risks:**
- "If you had only 2 developers, what would you cut?"
- "What skill does the team lack?"
- "What's your runway for validation?"

**Dependency Risks:**
- "What external API or service could break your product?"
- "What partner relationship is critical?"
- "What regulatory requirement could block launch?"

**Timing Risks:**
- "Is there a hard deadline? What happens if you miss it?"
- "Is there a market window closing?"
- "What seasonal factor affects launch timing?"

### Phase 3: Risk Documentation
For each identified risk, create RISK- entry with user input on severity and response.

### Phase 4: Priority & Review
- Force-rank risks by Impact × Likelihood
- Identify top 3-5 that require active mitigation
- Document "accept" decisions explicitly

## Interview Techniques

| Technique | How to Use | When to Use |
|-----------|------------|-------------|
| **Pre-mortem** | "It's 6 months from now and the product failed. Why?" | Opening question |
| **Constraint forcing** | "If you only had [X], what would you cut?" | Resource discovery |
| **Dependency mapping** | "What external factor could block launch?" | Dependency discovery |
| **Assumption surfacing** | "What must be true for this to work?" | Any category |
| **Devil's advocate** | "Let me argue the opposite—what if [X]?" | Challenge weak evidence |

## RISK- Output Template

```
RISK-XXX: [Risk Title]
Scoring Category: [Market | User | Technical]
Discovery Category: [Market | Technical | Adoption | Resource | Dependency | Timing]
Description: [What could go wrong]
Trigger: [What would cause this to happen]
Impact: [High | Medium | Low] — User assessed
Likelihood: [High | Medium | Low] — User assessed
Raw Score: [Impact × Likelihood, 1-9]
Status: [open | mitigating | mitigated | resolved | accepted]
Effective Score: [Raw Score × Status Weight]

Early Signal: [How we'd know this is happening]
Response: [Mitigate | Accept | Avoid | Transfer]
Mitigation: [Specific action if Response = Mitigate]
Owner: [Who is responsible for monitoring]

Linked IDs: [FEA-XXX, UJ-XXX, BR-XXX affected]
Review Date: [When to reassess this risk]
Added: [PRD stage when discovered, e.g., v0.5]
```

**Status weights**: open=1.0, accepted=1.0, mitigating=0.5, mitigated=0.25, resolved=0.0

**Example RISK- entry:**
```
RISK-001: Primary API Dependency (Stripe) Outage
Scoring Category: Technical
Discovery Category: Dependency
Description: Stripe API outage would block all payment processing
Trigger: Stripe infrastructure failure or rate limiting
Impact: High (3) — All revenue blocked during outage
Likelihood: Low (1) — Stripe has 99.99% uptime SLA
Raw Score: 3
Status: mitigating
Effective Score: 1.5

Early Signal: Stripe status page, payment failure rate spike
Response: Mitigate
Mitigation:
  - Implement graceful degradation (queue payments for retry)
  - Add status page monitoring alert
  - Document manual billing fallback process
Owner: Tech Lead

Linked IDs: FEA-020 (payments), UJ-005 (checkout), BR-030 (pricing)
Review Date: Before launch, quarterly thereafter
Added: v0.5
```

## Risk Response Types

| Response | When to Use | Example |
|----------|-------------|---------|
| **Mitigate** | Can reduce impact or likelihood | Add fallback provider, implement retry logic |
| **Accept** | Low impact or unavoidable | "Competitor might copy us—we accept" |
| **Avoid** | Change plan to eliminate risk | Remove feature with high technical uncertainty |
| **Transfer** | Someone else owns the risk | Use managed service instead of self-hosting |

## Severity Matrix

| | Low Impact | Medium Impact | High Impact |
|---|---|---|---|
| **High Likelihood** | Monitor | Mitigate | Mitigate urgently |
| **Medium Likelihood** | Accept | Monitor/Mitigate | Mitigate |
| **Low Likelihood** | Accept | Accept/Monitor | Monitor |

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Risk theater** | 50+ risks documented | Focus on top 10 that matter |
| **All high severity** | Everything is critical | Force rank; max 3-5 "High" |
| **No owner** | Risks without accountability | Every RISK- needs an owner |
| **Mitigation = "be careful"** | Vague responses | Require specific, testable actions |
| **Interview becomes lecture** | AI talks more than user | Ask, listen, summarize |
| **Killing ideas** | Every risk leads to "don't do it" | Frame as "how to succeed despite" |

## Phase 5: Score & Scorecard

After documenting all risks:

1. **Assign scoring categories**: Map each RISK- to Market, User, or Technical
2. **Calculate scores**: Raw Score = Impact × Likelihood; Effective = Raw × Status Weight (all start as `open`)
3. **Sum by category**: Add effective scores within each scoring category
4. **Determine risk level**: Total score → Low (0-12), Moderate (13-25), Elevated (26-40), High (41+)
5. **Update README scorecard**: Fill in the Risk Scorecard table in README.md

## Quality Gates

Before proceeding to Technical Stack Selection:

- [ ] All 6 risk categories explored
- [ ] Maximum 10-15 RISK- entries (focused, not exhaustive)
- [ ] Force-ranked by priority (Impact × Likelihood)
- [ ] Top 5 risks have specific mitigation plans
- [ ] "Accept" decisions are explicit, not accidental
- [ ] Every RISK- has an owner
- [ ] Every RISK- has a scoring category (Market/User/Technical)
- [ ] README Risk Scorecard updated with baseline scores

## Continuous Risk Management

v0.5 establishes the **baseline** risk register, but risk discovery does not end here. New RISK- entries can be added at any stage:

| Stage | Typical New Risks | Score Impact |
|-------|-------------------|--------------|
| v0.6 Architecture | Infrastructure complexity, integration unknowns | Technical score rises |
| v0.7 Build | Implementation blockers, test coverage gaps | Technical score rises |
| v0.8 Deployment | Operational risks, security findings | Technical score rises |
| v0.9 GTM | Market timing shifts, competitive moves | Market score rises |
| v1.0 Growth | Real adoption data contradicting assumptions | User score rises |

**Protocol when adding risks after v0.5**:
1. Use the same RISK- template (assign next available number)
2. Set `Added: v0.X` to record which stage surfaced it
3. Recalculate category and total scores
4. Update README Risk Scorecard

**Protocol when risk status changes**:
1. Update the RISK- entry status in PRD.md
2. Recalculate effective score (Raw × new Status Weight)
3. Update README Risk Scorecard totals

## Downstream Connections

RISK- entries feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **README Risk Scorecard** | Aggregated scores by category | Total score determines project risk level |
| **v0.5 Technical Stack Selection** | RISK- constraints affect tech choices | RISK-003 (latency) → choose edge hosting |
| **v0.6 Architecture Design** | Risk mitigations become architecture requirements | RISK-005 → add circuit breaker |
| **v0.7 Build Execution** | Risk monitoring in EPIC | Track RISK-001 early signals |
| **KPI- Thresholds** | Kill criteria from risks | "If RISK-002 triggers, evaluate pivot" |

## Detailed References

- **Interview question bank**: See `references/question-bank.md`
- **RISK- entry template**: See `assets/risk.md`
- **Example risk register**: See `references/examples.md`
