---
name: full-triage-alert
description: "Complete Tier 1 triage workflow. Orchestrates the full alert triage process: check-duplicates, triage-alert, enrich-ioc for each entity, and either close (FP/BTP) or escalate (TP/Suspicious). Use for end-to-end alert processing."
type: workflow
orchestrates:
  - check-duplicates
  - triage-alert
  - enrich-ioc
  - document-in-case
  - close-case-artifact
required_roles:
  chronicle: roles/chronicle.viewer
  soar: roles/chronicle.editor
  gti: GTI Standard
personas: [tier1-analyst]
---

# Full Alert Triage Workflow

A composite skill that orchestrates the complete Tier 1 alert triage process from initial receipt to disposition (close or escalate).

## Inputs

- `CASE_ID` or `ALERT_ID` - The alert/case to triage (required)

## Orchestrated Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FULL ALERT TRIAGE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START                                                          │
│    │                                                            │
│    ▼                                                            │
│  ┌─────────────────────┐                                        │
│  │  /check-duplicates  │                                        │
│  └──────────┬──────────┘                                        │
│             │                                                   │
│     ┌───────┴───────┐                                           │
│     ▼               ▼                                           │
│  DUPLICATE       NOT DUPLICATE                                  │
│     │               │                                           │
│     ▼               ▼                                           │
│  Close &      ┌─────────────────────┐                           │
│  Document     │   /triage-alert     │                           │
│     │         └───────────┬─────────┘                           │
│     │                     │                                     │
│     │         ┌───────────┴─────────┐                           │
│     │         │  For each entity:   │                           │
│     │         │    /enrich-ioc      │                           │
│     │         └───────────┬─────────┘                           │
│     │                     │                                     │
│     │         ┌───────────┴─────────┐                           │
│     │         │     DECISION        │                           │
│     │         └───────────┬─────────┘                           │
│     │                     │                                     │
│     │     ┌───────────────┼────────────────┐                    │
│     │     ▼               ▼                ▼                    │
│     │   FP/BTP         TP/Suspicious    Inconclusive            │
│     │     │                  │                  │               │
│     │     ▼                  ▼                  ▼               │
│     │  /document-in-case    /document-in-case /document-in-case │
│     │  /close-case-artifact  ESCALATE         Request more info │
│     │     │                  │                  │               │
│     └─────┴──────────────────┴──────────────────┘               │
│                    │                                            │
│                    ▼                                            │
│               /generate-report                                  │
│                    │                                            │
│                    ▼                                            │
│                  END                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Steps

### Phase 1: Pre-Check

**Step 1.1: Check for Duplicates**

Invoke: `/check-duplicates CASE_ID=$CASE_ID`

- If duplicate confirmed:
  - Invoke: `/document-in-case` with "Closing as duplicate of [Similar Case ID]"
  - Invoke: `/close-case-artifact` with reason NOT_MALICIOUS
  - **END WORKFLOW**
- If not duplicate: Continue to Phase 2

### Phase 2: Initial Triage

**Step 2.1: Perform Alert Triage**

Invoke: `/triage-alert CASE_ID=$CASE_ID`

Extract from results:
- `CLASSIFICATION` - FP, BTP, TP, or Suspicious
- `KEY_ENTITIES` - List of IOCs (IPs, domains, hashes, URLs)
- `ALERT_TYPE` - Type of alert (malware, authentication, network, etc.)
- `PRIORITY` - Suggested priority level

### Phase 3: Enrichment

**Step 3.1: Enrich Each Entity**

For each entity in `KEY_ENTITIES`:

Invoke: `/enrich-ioc IOC_VALUE=$entity`

Collect:
- `GTI_FINDINGS` - Threat intelligence results
- `SIEM_CONTEXT` - SIEM entity summary
- `IOC_MATCH_STATUS` - Whether IOC appears in threat feeds

Update `CLASSIFICATION` if enrichment reveals new information.

### Phase 4: Decision & Action

**Step 4.1: Make Final Classification**

Based on triage and enrichment, confirm classification:

| Classification | Criteria | Action |
|---------------|----------|--------|
| **False Positive (FP)** | No malicious indicators, known benign | Close |
| **Benign True Positive (BTP)** | Real but authorized/expected | Close |
| **True Positive (TP)** | Confirmed malicious | Escalate |
| **Suspicious** | Inconclusive, warrants investigation | Escalate |

**Step 4.2: Execute Disposition**

**If FP or BTP:**
1. Invoke: `/document-in-case` with:
   - Classification and rationale
   - Evidence summary from enrichment
   - Closure justification
2. Invoke: `/close-case-artifact` with:
   - Reason: NOT_MALICIOUS
   - Root cause: Appropriate option (e.g., "Legit action", "Normal behavior")

**If TP or Suspicious:**
1. Invoke: `/document-in-case` with:
   - Classification and rationale
   - Evidence summary
   - Recommended next steps
2. Output escalation recommendation:
   - Escalate to Tier 2
   - Suggest appropriate follow-up skill based on alert type:
     - Malware → `/triage-malware`
     - Authentication → `/triage-suspicious-login`
     - IOC-focused → `/deep-dive-ioc`

### Phase 5: Report

**Step 5.1: Generate Triage Report**

Invoke: `/generate-report REPORT_TYPE=triage`

Include:
- Case/Alert ID
- Classification with rationale
- Key entities and enrichment results
- SIEM queries executed
- Disposition taken
- Next steps (if escalated)

## Outputs

| Output | Description |
|--------|-------------|
| `FINAL_CLASSIFICATION` | FP, BTP, TP, or Suspicious |
| `DISPOSITION` | Closed or Escalated |
| `EVIDENCE_SUMMARY` | Key findings from triage and enrichment |
| `REPORT_PATH` | Path to generated triage report |
| `ESCALATION_TARGET` | If escalated, recommended next skill/tier |

## Error Handling

- If `/check-duplicates` fails → Log warning, continue with triage
- If `/enrich-ioc` fails for an entity → Log warning, continue with other entities
- If `/close-case-artifact` fails → Log error, manual closure required
- If any MCP tool unavailable → Document limitation, proceed with available data

## Performance Targets

- Total workflow time: < 15 minutes
- Duplicate detection: < 1 minute
- Per-entity enrichment: < 2 minutes
- Target accuracy: > 90% correct classification
