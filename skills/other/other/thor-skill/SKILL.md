---
name: thor-skills
description: Entry point and router for THOR-related work: running scans, analyzing THOR logs, troubleshooting THOR behavior, maintaining THOR installs, THOR Lens workflows, writing THOR plugins (v11+), and creating custom signatures/IOCs.
---

# THOR Skills

This is the root skill. It routes requests to the right sub-skill and enforces a few global rules.

Global rules
- Don't invent THOR flags or behavior. If something is unclear, ask for the missing detail instead of guessing.
- Prefer reproducible commands: explicit paths, explicit output directory, explicit mode.
- Keep changes safe: don't recommend deleting evidence or modifying the target system unless the user explicitly asks.
- Default focus is forensic / lab workflows. If it's live endpoint scanning, call that out and keep it conservative.
- THOR versions: v10 is stable; v11 is TechPreview. Some features are v11-only. In particular, THOR Lens relies on the audit trail output, which requires THOR v11 and is not available in THOR v10.
- THOR Lite vs full THOR: Lite is a free scanner with reduced features (~5 modules, ~4k open source signatures, no Sigma, no lab mode, no audit trail). Identify which version the user has before troubleshooting missing features.

## Routing rules

- If the user wants to run a scan or asks "what command should I run" - use thor-scan (also covers THOR Lite scanning with appropriate flag adjustments).
- If the user pasted results or asks "what does this finding mean" - use thor-log-analysis.
- If the user reports hangs, slowness, crashes, missing output, license/update weirdness - use thor-troubleshooting.
- If the user asks about update/upgrade/report generation/yara-forge/offline packs - use thor-maintenance.
- If the user asks about THOR Lens, forensic timeline viewing, importing audit trails, or MCP integration for timeline analysis - use thor-lens (note: requires full THOR v11, not compatible with THOR Lite).
- If the user asks about thor10.db/thor11.db, scan timing, performance tuning, slow rules, or resume state - use thor-db.
- If the user asks why a feature is missing, expects full THOR behavior from Lite, or asks about Lite limitations - use thor-lite.
- If the user wants to write a plugin, extend THOR functionality, parse custom formats, or asks about the plugin API - use thor-plugins (requires THOR v11+).
- If the user wants to create custom IOCs, YARA rules, Sigma rules, STIX indicators, or asks about the custom-signatures folder - use custom-signatures.

## Minimum inputs to collect (only what's needed)

- OS (Windows/Linux/macOS)
- THOR version (v10 or v11) and install path
- License situation if relevant (lab vs standard vs unknown)
- Target type: live path vs mounted image vs memory dump vs log-only analysis
- Where outputs/logs should go

## Available Skills

- [thor-scan/](thor-scan/) - Run THOR scans and produce the exact command line for the target scenario
- [thor-log-analysis/](thor-log-analysis/) - Triage and interpret THOR logs and findings
- [thor-troubleshooting/](thor-troubleshooting/) - Diagnose stuck/slow/failed THOR runs and recommend next actions
- [thor-maintenance/](thor-maintenance/) - Update/upgrade THOR, manage signature packs, generate reports
- [thor-lens/](thor-lens/) - THOR Lens forensic timeline viewer; import audit trails, web UI, MCP integration (requires THOR v11)
- [thor-db/](thor-db/) - Analyze ThorDB (thor10.db/thor11.db) for performance tuning and diagnostics
- [thor-lite/](thor-lite/) - THOR Lite limitations, workarounds, and guidance for the free scanner
- [thor-plugins/](thor-plugins/) - Write custom THOR plugins to extend scanner functionality (requires THOR v11+)
- [custom-signatures/](custom-signatures/) - Create custom IOCs, YARA rules, Sigma rules, and STIX indicators
