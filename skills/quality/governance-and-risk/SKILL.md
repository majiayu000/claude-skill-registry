---
name: governance-and-risk
description: Use when making architectural decisions without documentation, skipping risk analysis, accepting risks without mitigation, or treating governance as optional bureaucracy - enforces mandatory DAR/RSKM based on project risk level
---

# Governance and Risk

## Overview

This skill implements the **Decision Analysis & Resolution (DAR)** and **Risk Management (RSKM)** process areas from the CMMI-based SDLC prescription.

**Core principle**: Proactive governance prevents costly reactive firefighting. Documentation and risk management are investments that pay 3-10x returns by avoiding crisis mode.

**Critical distinction**:
- **Reactive**: Handle problems when they occur (expensive, stressful, compounding)
- **Proactive**: Identify and mitigate problems before they occur (cheap, controlled, preventive)

**Reference**: See `docs/sdlc-prescription-cmmi-levels-2-4.md` Sections 3.4.1 (DAR) and 3.4.2 (RSKM) for complete policy.

---

## When to Use

Use this skill when:
- Making architectural or technical decisions without ADRs
- Hearing "it's obvious" or "everyone agrees" (groupthink red flag)
- Skipping risk identification ("what could go wrong?")
- Accepting risks without mitigation plans
- Deferring to authority without independent analysis (CTO says, tech lead suggests)
- Using sunk cost to justify decisions ("we've already invested...")
- Treating governance as bureaucracy or overhead
- No ongoing risk monitoring ("set and forget")

**Do NOT use for**:
- Trivial decisions (variable names, code style) → Use coding standards
- Implementation details → Use design-and-build skill
- Security-specific risk analysis → Use ordis-security-architect

---

## Quick Reference

| Situation | Framework | Mandatory At | Key Action |
|-----------|-----------|--------------|------------|
| "Obvious" architectural decision | DAR with ADR | Level 3+ | Document alternatives even if choice is clear |
| High-risk decision (vendor, framework) | DAR with decision matrix | Level 2+ for high-risk | Evaluate alternatives before committing |
| Authority wants specific option | DAR with independent analysis | Level 3+ | Analyze alternatives BEFORE authority input |
| External dependency (API, vendor) | RSKM with mitigation | Level 2+ | Risk register + mitigation plan mandatory |
| "Low-risk" project | RSKM with risk identification | Level 2+ | Optimism bias - identify risks proactively |
| Mid-project (risk monitoring) | RSKM review cadence | Level 3+ | Scheduled reviews, not set-and-forget |

---

## Governance Level Framework

### When Practices Are MANDATORY

**Level 2 Baseline (All Projects)**:
- ADRs for high-risk decisions (vendor selection, framework choice, data storage)
- Risk identification with basic register
- Mitigation plans for high-probability or high-impact risks

**Level 3 Organizational Standard**:
- **ADRs for all architectural decisions** (not just high-risk)
- Alternatives analysis with decision criteria
- Risk register with probability/impact classification
- Scheduled risk reviews (not set-and-forget)
- Independent analysis before authority/consensus input

**Level 4 Quantitative**:
- Statistical risk models
- Quantitative decision criteria
- Process performance baselines for decision quality

### When Practices Are OPTIONAL

**Level 1 or Low-Risk Projects**:
- Internal prototypes (< 2 week lifespan)
- Single-developer projects with no audit requirements
- Throwaway code (spikes, experiments)

**CRITICAL**: "Low-risk" is often optimism bias. Verify with risk assessment before declaring optional.

---

## Anti-Patterns and Rationalizations

### "It's Obvious"

**Detection**: "Everyone agrees", "clear choice", "no brainer"

**Why it's tempting**: Saves time, reduces documentation burden, team aligned

**Why it fails**: Today's "obvious" is tomorrow's mysterious. Future maintainers lack context, assumptions not validated, alternatives not considered

**Counter**:
- **Level 3 requirement**: Document even "obvious" decisions
- Context loss timeline: 6 months for team turnover, 3 months for forgotten assumptions
- Question to ask: "If someone joins the team in 6 months, will they know WHY we chose this?"
- Lightweight ADR takes 20 minutes, saves hours of future confusion

**Red flags**: "We all know", "Obviously", "No need to write it down"

### "Low-Risk Project"

**Detection**: "Simple project", "Internal only", "We've done this before", "What could go wrong?"

**Why it's tempting**: Small scope, experienced team, reduces overhead

**Why it fails**: Scope creep, resource constraints, and timeline slips hit "simple" projects just as often. Optimism bias blinds to risks.

