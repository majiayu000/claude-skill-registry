---
name: windows-remote
description: Windows remote administration via PowerShell over SSH tunnel for filesystem and service operations
---

# Windows Remote Admin Skill (PowerShell via VPS Tunnel)

This skill provides Windows remote administration capabilities via PowerShell commands executed over SSH reverse tunnels.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Scope

- Filesystem operations on Windows hosts
- Service management on Windows hosts
- Executed via SSH to localhost ports (reverse tunnels from Windows workers)

## Architecture

```
[Claude] --> [VPS localhost:PORT] --> [SSH Reverse Tunnel] --> [Windows Host]
```

Windows workers establish reverse SSH tunnels to the VPS, exposing their SSH/PowerShell endpoint on a specific localhost port.

## Command Format

```bash
ssh -p <port> <user>@localhost powershell -Command "<powershell-command>"
```

## Command Allowlist

### Filesystem Operations

```powershell
Get-ChildItem <path>
Copy-Item <source> <destination>
Remove-Item <path>
New-Item <path> -ItemType <type>
Get-Content <file>
Set-Content <file> -Value <content>
Test-Path <path>
```

### Service Operations

```powershell
Get-Service <name>
Get-Service                          # List all services
Restart-Service <name>
Stop-Service <name>
Start-Service <name>
```

### Event Log Access

```powershell
Get-EventLog -LogName <log> -Newest <n>
Get-WinEvent -LogName <log> -MaxEvents <n>
```

## Policies

### Tunnel Verification

- Only use known tunnel ports and hostnames
- Never connect to arbitrary ports or hosts
- Verify worker configuration before connecting

### Forbidden Operations

The following are **strictly forbidden**:

- Domain/Active Directory management commands
- User account management (`New-LocalUser`, `Remove-LocalUser`, etc.)
- Group policy modifications
- System reboots (`Restart-Computer`) - unless **explicitly requested**
- Registry modifications
- Windows Update operations
- Firewall rule changes

### Reboot Policy

System reboots require:

1. Explicit user request containing the word "reboot" or "restart"
2. Confirmation of which worker to reboot
3. Verification that user understands the impact

## Workflow Examples

### Connect to a Worker

```bash
# Connect and list files
ssh -p 2222 admin@localhost powershell -Command "Get-ChildItem C:\Apps"
```

### Check Service Status

```bash
# Using the helper script: ./scripts/win_ps.sh <port> <user> <command>
./scripts/win_ps.sh 2222 admin "Get-Service MyAppService"
```

### Restart a Windows Service

```bash
# 1. Check current status
./scripts/win_ps.sh 2222 admin "Get-Service MyAppService"

# 2. View recent events
./scripts/win_ps.sh 2222 admin "Get-EventLog -LogName Application -Newest 20"

# 3. Restart service
./scripts/win_ps.sh 2222 admin "Restart-Service MyAppService"

# 4. Verify restart
./scripts/win_ps.sh 2222 admin "Get-Service MyAppService"
```

### List All Services

```bash
./scripts/win_ps.sh 2222 admin "Get-Service | Format-Table -AutoSize"
```

### Copy Files

```bash
./scripts/win_ps.sh 2222 admin "Copy-Item 'C:\Apps\config.bak' 'C:\Apps\config.json'"
```

## Helper Scripts

- `scripts/win_ps.sh` - Execute PowerShell commands via SSH tunnel

## Error Handling

Common issues and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Tunnel not active | Check if worker tunnel is up |
| Permission denied | Auth failure | Verify SSH user configuration |
| Service not found | Wrong service name | Use `Get-Service` to list services |
| Access denied | Insufficient privileges | May need admin account |
