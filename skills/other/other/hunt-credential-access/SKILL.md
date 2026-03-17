---
name: hunt-credential-access
description: "Hunt for credential access techniques like LSASS dumping or browser credential theft. Use when searching for evidence of credential harvesting. Takes MITRE technique IDs and searches for behavioral indicators in SIEM."
required_roles:
  chronicle: roles/chronicle.editor
  gti: GTI Standard
personas: [threat-hunter]
---

# Credential Access TTP Hunt Skill

Proactively hunt for MITRE ATT&CK Credential Access techniques (T1003, T1555, etc.) based on threat intelligence or hypothesis.

## Inputs

- `TECHNIQUE_IDS` - Comma-separated MITRE technique IDs (e.g., "T1003.001,T1555.003")
- `TIME_FRAME_HOURS` - Lookback period (default: 72)
- *(Optional)* `TARGET_SCOPE_QUERY` - UDM query to narrow scope
- *(Optional)* `HUNT_HYPOTHESIS` - Reason for the hunt
- *(Optional)* `HUNT_CASE_ID` - SOAR case for tracking

## Common Techniques

| Technique | Description |
|-----------|-------------|
| T1003.001 | LSASS Memory |
| T1003.002 | Security Account Manager |
| T1003.003 | NTDS |
| T1003.004 | LSA Secrets |
| T1003.005 | Cached Domain Credentials |
| T1003.006 | DCSync |
| T1555.001 | Keychain |
| T1555.003 | Credentials from Web Browsers |
| T1555.004 | Windows Credential Manager |

## Workflow

### Step 1: Research Techniques

For each technique in `TECHNIQUE_IDS`:
```
gti-mcp.get_threat_intel(query="Explain MITRE ATT&CK technique T1003.001")
```

Understand:
- What the technique does
- Common procedures/tools
- Detection methods

### Step 2: Develop Hunt Queries

**T1003.001 - LSASS Memory Access:**
```udm
metadata.event_type = "PROCESS_LAUNCH" AND
target.process.file.full_path = "C:\\Windows\\System32\\lsass.exe"
```
Look for suspicious parent processes accessing lsass.exe.

**T1003.001 - Known Dumping Tools:**
```udm
metadata.event_type = "PROCESS_LAUNCH" AND
(principal.process.command_line CONTAINS "mimikatz" OR
 principal.process.command_line CONTAINS "procdump" OR
 principal.process.command_line CONTAINS "sekurlsa")
```

**T1555.003 - Browser Credential Files:**
```udm
metadata.event_type = "FILE_OPEN" AND
(target.file.full_path CONTAINS "Login Data" OR
 target.file.full_path CONTAINS "Web Data" OR
 target.file.full_path CONTAINS "cookies.sqlite") AND
principal.process.file.full_path NOT IN ("chrome.exe", "firefox.exe", "msedge.exe")
```

**T1003.006 - DCSync:**
```udm
metadata.event_type = "DOMAIN_CONTROLLER_REPLICATION" AND
principal.hostname NOT IN @known_domain_controllers
```

**General - Credential Dumping Tools:**
```udm
metadata.event_type = "PROCESS_LAUNCH" AND
(target.process.file.full_path CONTAINS "mimikatz" OR
 target.process.file.full_path CONTAINS "lazagne" OR
 target.process.file.full_path CONTAINS "pypykatz")
```

Combine with `TARGET_SCOPE_QUERY` if provided.

### Step 3: Execute Searches

```
secops-mcp.search_security_events(text=query, hours_back=TIME_FRAME_HOURS)
```

### Step 4: Analyze Results

Look for:
- Low-prevalence events (unusual parent-child relationships)
- Access from unexpected applications
- Correlation with other suspicious activity
- Known bad tool signatures

### Step 5: Enrich Findings

If suspicious events found:
```
secops-mcp.lookup_entity(entity_value=USER_OR_HOST)
```

For file hashes:
```
gti-mcp.get_file_report(hash=HASH)
```

### Step 6: Document Hunt

Use `/document-in-case`:
- Techniques hunted with descriptions
- Queries used
- Findings (positive AND negative)
- Enrichment results
- Risk assessment

### Step 7: Escalate or Conclude

**Credential theft confirmed:**
→ Trigger `/respond-compromised-account` for affected users
→ Escalate to incident response
→ Consider password resets for exposed credentials

**No findings:**
→ Document negative results
→ Confirm detection coverage for these techniques

## Required Outputs

**After completing this skill, you MUST report these outputs:**

| Output | Description |
|--------|-------------|
| `FINDINGS` | Detected credential access activity (events, processes, files accessed) |
| `DETECTED_TECHNIQUES` | MITRE techniques observed (e.g., T1003.001, T1555.003) |
| `AFFECTED_ACCOUNTS` | Accounts potentially compromised (users whose credentials may be exposed) |

## Detection Gaps to Note

If queries return no results, consider:
- Is the required telemetry being collected?
- Are endpoint logs being forwarded to SIEM?
- Do detection rules exist for these techniques?

Document gaps for security engineering follow-up.
