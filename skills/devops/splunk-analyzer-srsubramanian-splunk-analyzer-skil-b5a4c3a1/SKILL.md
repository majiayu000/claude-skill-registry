---
name: splunk-analyzer
description: Automate Splunk queries and analyze results using Chrome DevTools MCP. Use when the user wants to run Splunk searches, export log data, or analyze Splunk results. Triggers on requests like "check error rates", "search Splunk for X", "run a Splunk query", "analyze logs from Splunk", or "find errors in payment-service".
---

# Splunk Analyzer

Automate Splunk searches via browser and analyze exported results.

## Configuration

```
SPLUNK_URL: https://your-splunk-instance.com
```

## Workflow

### 1. Navigate to Splunk

```
Navigate to: {SPLUNK_URL}/en-US/app/search/search
```

If login page appears, inform user: "Please authenticate in the browser. Let me know when you're logged in."

### 2. Build SPL Query

Convert natural language to SPL. See [references/spl-patterns.md](references/spl-patterns.md) for patterns.

**Query structure:**
```spl
index=<index> sourcetype=<sourcetype> <filters> | <transformations>
```

If user provides raw SPL, use it directly.

### 3. Execute Search

See [references/splunk-ui.md](references/splunk-ui.md) for UI selectors.

1. Find search bar (textarea with `data-test="search-bar"` or class `ace_text-input`)
2. Clear existing text, enter SPL query
3. Click search button (button with `data-test="search-button"` or "Search" text)
4. Wait for results (watch for "X events" or results table)

### 4. Export Results

1. Click "Export" button above results
2. Select "Raw" format
3. Set filename, click "Export"
4. Wait for download to complete

### 5. Analyze Results

Run analysis script on exported file:

```bash
python3 scripts/analyze_splunk.py <exported_file> [--charts]
```

**Analysis includes:**
- Event count and time range
- Top error patterns / log levels
- Field value distributions
- Anomaly detection (spikes, unusual values)
- Trend visualization (with `--charts`)

## Quick Reference

| User Request | Action |
|--------------|--------|
| "Check errors in service X" | `index=* "error" source="*X*" \| stats count by message` |
| "Show me logs from last hour" | `index=* earliest=-1h` |
| "Find slow requests" | `index=* duration>1000 \| stats avg(duration) by endpoint` |
| "Summarize today's exceptions" | Run query + full analysis with charts |