**Counter**:
- **Level 2 requirement**: Risk identification for ALL projects
- Common risks for "simple" projects: scope creep (stakeholders add "just one more thing"), resource availability (PTO, competing priorities), data access (permissions, security approvals), timeline slip (integration surprises)
- Reactive firefighting costs 3-10x proactive planning
- 30-minute risk session saves days of crisis mode

**Red flags**: "What could go wrong?", "It's just...", "Low-risk"

### "Authority/CTO Prefers It"

**Detection**: "CTO met with vendor", "Tech lead suggested", "Management wants"

**Why it's tempting**: Reduces conflict, speeds decision, aligns with leadership

**Why it fails**: Authority bias prevents genuine alternatives analysis. Senior stakeholders have blind spots, vendor relationships create bias, title ≠ technical correctness

**Counter**:
- **Level 3 requirement**: Independent alternatives analysis BEFORE authority input
- Document decision criteria first (security, cost, integration, vendor stability)
- Evaluate options against criteria WITHOUT authority preference
- Present analysis to authority: "Here's what the data shows, here's your preference, here's my recommendation"
- Authority can override, but must be documented as "decision override based on non-technical factors"

**Red flags**: "CTO wants", "We should align with leadership", "Don't want to contradict"

### "We've Already Invested Time" (Sunk Cost)

**Detection**: "We've had 2 sales calls", "Demo account set up", "Already started integration"

**Why it's tempting**: Feels wasteful to "go backwards", momentum toward choice

**Why it fails**: Sunk cost fallacy - past investment doesn't validate future commitment. Small sunk cost vs large future cost (vendor lock-in, wrong tool).

**Counter**:
- **Name the fallacy**: "This is sunk cost fallacy"
- Calculate future cost: "2 sales calls (4 hours sunk) vs 3-year vendor lock-in (hundreds of hours if wrong choice)"
- Reframe: "We invested 4 hours evaluating Option A. Should we invest 2 hours evaluating Options B and C to validate?"
- Past investment gives you evaluation data, not decision commitment

**Red flags**: "We've already", "Going backwards", "Wasted effort"

### "Trust the Vendor" / "99.9% SLA"

**Detection**: "Established company", "Good reputation", "SLA guarantees uptime"

**Why it's tempting**: Vendor reputation, SLA promises reduce perceived risk

**Why it fails**: SLAs are probabilistic, not guarantees. 99.9% = 43 minutes downtime per month. All vendors have outages. Trust ≠ technical mitigation.

**Counter**:
- **Calculate SLA impact**: 99.9% uptime = 43 min/month, 8.76 hours/year. Acceptable for your use case?
- **Mitigation still required**: Circuit breaker, fallback, queueing, graceful degradation
- Vendor reputation reduces probability but doesn't eliminate risk
- Question: "What happens to our users if vendor API is down for 1 hour? Do we have a plan?"

**Red flags**: "We can trust them", "SLA is good enough", "Reputable company"

### "We'll Fix It If It Happens"

**Detection**: "Handle issues as they come up", "React when needed", "Cross that bridge"

**Why it's tempting**: Defers work, avoids speculation, focuses on current tasks

**Why it fails**: Reactive firefighting costs 3-10x proactive mitigation. Incidents occur when you have least capacity to respond (deadlines, weekends, vacations).

**Counter**:
- **Cost math**: 1 hour mitigation planning now vs 10 hours firefighting later
- Reactive timing: Incidents don't wait for convenient times - they hit during sprints, before demos, on Friday evenings
- **Level 2 requirement**: Mitigation plan for high-probability or high-impact risks BEFORE acceptance
- Question: "Do you have 10 hours next week to drop everything and firefight this risk if it materializes?"

**Red flags**: "We'll handle it", "If it happens", "Cross that bridge when we come to it"

### "Risks Haven't Materialized" (Complacency)

**Detection**: "4 months in, no issues", "Original risks didn't hit", "We're good"

**Why it's tempting**: Past success validates approach, monitoring feels wasteful

**Why it fails**: Risks evolve throughout project lifecycle. Absence of risks to-date ≠ absence of future risks. Complacency before late-stage crunch (integration, final testing, deployment).

**Counter**:
- **Lifecycle risk evolution**: Early risks (requirements, team ramp-up) vs late risks (integration, tech debt, timeline crunch)
- Month 4 of 6: Integration testing, timeline pressure, technical debt, scope control
- **Level 3 requirement**: Scheduled risk reviews, not set-and-forget
- New risks emerge, probabilities shift, priorities change

**Red flags**: "No problems yet", "We're on track", "Monitoring feels like overhead"

