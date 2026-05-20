---
name: reliability-engineering-cloud
description: Reliability engineering for cloud systems — SLIs, SLOs, error budgets, SRE practices, runbooks, incident response, on-call rotation, blameless postmortems, chaos engineering, and the NASA Systems Engineering methodology (MCR/SRR/PDR/CDR/ORR phase gates, TAID verification, requirements tracing) adapted to cloud operations. Use when establishing SLOs for a new service, running an incident, writing a runbook, preparing a launch readiness review, or bringing NASA SE discipline to cloud deployments.
type: skill
category: cloud-systems
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/cloud-systems/reliability-engineering-cloud/SKILL.md
superseded_by: null
---
# Reliability Engineering for Cloud

Reliability is a property of a system, not of any individual component. A cloud service that meets its availability target is not necessarily built from components that individually meet their target — it is built from a system that absorbs component failures without exposing them to users. This skill covers the SRE toolkit (SLIs, SLOs, error budgets, runbooks, postmortems, chaos engineering) alongside NASA's Systems Engineering methodology for design reviews and verification, because cloud operations at serious scale have to borrow discipline from somewhere, and aerospace is the field that has been figuring this out the longest.

**Agent affinity:** gray (transaction processing reliability, ACID foundations), hamilton-cloud (SRE economics at AWS scale), lamport (formal safety arguments)

**Concept IDs:** cloud-se-phase-reviews, cloud-taid-verification, cloud-runbook-structure, cloud-procedure-execution, cloud-communication-loops

## Service Level Indicators, Objectives, and Agreements

**SLI (Service Level Indicator).** A quantitative measure of some aspect of service behavior. Examples: fraction of requests that succeed, fraction of requests served in under 200 ms, bytes delivered, freshness of returned data.

**SLO (Service Level Objective).** A target for an SLI over a window. "99.9% of requests succeed over a 30-day window." SLOs are set internally by the team that operates the service.

**SLA (Service Level Agreement).** A contractual commitment, typically looser than the SLO, with financial consequences for violation. SLAs are customer-facing; SLOs are the internal discipline that prevents you from ever needing to pay out on an SLA.

### Choosing SLIs

Good SLIs are:

- **User-centric.** Measure what users experience, not internal plumbing.
- **Ratio-based.** Expressed as "good events / total events" so they are interpretable across traffic levels.
- **Implementable.** Can be measured from existing data without instrumenting every code path.

Typical SLIs for a request/response service:

- Availability: fraction of non-5xx responses.
- Latency: fraction of responses under X ms.
- Quality: fraction of responses returning full results (not degraded).

## Error Budgets

The error budget is the inverse of the SLO. If the SLO is 99.9% availability, the error budget is 0.1% — about 43 minutes per month of downtime.

Error budgets are the unit of negotiation between "ship features" and "improve reliability." When the error budget is being spent faster than planned, the response is to slow feature velocity and address reliability. When the error budget is being preserved, new features and risk-taking are encouraged. This removes the "SRE says no, developers say yes" political argument and replaces it with a shared metric.

**Burn rate alerting.** Alert when the error budget is being consumed faster than the window allows. A 2% burn over 1 hour (30 days of error budget consumed in 24 hours) is worth paging; a 0.1% burn over a week is worth a ticket.

## Runbooks

A runbook is an executable procedure for a specific operational task: deploying a service, recovering from a known failure mode, running a database migration, rotating a credential. Good runbooks share structure:

1. **Title and scope.** What this runbook does and does not cover.
2. **Prerequisites.** State required before execution (access, data, approvals).
3. **Steps.** Each step has an action, an expected output, a verification check, and a timeout.
4. **Rollback.** What to do if the procedure fails partway.
5. **Escalation.** Who to contact when the runbook doesn't match the situation.
6. **Last reviewed.** Date and reviewer.

Runbooks that are out of date are worse than missing runbooks — they give false confidence. Schedule reviews.

### Procedure Step Discipline

Every step is a contract: "if I do this, I expect to see that, within this time." When the observed result differs, the operator stops and escalates rather than continuing on autopilot. This is borrowed from aviation crew resource management and nuclear plant operations — fields where continuing on a procedure mismatch is what causes accidents.

## Incident Response

An incident is an unplanned disruption that requires coordinated response. Structure:

**Detection.** Monitoring fires an alert. Ideal: alert fires before users notice. Acceptable: alert fires within seconds of the first user complaint.

**Triage.** Incident commander (IC) is designated. Severity is assessed. Initial scope is determined (which users, which regions, which services).

**Mitigation.** Stop the bleeding. Roll back the last change. Drain traffic from the affected region. Fail over to a backup. Mitigation is not a fix — it is a restoration of service so that the fix can be done calmly.

**Resolution.** The underlying cause is addressed and the system is returned to normal operation.

**Postmortem.** A blameless write-up of what happened, why, and what to do differently.

### The Incident Commander Role

The IC does not fix the incident. The IC coordinates: assigns tasks, tracks who is doing what, communicates with stakeholders, decides when to declare the incident resolved. Without an IC, everyone tries to fix things simultaneously, communication breaks down, and mitigation takes hours longer than it should.

