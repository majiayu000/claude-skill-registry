---
name: agentv-onboarding
description: Bootstrap AgentV in the current workspace after plugin-manager install. Ensures CLI availability, runs workspace init, and verifies setup artifacts.
---

# AgentV Onboarding

Use this skill when the user asks to set up AgentV in a repository.

## Goal

Set up AgentV in the current workspace:
- ensure the `agentv` CLI is available (install if needed)
- initialize workspace files
- verify setup artifacts and report status

## Workflow

### 1. Resolve Script Path

Find the directory that contains this `SKILL.md`, then resolve script paths relative to it.

Packaged scripts:
- `scripts/onboard-agentv.sh` for bash/zsh
- `scripts/onboard-agentv.ps1` for PowerShell

### 2. Run the Platform Script

Run from the repository root where AgentV should be initialized.

POSIX shells:

```bash
bash <skill-dir>/scripts/onboard-agentv.sh
```

PowerShell:

```powershell
pwsh -File <skill-dir>/scripts/onboard-agentv.ps1
```

If `pwsh` is unavailable on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File <skill-dir>/scripts/onboard-agentv.ps1
```

### 3. Handle Errors

If the script fails, report the exact error and stop. Do not claim setup succeeded.

### 4. Report Outcome Clearly

Summarize:
- `agentv` version in use
- whether CLI was installed during this run
- whether `agentv init` completed
- whether setup verification passed

## Re-run Behavior

Re-running is safe. The scripts run `agentv init`, and if setup artifacts are still missing they rerun once automatically before failing.
