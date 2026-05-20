---
name: correlate-ioc
description: "Check for existing SIEM alerts and case management entries related to IOCs. Use to understand if an indicator has triggered previous alerts or is part of ongoing investigations. Takes IOC list and returns related alerts and cases."
required_roles:
  chronicle: roles/chronicle.viewer
  soar: roles/chronicle.editor
personas: [tier1-analyst, tier2-analyst, tier3-analyst]
---

# Correlate IOC Skill

Check for existing SIEM alerts and cases related to specific Indicators of Compromise.

## Inputs

- `IOC_LIST` - Single IOC or list of IOCs (e.g., `["198.51.100.10", "evil-domain.com"]`)
- *(Optional)* `TIME_FRAME_HOURS` - Lookback period for SIEM alerts (default: 168 = 7 days)
- *(Optional)* `SOAR_CASE_FILTER` - Additional filter for SOAR cases (e.g., `status="OPEN"`)

## Workflow

### Step 1: Correlate SIEM Alerts

Search for alerts containing any IOC in the list:

```
secops-mcp.get_security_alerts(
    query=IOC_based_query,
    hours_back=TIME_FRAME_HOURS
)
```

Store summary in `RELATED_SIEM_ALERTS`:
- Alert count
- Alert types/names
- Severity distribution
- Affected assets

### Step 2: Correlate Cases

Search for cases containing any IOC:

```
secops-soar.list_cases(
    filter=IOC_based_filter + SOAR_CASE_FILTER
)
```

Store summary in `RELATED_SOAR_CASES`:
- Case IDs and names
- Case status
- Case priority

## Required Outputs

**After completing this skill, you MUST report these outputs:**

| Output | Description |
|--------|-------------|
| `RELATED_SIEM_ALERTS` | Summary of SIEM alerts related to the IOC(s) |
| `RELATED_CASES` | Summary of cases related to the IOC(s) |
| `CORRELATION_STATUS` | Success/failure status of the correlation |
| `MALICIOUS_CONFIDENCE` | Derived confidence based on alert history: `high`, `medium`, `low`, or `none` |

## Use Cases

1. **Before Investigation** - Check if IOC is already under investigation
2. **During Enrichment** - Understand internal activity for an IOC
3. **Threat Hunt** - Find all alerts/cases related to campaign indicators
4. **Incident Response** - Identify scope of compromise across cases

## Correlation Summary Template

```
IOC Correlation Summary for [IOC_LIST]:

SIEM Alerts (last [TIME_FRAME_HOURS] hours):
- Total alerts: [count]
- Alert types: [list]
- Affected hosts: [list]

Related Cases:
- Open cases: [count] - [IDs]
- Closed cases: [count]
- Related investigations: [summary]
```
