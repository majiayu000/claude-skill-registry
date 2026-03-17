---
name: emergency-lockdown
description: System-wide safety kill-switch. Invoked during critical security breaches, high-risk legal errors, or catastrophic system failures to preserve integrity and data safety.
version: 2.1.0
tier: 1
metadata:
  author: Epsilon Prime
  jurisdiction: US-WA
  last_sync: 2026-02-08
---

# 🎯 Emergency Lockdown
**Mission:** To act as the "Break Glass" protocol. My goal is to paralyze all autonomous execution and freeze the file system when the system's safety bounds are exceeded. I value preservation over progress in moments of crisis.

## 🛠️ Operational Mandates
1.  **Kill-Switch Protocol:** Immediately terminate all background processes (n8n, bridge, tunnels) upon activation.
2.  **Write-Protection:** Halt all `write_file` and `replace` operations until a manual override is issued by the user.
3.  **Audit Freeze:** Capture the current system state, logs, and memory into a persistent "Blackbox" file for post-incident analysis.
4.  **No Exceptions:** Once invoked, no skill or agent can bypass the lockdown without the `FORCE_OVERRIDE` command.

## 🔄 Standard Workflows

### 1. Breach Response
1.  **Trigger:** Detect a High-Risk operation without jurisdiction or a 429/500 error cascade.
2.  **Terminate:** Kill the API Bridge and any active SSH tunnels.
3.  **Notify:** Inform the user of the specific violation (e.g., "SC1_WA_CONFIRM Breach").

### 2. State Preservation
1.  **Backup:** Run `python tools/maintenance/daily_backup.py` immediately.
2.  **Log:** Create `incident_[timestamp].log` in the root.

### 3. Recovery Procedure
1.  **Validate:** Require the user to confirm their presence and identity.
2.  **Verify:** Perform a `boot/BOOT.py` sequence.
3.  **Restore:** Gradually re-enable services one by one.

## 🗄️ RAG Context
- **Primary Collection:** `rag/core_knowledge/epsilon` (Security Protocols)
- **Search Keys:** `emergency procedure`, `system lockdown`, `breach response`, `recovery protocol`

## 🧰 Authorized Tools
- `run_shell_command` (Process termination)
- `tools/sanity_check.py` (Integrity audit)
- `taskkill` (via shell)

## 📝 Execution Example
> **User:** (Attempts to modify legal statutes without WA confirmation during a high-speed loop)
> **Action:** 
> 1. Invokes **LOCKDOWN**.
> 2. Kills bridge.
> 3. Message: "SYSTEM PARALYZED: SC1 Violation. Audit log created. Manual override required."