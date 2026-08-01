---
name: managing-intelligence-lifecycle
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: managing-intelligence-lifecycle
description: >-
  Manage the complete cyber threat intelligence lifecycle from requirements
  definition through collection, processing, analysis, dissemination, and feedback.
domain: cybersecurity
subdomain: threat-intelligence
tags:
  - intelligence-lifecycle
  - cti-program
  - pir
  - intelligence-requirements
  - dissemination
  - tlp
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: []
---
# Managing Intelligence Lifecycle

## Overview

The intelligence lifecycle is the systematic process of converting raw data into
actionable intelligence through six phases: direction (requirements), collection,
processing, analysis, dissemination, and feedback. This skill covers establishing
Priority Intelligence Requirements (PIRs), building collection plans, processing
pipelines, analytic production standards, TLP-governed dissemination, and measuring
CTI program effectiveness.

## Prerequisites

- Understanding of organizational threat landscape and stakeholders
- MISP or OpenCTI for intelligence platform
- Familiarity with TLP, STIX/TAXII, and intelligence standards
- Python 3.10+ for automation tooling
- Knowledge of structured analytic techniques

```bash
pip install stix2 requests jinja2
```

## Key Concepts

### The Six Intelligence Phases

```
1. Direction     → Define PIRs, scope collection
2. Collection    → Gather data from sources (feeds, OSINT, HUMINT, sensors)
3. Processing    → Normalize, deduplicate, enrich raw data
4. Analysis      → Apply analytic techniques, produce assessments
5. Dissemination → Distribute to stakeholders via appropriate channels/TLP
6. Feedback      → Measure effectiveness, refine requirements
```

### Priority Intelligence Requirements (PIRs)

PIRs drive the entire lifecycle. They answer: *What does the organization need
to know to make security decisions?*

**PIR Categories:**
- **Strategic:** What threat actors target our sector? What's the 6-month threat trend?
- **Operational:** What campaigns are actively targeting our infrastructure?
- **Tactical:** What IOCs should our detection stack block this week?

**PIR Template:**
```
PIR-001: Which threat actors are currently targeting [sector] in [region]?
  Priority: HIGH
  Stakeholder: CISO, SOC Manager
  Collection Sources: ISAC feeds, vendor reports, dark web monitoring
  Update Frequency: Monthly
  Dissemination: TLP:AMBER — Executive threat brief
```

### Intelligence Products by Audience

| Product | Audience | Cadence | Content |
|---------|----------|---------|---------|
| Strategic Brief | C-suite, Board | Quarterly | Threat landscape, risk trends |
| Operational Report | SOC, IR Team | Weekly | Active campaigns, TTPs |
| Tactical Alert | SOC Analysts | Real-time | IOCs, detection rules |
| Threat Advisory | All Security | As needed | Vulnerability/campaign alerts |
| After-Action Report | IR, Management | Post-incident | Lessons learned, gaps |

### Confidence and Analytic Standards

All finished intelligence products must include:
- **Confidence level:** HIGH / MODERATE / LOW with criteria
- **Source reliability:** Admiralty scale (A-F for source, 1-6 for info)
- **Key assumptions:** Explicitly stated and challengeable
- **Alternative hypotheses:** At least one considered and documented
- **Limitations:** What the analysis cannot determine

## Workflow

### Step 1: Define Intelligence Requirements

```python
import json
from datetime import datetime

def create_pir(
    pir_id: str,
    question: str,
    priority: str,
    stakeholder: str,
    sources: list[str],
    cadence: str,
    tlp: str,
) -> dict:
    """Create a Priority Intelligence Requirement."""
    return {
        "pir_id": pir_id,
        "question": question,
        "priority": priority,
        "stakeholder": stakeholder,
        "collection_sources": sources,
        "update_cadence": cadence,
        "dissemination_tlp": tlp,
        "created": datetime.now().isoformat(),
        "status": "active",
        "last_answered": None,
    }

def create_collection_plan(pirs: list[dict]) -> dict:
    """Generate collection plan from PIRs."""
    sources_needed = set()
    for pir in pirs:
        sources_needed.update(pir["collection_sources"])

    return {
        "plan_id": f"CP-{datetime.now().strftime('%Y%m%d')}",
        "pir_count": len(pirs),
        "sources_required": sorted(sources_needed),
        "collection_tasks": [
            {"pir": p["pir_id"], "sources": p["collection_sources"],
             "cadence": p["update_cadence"], "priority": p["priority"]}
            for p in pirs
        ],
    }
```

