---
name: codex-app-automation-triage
description: Consolidate Codex macOS app automation worktrees and surface actionable changes. Use for morning triage and to review recommended automations.
metadata:
  short-description: Codex App automation consolidation
---

# Codex App Automation Triage

Use this skill to consolidate Codex macOS app automation output and separate signal from noise.

## Quick start

From repo root:

```bash
python3 scripts/ops/codex_automation_report.py
```

This writes a Markdown report to `docs/reports/automation/` and prints the path.

## What to do with the report

For each worktree with **signal**:

1. Inspect:
   ```bash
   git -C <worktree> status -sb
   git -C <worktree> diff
   ```
2. Decide:
   - **Keep**: cherry-pick or copy into your active branch
   - **Discard**: ignore or delete the worktree

## Other suggested automations

The project’s recommended automations and copy‑paste prompts are documented in:

- `docs/tools/CODEX_APP.md` → “Automation Prompts (Copy‑Paste Ready)”

If you need the prompts inline, open:

- `references/automation-prompts.md`
