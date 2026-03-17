---
name: full-investigation
description: "Complete Tier 2 investigation workflow. Orchestrates deep investigation of escalated cases: deep-dive-ioc, correlate-ioc, specialized triage (malware/login), pivot-on-ioc, and generate comprehensive report. Use for escalated cases requiring thorough analysis."
type: workflow
orchestrates:
  - deep-dive-ioc
  - correlate-ioc
  - triage-malware
  - triage-suspicious-login
  - pivot-on-ioc
  - document-in-case
  - generate-report
required_roles:
  chronicle: roles/chronicle.editor
  soar: roles/chronicle.editor
  gti: GTI Enterprise
  scc: roles/securitycenter.findingsViewer
personas: [tier2-analyst, tier3-analyst]
---

# Full Investigation Workflow

A composite skill that orchestrates comprehensive Tier 2/3 investigation of escalated security cases.

## Inputs

- `CASE_ID` - The escalated case to investigate (required)
- `PRIMARY_IOCS` - Key IOCs identified during Tier 1 triage (optional)
- `ALERT_TYPE` - Type of alert (malware, authentication, network, etc.)
- `ESCALATION_REASON` - Why this was escalated from Tier 1

## Orchestrated Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                   FULL INVESTIGATION                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ESCALATED CASE                                                 │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────┐                                        │
│  │   /deep-dive-ioc    │  (for each primary IOC)                │
│  └──────────┬──────────┘                                        │
│             │                                                   │
│             ▼                                                   │
│  ┌─────────────────────┐                                        │
│  │   /correlate-ioc    │                                        │
│  └──────────┬──────────┘                                        │
│             │                                                   │
│     ┌───────┴───────────────────┐                               │
│     │     ALERT TYPE ROUTING    │                               │
│     └───────────────────────────┘                               │
│             │                                                   │
│   ┌─────────┼───────────┬─────────┐                             │
│   ▼         ▼           ▼         ▼                             │
│ MALWARE   AUTH      NETWORK    OTHER                            │
│   │         │           │         │                             │
│   ▼         ▼           ▼         ▼                             │
│ /triage   /triage      /pivot   Continue                        │
│ -malware  -suspicious  -on-ioc  with pivoting                   │
│   │       -login        │         │                             │
│   └─────────┴───────────┴─────────┘                             │
│             │                                                   │
│             ▼                                                   │
│  ┌─────────────────────┐                                        │
│  │   /pivot-on-ioc     │  (expand investigation)                │
│  └──────────┬──────────┘                                        │
│             │                                                   │
│     ┌───────┴───────┐                                           │
│     │   DECISION    │                                           │
│     └───────┬───────┘                                           │
│             │                                                   │
│   ┌─────────┼─────────┐                                         │
│   ▼         ▼         ▼                                         │
│ INCIDENT  RESOLVED  ESCALATE                                    │
│   │         │       TO IR                                       │
│   ▼         ▼         │                                         │
│ Create   /close       │                                         │
│ Incident  -case       │                                         │
│   │       -artifact   │                                         │
│   │         │         │                                         │
│   └─────────┴─────────┘                                         │
│             │                                                   │
│             ▼                                                   │
│  ┌─────────────────────┐                                        │
│  │  /generate-report   │                                        │
│  └──────────┬──────────┘                                        │
│             │                                                   │
│             ▼                                                   │
│            END                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Steps

### Phase 1: Deep Analysis

**Step 1.0: Extract Primary IOCs (if not provided)**

If `PRIMARY_IOCS` is not provided as input, extract key entities from the case:

```
secops-soar.get_case_full_details(case_id=CASE_ID)
```

From the case details, extract IOCs:
- IP addresses from alert entities
- Domain names from network indicators
- File hashes from endpoint alerts
- URLs from web security alerts

Populate `PRIMARY_IOCS` with extracted IOCs.

**Step 1.1: Deep Dive on Primary IOCs**

For each IOC in `PRIMARY_IOCS`:

Invoke: `/deep-dive-ioc IOC_VALUE=$ioc CASE_ID=$CASE_ID`

Collect:
- `GTI_DEEP_FINDINGS` - Full threat intelligence analysis
- `SIEM_DEEP_CONTEXT` - Detailed SIEM context
- `RELATED_ENTITIES` - Discovered related IOCs and entities
- `THREAT_ATTRIBUTION` - Any threat actor/campaign links

**Step 1.2: Aggregate Discovered IOCs**

Combine all `RELATED_ENTITIES` collected from deep-dive steps into `ALL_DISCOVERED_IOCS`:

```
ALL_DISCOVERED_IOCS = PRIMARY_IOCS + all(RELATED_ENTITIES from each deep-dive)
```

