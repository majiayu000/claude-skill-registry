---
name: Escalation and Ownership
description: Defining clear ownership models and escalation procedures to ensure incidents are handled by the right people at the right time.
---

# Escalation and Ownership

## Overview

Escalation and Ownership defines who is responsible for incident response at each stage and when to escalate to more senior or specialized personnel. Clear ownership prevents incidents from falling through the cracks and ensures efficient resolution.

**Core Principle**: "Every incident must have an owner. Escalation is not failure—it's smart resource allocation."

---

## 1. The Ownership Model

### Primary On-Call (L1)
- **Responsibility**: First responder, initial triage
- **Authority**: Can page L2, declare SEV2+
- **Typical Role**: Mid-level engineer familiar with the system

### Secondary On-Call (L2)
- **Responsibility**: Subject matter expert, complex debugging
- **Authority**: Can page L3, escalate to SEV1
- **Typical Role**: Senior engineer, team lead

### Escalation Engineer (L3)
- **Responsibility**: Cross-team coordination, architectural decisions
- **Authority**: Can page executives, declare SEV0
- **Typical Role**: Staff/Principal engineer, architect

### Executive On-Call (L4)
- **Responsibility**: Business decisions, customer communication
- **Authority**: Final authority on trade-offs
- **Typical Role**: VP Engineering, CTO

---

## 2. When to Escalate

### Time-Based Escalation
```
SEV0: Escalate immediately to L2 + L3
SEV1: Escalate to L2 after 15 minutes if no progress
SEV2: Escalate to L2 after 30 minutes if no progress
SEV3: Escalate to L2 after 2 hours if no progress
```

### Complexity-Based Escalation
Escalate immediately if:
- Root cause involves multiple services
- Requires database schema changes
- Needs vendor support (AWS, GCP)
- Involves security breach or data loss
- Affects enterprise/VIP customers

### Skill-Based Escalation
```
Issue Type → Escalate To
─────────────────────────────
Database performance → DBA team
Network/DNS → Infrastructure team
Payment failures → Payments team
Security alert → Security team
```

---

## 3. The RACI Matrix for Incidents

| Activity | L1 On-Call | L2 SME | L3 Architect | Incident Commander | Exec |
|----------|------------|--------|--------------|-------------------|------|
| **Initial triage** | R | C | I | A | I |
| **Technical investigation** | R | R/A | C | I | I |
| **Escalation decision** | R | A | C | C | I |
| **Customer communication** | I | I | C | R | A |
| **Postmortem** | C | R | C | A | I |

**R**esponsible, **A**ccountable, **C**onsulted, **I**nformed

---

## 4. Escalation Procedures

### Step 1: Assess Severity
Use the severity matrix (see `severity-levels` skill) to determine if escalation is needed.

### Step 2: Notify Next Level
```bash
# PagerDuty CLI example
pd incident escalate INC-123 --level 2 --reason "Database deadlock requires DBA expertise"
```

### Step 3: Provide Context
When escalating, always include:
- Incident ID and severity
- What you've tried so far
- Current hypothesis
- Why you're escalating (time/complexity/skill)

### Step 4: Transfer Ownership
```markdown
**Escalation Handoff**

From: @alice (L1)
To: @bob (L2 - Database SME)

**Summary**: Payment API returning 500s
**Root Cause Hypothesis**: Connection pool exhaustion
**Attempted**: Restarted app servers (no effect)
**Current State**: 50% of payment requests failing
**Logs**: [link]
**Metrics**: [dashboard link]

@bob you have ownership. Let me know how I can assist.
```

---

## 5. The Incident Commander Role

For SEV0/1 incidents, assign a dedicated **Incident Commander** (IC).

### IC Responsibilities
- **Coordinate**: Manage the war room, assign tasks
- **Communicate**: Update stakeholders, run status calls
- **Decide**: Make trade-off decisions (rollback vs. forward fix)
- **Document**: Ensure timeline is captured
- **Protect**: Shield responders from distractions

### IC is NOT
- The person fixing the issue (that's the technical lead)
- The most senior person (it's a role, not a rank)
- Responsible for the root cause (they coordinate, not code)

---

## 6. On-Call Rotation Best Practices

### Rotation Schedule
```
Week 1: Alice (Primary), Bob (Secondary)
Week 2: Bob (Primary), Carol (Secondary)
Week 3: Carol (Primary), Alice (Secondary)
```

### Handoff Checklist
- [ ] Review open incidents from previous week
- [ ] Check for scheduled maintenance windows
- [ ] Verify PagerDuty/Opsgenie is configured correctly
- [ ] Review recent postmortems for new failure modes
- [ ] Test pager (send test alert)

### On-Call Compensation
- **Follow the Sun**: Distribute on-call across time zones
- **Compensation**: Pay on-call stipend + overtime for pages
- **Recovery Time**: Day off after a SEV0 overnight incident

---

## 7. Escalation Antipatterns

### ❌ The "Hero" Pattern
One person tries to solve everything alone instead of escalating.
**Fix**: Make escalation a positive action, not a sign of weakness.

### ❌ The "Hot Potato"
Passing the incident around without clear ownership transfer.
**Fix**: Use explicit handoff messages with acknowledgment.

### ❌ The "Escalation Spam"
Paging everyone immediately without attempting L1 triage.
**Fix**: Follow the escalation ladder; respect the on-call rotation.

### ❌ The "Silent Escalation"
Escalating without context or documentation.
**Fix**: Always provide a handoff summary.

---

## 8. Vendor Escalation

### AWS Support
```
Severity 1 (Critical): < 1 hour response
Severity 2 (Urgent): < 4 hours response
Severity 3 (Normal): < 12 hours response

Escalation: Open case via AWS Console or CLI
aws support create-case --subject "RDS outage" --severity urgent
```

### GCP Support
```
P1 (Critical): 15-minute response (Premium Support)
P2 (High): 4-hour response
P3 (Medium): 8-hour response

Escalation: Cloud Console → Support → Create Case
```

### Third-Party SaaS (Stripe, Twilio, etc.)
- Check status page first: status.stripe.com
- Use dedicated support channel for enterprise customers
- Escalate via account manager for critical issues

---

## 9. Ownership Documentation

### Service Ownership Registry
```yaml
# services.yaml
payment-api:
  owner: payments-team
  primary_oncall: "@payments-oncall"
  escalation_path:
    - L1: "@payments-oncall"
    - L2: "@payments-lead"
    - L3: "@platform-architect"
  runbook: "https://wiki/payments-api-runbook"
  slack_channel: "#team-payments"
```

### CODEOWNERS (GitHub)
```
# Automatically request reviews and assign ownership
/services/payment-api/ @payments-team
/services/auth/ @security-team
/infrastructure/ @platform-team
```

---

## 10. Escalation and Ownership Checklist

- [ ] **Clear Ladder**: Is the L1 → L2 → L3 escalation path documented?
- [ ] **Response SLAs**: Do we have defined response times for each level?
- [ ] **Handoff Protocol**: Do we use a standard template for ownership transfer?
- [ ] **IC Training**: Have we trained multiple people to be Incident Commanders?
- [ ] **Vendor Contacts**: Do we have escalation contacts for all critical vendors?
- [ ] **Service Registry**: Is every service mapped to an owning team?
- [ ] **Rotation Health**: Is on-call load balanced (no one person > 50% of pages)?

---

## Related Skills
- `41-incident-management/escalation-paths`
- `41-incident-management/severity-levels`
- `41-incident-management/incident-triage`
