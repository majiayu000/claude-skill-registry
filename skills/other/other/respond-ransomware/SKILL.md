---
name: respond-ransomware
description: "Respond to a ransomware incident following PICERL methodology. Use when ransomware is detected or suspected. Orchestrates identification, containment, eradication, and recovery phases. Requires CASE_ID and initial indicators."
required_roles:
  chronicle: roles/chronicle.admin
  soar: roles/chronicle.soarAdmin
  gti: GTI Enterprise
  scc: roles/securitycenter.adminEditor
personas: [incident-responder]
---

# Ransomware Incident Response Skill

Structured workflow for responding to suspected ransomware incidents using the PICERL model.

## Inputs

- `CASE_ID` - SOAR case ID for the incident
- `ALERT_GROUP_IDENTIFIERS` - Alert group identifiers from SOAR
- `INITIAL_INDICATORS` - Initial detection info:
  - Affected endpoint(s)
  - File hashes observed
  - Ransom note details (handle carefully)
  - Suspicious network connections

## Required Outputs

**After completing each phase, you MUST report these outputs:**

### Identification Phase
| Output | Description |
|--------|-------------|
| `AFFECTED_SYSTEMS` | Systems confirmed infected with ransomware |
| `RANSOMWARE_VARIANT` | Ransomware family/variant identified |
| `ENCRYPTION_STATUS` | Current encryption state of affected systems |
| `RANSOMWARE_IOCS` | File hashes, ransom note patterns, malicious files |

### Containment Phase
| Output | Description |
|--------|-------------|
| `ISOLATED_SYSTEMS` | Systems successfully isolated from network |
| `BLOCKED_IOCS` | IOCs blocked at firewall/proxy |
| `C2_INDICATORS` | C2 domains/IPs discovered during containment |

### Eradication Phase
| Output | Description |
|--------|-------------|
| `CLEANED_SYSTEMS` | Systems with malware/persistence removed |
| `REMOVED_PERSISTENCE` | Persistence mechanisms identified and removed |

### Recovery Phase
| Output | Description |
|--------|-------------|
| `RESTORED_SYSTEMS` | Systems restored to operational state |
| `VALIDATION_STATUS` | Post-recovery validation results |

## PICERL Phases

### Phase 1: Preparation (Ongoing)
*Prerequisites - verify before proceeding:*
- Tool connectivity (SIEM, SOAR, GTI, EDR)
- Backup availability and status
- Communication/escalation plans

---

### Phase 2: Identification

**Step 2.1: Get Context**
```
secops-soar.get_case_full_details(case_id=CASE_ID)
```

Use `/check-duplicates` to verify this isn't already under investigation.

**Step 2.2: Identify Ransomware Strain**

If file hash available:
```
gti-mcp.get_file_report(hash=FILE_HASH)
```

If name/family known:
```
gti-mcp.search_threats(query="LockBit ransomware", collection_type="malware-family")
```

Document: `IDENTIFIED_STRAIN`

**Step 2.3: Investigate Initial Access & Lateral Movement**

Search SIEM for activity BEFORE encryption:
```
secops-mcp.search_security_events(
    text="Suspicious logins, RDP, exploit attempts for affected endpoints",
    hours_back=168
)
```

Look for:
- Suspicious logins to affected endpoints
- Lateral movement tools (PsExec, Cobalt Strike)
- Credential dumping activity
- Network connections from affected endpoints

Identify: `INITIAL_ACCESS_VECTOR`, `POTENTIAL_ADDITIONAL_SYSTEMS`

**Step 2.4: Initial Scope Assessment**

Compile:
- `AFFECTED_ENDPOINTS` - Confirmed infected systems
- `MALICIOUS_IOCs` - Network IOCs (C2 domains/IPs)

**Step 2.5: Check Related Cases**

Use `/find-relevant-case` with affected entities.

**Step 2.6: Document**

Use `/document-in-case` with identification findings.

---

### Phase 3: Containment

**CRITICAL: Speed is essential. Contain first, investigate deeper later.**

**Step 3.1: Isolate Affected Endpoints**

For each endpoint in `AFFECTED_ENDPOINTS` and `POTENTIAL_ADDITIONAL_SYSTEMS`:

Use `/confirm-action`:
> "Isolate endpoint [HOSTNAME] from network?"

If confirmed, trigger endpoint isolation (via EDR or network).

**Step 3.2: Block Network IOCs**

For each IOC in `MALICIOUS_IOCs`:

Use `/confirm-action`:
> "Block IOC [VALUE] at firewall/proxy?"

If confirmed, implement blocks.

**Step 3.3: Contain User Accounts**

If compromised user identified:
→ Trigger `/respond-compromised-account`

**Step 3.4: Verify Containment**

Monitor SIEM for continued activity:
```
secops-mcp.search_security_events(
    text="Activity from contained systems or IOCs",
    hours_back=1
)
```

Use `/document-in-case` with containment status.

---

### Phase 4: Eradication

**Step 4.1: Identify Persistence**

Review GTI reports for known persistence TTPs of `IDENTIFIED_STRAIN`.

Common mechanisms:
- Scheduled tasks
- Services
- Registry run keys
- WMI subscriptions

**Step 4.2: Remove Malware & Persistence**

*(Requires EDR/endpoint tools)*
- Remove ransomware executables
- Delete persistence mechanisms
- **Note:** Re-imaging often preferred over cleaning

**Step 4.3: Scan Systems**

Perform thorough AV/EDR scans on affected systems.

Use `/document-in-case` with eradication actions.

---

### Phase 5: Recovery

**Step 5.1: Check Decryptor Availability**

Based on `IDENTIFIED_STRAIN`, check:
- NoMoreRansom.org
- Security vendor decryptor tools

**Step 5.2: Determine Recovery Strategy**

Options:
1. Restore from clean backups (most common)
2. Use decryptor if available
3. Rebuild systems from scratch

**Step 5.3: Execute Recovery**

*(Involves IT Ops/System Admins)*
- Rebuild/restore systems
- Verify backup integrity before restore
- Patch and harden before reconnecting
- Restore data from clean backups

**Step 5.4: Monitor & Lift Containment**

- Monitor recovered systems closely
- Gradually remove isolation measures
- Watch for signs of residual infection

Use `/document-in-case` with recovery status.

---

### Phase 6: Lessons Learned

Use `/generate-report` with comprehensive incident report.

Conduct post-incident review:
- Initial access vector analysis
- Detection timeline review
- Response effectiveness
- Recovery success
- Recommendations for prevention

---

## Critical Warnings

- **DO NOT delay containment** to perform deep analysis
- **DO NOT restore** without verifying backups/cleaning
- **DO check for lateral movement** before closing
- **ALWAYS confirm** isolation actions with analyst

## Quick Reference

| Phase | Key Actions | Skills Used |
|-------|-------------|-------------|
| Identification | Strain ID, scope | `/check-duplicates`, `/find-relevant-case` |
| Containment | Isolate, block | `/confirm-action`, `/document-in-case` |
| Eradication | Remove persistence | EDR tools |
| Recovery | Restore systems | IT Ops coordination |
| Lessons Learned | Report, review | `/generate-report` |
