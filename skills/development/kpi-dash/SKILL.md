---
name: kpi-dash
description: 'description: Generate weekly KPI report (3PL/WMS) from shipments/events'
---

﻿---
name: kpi-dash
description: Generate weekly KPI report (3PL/WMS) from shipments/events
---
Instructions:
- Run: powershell -ExecutionPolicy Bypass -File .codex/skills/kpi-dash/scripts/run.ps1
- Input: data/shipments.csv, data/events.csv
- Output: reports/weekly_kpi.md
Fail-safe:
- If inputs/columns missing, output only the '以묐떒' table in reports/weekly_kpi.md and exit.
Evidence Required:
- Unique shipments, OTIF%(proxy if needed), Avg dwell days, DEM/DET risk flags
