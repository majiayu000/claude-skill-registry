---
name: hunt-apt
description: "Hunt for a specific APT/threat actor in your environment. Use when you have a threat actor name or GTI collection ID and want to search for their TTPs and IOCs. Gathers intelligence from GTI, searches SIEM for IOCs and TTP-based indicators, and documents findings."
required_roles:
  chronicle: roles/chronicle.editor
  gti: GTI Enterprise+
personas: [threat-hunter, tier3-analyst]
---

# APT Threat Hunt Skill

Proactively hunt for TTPs and IOCs associated with a specific Advanced Persistent Threat (APT) group based on threat intelligence.

## Inputs

- `THREAT_ACTOR_ID` - GTI Collection ID or name of the target APT group
- `HUNT_TIMEFRAME_HOURS` - Lookback period (default: 168 = 7 days)
- *(Optional)* `TARGET_SCOPE_QUERY` - UDM query to narrow scope
- *(Optional)* `HUNT_HYPOTHESIS` - Specific hypothesis guiding the hunt
- *(Optional)* `HUNT_CASE_ID` - SOAR case for tracking

## Workflow

### Step 1: Identify Actor & Gather Intelligence

If starting with a name:
```
gti-mcp.search_threat_actors(query="APT_NAME")
```

Then gather comprehensive intelligence:
```
gti-mcp.get_collection_report(id=THREAT_ACTOR_ID)
gti-mcp.get_collection_mitre_tree(id=THREAT_ACTOR_ID)
gti-mcp.get_collection_timeline_events(id=THREAT_ACTOR_ID)
```

Extract associated IOCs:
```
gti-mcp.get_entities_related_to_a_collection(id=THREAT_ACTOR_ID, relationship_name="files")
gti-mcp.get_entities_related_to_a_collection(id=THREAT_ACTOR_ID, relationship_name="domains")
gti-mcp.get_entities_related_to_a_collection(id=THREAT_ACTOR_ID, relationship_name="urls")
```

Store as `GTI_IOC_LIST`.

### Step 2: Check SIEM IOC Matches

```
secops-mcp.get_ioc_matches(hours_back=HUNT_TIMEFRAME_HOURS)
```

Correlate results with `GTI_IOC_LIST`.

### Step 3: IOC-Based SIEM Search

For each IOC type in `GTI_IOC_LIST`, construct and execute UDM queries:

```
secops-mcp.search_security_events(
    text="UDM query for IOC",
    hours_back=HUNT_TIMEFRAME_HOURS
)
```

Document both positive and negative results → `IOC_SEARCH_FINDINGS`.

### Step 4: TTP-Based SIEM Search

Based on MITRE techniques from Step 1:
- Use `gti-mcp.get_threat_intel(query="MITRE technique details")` for detection ideas
- Formulate TTP-specific UDM queries
- Execute searches over the timeframe
- Combine with `TARGET_SCOPE_QUERY` if provided

Document results → `TTP_SEARCH_FINDINGS`.

### Step 5: Enrich Findings

If hits found (`IOC_SEARCH_FINDINGS` or `TTP_SEARCH_FINDINGS`):

For each found IOC or entity:
```
secops-mcp.lookup_entity(entity_value=FOUND_ITEM)
gti-mcp.get_..._report(identifier=FOUND_ITEM)
```

### Step 6: Check Related Cases

Use `/find-relevant-case` with found IOCs and entities.

### Step 7: Document & Report

Use `/document-in-case` (if HUNT_CASE_ID provided).

Use `/generate-report` with `REPORT_TYPE="apt_hunt"`:
- Hunt objective and hypothesis
- Threat actor summary
- TTPs investigated
- IOCs searched
- SIEM queries used
- Findings (positive AND negative)
- Recommendations

### Step 8: Escalate or Conclude

**Confirmed threat found:**
→ Escalate to Incident Response
→ Create incident case

**No threat found:**
→ Document negative findings
→ Conclude hunt

## Required Outputs

**After completing this skill, you MUST report these outputs:**

| Output | Description |
|--------|-------------|
| `ACTOR_IOCS` | IOCs associated with threat actor from GTI |
| `ACTOR_TTPS` | TTPs from threat actor profile (MITRE techniques) |
| `HUNT_RESULTS` | SIEM search results for actor indicators |
| `DISCOVERED_INDICATORS` | IOCs found in environment matching actor profile |
| `CONFIRMED_IOCS` | IOCs confirmed malicious via GTI enrichment |

## Key Intelligence Sources

| Source | Tool |
|--------|------|
| Actor Profile | `get_collection_report` |
| TTPs | `get_collection_mitre_tree` |
| Timeline | `get_collection_timeline_events` |
| Related IOCs | `get_entities_related_to_a_collection` |
| Technique Details | `get_threat_intel` |

## Critical Requirements

- Document ALL queries used (for reproducibility)
- Report negative findings (no hits is valuable intel)
- Don't report false positives as confirmed threats
