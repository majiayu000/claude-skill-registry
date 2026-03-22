<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->
---
name: incident-management
description: >-
  End-to-end incident management lifecycle including classification frameworks,
  escalation procedures, root cause analysis, metrics tracking (MTTD/MTTR/MTTC),
  crisis communication, timeline reconstruction, lessons learned, severity matrices,
  stakeholder notification, documentation standards, war room coordination, and
  incident trend analysis aligned with NIST SP 800-61 and ISO 27035.
domain: cybersecurity
subdomain: incident-management
tags:
  - incident-response
  - incident-management
  - classification
  - escalation
  - root-cause-analysis
  - crisis-communication
  - severity-matrix
  - war-room
  - lessons-learned
  - metrics
  - nist-800-61
  - iso-27035
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["TA0001", "TA0002", "TA0003", "TA0005", "TA0010", "TA0040"]
  nist-csf: ["RS.RP-1", "RS.CO-1", "RS.AN-1", "RS.MI-1", "RS.IM-1", "RC.RP-1"]
  frameworks: ["NIST SP 800-61", "ISO 27035", "SANS PICERL", "ITIL Incident Management"]
---

# Incident Management

## When to Use

Activate when the operator asks about incident classification, escalation workflows,
root cause analysis, crisis communication, severity assessment, war room procedures,
stakeholder notification, incident documentation, metrics tracking, lessons learned,
or incident trend analysis.

Mode: `[MODE: INCIDENT]` primary; `[MODE: BLUE]` for detection-to-incident handoff;
`[MODE: ARCHITECT]` for process design.

## Quick Reference

| Task | Framework / Tool | Context |
|------|-----------------|---------|
| Classify incident | NIST 800-61 Category + Functional Impact | Triage |
| Assign severity | Severity matrix (S1–S4) | Triage |
| Escalation path | Tiered escalation with SLA timers | Response |
| Root cause analysis | 5 Whys, Ishikawa, Fault Tree | Post-incident |
| Timeline reconstruction | Log correlation + visual timeline | Investigation |
| Crisis communication | Templated stakeholder notifications | Communication |
| War room coordination | Structured roles + cadence | Active incident |
| Lessons learned | Blameless retrospective framework | Post-incident |
| Metrics tracking | MTTD, MTTR, MTTC, recurrence rate | Continuous |
| Trend analysis | Category/severity trends over time | Strategic |

## Workflow

### 1. Incident Lifecycle (NIST SP 800-61)

```
PREPARATION
├── Classification framework defined (category + severity)
├── Escalation procedures documented and tested
├── Communication templates ready
├── War room procedures established
└── Roles and responsibilities assigned

DETECTION & ANALYSIS
├── Alert triage → incident declaration
├── Severity assignment via matrix
├── Timeline reconstruction begins
├── Stakeholder notification per severity
└── Documentation starts immediately

CONTAINMENT, ERADICATION & RECOVERY
├── War room activated (S1/S2)
├── Containment strategy selected (short-term / long-term)
├── Eradication of threat actor presence
├── Recovery and service restoration
└── Continuous documentation and status updates

POST-INCIDENT ACTIVITY
├── Root cause analysis (5 Whys, Ishikawa)
├── Lessons learned / blameless retrospective
├── Metrics capture (MTTD, MTTR, MTTC)
├── Detection gap remediation
├── Trend analysis update
└── Process improvements implemented
```

### 2. Severity Matrix

| Severity | Impact | Examples | Response SLA |
|----------|--------|----------|-------------|
| **S1 — Critical** | Business-threatening, data breach, total service loss | Ransomware, active data exfil, prod down | 15 min response, 1 hr containment |
| **S2 — High** | Significant impact, partial service loss | Compromised admin account, partial outage | 30 min response, 4 hr containment |
| **S3 — Medium** | Limited impact, no data loss | Malware on single host, phishing success | 2 hr response, 24 hr resolution |
| **S4 — Low** | Minimal impact, policy violation | Failed brute force, policy exception | 8 hr response, 72 hr resolution |

### 3. Escalation Tiers

```
TIER 1 — SOC Analyst (0-15 min)
├── Initial triage and classification
├── Severity assignment
├── Stakeholder notification (S1/S2 immediate)
└── Escalate if: confirmed malicious, scope unclear, S1/S2

TIER 2 — Incident Lead (15-60 min)
├── Assume incident command
├── Activate war room (S1/S2)
├── Coordinate containment
└── Escalate if: business impact, legal/regulatory trigger

TIER 3 — CISO / Executive (as needed)
├── Business decisions (pay/don't pay, disclose/don't)
├── Regulatory notification authorization
├── External communication approval
└── Resource allocation
```

