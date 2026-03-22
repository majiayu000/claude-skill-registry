<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: implementing-soc-automation-workflows
description: >-
  SOAR playbook development and automation workflow implementation for SOC
  operations including automated enrichment, containment actions, notification
  routing, ticket creation, IOC blocking, and response orchestration across
  Splunk SOAR, Cortex XSOAR, and Microsoft Sentinel Logic Apps.
domain: cybersecurity
subdomain: soc-operations
tags:
  - soc-automation
  - soar
  - playbook
  - orchestration
  - splunk-soar
  - xsoar
  - sentinel
  - workflow
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: []
---

# Implementing SOC Automation Workflows

## Overview

SOC automation accelerates response by executing repetitive analyst tasks
programmatically. Well-designed playbooks handle enrichment, triage decisions,
containment actions, and notification routing without human intervention for
known-good patterns, freeing analysts for complex investigations. This skill
covers SOAR playbook design patterns across major platforms.

## Prerequisites

| Requirement | Purpose |
|---|---|
| SOAR platform (Splunk SOAR/XSOAR/Sentinel) | Automation execution |
| SIEM integration configured | Alert ingestion triggers |
| API credentials for enrichment services | Automated lookups |
| Containment tool integration (EDR/FW) | Automated response |

## Key Concepts

### Automation Tiers

```
SOC AUTOMATION MATURITY:
├── Tier 0 — Notification Only
│   Alert → Format → Notify analyst via Slack/Teams/PagerDuty
│   Risk: None (no automated actions)
├── Tier 1 — Automated Enrichment
│   Alert → Enrich IOCs (VT, WHOIS, CMDB) → Attach to case
│   Risk: Low (read-only operations)
├── Tier 2 — Decision Support
│   Alert → Enrich → Score → Recommend action → Await approval
│   Risk: Low (human approval gate)
├── Tier 3 — Automated Containment
│   Alert + High Confidence → Isolate host / Block IP / Disable account
│   Risk: Medium (automated impact, rollback required)
└── Tier 4 — Full Auto-Response
    Alert → Enrich → Decide → Contain → Ticket → Close
    Risk: High (no human in loop, extensive testing required)
```

### Splunk SOAR Playbook Pattern

```python
# Enrichment playbook (Splunk SOAR / Phantom)
import phantom.rules as phantom

def on_start(container):
    # Extract IP artifacts
    artifacts = phantom.collect2(
        container=container,
        datapath=["artifact:*.cef.sourceAddress"],
        action_results=None)
    for artifact in artifacts:
        ip = artifact[0]
        if ip:
            phantom.act("ip reputation", parameters=[{"ip": ip}],
                        assets=["virustotal"], callback=enrich_complete)

def enrich_complete(action_results, **kwargs):
    for result in action_results:
        summary = result.get_summary()
        if summary.get("malicious", 0) > 5:
            phantom.act("block ip", parameters=[{"ip": result["ip"]}],
                        assets=["firewall"])
            phantom.set_severity(container, "high")
```

### Cortex XSOAR Playbook YAML

```yaml
# Phishing triage automation
id: phishing-auto-triage
name: Phishing Auto-Triage
starttaskid: "0"
tasks:
  "0":
    id: "0"
    taskid: extract-indicators
    type: regular
    task:
      name: Extract Indicators
      script: ExtractIndicatorsFromEmailBody
  "1":
    id: "1"
    taskid: enrich-urls
    type: playbook
    task:
      name: URL Enrichment
      playbookName: URL Enrichment - Generic v2
  "2":
    id: "2"
    taskid: check-verdict
    type: condition
    task:
      name: Is Malicious?
    conditions:
      - label: "yes"
        condition:
          - - operator: isEqualNumber
              left: DBotScore.Score
              right: {value: 3}
      - label: "no"
```

### Sentinel Logic App Automation

```json
{
  "definition": {
    "triggers": {
      "Microsoft_Sentinel_incident": {
        "type": "ApiConnectionNotification",
        "inputs": {
          "host": {"connection": {"name": "@parameters('$connections')['azuresentinel']['connectionId']"}},
          "body": {"callback_url": "@{listCallbackUrl()}"}
        }
      }
    },
    "actions": {
      "Enrich_IPs": {
        "type": "Http",
        "inputs": {
          "method": "GET",
          "uri": "https://www.virustotal.com/api/v3/ip_addresses/@{triggerBody()?['object']?['properties']?['relatedEntities'][0]?['properties']?['address']}"
        }
      },
      "Update_Incident": {
        "type": "ApiConnection",
        "inputs": {
          "body": {"severity": "High", "status": "Active"}
        }
      }
    }
  }
}
```

### Automation Guard Rails

```
SAFETY REQUIREMENTS:
  □ All containment playbooks have rollback procedures
  □ High-impact actions require approval gate (Tier 2+)
  □ Rate limiting on automated blocking actions
  □ Allowlist of critical assets excluded from auto-containment
  □ Audit trail for every automated action
  □ Circuit breaker: pause automation if error rate > threshold
  □ Testing in simulation mode before production deployment
```

## Workflow

1. **Identify** — Select high-volume, repetitive analyst tasks for automation
2. **Design** — Map playbook logic with decision trees and approval gates
3. **Build** — Implement in SOAR platform with error handling
4. **Test** — Validate with synthetic events in staging environment
5. **Deploy** — Enable in production with monitoring and alerting
6. **Monitor** — Track execution success rate and mean execution time
7. **Iterate** — Refine based on analyst feedback and edge cases

## Verification

| Check | Method |
|---|---|
| Playbook triggers correctly | Test with known alert patterns |
| Enrichment data accurate | Compare automated vs. manual enrichment |
| Containment actions reversible | Execute and verify rollback procedure |
| Approval gates functional | Verify human-in-loop for Tier 2+ |
| Audit trail complete | Review action log for full traceability |