### "Process Feels Like Bureaucracy"

**Detection**: "Overhead", "Red tape", "Meetings for meetings' sake", "We want to code"

**Why it's tempting**: Team wants to deliver, documentation feels unproductive

**Why it fails**: Lightweight process prevents heavyweight problems. 30 min planning saves hours of firefighting. Process ≠ bureaucracy.

**Counter**:
- **Process vs bureaucracy**: Process has ROI (30 min → saves hours). Bureaucracy has no ROI (forms for forms' sake).
- Lightweight governance: 20-min ADR, 30-min risk session, 15-min risk review
- **Cost comparison**: 30 min process now vs 10+ hours crisis later
- Question: "Would you rather spend 30 minutes planning or 10 hours firefighting next month?"

**Red flags**: "Bureaucracy", "Overhead", "Red tape", "Slows us down"

### "We're Tired / Under Pressure"

**Detection**: "Just finished major release", "Deadline is tight", "Team exhausted"

**Why it's tempting**: Exhaustion and deadlines are real, shortcuts feel necessary

**Why it fails**: Shortcuts under pressure create more pressure later. Technical debt compounds into crisis. Skipping governance creates future exhaustion.

**Counter**:
- **Compound effect**: Skipping governance now creates 3x more work later
- Pressure math: 2 hours deadline pressure now vs 10+ hours crisis pressure later
- When you're exhausted is exactly when you need process (prevents mistakes)
- Question: "Will skipping governance make the NEXT deadline easier or harder?"

**Red flags**: "We're exhausted", "Too busy", "Under pressure", "Just this once"

### "We'll Document Later"

**Detection**: "After we ship", "When we have time", "In the next sprint"

**Why it's tempting**: Defers effort, focuses on delivery now

**Why it fails**: "Later" never comes. Context is lost immediately. Future maintainers suffer.

**Counter**:
- **Historical pattern**: "Later" has 5% success rate (documented fact)
- Context loss: Starts immediately, complete within 2 weeks
- **Requirement**: Documentation is part of "done", not optional follow-up
- Question: "When exactly is 'later'? Put it on the calendar now."

**Red flags**: "Later", "After we ship", "When we have time", "Eventually"

---

## Handling "My Project Is Special" Exceptions

**Common exception requests**:
- "We're a startup, need to move fast"
- "This is just an MVP/prototype"
- "We'll upgrade to proper governance after product-market fit"
- "Our team is experienced, we don't need process"
- "This project is different because..."

**Why it's tempting**: Context appears legitimately exceptional, constraints feel unique, team confidence is high

**Why it fails**: Every team thinks they're special. Startups fail from poor decisions as often as slow delivery. "MVP" and "prototype" often become production. "After product-market fit" never arrives.

**Response framework**:

1. **Acknowledge the constraint**: "Startup time pressure IS real, I understand the urgency"

2. **Reframe governance as enabler**: "Governance prevents the costly mistakes that kill startups - bad vendor choices, unmitigated risks, undocumented decisions that create chaos during scaling"

3. **Offer Level 2 as minimum**: "Not suggesting heavyweight process. Level 2 = 30-min risk session, ADRs for high-risk decisions only. That's ~2% overhead, not 20%."

4. **Make exception criteria explicit**:
   - **Non-negotiable Level 2 minimum**: Security-critical, customer-facing, financially-material, or >3 month projects
   - **Level 1 acceptable**: Internal prototype <2 weeks, single developer, throwaway code, no audit trail needed
   - **Exception must be documented**: If declaring Level 1, document why in project README

5. **Show the math**: "30 minutes planning vs 10+ hours crisis firefighting. Which timeline can your startup afford?"

**Red flags indicating exception is rationalization, not legitimate**:
- "Just this once" (it's never just once)
- "We'll add governance later" (later has 5% success rate)
- "Trust me, I've done this before" (past success ≠ future guarantee)
- Can't articulate specific criteria for when to upgrade governance

**Non-negotiable boundaries**:
- Customer-facing code: Minimum Level 2
- Financial transactions: Minimum Level 2
- Security-sensitive (PII, auth, payments): Minimum Level 2
- >3 month timeline: Minimum Level 2
- >5 developers: Minimum Level 3

**Example response**:
```
User: "We're a startup MVP, can we skip the ADRs?"

Agent: "I understand the pressure to move fast. Let's find the right balance:

Your MVP is customer-facing with payment processing → Level 2 minimum, not negotiable.

Level 2 = lightweight, not heavyweight:
- ADRs for high-risk decisions only (database, payment gateway, auth provider)
- 30-min risk session (identify risks, plan mitigation for top 3)
- Total overhead: ~2% of project time

This prevents the mistakes that kill MVPs:
- Wrong payment provider → costly migration mid-growth
- No auth security planning → breach before Series A
- Undocumented decisions → chaos when scaling team

ROI: 2 hours planning saves 20+ hours crisis firefighting.

Can we start with risk identification? 30 minutes now."
```

---

## Reference Sheets

The following reference sheets provide detailed methodologies for specific governance domains. Load them on-demand when needed.

### 1. Decision Analysis & Resolution (DAR)

**When to use**: Making architectural decisions, evaluating alternatives, documenting choices

→ See [dar-methodology.md](./dar-methodology.md)

**Covers**:
- When ADRs are mandatory vs optional
- ADR template and examples
- Decision criteria frameworks
- Alternatives analysis process
- Decision matrix tools
- Authority bias resistance

### 2. Risk Management (RSKM)

**When to use**: Identifying risks, assessing probability/impact, planning mitigation, monitoring risks

→ See [rskm-methodology.md](./rskm-methodology.md)

**Covers**:
- Risk identification techniques
- Probability × Impact matrix
- Risk mitigation strategies (avoid, transfer, mitigate, accept)
- Risk register template
- Monitoring and review cadence
- Risk triggers for ad-hoc reviews

### 3. Templates and Examples

**When to use**: Need concrete templates for ADRs or risk registers

→ See [templates.md](./templates.md)

**Covers**:
- ADR template (lightweight and comprehensive)
- Risk register format
- Decision matrix template
- Real-world examples

### 4. Level 2→3→4 Scaling

**When to use**: Understanding appropriate governance rigor for project tier

→ See [level-scaling.md](./level-scaling.md)

**Covers**:
- Level 2 baseline practices
- Level 3 organizational standards
- Level 4 quantitative management
- When to escalate or de-escalate rigor

---

## Common Mistakes

| Mistake | Why It Fails | Better Approach |
|---------|--------------|-----------------|
| "Obvious" decisions undocumented | Context loss in 6 months, assumptions not validated | Level 3: Document all architectural decisions, even "obvious" ones |
| Alternatives analysis after commitment | Analysis becomes validation theater | Evaluate alternatives BEFORE authority/consensus input |
| Risk acceptance without mitigation | Reactive firefighting costs 3-10x | Mitigation plan required for high-probability or high-impact risks |
| Set-and-forget risk planning | Risks evolve, complacency before late-stage crunch | Scheduled reviews based on project length |
| Deferring to authority without analysis | Authority bias, vendor relationships create blind spots | Independent analysis first, authority input second |
| Sunk cost justifies decision | Small sunk cost vs large future cost | Name the fallacy, calculate future cost |
| "We'll document later" | "Later" never comes (5% success rate) | Documentation = part of "done" |

---

## Integration with Other Skills

| When You're Doing | Also Use | For |
|-------------------|----------|-----|
| Creating ADRs | `design-and-build` | Technical decision criteria |
| Risk identification for security | `ordis-security-architect` | Security-specific risk techniques |
| Decision analysis with data | `quantitative-management` | Quantitative decision criteria |
| Requirements with risks | `requirements-lifecycle` | Risk-driven requirements prioritization |

---

## Real-World Impact

**Without this skill**: Teams experience:
- "Obvious" decisions become mysterious (context loss)
- Authority bias and groupthink (bad decisions)
- Reactive firefighting (3-10x cost)
- No risk mitigation (crisis mode when risks materialize)
- Documentation never happens ("later")

**With this skill**: Teams achieve:
- Documented decisions with rationale (knowledge retention)
- Independent alternatives analysis (better decisions)
- Proactive risk mitigation (prevent crisis)
- Ongoing risk monitoring (adapt to changing conditions)
- Governance as lightweight process (ROI-positive)

---

## Next Steps

1. **Determine project level**: Check CLAUDE.md or ask user for CMMI target level (default: Level 3)
2. **Identify situation**: Use Quick Reference table to find applicable framework
3. **Load reference sheet**: Read detailed methodology (DAR or RSKM)
4. **Enforce requirements**: Level 3 requires ADRs for all architectural decisions, risk mitigation for high risks
5. **Counter rationalizations**: Use anti-pattern catalog to address shortcuts
6. **Provide templates**: Lightweight ADR or risk register to reduce friction
7. **Calculate ROI**: Show cost comparison (30 min planning vs 10+ hours firefighting)

**Remember**: Proactive governance prevents costly reactive firefighting. Documentation and risk management are investments with 3-10x returns.
