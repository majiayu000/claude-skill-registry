<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: engagement-pipeline
description: >-
  Structured security engagement methodology with 5 stages (Scope, Recon, Assess,
  Exploit, Report) and quality gates at each transition. Includes templates for
  Rules of Engagement, engagement reports, IR runbooks, and threat models. Use
  when starting any security engagement, penetration test, red team operation,
  vulnerability assessment, or architecture review.
domain: cybersecurity
subdomain: engagement-methodology
tags:
  - engagement-pipeline
  - penetration-testing
  - methodology
  - quality-gates
  - rules-of-engagement
  - reporting
  - threat-model
  - ir-runbook
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  frameworks: ["PTES", "OWASP Testing Guide", "NIST SP 800-115", "CREST"]
---

# Engagement Pipeline

## When to Use

Activate when the operator starts a security engagement, penetration test, red team
operation, vulnerability assessment, architecture review, or incident response.
This skill provides the overarching methodology — individual technical skills
(web, AD, cloud, etc.) are loaded as needed within each stage.

Mode: Inherits from engagement type. Pipeline methodology is mode-agnostic.

## Pipeline Stages

| Stage | Gate | Purpose |
|-------|------|---------|
| 1. SCOPE | Gate 1: Scope Approval | Define boundaries, get authorization |
| 2. RECON | Gate 2: Recon Complete | Map attack surface |
| 3. ASSESS | Gate 3: Assessment Complete | Identify vulnerabilities |
| 4. EXPLOIT | Gate 4: Exploitation Complete | Prove impact |
| 5. REPORT | Gate 5: Report Delivered | Actionable deliverables |

See `pipeline/PIPELINE.md` for full methodology.

## Templates

| Template | Location | Purpose |
|----------|----------|---------|
| Rules of Engagement | `pipeline/templates/rules-of-engagement.md` | Engagement authorization |
| Engagement Report | `pipeline/templates/engagement-report.md` | Final deliverable |
| IR Runbook | `pipeline/templates/ir-runbook.md` | Incident response procedure |
| Threat Model | `pipeline/templates/threat-model.md` | STRIDE/DREAD analysis |

## Gate Validation

Read `pipeline/gates/gate-definitions.json` for machine-readable gate checks.

At each gate transition, validate all required checks pass before proceeding:
- **CONTINUE** — Gate passed, proceed
- **PIVOT** — Findings warrant scope change (get approval)
- **PAUSE** — Blocked on dependency
- **ESCALATE** — Critical finding, notify immediately
- **ABORT** — Safety or legal concern

## Quick Start

1. Determine engagement type (pentest, red team, vuln assessment, arch review)
2. Read `pipeline/templates/rules-of-engagement.md` — fill with client
3. Pass Gate 1 (signed RoE)
4. Follow stage sequence for engagement type
5. At each gate, validate checks before proceeding
6. Produce final report using `pipeline/templates/engagement-report.md`



### Example: Engagement Initialization

```bash
# Start a new engagement
/cipher:engage

# Select type: pentest | red-team | vuln-assessment | arch-review | ir | threat-model
# Pipeline auto-creates .cipher/ENGAGEMENT.md

# Resume an engagement
/cipher:resume  # Shows current phase, findings, next actions

# Export final report
/cipher:export  # Generates formatted security report
```

### Example: Gate Decision

```yaml
# Gate G2 (Recon → Assess) decision criteria:
gate: G2
checks:
  - asset_inventory_complete: true
  - scope_validated: true
  - attack_surface_mapped: true
  - passive_recon_done: true
decision: CONTINUE  # or PIVOT, PAUSE, ESCALATE, ABORT
```


## Verification

- [ ] Engagement type selected and stages identified
- [ ] RoE signed before any testing begins
- [ ] Each stage gate validated before transition
- [ ] All findings documented in standard format
- [ ] Report delivered securely with debrief scheduled
