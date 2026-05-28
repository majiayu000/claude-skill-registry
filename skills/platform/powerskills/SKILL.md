---
name: powerskills
description: Windows automation toolkit for AI agents. Provides Outlook email/calendar, Edge browser (CDP), desktop screenshots/window management, and shell commands via PowerShell. Install this for the full suite, or install individual sub-skills (powerskills-outlook, powerskills-browser, powerskills-desktop, powerskills-system) separately.
license: MIT
metadata:
  author: aloth
  cli: powerskills
---

# PowerSkills

Windows capabilities for AI agents via PowerShell. Each skill in `skills/` is independently discoverable.

## Setup

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Usage

```powershell
.\powerskills.ps1 <skill> <action> [--param value ...]
.\powerskills.ps1 list                          # Discover available skills
.\powerskills.ps1 outlook inbox --limit 10       # Run an action
```

## Output Format

All actions return JSON:

```json
{"status": "success", "exit_code": 0, "data": {...}, "timestamp": "..."}
```

## Configuration

Edit `config.json`:

```json
{
  "edge_debug_port": 9222,
  "default_timeout": 30,
  "outlook_body_max_chars": 5000
}
```

## Skills

| Skill | Description |
|-------|-------------|
| [outlook](skills/outlook/SKILL.md) | Email & calendar via Outlook COM |
| [browser](skills/browser/SKILL.md) | Edge automation via CDP |
| [desktop](skills/desktop/SKILL.md) | Screenshots, window management, keystrokes |
| [system](skills/system/SKILL.md) | Shell commands, processes, system info |
