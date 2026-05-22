---
name: triage-suspicious-login
description: "Triage suspicious login alerts like impossible travel, untrusted location, or multiple failures. Use when investigating authentication anomalies. Analyzes user history, source IP reputation, login patterns, and determines if escalation is needed."
required_roles:
  chronicle: roles/chronicle.viewer
  soar: roles/chronicle.editor
  gti: GTI Standard
personas: [tier1-analyst, tier2-analyst, tier3-analyst]
---

# Suspicious Login Triage Skill

Guide initial triage of suspicious login alerts (impossible travel, untrusted location, multiple failed logins) for Tier 1 SOC Analysts.

## Inputs

- `CASE_ID` - SOAR case ID containing the alert(s)
- `ALERT_GROUP_IDENTIFIERS` - Alert group identifiers from the case
- *(Optional)* `USER_ID` - The user ID if known upfront
- *(Optional)* `SOURCE_IP` - The source IP if known upfront

## Workflow

### Step 1: Get Case Context

```
secops-soar.get_case_full_details(case_id=CASE_ID)
```

### Step 2: Extract Key Entities

```
secops-soar.list_events_by_alert(case_id=CASE_ID, alert_id=ALERT_ID)
```

Parse events to extract:
- `USER_ID` - The user account
- `SOURCE_IP` - The login source IP
- `HOSTNAME` - The target/source hostname (if available)

### Step 3: User Context (SIEM)

```
secops-mcp.lookup_entity(entity_value=USER_ID)
```

Record: Recent activity, first/last seen, related alerts.

### Step 4: Source IP Enrichment

Use `/enrich-ioc` with IOC_TYPE="IP Address":
- GTI reputation and geolocation
- SIEM entity summary
- IOC match status

### Step 5: Hostname Context (if available)

```
secops-mcp.lookup_entity(entity_value=HOSTNAME)
```

### Step 6: Recent Login Activity

Search for login patterns over the last 96 hours:

```
secops-mcp.search_security_events(
    text='metadata.event_type IN ("USER_LOGIN", "AUTH_ATTEMPT") AND principal.user.userid = "USER_ID"',
    hours_back=96
)
```

Analyze for:
- Logins from unusual IPs
- Successful logins after failures
- Geographic anomalies (impossible travel)
- Concurrent sessions from different locations

### Step 7: Check Related Cases

Use `/find-relevant-case` with search terms: `[USER_ID, SOURCE_IP, HOSTNAME]`

### Step 8: (Optional) Identity Provider Check

If IDP tools available (e.g., Okta):
- Account status
- MFA enrollment
- Recent legitimate logins
- Password change history

### Step 9: Synthesize & Document

Use `/document-in-case` with findings summary:

```
Suspicious Login Triage for USER_ID from SOURCE_IP:
- User SIEM Summary: [...]
- Source IP GTI: [reputation, geo]
- Login Pattern: [normal/anomalous]
- Related Cases: [...]
- Recommendation: [Close as FP | Escalate to Tier 2]
```

## Required Outputs

**After completing this skill, you MUST report these outputs:**

| Output | Description |
|--------|-------------|
| `LOGIN_VERDICT` | Assessment: `legitimate`, `suspicious`, or `malicious` |
| `ANOMALY_INDICATORS` | What made the login suspicious (impossible travel, new device, etc.) |
| `RELATED_ACTIVITY` | Other suspicious activity from user or source IP |
| `RISK_SCORE` | Numerical risk assessment (0-100) based on findings |

## Decision Matrix

| Finding | Recommendation |
|---------|----------------|
| Known VPN/corporate IP + normal pattern | Close as FP |
| User confirmed travel + MFA used | Close as Benign TP |
| Malicious IP reputation | Escalate |
| Impossible travel + no MFA | Escalate urgently |
| Multiple failures then success from new IP | Escalate |
| Pattern matches user's normal behavior | Close as FP |

## Key Patterns to Detect

**Impossible Travel:**
- Login from NYC, then London 30 mins later
- Check if VPN or cloud service could explain

**Credential Stuffing:**
- Many failures across multiple accounts from same IP
- Success after many failures

**Account Takeover:**
- Login from new device/location
- Followed by password change or MFA modification

**Lateral Movement:**
- Same user logging into many systems rapidly
- Unusual service account activity
