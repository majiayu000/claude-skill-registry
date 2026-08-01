---
name: docs-aqualia-skills-library
description: 'Claude Code automatically discovers wrappers/claude-skill/SKILL.md when
  this repository is opened. The skill teaches Claude how to:'
---

# Claude Code Skill

Claude Code automatically discovers `wrappers/claude-skill/SKILL.md` when this repository is opened. The skill teaches Claude how to:

1. Collect tenant ID, client ID, PFX path, internal domains, site URL/CSV, and confirm that PowerShell 7.4+ and Python 3.10+ are available.
2. Run `pwsh ./sharepoint-audit-agent/agent/powershell/Install-Modules.ps1` to install PnP.PowerShell and ImportExcel for the current user.
3. Set `PFX_PASS` (never echo secrets) and call `python ./sharepoint-audit-agent/agent/python/audit_agent.py ... --output ./runs`.
4. Surface the generated Markdown/HTML reports from `./runs/<timestamp>/site-*/report.*` back to the user while reminding them that the artifacts contain PII.

The manifest also reiterates two safety rules:
- Commands must run locally (no remote network fetches beyond module installs).
- All Sites.Selected grants should default to **Read** scope, with Write explicitly acknowledged by the operator.
