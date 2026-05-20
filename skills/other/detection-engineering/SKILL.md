<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: detection-engineering
description: >-
  Detection engineering lifecycle management including detection-as-code
  frameworks, Sigma rule development, coverage analysis, behavioral detection
  models, testing frameworks, false positive analysis, log parsers, lifecycle
  management, gap remediation, threat-informed detections, metrics tracking,
  and rule optimization.
domain: cybersecurity
subdomain: detection-engineering
tags:
  - detection-as-code
  - sigma-rules
  - detection-coverage
  - behavioral-detection
  - detection-testing
  - false-positive-analysis
  - log-parsers
  - detection-lifecycle
  - gap-remediation
  - threat-informed
  - detection-metrics
  - rule-optimization
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack:
    - T1059
    - T1003
    - T1053
    - T1055
    - T1021
    - T1078
  nist-csf:
    - DE.AE-2
    - DE.AE-3
    - DE.CM-1
    - DE.CM-4
    - DE.DP-1
  frameworks:
    - "Sigma"
    - "MITRE ATT&CK"
    - "DeTT&CT"
---

# SKILL: Detection Engineering

## When to Use

Activate this skill when the operator asks about:
- **Detection-as-code** — CI/CD pipelines for detection rules, version control, automated testing
- **Sigma rule development** — Writing, validating, and converting cross-SIEM detection rules
- **Coverage analysis** — Mapping detection coverage to ATT&CK matrix, identifying blind spots
- **Behavioral detection** — Building models for anomaly detection beyond signature matching
- **Testing frameworks** — Atomic Red Team, MITRE Caldera, detection validation
- **False positive analysis** — Systematic FP investigation, tuning, and documentation
- **Log parsers** — Custom parsing for non-standard log sources
- **Lifecycle management** — Detection rule states, ownership, review cadence, retirement
- **Gap remediation** — Prioritized detection gap closure using threat intelligence
- **Threat-informed detections** — Building detections from CTI reports and adversary emulation
- **Metrics tracking** — Detection efficacy, coverage, quality, and operational metrics
- **Rule optimization** — Performance tuning, query efficiency, resource reduction

## Prerequisites

| Requirement | Purpose |
|---|---|
| Sigma CLI | Rule validation and conversion (`pip install sigma-cli`) |
| Git | Version control for detection-as-code workflows |
| SIEM Platform | Splunk, Elastic, or Microsoft Sentinel for deployment |
| Atomic Red Team | Detection validation and testing framework |
| DeTT&CT | ATT&CK coverage visualization and gap analysis |

## Quick Reference

### Detection Rule Lifecycle

```yaml
title: Suspicious Process Spawned by Office Application
id: 5e1c0d42-8a3f-4b2e-9c7d-1f6e8a3b4c5d
status: experimental
logsource:
  category: process_creation
  product: windows
detection:
  selection_parent:
    ParentImage|endswith:
      - '\\winword.exe'
      - '\\excel.exe'
  selection_child:
    Image|endswith:
      - '\\cmd.exe'
      - '\\powershell.exe'
  condition: selection_parent and selection_child
level: high
tags:
  - attack.execution
  - attack.t1059.001
```

| Task | Detail |
|---|---|
| Validate Sigma rule | `sigma check rules/rule.yml` |
| Convert to Splunk | `sigma convert -t splunk -p splunk_cim rule.yml` |
| Convert to Elastic | `sigma convert -t elasticsearch -p ecs_windows rule.yml` |
| Run Atomic test | `Invoke-AtomicTest T1059.001 -GetPrereqs` |
| DeTT&CT coverage | `python dettect.py -ft techniques.yaml` |
| Batch validate | `find rules/ -name '*.yml' -exec sigma check {} \;` |

## Workflow

### 1. Detection Development

Author detection rules using detection-as-code principles. Version control,
peer review, automated validation, and CI/CD deployment to SIEM platforms.

→ **Deep reference:** [references/detection-development.md](references/detection-development.md)
  - Detection-as-code pipeline architecture
  - Sigma rule authoring best practices
  - CI/CD integration for detection deployment
  - Rule quality scoring and review checklist

### 2. Coverage Analysis & Gap Remediation

Map current detection coverage to MITRE ATT&CK matrix. Identify gaps using
DeTT&CT and prioritize based on threat intelligence relevance.

→ **Deep reference:** [references/coverage-analysis.md](references/coverage-analysis.md)
  - ATT&CK coverage heatmap generation
  - DeTT&CT configuration and scoring
  - Gap prioritization using CTI
  - Coverage improvement tracking

### 3. Testing & Optimization

Validate detections using adversary emulation, tune for false positives,
and optimize query performance for production SIEM workloads.

→ **Deep reference:** [references/testing-optimization.md](references/testing-optimization.md)
  - Atomic Red Team integration
  - False positive investigation workflow
  - Query performance optimization
  - Detection efficacy measurement

## Verification

| Check | Method |
|---|---|
| Rules pass validation | `sigma check` returns exit 0 for all rules |
| Coverage mapped | DeTT&CT heatmap generated with current scores |
| Tests executed | Atomic Red Team validates detection triggers |
| FP rate documented | Each rule has measured FP rate below threshold |
| Metrics dashboard live | Detection KPIs tracked with automated collection |
| Lifecycle enforced | All rules have owner, review date, and status |

## References

- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [ISO 27001:2022](https://www.iso.org/standard/27001)
- [CIS Controls v8](https://www.cisecurity.org/controls)

---
v1.0 | Validated: 2026-03-18