## Blameless Postmortems

A postmortem is a report on an incident. It should answer:

- What happened? (Timeline of events.)
- What was the impact?
- What went well?
- What went poorly?
- Where did we get lucky?
- What are the action items, with owners and due dates?

"Blameless" means the narrative avoids assigning fault to individuals. The goal is not "Alice shouldn't have deployed on Friday" — the goal is "our deploy system should have caught this regression." People who fear blame hide their mistakes, and hidden mistakes are the ones that kill systems.

## Chaos Engineering

Chaos engineering is the discipline of testing the system by deliberately introducing failures. Not to break things, but to verify that the designed-in resilience actually works.

**Principles.**

1. Build a hypothesis about steady-state behavior ("the service stays available when one replica is killed").
2. Vary real-world events (kill a replica, introduce latency, drop packets).
3. Run in production ideally, or in a staging environment that is representative.
4. Automate and run continuously.
5. Minimize blast radius.

Tools: Netflix Chaos Monkey (kill random instances), Chaos Kong (kill regions), Gremlin, Chaos Mesh.

## NASA Systems Engineering Phase Gates

NASA's Systems Engineering Handbook defines a lifecycle from Pre-Phase A (concept exploration) through Phase F (decommissioning), with formal reviews at phase transitions:

- **MCR** — Mission Concept Review. Is the mission needed? Feasible?
- **SRR** — System Requirements Review. Are the requirements complete and achievable?
- **SDR** — System Definition Review. Is the architecture defined to satisfy the requirements?
- **PDR** — Preliminary Design Review. Does the preliminary design meet the requirements?
- **CDR** — Critical Design Review. Is the detailed design ready for fabrication?
- **SIR** — System Integration Review. Are integration plans ready?
- **ORR** — Operational Readiness Review. Is the operations team ready to run the system?
- **FRR** — Flight Readiness Review. (Aerospace-specific; cloud analog: "go-live review.")

Each review has entrance criteria (you can't hold the review until X is true) and exit criteria (the review isn't closed until Y is agreed).

### Mapping to Cloud

Not every cloud deployment needs all eight reviews. A new microservice might need MCR-lite (design doc), SRR-lite (requirements review), CDR-lite (code review), and ORR (runbook and on-call review). A new multi-region rollout with customer SLAs probably deserves the full set, adapted for cloud terminology. The point is not ceremony — it is that you cannot review what you have not defined, and forcing the definition gets bugs out of the design before they become expensive.

## TAID Verification

NASA classifies verification methods by how the requirement is checked:

- **T — Test.** Run the system and observe. (Unit tests, integration tests, load tests, failover drills.)
- **A — Analysis.** Prove by calculation, simulation, or model-checking. (Capacity modeling, reliability analysis, TLA+ spec check.)
- **I — Inspection.** Review an artifact against a checklist. (Code review, configuration audit, documentation review.)
- **D — Demonstration.** Show the system behaving correctly in front of witnesses. (Go-live rehearsal, chaos drill, red-team exercise.)

Every requirement should have a declared verification method. A requirement without a verification method is a wish.

## Requirements Tracing

A requirement trace matrix links each requirement to (a) the design element that satisfies it, (b) the verification activity that validates it, and (c) the evidence that the verification passed. Tracing prevents requirements from slipping through the cracks and makes it explicit when something is being changed without covering the old requirements.

## When to Use This Skill

- Establishing SLOs and error budgets for a new service.
- Running an incident as commander or participant.
- Writing or reviewing a runbook.
- Preparing for a launch readiness review.
- Bringing NASA SE discipline to a cloud deployment with strict availability requirements.
- Writing a postmortem.
- Planning a chaos engineering program.

## When NOT to Use This Skill

- Early-stage prototyping where reliability is not yet the binding constraint.
- One-off scripts or tools where operational discipline is not worth the overhead.

## Decision Guidance

| Situation | Approach |
|---|---|
| New service, unknown reliability needs | Start with a loose SLO (99%), tighten as you learn |
| Critical service with customer SLA | SLO tighter than SLA by at least 10x in error budget |
| Frequent small incidents | Fix detection and process, not heroic mitigation |
| Rare large incidents | Invest in runbooks and drills, not engineering |
| New production deployment | Lightweight ORR mandatory |
| Multi-region critical system | Full phase gate review suite, chaos drills |

## References

- Beyer, B., et al. (2016). *Site Reliability Engineering*. O'Reilly.
- Beyer, B., et al. (2018). *The Site Reliability Workbook*. O'Reilly.
- NASA SP-2016-6105 Rev 2. *NASA Systems Engineering Handbook*.
- NASA NPR 7123.1. "NASA Systems Engineering Processes and Requirements."
- Allspaw, J. (2012). "Blameless PostMortems and a Just Culture." Etsy Code as Craft.
- Basiri, A., et al. (2016). "Chaos Engineering." IEEE Software 33(3).
- Dekker, S. (2014). *The Field Guide to Understanding Human Error*. Ashgate.