This aggregated list is used for correlation in Phase 2.

### Phase 2: Correlation

**Step 2.1: Correlate with Existing Cases**

Invoke: `/correlate-ioc IOC_LIST=$ALL_DISCOVERED_IOCS`

Collect:
- `RELATED_CASES` - Other cases with same IOCs
- `RELATED_ALERTS` - Alerts involving same entities
- `PATTERN_ANALYSIS` - Detected patterns across cases

**Step 2.2: Find Related Open Cases**

Invoke: `/find-relevant-case` with key entities

Document any linked investigations.

### Phase 3: Specialized Analysis

**Step 3.1: Route by Alert Type**

Based on `ALERT_TYPE`, invoke specialized triage:

| Alert Type | Skill | Focus |
|------------|-------|-------|
| Malware | `/triage-malware` | File analysis, behavior, persistence |
| Authentication | `/triage-suspicious-login` | User activity, login patterns |
| Network | `/pivot-on-ioc` | Network IOC relationships |
| Other | Continue to pivoting | General IOC expansion |

**For Malware:**
Invoke: `/triage-malware FILE_HASH=$hash CASE_ID=$CASE_ID`

Collect:
- Malware family identification
- Behavioral analysis
- Affected systems
- Containment recommendations

**For Authentication:**
Invoke: `/triage-suspicious-login USER=$user CASE_ID=$CASE_ID`

Collect:
- Login anomaly analysis
- User activity timeline
- Compromised account indicators
- Account status recommendations

### Phase 4: Expansion

**Step 4.1: Pivot on High-Confidence IOCs**

For each high-confidence malicious IOC:

Invoke: `/pivot-on-ioc IOC_VALUE=$ioc`

Collect:
- `RELATED_INFRASTRUCTURE` - Connected domains, IPs, files
- `CAMPAIGN_LINKS` - Associated campaigns or actors
- `ADDITIONAL_IOCS` - New IOCs to hunt for

**Step 4.2: Validate Expanded IOCs**

For significant new IOCs discovered:
- Quick GTI lookup
- SIEM presence check
- Add to investigation scope if relevant

### Phase 5: Assessment

**Step 5.1: Determine Investigation Outcome**

Assess all findings and classify:

| Outcome | Criteria | Action |
|---------|----------|--------|
| **Incident Confirmed** | Active compromise, ongoing threat | Escalate to IR |
| **Resolved - Contained** | Threat neutralized, no ongoing risk | Document & Close |
| **Resolved - False Positive** | Deep analysis confirms benign | Document & Close |
| **Requires IR Escalation** | Containment/eradication needed | Escalate to IR |

**Step 5.2: Execute Disposition**

**If Incident Confirmed / Requires IR:**
1. Invoke: `/document-in-case` with full findings
2. Output escalation recommendation:
   - Recommend specific IR skill:
     - Ransomware indicators → `/respond-ransomware`
     - Malware persistence → `/respond-malware`
     - Phishing origin → `/respond-phishing`
     - Account compromise → `/respond-compromised-account`
3. Prepare handoff package for IR team

**If Resolved:**
1. Invoke: `/document-in-case` with:
   - Investigation summary
   - All queries and findings
   - Resolution rationale
2. If closing: Invoke: `/close-case-artifact` with appropriate reason

### Phase 6: Documentation

**Step 6.1: Generate Investigation Report**

Invoke: `/generate-report REPORT_TYPE=investigation`

Include:
- Executive summary
- Investigation timeline
- All IOCs analyzed (with verdicts)
- SIEM queries used
- GTI findings
- Correlation results
- Attack chain (if identified)
- Recommendations
- Lessons learned

## Outputs

| Output | Description |
|--------|-------------|
| `INVESTIGATION_OUTCOME` | Incident, Resolved, or Escalated |
| `THREAT_ASSESSMENT` | Severity, scope, and attribution |
| `ALL_IOCS` | Complete list of analyzed IOCs with verdicts |
| `ATTACK_CHAIN` | Reconstructed attack timeline (if applicable) |
| `REPORT_PATH` | Path to investigation report |
| `ESCALATION_DETAILS` | If escalated, target and handoff package |

## Error Handling

- If `/deep-dive-ioc` fails → Fall back to `/enrich-ioc`, continue
- If GTI Enterprise features unavailable → Document limitation, use Standard features
- If specialized triage fails → Document, continue with general analysis
- If correlation timeout → Proceed with available data, note gap

## Performance Targets

- Total workflow time: < 2 hours
- Deep dive per IOC: < 15 minutes
- Correlation: < 10 minutes
- Specialized triage: < 30 minutes
- Report generation: < 15 minutes
- Target accuracy: > 95% correct assessment
