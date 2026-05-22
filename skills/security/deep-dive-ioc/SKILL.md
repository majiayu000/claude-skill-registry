---
name: deep-dive-ioc
description: "Perform exhaustive analysis of a critical IOC. Use when an IOC needs Tier 2+ investigation beyond basic enrichment - includes GTI pivoting, deep SIEM searches, correlation with related entities, and threat attribution. For escalated IOCs requiring comprehensive investigation."
required_roles:
  chronicle: roles/chronicle.editor
  soar: roles/chronicle.editor
  gti: GTI Enterprise
personas: [tier2-analyst, tier3-analyst, threat-hunter, incident-responder]
---

# Deep Dive IOC Analysis Skill

Perform exhaustive analysis of a single, potentially critical Indicator of Compromise escalated from Tier 1 or identified during an investigation.

## Inputs

- `IOC_VALUE` - The IOC to analyze (IP, domain, hash, or URL)
- `IOC_TYPE` - The type: "IP Address", "Domain", "File Hash", or "URL"
- `CASE_ID` - case ID for documentation (optional)
- `TIME_FRAME_HOURS` - Lookback period (default: 168 = 7 days)

## Workflow

### Step 1: Get Case Context (if CASE_ID provided)

```
secops-soar.get_case_full_details(case_id=CASE_ID)
```

### Step 2: Detailed GTI Report

Get comprehensive threat intelligence:

| IOC Type | Tool |
|----------|------|
| IP | `gti-mcp.get_ip_address_report(ip_address=IOC_VALUE)` |
| Domain | `gti-mcp.get_domain_report(domain=IOC_VALUE)` |
| Hash | `gti-mcp.get_file_report(hash=IOC_VALUE)` |
| URL | `gti-mcp.get_url_report(url=IOC_VALUE)` |

Record:
- Reputation and classifications
- First/last seen dates
- Associated threats (malware families, actors) → `ASSOCIATED_THREAT_IDS`
- Key behaviors (for file hashes)

### Step 3: GTI Pivoting

Use `/pivot-on-ioc` or directly call GTI relationship tools:

**Recommended relationships by type:**
- **IP**: `communicating_files`, `downloaded_files`, `resolutions`
- **Domain**: `resolutions`, `communicating_files`, `subdomains`
- **Hash**: `contacted_domains`, `contacted_ips`, `dropped_files`
- **URL**: `communicating_files`, `downloaded_files`

For file hashes, also get behavior summary:
```
gti-mcp.get_file_behavior_summary(hash=IOC_VALUE)
```

### Step 4: Deep SIEM Search

Search for activity involving the IOC and its related entities:

```
secops-mcp.search_security_events(
    text="UDM query for IOC_VALUE",
    hours_back=TIME_FRAME_HOURS
)
```

**Identify `OBSERVED_RELATED_IOCS`** - IOCs from GTI pivoting that actually appear in SIEM results.

### Step 5: SIEM Enrichment & Correlation

For the IOC and each `OBSERVED_RELATED_IOC`:
- Use `/enrich-ioc` for enrichment
- Use `/correlate-ioc` for alert/case correlation
- Use `/find-relevant-case` for broader case search

### Step 6: Enrich Associated Threats (Optional)

If `ASSOCIATED_THREAT_IDS` were found (malware families, actors):

```
gti-mcp.get_collection_report(id=THREAT_ID)
```

### Step 7: Synthesize & Report

Combine all findings:
- GTI report details
- Related entities from pivoting
- SIEM search results
- Observed related IOCs with enrichment
- Related alerts and cases
- Associated threat context

**Document in Case** (if CASE_ID provided):
```
Use /document-in-case with comprehensive findings summary
```

**Or generate standalone report:**
```
Use /generate-report with REPORT_TYPE="deep_dive_ioc"
```

## Required Outputs

**After completing this skill, you MUST report these outputs:**

| Output | Description |
|--------|-------------|
| `GTI_DEEP_FINDINGS` | Comprehensive GTI analysis (reputation, classification, behaviors) |
| `SIEM_DEEP_CONTEXT` | Extended SIEM event context (hosts, users, timelines) |
| `RELATED_ENTITIES` | Related IOCs from GTI pivoting (infrastructure connections) |
| `DISCOVERED_IOCS` | All IOCs discovered during analysis |
| `THREAT_ATTRIBUTION` | Threat actor/campaign attribution if found |

Additionally provide:
- Impact assessment and scope identification
- Recommendations (escalate, contain, monitor)
- Documentation in case or standalone report

## When to Use This vs Basic Enrichment

| Use `/enrich-ioc` | Use `/deep-dive-ioc` |
|-------------------|----------------------|
| Initial triage | Escalated from Tier 1 |
| Quick context needed | Comprehensive investigation |
| Single IOC lookup | Full infrastructure mapping |
| Tier 1 workflow | Tier 2+ investigation |
