---
name: powerskills-system
description: Windows system commands and info via PowerShell. Execute shell commands, get system info (hostname, OS, uptime), list top processes, read environment variables. Use when needing to run commands, check system status, or inspect the Windows environment.
license: MIT
metadata:
  author: aloth
  cli: powerskills
  parent: powerskills
---

# PowerSkills — System

Shell commands, process management, system info.

## Requirements

- PowerShell 5.1+

## Actions

```powershell
.\powerskills.ps1 system <action> [--params]
```

| Action | Params | Description |
|--------|--------|-------------|
| `exec` | `--command "whoami" [--timeout 30]` | Run a PowerShell command |
| `info` | | System info: hostname, OS, user, domain, arch, uptime |
| `processes` | `--limit N` | Top processes by CPU (default: 20) |
| `env` | `--name PATH` | Get environment variable value |

## Examples

```powershell
# Run a command
.\powerskills.ps1 system exec --command "Get-Process | Select -First 5"

# System info
.\powerskills.ps1 system info

# Top 10 CPU consumers
.\powerskills.ps1 system processes --limit 10

# Check an env var
.\powerskills.ps1 system env --name COMPUTERNAME
```

## Output Fields

### info
`hostname`, `user`, `domain`, `os`, `arch`, `ps_version`, `uptime_hours`

### processes
`name`, `pid`, `cpu`, `mem_mb`

### exec
`stdout`, `stderr`, `exit_code`
