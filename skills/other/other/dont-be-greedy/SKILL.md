---
name: dont-be-greedy
description: |
  When a user uploads or references a data file (CSV, JSON, XLSX, TXT, LOG) or any
  file larger than 100KB, immediately estimate token cost using scripts/estimate_size.py.
  If >30k tokens, chunk the file and summarize each chunk. If smaller, run quick inspection.
  Return a safe preview and summary without asking the user what to do.
allowed-tools: |
  bash: python, cat, head, tail, wc, ls, file
  file: read
---

# Don't Be Greedy

<purpose>
Prevents context overflow by enforcing size-aware data loading. Large files can
exceed context windows and crash agent workflows. This skill measures files before
loading, chunks oversized data, and returns compact summaries with safe previews
so downstream processing can continue without context exhaustion.
</purpose>

## Instructions

### Step 1: Estimate Token Cost

Before loading ANY data file:

```bash
python scripts/estimate_size.py "<file_path>"
```

This returns byte count and estimated token count.

### Step 2: Apply Strategy Based on Size

| Estimated Tokens | Action |
|------------------|--------|
| < 10,000 | Run quick inspection, load directly |
| 10,000 - 30,000 | Run quick inspection, consider filtering |
| > 30,000 | Chunk and summarize before loading |

### Step 3: Execute Appropriate Workflow

<strategy name="small-file">
For files under 10k tokens:

```bash
python scripts/quick_inspect.py "<file_path>"
```

Return stats and load file directly.
</strategy>

<strategy name="large-file">
For files over 30k tokens:

```bash
python scripts/chunker.py "<file_path>"
python scripts/summarize.py "<chunk_file>"
```

Return overall summary + per-chunk summaries + safe preview of first rows.
</strategy>

### Step 4: Return Structured Output

Always provide:
- Overall summary (1-3 paragraphs)
- Safe preview (first N rows/lines)
- Recommendation for next steps
- Chunk information if file was split

## NEVER

- Load files without running estimate_size.py first
- Use `cat` on unknown or large files
- Ask "What would you like me to do with this file?"
- Wait for user direction before acting on file uploads
- Load raw data exceeding 30k tokens into context

## ALWAYS

- Run size estimation before any file operation
- Chunk files over 30k tokens automatically
- Provide a safe preview even for large files
- Act immediately when a data file is detected
- Be thorough in first response with summary + preview + recommendation

## Examples

### Example 1: User uploads large CSV

**Input:** User says "Analyze this sales data" and uploads a 50MB CSV file

**Workflow:**
1. Run `scripts/estimate_size.py sales.csv` → Output: `bytes=52428800 (50.0MB) tokens=13107200`
2. Way over 30k tokens. Run `scripts/chunker.py sales.csv` → Creates 6500+ chunks
3. Run `scripts/summarize.py` on representative chunks
4. Return:
   - Overall summary of data structure and content
   - Safe preview showing first 10 rows
   - Recommendation: "Data contains 1M rows of sales transactions. I've chunked it for processing. Want me to analyze specific columns or date ranges?"

### Example 2: User references small JSON config

**Input:** User asks "Check my config.json for issues"

**Workflow:**
1. Run `scripts/estimate_size.py config.json` → Output: `bytes=2048 (2.0KB) tokens=512`
2. Under 10k tokens. Run `scripts/quick_inspect.py config.json`
3. Load file directly and analyze
4. Return: Full analysis with any issues found

### Example 3: User uploads medium log file

**Input:** User uploads a 500KB application.log

**Workflow:**
1. Run `scripts/estimate_size.py application.log` → Output: `bytes=512000 (500.0KB) tokens=128000`
2. Over 30k tokens. Run `scripts/chunker.py application.log`
3. Summarize chunks focusing on errors and warnings
4. Return:
   - Summary of log timespan and key events
   - Count of errors, warnings, info messages
   - Safe preview of recent entries
   - Recommendation for focused analysis
