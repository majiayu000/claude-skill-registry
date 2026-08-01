---
name: hs-risk
description: 'description: Data-only HS risk scoring (format/missing/haz/oog flags)
  with markdown report'
---

﻿---
name: hs-risk
description: Data-only HS risk scoring (format/missing/haz/oog flags) with markdown report
---
Instructions:
- Input: data/items.csv (use data/templates/items.template.csv)
- Run: powershell -ExecutionPolicy Bypass -File .codex/skills/hs-risk/scripts/run.ps1
- Output: reports/hs_risk.md
- Fail-safe: if inputs/columns missing, output only the '以묐떒' table.
Evidence Required:
- Report must include counts by tier and a ranked table with reasons.
