---
name: hunt-threat
description: "Conduct proactive, hypothesis-driven threat hunting. Use when performing advanced hunting based on threat intelligence, TTPs, or anomalies. For Tier 3 analysts or dedicated threat hunters. Supports iterative search, pivoting, and comprehensive documentation."
required_roles:
  chronicle: roles/chronicle.editor
  gti: GTI Enterprise
personas: [threat-hunter, tier3-analyst]
---

# Advanced Threat Hunting Skill

Conduct proactive, hypothesis-driven threat hunts based on threat intelligence, observed anomalies, or specific TTPs.

## Inputs

- `HUNT_HYPOTHESIS` - Clear statement of the hunt objective (required)
  - Example: "Suspected DNS tunneling for C2 based on recent actor TTPs"
  - Example: "Anomalous PowerShell execution on critical servers"
  - Example: "Living-off-the-land techniques bypassing EDR"
- *(Optional)* `RELEVANT_GTI_REPORTS` - GTI Collection IDs or report names
- *(Optional)* `TARGET_SCOPE_QUERY` - UDM query to narrow initial scope
- `TIME_FRAME_HOURS` - Lookback period (default: 168 = 7 days)
- *(Optional)* `HUNT_CASE_ID` - case for tracking the hunt

## Workflow

### Step 1: Define Hypothesis & Scope

Clearly articulate:
- What threat behavior are we looking for?
- What would evidence of this look like in logs?
- What systems/users are in scope?
- What time period is relevant?

Create or identify `HUNT_CASE_ID` for documentation.

### Step 2: Deep Intelligence Analysis

For each relevant GTI report:

```
gti-mcp.get_collection_report(id=REPORT_ID)
gti-mcp.get_entities_related_to_a_collection(id=REPORT_ID, relationship_name="attack_techniques")
gti-mcp.get_collection_timeline_events(id=REPORT_ID)
gti-mcp.get_collection_mitre_tree(id=REPORT_ID)
```

Also:
```
gti-mcp.get_threat_intel(query="Details on specific TTPs")
```

### Step 3: Develop Initial Hunt Queries

Based on hypothesis and intelligence, formulate advanced queries:

**SIEM queries:**
```
secops-mcp.search_security_events(
    text="Advanced UDM query targeting specific behaviors",
    hours_back=TIME_FRAME_HOURS
)
```

**BigQuery (for large-scale analysis):**
```
bigquery.execute-query(query="Complex analytical query")
```

### Step 4: Iterative Search & Analysis

**Hunt Loop:**
1. Execute queries
2. Analyze results for outliers, suspicious patterns
3. Identify leads (suspicious hosts, users, processes, connections)
4. Refine hypothesis based on findings
5. Develop new, more targeted queries
6. Repeat until exhausted or time limit reached

**Key questions at each iteration:**
- Does this match our hypothesis?
- What's the baseline/normal behavior?
- Are these true anomalies or noise?
- What should we pivot on next?

### Step 5: Advanced Enrichment

For each promising lead:

```
secops-mcp.lookup_entity(entity_value=LEAD)
```

GTI enrichment and pivoting:
```
gti-mcp.get_..._report(identifier=LEAD)
gti-mcp.get_entities_related_to_...(identifier=LEAD)
```

Check IOC matches:
```
secops-mcp.get_ioc_matches()
```

### Step 6: Continuous Documentation

Document throughout in `HUNT_CASE_ID`:
- Queries used (with results summary)
- Analysis reasoning
- Positive and negative findings
- Pivots and why they were taken

Use `/document-in-case` for each significant finding.

### Step 7: Hunt Report

Use `/generate-report` with `REPORT_TYPE="hunt_summary"`:
- Hypothesis and scope
- Intelligence sources used
- Queries executed
- Findings (positive and negative)
- Recommendations

### Step 8: Action Based on Findings

**Confirmed Threat Found:**
→ Escalate to Incident Response immediately
→ Create incident case, hand over evidence

**Suspicious Activity (not confirmed):**
→ Recommend enhanced monitoring
→ Propose new detection rules to Security Engineering

**Valuable Insights (no active threat):**
→ Document for future reference
→ Propose detection improvements

**Inconclusive:**
→ Document process and limitations
→ Note areas for future investigation

## Required Outputs

**After completing this skill, you MUST report these outputs:**

| Output | Description |
|--------|-------------|
| `HUNT_QUERIES` | UDM queries executed during the hunt |
| `INITIAL_FINDINGS` | Raw findings from SIEM searches |
| `FINDINGS_TYPE` | Category: `lateral_movement`, `credential_access`, `data_exfil`, or `generic` |
| `DISCOVERED_IOCS` | IOCs extracted from findings (IPs, domains, hashes) |
| `HIGH_CONFIDENCE_IOCS` | IOCs confirmed malicious via GTI enrichment |
| `THREAT_CONFIRMED` | Boolean: `true` if active threat confirmed, `false` otherwise |

## Hunt Hypothesis Templates

**TTP-Based:**
> "Hunt for [MITRE Technique] activity, specifically [observable behavior], targeting [scope] over [timeframe]."

**Actor-Based:**
> "Hunt for [Threat Actor] TTPs including [specific techniques], focusing on [likely targets] based on [intelligence source]."

**Anomaly-Based:**
> "Investigate anomalous [behavior type] observed in [data source], specifically [anomaly description], to determine if malicious."

## Example Hunt Queries

**DNS Tunneling:**
```udm
metadata.event_type = "NETWORK_DNS" AND
network.dns.questions.name MATCHES ".*[a-z0-9]{30,}.*" AND
target.hostname NOT IN @known_cdn_domains
```

**Suspicious PowerShell:**
```udm
metadata.event_type = "PROCESS_LAUNCH" AND
target.process.file.full_path MATCHES ".*powershell.*" AND
target.process.command_line MATCHES ".*(encodedcommand|bypass|hidden).*"
```

**Living-off-the-Land:**
```udm
metadata.event_type = "PROCESS_LAUNCH" AND
target.process.file.full_path IN @lolbins_list AND
principal.user.userid NOT IN @authorized_admins
```
