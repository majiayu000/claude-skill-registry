---
name: etl-duckdb
description: 'description: Load CSV/XLSX into DuckDB with validation and an ETL markdown
  report'
---

﻿---
name: etl-duckdb
description: Load CSV/XLSX into DuckDB with validation and an ETL markdown report
---
Instructions:
- Run: powershell -ExecutionPolicy Bypass -File .codex/skills/etl-duckdb/scripts/run.ps1
- Output:
  - data/_artifacts/ops.duckdb
  - reports/etl_report.md
Fail-safe:
- If inputs missing, produce only the '以묐떒' table in reports/etl_report.md and exit.
Evidence Required:
- input_rows, null_cells, duplicated_rows, duckdb_written
