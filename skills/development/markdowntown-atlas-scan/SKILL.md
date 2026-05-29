---
name: markdowntown-atlas-scan
description: Atlas Simulator scan flow and next-step guidance for markdowntown. Use when working on folder scanning, tool detection, cwd handling, results panels, or scan-to-workbench CTAs.
---

# markdowntown-atlas-scan

## Core workflow
1. Confirm entry points to `/atlas/simulator` and the primary scan action.
2. Validate tool detection and cwd behavior for ancestor-scanning tools.
3. Ensure results highlight missing/loaded files and scan metadata.
4. Keep the Next steps panel prominent and action-oriented.
5. Route users into Workbench with scan context intact.

## Guardrails
- Scans are local-only; do not upload file contents.
- Handle permission errors, empty scans, and truncated scans with clear copy.
- Prefer one primary CTA per results state.

## References
- docs/atlas/simulator.md
- docs/atlas/scan-next-steps.md
- docs/architecture/atlas-simulator-flow.md
- docs/ui/scan-flow.md
- codex/skills/markdowntown-atlas-scan/references/atlas-docs.md
- codex/skills/markdowntown-atlas-scan/references/atlas-source.md
