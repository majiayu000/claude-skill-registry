---
name: shared-auxiliary-scripts
description: Auxiliary script management rules for Ralph agents. Use proactively when creating helper scripts in .claude/session/.
category: infrastructure
tags: [scripts, auxiliary, automation, cleanup]
dependencies: [shared-file-permissions, shared-ralph-core]
---

# Auxiliary Script Management

> "Auxiliary scripts help with automation – temporary scripts auto-cleanup after 1 hour."

## When to Use This Skill

Use **when**:
- Creating helper scripts in `.claude/session/`
- Managing script cleanup and retention
- Understanding script classification

Use **proactively**:
- Document reusable scripts in AGENT.md
- Use descriptive naming for scripts

---

## Quick Start

<examples>
Example 1: Script classification
```
*.runner.ps1           → Temporary (auto-deleted after 1 hour)
msg-*-*.json           → Temporary (auto-deleted after 1 hour)
{agent}-{purpose}.ps1  → Reusable (persist across sessions)
```

Example 2: Reusable script template
```powershell
# Script: developer-deployment.ps1
# Purpose: Deploy build artifacts to staging
# Created: 2026-01-23
# Used by: developer

param([string]$Environment)

# Script logic here
```

Example 3: Adding to config
```powershell
$Script:AuxiliaryScripts.Reusable = @{
    "developer-deployment.ps1" = @{
        Purpose = "Deploy build artifacts"
        Created = "2026-01-23"
        UsedBy = @("developer")
    }
}
```
</examples>

---

## Script Classification

| Classification | Pattern | Retention |
|---------------|---------|-----------|
| **Temporary** | `*-runner.ps1`, `msg-*-*.json`, `*.exit`, `*.tmp` | Auto-deleted after 1 hour |
| **Reusable** | Documented in AGENT.md | Persist across sessions |
| **Unknown** | Everything else | Manual cleanup required |

---

## Temporary Scripts

Auto-cleaned after 1 hour:
- `*-runner.ps1` - Agent runner scripts
- `msg-*-*.json` - Message files
- `*.exit` - Agent exit status files
- `restart-flag-*.json` - Restart signal files
- `*.tmp` - Temporary files

**Do NOT rely on these persisting.**

---

## Creating Reusable Scripts

1. **Document it** in AGENT.md "Reusable Scripts" section
2. **Use descriptive naming**: `{agent}-{purpose}.ps1`
3. **Add to ralph-config.ps1** under `AuxiliaryScripts.Reusable`
4. **Explain purpose** for future sessions

**Template:**
```powershell
# Script: {AGENT}-{PURPOSE}.ps1
# Purpose: {Brief description}
# Created: {DATE}
# Used by: {Which agents}

param([string]$SomeParameter)
# Script logic
```

---

## Documentation in AGENT.md

| Script | Purpose | Usage |
|--------|---------|-------|
| _(none yet)_ | | |

Update this table when creating new reusable scripts.

---

## Script Permissions

- All scripts in `.claude/session/` executable by agents
- Never create scripts that modify source code without task assignment
- Scripts should only update session/state files

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `shared-file-permissions` | File write permissions |
| `shared-context-management` | Context reset procedures |
