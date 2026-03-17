---
name: hunt-ioc
description: "Hunt for specific IOCs across your environment. Use when you have a list of IPs, domains, hashes, or URLs from threat intel and want to check if they appear in your SIEM. Systematic searching with enrichment and documentation."
required_roles:
  chronicle: roles/chronicle.editor
  gti: GTI Enterprise
personas: [threat-hunter, tier2-analyst]
---

# IOC Threat Hunt Skill

Proactively hunt for specific Indicators of Compromise (IOCs) across the environment based on threat intelligence feeds, recent incidents, or emerging threats.

## Inputs

- `IOC_LIST` - Comma-separated list of IOC values to hunt
- `IOC_TYPES` - Corresponding types (e.g., "IP Address, Domain, File Hash")
- `HUNT_TIMEFRAME_HOURS` - Lookback period (default: 96)
- *(Optional)* `HUNT_CASE_ID` - SOAR case for tracking
- *(Optional)* `REASON_FOR_HUNT` - Why these IOCs are being hunted

## Workflow

### Step 1: Parse and Validate IOCs

Parse `IOC_LIST` and `IOC_TYPES` into structured list.
Validate IOC formats (IP regex, hash length, etc.).

### Step 2: Initial IOC Match Check

```
secops-mcp.get_ioc_matches(hours_back=HUNT_TIMEFRAME_HOURS)
```

Check if any IOCs appear in integrated threat feeds.

### Step 3: Iterative SIEM Search

For each IOC, construct appropriate UDM query:

**IP Address:**
```udm
(principal.ip = "IOC" OR target.ip = "IOC" OR network.ip = "IOC")
```

**Domain:**
```udm
(principal.hostname = "IOC" OR target.hostname = "IOC" OR network.dns.questions.name = "IOC")
```

**File Hash:**
```udm
(target.file.sha256 = "IOC" OR target.file.md5 = "IOC" OR target.file.sha1 = "IOC")
```

**URL:**
```udm
target.url = "IOC"
```

Execute each search:
```
secops-mcp.search_security_events(text=query, hours_back=HUNT_TIMEFRAME_HOURS)
```

### Step 4: Analyze Results

For each search result:
- Identify affected hosts, users, processes
- Note event types (login, network connection, file execution)
- Assess if activity is suspicious or expected

### Step 5: Enrich Hits

If hits found for an IOC:

Use `/enrich-ioc` for the IOC itself.

For involved entities (hosts, users):
```
secops-mcp.lookup_entity(entity_value=ENTITY)
```

### Step 6: Document Hunt

Use `/document-in-case` (if HUNT_CASE_ID provided):

```
IOC Hunt Summary:
- IOCs Hunted: [list]
- Timeframe: [hours]
- Queries Used: [list with results summary]
- IOCs with Hits: [list with details]
- IOCs with No Hits: [list - confirms environment is clean]
- Enrichment: [for hits]
- Recommendations: [next steps]
```

### Step 7: Escalate or Conclude

**Confirmed malicious activity:**
→ Create/update incident case
→ Trigger appropriate response runbook

**No significant findings:**
→ Document hunt completion
→ Note clean IOCs for future reference

## Output Summary Template

```markdown
# IOC Hunt Results

**Hunt Date:** [timestamp]
**Timeframe:** Last [X] hours
**Reason:** [REASON_FOR_HUNT]

## IOCs Searched
| IOC | Type | Result | Notes |
|-----|------|--------|-------|
| 198.51.100.10 | IP | NO HITS | Clean |
| evil.com | Domain | 3 HITS | DNS lookups from HOST1 |

## Hits Analysis
[Details for each IOC with hits]

## Recommendations
[Actions to take]
```

## Required Outputs

**After completing this skill, you MUST report these outputs:**

| Output | Description |
|--------|-------------|
| `MATCHES` | IOCs found in SIEM (list of IOCs with hits) |
| `MATCH_CONTEXT` | Context for each match (events, assets, users affected) |
| `MATCHES_FOUND` | Boolean: `true` if any IOCs found in environment, `false` otherwise |

## Critical Requirements

- Search ALL provided IOCs (don't skip any)
- Use correct timeframe (not 1 hour instead of 72)
- Document negative results (confirms environment is clean)
- Don't declare "clean" if there were obvious hits