### Step 2: Collection Management

```python
def track_collection(source: str, pir_id: str, data_collected: int) -> dict:
    """Track collection activity against PIR."""
    return {
        "source": source,
        "pir_id": pir_id,
        "timestamp": datetime.now().isoformat(),
        "data_collected": data_collected,
        "status": "collected",
    }

def assess_collection_gaps(pirs: list[dict], collection_log: list[dict]) -> dict:
    """Identify PIRs with insufficient collection."""
    answered_pirs = {c["pir_id"] for c in collection_log}
    gaps = [p for p in pirs if p["pir_id"] not in answered_pirs]
    return {
        "total_pirs": len(pirs),
        "answered": len(answered_pirs),
        "gaps": [{"pir_id": p["pir_id"], "question": p["question"]} for p in gaps],
    }
```

### Step 3: Analytic Production

```python
def create_intelligence_product(
    title: str,
    product_type: str,
    tlp: str,
    key_findings: list[str],
    confidence: str,
    recommendations: list[str],
    pir_addressed: list[str],
) -> dict:
    """Create structured intelligence product."""
    return {
        "title": title,
        "type": product_type,
        "tlp": tlp,
        "produced": datetime.now().isoformat(),
        "confidence": confidence,
        "key_findings": key_findings,
        "recommendations": recommendations,
        "pirs_addressed": pir_addressed,
        "key_assumptions": [],
        "alternative_hypotheses": [],
        "limitations": [],
    }
```

### Step 4: Dissemination Tracking

```python
def disseminate(product: dict, recipients: list[str], channel: str) -> dict:
    """Track dissemination of intelligence product."""
    return {
        "product_title": product["title"],
        "tlp": product["tlp"],
        "channel": channel,
        "recipients": recipients,
        "disseminated_at": datetime.now().isoformat(),
        "feedback_requested": True,
    }

def validate_tlp_compliance(product: dict, recipients: list[str]) -> dict:
    """Validate TLP marking matches recipient scope."""
    tlp = product["tlp"].upper()
    issues = []
    if tlp == "TLP:RED" and len(recipients) > 5:
        issues.append("TLP:RED should only go to named recipients")
    if tlp == "TLP:AMBER+STRICT" and any("external" in r for r in recipients):
        issues.append("TLP:AMBER+STRICT restricted to organization")
    return {"compliant": len(issues) == 0, "issues": issues}
```

### Step 5: Program Metrics and Feedback

```python
def calculate_program_metrics(
    pirs: list[dict],
    products: list[dict],
    feedback: list[dict],
) -> dict:
    """Calculate CTI program effectiveness metrics."""
    pirs_addressed = set()
    for p in products:
        pirs_addressed.update(p.get("pirs_addressed", []))

    positive_feedback = sum(1 for f in feedback if f.get("useful", False))

    return {
        "metrics_period": datetime.now().strftime("%Y-Q%q" if False else "%Y-%m"),
        "pir_coverage": f"{len(pirs_addressed)}/{len(pirs)}",
        "products_produced": len(products),
        "stakeholder_satisfaction": (
            round(positive_feedback / max(len(feedback), 1) * 100, 1)
        ),
        "mean_time_to_produce_hours": 0,  # Calculate from timestamps
        "feedback_count": len(feedback),
        "recommendations": [
            "Review unanswered PIRs for collection gaps",
            "Survey stakeholders on product relevance",
            "Track time-to-detection for tactical IOCs",
        ],
    }
```

## Verification

- [ ] PIRs documented with priority, stakeholder, and collection sources
- [ ] Collection plan maps sources to PIRs with update cadence
- [ ] Intelligence products include confidence, assumptions, and alternatives
- [ ] TLP markings validated against recipient scope
- [ ] Dissemination tracked with feedback mechanism
- [ ] Program metrics calculated and reported quarterly

## References

- [NIST SP 800-150: Guide to CTI Sharing](https://csrc.nist.gov/publications/detail/sp/800-150/final)
- [Traffic Light Protocol (TLP)](https://www.first.org/tlp/)
- [Intelligence Cycle (CIA)](https://www.cia.gov/static/9a5f1162fd0932c29e985f0159f56ec1/Tradecraft-Primer-apr09.pdf)
- [MISP Project](https://www.misp-project.org/)
- [OpenCTI Documentation](https://docs.opencti.io/)
