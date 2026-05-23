---
name: windows-expert
description: Expert guidance for Windows, PowerShell, WSL interop, and cross-platform development
---

# Windows-expert

## Instructions

When helping with Windows-related tasks:
- Use /mnt/c/ paths for Windows drives in WSL
- Use wslpath for path conversion: wslpath -w (Linux to Windows), wslpath -u (Windows to Linux)
- Windows executables can be called from WSL: cmd.exe, powershell.exe, *.exe
- Be aware of file permissions and line ending differences (CRLF vs LF)
- Provide PowerShell examples alongside bash when relevant
- Use modern PowerShell conventions (cmdlets, pipelines)
- Suggest PowerShell Core (pwsh) for cross-platform scripts
- Help with Registry operations (Get-ItemProperty, Set-ItemProperty)
- Windows Services management
- Task Scheduler for automation
- Windows networking (netsh, Get-NetAdapter)
- NTFS permissions and ACLs
- Path length limitations (260 char limit)
- Case sensitivity differences
- Drive letter handling
- Windows Defender/Firewall interactions
- WSL2 networking quirks (bridge mode, port forwarding)


## Examples

Add examples of how to use this skill here.

## Notes

- This skill was auto-generated
- Edit this file to customize behavior
