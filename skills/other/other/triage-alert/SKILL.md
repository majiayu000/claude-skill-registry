---
name: triage-alert
description: "Triage a security alert or case. Use when given an ALERT_ID or CASE_ID to assess if it's a real threat. Enriches IOCs, searches SIEM for context, and determines if the alert should be closed (false positive) or escalated for investigation."
required_roles:
  chronicle: roles/chronicle.viewer
  soar: roles/chronicle.editor
  gti: GTI Standard
personas: [tier1-analyst, tier2-analyst, tier3-analyst, incident-responder]
---

# Alert Triage Skill

Perform standardized initial assessment of security alerts to determine if they represent real threats requiring investigation or can be closed as false positives.

## Inputs

You need one of these identifiers to begin:
- `ALERT_ID` - The alert identifier
- `CASE_ID` - The case identifier

## Workflow

### Step 1: Gather Initial Context

Retrieve full details about the alert/case:

```
Use secops-soar tools:
- get_case_full_details(case_id) - Get case metadata and context
- list_alerts_by_case(case_id) - List all alerts in the case
- list_events_by_alert(alert_id) - Get triggering events
```

Extract and note:
- Alert type and severity
- Key entities involved (IPs, domains, hashes, users, hostnames)
- Triggering events and timestamps

> **Note:** Duplicate detection should be handled by invoking `/check-duplicates`
> before this skill, or by using the `/full-triage-alert` workflow which
> orchestrates both skills in the correct sequence.

### Step 2: Find Related Open Cases

Search for other open cases involving the same entities:

```
Use secops-soar.list_cases with:
- Search terms = key entities from Step 1
- Status filter = "Opened"
```

Note any related cases for correlation.

### Step 3: Alert-Specific SIEM Search

Perform a targeted SIEM search based on the alert type:

```
Use secops-mcp.search_security_events with relevant query
```

**By alert type:**
- **Suspicious Login**: Search login events (success/failure) for user/source IP around alert time
- **Malware Detection**: Search process execution, file mods, network events for the hash/endpoint
- **Network Alert**: Search network flows, DNS lookups for source/destination IPs/domains

### Step 4: Enrich Key Entities

For each key entity (IP, domain, hash, URL), gather threat intelligence:

**GTI Enrichment** (use gti-mcp tools):
- `get_ip_address_report(ip)` - IP reputation and context
- `get_domain_report(domain)` - Domain reputation
- `get_file_report(hash)` - File/hash analysis
- `get_url_report(url)` - URL reputation

**SIEM Enrichment** (use secops-mcp tools):
- `lookup_entity(entity)` - Entity summary from SIEM
- `get_ioc_matches(hours_back)` - Check if IOC appears in threat feeds

### Step 5: Make Assessment

Based on all gathered evidence, classify the alert:

| Classification | Criteria | Action |
|---------------|----------|--------|
| **False Positive (FP)** | No malicious indicators, known benign activity | Close |
| **Benign True Positive (BTP)** | Real detection but authorized/expected activity | Close |
| **True Positive (TP)** | Confirmed malicious indicators or suspicious behavior | Escalate |
| **Suspicious** | Inconclusive but warrants investigation | Escalate |

### Step 6: Take Action

**If FP or BTP:**
1. Document findings in case comments explaining the rationale
2. Close the case/alert:
   - Use `secops-soar.siemplify_close_case` or `siemplify_close_alert`
   - Closure reason: `NOT_MALICIOUS`
   - Root cause: Use `get_case_settings_root_causes` to get valid options (e.g., "Legit action", "Normal behavior")

**If TP or Suspicious:**
1. Optionally adjust priority with `secops-soar.change_case_priority`
2. Document initial findings and assessment in case comments
3. Escalate to Tier 2 or trigger appropriate investigation runbook:
   - Suspicious login → `suspicious_login_triage`
   - Malware → `malware_triage`
   - IOC-focused → `deep_dive_ioc_analysis`

## Output Requirements

After completing triage, provide:

1. **Alert Status**: Closed (with reason) or Escalated
2. **Classification**: FP, BTP, TP, or Suspicious
3. **Evidence Summary**: Key findings from enrichment and SIEM searches
4. **Rationale**: Why this classification was chosen
5. **Next Steps**: What happens next (closed, assigned to whom, which runbook triggered)

## Quick Reference

**SOAR Tools:**
- `get_case_full_details`, `list_alerts_by_case`, `list_events_by_alert`
- `post_case_comment`, `change_case_priority`
- `siemplify_get_similar_cases`, `siemplify_close_case`, `siemplify_close_alert`

**SIEM Tools:**
- `lookup_entity`, `get_ioc_matches`, `search_security_events`

**GTI Tools:**
- `get_file_report`, `get_domain_report`, `get_ip_address_report`, `get_url_report`

---

For detailed workflow diagrams, completion criteria, and evaluation rubric, see [reference.md](./reference.md).
