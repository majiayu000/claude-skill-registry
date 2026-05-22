---
name: xan
description: High-performance CSV processing with xan CLI for large tabular datasets, streaming transformations, and low-memory pipelines.
---

# xan

Use this skill when tabular work involves large CSV-like files and shell-oriented data pipelines.

## When to Use

- CSV/TSV files are large (size or rows) and Python/pandas style processing is too heavy.
- You need fast CLI operations such as `filter`, `sort`, `dedup`, `groupby`, `frequency`, `join`.
- You want low-memory streaming workflows in terminal pipelines.

## Boundaries

- Not for workbook semantics (`.xlsx` formula/layout preservation) — use `xlsx` or `excel-analysis`.
- Not for ML model training pipelines — use `data-ml` skills.
- This skill is a thin CLI wrapper; it does not implement custom parsing logic itself.

## Script

- Path: `scripts/xan.ps1`

### Examples

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\xan\scripts\xan.ps1" count data.csv
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\xan\scripts\xan.ps1" filter "score > 0.8" data.csv
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\xan\scripts\xan.ps1" groupby category "sum(amount) as total" sales.csv
```
