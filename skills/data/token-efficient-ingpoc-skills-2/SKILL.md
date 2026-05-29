---
name: token-efficient
description: "Use when processing 50+ items, analyzing CSV/log files, executing code in sandbox, or searching for tools. Load for data processing tasks. Achieves 98%+ token savings via in-sandbox execution, progressive disclosure, and pagination. Supports heredocs for multi-line bash."
keywords: csv, logs, execute, sandbox, pagination, batch, filter, aggregate
---

# Token-Efficient MCP

Process data in sandbox, return only results. 98%+ token savings.

## Instructions

1. Search for tool: `search_tools("csv")` (95% savings vs loading all)
2. Process data in sandbox (never load raw to context)
3. Use pagination for large files: `offset`, `limit`
4. Return summaries, not raw data

## Quick Commands

```bash
# Process CSV with filter
scripts/process-csv.sh data.csv "price > 100"

# Search logs for errors
scripts/search-logs.sh app.log "ERROR|WARN"

# Execute code in sandbox
scripts/run-sandbox.sh script.py
```

## Token Savings

| Tool | Savings | Example |
|------|---------|---------|
| `execute_code` | 98%+ | Run Python without loading |
| `process_csv` | 99% | 10K rows → 100 results |
| `process_logs` | 95% | 100K lines → 500 matches |
| `search_tools` | 95% | Find tools on-demand |

## MCP Tools

| Tool | Purpose |
|------|---------|
| `execute_code` | Python/Bash/Node in sandbox |
| `process_csv` | Filter, aggregate CSV |
| `process_logs` | Pattern match logs |
| `search_tools` | Find tools by keyword |
| `batch_process_csv` | Multiple CSVs at once |

## References

| File | Load When |
|------|-----------|
| references/patterns.md | Choosing which tool |
| references/examples.md | Need code examples |
