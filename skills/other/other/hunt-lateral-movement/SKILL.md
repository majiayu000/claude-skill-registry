---
name: hunt-lateral-movement
description: "Hunt for lateral movement using PsExec, WMI, or similar techniques. Use when proactively searching for attackers moving through your network using admin tools. Searches for service installations, remote process execution, and suspicious network correlations."
required_roles:
  chronicle: roles/chronicle.editor
  gti: GTI Standard
personas: [threat-hunter]
---

# Lateral Movement Hunt Skill (PsExec/WMI)

Proactively hunt for signs of lateral movement using common administrative tools like PsExec or WMI abuse.

## Inputs

- `TIME_FRAME_HOURS` - Lookback period (default: 72)
- *(Optional)* `TARGET_SCOPE_QUERY` - UDM query to narrow scope
- *(Optional)* `HUNT_HYPOTHESIS` - Reason for the hunt
- *(Optional)* `HUNT_CASE_ID` - SOAR case for tracking

## Workflow

### Step 1: Research Techniques

```
secops-mcp.get_threat_intel(query="MITRE T1021.002 SMB Admin Shares")
secops-mcp.get_threat_intel(query="MITRE T1047 WMI")
secops-mcp.get_threat_intel(query="MITRE T1570 Lateral Tool Transfer")
```

### Step 2: Develop Hunt Queries

#### Query Placeholders

The queries below use placeholders that must be customized for your environment:

| Placeholder | Type | Description |
|-------------|------|-------------|
| `known_services` | Reference List | Legitimate services spawned by services.exe. Define this list in Chronicle and populate with your environment baseline. |
| `TARGET_IP` | IP Address | Replace with the target system IP from your investigation context. |
| `SOURCE_IP` | IP Address | Replace with the source system IP from your investigation context. |

**PsExec Service Installation:**
```udm
metadata.product_event_type = "ServiceInstalled" AND
target.process.file.full_path CONTAINS "PSEXESVC.exe"
```

**PsExec Execution (services.exe spawning unusual processes):**
```udm
metadata.event_type = "PROCESS_LAUNCH" AND
principal.process.file.full_path = "C:\\Windows\\System32\\services.exe" AND
target.process.file.full_path NOT IN @known_services  // Replace with your Chronicle reference list
```

**WMI Process Creation:**
```udm
metadata.event_type = "PROCESS_LAUNCH" AND
principal.process.file.full_path = "C:\\Windows\\System32\\wbem\\WmiPrvSE.exe" AND
target.process.file.full_path IN ("cmd.exe", "powershell.exe")
```

**WMI Remote Execution:**
```udm
metadata.event_type = "PROCESS_LAUNCH" AND
principal.process.command_line CONTAINS "wmic" AND
principal.process.command_line CONTAINS "/node:" AND
principal.process.command_line CONTAINS "process call create"
```

**PowerShell WMI Methods:**
```udm
metadata.event_type = "PROCESS_LAUNCH" AND
target.process.file.full_path CONTAINS "powershell.exe" AND
(target.process.command_line CONTAINS "Invoke-WmiMethod" OR
 target.process.command_line CONTAINS "Invoke-CimMethod")
```

Combine with `TARGET_SCOPE_QUERY` if provided.

### Step 3: Execute SIEM Searches

```
secops-mcp.search_security_events(text=query, hours_back=TIME_FRAME_HOURS)
```

Run each developed query.

### Step 4: Network Correlation

If suspicious process activity found, correlate with network:

```udm
metadata.event_type = "NETWORK_CONNECTION" AND
target.port = 445 AND
target.ip = "TARGET_IP" AND      // Replace with actual target IP from findings
principal.ip = "SOURCE_IP"       // Replace with actual source IP from findings
```

Look for SMB connections temporally correlated with remote execution.

### Step 5: Analyze Results

Look for anomalous patterns:
- PsExec/WMI from unexpected sources (user workstations vs. admin servers)
- Execution targeting many hosts rapidly
- Suspicious commands executed via WMI
- Temporal correlation between network connections and remote process execution

### Step 6: Enrich Findings

If suspicious activity found:

For each suspicious entity (host, user):
```
secops-mcp.lookup_entity(entity_value=ENTITY)
```

For any discovered IOCs:
Use `/enrich-ioc`

### Step 7: Check Related Cases

Use `/find-relevant-case` with suspicious entities.

### Step 8: Document & Conclude

Use `/document-in-case`:
- Hunt hypothesis
- Techniques hunted (T1021.002, T1047, etc.)
- Queries used (with results)
- **Negative results explicitly noted**
- Suspicious findings with enrichment
- Suggested follow-on actions

**If lateral movement confirmed:**
→ Trigger `case_event_timeline_and_process_analysis` for affected processes
→ Trigger `compromised_user_account_response` for involved users
→ Escalate to incident response

## Required Outputs

**After completing this skill, you MUST report these outputs:**

| Output | Description |
|--------|-------------|
| `FINDINGS` | Detected lateral movement activity (events, processes, connections) |
| `DETECTED_TECHNIQUES` | MITRE techniques observed (e.g., T1021.002, T1047) |
| `AFFECTED_HOSTS` | Hosts involved in lateral movement (source and target systems) |

## Key Indicators

| Technique | Indicator | Query Focus |
|-----------|-----------|-------------|
| PsExec | PSEXESVC.exe service | Service installation events |
| PsExec | services.exe spawning | Process parent-child |
| WMI | WmiPrvSE.exe spawning | Process parent-child |
| WMI | wmic /node: | Command line |
| General | SMB port 445 | Network connections |