### 4. Metrics Framework

```
Operational Metrics:
├── MTTD: Mean Time to Detect — alert to declaration
├── MTTR: Mean Time to Respond — declaration to containment
├── MTTC: Mean Time to Close — declaration to resolution
├── MTTRE: Mean Time to Remediate — RCA finding to fix deployed
├── Recurrence Rate: incidents reopened / total incidents
└── Escalation Accuracy: correct severity at declaration

Process Metrics:
├── Documentation Completeness: required fields filled %
├── Lessons Learned Completion: retros held within SLA %
├── Action Item Closure Rate: retro actions completed on time %
└── Communication SLA: stakeholder updates sent within SLA %

Trend Metrics:
├── Incidents by category (monthly)
├── Incidents by severity (monthly)
├── Top 5 root causes (quarterly)
├── Repeat incident rate (quarterly)
└── Detection coverage improvement (quarterly)
```

### 5. Communication Templates

```
INITIAL NOTIFICATION (S1/S2):
Subject: [INCIDENT-{ID}] {Severity} — {Short Description}
Body:
  Status: ACTIVE
  Severity: {S1|S2|S3|S4}
  Impact: {description of business impact}
  Current Actions: {what is being done now}
  Next Update: {time of next scheduled update}
  Incident Commander: {name}
  War Room: {link/location}

STATUS UPDATE:
Subject: [INCIDENT-{ID}] UPDATE #{n} — {Status}
Body:
  Status: {ACTIVE|CONTAINED|ERADICATED|RESOLVED}
  Changes Since Last Update: {what changed}
  Current Actions: {what is being done now}
  Next Update: {time}

RESOLUTION NOTIFICATION:
Subject: [INCIDENT-{ID}] RESOLVED — {Short Description}
Body:
  Status: RESOLVED
  Duration: {total time from declaration to resolution}
  Root Cause: {brief summary}
  Impact Summary: {systems/users affected}
  Lessons Learned Review: {scheduled date}
```

## Techniques

| Technique | Description |
|-----------|------------|
| [implementing-incident-classification-framework](techniques/implementing-incident-classification-framework/) | Define category taxonomy and functional impact ratings |
| [building-incident-escalation-procedures](techniques/building-incident-escalation-procedures/) | Tiered escalation with SLA timers and decision trees |
| [performing-root-cause-analysis](techniques/performing-root-cause-analysis/) | 5 Whys, Ishikawa, and Fault Tree methods |
| [implementing-incident-metrics-tracking](techniques/implementing-incident-metrics-tracking/) | MTTD/MTTR/MTTC dashboards and KPIs |
| [building-crisis-communication-plans](techniques/building-crisis-communication-plans/) | Stakeholder templates and communication cadence |
| [performing-incident-timeline-reconstruction](techniques/performing-incident-timeline-reconstruction/) | Multi-source log correlation and visual timelines |
| [implementing-lessons-learned-processes](techniques/implementing-lessons-learned-processes/) | Blameless retrospective framework and action tracking |
| [building-incident-severity-matrices](techniques/building-incident-severity-matrices/) | Multi-factor severity scoring and SLA mapping |
| [performing-stakeholder-notification](techniques/performing-stakeholder-notification/) | Automated notification routing and regulatory compliance |
| [implementing-incident-documentation-standards](techniques/implementing-incident-documentation-standards/) | Structured templates and completeness validation |
| [building-war-room-procedures](techniques/building-war-room-procedures/) | Role assignments, cadence, and coordination protocols |
| [performing-incident-trend-analysis](techniques/performing-incident-trend-analysis/) | Statistical trend detection and forecasting |

## Verification

- [ ] Classification framework covers all NIST 800-61 categories
- [ ] Severity matrix validated with business stakeholders
- [ ] Escalation procedures tested via tabletop exercise
- [ ] Communication templates approved by legal and PR
- [ ] Metrics dashboard operational (MTTD, MTTR, MTTC)
- [ ] Lessons learned process running for all S1/S2 incidents
- [ ] War room procedures exercised quarterly
- [ ] Incident documentation completeness > 90%
- [ ] Trend analysis reviewed monthly by leadership
